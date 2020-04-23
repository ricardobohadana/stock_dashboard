import requests
import bs4
from bs4 import BeautifulSoup
from .models import Stock

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


# ADQUIRE OS DADOS REFERENTE A AÇÃO DESEJADA
def get_Stock_Data(symbol):
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
    name = sp.find('div', {'class':'quote-header-section Cf Pos(r) Mb(5px) Maw($maxModuleWidth) Miw($minGridWidth) smartphone_Miw(ini) Miw(ini)!--tab768 Miw(ini)!--tab1024 Mstart(a) Mend(a) Px(20px) smartphone_Pb(0px) smartphone_Mb(0px)'}).find('h1').text[11:]
    jsobj = {
        'price': price,
        'change_percent': change_percentage,
        # 'updated': updated,
        'name': name,
        'symbol': symbol,
    }
    return jsobj


# CRIA O OBJETO NA DATABASE NO CASO DE UM UPDATE
def create_Stock_object(symbol, update):
    jsobj = get_Stock_Data(symbol)
    if jsobj == 1:
        return False
    else:
        if check_duplicate(jsobj, symbol, update):
            obj = Stock.objects.create(
                    symbol = symbol,
                    name = jsobj['name'],
                    price = jsobj['price'],
                    # updated = jsobj['updated'], 
                    change_percent = jsobj['change_percent'],
                )
            return obj
        else:
            return print('é duplicata')
        


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
    st_final = []
    for item in st:
        st_final.append(Stock.objects.filter(symbol=item).latest('updated'))
    return st_final


# ADQUIRE OS DADOS HISTÓRICOS DE 3 MESES
def get_historicalData(symbol):
    symbol = 'MGLU3'
    url = 'https://finance.yahoo.com/quote/'+symbol.upper()
    last3months = '.SA/history?p='+symbol.upper() + '.SA'
    r = requests.get(url+last3months)
    sp = BeautifulSoup(r.text, "lxml")
    vet = sp.find('div', {'class':'Pb(10px) Ovx(a) W(100%)'}).find('tbody')
    labs = []
    datas = []
    for item in vet:
        try:
            labs.append(item.find('td', {'class':'Py(10px) Ta(start) Pend(10px)'}).text)
            datas.append(float(item.find_all('td', {'class':'Py(10px) Pstart(10px)'})[3].text))
        except IndexError:
            pass
        except ValueError:
            labs.pop()

            


    check_2_remove(labs)
    # check_2_remove(datas)
    labs.reverse()
    datas.reverse()
    return labs, datas


# REMOVE AS DUPLICATAS DE UMA LISTA
def check_2_remove(vet):
    for item in vet:
        if vet.count(item) > 1:
            vet.remove(item)