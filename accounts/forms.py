from django import forms
from django.forms import ModelForm
from .models import Stock

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