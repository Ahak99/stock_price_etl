########################## Save DATA locally ##########################

import os
import time
from datetime import datetime
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import get_latest_file, load_json_data, save_csv_files, get_sp500_constituents
from services.sync_launcher import sync_launcher
   
    
def transformation(ticker):
    print(f"Ticker : {ticker}")
        
    # Use the function with your specific file path
    json_file_path = get_latest_file(f"src/stock_price_etl/data/raw_data/{ticker}/{ticker}_Company_Profile/{ticker}_company_profile_*.json")

    if not os.path.exists(f"src/stock_price_etl/data/transformed_data/{ticker}"):
        os.makedirs(f"src/stock_price_etl/data/transformed_data/{ticker}")

    # Load JSON data and update CSVs by appending
    json_data = load_json_data(json_file_path)
    save_csv_files(ticker, json_data)
    
def data_transformation():
    _, sectors, tickers_sector = get_sp500_constituents()
    for sector in sectors:
        print(f"\n######   Start Data Transformation | Sector :  {sector}  ######\n")  
        # Launch Transformation for each ticker in parallel
        args_list = [(ticker) for ticker in tickers_sector[sector]]
        sync_launcher(transformation, args_list)
        print(f"\n######   End of Data Transformation | Sector :  {sector}  ######\n")
        time.sleep(5)

# def data_transformation(ticker):
#     print(f"Ticker : {ticker}")
        
#     # Use the function with your specific file path
#     json_file_path = get_latest_file(f"data/raw_data/{ticker}/{ticker}_Company_Profile/{ticker}_company_profile_*.json")

#     if not os.path.exists(f"data/transformed_data/{ticker}"):
#         os.makedirs(f"data/transformed_data/{ticker}")

#     # Load JSON data and update CSVs by appending
#     json_data = load_json_data(json_file_path)
#     save_csv_files(ticker, json_data)

# data_transformation()












# ########################## Save DATA in s3 ##########################

# import os
# import sys
# from utils import get_latest_file_from_s3, load_json_from_s3, save_csv_files

# sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# def data_transformation(ticker):
#     bucket_name = "smap-data-bucket"
    
#     print(f"Processing Ticker: {ticker}")

#     # Get the latest file path for the current ticker in the raw data bucket
#     json_file_key = get_latest_file_from_s3(bucket_name, f"raw_data_bucket/{ticker}/{ticker}_Company_Profile/")
        
#     if json_file_key is None:
#         print(f"No files found for {ticker} in raw data bucket.")

#     # Load JSON data from S3 using the latest file path
#     json_data = load_json_from_s3(bucket_name, json_file_key)

#     # Ensure transformed data path exists in the transformed_data_bucket
#     s3_folder_key = f"transformed_data_bucket/{ticker}/"
#     # os.makedirs(s3_folder_key, exist_ok=True)
        
#     # Save each CSV section to S3 using the JSON data
#     save_csv_files(ticker, json_data, bucket_name)
        
#     print("\n **************** Processing Complete ****************\n")
