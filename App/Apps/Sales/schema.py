from pydantic import BaseModel
from typing import *
from fastapi import *
from App.constants import *

class sales_order_creation_schema(BaseModel):
    customer_name : str
    item : str 
    quantity : int 

class SalesQuerySchema(BaseModel):
    ivColumnHeader:QuerySalesData
    ivOperator:Operation
    value:Union[str,None]
    ivOrderBy:Union[QueryOrderBy,None]
    ivGroupBy:Union[QueryGroupBy,None]
    ivGroupBy_field:Union[QuerySalesData,None]

def SalesQueryParameterDepend(
       Fields : QuerySalesData=Query(description="Field"),     # It Acts as Required when no Default
       Operator:Operation = Query(default="EQ"),
       Value : Union[str,None] = Query(default=None,description="Value on Field"),
       OrderBy:QueryOrderBy = Query(default=None),
       GroupBy:QueryGroupBy=Query(default=None),
       GroupByField:QuerySalesData=Query(default=None)
)->SalesQuerySchema:
    return SalesQuerySchema(
        ivColumnHeader=Fields,
        ivOperator=Operator,
        value=Value,
        ivOrderBy=OrderBy,
        ivGroupBy=GroupBy,
        ivGroupBy_field=GroupByField
    )       