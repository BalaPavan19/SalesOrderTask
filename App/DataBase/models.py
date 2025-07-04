from App.DataBase.database import Base
from sqlalchemy import Column,Integer,String,Float,Date,BigInteger
from sqlalchemy.orm import relationship

class Item(Base):
   __tablename__ = "Items"

   item_id= Column(String,primary_key=True)
   item = Column(String,nullable=False)
   name = Column(String)
   stock_quantity = Column(Integer)
   stock_price = Column(Float)
   created_on = Column(String)
   flag = Column(Integer)


class Customer(Base):
   __tablename__ = "Customers"

   id = Column(String,primary_key=True)
   name = Column(String,nullable=False)
   contact = Column(String)
   country = Column(String)
   city = Column(String)
   flag = Column(Integer)

class SalesModel(Base):
   __tablename__ = "Sales"  

   order_id = Column(String)
   item_id = Column(String,primary_key=True)
   customer_name = Column(String)
   item = Column(String,nullable=False)
   quantity = Column(Integer)
   price = Column(Float)   
   created_on = Column(Date)
   flag = Column(Integer)


class LoginModel(Base):
   __tablename__ = "Login"
   
   user_id = Column(String,primary_key=True)
   username = Column(String,nullable=False)
   password = Column(String,nullable=False)

# login = relationship('ClientModel', back_populates='client')


# class ClientModel(Base):
#    __tablename__ = "Client"

#    client_id = Column(String,primary_key=True)
#    client_secret = Column(String,nullable=False)

# client = relationship('LoginModel', back_populates='login')
