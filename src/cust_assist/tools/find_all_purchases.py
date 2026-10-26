from crewai.tools import BaseTool
from src.cust_assist.database.connection import get_connection

class CustomerPurchasesTool(BaseTool):
    
    name : str = "customer_purchases"
    description : str = "Get all purchased products by customer email"

    def _run(self, email: str):

        sql = """
        SELECT
            p.product_name,
            p.category,
            oi.serial_number,
            o.order_date,
            o.status
        FROM customers c
        JOIN orders o
            ON c.customer_id = o.customer_id
        JOIN order_items oi
            ON o.order_id = oi.order_id
        JOIN products p
            ON oi.product_id = p.product_id
        WHERE c.email = %s
        """

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (email,))
                return cur.fetchall()