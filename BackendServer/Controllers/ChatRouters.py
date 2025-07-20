from fastapi import APIRouter, Depends, Body, WebSocket, WebSocketDisconnect
from Repository.database import getdb 
from Services.ChatServices import ChatService
from PydanticModels.Models import addContactModel
from termcolor import colored



ChatRouter : APIRouter = APIRouter()



@ChatRouter.post("/add-contact")
async def addContact(UserId : int,responseBody : addContactModel,session = Depends(getdb)) :

    
       MobileNumber : str = responseBody.MobileNumber
       # UserId : int = responseBody.UserId
       response = await ChatService.addContact(MobileNumber,UserId, session)
       return response


@ChatRouter.get("/get-chat-rooms")
async def getChatRooms( UserId : int, pageOffset : int ,session = Depends(getdb)) :

    
    response  = await ChatService.listChatRooms(userId=UserId, pageOffset = pageOffset ,session=session)
    
    return response


@ChatRouter.websocket("/ws/chat/send")
async def sendChat( websocket : WebSocket) :

       try :
             

         await ChatService.handleChatWebsocket(websocket)

       except Exception as e :
            
            print( colored(f"Error : {e}", "red", attrs=["bold"]) )
            

       
       
@ChatRouter.get("/getmessages")
async def getMessages( UserId : int, chatRoomId : int, lastMessageTimeStamp : float , session = Depends(getdb)) :


       #      print(colored(f"{UserId=}{chatRoomId=} laste message datetime {datetime.fromtimestamp(lastMessageTimeStamp).replace(tzinfo=timezone.utc)}{session=}", "green", attrs=["bold"]))

            response = await ChatService.getMessages(chatRoomId=chatRoomId, lastMessageDateTime=lastMessageTimeStamp,session=session)

            return response          

