########################## Save data locally ##########################

import os
import json
from datetime import datetime
import pandas as pd # type: ignore
import re
import glob
import yfinance as yf # type: ignore

# *******************   Extract   *******************
# Function to get S&P 500 constituents from Wikipedia
def get_sp500_constituents():
    # URL of the Wikipedia page containing the S&P 500 constituent list
    sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'

    # Read the first table from the Wikipedia page
    sp500_table = pd.read_html(sp500_url)[0]

    # Extract the 'Symbol' and 'Sector' columns
    tickers = sp500_table['Symbol'].tolist()  # Convert to list
    sectors = sp500_table['GICS Sector']

    # Add the S&P 500 index ticker (^GSPC) at the beginning of the tickers list
    sp500_index_ticker = "^GSPC"
    tickers.insert(0, sp500_index_ticker)  # Insert ^GSPC as the first ticker

    # Create a dictionary to hold tickers by sector
    tickers_sector = {
        "Real Estate": [],
        "Energy": [],
        "Information Technology": [],
        "Consumer Staples": [],
        "Utilities": [],
        "Health Care": [],
        "Industrials": [],
        "Consumer Discretionary": [],
        "Financials": [],
        "Communication Services": [],
        "Materials": []
    }

    # Populate the dictionary with tickers by sector
    for ticker, sector in zip(tickers[1:], sectors):  # Skip the first ticker (^GSPC)
        if sector:
            tickers_sector[sector].append(ticker)
        else:
            print(f"Unknown sector '{sector}' for ticker '{ticker}'")

    # Return the tickers list (with ^GSPC), unique sectors, and tickers by sector
    return tickers, set(sectors), tickers_sector

# Function to save data to a JSON file
def save_to_json(data, ticker, path, data_type, current_time):
    filename = f"{path}/{ticker}_{data_type}_{current_time}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Function to get company profile and stock info using yfinance
def get_company_profile(ticker, p_run_time):
    stock = yf.Ticker(ticker)
    
    data = stock.info  # Returns company information and stock data
    current_prices = stock.history(period="1d")
    if not current_prices.empty:
        data["Timestamp"] = current_prices.index[-1].strftime("%Y-%m-%d %H:%M")
    else:
        data["Timestamp"] = None
    if not current_prices.empty and not current_prices['Open'].empty:
        data["open"] = current_prices['Open'].iloc[-1]
    else:
        data["open"] = None
    if not current_prices.empty and not current_prices['High'].empty:
        data["high_price"] = current_prices['High'].iloc[-1]
    else:
        data["high_price"] = None
    if not current_prices.empty and not current_prices['Low'].empty:
        data["low_price"] = current_prices['Low'].iloc[-1]
    else:
        data["low_price"] = None
    if not current_prices.empty and not current_prices['Close'].empty:
        data["close"] = current_prices['Close'].iloc[-1]
    else:
        data["close"] = None
    
    data["PipelineRunTime"] = p_run_time.strftime("%Y-%m-%d %H:%M")
    save_to_json(data, ticker, f"src/stock_price_etl/data/raw_data/{ticker}/{ticker}_Company_Profile", "company_profile", p_run_time.strftime("%Y-%m-%d_%H-%M"))
    return data

# *******************   Transformation   *******************

# Normalization function
def normalize_value(value):
    if value is None:  # Return NaN if the value is None
        return float('nan')
        
    if isinstance(value, str):
        # Remove percentage signs and convert to decimal
        if "%" in value:
            return float(value.replace("%", "")) / 100
        # Handle billion (B), million (M), and thousand (K) notations
        if "B" in value:
            return float(value.replace("B", "")) * 1e9
        elif "M" in value:
            return float(value.replace("M", "")) * 1e6
        elif "K" in value:
            return float(value.replace("K", "")) * 1e3
        # Remove any other extraneous symbols like "$" and commas
        value = re.sub(r'[^\d.]', '', value)
    
    # Attempt to convert to float if not already
    try:
        return float(value)
    except (ValueError, TypeError):
        return float('nan')  # Return NaN if conversion fails
    
