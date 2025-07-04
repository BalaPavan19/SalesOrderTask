from App.Apps.Customers.crud import *
from App.Apps.Customers.schema import *
from App.DataBase.database import *
from App.DataBase.models import Customer
from App.exceptions import *
import random
from fastapi import Response
from fastapi.encoders import jsonable_encoder
from sqlalchemy import desc

class customer_handler():
    
    @staticmethod
    def read_data(db:Session):
     return read_customers(db)
    
    @staticmethod
    def create_data(io_customer_li:list[create_customer_schema],db:Session):
        for io_customer in io_customer_li:
            cust_name = io_customer.name
            if customer_duplicate(db,cust_name):
                 raise DupliacteRecord(f"Record Already Exists for {cust_name}, You can Update It")
            else:
                ares = []
                inum = random.randint(0,99)
                db_data = Customer( name =io_customer.name, 
                                    country = io_customer.country,
                                    contact = io_customer.contact,
                                    city = io_customer.city,
                                    id = io_customer.name[0:1]+io_customer.country[0:1]+str(inum),
                                    flag = 1 )
                ares.append(jsonable_encoder(db_data))
                create_customer(db_data,db)
        return ares 
     
    
    @staticmethod
    def read(iv_id:str,db:Session):
        if customer_not_found(db,iv_id):
            raise RecordNotFound("Record Not Found")
        else:
            return read_customer(iv_id,db)
    
    @staticmethod
    def updation(io_customer:create_customer_schema,db:Session):
        cust_name = io_customer.name
        if customer_not_found_updation(cust_name,db):
            raise RecordNotFound("Record Not Found")
        else:
            return update_customer(db,io_customer)
       
    
    @staticmethod
    def deletion(iv_id:str,db:Session):
        if customer_not_found(db,iv_id):
            raise RecordNotFound("Record Not Found")
        else:
            return delete_customer(db,iv_id)

    @staticmethod    
    def query_data(ioQuery:CustomerQuerySchema,db:Session):
        Fields=getattr(Customer,ioQuery.ivColumnHeader)
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
                     ocust = customer_query(db).filter(condition).order_by(Fields).all()
              else:
                     ocust = customer_query(db).filter(condition).order_by(desc(Fields)).all()
        else:
            if OrderBy == 'Ascending':
              ocust = customer_query(db).order_by(Fields).all()
            else:
              ocust = customer_query(db).order_by(desc(Fields)).all()        

        return ocust     