from App.Apps.Products.crud import *
from App.Apps.Products.schema import *
from App.DataBase.database import *
from App.DataBase.models import Item
from App.exceptions import *
import random
import datetime
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc

class item_handler():
    
    @staticmethod
    def read_data(db:Session):
     return read_items(db)
    
    @staticmethod
    def create_data(io_item_li:list[item_creation_schema],db:Session):
        for io_item in io_item_li:
            item_name = io_item.item
            if item_duplicate(db,item_name):
                 raise DupliacteRecord(f"Record Already Exists for {item_name}, You can Update It")
            else:
                ares = []
                inum = random.randint(0,99)
                db_data = Item( item =io_item.item,
                                name =io_item.name, 
                                item_id=io_item.item[0:2]+str(inum),
                                stock_quantity =io_item.stock_quantity,
                                stock_price =io_item.stock_price,
                                created_on = datetime.datetime.now().strftime("%Y-%m-%d"),
                                flag = 1 )
                ares.append(jsonable_encoder(db_data))
                create_item(db_data,db)
        return ares        
    
    @staticmethod
    def read(iv_item_id:str,db:Session):
        if item_not_found(db,iv_item_id):
            raise RecordNotFound("Record Not Found")
        else:
            return read_item(iv_item_id,db)
     
    @staticmethod
    def updation(io_item:item_creation_schema,db:Session):
        item_name = io_item.item
        if item_not_found_updation(item_name,db):
            raise RecordNotFound("Record Not Found")
        else:
            return update_data(db,io_item)
    
    @staticmethod
    def deletion(iv_item_id:str,db:Session):
        if item_not_found(db,iv_item_id):
            raise RecordNotFound("Record Not Found")
        else:
            return delete_data(db,iv_item_id)

    @staticmethod   
    def query_data(ioQuery:ItemsQuerySchema,db:Session):
        Fields=getattr(Item,ioQuery.ivColumnHeader)
        Operator = ioQuery.ivOperator
        Value = ioQuery.value
        OrderBy = ioQuery.ivOrderBy
        if Operator == 'EQ':
             condition = Fields == Value
        elif Operator == 'GT':
             condition = Fields > Value
        if Operator == 'LT':
             condition = Fields < Value          
        if Value != None:
              if OrderBy == 'Ascending':
                     oitem = product_query(db).filter(condition).order_by(Fields).all()
              else:
                     oitem = product_query(db).filter(condition).order_by(desc(Fields)).all()
        else:
            if OrderBy == 'Ascending':
              oitem = product_query(db).order_by(Fields).all()
            else:
              oitem = product_query(db).order_by(desc(Fields)).all()        

        return oitem