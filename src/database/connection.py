# database/setup_db.py
import os
import psycopg2
from dotenv import load_dotenv
from typing import Optional
from pydantic import BaseModel

load_dotenv()

# ================== Connect to Database ==================
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")

def get_db_connection():
	return psycopg2.connect(
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)

# # ================== Setup ORM types ==================
# class MenuItems(BaseModel):
#   id:                  Optional[int] = None
#   title:               str
#   price:               float
#   image_url:           str
#   description:         str
#   main_category:       str
#   sub_category:        Optional[str] = None
  
# class Order(BaseModel):
#   id:                 Optional[int] = None
#   customer_id:        str
#   order_time:         
#   status:             str
#   total_price:        float

# class OrderItems(BaseModel):
#   id:                  Optional[int] = None 
#   order_id:            int
#   item_id:             int
#   quantity:            int
#   customizations:      str
   