def get_latest_file(path):
    # Get a list of all matching files in the directory
    files = glob.glob(path)
    # Sort files based on modification time (newest first) and return the first one
    if files:
        latest_file = max(files, key=os.path.getmtime)
        return latest_file
    else:
        return None
  
# Function to load JSON data
def load_json_data(json_path):
    with open(json_path, 'r') as f:
        return json.load(f)

# Append data to CSV if it exists, or create new CSV if it doesn't
def append_to_csv(data_dict, filename):
    df = pd.DataFrame([data_dict])
    
    if os.path.isfile(filename):
        df.to_csv(filename, mode='a', header=False, index=False)  # Append without header
    else:
        df.to_csv(filename, mode='w', header=True, index=False)  # Write with header
      
def extract_company_profile(data):
    return {
        "PipelineRunTime": data.get("PipelineRunTime"),
        "Timestamp": data.get("Timestamp"),
        "Name": data.get("longName"),
        "Ticker Symbol": data.get("symbol"),
        "Industry/Sector": f"{data.get('industry')}, {data.get('sector')}",
        "Location": f"{data.get('city')}, {data.get('country')}",
        "Employees": normalize_value(data.get("fullTimeEmployees")),
    }

def extract_market_data(data):
    return {
        "PipelineRunTime": data.get("PipelineRunTime"),
        "Timestamp": data.get("Timestamp"),
        "Current Price": normalize_value(data.get("currentPrice")),
        "52-Week Range": f"{normalize_value(data.get('fiftyTwoWeekLow'))} - {normalize_value(data.get('fiftyTwoWeekHigh'))}",
        "Daily Range": f"{normalize_value(data.get('dayLow'))} - {normalize_value(data.get('dayHigh'))}",
        "Volume (Current)": normalize_value(data.get("volume")),
        "Average Volume (10 Days)": normalize_value(data.get("averageVolume10days")),
        "Market Cap": normalize_value(data.get("marketCap")),
        "Beta": normalize_value(data.get("beta")),
    }

def extract_valuation_ratios(data):
    return {
        "PipelineRunTime": data.get("PipelineRunTime"),
        "Timestamp": data.get("Timestamp"),
        "Trailing P/E": normalize_value(data.get("trailingPE")),
        "Forward P/E": normalize_value(data.get("forwardPE")),
        "PEG Ratio": normalize_value(data.get("pegRatio")),
        "Price-to-Book": normalize_value(data.get("priceToBook")),
        "Price-to-Sales": normalize_value(data.get("priceToSalesTrailing12Months")),
        "Enterprise Value": normalize_value(data.get("enterpriseValue")),
        "EV/Revenue": normalize_value(data.get("enterpriseToRevenue")),
        "EV/EBITDA": normalize_value(data.get("enterpriseToEbitda")),
    }

def extract_dividends_returns(data):
    return {
        "PipelineRunTime": data.get("PipelineRunTime"),
        "Timestamp": data.get("Timestamp"),
        "Dividend Rate": normalize_value(data.get("dividendRate")),
        "Dividend Yield": normalize_value(data.get("dividendYield")),
        "Payout Ratio": normalize_value(data.get("payoutRatio")),
        "5-Year Avg. Dividend Yield": normalize_value(data.get("fiveYearAvgDividendYield")),
        "Return on Assets (ROA)": normalize_value(data.get("returnOnAssets")),
        "Return on Equity (ROE)": normalize_value(data.get("returnOnEquity")),
    }

def extract_financial_health(data):
    return {
        "PipelineRunTime": data.get("PipelineRunTime"),
        "Timestamp": data.get("Timestamp"),
        "Total Cash": normalize_value(data.get("totalCash")),
        "Total Debt": normalize_value(data.get("totalDebt")),
        "Quick Ratio": normalize_value(data.get("quickRatio")),
        "Current Ratio": normalize_value(data.get("currentRatio")),
        "Debt-to-Equity": normalize_value(data.get("debtToEquity")),
        "Free Cash Flow": normalize_value(data.get("freeCashflow")),
        "Operating Cash Flow": normalize_value(data.get("operatingCashflow")),
    }

