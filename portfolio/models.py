from django.db import models
from django.conf import settings

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

class DailyPortfolioValue(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField()
    total_value = models.DecimalField(max_digits=20, decimal_places=2)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.total_value}"