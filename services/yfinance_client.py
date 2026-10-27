import yfinance as yf
import pandas as pd

@staticmethod
def get_stock_data(ticker:str)->float:
   
    try:
        price = yf.Ticker(ticker).info['regularMarketPrice']
        return price

    except Exception as e:
        print(f"Error fetching data for {ticker}: {e}")
        return None

@staticmethod
def get_historical_data(ticker:str, start_date:str, end_date:str, 
                        interval:str="1d")->pd.DataFrame:
    try:
        data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
        return data

    except Exception as e:
        print(f"Error fetching historical data for {ticker}: {e}")
        return pd.DataFrame()       

