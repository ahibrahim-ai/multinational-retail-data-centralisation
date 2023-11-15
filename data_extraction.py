import pandas as pd
import tabula
from sqlalchemy import text 

class DataExtractor:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def read_rds_table(self, db_connector, table_name):
        try:
            # Check if the specified table exists in the database
            all_tables = db_connector.list_db_tables()
            if table_name not in all_tables:
                print(f"Error: Table '{table_name}' not found in the database.")
                return pd.DataFrame()

            # Read data from the specified table
            with self.db_engine.connect() as connection:
                query = text(f"SELECT * FROM {table_name}")
                result = connection.execute(query)
                data = result.fetchall()

            # Convert the result to a pandas DataFrame
            df = pd.DataFrame(data, columns=result.keys())
            return df

        except Exception as e:
            print(f"Error reading data from table {table_name}: {e}")
            return pd.DataFrame()    
    
    def retrieve_pdf_data(self, link):
        pdf_table = tabula.read_pdf(link, pages='all', multiple_tables=True)
        pdf_df = pd.concat(pdf_table)
        return pdf_df 
    
