import os
import time
from datetime import datetime
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import s3fs
from utils import get_latest_file, load_json_data, save_csv_files, get_sp500_constituents
from services.sync_launcher import sync_launcher
   
    
def transformation(ticker):
    print(f"Ticker : {ticker}")
        
    # Use the function with your specific file path
    json_file_path = get_latest_file(f"s3://stocks-etl-bucket/raw_data/{ticker}/{ticker}_Company_Profile/{ticker}_company_profile_*.json")

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


