from pydantic import BaseModel
from App.constants import *
from fastapi import *
from typing import *

class create_customer_schema(BaseModel):
    name:str
    contact:int
    country:str
    city:str

class CustomerQuerySchema(BaseModel):
    ivColumnHeader:QueryCustomersData
    ivOperator:Operation
    value:Union[str,None]
    ivOrderBy:QueryOrderBy

def CustomerQueryParameterDepend(
        Fields : QueryCustomersData=Query(description="Field"),     # It Acts as Required when no Default
        Operator:Operation = Query(default="EQ"),
        Value : Union[str,None] = Query(default=None,description="Value on Field"),
        OrderBy:QueryOrderBy = Query(default='Ascending')
)->CustomerQuerySchema:
    return CustomerQuerySchema(
        ivColumnHeader=Fields,
        ivOperator=Operator,
        value=Value,
        ivOrderBy=OrderBy
    )       