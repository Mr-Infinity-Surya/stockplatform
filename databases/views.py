from datetime import datetime
import json

from django.shortcuts import redirect, render
from django.http import HttpResponse
import yfinance as yf
import numpy as np
from databases.models import Bank, Company, Investment, Stock
import plotly.graph_objs as go
from django.contrib.auth.models import User
import redis

# Create your views here.
def index(request):
    return HttpResponse("OK")

def stock_manage(request):
    if request.user.is_authenticated :
        #define the ticker symbol
        print(request.GET)
        stockt = request.GET['name'] #'TATAPOWER.NS'
        #get data on this ticker
        data = yf.Ticker(stockt).history(start='2021-01-02',end=datetime.today().strftime('%Y-%m-%d'),interval="1d")[["Open","High","Low","Close","Volume"]]
        stockdata = data.info
        #stock = Stock(request.POST)
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index,open = data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name = 'market data'))
        fig.update_layout(title = f'share price of {stockt}', yaxis_title = 'Stock Price')
        x = fig.to_html()
        context = {}
        context['stock'] = x
        #print(x,"123")
        return HttpResponse(x)
    else:
        return HttpResponse("<h1> Illegal request </h1>")
    # return render(request,'index.html',context)

def user_stock(request):
    if request.user.is_authenticated:
        if Stock.objects.filter(ISIN = Investment.objects.get(User_Account_no= Bank.objects.get(Username=request.user.username).Account_no).Stock_ISIN).exists() is True:
            stocku = Stock.objects.get(ISIN = Investment.objects.get(User_Account_no= Bank.objects.get(Username=request.user.username).Account_no).Stock_ISIN)
            return HttpResponse("ok<br>{{stocku}}")
        else:
            return HttpResponse("Error")
        
def get_stock_data(stock_name):
    data=yf.Ticker(stock_name)
    info = data.info
    stk_values = {'currentPrice','beta','volume','regularMarketOpen','revenueGrowth','dayHigh','open','previousClose','dayLow'}
    cmp_values = {'sector','industry','longBusinessSummary','website','grossProfits','longName'}
    stk_res = {key: info[key] for key in info.keys() & stk_values}
    cmp_res = {key: info[key] for key in info.keys() & cmp_values}
    stk_res['ISIN'] = data.isin
    stk_res['Name'] = stock_name
    cmp_res['ISIN'] = stk_res['ISIN']
    return stk_res,cmp_res

def fill_db(request):
    if request.user.is_superuser:
        st = Stock()
        stk_list = ['AXISBANK.NS','BHARTIARTL.NS','CIPLA.NS','HCLTECH.NS','ICICIBANK.NS','ITC.NS','KOTAKBANK.NS','JSWSTEEL.NS','MARUTI.NS','POWERGRID.NS','SBIN.NS','TATAMOTORS.NS','TATASTEEL.NS','TCS.NS','WIPRO.NS','EICHERMOT.NS','GRASIM.NS', 'HINDUNILVR.NS', 'IOC.NS', 'LT.NS', 'NESTLEIND.NS', 'NTPC.NS','SUNPHARMA.NS', 'TECHM.NS', 'ULTRACEMCO.NS']
        for i in stk_list:
            if Stock.objects.filter(Name = i).exists() is True:
                return HttpResponse("Already updated")
        for x in stk_list:
            st = Stock() 
            stk_res,cmp_res = get_stock_data(x)
            st.Name = str(stk_res['Name'])
            st.ISIN = str(stk_res['ISIN'])
            st.Volume = int(stk_res['volume'])
            st.Prev_Close = float(stk_res['previousClose'])
            st.Day_low =  float(stk_res['dayLow'])
            st.Current_price =  float(stk_res['currentPrice'])
            st.Beta =  float(stk_res['beta'])
            st.Regular_market_open =  float(stk_res['regularMarketOpen'])
            st.Day_high =  float(stk_res['dayHigh'])
            st.Open =  float(stk_res['open'])
            st.Revenue_growth =  float(stk_res['revenueGrowth'])
            print(st)
            st.clean()
            st.save()
        return HttpResponse("ok<br>{{Stock.objects.all}}")
    else:
        return HttpResponse("<h1> Hello, ur not supposed to enter HERE !!!!! </h1>")

