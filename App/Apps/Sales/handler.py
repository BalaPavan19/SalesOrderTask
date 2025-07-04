from sqlalchemy.orm import Session
from App.Apps.Sales.crud import *
from App.Apps.Sales.schema import *
from App.DataBase.models import SalesModel,Item,Customer
from App.exceptions import *
from fastapi import Response
import random
import datetime
from sqlalchemy import desc,func
from App.Apps.Sales.schema import *

class sales_handler():
    
    @staticmethod
    def read_data(db:Session):
     return read_sales(db)
    
    @staticmethod
    def create_data(io_sales_order_creation:list[sales_order_creation_schema],db:Session):
       cnt = 0
       for io_item in io_sales_order_creation:
            cust_name = io_item.customer_name
            item_name = io_item.item
            item_quantity = io_item.quantity
            if customer_not_found(cust_name,db):
                raise RecordNotFound(f"Record Not Found {io_item.customer_name}")
            elif item_not_found(item_name,db):
                raise RecordNotFound(f"Record Not Found {io_item.item}")
            elif quantity_exceeded(item_quantity,item_name,db):
                raise ExceededQuantity(f"Quantity got Exceeded over Items stock Quantity")
            else:
                cnt += 1
                ares = []
                item_instance = get_item_instance(item_name,db)
                inum = random.randint(0,99)
                if item_instance.stock_quantity <= 0 :
                    raise LessQuantity(f"Products Stock Qunatity is Empty")
                else:
                    price_each = ((item_instance.stock_price)//(item_instance.stock_quantity))
                db_data = SalesModel( item =io_item.item,
                                     item_id = io_item.item[0:2]+str(inum),
                                     order_id = str(db.query(SalesModel).count())+str(cnt) if db.query(SalesModel).count() > 0 else str('1'+str(cnt)),
                                    customer_name =io_item.customer_name, 
                                    quantity =io_item.quantity,
                                    price = price_each*io_item.quantity,
                                    created_on = datetime.datetime.now().strftime("%Y-%m-%d"),
                                    flag = 1 )
                ares.append(jsonable_encoder(db_data))
                item_name = io_item.item
                item_stock = io_item.quantity
                create_item(db_data,db,item_name,item_stock,price_each)
       return ares
    
    @staticmethod
    def read(iv_sales_id:str,db:Session):
        if sales_id_not_found(iv_sales_id,db):
            raise RecordNotFound("Record Not Found")
        else:
            return read_sales_order(iv_sales_id,db)
        
    @staticmethod    
    def updation(iv_sales_id:str,io_item:sales_order_creation_schema,db:Session):   
        
        item_name = io_item.item
        item_quantity = io_item.quantity
        sales = get_sales_instance(iv_sales_id,db)
        if sales_id_not_found(iv_sales_id,db):
            raise RecordNotFound(f"Record Not Found {iv_sales_id}")
        elif item_not_found(item_name,db):
            raise RecordNotFound(f"Record Not Found {io_item.item}") 
        elif is_item_deleted(item_name,db):
            raise RecordNotFound(f"Record Not Found {io_item.item}") 
        elif quantity_exceeded(item_quantity,item_name,db):
            raise ExceededQuantity(f"Quantity got Exceeded over Items stock Quantity")
        else:
            item = get_item_instance(item_name,db)
            if item.stock_quantity <= 0 :
                raise LessQuantity(f"Products Stock Qunatity is Empty")
            else:
                price_each = ((item.stock_price)//(item.stock_quantity))
            sales.customer_name = io_item.customer_name
            sales.item =io_item.item
            item.stock_quantity = item.stock_quantity+sales.quantity
            sales.quantity =io_item.quantity
            sales.price = price_each*io_item.quantity
            item_name = io_item.item
            item_stock = io_item.quantity
            return update_data(db,sales,item_name,item_stock,price_each)  
        
    @staticmethod
    def deletion(iv_sales_id:str,db:Session):
         
        if sales_id_not_found(iv_sales_id,db):
            raise RecordNotFound("Record Not Found")
        else:
            # db.delete(sales)
            return delete_data(db,iv_sales_id)

    @staticmethod    
    def query_data(ioQuery:SalesQuerySchema,db:Session):
        Fields=getattr(SalesModel,ioQuery.ivColumnHeader)
        Operator = ioQuery.ivOperator
        Value = ioQuery.value
        OrderBy = ioQuery.ivOrderBy
        GroupBy = ioQuery.ivGroupBy
        if ioQuery.ivGroupBy_field != None:
            GroupByField = getattr(SalesModel,ioQuery.ivGroupBy_field)
        if Operator == 'EQ':
             condition = Fields == Value
        elif Operator == 'GT':
             condition = Fields > Value
        elif Operator == 'LT':
             condition = Fields < Value   
        osales = sales_query(db).filter(condition)          
        if Value != None:
              if OrderBy == 'Ascending':
                     osales = osales.order_by(Fields)
              elif OrderBy == 'Descending':
                     osales = osales.order_by(desc(Fields))             
        else:
            if OrderBy == 'Ascending':
              osales = sales_query(db).order_by(Fields)
            elif OrderBy == 'Descending':
              osales = sales_query(db).order_by(desc(Fields))       
        if GroupBy != None:
            groupby={
                "sum":func.sum,
                "count":func.count,
                "max":func.max,
                "min":func.min
            }
            numerical_fields = ['Sales.quantity','Sales.price']
            if groupby[GroupBy.value]=='sum' and GroupByField not in numerical_fields:
                raise RecordNotFound(f"Aggregation Supported to Numerical Only")
            else:
                osales = db.query(Fields,groupby[GroupBy.value](GroupByField)).group_by(Fields).all()    # List of Tuple ga Returning
            print(osales)
            li =[{i[0]:i[1]} for i in osales]
            return li
        return osales.all()   