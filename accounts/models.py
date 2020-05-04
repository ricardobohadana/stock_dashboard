from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Stock(models.Model):
    # name = models.CharField(max_length=200)
    symbol = models.CharField(max_length = 10, unique=True)
    price = models.FloatField()
    updated = models.DateTimeField(auto_now_add=True)
    change_percent = models.FloatField(default=0.0)

    def __str__(self):
        return self.symbol
    
class Wallet(models.Model):
    stock = models.OneToOneField(Stock, unique=True, on_delete=models.CASCADE)
    investment = models.FloatField()
    money_amount = models.FloatField()
    stock_amount = models.IntegerField()
    
    def __str__(self):
        return self.stock