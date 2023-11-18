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
            # fix address
            s_df = user_data_df['address'].str.split('\n', expand=True)
            s_df.columns = ['address-line-1', 'address-line-2', 'address-line-3', 'postcode']
            s_df['postcode'].replace('None', pd.NA)
            user_data_df = pd.concat([user_data_df, s_df], axis=1)
            user_data_df = user_data_df[['index', 'first_name', 'last_name', 'date_of_birth', 
                                         'company', 'email_address', 'address-line-1', 
                                         'address-line-2', 'address-line-3', 'postcode', 
                                         'address', 'country', 'country_code', 'phone_number', 'join_date', 'user_uuid']]
            user_data_df.drop(labels='index', axis=1, inplace=True)
            user_data_df.drop(labels='address', axis=1, inplace=True)
            # Check for NULL values
            user_data_df = user_data_df.dropna()
            # Handle errors with dates
            user_data_df['date_of_birth'] = pd.to_datetime(user_data_df['date_of_birth'], errors='coerce')
            return user_data_df
        except Exception as e:
            print(f"Error cleaning user data: {e}")
            return pd.DataFrame()
    
    def clean_card_data(self, pdf_df):
        try:
            pdf_df.dropna()
            # remove any characters in card number
            pdf_df['card_number'] = pdf_df['card_number'].apply(lambda x: str(x) if x is not None and str(x).isdigit() else pd.NA)
            # # remove null values and non conforming values
            pdf_df['expiry_date'] = pd.to_datetime(pdf_df['expiry_date'], errors='coerce',format='%m/%y')
            pdf_df['expiry_date'] = pdf_df['expiry_date'].dt.strftime('%m/%y')
            pdf_df['card_provider'] = pdf_df['card_provider'].str.upper()
            pdf_df['date_payment_confirmed'] = pd.to_datetime(pdf_df['date_payment_confirmed'], errors='coerce')
            pdf_df.dropna(inplace=True)
            return pdf_df
        except Exception as e:
            print(f"Error cleaning user data: {e}")
            return pd.DataFrame()
    
    def clean_store_data(self, all_stores_df):
        try:
            # remove unnecessary lat column
            all_stores_df.drop(labels=['lat'], axis=1, inplace=True)
            all_stores_df.replace('NULL', pd.NA, inplace=True)
            # Start fixing address. 1: split up info in address column.
            split_df = all_stores_df['address'].str.split('\n', expand=True)
            split_df.columns = ['address-line-1', 'Name', 'address-line-2', 'postcode']
            # 2:reorder columns
            split_df = split_df[['Name', 'address-line-1', 'address-line-2', 'postcode']]
            split_df['Name'] = split_df['Name'].str.title()
            # 3: Remove repeated info
            split_df['postcode'] = split_df['postcode'].str.replace(r',.*', '', regex=True)
            # 4: join onto df
            all_stores_df = pd.concat([all_stores_df, split_df], axis=1)
            # 5: format date
            all_stores_df['opening_date'] = pd.to_datetime(all_stores_df['opening_date'], errors='coerce', format='%Y-%m-%d')
            #6: reorder columns
            all_stores_df = all_stores_df[['Name', 'address-line-1', 'address-line-2', 'postcode',
                                            'locality', 'opening_date', 'store_code', 'store_type', 
                                            'staff_numbers', 'country_code', 'continent', 'longitude', 
                                            'latitude', 'address', 'index']]
            # drop address and index column
            all_stores_df.drop(labels='index', axis=1, inplace=True)
            all_stores_df.drop(labels='address', axis=1, inplace=True)
            # 7: remove null values
            all_stores_df.dropna(inplace=True)
            return all_stores_df
        except Exception as e:
            print(f"Error cleaning user data: {e}")
            return pd.DataFrame()