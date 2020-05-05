from django import forms
from django.forms import ModelForm
from .models import Stock, Wallet

class StockForm(ModelForm):
    class Meta:
        model = Stock
        fields = [
            'symbol'
        ]

        exclude = [
            'name',
            'price',
            'updated'
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