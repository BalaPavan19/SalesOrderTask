from fastapi import APIRouter,Depends,Path
from typing import Annotated
from App.Apps.Customers.handler import customer_handler
from App.Apps.Customers.schema import *
from sqlalchemy.orm import Session
from App.DataBase.database import get_db
from fastapi.security import OAuth2PasswordBearer
 
router = APIRouter(prefix="/CustomerData",tags=["Customers"])

                   
 
@router.get("/read_customer_data")       
def read_complete_data(db: Session = Depends(get_db)):
    try:      
        return customer_handler.read_data(db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))


@router.post('/create')      
def create_item(io_customer_creation:list[create_customer_schema],db: Session = Depends(get_db))->list[create_customer_schema]:
    try:         
        return customer_handler.create_data(io_customer_creation,db) 
    except BaseException as e:
        return Response(status_code=409,content=str(e))

@router.get("/read/{iv_id}")       
def read_customer(iv_id:Annotated[str, Path(max_length=4)],db: Session = Depends(get_db))->dict:  
    try:          
        return customer_handler.read(iv_id,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))


@router.put("/update")           
def update_customer(io_customer:create_customer_schema,db: Session = Depends(get_db))->create_customer_schema:
    try:
        return customer_handler.updation(io_customer,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))


@router.delete("/delete/{iv_id}")
def delete_customer(iv_id:str,db: Session = Depends(get_db)):
    try:
        return customer_handler.deletion(iv_id,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))


@router.post("/QueryCustomer")
def customer_query(ioQuery:CustomerQuerySchema=Depends(CustomerQueryParameterDepend),db: Session = Depends(get_db)):
    try:
        return customer_handler.query_data(ioQuery,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))