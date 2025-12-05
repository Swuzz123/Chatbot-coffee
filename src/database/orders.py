# database/orders.py
from .connection import Order
from .connection import get_db_connection

# ==================== CRUD: Order ====================
def initOrder():
  try:
    with get_db_connection() as conn:
      with conn.cursor() as cur:
        cur.execute(
          """
          CREATE TABLE IF NOT EXISTS order (
            id                SERIAL PRIMARY KEY,
            customer_id       VARCHAR(255) NOT NULL,
            status            VARCHAR(50) NOT NULL DEFAULT 'pending',
            total_price       NUMERIC(10, 2),
            order_time        TIMESTAMP DEFAULT NOW()
          )
          """
        )
        conn.commit()
        print("Successfully create Order table!")
  except Exception as e:
    print(f"Cannot create Order table, reason: {e}")
    
def insertOrder(order: Order) -> int:
  try:
    with get_db_connection() as conn:
      with conn.cursor() as cur:
        cur.execute(
          """
          INSERT INTO order (
            customer_id, status, total_price, order_time
          ) VALUES (%s, %s, %s, %s)
          RETURNING id
          """,
          (
            order.customer_id,
            order.status,
            order.total_price,
            order.order_time
          )
        )
        order_id = cur.fetchone()[0]
        conn.commit()
        print(f"Insert order {order_id} successfully!")
        return order_id
  except Exception as e:
    print(f"Cannot insert order {id}, reason: {e}")
    raise
  
def updateOrderStatus(order_id: int, new_status: str) -> None:
  try:
    with get_db_connection() as conn:
      with conn.cursor() as cur:
        cur.execute(
          """
          UPDATE order SET status = %s WHERE id = order_id
          """, (new_status, order_id)
        )
        conn.commit()
  except Exception as e:
    print(f"Cannot update order status, reason: {e}")
    raise

def getOrderStatus(order_id: int) -> str:
  try:
    with get_db_connection() as conn:
      with conn.cursor() as cur:
        cur.execute(
          """
          SELECT
            status, total_price
          FROM order
          WHERE id = %s
          """, (order_id,)
        )
        order = cur.fetchone()
        if order:
          return f"Order ID: {order_id} status: {order['status']}. Total price: {order['total_price']} VNĐ"
        else:
          return f"Order ID: {order_id} not found"
  except Exception as e:
    print(f"Cannot get order status, reason: {e}")
    return ""   