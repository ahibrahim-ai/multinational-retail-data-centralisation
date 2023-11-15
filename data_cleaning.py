import pandas as pd
import numpy as np
import re

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
            user_data_df['date_of_birth'] = pd.to_datetime(user_data_df['date_of_birth'], errors='coerce')

            # Handle incorrectly typed values (assuming 'Age' is a numeric column)
            #user_data_df['Age'] = pd.to_numeric(user_data_df['Age'], errors='coerce')

            # Remove rows filled with the wrong information (example: where 'Category' is not in a predefined list)
            #predefined_categories = ['A', 'B', 'C']
            #user_data_df = user_data_df[user_data_df['Category'].isin(predefined_categories)]

            return user_data_df

        except Exception as e:
            print(f"Error cleaning user data: {e}")
            return pd.DataFrame()
    
    def clean_card_data(self, pdf_df):
            pdf_df.dropna()
            # pdf_df = pdf_df.replace('NULL', pd.NA, inplace=True)
            # remove any non digits from card number by converting to float
            # pdf_df['card_number'].dropna(inplace=True)
            # pdf_df['card_number'] = np.where(pdf_df['card_number'].astype(str).str.isalpha(), pdf_df['card_number'], None)
            pdf_df['card_number'] = pdf_df['card_number'].apply(lambda x: str(x) if x is not None and str(x).isdigit() else pd.NA)
            # define expiry date format
            # date_pattern = r'^(0[1-9]|1[0-2])/\d{2}$'
            # def validate_expiry_date(date_str):
            #     return re.fullmatch(date_pattern, str(date_str)) is not None
            # # remove null values and non conforming values
            pdf_df['expiry_date'] = pd.to_datetime(pdf_df['expiry_date'], errors='coerce',format='%m/%y')
            pdf_df['expiry_date'] = pdf_df['expiry_date'].dt.strftime('%m/%y')
            # pdf_df['valid_expiry_date'] = pdf_df['expiry_date'].apply(validate_expiry_date)
            # pdf_df['expiry_date'] = pd.to_datetime(pdf_df['expiry_date'], errors='coerce', format='%m/%y')
            pdf_df['card_provider'] = pdf_df['card_provider'].str.upper()
            pdf_df['date_payment_confirmed'] = pd.to_datetime(pdf_df['date_payment_confirmed'], errors='coerce')
            # pdf_df['date_payment_confirmed'] = pdf_df['date_payment_confirmed'].dt.strftime('%Y-%m-%d')
            pdf_df.dropna(inplace=True)
            return pdf_df
    