def fill_db2(request):
    if request.user.is_superuser:
        co = Company()
        stk_list = ['SBIN.NS','TATAMOTORS.NS','TATASTEEL.NS','TCS.NS','WIPRO.NS','EICHERMOT.NS','GRASIM.NS', 'HINDUNILVR.NS', 'IOC.NS', 'LT.NS', 'NESTLEIND.NS', 'NTPC.NS','SUNPHARMA.NS', 'TECHM.NS', 'ULTRACEMCO.NS']   #'AXISBANK.NS','BHARTIARTL.NS','CIPLA.NS','HCLTECH.NS','ICICIBANK.NS','ITC.NS','KOTAKBANK.NS','JSWSTEEL.NS','MARUTI.NS','POWERGRID.NS'
        for i in stk_list:
            if Company.objects.filter(Name = i).exists() is True:
                return HttpResponse("Already updated")
        for x in stk_list:
            co = Company() 
            stk_res,cmp_res = get_stock_data(x)
            co.Name = str(cmp_res['longName'])
            co.Stock_ISIN = Stock.objects.get(ISIN = str(cmp_res['ISIN']))
            co.Sector = str(cmp_res['sector'])    
            co.Industry = str(cmp_res['industry'])
            co.Business_Summary =str(cmp_res['longBusinessSummary'])
            co.Website = cmp_res['website']
            co.Gross_Profit = float(cmp_res['grossProfits'])
            print(co)
            co.clean()
            co.save()
        x = Stock.objects.all()
        return HttpResponse("ok<br>{{x}}")
    else:
        return HttpResponse("<h1> Hello, ur not supposed to enter HERE !!!!! </h1>")


def get_topnews(ticker_obj,p):
    result = []
    news_data = ticker_obj.news[:p]
    for item in news_data:
        result.append({key: item[key] for key in item.keys() & {'title','link'}})
    return result

def redis_data(request):
    # Link : https://stackoverflow.com/questions/15219858/how-to-store-a-complex-object-in-redis-using-redis-py
    r = redis.StrictRedis(host='localhost',port='6379',db=0)
    if request.user.is_superuser:
        if (request.GET['num'] == ''):
            return HttpResponse("<h1> Hello, ur not supposed to enter HERE !!!!! </h1>")
        p = int(request.GET['num'])
        stock_name =  ['AXISBANK.NS','BHARTIARTL.NS','CIPLA.NS','HCLTECH.NS','ICICIBANK.NS','ITC.NS','KOTAKBANK.NS','JSWSTEEL.NS','MARUTI.NS','POWERGRID.NS','SBIN.NS','TATAMOTORS.NS','TATASTEEL.NS','TCS.NS','WIPRO.NS','EICHERMOT.NS','GRASIM.NS', 'HINDUNILVR.NS', 'IOC.NS', 'LT.NS', 'NESTLEIND.NS', 'NTPC.NS','SUNPHARMA.NS', 'TECHM.NS', 'ULTRACEMCO.NS']
        for i in stock_name:
            if r.get(i) is None or p != 0:
                data=yf.Ticker(i)
                res = get_topnews(data,p)
                print(res)
                x = json.dumps(res)
                r.set(i,x)
                r.save()
        res = json.loads(r.get(stock_name[0]))  #Retriving data from json
        y = res[0]['title']
        return HttpResponse(f'<h1> okk <br><br>{y} </h1>')
    elif request.user.is_authenticated:
        if request.method == 'GET':
            name = request.GET['name']
            data=yf.Ticker(name)
            res2 = json.dumps(get_topnews(data,5))
            res = json.loads(r.get(name))
            if str(res2) != str(res):
                r.set(name,res2)
                r.save()
            context={}
            context['news'] = res
            context['name'] = name
            stockobj = Stock.objects.get(Name=name)
            print(stockobj)
            context['stock'] = stockobj
            return render(request,'apinews.html',context)
        else:
            return HttpResponse("<h1> Hello, ur not supposed to enter HERE !!!!! </h1>")
    else:
        return HttpResponse("<h1> Hello, ur not supposed to enter HERE !!!!! </h1>")



