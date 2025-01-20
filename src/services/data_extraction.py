"""
Module for data extraction.

This module contains functions for extracting company profile and current price data.
"""

import os
import time
from datetime import datetime
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import get_company_profile, get_sp500_constituents
from services.sync_launcher import sync_launcher

# def create_directories(ticker):
#     """
#     Create directories for raw data if they do not exist.

#     Args:
#         ticker (str): Ticker symbol.
#     """
#     if not os.path.exists(f"src/data/raw_data/{ticker}"):
#         os.makedirs(f"src/data/raw_data/{ticker}")
#     if not os.path.exists(f"src/data/raw_data/{ticker}/{ticker}_Company_Profile"):
#         os.makedirs(f"src/data/raw_data/{ticker}/{ticker}_Company_Profile")
  
def extraction(ticker, p_run_time):
    """
    Extract company profile and current price data.

    Args:
        ticker (str): Ticker symbol.
    """
    print(f"Ticker : {ticker}")
    # create_directories(ticker)
    get_company_profile(ticker, p_run_time)
    
def data_extraction():
    p_run_time = datetime.now()
    _, sectors, tickers_sector = get_sp500_constituents()
    for sector in sectors:
        print(f"\n######   Start Data Extraction | Sector :  {sector}  ######\n")  
        # Launch extraction for each ticker in parallel
        args_list = [(ticker, p_run_time) for ticker in tickers_sector[sector]]
        sync_launcher(extraction, args_list)
        print(f"\n######   End of Data Extraction | Sector :  {sector}  ######\n")
        time.sleep(15)
