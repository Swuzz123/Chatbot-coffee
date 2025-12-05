# database/order_items.py
from typing import List
from .connection import get_db_connection

# ==================== CRUD: Order Items ====================
def initOrderItems():
  try:
    with get_db_connection() as conn:
      with conn.cursor() as cur:
        cur.execute(
          """
          CREATE TABLE IF NOT EXISTS order_items (
            id                SERIAL PRIMARY KEY,
            order_id          INTERGER NOT NULL REFERENCES orders(id) ON DELETE CASCADE,
            item_id           INTERGER NOT NULL REFERENCES menu_items(id) ON DELETE CASCADE,
            quantity          INTEGER NOT NULL DEFAULT 1,
            customizations    TEXT
          )
          """
        )
        conn.commit()
        print("Successfully create Order Items table!")
  except Exception as e:
    print(f"Cannot create Order Items table, reason: {e}")