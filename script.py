import pandas as pd
from database_utils import DatabaseConnector
from data_extraction import DataExtractor
from data_cleaning import DataCleaning

# Step 1: Instantiate the DatabaseConnector with credentials from the YAML file
connector = DatabaseConnector(credentials_file_path='db_creds.yaml')

# Step 2: Instantiate the DataExtractor and read data from the specified table
extractor = DataExtractor(db_engine=connector.engine)
table_name_to_extract = ""  # Replace with the actual table name
user_data_df = extractor.read_rds_table(db_connector=connector, table_name=table_name_to_extract)

# Step 3: Instantiate the DataCleaning class and clean the user data
cleaner = DataCleaning()
cleaned_user_data = cleaner.clean_user_data(user_data_df)

# Step 4: Specify the table name in the database for upload
table_name_to_upload = "dim_users"

# Step 5: Upload the cleaned user data to the specified table
connector.upload_to_db(df=cleaned_user_data, table_name=table_name_to_upload)
