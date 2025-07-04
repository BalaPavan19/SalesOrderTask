from App.DataBase.models import LoginModel
from sqlalchemy.orm import Session
from App.exceptions import *
from fastapi import Response
from App.constants import *
from App.Apps.Login.crud import *
from App.Apps.Login.schema import *
from App.auth.authontication import *

class login_handler():

    def valid_login(login:LoginSchema,db:Session):
        if valid_login(db,login):
            return {"Sucess Login"}
           
        else:
             raise RecordNotFound("InValid Data") 

    
    def valid_form_login(form_data:LoginSchema,db:Session):
        if valid_login(db,form_data):
            access_token = create_access_token(data={"sub": form_data.username})
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            raise RecordNotFound("In Valid Format")
            

    def signup(login:LoginSchema,db:Session):
        if duplicate_login(db,login):
            raise DupliacteRecord("Record Already Exists, You can Login")
        elif not validatepassword(login.password):
            raise RecordNotFound("Password not in Valid Format")
        else:
             return signup(login,db)