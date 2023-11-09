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