from Models.models import ChatRooms, User, Messages
from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import JSONResponse
from datetime import datetime, timezone
from termcolor import colored
from fastapi import WebSocket, WebSocketDisconnect, WebSocketException
from Repository.database import getdb
from Serializers.Serializers import Serializer

import re



class ChatService() :


        webSockets : dict[int, WebSocket] = {}

        
        @staticmethod
        async def validateMobileNumber(mobileNumber) -> bool :
                
                regex_pattern : str = r"^[0-9]{10}$"
                match = re.search(regex_pattern,mobileNumber)

                return True if match else False
        
        @staticmethod
        async def sortChatRooms(chatrooms : list[dict]) -> list[dict] :
             
                   keyfunction = lambda chatRoom : chatRoom["lastMessageTime"]

                   return sorted(chatrooms, key= keyfunction)
         

        @staticmethod
        async def serializingChatRooms(chatRooms : list[ChatRooms], user : User) -> list[dict] :
                
                   chatContacts : list[dict] = []
                 

                   for chatRoom in chatRooms :
                                  
                        for chatuser in chatRoom.users :
                                         
                                if(not user.id == chatuser.id ) :
                                                
                                     chatContacts.append({"chatRoomId": chatRoom.id ,"chatUserId" : chatuser.id, "mobileNumber" : chatuser.mobileNo,"profileImageUrl" : chatuser.profileImageUrl,"userName" : chatuser.userName, "lastMessageTime" : (datetime.timestamp(chatRoom.lastMessageTime))})
                   
                   return chatContacts


        @classmethod
        async def addContact(cls,mobileNumber : str,userId : int,session : AsyncSession) -> JSONResponse :
                

                if(await ChatService.validateMobileNumber(mobileNumber)) :
                        

                        user_query = select(User).where(User.mobileNo == mobileNumber)
                        user_result = await session.execute(user_query)
                        user_1 = user_result.scalar_one_or_none()
                        user_query = select(User).where(User.id == userId)
                        user_result = await session.execute(user_query)
                        user_2 = user_result.scalar_one_or_none()

                        if(user_1 and user_2) :

                                # print("chat room users",chat_room.users)
                                chat_room_query = select(ChatRooms).where(ChatRooms.users.contains(user_1),ChatRooms.users.contains(user_2))
                                chat_room_result = await session.execute(chat_room_query)
                                chat_room = chat_room_result.scalar_one_or_none()
                                
                                if(chat_room) :

                        
                                        print("chat room : ",chat_room.users) 
                                
                                else :

                                        chat_room_object = ChatRooms()
                                        chat_room_object.users.append(user_1)
                                        chat_room_object.users.append(user_2)
                                        session.add(chat_room_object)
                                        await session.commit()
                                        print("chat room object : ",chat_room_object)
                        
                                if(chat_room or chat_room_object)  :
                                       
                                       response = JSONResponse({"message" : "chat room created", "success" : True},status_code=200)

                                
                        else :


                                response = JSONResponse({"message" : "user does not exist","success" : False},status_code=409)
                         

                else :
                        
                         response = JSONResponse({"message" : "Mobile Number Invalid","success" : False},status_code=409)


                return response
        

        


        @staticmethod
        async def listChatRooms(userId : int,pageOffset : int ,session : AsyncSession) -> JSONResponse :
            
            try :
                user_query = select(User).where(User.id == userId)
                user_result = await session.execute(user_query)
                user = user_result.scalar_one_or_none()
                print("user : ",user)
               
                if(not pageOffset < 0) :

                  if(user) :

                        chatRooms_query = select(ChatRooms).where(ChatRooms.users.contains(user)).limit(10).offset(pageOffset * 10)
                        chatRooms_result = await session.execute(chatRooms_query)
                        chatRooms = chatRooms_result.scalars().all()
                        
                        if(len(chatRooms) > 0) :

                           chatContacts : list[dict] = await ChatService.serializingChatRooms(chatRooms, user)
                           chatContacts = sorted(chatContacts, key =  lambda chatContact : chatContact["lastMessageTime"] )
                           chatContacts.reverse()
                           print(colored(f"chatRooms : {chatContacts}", "green", attrs=["bold"]))
                           response = JSONResponse({"message" : "chat room exists","chatContacts" : chatContacts,"success" : True},status_code=200)
                        
                        else :

                           response = JSONResponse({"message" : "chat rooms not exists","chatContacts" : [],"success" : True},status_code=200)

                  else :

                        response = JSONResponse({"message" : "user does not exists"},status_code=409)
                else :
                       
                       response = JSONResponse({"message" : "Negative Page Offset","success" : False},status_code=409)
                
                return response
           
            except Exception as e :
                   
                   print(colored(f"Error : {e}","red",attrs=["bold"]))
                   return JSONResponse({"meesage" : "Internal Server Error", "success" : False},status_code=500)
               

        @classmethod
        async def sendChat(cls, message, receiverId, senderId, chatRoomId, messageTime, id) :
               
               receiverWebSocket = cls.webSockets.get(receiverId, None)

               if(receiverWebSocket) :
                      
                      message = {"id" : id,"message" : message, "senderId" : senderId, "receiverId" : receiverId, "chatRoomId" : chatRoomId,"messageTime" : str(messageTime)}
                      await receiverWebSocket.send_json(message)



        @classmethod
        async def receiveChat(cls, websocket : WebSocket) :
               
                 
                     dbGenerator = getdb()
                     session = await dbGenerator.__anext__()
                     print("session : ",session)
                     try :
                        
                       while True : 
                                                
                        message = await websocket.receive_json()
                        print(colored( f"message {message}", "green", attrs=["bold"] ))
                        message_text = message["message"]
                        # print( colored(f"Info : message = {message_text}","green",attrs=["bold"] ))
                        senderId = int( message["senderId"] )
                        receiverId = int( message["receiverId"] )
                        chatRoomId = int( message["chatRoomId"] )
                        await ChatService.sendChat(message=message_text, senderId=senderId, receiverId=receiverId, chatRoomId=chatRoomId, messageTime=datetime.now(tz=timezone.utc), id=1)
                        sender_query = select(User).where(User.id == senderId)
                        receiver_query = select(User).where(User.id == receiverId)
                        chat_room_query = select(ChatRooms).where(ChatRooms.id == chatRoomId)
                        query_results = {}

                        for id,query in ((senderId,sender_query),(receiverId,receiver_query),(chatRoomId,chat_room_query)) :

                                query_results[id] =  await session.execute(query) 

                        print(colored( f"query results :  {query_results}", "green", attrs=["bold"] ))
                        result_objects = {}
                     
                        for id in query_results.keys() :
                               
                                result_objects[id] = query_results[id].scalar_one_or_none()

                        
                        print(colored( f"RESULT OBJECTS :  {result_objects}", "green", attrs=["bold"] ))
                        if(len(result_objects) >= 2 and senderId in result_objects and receiverId in result_objects) :

                          message_object = Messages(chat_room_id = result_objects[chatRoomId].id , text = message_text, sender_id = result_objects[senderId].id, receiver_id = result_objects[receiverId].id )
                          session.add(message_object)
                          result_objects[chatRoomId].lastMessageTime = datetime.now(tz=timezone.utc)
                          await session.commit()
                          await session.refresh(message_object)
                          
                        
                        else :
                               
                               raise Exception("Invalid Credentials")
                     
                     except WebSocketDisconnect as e :
                             
                             print( colored(f"Info : Websocket Disconnected", "green", attrs=["bold"]))
               
                     except WebSocketException as e :
                             
                             print( colored(f"Exception ocuured in Websocket {e}", "red", attrs=["bold"]))
                             await websocket.close()
                     except Exception as e :
                             
                             print(colored( f"message {message}", "green", attrs=["bold"] ))
                             print( colored(f"Exception occured in Websocket handler {e}", "red", attrs=["bold"]))
                             await websocket.close()

                        
                     await dbGenerator.aclose()

        @staticmethod
        async def handleChatWebsocket(websocket : WebSocket) :
               
               await websocket.accept()

               userId = websocket.query_params.get("userId")
                 
               if(userId) :
                      
                      try :
                             userId = int(userId)
                             ChatService.webSockets[userId] = websocket
                             await ChatService.receiveChat(websocket)
                     
                             

                      except WebSocketDisconnect as e :
                             
                             print( colored(f"Info : Websocket Disconnected", "green", attrs=["bold"]))
               
                      except WebSocketException as e :
                             
                             print( colored(f"Exception ocuured in Websocket {e}", "red", attrs=["bold"]))
                             await websocket.close()
                      except Exception as e :
                             
                             print( colored(f"Exception occured in Websocket handler {e}", "red", attrs=["bold"]))
                             await websocket.close()

               else :
                      
                      await websocket.close()


        @staticmethod
        async def getMessages(chatRoomId : int, lastMessageDateTime : datetime , session : AsyncSession) -> JSONResponse :
               

                        try :
                               

                                 chat_room_query = select(ChatRooms).where( ChatRooms.id == chatRoomId)
                                 chat_room_result = await session.execute(chat_room_query)
                                 chat_room_object = chat_room_result.scalar_one_or_none()
                                 lastMessageDateTime = datetime.fromtimestamp(lastMessageDateTime)
                                 lastMessageDateTime = lastMessageDateTime.replace(tzinfo=timezone.utc)
                                 print( colored(f"Info : {lastMessageDateTime}","green", attrs=["bold"]))

                                 if(chat_room_object) :

                                        messages_query = select(Messages).where(Messages.chat_room_id == chat_room_object.id, Messages.message_time < lastMessageDateTime).limit(50).order_by(desc(Messages.message_time))
                                        messages_results = await session.execute(messages_query)
                                        messages_objects = messages_results.scalars().all()
                                        # print( colored(f"Info : Message Datetime : {lastMessageDateTime}", "green", attrs=["bold"]))
                                        
                                        if(len(messages_objects) > 0) :
                                          
                                          data = Serializer.ListSerializer(messages_objects, fields = ["id","text" ,"chat_room_id", "sender_id","receiver_id","message_time"])
                                        
                                        else :
                                               
                                          data = []

                                        print( colored(f"Info : Message Objects : {data}", "green", attrs=["bold"]))
                                        return JSONResponse({"message" : "ok", "messages" : data,"success" : True}, status_code=200)

                                 else :

                                        return JSONResponse({"message" : "ChatRoom Does Not Exists", "success" : False},status_code=409)         
                
                        except Exception as e :
                               
                                print( colored(f"Error : {e}","red", attrs=["bold"]) )
                                return JSONResponse({"message" : "Internal Server Error", "success" : False},status_code=500)
