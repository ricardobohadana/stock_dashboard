from datetime import datetime, date, timedelta
import pandas_datareader as web
import numpy as np
import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
from .models import Stock, Wallet
import math
import time
pd.options.mode.chained_assignment = None


def get_Stock_Data_old(symbol):
    url = 'https://finance.yahoo.com/quote/'+ symbol +'.SA?p='+ symbol +'.SA&.tsrc=fin-srch'
    r = requests.get(url)
    if r.status_code != 200:
        print('Status code error')
        return 1
    sp = BeautifulSoup(r.text, "lxml")
    try:
        vet = sp.find('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'}).find_all('span')
        price = float(vet[0].text)
        change_percentage = vet[1].text.split(' ')[1][1:5]
    except ValueError:
        change_percentage = vet[1].text.split(' ')[1][2:6]
    except AttributeError:
        return 1
    # updated = vet[2].text[11:17]
    # name = sp.find('div', {'class':'quote-header-section Cf Pos(r) Mb(5px) Maw($maxModuleWidth) Miw($minGridWidth) smartphone_Miw(ini) Miw(ini)!--tab768 Miw(ini)!--tab1024 Mstart(a) Mend(a) Px(20px) smartphone_Pb(0px) smartphone_Mb(0px)'}).find('h1').text[11:]
    jsobj = {
        'price': price,
        'change_percent': change_percentage,
        'symbol': symbol,
    }
    return jsobj



