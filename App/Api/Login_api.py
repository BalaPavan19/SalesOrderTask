from fastapi import APIRouter,Depends,Path
from fastapi.security import OAuth2PasswordBearer,OAuth2PasswordRequestForm
from App.auth.authontication import *
from App.Apps.Login.handler import *
from sqlalchemy.orm import Session
from App.DataBase.database import get_db
from App.Apps.Login.schema import *

router = APIRouter(tags=["Login"])


@router.post("/token")
def login_for_access_token(db:Session=Depends(get_db),form_data: OAuth2PasswordRequestForm = Depends()):
    try:
       return login_handler.valid_form_login(form_data,db)
    except BaseException as e:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    

@router.get("/protected")
def protected_route(username: str = Depends(get_current_user)):      #Decoded User Details
    return {"message": f"Hello, {username}! This is a protected resource."}



@router.post("/signup")
def sign_up(login:LoginSchema,db:Session=Depends(get_db)):
    try:
        return login_handler.signup(login,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))