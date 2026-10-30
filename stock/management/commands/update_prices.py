from datetime import date
import pandas as pd
from decimal import Decimal
from django.core.management.base import BaseCommand
from stock.models import Stock, HistoricalPrice, StockFundamental
from services.yfinance_client import get_stock_data, get_historical_data 
from services.finnhub_client import FinnhubService 

class Command(BaseCommand):
    help = 'Update stock prices, historical data, and fundamental metrics'

    def handle(self, *args, **kwargs):
        stocks = Stock.objects.all()
        finnhub_service = FinnhubService()
        
        start_date = '2020-01-01'
        end_date = date.today().strftime('%Y-%m-%d')

        for stock in stocks:
            symbol = stock.symbol
            self.stdout.write(f"--- Bezig met verwerken van {symbol} ---")

            # 1. Update current price (via yfinance)
            current_price = get_stock_data(symbol)
            if current_price is not None:
                stock.price = Decimal(str(current_price))
                stock.save()
                self.stdout.write(self.style.SUCCESS(f'  [Prijs] Geüpdatet naar {current_price}'))
            else:
                self.stdout.write(self.style.ERROR(f'  [Prijs] Ophalen mislukt'))

            # 2. Update Stock Fundamentals (via Finnhub)
            try:
                response = finnhub_service.client.basic_financials(symbol=symbol.upper(), metric='all')
                metrics = response.get('metric', {})
                
                if metrics:
                    StockFundamental.objects.update_or_create(
                        stock=stock,
                        defaults={
                            'pe_ratio': metrics.get('peBasicExclExtraTTM'),
                            'pb_ratio': metrics.get('pbAnnual'),
                            'roe': metrics.get('roeTTM'),
                            'net_profit_margin': metrics.get('netProfitMarginTTM'),
                            'dividend_yield': metrics.get('dividendYieldIndicatedAnnual'),
                            'market_cap': metrics.get('marketCapitalization'),
                        }
                    )
                    self.stdout.write(self.style.SUCCESS(f'  [Fundamentals] Succesvol bijgewerkt'))
                else:
                    self.stdout.write(self.style.WARNING(f'  [Fundamentals] Geen metrics gevonden'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  [Fundamentals] Fout: {e}'))

            # 3. Update historical data (via yfinance)
            historical_data = get_historical_data(symbol, start_date, end_date)
            if not historical_data.empty:
                count = 0
                for index, row in historical_data.iterrows():
                    price_date = index.date() if hasattr(index, 'date') else index
                    close_price = row.get('Close')
                    
                    if close_price is not None and not pd.isna(close_price):
                        HistoricalPrice.objects.update_or_create(
                            stock=stock,
                            date=price_date,
                            defaults={'close_price': Decimal(str(close_price))}
                        )
                        count += 1
                        
                self.stdout.write(self.style.SUCCESS(f'  [Historie] {count} datapunten opgeslagen'))
            else:
                self.stdout.write(self.style.ERROR(f'  [Historie] Ophalen mislukt'))

        self.stdout.write(self.style.SUCCESS("Alle aandelen zijn succesvol gesynchroniseerd!"))