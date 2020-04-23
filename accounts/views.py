from django.shortcuts import render, redirect
from .models import Stock
from .forms import StockForm
from django.contrib import messages
from .utilities import *


# homepage
def homeView(request):
    st = get_diff_stocks()
    lucro = 0
    for item in st:
        lucro = lucro + (item.price - (item.price/((item.change_percent/100)+1)))
    lucro = round(lucro, 2)

    context = {
        'stocks': st,
        'lucro': lucro,
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
                nform.name = jsobj['name']
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
    stock = get_diff_stocks()
    for item in stock:
        obj = create_Stock_object(item.symbol, True)
        obj.save()
        item.delete()
    messages.success(request, 'Seu portfólio foi atualizado com sucesso')
    return redirect('homepage')


def detailedstockView(request, pk):
    st = get_diff_stocks()
    obj = Stock.objects.get(pk=pk)
    labs, datas = get_historicalData(obj.symbol)
    variance = ['sem informação']

    for i in range(1, len(datas)):
        try:
            variance.append(datas[i]/datas[i-1])
        except IndexError:
            pass

    for i in range(1, len(variance)):
        try:
            variance[i] = round(100*(variance[i]-1), 2)
        except TypeError:
            pass

    all_lists = []
    for i in range(0, len(datas)):
        all_lists.append([labs[i], datas[i], variance[i]])

    context = {
        'datas': datas,
        'labs': labs,
        'obj': obj,
        'variance': variance,
        'all_lists': all_lists,
        'stocks': st,
    }
    return render(request, 'accounts/detailedStock.html', context)
