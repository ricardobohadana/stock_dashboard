from accounts.api.serializers import StockSerializer, WalletSerializer
from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse, JsonResponse
from django.views.generic import View
from .models import Stock, Wallet, Transaction
from .forms import StockForm, WalletForm
from django.contrib import messages
from .utilities import *
import simplejson as json


class StocksSummary(View):
    template_name = "accounts/sum_stocks.html"

    def get(self, request, id, *args, **kwargs):
        id_disclosure = [
            'Caco',
            'Ricardo',
            'Itala',
            'Thayssa',
        ]
        if request.is_ajax():
            updated_stocks = []
            stocks = [item.stock for item in Wallet.objects.filter(owner=id_disclosure[int(id)-1])]
            for stock in stocks:
                db_obj = Stock.objects.get(pk=stock.pk)
                obj = get_Stock_Data(stock.symbol)
                if obj == 1:
                    return HttpResponse('error')
                db_obj.price = obj['price']
                db_obj.change_percent = obj['change_percent']
                db_obj.updated = timezone.now()
                db_obj.save()
                updated_stocks.append({
                    'symbol': stock.symbol,
                    'price': db_obj.price,
                    'change_percent': db_obj.change_percent,
                    'is_etf': db_obj.is_etf,
                    'is_fund': db_obj.is_fund,
                })
            return JsonResponse(updated_stocks, safe=False)

        context = {
            # 'stocks': stocks,
            'id': id,

        }

        return render(request, self.template_name, context)

class TransactionSummary(View):
    template_name = 'accounts/sum_trans.html'

    def create_transaction(self, data):
        try:
            pass
            instance = Transaction.objects.create(
                stock = data[0],
                operation = data[1],
                document = data[2],
                date = data[3],
                broker = data[4],
                )
            instance.save()
            return True
        except:
            return False

    def post(self, request, *args, **kwargs):
        # procura pelo nome
        date = request.POST.get('transaction-date', None)
        broker = request.POST.get('transaction-broker', None)
        stock = str(request.POST.get('transaction-stock', None)).upper()
        document = request.FILES['transaction-file']
        operation = request.POST.get('transaction-operation', None)
        obj = [stock, operation, document, date, broker]
        print(obj)
        if (date and stock and document and operation):
            done = self.create_transaction(obj)
            if done:
                return redirect('summarytransactionspage')
            else:
                return HttpResponse('/error/')
        else:
            return HttpResponse('/error/')


    def get(self, request, id, *args, **kwargs):
        if request.is_ajax():
            if request.GET.get('action', None) == 'delete':
                    pk = request.GET.get('pk', None)
                    Transaction.objects.get(pk=pk).delete()
                    return JsonResponse({'deleted': True})
        broker = [
            'Agora - Caco',
            'BB - Ricardo',
            'BB - Itala',
            'BB - Thayssa',
        ]
        transactions = Transaction.objects.filter(broker=broker[int(id)-1]).order_by('-date')
        context ={
            'id': int(id),
            'transactions': transactions
        }

        return render(request, self.template_name, context)


