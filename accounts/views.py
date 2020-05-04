from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import Stock, Wallet
from .forms import StockForm, WalletForm
from django.contrib import messages
from .utilities import *
import simplejson as json

def newhomeView(request):
    st = Stock.objects.all()
    atual = 0
    antigo = 0
    lucro = 0
    for item in st:
        atual = atual + item.price
        antigo = antigo + (item.price/((item.change_percent/100)+1))
        lucro = ((atual/antigo)-1)*100
    lucro = round(lucro, 2)
    obj = get_ibovespaData()

    context = {
        'stocks': st,
        'lucro': lucro,
        'obj': obj,
    }
    return render(request, 'accounts/home2.html', context)


def walletView(request):
    stocks = Stock.objects.all()
    form = WalletForm()
    wallet = Wallet.objects.all()
    if not updateWallet():
        messages.warning('Algo errado com o update')
    if request.method == 'POST':
        form = WalletForm(request.POST)
        if form.is_valid():
            nform = form.save(commit=False)
            nform.money_amount = nform.investment
            nform.save()
            messages.success(request, 'Papéis adicionadas a sua carteira')
            return redirect('walletpage')
    context = {
        'wallet': wallet,
        'form': form,
        'stocks':stocks,
    }
    return render(request, 'accounts/wallet.html', context)


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

# UPDATE ALL STOCKS
def updatestocksView(request):
    # start = time.process_time()
    stock = Stock.objects.all()
    for item in stock:
        obj = get_Stock_Data(item.symbol)
        db_query = Stock.objects.filter(symbol=item.symbol)
        db_query.update(
            price=obj['price'],
            change_percent=obj['change_percent'],
            updated=timezone.now()
        )
    # print('Processamento de updatesstocsView: ' + str(time.process_time() - start))
    messages.success(request, 'Seu portfólio foi atualizado com sucesso')
    return redirect('homepage')


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

        