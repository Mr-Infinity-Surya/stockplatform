from datetime import datetime
from django.conf.urls import url
from django.shortcuts import render
from django.http import HttpResponse
import yfinance as yf
import numpy as np
from databases.models import Bank, Company, Investment, Stock
import plotly.graph_objs as go
from django.contrib.auth.models import User

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

