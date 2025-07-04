from pydantic import BaseModel
from fastapi import *
from typing import *
from App.constants import *

 
class item_creation_schema(BaseModel):
    item : str
    name : str
    stock_quantity : int
    stock_price : float
    class Config:
        orm_mode = True        #Pydantic Model Config


class update_item_schema(BaseModel):
    name : str
    stock_quantity : int
    stock_price : float 
    created_on : str
    class Config:
        orm_mode = True


class ItemsQuerySchema(BaseModel):
    ivColumnHeader:QueryItemData
    ivOperator:Operation
    value:Union[str,None]
    ivOrderBy:QueryOrderBy
    class Config:
        orm_mode = True

def ItemQueryParameterDepend(
        Fields : QueryItemData=Query(description="Field"),     # It Acts as Required when no Default
        Operator:Operation = Query(default="EQ"),
        Value : Union[str,None] = Query(default=None,description="Value on Field"),
        OrderBy:QueryOrderBy = Query(default='Ascending')
)->ItemsQuerySchema:
    return ItemsQuerySchema(
        ivColumnHeader=Fields,
        ivOperator=Operator,
        value=Value,
        ivOrderBy=OrderBy
    )    
 
