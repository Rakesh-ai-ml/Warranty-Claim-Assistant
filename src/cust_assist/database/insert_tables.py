import os
import requests
import pandas as pd
from pathlib import Path
from src.cust_assist.database.connection import get_connection
from dotenv import load_dotenv
load_dotenv()
from src.cust_assist.logger import logger

class InsertTables:

    def __init__(self):

        self.root_dir = Path(__file__).resolve().parents[3] 
        self.tables=['customers', 'products', 'orders', 'order_items', 'warranty_claims']
        self.url = "https://fabricate.tonic.ai/api/v1/workspaces/RakeshT/projects/My%20Project/versions/v1/api/"
        self.headers = {
                    "Authorization": f"Bearer {os.getenv('FABRICATE_API_KEY')}"
                    }
        

    def get_tables_csv(self):

        for i in self.tables:

            url = self.url + f"{i}"
            response = requests.get( url, headers=self.headers)

            data = response.json()
            df = pd.DataFrame(data)

            for col in df.select_dtypes(include=["object"]).columns:
                df[col] = (
                    df[col]
                    .astype(str)
                    .str.replace("\r", "", regex=False)
                    .str.strip()
                )
            
            df.to_csv(
                f"artifacts/data_ingestion/{i}.csv",
                index=False,
                lineterminator='\n'
            )

    def insert_tables(self):

        try:
            with get_connection() as conn:
                with conn.cursor() as cur:
                                
                    for i in self.tables:

                        file_path = (self.root_dir / "artifacts" / "data_ingestion" / f"{i}.csv").as_posix()
                                    
                        query= f"""LOAD DATA LOCAL INFILE '{file_path}'
                        INTO TABLE {i}
                        FIELDS TERMINATED BY ','
                        ENCLOSED BY '"'
                        LINES TERMINATED BY '\n'
                        IGNORE 1 ROWS;"""
                        logger.info(f"inserted data into {i} table")
                        cur.execute(query)

                conn.commit()

            logger.info("Executed tables insertion successfully")

        except Exception as e:
            print(e)

