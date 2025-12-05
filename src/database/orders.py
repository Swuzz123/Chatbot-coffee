# database/orders.py
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