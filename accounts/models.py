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
        ('Itala-Caco','Itala-Caco'),
    ]
    stock = models.ForeignKey(Stock, on_delete=models.CASCADE)
    investment = models.FloatField()
    money_amount = models.FloatField()
    stock_amount = models.IntegerField()
    buy_price = models.FloatField()
    owner = models.CharField(choices=person_choices, default='Caco', max_length=11)

    def __str__(self):
        return self.stock.symbol

    class Meta:
        unique_together = ['owner', 'stock']


class Transaction(models.Model):
    options_operation = [
        ('Compra', 'Compra'),
        ('Compra e Venda', 'Compra e Venda'),
        ('Venda', 'Venda')
    ]
    options_broker = [
        ('Agora - Caco','Agora - Caco'),
        ('Agora - Ricardo', 'Agora - Ricardo'),
        ('BB - Ricardo', 'BB - Ricardo'),
        ('BB - Itala', 'BB - Itala'),
    ]
    stock = models.CharField(max_length=50)
    operation = models.CharField(max_length=25, choices=options_operation)
    document = models.FileField('documents/pdfs')
    date = models.DateField('Data da transação',auto_now=False, auto_now_add=False)
    broker = models.CharField(max_length=25, choices=options_broker)

    def __str__(self):
        return (self.id + ' - ' + self.operation + ' ' + self.stock)