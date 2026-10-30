from django.contrib import admin
from .models import Asset, Transaction, UserPortfolio

# Register your models here.
admin.site.register(Asset)
admin.site.register(Transaction)
admin.site.register(UserPortfolio)
