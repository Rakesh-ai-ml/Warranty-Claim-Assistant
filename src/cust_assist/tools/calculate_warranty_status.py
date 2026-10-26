from datetime import datetime
from dateutil.relativedelta import relativedelta
from crewai.tools import BaseTool
from src.cust_assist.database.connection import get_connection

class WarrantyStatusTool(BaseTool):
    name : str = "warranty_status"
    description : str = "Check warranty status using serial number"

    def _run(self, serial_number: str):

        sql = """
        SELECT
            oi.serial_number,
            o.order_id,
            o.order_date,
            p.warranty_months,
            p.product_name
        FROM order_items oi
        JOIN orders o
            ON oi.order_id = o.order_id
        JOIN products p
            ON oi.product_id = p.product_id
        WHERE oi.serial_number = %s
        """

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (serial_number,))
                row = cur.fetchone()

        if not row:
            return "Serial number not found"

        expiry = row["order_date"] + relativedelta(
            months=row["warranty_months"]
        )

        active = datetime.now().date() <= expiry

        return {
            "order_id": row["order_id"],
            "product": row["product_name"],
            "purchase_date": str(row["order_date"]),
            "expiry_date": str(expiry),
            "warranty_active": active
        }