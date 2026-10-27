from django.contrib import admin
from .models import Stock, UserPortfolio, HistoricalPrice

# Register your models here.
admin.site.register(Stock)
admin.site.register(UserPortfolio)
admin.site.register(HistoricalPrice)    