def buyupdate(request):
    print(request.POST)
    if request.user.is_authenticated and 'Buy' in request.POST:
        print(request.POST)
        if request.POST['Quantity'] == '':
            return HttpResponse('<h1>Please Enter quantity</h1>')
        quantity = int(request.POST['Quantity']) # GET from page
        stk_name = request.GET['name']#"TATAPOWER.NS" #GET FROM PAGE
        loguser = request.user.username
        bankobj=Bank.objects.get(Username=loguser)
        accno=bankobj.Account_no
        invested = Investment.objects.raw("SELECT id,Stock_ISIN_id FROM databases_investment WHERE User_Account_no_id='"+accno+"'")
        purchased = 0
        done = 0
        for x in invested : 
            stk = Stock.objects.get(ISIN=x.Stock_ISIN_id)
            if (stk.Name == stk_name) :
                #stk is purchased
                if(bankobj.Current_amount < stk.Current_price*quantity):
                    purchased = 1
                    invested2 = Investment.objects.get(id=x.id)
                    invested2.Quantity += int(quantity)
                    invested2.Purchased_Value = stk.Current_price
                    invested2.Date_of_Purchased = datetime.today()
                    invested2.save()
                    bankobj.Current_amount -= int(stk.Current_price*int(quantity))
                    bankobj.save()
                    done = 1
                    
        if(purchased==0):
            stk = Stock.objects.get(Name=stk_name)
            investobj = Investment()
            investobj.Quantity = quantity
            investobj.Date_of_Purchased = datetime.today()
            investobj.Purchased_Value = stk.Current_price
            investobj.User_Account_no = bankobj
            investobj.Stock_ISIN = stk
            investobj.save()
            bankobj.Current_amount -= int(stk.Current_price*int(quantity))
            bankobj.save()
            done = 1
        if(done==0) :
            return HttpResponse("<h1> Buy fail </h1>")
        else:
            return redirect('dashboard:index')
    elif request.user.is_authenticated and 'Sell' in request.POST:
        return sellupdate(request) #redirect('databases:sell')#
    else:
        return HttpResponse("<h1> Buy fail </h1>")

def sellupdate(request):
    if request.user.is_authenticated and 'Sell' in request.POST:
        print(request.POST)
        if request.POST['Quantity'] == '':
            return HttpResponse('<h1>Please Enter quantity</h1>')
        quantity = int(request.POST['Quantity']) # GET from page
        stk_name = request.GET['name'] #"TATAPOWER.NS" #GET FROM PAGE
        loguser = request.user.username
        bankobj = Bank.objects.get(Username=loguser)
        accno=bankobj.Account_no
        invested = Investment.objects.raw("SELECT id,Stock_ISIN_id FROM databases_investment WHERE User_Account_no_id='"+accno+"'")
        purchased = 0
        done = 0
        for x in invested : 
            stk = Stock.objects.get(ISIN=x.Stock_ISIN_id)
            if (stk.Name == stk_name) :
                #stk is purchased
                if(x.Quantity >= quantity):
                    invested2 = Investment.objects.get(id=x.id)
                    if invested2.Quantity == quantity:
                        invested2.delete()
                    else:
                        invested2.Quantity -= quantity
                        bankobj.Current_amount += quantity*float(stk.Current_price)
                        invested2.save()
                        bankobj.save()
                    done = 1
                    break
                else : 
                    return HttpResponse('<h1> Not enough quantity in your holdings </h1>')#say not enough quantity
        if(done == 0) : 
            return HttpResponse('<h1> you have not purchased stock </h1>') #say you have not purchased stock
        else:
            return redirect('dashboard:index')
    elif request.user.is_authenticated and 'Buy' in request.POST:
        return buyupdate(request) # redirect('databases:buy_sell')  #
    else:
        return HttpResponse("<h1> Sell fail </h1>")
