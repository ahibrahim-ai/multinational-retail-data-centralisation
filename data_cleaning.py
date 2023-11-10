import pandas as pd

class DataCleaning:
    def __init__(self) -> None:
        pass

    def clean_user_data(self, user_data_df):
        try:
            # Check if user_data_df is not provided
            if user_data_df is None:
                print("Error: No user data provided for cleaning.")
                return pd.DataFrame()

            # Check for NULL values
            user_data_df = user_data_df.dropna()

            # Handle errors with dates (assuming 'DateOfBirth' is the column containing dates)
            user_data_df['DateOfBirth'] = pd.to_datetime(user_data_df['DateOfBirth'], errors='coerce')

            # Handle incorrectly typed values (assuming 'Age' is a numeric column)
            user_data_df['Age'] = pd.to_numeric(user_data_df['Age'], errors='coerce')

            # Remove rows filled with the wrong information (example: where 'Category' is not in a predefined list)
            predefined_categories = ['A', 'B', 'C']
            user_data_df = user_data_df[user_data_df['Category'].isin(predefined_categories)]

            return user_data_df

        except Exception as e:
            print(f"Error cleaning user data: {e}")
            return pd.DataFrame()

