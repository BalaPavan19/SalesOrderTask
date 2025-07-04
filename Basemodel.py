from sqlalchemy.orm import as_declarative
from sqlalchemy import Column,Integer,String

@as_declarative()
class Base():
    pass

class Users(Base):
    __tablename__ = "User"
    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)

print(Users.__tablename__)
print(type(Users.id))