# agent/tools.py
from langchain.tools import tool
from src.utils.settings import mappings
from src.utils.helpers import QueryClassifier
from src.database.menu_items import (
  getExactItem, 
  getTopItemsFromSub, 
  getTopItemsFromMain
)

# ================== TOOLS USAGE ==================
@tool
def hand_customer_query(query: str) -> list[str]:
  """Tool to find drink or food according to the customer's request"""
  qc = QueryClassifier(mappings)
  classification = qc.classify_query(query)
  
  if classification["type"] == "item":
    return getExactItem(classification["keyword"])

  elif classification["type"] == "sub_category":
    return getTopItemsFromSub(classification["keyword"])

  elif classification["type"] == "main_category":
    return getTopItemsFromMain(classification["keyword"])

  else:
    return ["Tôi chưa hiểu bạn muốn uống gì. Bạn có thể mô tả rõ hơn không?"]
  
  
tools = [hand_customer_query]
  

