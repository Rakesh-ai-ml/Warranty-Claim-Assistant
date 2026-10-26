from crewai.tools import BaseTool
from src.cust_assist.database.connection import get_connection

class FindCustomerTool(BaseTool):
    
    name : str = "find_customer"
    description : str = "Find customer using email address"

    def _run(self, email: str):

        sql = """
        SELECT *
        FROM customers
        WHERE email = %s
        """

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (email,))
                return cur.fetchone()