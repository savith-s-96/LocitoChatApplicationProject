from fastapi import APIRouter, Depends
from Repository.database import getdb
from PydanticModels.Models import UserRegister
from Services.AuthenticationServices import register_and_login_service, regenrate_otp_service, verify_otp_service, get_access_token_service
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

AuthenticationRouter : APIRouter = APIRouter()

# AuthenticationRouter.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://127.0.0.1:5173"],  # your React frontend
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )


@AuthenticationRouter.post("/register") 
async def Register_and_login(user : UserRegister, session : Annotated[AsyncSession,Depends(getdb)]) :
      
      
      response = await register_and_login_service(user,session)
      
      return response



@AuthenticationRouter.get("/resend/otp")
async def RegenerateOtp(session : Annotated[AsyncSession, Depends(getdb)],user_id : int ) :
      
      response = await regenrate_otp_service(user_id,session)

      return response

@AuthenticationRouter.get("/verify/otp/user")
async def verifyOtp( session : Annotated[AsyncSession,Depends(getdb)] , user_id : int ,otp : str = None) :
  
      print("user id  : ",user_id)
      print("otp : ", otp)
      response = await verify_otp_service(user_id,otp,session)

      return response



@AuthenticationRouter.get("/user/get/access-token")
async def get_access_token(request : Request,session : Annotated[AsyncSession,Depends(getdb)]) :

       
                  

            print(request.cookies)
            response = await get_access_token_service(refresh_token=request.cookies.get("refresh_token",None),session = session)

            return response

