from Models.models import User
from Configurations.configurations import BASE_DIR
from os import path , remove
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import query
from sqlalchemy import select
from starlette.responses import JSONResponse
from datetime import datetime, timezone
import magic
from fastapi.responses import FileResponse
from Serializers.Serializers import Serializer
import aiofiles
from termcolor import colored

class UserService() :

          
          @staticmethod
          async def uploadUserProfile(ProfileImageFile) :
                 
                    chunk_size : int = 5*1024 * 1024
                    start_index = 0
                    ProfileImageUploadDirectory = path.join(BASE_DIR,"Media","ProfileImages")
                    print("file Name : ", ProfileImageFile)
                    fileName = str(datetime.timestamp(datetime.now(tz= timezone.utc))) + ProfileImageFile.filename 
                    file_path = path.join(ProfileImageUploadDirectory,fileName)
                    file_object = await aiofiles.open(file_path, "+ab")
                    while True :
                            
                            await ProfileImageFile.seek(start_index)
                            data = await ProfileImageFile.read(chunk_size)
                            
                            if( not data) :
                                    
                                    break 
                            
                            await file_object.write(data)
                            start_index = start_index + chunk_size
                    await ProfileImageFile.close()
                    await file_object.close()

                    return {"fileName" : fileName, "size" : path.getsize(file_path)}
                    

                            
                            


          @staticmethod
          async def userUpdate(userId,session : AsyncSession,userName : str = None, ProfileImage = None, ) -> JSONResponse :

              try :
                  
                  
                
                  if((userName or ProfileImage) and userId) : 
                             
                             fileName = None
                             userquery = select(User).where(User.id == userId)
                             user_result = await session.execute(userquery)
                             user_object = user_result.scalar_one_or_none()

                             if(user_object) : 
                               
                               if(userName) :
                                    
                    
                                    user_object.userName = userName
                             
                               if(ProfileImage and ProfileImage.size != 0) :
                                    

                                     
                                   if(user_object.profileImageUrl) :
                               
                                                 existing_file_path = path.join(BASE_DIR,"Media",user_object.profileImageUrl)
                                                 if(path.exists(existing_file_path)) :
                                                        
                                                        remove(existing_file_path)
                                                   
                                   fileData = await UserService.uploadUserProfile( ProfileImageFile = ProfileImage)
                                   relative_file_path = path.join("ProfileImages",fileData["fileName"])

                                   user_object.profileImageUrl = relative_file_path 


                               await session.commit() 
                               await session.refresh(user_object)
                               data = Serializer.Serializer(user_object, fields={"userName","Email","mobileNo","profileImageUrl"})
                               print(colored(f"data : {data}","green",attrs=["bold"]))
                               response = JSONResponse({"message" : "User data updated successfully", "success" : True, **data},status_code=200)
                                   
                               

                             else :
                             
                                   response = JSONResponse({'message' : "user not exists", "success" : False},status_code=409)
                             
                  
                  else :
                         
                         response = JSONResponse({"message" : "user has no data to update", "success" : False},status_code=409)
                  
                  return response
              
              except Exception as e:

                     print(colored(f"Error : {e}","red",attrs=["bold"]))
                     return JSONResponse({"message" : "Internal Server Error" , "success" : False},status_code=500)     


          @staticmethod
          async def serveProfile(file_path : str) -> FileResponse | None :
                 
                  

                  try :
                         file_path = path.join(BASE_DIR,"Media",file_path)
                         if(path.exists(file_path)) :
                                
                                mime = magic.Magic(mime=True)
                                mime_type = mime.from_file(file_path)

                                return FileResponse(file_path,media_type=mime_type)
                                
                         
                         else :
                                
                                return None
                  
                  except Exception as e :
                         
                         print(colored(f"Error : {e}","red",attrs=["bold"]))
                         return None 
                  
          @staticmethod        
          async def getUser(UserId : int, session : AsyncSession) -> JSONResponse :
                 
                 try :

                    if(UserId) :
                           
                           user_query = select(User).where(User.id == UserId) 
                           user_query_result = await session.execute(user_query)
                           user_object = user_query_result.scalar_one_or_none()

                           if(user_object) :
                                  
                                  data = Serializer.Serializer(user_object, fields={"id","userName","Email","mobileNo","profileImageUrl"})
                                  print("data : ", data)
                                  response = JSONResponse({"message" : "user exist", "success" : True,**data},status_code=200)
                           
                           else :
                                  
                                  response = JSONResponse({"message" : "user not found", "success" : False},status_code=409)

                    
                    else :
                           
                          response = JSONResponse({"message" : "Invalid user id", "success" : False},status_code=402)

                    return response
                
                 except Exception as e :
                        
                        print(colored(f"Error : {e}","red",attrs=["bold"]))
                        response = JSONResponse({"message" : "Internal Server Error", "success" : False},status_code=500)
                        return response
                       




