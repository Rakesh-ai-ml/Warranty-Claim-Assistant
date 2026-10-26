from crewai.tools import BaseTool
from src.cust_assist.database.connection import get_connection

class VerifySerialTool(BaseTool):
    
    name : str = "verify_serial"
    description : str = "Verify product serial number"

    def _run(self, serial_number: str):
        
        serial_number = serial_number.strip()
        serial_number = (
        serial_number
        .strip()
        .replace("\r", "")
        .replace("\n", "")
    )

        print("CLEAN:", repr(serial_number))
        print(f"Searching for: {serial_number}")

        sql = """
        SELECT
            oi.serial_number,
            oi.order_id,
            p.product_name,
            o.order_date
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        JOIN orders o
            ON oi.order_id = o.order_id
        WHERE oi.serial_number = %s
        """

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (serial_number,))
                result = cur.fetchone()

        print("DB Result:", result)

        if not result:
            return "Invalid serial number"
        

        return result
