from rest_framework import serializers

from accounts.models import Wallet, Stock
from accounts.utilities import *

from django.utils import timezone

class StockSerializer(serializers.ModelSerializer):
	price = serializers.FloatField(required=False)
	updated = serializers.DateTimeField(required=False)
	change_percent = serializers.FloatField(required=False)
	favorite = serializers.BooleanField(required=False, default=False)

	class Meta:
		model = Stock
		fields = [
			'symbol',
			'price',
			'updated',
			'change_percent',
			'favorite',
		]

	def create(self, validated_data):
		symbol = validated_data['symbol']
		jsobj = get_Stock_Data(symbol)
		if jsobj != 1:
			validated_data = jsobj
			instance = Stock.objects.create(
				symbol=validated_data['symbol'],
				change_percent=validated_data['change_percent'],
				price=validated_data['price'],
			)
			instance.save()
			return instance
	
	def update(self, symbol):
		new_obj = get_Stock_Data(symbol)
		db_query = Stock.objects.filter(symbol=symbol)
		return db_query.update(
			price=new_obj['price'],
			change_percent=new_obj['change_percent'],
			updated=timezone.now(),
		)

	


class WalletSerializer(serializers.ModelSerializer):
	stock = serializers.CharField(required=True)
	investment = serializers.FloatField(required=False)
	money_amount = serializers.FloatField(required=False)
	class Meta:
		model = Wallet
		fields = [
			'stock',
			'stock_amount',
			'buy_price',
			'investment',
			'money_amount',
		]

	def create(self, validated_data):
		# if Wallet.objects.filter(stock=Stock.objects.filter(symbol=)[0].pk):
		obj = Stock.objects.filter(symbol=validated_data['symbol'])
		validated_data['stock'] = obj[0]

		validated_data['money_amount'] = validated_data['stock'].price * validated_data['stock_amount']
		validated_data['investment'] = validated_data['buy_price'] * validated_data['stock_amount']

		instance = Wallet.objects.create(
			stock=validated_data['stock'],
			stock_amount=validated_data['stock_amount'],
			buy_price=validated_data['buy_price'],
			money_amount=validated_data['money_amount'],
			investment=validated_data['investment'],
		)
		instance.save()
		return instance
	
	def update(self, instance, validated_data):
		if validated_data == None:
			money_amount = round(instance.stock.price * instance.stock_amount, 2)
			instance.money_amount = money_amount
			instance.save()
		else:
			stock_amount = validated_data['stock_amount']
			buy_price = validated_data['buy_price']
			stock_amount_new = (stock_amount + instance.stock_amount)
			investment_new = instance.investment + (buy_price * stock_amount)
			buy_price_new = (((stock_amount*buy_price)*(instance.stock_amount * instance.buy_price))/(stock_amount + instance.stock_amount))
			money_amount_new = stock_amount_new*instance.stock.price
			instance.investment = investment_new
			instance.money_amount = money_amount_new
			instance.stock_amount = stock_amount_new
			instance.buy_price = buy_price_new
			instance.save()

		return instance
		