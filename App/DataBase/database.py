from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from pydantic import PostgresDsn
import os 
from dotenv import load_dotenv

load_dotenv()
 

DB_URL = PostgresDsn.build(
            host=os.getenv("HOST"),
            port=5432,
            scheme=os.getenv("DBSCHEME"),
            username=os.getenv("DBUSERNAME"),
            password=os.getenv("DBPASSWORD"),
            path=os.getenv("DBPATH")
        )  

engine = create_engine(str(DB_URL),pool_pre_ping=True,connect_args={"options": f"-csearch_path=zbp_salesdata"})
sessionlocal = sessionmaker(autocommit = False, autoflush=False, bind=engine) #To Perform Actions on DB 
Base = declarative_base()    #To Create Tables 

def get_db():
    db = sessionlocal()
    try:
        yield db
    finally:
        db.close()

def create_table():
    Base.metadata.create_all(bind=engine)
