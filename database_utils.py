import yaml
import sqlalchemy 
import psycopg2
from sqlalchemy import create_engine, MetaData

class DatabaseConnector:
    def __init__(self, credentials_file_path) -> None:
        self.credentials_file_path = credentials_file_path
        self.credentials = self.read_db_creds()
        self.engine = self.init_db_engine()

    def read_db_creds(self):
        try:
            with open(self.credentials_file_path, 'r') as file:
                credentials = yaml.safe_load(file)
                return credentials
        except FileNotFoundError:
            print(f"Error: File not found at {self.credentials_file_path}")
        except yaml.YAMLError as e:
            print(f"Error reading YAML file: {e}")

    def init_db_engine(self):
        try:
            db_url = (
                f"postgresql://{self.credentials['RDS_USER']}:{self.credentials['RDS_PASSWORD']}@"
                f"{self.credentials['RDS_HOST']}:{self.credentials['RDS_PORT']}/{self.credentials['RDS_DATABASE']}"
            )
            engine = create_engine(db_url)
            return engine
        except (KeyError, TypeError) as e:
            print(f"Error: Missing key in credentials - {e}")
        except Exception as e:
            print(f"Error initializing database engine: {e}")
    
    def list_db_tables(self):
        try:
            metadata = MetaData()
            metadata.reflect(bind=self.engine)
            table_names = metadata.tables.keys()
            return table_names
        except Exception as e:
            print(f"Error listing database tables: {e}")
            return []
        
    def upload_to_db(self, df, table_name):
        try:
            # Create a new engine with a specific isolation level
            engine_with_transaction = create_engine(
                self.engine.url,
                isolation_level="AUTOCOMMIT"  # Choose the appropriate isolation level
            )

            with engine_with_transaction.connect() as connection:
                # Upload the DataFrame to the specified table
                df.to_sql(name=table_name, con=connection, index=False, if_exists='replace')
                print(f"Data uploaded to table {table_name} successfully.")
        except Exception as e:
            print(f"Error uploading data to table {table_name}: {e}")

