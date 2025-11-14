import sqlite3

conn = sqlite3.connect("database/ecommerce.db")
cursor = conn.cursor()

query = """
SELECT 
    c.first_name || ' ' || c.last_name AS customer_name,
    o.order_date,
    p.name AS product_name,
    oi.quantity,
    oi.unit_price,
    oi.line_total AS total_amount
FROM orders o
JOIN customers c ON c.customer_id = o.customer_id
JOIN order_items oi ON oi.order_id = o.order_id
JOIN products p ON p.product_id = oi.product_id
LIMIT 20;
"""

for row in cursor.execute(query):
    print(row)

conn.close()
