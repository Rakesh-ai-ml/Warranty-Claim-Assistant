from crewai.tools import BaseTool
from src.cust_assist.database.connection import get_connection

class CreateClaimTool(BaseTool):
    name : str = "create_claim"
    description : str = "Create warranty claim"

    def _run(
        self,
        serial_number: str,
        issue_description: str
    ):

        find_sql = """
        SELECT order_item_id
        FROM order_items
        WHERE serial_number = %s
        """

        insert_sql = """
        INSERT INTO warranty_claims
        (
            order_item_id,
            issue_description,
            status
        )
        VALUES
        (
            %s,
            %s,
            'submitted'
        )
        """

        with get_connection() as conn:

            with conn.cursor() as cur:

                cur.execute(find_sql, (serial_number,))
                item = cur.fetchone()

                if not item:
                    return "Serial number not found"

                cur.execute(
                    insert_sql,
                    (
                        item["order_item_id"],
                        issue_description
                    )
                )

                conn.commit()

                return {
                    "claim_id": cur.lastrowid,
                    "status": "submitted"
                }