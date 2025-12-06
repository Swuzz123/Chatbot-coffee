# database/ingestion.py
from .menu_items import initMenuItems, insertItems
from .order_items import initOrderItems
from .orders import initOrder

def ingest_data(file_path: str):
  
  # Create Menu Items table and Insert data
  initMenuItems()
  insertItems(file_path)
  
  # Create Order and Order Items tables
  initOrder()
  initOrderItems()
    