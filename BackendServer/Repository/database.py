
from Configurations.configurations import AsyncSessionLocal

async def getdb() :

     async with AsyncSessionLocal() as session :
            
            yield session
 