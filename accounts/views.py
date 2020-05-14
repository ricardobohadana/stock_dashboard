from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .models import Stock, Wallet
from .forms import StockForm, WalletForm
from django.contrib import messages
from .utilities import *
import simplejson as json

class forexView(View):
    model = None

    def get(self, request, *args, **kwargs):
        stocks = Stock.objects.all()
        context = {
            'stocks': stocks
        }
        return render(request, 'accounts/forex.html', context)






class WalletView(View):
    model = Wallet
    template_name = 'accounts/wallet.html'

    def get(self, request, *args, **kwargs):
        stocks = Stock.objects.all()
        wallet = Wallet.objects.all()
        updateWallet()
        context = {
            'stocks': stocks,
            'wallet': wallet,
        }
        return render(request, 'accounts/wallet.html', context)

class createWalletView(View):
    def get(self, request, *args, **kwargs):    
        stock = Stock.objects.get(pk=request.GET.get('stock', None))
        stock_amount = int(request.GET.get('stock_amount', None))
        buy_price = float(request.GET.get('buy_price', None))
        money_amount = stock.price * stock_amount
        investment = float(buy_price * stock_amount)
        
        obj = Wallet.objects.create(
            stock=stock,
            stock_amount=stock_amount,
            buy_price=round(buy_price,2),
            money_amount=round(money_amount,2),
            investment=round(investment,2),
        )
        obj.save()
        data = {
            'pk': obj.pk,
            'stocksymbol': obj.stock.symbol,
            'stock_price': obj.stock.price,
            'stock_amount': obj.stock_amount,
            'investment': obj.investment,
            'money_amount': obj.money_amount,
            'buy_price': obj.buy_price,
        }
        return JsonResponse(data)

class updateWalletView(View):
    def get(self, request, *args, **kwargs):
        symbol = request.GET.get('stock_symbol', None)
        stock_amount = int(request.GET.get('stock_amount', None))
        buy_price = float(request.GET.get('buy_price', None))
        stock = Stock.objects.filter(symbol=symbol)
        stock = stock[0]
        wallet = Wallet.objects.filter(stock=stock.pk)
        stock_amount_new = (stock_amount + wallet[0].stock_amount)
        investment_new = wallet[0].investment + (buy_price * stock_amount)
        buy_price_new = ((stock_amount*buy_price)*(wallet[0].stock_amount * wallet[0].buy_price))/(stock_amount + wallet[0].stock_amount)
        money_amount_new = stock_amount_new*stock.price
        wallet.update(
            investment=investment_new,
            money_amount=money_amount_new,
            stock_amount=stock_amount_new,
            buy_price=buy_price_new,
        )
        obj = Wallet.objects.get(pk=wallet[0].pk)
        data = {
            'pk': obj.pk,
            'stocksymbol': obj.stock.symbol,
            'stock_price': obj.stock.price,
            'stock_amount': obj.stock_amount,
            'investment': obj.investment,
            'money_amount': obj.money_amount,
            'buy_price': obj.buy_price,
        }
        return JsonResponse(data)
        

class deleteWalletView(View):
    def get(self, request, *args, **kwargs):
        pk = request.GET.get('pk', None)
        Wallet.objects.get(pk=pk).delete()
        data = {
            'deleted': True,
        }
        return JsonResponse(data)

class newhomeView(View):
    model = Stock
    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            symbol = str(request.GET.get('stock_symbol', None))
            obj = get_Stock_Data(symbol)
            db_query = Stock.objects.filter(symbol=symbol)
            db_query.update(
                price=obj['price'],
                change_percent=obj['change_percent'],
                updated=timezone.now()
            )
            obj['updated'] = timezone.now()
            obj['pk'] = db_query[0].pk
            obj['symbol'] = symbol
            return JsonResponse(obj)

        obj = get_ibovespaData()
        st = Stock.objects.all()
        atual = 0
        antigo = 0
        lucro = 0
        symbols = []
        for item in st:
            symbols.append(item.symbol)
            atual = atual + item.price
            antigo = antigo + (item.price/((item.change_percent/100)+1))
            lucro = ((atual/antigo)-1)*100
            lucro = round(lucro, 2)
        context = {
            'symbols': symbols,
            'stocks': st,
            'lucro': lucro,
            'obj': obj,
        }
        return render(request, 'accounts/home2.html', context)


def newstockView(request):
    stocks = Stock.objects.all()
    form = StockForm()
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            nform = form.save(commit=False)
            jsobj = get_Stock_Data(nform.symbol)
            if jsobj != 1:
                # if not check_duplicate(jsobj, nform.symbol, False):
                #     messages.warning(request, 'Ops, este ativo já está cadastrado em seu portfólio')
                #     return redirect('addstockpage')
                nform.symbol = nform.symbol.upper()
                # nform.name = jsobj['name']
                nform.price = jsobj['price']
                # nform.updated = jsobj['updated']
                nform.change_percent = jsobj['change_percent']
                nform.save()
                messages.success(request, 'Ativo adicionado com sucesso ao seu portfólio')
                return redirect('addstockpage')
            else:
                messages.warning(request, 'Ops, verifique se a abreviação do ativo foi digitada corretamente.')
        else:
            messages.warning(request, 'Ops, este ativo já está em seu portfólio!')
    context = {
        'form': form,
        'stocks':stocks
    }
    return render(request, 'accounts/addStock.html', context)

def detailedstockView(request, pk):
    stocks = Stock.objects.all()
    obj = Stock.objects.get(pk=pk)
    if request.is_ajax():
        print("IS AJAX")
        ndays = int(request.POST.get('value'))
        labs, datas, variance, prev = get_historicalData(obj.symbol, ndays)
        all_lists = []
        for i in range(0, len(variance)):
            all_lists.append([datas[0][i], labs[i], variance[i]])
        price = datas[0][-1]
        context = {
            'price': price,
            'prev': prev,
            'stock': datas[0],
            'sma15': datas[1],
            'sma30': datas[2],
            'sma60': datas[3],
            'labs': labs,
            'variance': variance,
            'all_lists': all_lists,
        }

        return HttpResponse(json.dumps(context), content_type="application/json")
    
    
    labs, datas, variance, prev = get_historicalData(obj.symbol, 90)

    all_lists = []
    for i in range(0, len(variance)):
        all_lists.append([datas[0][i], labs[i], variance[i]])
    price = datas[0][-1]
    context = {
        'stocks': stocks,
        'price': price,
        'prev': prev,
        'stock': datas[0],
        'sma15': datas[1],
        'sma30': datas[2],
        'sma60': datas[3],
        'labs': labs,
        'obj': obj,
        'variance': variance,
        'all_lists': all_lists,
    }
    return render(request, 'accounts/detailedStock.html', context)


def removestockView(request, pk):
    stock = Stock.objects.get(pk=pk)
    stock.delete()
    messages.success(request, 'Ativo removido do portfólio com sucesso!')
    return redirect('homepage')

        