from fastapi import APIRouter, UploadFile, Form, Depends
from typing import Annotated
from Repository.database import getdb
from Services.UserServices import UserService


user_router = APIRouter()

@user_router.put("/user/profile/update")
async def user_update(UserId : int,userName : Annotated[str | None , Form()] =  None,ProfileImage : None | UploadFile = None,session = Depends(getdb),) :


             response = await UserService.userUpdate(UserId,session,userName=userName,ProfileImage=ProfileImage)

             return response 


@user_router.get("/user/profile")
async def serveUserprofile(filePath : str) :
        

          response = await UserService.serveProfile(filePath)

          return response
           

@user_router.get("/user/profile/details")
async def getUser(UserId : int, session = Depends(getdb)) :
        
        response = await UserService.getUser(UserId, session)

        return response
        






