import sys
try :
   
   from dotenv import load_dotenv
   from os import path,getenv
   from pathlib import Path
   from sqlalchemy.ext.asyncio import create_async_engine
   from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession


except ImportError as Error :
     
        print("Import Error as : ",Error.name)
        sys.exit(0)

BASE_DIR = Path(__file__).parent.parent
env_folder = path.join(BASE_DIR,"Configurations","configuration.env")
load_dotenv(env_folder)


DatabaseMetaKeys = ["DatabaseName","DatabasePort","DatabaseHost","DatabaseType","DatabaseDriver","DatabasePassword","DatabaseUserName"]

DatabaseMetaData = {}

try :
      
  for DatabaseMetaKey in DatabaseMetaKeys :


      EnvData = getenv(DatabaseMetaKey)

      if(EnvData) :

            DatabaseMetaData[DatabaseMetaKey] = EnvData 

      else :

            raise Exception(f"{DatabaseMetaKey} has None value") 
      
except Exception as Error :

     print("Database Configuration Error : ",Error)  
     sys.exit(0)


DataBaseUrl = f"{DatabaseMetaData["DatabaseType"]}+{DatabaseMetaData["DatabaseDriver"]}://{DatabaseMetaData["DatabaseUserName"]}:{DatabaseMetaData["DatabasePassword"]}@{DatabaseMetaData["DatabaseHost"]}:{DatabaseMetaData["DatabasePort"]}/{DatabaseMetaData["DatabaseName"]}"

# DataBaseUrl = "mysql+aiomysql:///chatdb.db"

DatabaseEngine = create_async_engine(
    DataBaseUrl,
    echo=True,
    pool_size=20,
    max_overflow=30,
    pool_timeout=30,
    connect_args={
        "connect_timeout": 10,
        "charset": "utf8mb4",
    },
)

AsyncSessionLocal = async_sessionmaker(
    bind=DatabaseEngine,
    class_=AsyncSession,
    expire_on_commit=False
)

