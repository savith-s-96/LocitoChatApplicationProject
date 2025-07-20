from starlette.middleware.base import BaseHTTPMiddleware 
from starlette.requests import Request 
from starlette.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession,async_sessionmaker
from Configurations.configurations import DatabaseEngine, env_folder
from Models.models import AccessTokenModel
from sqlalchemy import select
from datetime  import datetime, timezone
from dotenv import load_dotenv
from os import getenv
import jwt
from urllib.parse import urlencode, parse_qs
from jwt.exceptions import InvalidTokenError, DecodeError, ExpiredSignatureError, MissingRequiredClaimError
from termcolor import colored
load_dotenv(env_folder)
def prefixInclude(prefix : str , urls : list[str] ) -> list[str] :

        for i in range(len(urls)) :
              
              urls[i] = prefix + urls[i]

        return urls


def IncludeAuthenticatedurls(list_urls : list[list[str]]) -> list[str] :


       try :
           temp : list[str] = []
      #      print("list urls : ",list_urls)
           for urls in list_urls :
                 
                 for url in urls :
                       
                        temp.append(url)

           return temp

       except Exception as e:

          print("Error : ",e)


chat_url_prefix = "/chat/"
chat_urls  : list[str] = ["add-contact","get-chat-rooms"]
chat_urls = prefixInclude(chat_url_prefix,chat_urls)
# print("chat urls ",chat_urls)



all_authenticated_urls : list[list[str]] = [chat_urls,["/user/profile/update", "/user/profile", "/user/profile/details", "/chat/send", "/chat/getmessages"]]

authenticated_urls : list[str] = IncludeAuthenticatedurls(all_authenticated_urls)

unauthenticated_urls : list[str] = ["/register","/","/resend/otp","/verify/otp/user","/user/get/access-token","/regenerate/otp","/media/"]



class AuthenticationMiddleware(BaseHTTPMiddleware) :


    async def dispatch(self, request : Request, call_next):
        
             try :
                  path : str = request.url.path 
                  print("path", path)
                  print(colored(f"cookies : {request.cookies} ","red",attrs=["bold"]))
                  # # access_token = request.cookies.get("_token")
                  # # print("access token : ",access_token)
                  # print("Cookies : ", request.cookies)
                 
                  if(path in authenticated_urls or path in unauthenticated_urls) :
                          

                  
                         if(path in unauthenticated_urls) :
                              
                              try :
                                  
                                  response = await call_next(request)

                                  return response

                              except Exception as e :
                                     
                                     print("Error in Authentication middleware",e)
                                     response = JSONResponse({"message" : "Internal Server Error"},status_code=500)
                                     response.headers["Access-Control-Allow-Origin"] = request.headers.get("origin")
                                     response.headers["Access-Control-Allow-Credentials"] = "true"
                                     return response

                  
                         else :
                                 
                                 
                                 access_token = request.cookies.get("access_token")
                                 print("access token : ", access_token)
                                 if(access_token) :
                                    
                                    try :
                                       
                                       secret_key =  getenv("SECRETKEY")
                                       decoded_token = jwt.decode(access_token,secret_key,algorithms=["HS256"])
                                       query_params = dict(request.query_params)
                                       query_params["UserId"] = int(decoded_token["user_id"])
                                       query_string = urlencode(query_params)
                                       request.scope["query_string"] = query_string.encode("utf-8")
                                       conn = await DatabaseEngine.connect()
                                       session = async_sessionmaker(bind=DatabaseEngine,class_=AsyncSession,expire_on_commit=False)
                                       access_token_object : AccessTokenModel = await session().execute(select(AccessTokenModel).where(AccessTokenModel.access_token == access_token))
                                       access_token_object : AccessTokenModel = access_token_object.scalar_one_or_none()
                                       if(access_token_object) :
                                             
                                             if(access_token_object.expired_at.replace(tzinfo=timezone.utc) > datetime.now(timezone.utc)) :
                                                   
                                                   response = await call_next(request) 
                                                   return response
                                             
                                             else :
                                                   
                                                   response = JSONResponse({"message" : "access token expired","success" : "true","access_token" : "true","expired" : "true"},status_code=200)
                                       
                                       else :
                                             
                                             response = JSONResponse({"message" : "access token incorrect error","success" : 'false',"access_token" : "false"},status_code=422)
                                       await conn.close()  
                                    
                                    except (InvalidTokenError, DecodeError, MissingRequiredClaimError) as e :
                                            
                                            print(colored(f"Error : {e}","red",attrs=["bold"]))
                                            response = JSONResponse({"message" : "Authentication failed"},status_code=403)
                                    
                                    except ExpiredSignatureError as e:
                                            

                                            print(colored(f"Error : {e}","red",attrs=["bold"]))
                                            response = JSONResponse({"message" : "access token expired","success" : "true","access_token" : "true","expired" : "true"},status_code=200)
            

                                 else :
                                       print("access token is missing")   
                                       response = JSONResponse({"message" : "access token is missing","access_token" : "false","success" : "false"},status_code=200)

                              #    await session.close()      
                              
                              
                                 if(request.headers.get("origin")) :
                                   
                                   response.headers["Access-Control-Allow-Origin"] = request.headers.get("origin")

                                 response.headers["Access-Control-Allow-Credentials"] = "true"
                                 response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                                 response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
                                 return response
                         
                  
                  response =  JSONResponse({"message" : "requested resource does not exist"},status_code=200)
                  if(request.headers.get("origin")) :
                                   
                                   response.headers["Access-Control-Allow-Origin"] = request.headers.get("origin")

                  response.headers["Access-Control-Allow-Credentials"] = "true"
                  response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                  response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
                  return response
            
             except Exception as e :
      
                  print(colored(f"Error : {e}","red",attrs=["bold"]))
                   
                  response =  JSONResponse({"message" : "Internal Server Error"},status_code=409)
                  if(request.headers.get("origin")) :
                                   
                                   response.headers["Access-Control-Allow-Origin"] = request.headers.get("origin")

                  response.headers["Access-Control-Allow-Credentials"] = "true"
                  response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
                  response.headers["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
                  return response
                   

