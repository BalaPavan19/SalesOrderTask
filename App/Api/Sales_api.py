from fastapi import APIRouter,Depends,Path
from typing import Annotated
from App.Apps.Sales.handler import sales_handler
from App.Apps.Sales.schema import *
from App.constants import *
from sqlalchemy.orm import Session
from App.DataBase.database import get_db


router = APIRouter(prefix="/SalesData",tags=["Sales"])

 
@router.get("/read_sales_data")       
def read_complete_data(db:Session=Depends(get_db)):
    try:            
        return sales_handler.read_data(db)
    except BaseException as e:
        return str(e)

@router.post('/create_order')      
def create_sales(io_sales_order_creation:list[sales_order_creation_schema],db: Session = Depends(get_db))->list[sales_order_creation_schema]:
    try:         
        return sales_handler.create_data(io_sales_order_creation,db) 
    except BaseException as e:
        return Response(status_code=409,content=str(e))
    

@router.get("/read_order/{iv_sales_id}")       
def read_sales_order(iv_sales_id:Annotated[str, Path(max_length=4)],db: Session = Depends(get_db)):   
    try:         
        return sales_handler.read(iv_sales_id,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))

@router.put("/update_order/{iv_sales_id}")           
def update_sales_order(iv_sales_id:str,io_item:sales_order_creation_schema,db: Session = Depends(get_db))->sales_order_creation_schema:
    try:
        return sales_handler.updation(iv_sales_id,io_item,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))


@router.delete("/delete_order/{iv_sales_id}")
def delete_sales_order(iv_sales_id:str,db: Session = Depends(get_db)):
    try:
        return sales_handler.deletion(iv_sales_id,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))

@router.post("/QuerySales")
def sales_query(ioQuery:SalesQuerySchema=Depends(SalesQueryParameterDepend),db:Session=Depends(get_db)):
    try:
        return sales_handler.query_data(ioQuery,db)
    except BaseException as e:
        return Response(status_code=404,content=str(e))
