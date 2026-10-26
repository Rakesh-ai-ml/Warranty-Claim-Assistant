from crewai.tools import BaseTool
from src.cust_assist.database.connection import get_connection

class ClaimStatusTool(BaseTool):
    name : str = "claim_status"
    description : str = "Check current claim status"

    def _run(self, claim_id: int):

        sql = """
        SELECT *
        FROM warranty_claims
        WHERE claim_id = %s
        """

        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (claim_id,))
                return cur.fetchone()