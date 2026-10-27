from stocks.models import UserPortfolio, HistoricalPrice    
import pandas as pd

class PortfolioCalculator:
    @staticmethod
    def calculate_portfolio_value(user, date):
        # Fetch all stocks in the user's portfolio
        user_portfolio = UserPortfolio.objects.filter(user=user)
        
        total_value = 0.0
        
        for portfolio_item in user_portfolio:
            stock = portfolio_item.stock
            quantity = portfolio_item.quantity
            
            # Fetch historical price for the given date
            try:
                historical_price = HistoricalPrice.objects.get(stock=stock, date=date)
                total_value += quantity * historical_price.close_price
            except HistoricalPrice.DoesNotExist:
                print(f"No historical price data for {stock.symbol} on {date}")
        
        return total_value