class InvestmentSummary(View):
    template_name = 'accounts/summary.html'
    id_disclosure = [
         'Caco',
         'Ricardo',
         'Itala',
         'Thayssa',
    ]
    def get_data(self, id):
        owner = self.id_disclosure[int(id)-1]
        return Wallet.objects.filter(owner=owner)
        

    def get(self, request, id, *args, **kwargs):
        obj = get_ibovespaData()
        nasdaq = get_internationalData('^IXIC')
        sp500 = get_internationalData('^GSPC')
        dji = get_internationalData('^DJI')



        wallet = self.get_data(id)
        amount_all = sum([item.money_amount for item in wallet])
        investment_all = sum([item.investment for item in wallet])
        # stock_amount_all = sum([item.stock_amount for item in wallet])

        stocks_all = [[round(((item.stock.price/item.buy_price)-1)*100, 2), item.stock.symbol, item.money_amount, round(item.money_amount-item.investment, 2), item.stock.pk] for item in wallet]
        best_stock = max(stocks_all)
        worst_stock = min(stocks_all)

        # stock_amount_etf = sum([item.stock_amount for item in wallet if item.stock.is_etf])
        amount_etf = sum([item.money_amount for item in wallet if item.stock.is_etf])
        # investment_etf = sum([item.investment for item in wallet if item.stock.is_etf])
        
        # stock_amount_fund = sum([item.stock_amount for item in wallet if item.stock.is_fund])
        amount_fund = sum([item.money_amount for item in wallet if item.stock.is_fund])
        # investment_fund = sum([item.investment for item in wallet if item.stock.is_fund])
        
        # stock_amount_stock = sum([item.stock_amount for item in wallet if not item.stock.is_etf and not item.stock.is_fund])
        amount_stock = sum([item.money_amount for item in wallet if not item.stock.is_etf and not item.stock.is_fund])
        investment_stock = sum([item.investment for item in wallet if not item.stock.is_etf and not item.stock.is_fund])
        
        performance = round(sum([(item.stock.change_percent*item.stock.price*item.stock_amount/100) for item in wallet]),2)
        performance_change_percent = round(((performance/investment_all))*100,2)
        performance_change_percent_class = 'success' if performance_change_percent > 0 else 'danger'
        performance_change_percent_color = 'green' if performance_change_percent > 0 else 'red'


         
        try:
            change_percent_all = round(((amount_all/investment_all)-1)*100, 2)
        except ZeroDivisionError:
            change_percent_all = 0
        # try:
        #     change_percent_etf = round(((amount_etf/investment_etf)-1)*100, 2)
        # except ZeroDivisionError:
        #     change_percent_etf = 0
        # try:
        #     change_percent_fund = round(((amount_fund/investment_fund)-1)*100, 2)
        # except ZeroDivisionError:
        #     change_percent_fund = 0
        try:
            change_percent_stock = round(((amount_stock/investment_stock)-1)*100, 2)
        except ZeroDivisionError:
            change_percent_stock = 0

            
        if change_percent_all > 0:
            change_percent_all_class = 'success'
            change_percent_all_color = 'green'
        else:
            change_percent_all_class = 'danger'
            change_percent_all_color = 'red'
            
        # print(request.GET)
        context = {
            "id": int(id),
            'ibovespa': obj,
            'nasdaq': nasdaq,
            'sp500': sp500,
            'dji': dji,
            'stocks_all': stocks_all,
            'best_stock': best_stock,
            'worst_stock': worst_stock,
            'amount_all':amount_all,
            # 'stock_amount_all':stock_amount_all,
            # 'investment_all':investment_all,
            'change_percent_all':change_percent_all,
            'change_percent_all_color':change_percent_all_color,
            'change_percent_all_class':change_percent_all_class,
            # 'stock_amount_fund':stock_amount_fund,
            'amount_fund':amount_fund,
            # 'investment_fund':investment_fund,
            # 'change_percent_fund':change_percent_fund,
            # 'stock_amount_etf':stock_amount_etf,
            'amount_etf':amount_etf,
            # 'investment_etf':investment_etf,
            # 'change_percent_etf':change_percent_etf,
            # 'stock_amount_stock':stock_amount_stock,
            'amount_stock':amount_stock,
            # 'investment_stock':investment_stock,
            # 'change_percent_stock':change_percent_stock,
            'performance': performance,
            'performance_change_percent': performance_change_percent,
            'performance_change_percent_class': performance_change_percent_class,
            'performance_change_percent_color': performance_change_percent_color,
        }

        return render(request, self.template_name, context)


class transactionView(View):
    model = Transaction
    template_name = 'accounts/transaction.html'
    
    def create_transaction(self, data):
        try:
            pass
            instance = Transaction.objects.create(
                stock = data[0],
                operation = data[1],
                document = data[2],
                date = data[3],
                broker = data[4],
                )
            instance.save()
            return True
        except:
            return False

    def post(self, request, *args, **kwargs):
        # procura pelo nome
        date = request.POST.get('transaction-date', None)
        broker = request.POST.get('transaction-broker', None)
        stock = str(request.POST.get('transaction-stock', None)).upper()
        document = request.FILES['transaction-file']
        operation = request.POST.get('transaction-operation', None)
        obj = [stock, operation, document, date, broker]
        print(obj)
        if (date and stock and document and operation):
            done = self.create_transaction(obj)
            if done:
                return redirect('transactionspage')
            else:
                return HttpResponse('/error/')
        else:
            return HttpResponse('/error/')


    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            if request.GET.get('action', None) == 'delete':
                    pk = request.GET.get('pk', None)
                    Transaction.objects.get(pk=pk).delete()
                    return JsonResponse({'deleted': True})
        transactions = Transaction.objects.all().order_by('-date')
        context ={
            'transactions': transactions
        }

        return render(request, self.template_name, context)


class bvspView(View):
    model = None
    template_name = 'accounts/bvsp.html'

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            ndays = int(request.GET.get('value', None))
            return JsonResponse(getHistoricalIbovespa(ndays))

        ibov = getHistoricalIbovespa()
        context = {
            'ibov': ibov
        }
        return render(request, self.template_name, context)


