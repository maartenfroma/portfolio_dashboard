from decimal import Decimal
from django.db import models
from django.conf import settings
from stock.models import Stock

# Create your models here.

class Asset(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    ticker = models.CharField(max_length=10)
    asset_type = models.CharField(max_length=50)
    value = models.DecimalField(max_digits=20, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.value}"

class Transaction(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10)  # 'buy' or 'sell'
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    price_per_unit = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_date = models.DateTimeField()

    def __str__(self):
        return f"{self.transaction_type} {self.quantity} of {self.asset.name} at {self.price_per_unit}"

class UserPortfolio(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='portfolios')
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='portfolios')
    quantity = models.DecimalField(max_digits=20, decimal_places=2)
    average_price = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return f"{self.user.username} - {self.stock.symbol} ({self.quantity})"

    @property
    def total_value(self):
        """Berekent de actuele waarde op basis van de live koers, met fallback naar inkoopwaarde."""
        if self.stock.price is not None:
            return self.quantity * self.stock.price
        return self.total_cost

    @property
    def total_cost(self):
        """Berekent de totale inkoopwaarde."""
        return self.quantity * self.average_price   

    @property
    def profit_loss(self):
        """Berekent winst/verlies, veilig afgeschermd als de prijs nog niet is opgehaald."""
        if self.stock.price is not None:
            return (self.stock.price - self.average_price) * self.quantity 
        return Decimal('0.00')

    @property
    def profit_loss_percentage(self):
        """Berekent het rendement in procenten."""
        cost = self.total_cost
        if cost == 0 or self.stock.price is None:
            return Decimal('0.00')
        return (self.profit_loss / cost) * Decimal('100')