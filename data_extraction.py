import pandas as pd
import tabula
import requests 
from sqlalchemy import text 
import boto3 
from io import StringIO

class DataExtractor:
    def __init__(self, db_engine):
        self.db_engine = db_engine
        self.base_url = "https://aqj7u5id95.execute-api.eu-west-1.amazonaws.com/prod/" 
        self.header = {'x-api-key': 'yFBQbwXe9J3sd6zWVAMrK6lcxxr0q1lr2PT6DDMX'}
        self.s3_client = boto3.client('s3')

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
    
    def list_stores(self, endpoint):
        url = self.base_url + endpoint
        response = requests.get(url, headers=self.header)
        print(f'API Response: {response.text}')

        if response.status_code == 200:
            try:
                data = response.json()
                number_of_stores = data.get('number_stores')
                return number_of_stores
            except Exception as e:
                print(f"Error parsing JSON: {e}")
                return None
        else:
            print(f"Error: {response.status_code}")
            return None
    
    def retrieve_stores_data(self, retrieve_store_endpoint, store_numbers):
        all_stores = []

        for store_number in store_numbers:
            endpoint = retrieve_store_endpoint.format(store_number=store_number)
            store_data = self.retrieve_single_store_data(endpoint)

            if store_data is not None:
                all_stores.append(store_data)
            else:
                print(f'Error reaching')
        if all_stores:
            all_stores_df = pd.DataFrame(all_stores)
            return all_stores_df
        else:
            return None
        
    def retrieve_single_store_data(self, endpoint):
        
        response = requests.get(endpoint, headers=self.header)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error for store {endpoint}: {response.status_code}")
            return None
    
    def extract_from_s3(self, s3_address):
        try:
            bucket, key = s3_address.replace("s3://", "").split("/", 1)
            file_content = self.s3_client.get_object(Bucket=bucket, Key=key)['Body'].read().decode('utf-8')
            return pd.read_json(StringIO(file_content))

        except Exception as e:
            print(f"Error extracting data from S3: {e}")
            return None