def extract_growth_metrics(data):
    return {
        "PipelineRunTime": data.get("PipelineRunTime"),
        "Timestamp": data.get("Timestamp"),
        "Revenue": normalize_value(data.get("totalRevenue")),
        "Revenue Growth (YoY)": normalize_value(data.get("revenueGrowth")),
        "Earnings Growth (YoY)": normalize_value(data.get("earningsGrowth")),
        "Gross Margin": normalize_value(data.get("grossMargins")),
        "EBITDA Margin": normalize_value(data.get("ebitdaMargins")),
        "Operating Margin": normalize_value(data.get("operatingMargins")),
    }

def extract_risk_assessment(data):
    return {
        "PipelineRunTime": data.get("PipelineRunTime"),
        "Timestamp": data.get("Timestamp"),
        "Overall Risk Score": normalize_value(data.get("overallRisk")),
        "Audit Risk": normalize_value(data.get("auditRisk")),
        "Compensation Risk": normalize_value(data.get("compensationRisk")),
        "Shareholder Rights Risk": normalize_value(data.get("shareHolderRightsRisk")),
    }

def extract_current_prices(data):
    return {
        "PipelineRunTime": data.get("PipelineRunTime"),
        "Timestamp": data.get("Timestamp"),
        "Open": normalize_value(data.get("open")),
        "Low": normalize_value(data.get("close")),
        "High": normalize_value(data.get("high_price")),
        "Close": normalize_value(data.get("low_price"))
    }

def extract_analyst_price_targets(data):
    return {
        "PipelineRunTime": data.get("PipelineRunTime"),
        "Timestamp": data.get("Timestamp"),
        "Target High Price": normalize_value(data.get("targetHighPrice")),
        "Target Low Price": normalize_value(data.get("targetLowPrice")),
        "Mean Price Target": normalize_value(data.get("targetMeanPrice")),
        "Median Price Target": normalize_value(data.get("targetMedianPrice")),
    }
    
# Function to process and append data for each section
def save_csv_files(ticker, json_data):
    try:
        # Define the sections to extract and append
        append_to_csv(extract_company_profile(json_data), f"src/stock_price_etl/data/transformed_data/{ticker}/{ticker}_Company_Profile.csv")
        append_to_csv(extract_market_data(json_data), f"src/stock_price_etl/data/transformed_data/{ticker}/{ticker}_Market_Data.csv")
        append_to_csv(extract_valuation_ratios(json_data), f"src/stock_price_etl/data/transformed_data/{ticker}/{ticker}_Valuation_Ratios.csv")
        append_to_csv(extract_dividends_returns(json_data), f"src/stock_price_etl/data/transformed_data/{ticker}/{ticker}_Dividends_and_Returns.csv")
        append_to_csv(extract_financial_health(json_data), f"src/stock_price_etl/data/transformed_data/{ticker}/{ticker}_Financial_Health.csv")
        append_to_csv(extract_growth_metrics(json_data), f"src/stock_price_etl/data/transformed_data/{ticker}/{ticker}_Growth_Metrics.csv")
        append_to_csv(extract_risk_assessment(json_data), f"src/stock_price_etl/data/transformed_data/{ticker}/{ticker}_Risk_Assessment.csv")
        append_to_csv(extract_current_prices(json_data), f"src/stock_price_etl/data/transformed_data/{ticker}/{ticker}_Current_Prices.csv")
        append_to_csv(extract_analyst_price_targets(json_data), f"src/stock_price_etl/data/transformed_data/{ticker}/{ticker}_Analyst_Price_Targets.csv")
    except Exception as e:
        print(f"Error appending Company Profile for ticker {ticker}: {e}")
# ########################## Save DATA in s3 ##########################

# import os
# import json
# from datetime import datetime
# import pandas as pd
# import re
# import glob
# import yfinance as yf # type: ignore
# from dotenv import load_dotenv

# # Load the .env file
# load_dotenv()

# from io import StringIO
# import boto3 # type: ignore
# import botocore.exceptions # type: ignore

# # Initialize boto3 S3 client
# s3_client = boto3.client("s3")
# bucket_name = "smap-data-bucket"

