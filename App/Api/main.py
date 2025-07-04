from fastapi import FastAPI
from App.DataBase.database import *
from App.Api.Items_api import router as ItemsData_router
from App.Api.Customer_api import router as CustomerData_router
from App.Api.Sales_api import router as SalesData_router
from App.Api.Login_api import router as LoginData_router



app = FastAPI()
create_table()



app.include_router(LoginData_router)
app.include_router(ItemsData_router)
app.include_router(CustomerData_router)
app.include_router(SalesData_router)


# import os 

# print(os.getenv("DATABASE_URL"))