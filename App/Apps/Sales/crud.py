import App.DataBase.models as models
from sqlalchemy.orm import Session
from fastapi import Depends
from App.DataBase.database import get_db
from typing import Annotated
from fastapi.encoders import jsonable_encoder
from App.Apps.Sales.schema import *
from App.constants import *

def read_sales(db: Session):
    # return db.query(models.Item).all()
    return db.query(models.SalesModel).filter(models.SalesModel.flag==1).all()

def data():
    return Annotated[Session,Depends(get_db)]

def create_item(db_data,db:Session,item_name,item_stock,price_each):
    "Appending Sales Data"
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

    "Updating Item Data"
    item = db.query(models.Item).filter(models.Item.item==item_name).first()
    item.stock_quantity = item.stock_quantity - item_stock
    item.stock_price = price_each*(item.stock_quantity)
    db.commit()
    db.refresh(item)

def read_sales_order(iv_sales_id,db:Session):
    osales = db.query(models.SalesModel).filter(models.SalesModel.item_id==iv_sales_id ).filter(models.Item.flag=='1').first()
    return jsonable_encoder(osales)

def update_data(db:Session,sales,item_name,item_stock,price_each):
    

    "Updating Sales Data"
    db.commit()
    db.refresh(sales)

    "Updating Items Data"
    item = db.query(models.Item).filter(models.Item.item==item_name).first()
    item.stock_quantity = item.stock_quantity - item_stock
    item.stock_price = price_each*(item.stock_quantity)
    db.commit()
    db.refresh(item)

    return sales  


def delete_data(db:Session,iv_sales_id):
    sales = db.query(models.SalesModel).filter(models.SalesModel.item_id==iv_sales_id ).filter(models.Item.flag=='1').first()
    sales.flag = 0
    db.commit()
    db.refresh(sales)
    return {"detail": "Sales Order deleted"} 


def sales_query(db:Session):
     return db.query(models.SalesModel) 

def customer_not_found(cust_name,db:Session):
    if db.query(models.Customer).filter(models.Customer.name==cust_name).filter(models.Customer.flag=='1').first() is None:
        return True
    
def item_not_found(item_name,db:Session):
    if db.query(models.Item).filter(models.Item.item==item_name ).filter(models.Item.flag=='1').first() is None: 
        return True
    
def quantity_exceeded(item_quantity,item_name,db:Session):
    if db.query(models.Item).filter(models.Item.item==item_name).first().stock_quantity<item_quantity :
        return True

def get_item_instance(item_name,db:Session):
    oitem = db.query(models.Item).filter(models.Item.item==item_name).first()
    return oitem

def get_sales_instance(iv_sales_id,db:Session):
    sales = db.query(models.SalesModel).filter(models.SalesModel.item_id==iv_sales_id).filter(models.SalesModel.flag=='1').first()
    return sales
    
def sales_id_not_found(iv_sales_id,db:Session):
    if db.query(models.SalesModel).filter(models.SalesModel.item_id==iv_sales_id).filter(models.SalesModel.flag=='1').first() is None: 
        return True

def is_item_deleted(item_name,db:Session):
    if db.query(models.Item).filter(models.Item.item==item_name).filter(models.Item.flag=='1').first() is None:
        return True
        