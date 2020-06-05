from django.db import models
from django.contrib.auth.models import User



class Stock(models.Model):
    # name = models.CharField(max_length=200)
    symbol = models.CharField(max_length = 100, unique=True)
    price = models.FloatField()
    updated = models.DateTimeField(auto_now_add=True)
    change_percent = models.FloatField(default=0.0)
    favorite = models.BooleanField(default=False);

    def __str__(self):
        return self.symbol
    
class Wallet(models.Model):
    person_choices = [
        ('Caco','Caco'),
        ('Ricardo', 'Ricardo'),
        ('Itala', 'Itala'),
        ('Thayssa', 'Thayssa'),
    ]
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    investment = models.FloatField()
    money_amount = models.FloatField()
    stock_amount = models.IntegerField()
    buy_price = models.FloatField()
    owner = models.CharField(choices=person_choices, default='Caco', max_length=7)

    def __str__(self):
        return self.stock.symbol

    class Meta:
        unique_together = ['owner', 'stock']
        