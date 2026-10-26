from crewai.tools import BaseTool
from src.cust_assist.database.connection import get_connection

class OrderDeliveryTool(BaseTool):
    name : str = "check_order_delivery"
    description : str = "Check whether order was delivered"

    def _run(self, order_id: int):

        sql = """
        SELECT status
        FROM orders
        WHERE order_id = %s
        """

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (order_id,))
                result = cur.fetchone()

        if not result:
            return "Order not found"

        return {
            "order_id": order_id,
            "delivered": result["status"] == "delivered"
        }