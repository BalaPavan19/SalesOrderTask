import re

def validatepassword(password):
    password_pattern = re.compile(r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[!@#$%^&*()-+=_]).{8,}$")   
    return bool(password_pattern.fullmatch(password))



from enum import Enum

class Operation(str,Enum):
    Eq = "EQ"
    Lt = "LT"
    Gt = "GT"
 
class QueryItemData(str,Enum):
    item_id = 'item_id'
    stock_quantity = 'stock_quantity'
    stock_price = 'stock_price'
    item = 'item'
    created_on = 'created_on'

class QuerySalesData(str,Enum):
    item_id = 'item_id'
    item = 'item'
    customer_name = 'customer_name'
    quantity = 'quantity'
    price = 'price'
    created_on = 'created_on'

class QueryGroupBy(str,Enum):
    count = 'count'
    sum = 'sum'
    min ='min'
    max = 'max'
    avg = 'avg'    

class QueryCustomersData(str,Enum):
    id = 'id'
    name = 'name'
    country = 'country'
    city = 'city'

class QueryOrderBy(str,Enum):
    Ascending = 'Ascending'
    Descending = 'Descending'
