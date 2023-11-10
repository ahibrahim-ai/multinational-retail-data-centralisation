class DataExtractor:
    def __init__(self, db_engine):
        self.db_engine = db_engine

    def read_data_from_table(self, table_name):
        try: 
            with self.db_engine.connect() as connection:
                query = f"SELECT * FROM (table_name)"
                result = connection.execute(query)
                data = result.fetchall()
                return data
        except Exception as e:
            print(f"Error reading data from table {table_name}: {e}")
            return []    
    
    def read_rds_table(self, table_name):
        try: 
            if table_name not in self.list_db_tables():
                print(f"Error: Table '{table_name}' does not exist.")
                return None
            
            query = f"SELECT * FROM (ta)"