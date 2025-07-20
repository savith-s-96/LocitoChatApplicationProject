import random
from sib_api_v3_sdk.rest import ApiException
import regex
from starlette.responses import JSONResponse
from Models.models import User,Otp,JsonTokenModel,AccessTokenModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import httpx
from datetime import datetime, timedelta, timezone
import jwt 
from Configurations.configurations import env_folder
from dotenv import load_dotenv
from os import getenv
from termcolor import colored

load_dotenv(env_folder)
" mysql+mysqlconnector://root:SAVITH%%402004@localhost:3306/locitomessenger"

def InvalidCredentialsResponse() -> JSONResponse :
     

     return JSONResponse({"message" : "Invalid User Credentials","success" : "false"},status_code=409)


async def generate_otp() : #otp generation function

     return random.randrange(100000,999999)


async def sendingMail( sendermail : str , receivermail : str, otp : str,sendername : str, receivername : str) : #function for sending mail using httpx asyncleint
 
 try :
      
     
      html_content = f"""
      <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <h2>Hello, {sendername}!</h2>
            <p>Here is your One-Time Password (OTP):</p>
            <div style="font-size: 24px; font-weight: bold; color: #2F4F4F;">{otp}</div>
            <p>This OTP is valid for <strong>5 minutes</strong>.</p>
            <p>If you did not request this, please ignore this email.</p>
            <hr>
            <p style="font-size: 12px;">This is an automated email, please do not reply.</p>
            <h2> Thank you from Locito Messenger Team <h2/>
        </body>
    </html>
     """
      api_key = getenv("BREVOAPIKEY") 
      headers : dict = {
           "accept" : "application/json",
           "api-key" : api_key,
           "content-type" : "application/json"
      }
      pay_load : dict = {
            "sender" : {
                  "name" : sendername,
                  "email" : sendermail
           },

           "to" :
            
            [ {
                "email" : receivermail
                }
            ],

            "subject" : "Locito Messenger Your OTP Code - Secure Login",
            "htmlContent" : html_content
           }
      brevo_api_url  : str = "https://api.brevo.com/v3/smtp/email"

      async with httpx.AsyncClient() as cleint :

             response = await cleint.post(brevo_api_url,headers=headers,json=pay_load)  

             if(response.status_code == 201) :

                   return True    
             else :
                   
                   print("Email not send : status code = ",response.status_code)
                   print("Email response error details : ",response.text)

 except Exception as e :

      print(colored(f"Error : {e}","red",attrs=["bold"]))


async def otp_send_and_store(user : User,session : AsyncSession) -> bool : # function for sending and storing a otp on a database
 
  try :
      otp : str = await generate_otp()
      otp = str(otp)
      try :
       
       otp_object = await session.execute(select(Otp).where(Otp.user_id == user.id))
       otp_object = otp_object.scalar_one_or_none()
       if(otp_object) :

            otp_object.otp = otp 
            otp_object.createdAt = datetime.now(timezone.utc)
            otp_object.expiredAt = datetime.now(timezone.utc) + timedelta(minutes=5)
       else :

            otp_object = Otp(otp = otp)
            otp_object.user = user 
            session.add(otp_object)

       await session.commit()
       user_email = user.Email
       await sendingMail(sendername="Locito Messenger Team",sendermail="savithparthi79@gmail.com",receivername=user_email,receivermail=user_email,otp=otp)
       return True
       
      except Exception as e :
           
           print("Error inside otp send function : \n",e)  
           return False
  except Exception as e:
       
        print(colored(f"Error : {e}","red",attrs=["bold"]))



async def register_and_login_service(user : User,session : AsyncSession) -> JSONResponse : # register service for user registeration and login using otp authentication
 
      try :
          email_regex : str = r"[a-zA-Z0-9!#$%&'*+/=?^_{|}~.-`]+@[a-zA-z].[a-zA-Z]{3}"
          mobile_no_regex : str = r"[0-9]{10}"

          if(regex.match(string=user.UserEmail,pattern=email_regex) and regex.match(string=user.MobileNumber,pattern=mobile_no_regex)) :
                
              user_already_exist = await session.execute(select(User).where(User.mobileNo == user.MobileNumber))
              user_already_exist = user_already_exist.scalar_one_or_none()
              print("user : ", user_already_exist)
              if(user_already_exist) :  
                    
                    user_object = user_already_exist
                    if(user_object.Email != user.UserEmail) :

                         return JSONResponse({"message":"Invalid Credentials", "success" : False},status_code=409)
              
              else :
                    
                    user = User(Email = user.UserEmail,mobileNo=user.MobileNumber) 
                    session.add(user)
                    await session.commit()
                    user = await session.execute(select(User).where(User.mobileNo == user.mobileNo))
                    user_object = user.scalar_one_or_none()
                    print("user : " , user_object)
                  
          
              is_otp_sended = await otp_send_and_store(user_object, session)

              if(is_otp_sended) :
                    
                    response = JSONResponse({"message" : f"Login Otp sended to email {user_object.Email}","user_id" : user_object.id,"success" : "true"},status_code=200)
      
              else :
                    
                    response = JSONResponse({"message" : "Invalid Credentials Otp not sended for login"},status_code=409)
          
          else :
                
                    response = InvalidCredentialsResponse()
                

          return response
      
      except Exception as e :
           
           print(colored(f"Error : {e}","red",attrs=["bold"]))
           return JSONResponse({"message" : "Internal Server Error", "success" : False},status_code=500)





      