class queryView(View):
    model = None
    template_name = 'accounts/query.html'

    def query(self, symbol):
        labs, datas, variance, prev = get_historicalData(symbol)
        all_lists = []
        for i in range(0, len(variance)):
            all_lists.append([datas[0][3][i], labs[i], variance[i]])
        context = {
            # 'price': price,
            'symbol': symbol,
            'mean': prev,
            'stock': datas[0],
            'sma15': datas[1],
            'labs': labs,
            'variance': variance,
            'all_lists': all_lists,
        }
        return context


    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            ndays = int(request.POST.get('range'))
            symbol = str(request.POST.get('symbol'))
            labs, datas, variance, prev = get_historicalData(symbol, ndays)
            all_lists = []
            for i in range(0, len(variance)):
                all_lists.append([datas[0][3][i], labs[i], variance[i]])
            context = {
                # 'price': price,
                'symbol': symbol,
                'mean': prev,
                'stock': datas[0],
                'sma15': datas[1],
                'labs': labs,
                'variance': variance,
                'all_lists': all_lists,
            }
            return JsonResponse(context)

    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            get_action = {
                'query': self.query,
            }
            action = str(request.GET.get('action', None))
            return JsonResponse(get_action[action](request.GET.get('data', None)))

        context = {}
        return render(request, self.template_name, context)


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
        investment = float(request.GET.get('investment', None))
        owner = str(request.GET.get('owner', None))
        money_amount = stock.price * stock_amount
        buy_price = float(investment / stock_amount)

        obj = Wallet.objects.create(
            stock=stock,
            owner=owner,
            stock_amount=stock_amount,
            buy_price=round(buy_price,2),
            money_amount=round(money_amount,2),
            investment=round(investment,2),
        )
        obj.save()
        data = {
            'pk': obj.pk,
            'stock_symbol': obj.stock.symbol,
            'stock_price': obj.stock.price,
            'stock_amount': obj.stock_amount,
            'investment': obj.investment,
            'money_amount': obj.money_amount,
            'buy_price': obj.buy_price,
        }
        return JsonResponse(data)


class updateWalletView(View):
    def get(self, request, *args, **kwargs):
        symbol = str(request.GET.get('stock_symbol', None))
        stock_amount = int(request.GET.get('stock_amount', None))
        buy_price = float(request.GET.get('buy_price', None))
        stock = Stock.objects.filter(symbol=symbol)
        stock = stock[0]
        wallet = Wallet.objects.filter(stock=stock.pk)
        stock_amount_new = (stock_amount + wallet[0].stock_amount)
        investment_new = wallet[0].investment + (buy_price * stock_amount)
        buy_price_new = ((stock_amount*buy_price)+(wallet[0].stock_amount * wallet[0].buy_price))/(stock_amount + wallet[0].stock_amount)
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
    template_name = 'accounts/home2.html'

    def update_favorites(self, data):
        id = int(data)
        obj = Stock.objects.get(pk=id)
        obj.favorite = not obj.favorite
        obj.save()
        context = {
            "fav": obj.favorite,
        }
        return context

    def update_stocks(self, data):
        symbol = str(data)
        obj = get_Stock_Data(symbol)
        labs, datas, variance, prev = get_historicalData(symbol)
        SMA_14d = datas[1][-1]
        SMA_30d = datas[2][-1]

        if obj == 1:
            return JsonResponse({"error":"error"})
        db_query = Stock.objects.filter(symbol=symbol)
        db_query.update(
            price=obj['price'],
            change_percent=obj['change_percent'],
            updated=timezone.now()
        )
        obj['pk'] = db_query[0].pk
        obj['symbol'] = symbol
        obj['favorite'] = db_query[0].favorite
        obj['SMA_30'] = SMA_30d
        obj['SMA_14'] = SMA_14d
        return obj

    # def update_features(self, data):
    #     stock_high = []
    #     stock_low = []
    #     stock_h = Stock.objects.order_by("-change_percent")
    #     stock_l = Stock.objects.order_by("change_percent")
    #     for i in range(len(stock_h)):
    #         stock_high.append({
    #             "symbol": stock_h[i].symbol,
    #             "price": stock_h[i].price,
    #             "change_percent": stock_h[i].change_percent,
    #         })
    #         stock_low.append({
    #             "symbol": stock_l[i].symbol,
    #             "price": stock_l[i].price,
    #             "change_percent": stock_l[i].change_percent,
    #         })
    #     abs_high, abs_low = getAbsoluteHighLow()
    #     print(stock_low)
    #     return {
    #         "highrel":stock_high[:5],
    #         "highabs":abs_high,
    #         "lowrel":stock_low[:-5],
    #         "lowabs":abs_low,
    #         }



    def get(self, request, *args, **kwargs):
        if request.is_ajax():
            get_action = {
                "update_favorites": self.update_favorites,
                "update_stocks": self.update_stocks,
                # "update_features": self.update_features,
                }
            action = str(request.GET.get('action', None))
            return JsonResponse(get_action[action](request.GET.get('data', None)))
        obj = get_ibovespaData()
        st = Stock.objects.order_by('-favorite')
        favorites = [stock.symbol for stock in Stock.objects.filter(favorite=True)]
        # atual = 0
        # antigo = 0
        # lucro = 0
        serializer = StockSerializer(Stock.objects.all(), many=True)
        symbols = [stock.symbol for stock in Stock.objects.order_by('-favorite')]
        context = {
            'symbols': symbols,
            'favorites': favorites,
            'stocks': st,
            'stocks_json':serializer.data,
            # 'lucro': lucro,
            'obj': obj,
        }
        return render(request, self.template_name, context)


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
            all_lists.append([datas[0][3][i], labs[i], variance[i]])
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


    labs, datas, variance, prev = get_historicalData(obj.symbol)

    all_lists = []
    for i in range(0, len(variance)):
        all_lists.append([datas[0][3][i], labs[i], variance[i]])
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