# # Function to save JSON data to S3
# def save_to_s3_json(data, ticker, path, data_type, current_time):
#     filename = f"{path}/{ticker}_{data_type}_{current_time}.json"
#     s3_client.put_object(
#         Body=json.dumps(data, indent=4),
#         Bucket=bucket_name,
#         Key=filename
#     )

# # Load JSON data from S3, given the bucket and file key
# def load_json_from_s3(bucket_name, json_key):
#     # Retrieve the file from S3
#     response = s3_client.get_object(Bucket=bucket_name, Key=json_key)
    
#     # Read and parse the JSON data
#     json_data = json.loads(response['Body'].read().decode('utf-8'))
#     return json_data

# # Function to save CSV data to S3
# def save_to_s3_csv(data_dict, filename):
#     csv_buffer = StringIO()
#     df = pd.DataFrame([data_dict])
#     df.to_csv(csv_buffer, index=False)
#     s3_client.put_object(Body=csv_buffer.getvalue(), Bucket=bucket_name, Key=filename)

# # Function to retrieve the latest file in a specific S3 directory
# def get_latest_file_from_s3(bucket_name, prefix):
#     # List objects in the specified S3 directory
#     response = s3_client.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    
#     # Check if files are returned, if not return None
#     if 'Contents' not in response:
#         return None
    
#     # Get the most recent file based on LastModified
#     latest_file = max(response['Contents'], key=lambda x: x['LastModified'])
#     return latest_file['Key']

# def append_to_csv_in_s3(ticker, data_dict, s3_key, bucket_name):
#     # Convert the new data_dict to a DataFrame
#     new_data_df = pd.DataFrame([data_dict])

#     try:
#         # Try to read the existing CSV file from S3
#         csv_obj = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
#         existing_data_df = pd.read_csv(csv_obj['Body'])

#         # Append the new data to the existing data
#         updated_data_df = pd.concat([existing_data_df, new_data_df], ignore_index=True)
#     except botocore.exceptions.ClientError as e:
#         # If the file does not exist, use the new data as the only content
#         if e.response['Error']['Code'] == "NoSuchKey":
#             print(f"{s3_key} not found in {bucket_name}. Creating new file.")
#             updated_data_df = new_data_df
#         else:
#             raise e

#     # Write the updated DataFrame back to a CSV in S3
#     csv_buffer = StringIO()
#     updated_data_df.to_csv(csv_buffer, index=False)
#     s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=csv_buffer.getvalue())

# #######################################################
# # *******************   Extract   ******************* #
# #######################################################

# def get_sp500_constituents():
#     sp500_url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
#     sp500_table = pd.read_html(sp500_url)[0]
#     tickers = sp500_table['Symbol'].tolist()
#     sectors = sp500_table['GICS Sector']
#     sp500_index_ticker = "^GSPC"
#     tickers.insert(0, sp500_index_ticker)
#     tickers_sector = {sector: [] for sector in sectors.unique()}
#     for ticker, sector in zip(tickers[1:], sectors):
#         tickers_sector[sector].append(ticker)
#     return tickers, set(sectors), tickers_sector

# def get_company_profile(ticker):
#     current_time = datetime.now()
#     stock = yf.Ticker(ticker)
#     data = stock.info
#     data["Timestamp"] = current_time.strftime("%Y-%m-%d %H:%M")
#     # data["PipelineRunTime"] = p_run_time
#     save_to_s3_json(data, ticker, f"raw_data_bucket/{ticker}/{ticker}_Company_Profile", "company_profile", current_time.strftime("%Y-%m-%d_%H-%M"))
#     return data

# def get_current_price(ticker):
#     stock = yf.Ticker(ticker)
#     data = stock.history(period="1d", interval="1m")
#     if not data.empty:
#         current_price = data['Close'].iloc[-1]
#         price_data = {
#             # "PipelineRunTime": p_run_time,
#             "Timestamp": data.index[-1].strftime("%Y-%m-%d %H:%M"),
#             "current_price": current_price
#         }
#         save_to_s3_json(price_data, ticker, f"raw_data_bucket/{ticker}/{ticker}_Current_Price", "current_price", data.index[-1].strftime("%Y-%m-%d_%H-%M"))
#         return price_data
#     else:
#         return {"error": "No real-time data available"}