# ADQUIRE OS DADOS REFERENTE A AÇÃO DESEJADA
def get_Stock_Data(symbol):
    # start = time.process_time()
    try:
        today = datetime.today().strftime("%Y-%m-%d")
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        df = web.DataReader(symbol.upper()+'.SA', data_source='yahoo', start=yesterday, end=today)
        if len(df) == 1:
            yesterday = (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
            df = web.DataReader(symbol.upper()+'.SA', data_source='yahoo', start=yesterday, end=today)

        price_today =  round(df.Close.values[1], 2)
        price_yesterday = round(df.Close.values[0], 2)
        variance = round((((df.Close.values[1]/df.Close.values[0])-1)*100), 2)
    
        jsobj = {
            'price': price_today,
            'change_percent': variance,
            'symbol': symbol,
            }

    except:
        jsobj = get_Stock_Data_old(symbol)
    
    return jsobj



# ADQUIRE OS DADOS HISTÓRICOS DE 180 DIAS
def get_historicalData(symbol, ndays=180):
    today = datetime.today().strftime("%Y-%m-%d")
    days_180 = (datetime.today() - timedelta(ndays)).strftime("%Y-%m-%d")
    df = web.DataReader(symbol.upper()+'.SA', data_source='yahoo', start=days_180, end=today)
    df['Variance'] = 0.00
    for i in range(len(df['Close'])):
        if i == 0:
            df['Variance'][i] = 0.00
        else:
            a = df.Close.values[i-1]
            b = df.Close.values[i]
            df['Variance'][i] = round((((b/a)-1)*100),2)
    df, prev = get_SMA(df)    
    variance = round((((df.Close.values[1]/df.Close.values[0])-1)*100), 2)
    datas = [[],[],[],[]]
    datas[0] = [[round(pr, 2) for pr in df.Open.tolist()], [round(pr, 2) for pr in df.High.tolist()],[round(pr, 2) for pr in df.Low.tolist()],[round(pr, 2) for pr in df.Close.tolist()]]
    datas[1] = [None if math.isnan(s) else round(s, 2) for s in df['SMA(14)'].tolist()]
    datas[2] = [None if math.isnan(r) else round(r, 2) for r in df['SMA(30)'].tolist()]
    datas[3] = [None if math.isnan(t) else round(t, 2) for t in df['SMA(7)'].tolist()]
    variance = df.Variance.tolist()
    labs = [dat.strftime("%Y-%m-%d") for dat in df.index.tolist()]

    return labs, datas, variance, prev
    

# PEGA OS ÍNDICES DA IBOVESPA
def get_ibovespaData():
    try:
        today = datetime.today().strftime("%Y-%m-%d")
        yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
        df = web.DataReader('^BVSP', data_source='yahoo', start=yesterday, end=today)
        change_percent = round( ((df.Close[-1]/df.Close[0])-1)*100 ,2)
        change_points = df.Close[-1] - df.Close[0]
        jsobj = {
            'price': df.Close['-1'],
            'change_percent': change_percent,
            'change_points': change_points,
        }
        return jsobj
    except:
        url = 'https://finance.yahoo.com/quote/%5EBVSP?p=^BVSP&.tsrc=fin-srch'
        r = requests.get(url)
        if r.status_code != 200:
            print('Status code error')
            return 1
        sp = BeautifulSoup(r.text, "lxml")
        try:
            vet = sp.find('div', {'class':'My(6px) Pos(r) smartphone_Mt(6px)'}).find_all('span')
            price = float((vet[0].text.replace(',','')))
            change_points = vet[1].text.split(' ')[0].replace(',','')
            change_percentage = float(vet[1].text.split(' ')[1][1:6])
        except ValueError:
            change_percentage = float(vet[1].text.split(' ')[1][2:6])
        except AttributeError:
            return 1
        # updated = vet[2].text[11:17]
        jsobj = {
            'price': price,
            'change_percent': change_percentage,
            'change_points': change_points,
        }
        return jsobj

def get_SMA(df):
    df['SMA(14)'] = df.Close.rolling(14).mean()
    df['SMA(30)'] = df.Close.rolling(30).mean()
    df['SMA(7)'] = df.Close.rolling(7).mean()
    prev = [[], [], []]
    prev[0].append(round(df['Close'][-14:].sum()/14, 2))
    prev[0].append(round(((prev[0][0]/df['Close'][-1])-1)*100,2))
    prev[0].append('14')
    prev[1].append(round(df['Close'][-30:].sum()/30, 2))
    prev[1].append(round(((prev[1][0]/df['Close'][-1])-1)*100,2))
    prev[1].append('30')
    prev[2].append(round(df['Close'][-7:].sum()/7, 2))
    prev[2].append(round(((prev[2][0]/df['Close'][-1])-1)*100,2))
    prev[2].append('7')

    return df, prev

def updateWallet():
    wallet = Wallet.objects.all()
    for item in wallet:
        obj = Wallet.objects.filter(pk=item.pk)
        money_amount = round(obj[0].stock.price * obj[0].stock_amount, 2)
        obj.update(money_amount=money_amount)
    return True


def getAbsoluteHighLow():
    high, low = [], []
    for stock in Stock.objects.raw('SELECT * FROM accounts_stock WHERE change_percent > 0 ORDER BY change_percent DESC;'):
        try:
            price_change = round(stock.price - (stock.price/((stock.change_percent/100)+1)), 2)
            high.append({"price_change": price_change, "symbol":stock.symbol, "price":stock.price})
        except (IndexError, TypeError):
            break

    for stock in Stock.objects.raw('SELECT * FROM accounts_stock WHERE change_percent < 0 ORDER BY change_percent DESC;'):
        try:
            price_change = round(stock.price - (stock.price/((stock.change_percent/100)+1)),2)
            low.append({'price_change': price_change, "symbol":stock.symbol, "price":stock.price})
        except (IndexError, TypeError):
            break
    high_final = sorted(high, key=lambda k: k['price_change'], reverse=True)[:5]
    low_final = sorted(low, key=lambda x: x['price_change'])[:5]
    return high_final, low_final
        

def getHistoricalIbovespa(ndays=180):
    today = datetime.today().strftime("%Y-%m-%d")
    days = (datetime.today() - timedelta(ndays)).strftime("%Y-%m-%d")
    df = web.DataReader("^BVSP", data_source='yahoo', start=days, end=today)
    df['Variance'] = 0.00
    for i in range(len(df['Close'])):
        if i == 0:
            df['Variance'][i] = 0.00
        else:
            a = df.Close.values[i-1]
            b = df.Close.values[i]
            df['Variance'][i] = round((((b/a)-1)*100),2)
    df['SMA10'] = df.Close.rolling(10).mean()
    df['EWMA'] = df.Close.ewm(alpha=1, min_periods=15).mean()
    High = [None if math.isnan(s) else round(s, 2) for s in df.High.tolist()]
    Close = [None if math.isnan(s) else round(s, 2) for s in df.Close.tolist()]
    Open = [None if math.isnan(s) else round(s, 2) for s in df.Open.tolist()]
    Low = [None if math.isnan(s) else round(s, 2) for s in df.Low.tolist()]
    Variance = [None if math.isnan(s) else round(s, 2) for s in df.Variance.tolist()]
    sma10 = [None if math.isnan(s) else round(s, 2) for s in df['SMA10'].tolist()]
    ewma = [None if math.isnan(s) else round(s, 2) for s in df.EWMA.tolist()]
    labs =  [s.to_pydatetime() for s in df.index.tolist()]
    
    jsobj = {
        'High': High,
        'Open': Open,
        'Low': Low,
        'Close': Close,
        'Variance': Variance,
        'sma10': sma10,
        'labs': labs,
        'ewma': ewma,
    }
    return jsobj
# # REMOVE AS DUPLICATAS DE UMA LISTA
# def check_2_remove(vet):
#     for item in vet:
#         if vet.count(item) > 1:
#             vet.remove(item)



# # CHECA SE UM OBJETO NA DATABASE JÁ EXISTE PARA EVITAR ADICIONÁ-LO MAIS DE UMA VEZ
# def check_duplicate(obj, symbol, update):
#     symbol = symbol.upper()
#     filter_stocks = Stock.objects.filter(symbol=obj['symbol'])
#     if len(filter_stocks) == 0:
#         return True
#     else:
#         if update:
#             return True
#         else:
#             return False


# # PEGA OS OBJETOS AÇÃO DIFERENTES E MAIS ATUALIZADOS
# def get_diff_stocks():
#     stocks = Stock.objects.all()
#     if len(stocks) == 0:
#         return []
#     st = [stocks[0].symbol]
#     for i in range(1, len(stocks)):
#         if stocks[i].symbol not in st:
#             st.append(stocks[i].symbol)
#     st_final = [Stock.objects.filter(symbol=item).latest('updated') for item in st]
#     # for item in st:
#     #     st_final.append(Stock.objects.filter(symbol=item).latest('updated'))
#     return st_final
