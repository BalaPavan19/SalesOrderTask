from sqlalchemy.orm import Session
from App.DataBase.models import *
from App.Apps.Login.schema import *
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class Hasher():
    @staticmethod
    def verify_password(plain_password, hashed_password):             # Verification
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):                   # Encryption
        return pwd_context.hash(password)


def signup(login:LoginSchema,db:Session):
    id = login.username[0:3]+str(db.query(LoginModel).count()+1)
    hashed_password = Hasher.get_password_hash(login.password)
    db_data = LoginModel(user_id = id,username=login.username,password=hashed_password)
    db.add(db_data)
    db.commit()
    db.refresh(db_data)
    return "SignUp Done"


def valid_login(db:Session,login:LoginSchema):
    if db.query(LoginModel).filter(LoginModel.username==login.username).first() is not None:
        user = db.query(LoginModel).filter(LoginModel.username==login.username).first()
        password = user.password
        if Hasher.verify_password(login.password,password):
            return True
    


def duplicate_login(db:Session,login:LoginSchema):
    if db.query(LoginModel).filter(LoginModel.username==login.username).first() is not None:
        return True
        
