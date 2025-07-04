import App.DataBase.models as models
from sqlalchemy.orm import Session
from fastapi import Depends
from App.DataBase.database import get_db
from typing import Annotated
from fastapi.encoders import jsonable_encoder
from App.Apps.Customers.schema import *

def read_customers(db: Session):
    return db.query(models.Customer).filter(models.Customer.flag==1).all()

def data():
    return Annotated[Session,Depends(get_db)]

def create_customer(db_data,db:Session):
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

def read_customer(iv_id,db:Session):
    customer = db.query(models.Customer).filter(models.Customer.id==iv_id ).filter(models.Customer.flag=='1').first()
    return jsonable_encoder(customer)

def update_customer(db:Session,io_customer:create_customer_schema):
    customer = db.query(models.Customer).filter(models.Customer.name==io_customer.name).filter(models.Customer.flag=='1').first()
    customer.name = io_customer.name
    customer.country = io_customer.country
    customer.contact =io_customer.contact
    customer.city =io_customer.city
    db.commit()
    db.refresh(customer)
    return jsonable_encoder(customer)   

def delete_customer(db:Session,iv_id):
    customer = db.query(models.Customer).filter(models.Customer.id==iv_id ).filter(models.Customer.flag=='1').first()
    customer.flag = 0
    db.commit()
    db.refresh(customer)
    return {"detail": "Customer deleted"}   

def customer_duplicate(db:Session,cust_name):
      if db.query(models.Customer).filter(models.Customer.name==cust_name).first() is not None:
            return True
      
def customer_not_found(db:Session,iv_id):
     if db.query(models.Customer).filter(models.Customer.id==iv_id ).filter(models.Customer.flag=='1').first() is None:
          return True  

def customer_not_found_updation(cust_name,db:Session):
    if db.query(models.Customer).filter(models.Customer.name==cust_name ).filter(models.Customer.flag=='1').first() is  None:
         return True  

def customer_query(db:Session):
     return db.query(models.Customer)           