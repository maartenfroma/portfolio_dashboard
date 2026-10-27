from django.core.management.base import BaseCommand
from stock.models import Stock, HistoricalPrice
from services.yfinance_client import get_stock_data, get_historical_data 

class Command(BaseCommand):
    help = 'Update stock prices and historical data'

    def handle(self, *args, **kwargs):
        stocks = Stock.objects.all()
        for stock in stocks:
            # Update current price
            current_price = get_stock_data(stock.ticker)
            if current_price is not None:
                stock.current_price = current_price
                stock.save()
                self.stdout.write(self.style.SUCCESS(f'Updated {stock.ticker} price to {current_price}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to update {stock.ticker} price'))

            # Update historical data
            historical_data = get_historical_data(stock.ticker, '2020-01-01', '2024-01-01')
            if not historical_data.empty:
                for date, row in historical_data.iterrows():
                    HistoricalPrice.objects.update_or_create(
                        stock=stock,
                        date=date,
                        defaults={'price': row['Close']}
                    )
                self.stdout.write(self.style.SUCCESS(f'Updated historical data for {stock.ticker}'))
            else:
                self.stdout.write(self.style.ERROR(f'Failed to update historical data for {stock.ticker}'))