async def regenrate_otp_service(user_id : int,session : AsyncSession) -> JSONResponse :
     
              if(user_id) :
                  
                  
                  user = await session.get(User,user_id)
                  
                  if(user) :
                       
                       otp = user.otp
                       if(otp) :
     
                        if(not(otp.expiredAt.replace(tzinfo = timezone.utc) > datetime.now(timezone.utc))) :
                            
                            await otp_send_and_store(user,session)
                            response = JSONResponse({"message" : f"otp send to email : {user.Email}","success" : "true"},status_code=200)
                       
                        else :
                            
                            response = JSONResponse({"message" : "previous otp not expired","success" :"false"},status_code=200)
                       

                       else :
                            
                             return InvalidCredentialsResponse
                       
                       return response
                  
              return InvalidCredentialsResponse()


async def generate_access_token(refresh_token : JsonTokenModel,session : AsyncSession) :
      
         try :  
           
           
           user = refresh_token.user 
           print("user : ",user)
           key = getenv("SECRETKEY")
           access_token_exp = datetime.now(timezone.utc) + timedelta(minutes=15)
           access_token_crt = datetime.now(timezone.utc)
           access_token = jwt.encode({"user_id" : user.id, "exp" : access_token_exp}, key=key, algorithm="HS256")
           access_token_object = AccessTokenModel(access_token = access_token, created_at = access_token_crt, expired_at = access_token_exp)
           access_token_object.refresh_token = refresh_token 
           session.add(access_token_object)
           await session.commit()
           await session.refresh(access_token_object)
           return [access_token_object.access_token,access_token_exp.replace(tzinfo = timezone.utc)]
           
         except Exception as e :

             print(colored(f"Error : {e}","red",attrs=["bold"]))


async def generate_json_web_token(user : User,session : AsyncSession) :

    try :
      key = getenv("SECRETKEY")
      refresh_token_exp = datetime.now(timezone.utc) + timedelta(days=90)
      refresh_token_crt = datetime.now(timezone.utc)
      json_token_object = user.jsontoken 

      if(json_token_object) :
           
            if(json_token_object.expired_at.replace(tzinfo = timezone.utc) > datetime.now(timezone.utc)) :
                 
                   refresh_token = jwt.encode({"user_id" : user.id,"exp" : refresh_token_exp},key=key,algorithm="HS256")
                   json_token_object.refresh_token = refresh_token
                   json_token_object.created_at = refresh_token_crt
                   json_token_object.expired_at = refresh_token_exp

      else :
                
        refresh_token = jwt.encode({"user_id" : user.id,"exp" : refresh_token_exp},key=key,algorithm="HS256")
        json_token_object = JsonTokenModel(refresh_token = refresh_token, created_at = refresh_token_crt, expired_at = refresh_token_exp)
        json_token_object.user = user 
        session.add(json_token_object)
      await session.commit()
      await session.refresh(json_token_object)
      access_token = await generate_access_token(json_token_object, session)
      return {"refresh_token" : json_token_object.refresh_token,"refresh_token_exp" : refresh_token_exp.replace(tzinfo = timezone.utc),"access_token" : access_token[0],"access_token_exp" : access_token[1]}
    
    except Exception as e :
         
         print(colored(f"Error : {e}","red",attrs=["bold"]))

async def verify_otp_service(user_id : int | None, otp : str, session : AsyncSession) -> JSONResponse :
     
        try :
       
              if(user_id and otp) :

                    user = await session.get(User,user_id)
                    otp_object = user.otp 
          
                    if(otp and otp_object) :
                          
                           if((otp_object.expiredAt.replace(tzinfo = timezone.utc) > datetime.now(timezone.utc)) and (otp_object.otp == otp)) :
                                
                                json_token = await generate_json_web_token(user,session)
                              #   print("refresh token expiry : ",json_token["refresh_token_exp"],"\n access token expiry  : ",json_token["access_token_exp"])
                                response : JSONResponse = JSONResponse({"message" : "otp verification successful","success" : "true","verified" : "true"},status_code=200)
                                response.set_cookie("refresh_token" , json_token["refresh_token"],expires=json_token["refresh_token_exp"],httponly=True,samesite="none",secure=True)
                                response.set_cookie("access_token",json_token["access_token"],expires=json_token["access_token_exp"],httponly=True,samesite="none",secure=True)
                              #   print(response.headers)
                                return response
                           
                           else :
                                 
                                 return JSONResponse({"message" : "otp expired or wrong please resend","success" : "false","verified" :"false"},status_code=200)
                    else :
                          
                         return JSONResponse({"message" : "Otp not present","success" : "false","verified" : "false"},status_code=409)
       
              else :
                    
                    return JSONResponse({"message" : "Invalid User Credentials","success" : "false","verified" : "false"},status_code=409)
        except Exception as e :
             
               print(colored(f"Error : {e}","red",attrs=["bold"]))

               return JSONResponse({"message" : "Internal Server Error"},status_code=501)
        


async def get_access_token_service(refresh_token : str,session : AsyncSession) -> JSONResponse :

           if(refresh_token) :
                
                refresh_token_result : JsonTokenModel = await session.execute(select(JsonTokenModel).where(JsonTokenModel.refresh_token == refresh_token))
                refresh_token_object = refresh_token_result.scalars().first()
                if(refresh_token_object) :
                  print("refresh token object : ",refresh_token_object.refresh_token)
                  access_token = await generate_access_token(refresh_token_object,session)
                  response = JSONResponse({"message" : "access token got","userId" : refresh_token_object.user_id,"success" : "true"},status_code=200)
                  response.set_cookie("access_token",access_token[0],expires=access_token[1],httponly=True, samesite="none", secure= True)
                else :
                     
                     response = JSONResponse({"message" : "Invalid Refresh Token"},status_code=401)

                return response

           else :
                
                print("token missing")
                return JSONResponse({"message" : "refresh token missing","success" : "false"},status_code=409)