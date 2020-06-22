from django import forms
from django.forms import ModelForm
from .models import Stock, Wallet

class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = [
            'symbol',
            'is_fund',
            'is_etf',
        ]

        exclude = [
            'price',
            'updated'
            'change_percent',
            'favorite',
        ]

class WalletForm(ModelForm):
    class Meta:
        model = Wallet
        field = [
            'stock',
            'stock_amount',
            'buy_price',
        ]
        exclude = [
            'investment',
            'money_amount',
        ]