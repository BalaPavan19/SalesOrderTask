from fastapi import APIRouter,Depends,Path
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from App.Apps.Products.handler import item_handler
from App.Apps.Products.schema import *
from App.constants import *
from sqlalchemy.orm import Session
from App.DataBase.database import get_db
 
router = APIRouter(prefix="/ProductsData")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.get("/readproductdata",tags=["Products"])      
def read_complete_data(db: Session = Depends(get_db)):
    try:         
        return item_handler.read_data(db) 
    except BaseException as e:
        return str(e) 


@router.post('/create')      
def create_item(io_item_creation:list[item_creation_schema],db: Session = Depends(get_db),token:str=Depends(oauth2_scheme))->list[item_creation_schema]:
    try:         
        return item_handler.create_data(io_item_creation,db) 
    except BaseException as e:
        return Response(status_code=409,content=str(e))


@router.get("/read/{iv_item_id}")       
def read_item(iv_item_id:Annotated[str, Path(max_length=4)],db: Session = Depends(get_db))->dict:
    try:       
        return item_handler.read(iv_item_id,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))   


@router.put("/update")           
def update_item(io_item:item_creation_schema,db: Session = Depends(get_db),token:str=Depends(oauth2_scheme))->item_creation_schema:
    try:
        return item_handler.updation(io_item,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))   


@router.delete("/delete/{iv_item_id}")
def delete_item(iv_item_id:str,db: Session = Depends(get_db),token:str=Depends(oauth2_scheme)):
    try:
        return item_handler.deletion(iv_item_id,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))   


@router.post("/QueryProducts")
def items_query(ioQuery:ItemsQuerySchema=Depends(ItemQueryParameterDepend),db:Session=Depends(get_db)):
    try:
        return item_handler.query_data(ioQuery,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))