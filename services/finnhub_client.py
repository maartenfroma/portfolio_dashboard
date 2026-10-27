import finnhub
from django.conf import settings    

class FinnhubService:
    def __init__(self):
        api_key=getattr(settings, 'FINNHUB_API_KEY', None)
        if not api_key:
            raise ValueError("FINNHUB_API_KEY is not set in settings.")
        self.client = finnhub.Client(api_key=api_key)

    def get_stock_quote(self,ticker:str)->float:
        try:
            quote = self.client.quote(ticker.upper())
            return float(quote.get('c', 0.0))  # Return the current price, default to 0.0 if not found  
        except Exception as e:
            print(f"Error fetching stock quote for {ticker}: {e}")
            return 0.0  
        

    def get_company_profile(self, ticker):
        try:
            profile = self.client.company_profile2(symbol=ticker.upper())
            return profile                          
        except Exception as e:
            print(f"Error fetching company profile for {ticker}: {e}")
            return {}      

    def get_basic_financials(self, ticker:str)->dict:
        try:
            financials = self.client.basic_financials(symbol=ticker.upper())
            return financials
        except Exception as e:
            print(f"Error fetching basic financials for {ticker}: {e}")
            return {}