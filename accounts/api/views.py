from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.utils import timezone

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from accounts.models import Stock, Wallet
from accounts.api.serializers import StockSerializer, WalletSerializer


class ApiOverview(APIView):
  def get(self, request):
    context = {
      'API Information': 'api/',
      'Stocks': 'api/stock/',
      'Detailed Stock': 'api/stock/<str:pk>',
      'Create Stock': 'api/create',
      'Update Stock': 'api/update/<str:pk>',
      'Delete Stock': 'api/delete/<str:pk>',

      'Wallet': 'api/wallet/',
      'Create Wallet Item': 'api/wallet/create/',
      'Update Wallet Item': 'api/update/<str:pk>',
      'Delete Wallet Item': 'api/delete/<str:pk>',
    }

    return Response(context)


class StockApiView(APIView):
  def get(self, request):
    stocks = Stock.objects.all()
    serializer = StockSerializer(stocks, many=True)


    return Response(serializer.data, status=200)

  def post(self, request):
    data = request.data
    serializer = StockSerializer(data=data)
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.error_messages, status=400)



class StockApiDetailView(APIView):
  def get_object(self, id):
    try:
      return Stock.objects.get(pk=id)
    except:
      return Response({"error": "The Stock object with the given primary key doesn't exist"}, status=404)

  def get(self, request, id=None):
    instance = self.get_object(id)
    serializer = StockSerializer(instance)
    return Response(serializer.data, status=200)

  def delete(self, request, id=None):
    instance = self.get_object(id)
    instance.delete()
    return Response({"success": "Stock object deleted sucessfully"}, status=204)



class StockApiUpdateView(APIView):
  def get(self, request):
    try:
      stocks = Stock.objects.all()
      print(stocks)
      for stock in stocks:
        serializer = StockSerializer(stock)
        serializer.update(stock.symbol)
      
      return Response({"success": "All Stocks were updated successfully"}, status=200)
    except:
      return Response({"error":"Something prevented the update from being executed"}, status=400)



class WalletApiView(APIView):
  def get(self, request):
    wallet = Wallet.objects.all()
    serializer = WalletSerializer(wallet, many=True)

    return Response(serializer.data, status=200)

  def post(self, request):
    data = request.data
    serializer = WalletSerializer(data=data)
    
    if serializer.is_valid():
      serializer.save()
      return Response(serializer.data, status=201)
    return Response(serializer.error_messages, status=400)



class WalletApiUpdateView(APIView):
  def get_object(self, symbol):
    try:
      id = Stock.objects.filter(symbol=symbol)[0].pk
      return Wallet.objects.filter(stock=id)[0]
    except:
      return Response({"error": "The Wallet object with the given primary key doesn't exist"}, status=404)

  def get(self, request):
    wallet = Wallet.objects.all()
    for instance in wallet:
      serializer = WalletSerializer(instance)
      serializer.update(instance, None) 

    return Response({"success":"Your wallet was updated"})

  def put(self, request):
    data = request.data
    instance = self.get_object(data['stock'])
    serializer = WalletSerializer(instance, data=data)
    if serializer.is_valid():
      serializer.update(instance, data)
      return Response({"success": "The wallet "+ instance.stock.symbol +" was updated successfully"}, status=201)
    return Response({"error":"Something prevented the wallet from being updated"}, status=400)

  def delete(self, request):
    data = request.data
    instance = self.get_object(data['stock'])
    instance.delete()
    return Response({"success": "The wallet item was deleted"}, status=204)
  
# class WalletApiDeleteView(APIView):
#   def get_object(self, id):


