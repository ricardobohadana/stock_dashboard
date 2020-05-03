from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from .utilities import *
import simplejson as json


# homepage
def homeView(request):
    st = get_diff_stocks()
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

    return render(request, 'accounts/home.html', context)


def newstockView(request):
    st = get_diff_stocks()
    form = StockForm()
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            nform = form.save(commit=False)
            jsobj = get_Stock_Data(nform.symbol)
            if jsobj != 1:
                if not check_duplicate(jsobj, nform.symbol, False):
                    messages.warning(request, 'Ops, este ativo já está cadastrado em seu portfólio')
                    return redirect('addstockpage')
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
            messages.warning(request, 'Ops, há algum erro')
    context = {
        'form': form,
        'stocks': st,

    }
    return render(request, 'accounts/addStock.html', context)

# UPDATE SPECIFIC STOCK
def updatestockView(request, pk):
    stock = Stock.objects.get(pk=pk)
    obj = create_Stock_object(stock.symbol, True)
    obj.save()
    stock.delete()
    return redirect('homepage')


# UPDATE ALL STOCKS
def updatestocksView(request):
    start = time.process_time()
    stock = get_diff_stocks()
    for item in stock:
        obj = create_Stock_object(item.symbol, True)
        obj.save()
        item.delete()
    print('Processamento de updatesstocsView: ' + str(time.process_time() - start))
    messages.success(request, 'Seu portfólio foi atualizado com sucesso')
    return redirect('homepage')


def detailedstockView(request, pk):
    st = get_diff_stocks()
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
        'stocks': st,
    }
    return render(request, 'accounts/detailedStock.html', context)


def removestockView(request, pk):
    stock = Stock.objects.get(pk=pk)
    stocks = Stock.objects.filter(symbol=stock.symbol)
    for item in stocks:
        item.delete()
    messages.success(request, 'Ativo removido do portfólio com sucesso!')
    return redirect('homepage')


def graphRange(request, pk):
    if request.is_ajax():
        # get_historicalData()
        pass
    return
        