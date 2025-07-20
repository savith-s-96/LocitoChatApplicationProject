from pydantic import BaseModel

class UserRegister(BaseModel) :

    UserEmail : str 
    MobileNumber : str  


# class userId(BaseModel) :

#     UserId : int 


class addContactModel(BaseModel) :

     MobileNumber : str
     

