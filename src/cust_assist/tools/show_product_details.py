from crewai.tools import BaseTool
from src.cust_assist.database.connection import get_connection

class ProductDetailsTool(BaseTool):
    name : str = "product_details"
    description : str = "Get product details"

    def _run(self, sku: str):

        sql = """
        SELECT *
        FROM products
        WHERE sku = %s
        """

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (sku,))
                return cur.fetchone()