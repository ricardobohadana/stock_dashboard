from django.contrib import admin
from .models import Stock, Wallet, Transaction
from django.contrib.auth.models import User

# Register your models here.
admin.site.register(Stock)
admin.site.register(Wallet)
admin.site.register(Transaction)