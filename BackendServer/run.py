import uvicorn
import asyncio
import os
if __name__ == "__main__" :

  try :

     key_file = os.path.abspath("key.pem")
     cert_file = os.path.abspath("cert.pem")
     print(key_file,cert_file)
     # uvicorn.run("Controllers.main:app",host="192.168.211.15",port=8000,reload=True, ssl_keyfile=key_file, ssl_certfile=cert_file)
     uvicorn.run("Controllers.main:app",host="127.0.0.1",port=8000,reload=True,)
  except asyncio.CancelledError as error :

       print("Server Shutting down...")
     
  except KeyboardInterrupt as error :

       print("Server Shutting down...")