# #########################################################
# # *******************   Transform   ******************* #
# #########################################################

# # Normalization function
# def normalize_value(value):
#     if value is None:  # Return NaN if the value is None
#         return float('nan')
        
#     if isinstance(value, str):
#         # Remove percentage signs and convert to decimal
#         if "%" in value:
#             return float(value.replace("%", "")) / 100
#         # Handle billion (B), million (M), and thousand (K) notations
#         if "B" in value:
#             return float(value.replace("B", "")) * 1e9
#         elif "M" in value:
#             return float(value.replace("M", "")) * 1e6
#         elif "K" in value:
#             return float(value.replace("K", "")) * 1e3
#         # Remove any other extraneous symbols like "$" and commas
#         value = re.sub(r'[^\d.]', '', value)
    
#     # Attempt to convert to float if not already
#     try:
#         return float(value)
#     except (ValueError, TypeError):
#         return float('nan')  # Return NaN if conversion fails

# def extract_company_profile(data):
#     return {
#         # "PipelineRunTime": data.get("PipelineRunTime"),
#         "Timestamp": data.get("Timestamp"),
#         "Name": data.get("longName"),
#         "Ticker Symbol": data.get("symbol"),
#         "Industry/Sector": f"{data.get('industry')}, {data.get('sector')}",
#         "Location": f"{data.get('city')}, {data.get('country')}",
#         "Employees": normalize_value(data.get("fullTimeEmployees")),
#     }

# def extract_market_data(data):
#     return {
#         # "PipelineRunTime": data.get("PipelineRunTime"),
#         "Timestamp": data.get("Timestamp"),
#         "Current Price": normalize_value(data.get("currentPrice")),
#         "52-Week Range": f"{normalize_value(data.get('fiftyTwoWeekLow'))} - {normalize_value(data.get('fiftyTwoWeekHigh'))}",
#         "Daily Range": f"{normalize_value(data.get('dayLow'))} - {normalize_value(data.get('dayHigh'))}",
#         "Volume (Current)": normalize_value(data.get("volume")),
#         "Average Volume (10 Days)": normalize_value(data.get("averageVolume10days")),
#         "Market Cap": normalize_value(data.get("marketCap")),
#         "Beta": normalize_value(data.get("beta")),
#     }

# def extract_valuation_ratios(data):
#     return {
#         # "PipelineRunTime": data.get("PipelineRunTime"),
#         "Timestamp": data.get("Timestamp"),
#         "Trailing P/E": normalize_value(data.get("trailingPE")),
#         "Forward P/E": normalize_value(data.get("forwardPE")),
#         "PEG Ratio": normalize_value(data.get("pegRatio")),
#         "Price-to-Book": normalize_value(data.get("priceToBook")),
#         "Price-to-Sales": normalize_value(data.get("priceToSalesTrailing12Months")),
#         "Enterprise Value": normalize_value(data.get("enterpriseValue")),
#         "EV/Revenue": normalize_value(data.get("enterpriseToRevenue")),
#         "EV/EBITDA": normalize_value(data.get("enterpriseToEbitda")),
#     }

# def extract_dividends_returns(data):
#     return {
#         # "PipelineRunTime": data.get("PipelineRunTime"),
#         "Timestamp": data.get("Timestamp"),
#         "Dividend Rate": normalize_value(data.get("dividendRate")),
#         "Dividend Yield": normalize_value(data.get("dividendYield")),
#         "Payout Ratio": normalize_value(data.get("payoutRatio")),
#         "5-Year Avg. Dividend Yield": normalize_value(data.get("fiveYearAvgDividendYield")),
#         "Return on Assets (ROA)": normalize_value(data.get("returnOnAssets")),
#         "Return on Equity (ROE)": normalize_value(data.get("returnOnEquity")),
#     }

