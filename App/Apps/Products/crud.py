import App.DataBase.models as models
from sqlalchemy.orm import Session
from fastapi import Depends
from App.DataBase.database import get_db
from typing import Annotated
from fastapi.encoders import jsonable_encoder
from App.exceptions import *
from App.Apps.Products.schema import *
import datetime

def read_items(db: Session):
    # return db.query(models.Item).all()
    return db.query(models.Item).filter(models.Item.flag=='1').all()

def read_item(iv_item_id,db:Session):
    item = db.query(models.Item).filter(models.Item.item_id==iv_item_id ).filter(models.Item.flag=='1').first()
    return jsonable_encoder(item)
  
def create_item(db_data,db:Session):
    db.add(db_data)
    db.commit()
    db.refresh(db_data)

def update_data(db:Session,io_item:item_creation_schema):
    item = db.query(models.Item).filter(models.Item.item==io_item.item ).filter(models.Item.flag=='1').first()
    item.name = io_item.name
    item.stock_quantity =io_item.stock_quantity
    item.stock_price =io_item.stock_price
    db.commit()
    db.refresh(item)
    return jsonable_encoder(item)   
 
def delete_data(db:Session,iv_item_id):
    item = db.query(models.Item).filter(models.Item.item_id==iv_item_id ).filter(models.Item.flag=='1').first()
    item.flag = 0
    db.commit()
    db.refresh(item)
    return {"detail": "Item deleted"}   

def product_query(db:Session):
     return db.query(models.Item)    

def item_duplicate(db:Session,item_name):
      if db.query(models.Item).filter(models.Item.item==item_name).first() is not None:
            return True

def item_not_found(db:Session,iv_item_id):
     if db.query(models.Item).filter(models.Item.item_id==iv_item_id ) is None:
          return True
     elif db.query(models.Item).filter(models.Item.item_id==iv_item_id ).filter(models.Item.flag=='1').first() is None:
          return True

def item_not_found_updation(item_name,db:Session):
    if db.query(models.Item).filter(models.Item.item==item_name ) is None:
         return True
    elif db.query(models.Item).filter(models.Item.item==item_name ).filter(models.Item.flag=='1').first() is  None:
         return True