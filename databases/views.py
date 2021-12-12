from datetime import datetime
from django.shortcuts import render
from django.http import HttpResponse
import yfinance as yf
import numpy as np
from databases.models import Stock
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
