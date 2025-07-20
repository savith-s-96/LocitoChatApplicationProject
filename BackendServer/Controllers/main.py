from fastapi import FastAPI, Depends, Body
from fastapi.middleware.cors import CORSMiddleware 
from Configurations.configurations import DatabaseEngine, BASE_DIR
from contextlib import asynccontextmanager
from fastapi.staticfiles import StaticFiles
from Middlewares.AuthenticationMiddleware import AuthenticationMiddleware
from .AuthenticationRouters import AuthenticationRouter
from .ChatRouters import ChatRouter
from .UserRouters import user_router
from os import path






######### server startup and shutdown function #######
@asynccontextmanager
async def serverStartupFunction(app : FastAPI) :

       conn = await DatabaseEngine.connect()
   
       yield

       try :


           await conn.close() 
           await DatabaseEngine.dispose()

       except Exception as e:

            print("Error : " , e)



########## main fastapi application ##############

app = FastAPI(lifespan = serverStartupFunction)

origins = [
    "http://127.0.0.1:5173",
    "http://localhost:5173",
    "http://192.168.211.15:5173"   # React sometimes switches to this
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.add_middleware(AuthenticationMiddleware)
app.mount("/media/",StaticFiles(directory= path.join(BASE_DIR,"Media")),name="media")
app.include_router(router=AuthenticationRouter)
app.include_router(router=ChatRouter, prefix="/chat")
app.include_router(router=user_router)

@app.get("/")
def Home() :

      return "Welcome to Locito Messenger Api"



      
