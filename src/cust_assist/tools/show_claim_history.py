from crewai.tools import BaseTool
from src.cust_assist.database.connection import get_connection

class ClaimHistoryTool(BaseTool):
    name : str = "claim_history"
    description : str = "Get all claims for a customer"

    def _run(self, email: str):

        sql = """
        SELECT
            wc.claim_id,
            wc.claim_date,
            wc.status,
            p.product_name
        FROM warranty_claims wc
        JOIN order_items oi
            ON wc.order_item_id = oi.order_item_id
        JOIN orders o
            ON oi.order_id = o.order_id
        JOIN customers c
            ON o.customer_id = c.customer_id
        JOIN products p
            ON oi.product_id = p.product_id
        WHERE c.email = %s
        ORDER BY wc.claim_date DESC
        """

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (email,))
                return cur.fetchall()