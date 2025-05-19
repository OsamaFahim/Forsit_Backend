from fastapi.responses import PlainTextResponse 
from fastapi import FastAPI, Query #fastapi to run the endpoints on browser
from typing import Optional  #ro run the endpoints without some parameters, for eg for sales, you can run /sales to view all sales
from datetime import date
from Database.Database_Manager import Database_Manager #this singelton class is resposible for creation of connection
from Database.Database_Schema import create_all_tables, populate_all_tables, reset_all_tables, create_indexes #this class creates schema
#Working of endpoints are done in these classes
from Endpoint_functionalities.sales import get_sales, revenue_daily, revenue_weekly, revenue_monthly, revenue_yearly, revenue_compare
from Endpoint_functionalities.inventory import get_inventory, update_inventory

# Initialize FastAPI app
app = FastAPI()

# Initialize DB
#This will give us the database connection and cursor which we can use, it will print 
#"The Database named {your db name from .env} is already created" or 
#"The Datavase named {your db name from .env} is already"
db = Database_Manager()

#NOTE: Uncomment only when you are required to use these functions, recreation requires resetting first, and then indexing is done, similarly
#for population
#Below are the function calls which helps create or reset schema, and also create indexing
#create_all_tables(db)  #Run this function call only once
#populate_all_tables(db)
#create_indexes(db)

#NOTE: Reset only when recreation is required, after that populate the tables again and indexing as well
#reset_all_tables(db)

#Default endpoint

@app.get("/", response_class=PlainTextResponse)
def show_welcome_text():
    return (
        "Welcome to Forsit_DB_Backend_Assignment,\n"
        "You can use the endpoints, the default one is welcome screen\n"
        "Examples of some are:\n"
        "http://127.0.0.1:8000/sales\n"
        "http://127.0.0.1:8000/revenue/daily\n"
        "http://127.0.0.1:8000/revenue/weekly\n"
        "http://127.0.0.1:8000/revenue/monthly\n"
        "http://127.0.0.1:8000/inventory\n"
        "For dates you could use the format ?start_date=YYYY-MM-DD&end_date=YYYY-MM-DD (after base link)\n")

#Below are the sales endpoints

@app.get("/sales")
def fetch_sales(start_date: Optional[date] = None,end_date: Optional[date] = None,product_id: Optional[int] = None,
category_id: Optional[int] = None):
    return get_sales(db, start_date, end_date, product_id, category_id)


@app.get("/revenue/daily")
def daily_revenue(start_date: Optional[date] = None, end_date: Optional[date] = None):
    return revenue_daily(db, start_date, end_date)


@app.get("/revenue/weekly")
def weekly_revenue(start_date: Optional[date] = None, end_date: Optional[date] = None):
    return revenue_weekly(db, start_date, end_date)


@app.get("/revenue/monthly")
def monthly_revenue(start_date: Optional[date] = None, end_date: Optional[date] = None):
    return revenue_monthly(db, start_date, end_date)


@app.get("/revenue/yearly")
def yearly_revenue(start_date: Optional[date] = None, end_date: Optional[date] = None):
    return revenue_yearly(db, start_date, end_date)


@app.get("/revenue/compare")
def compare_revenue(
    start_date1: date,
    end_date1: date,
    start_date2: date,
    end_date2: date,
    category_id: Optional[int] = None,
):
    return revenue_compare(db, start_date1, end_date1, start_date2, end_date2, category_id)


#Below are the inventory endpoints

@app.get("/inventory")
def fetch_inventory(low_stock_threshold: Optional[int] = Query(None, description="Only show stock <= this value")):
    return get_inventory(db, low_stock_threshold)


@app.post("/inventory/update")
def update_inventory_quantity(product_id: int, quantity: int):
    return update_inventory(db, product_id, quantity)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