# def extract_financial_health(data):
#     return {
#         # "PipelineRunTime": data.get("PipelineRunTime"),
#         "Timestamp": data.get("Timestamp"),
#         "Total Cash": normalize_value(data.get("totalCash")),
#         "Total Debt": normalize_value(data.get("totalDebt")),
#         "Quick Ratio": normalize_value(data.get("quickRatio")),
#         "Current Ratio": normalize_value(data.get("currentRatio")),
#         "Debt-to-Equity": normalize_value(data.get("debtToEquity")),
#         "Free Cash Flow": normalize_value(data.get("freeCashflow")),
#         "Operating Cash Flow": normalize_value(data.get("operatingCashflow")),
#     }

# def extract_growth_metrics(data):
#     return {
#         # "PipelineRunTime": data.get("PipelineRunTime"),
#         "Timestamp": data.get("Timestamp"),
#         "Revenue": normalize_value(data.get("totalRevenue")),
#         "Revenue Growth (YoY)": normalize_value(data.get("revenueGrowth")),
#         "Earnings Growth (YoY)": normalize_value(data.get("earningsGrowth")),
#         "Gross Margin": normalize_value(data.get("grossMargins")),
#         "EBITDA Margin": normalize_value(data.get("ebitdaMargins")),
#         "Operating Margin": normalize_value(data.get("operatingMargins")),
#     }

# def extract_risk_assessment(data):
#     return {
#         # "PipelineRunTime": data.get("PipelineRunTime"),
#         "Timestamp": data.get("Timestamp"),
#         "Overall Risk Score": normalize_value(data.get("overallRisk")),
#         "Audit Risk": normalize_value(data.get("auditRisk")),
#         "Compensation Risk": normalize_value(data.get("compensationRisk")),
#         "Shareholder Rights Risk": normalize_value(data.get("shareHolderRightsRisk")),
#     }

# def extract_analyst_price_targets(data):
#     return {
#         # "PipelineRunTime": data.get("PipelineRunTime"),
#         "Timestamp": data.get("Timestamp"),
#         "Target High Price": normalize_value(data.get("targetHighPrice")),
#         "Target Low Price": normalize_value(data.get("targetLowPrice")),
#         "Mean Price Target": normalize_value(data.get("targetMeanPrice")),
#         "Median Price Target": normalize_value(data.get("targetMedianPrice")),
#     }
    
# # Updated save_csv_files to append instead of overwrite
# def save_csv_files(ticker, json_data, bucket_name):
#     # Define each CSV file content and corresponding S3 path
#     csv_files = {
#         f"transformed_data_bucket/{ticker}/{ticker}_Company_Profile.csv": extract_company_profile(json_data),
#         f"transformed_data_bucket/{ticker}/{ticker}_Market_Data.csv": extract_market_data(json_data),
#         f"transformed_data_bucket/{ticker}/{ticker}_Valuation_Ratios.csv": extract_valuation_ratios(json_data),
#         f"transformed_data_bucket/{ticker}/{ticker}_Dividends_and_Returns.csv": extract_dividends_returns(json_data),
#         f"transformed_data_bucket/{ticker}/{ticker}_Financial_Health.csv": extract_financial_health(json_data),
#         f"transformed_data_bucket/{ticker}/{ticker}_Growth_Metrics.csv": extract_growth_metrics(json_data),
#         f"transformed_data_bucket/{ticker}/{ticker}_Risk_Assessment.csv": extract_risk_assessment(json_data),
#         f"transformed_data_bucket/{ticker}/{ticker}_Analyst_Price_Targets.csv": extract_analyst_price_targets(json_data)
#     }

#     # Save each section as an appended CSV file in S3
#     for s3_key, data_dict in csv_files.items():
#         append_to_csv_in_s3(ticker, data_dict, s3_key, bucket_name)
       
# ########################################################
# # *******************   Pipeline   ******************* #
# ########################################################

# def new_ticker_list(arg_list, chunk_size):
#   new_arg_list = []
#   for i in range(0, len(arg_list), len(arg_list)//chunk_size):
#     new_arg_list.append(arg_list[i:i+(len(arg_list)//chunk_size)])
#   return new_arg_list