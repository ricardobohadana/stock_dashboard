from datetime import datetime, date, timedelta
import pandas_datareader as web
import numpy as np
import pandas as pd
import requests
import bs4
from bs4 import BeautifulSoup
from .models import Stock
import math
import time
pd.options.mode.chained_assignment = None


# MEDIR O TEMPO DE PROCESSAMENTO DE CADA FUNÇÃO

# CRIA O OBJETO JSON QUE SERÁ PASSADO PARA A PÁGINA HTML
def createJSON():
    stocks = Stock.objects.all()
    dic = {}
    for i in range(0, len(stocks)):
        if dic.get(stocks[i].symbol) != None:
            dic[stocks[i].symbol] = dic[stocks[i].symbol].append({
                'price': stocks[i].price,
                'updated': stocks[i].updated
                })
        else:
            dic[stocks[i].symbol] = [{
                'price': stocks[i].price,
                'updated': stocks[i].updated
                }]
    return dic

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
        change_percentage = vet[1].text.split(' ')[1][1:6]
    except ValueError:
        change_percentage = vet[1].text.split(' ')[1][2:7]
    except AttributeError:
        return 1
    # updated = vet[2].text[11:17]
    # name = sp.find('div', {'class':'quote-header-section Cf Pos(r) Mb(5px) Maw($maxModuleWidth) Miw($minGridWidth) smartphone_Miw(ini) Miw(ini)!--tab768 Miw(ini)!--tab1024 Mstart(a) Mend(a) Px(20px) smartphone_Pb(0px) smartphone_Mb(0px)'}).find('h1').text[11:]
    jsobj = {
        'price': price,
        'change_percent': change_percentage,
        # 'updated': updated,
        # 'name': name,
        'symbol': symbol,
    }
    return jsobj



# ADQUIRE OS DADOS REFERENTE A AÇÃO DESEJADA
def get_Stock_Data(symbol):
    # start = time.process_time()
    try:
        try:
            today = datetime.today().strftime("%Y-%m-%d")
            yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
            df = web.DataReader(symbol.upper()+'.SA', data_source='yahoo', start=yesterday, end=today)
            price_today =  round(df.Close.values[1], 2)
            price_yesterday = round(df.Close.values[0], 2)
            variance = round((((df.Close.values[1]/df.Close.values[0])-1)*100), 2)
        except:
            today = datetime.today().strftime("%Y-%m-%d")
            yesterday = (datetime.today() - timedelta(days=2)).strftime("%Y-%m-%d")
            df = web.DataReader(symbol.upper()+'.SA', data_source='yahoo', start=yesterday, end=today)
            price_today =  round(df.Close.values[1], 2)
            price_yesterday = round(df.Close.values[0], 2)
            variance = round((((df.Close.values[1]/df.Close.values[0])-1)*100), 2)

        jsobj = {
            'price': price_today,
            'change_percent': variance,
            # 'updated': updated,
            # 'name': name,
            'symbol': symbol,
        }

    except:
        jsobj = get_Stock_Data_old(symbol)
    
    # name = sp.find('div', {'class':'quote-header-section Cf Pos(r) Mb(5px) Maw($maxModuleWidth) Miw($minGridWidth) smartphone_Miw(ini) Miw(ini)!--tab768 Miw(ini)!--tab1024 Mstart(a) Mend(a) Px(20px) smartphone_Pb(0px) smartphone_Mb(0px)'}).find('h1').text[11:]
    # print('Processamento de get_Stock_Data(): ' + str(time.process_time() - start))
    return jsobj


# CRIA O OBJETO NA DATABASE NO CASO DE UM UPDATE
def create_Stock_object(symbol, update):
    # start = time.process_time()
    # print('Processamento de create_Stock_object(): ' + str(time.process_time() - start))
    jsobj = get_Stock_Data(symbol)
    if jsobj == 1:
        return False
    else:
        if check_duplicate(jsobj, symbol, update):
            obj = Stock.objects.create(
                    symbol = symbol,
                    # name = jsobj['name'],
                    price = jsobj['price'],
                    # updated = jsobj['updated'],
                    change_percent = jsobj['change_percent'],
                )
            return obj
        else:
            return print('é duplicata')
    # print('Processamento de create_Stock_object(): ' + str(time.process_time() - start))



# CHECA SE UM OBJETO NA DATABASE JÁ EXISTE PARA EVITAR ADICIONÁ-LO MAIS DE UMA VEZ
def check_duplicate(obj, symbol, update):
    symbol = symbol.upper()
    filter_stocks = Stock.objects.filter(symbol=obj['symbol'])
    if len(filter_stocks) == 0:
        return True
    else:
        if update:
            return True
        else:
            return False


# PEGA OS OBJETOS AÇÃO DIFERENTES E MAIS ATUALIZADOS
def get_diff_stocks():
    stocks = Stock.objects.all()
    if len(stocks) == 0:
        return []
    st = [stocks[0].symbol]
    for i in range(1, len(stocks)):
        if stocks[i].symbol not in st:
            st.append(stocks[i].symbol)
    st_final = [Stock.objects.filter(symbol=item).latest('updated') for item in st]
    # for item in st:
    #     st_final.append(Stock.objects.filter(symbol=item).latest('updated'))
    return st_final


# ADQUIRE OS DADOS HISTÓRICOS DE 180 DIAS
def get_historicalData(symbol, ndays):
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
    datas[0] = [round(pr, 2) for pr in df.Close.tolist()]
    datas[1] = [None if math.isnan(s) else round(s, 2) for s in df['SMA(14)'].tolist()]
    datas[2] = [None if math.isnan(r) else round(r, 2) for r in df['SMA(30)'].tolist()]
    datas[3] = [None if math.isnan(t) else round(t, 2) for t in df['SMA(7)'].tolist()]
    variance = df.Variance.tolist()
    labs = [dat.strftime("%Y-%m-%d") for dat in df.index.tolist()]

    return labs, datas, variance, prev
    


# REMOVE AS DUPLICATAS DE UMA LISTA
def check_2_remove(vet):
    for item in vet:
        if vet.count(item) > 1:
            vet.remove(item)



# PEGA OS ÍNDICES DA IBOVESPA
def get_ibovespaData():
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