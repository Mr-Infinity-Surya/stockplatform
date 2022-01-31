import yfinance as yf
import datetime
import redis
import plotly.graph_objs as go
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import numpy as np
import keras
import tensorflow as tf
import json
from keras.preprocessing.sequence import TimeseriesGenerator

from keras.models import Sequential
from keras.layers import LSTM, Dense


def predict(num_prediction, model,close_data,look_back):
    prediction_list = close_data[-look_back:]
    
    for _ in range(num_prediction):
        x = prediction_list[-look_back:]
        x = x.reshape((1, look_back, 1))
        out = model.predict(x)[0][0]
        prediction_list = np.append(prediction_list, out)
    prediction_list = prediction_list[look_back-1:]
        
    return prediction_list
    
def predict_dates(num_prediction,last_date):
    prediction_dates = pd.date_range(last_date, periods=num_prediction+1).tolist()
    return prediction_dates

def redis_pred():
    """
    usage : 
    (pred_graph,current_graph,predicted_values,predecited_dates) = predction("AAPL")
    returns 10 days of predtion
    """
    stock_name =  ['AXISBANK.NS','BHARTIARTL.NS','CIPLA.NS','HCLTECH.NS','ICICIBANK.NS','ITC.NS','KOTAKBANK.NS','JSWSTEEL.NS','MARUTI.NS','POWERGRID.NS','SBIN.NS','TATAMOTORS.NS','TATASTEEL.NS','TCS.NS','WIPRO.NS','EICHERMOT.NS','GRASIM.NS', 'HINDUNILVR.NS', 'IOC.NS', 'LT.NS', 'NESTLEIND.NS', 'NTPC.NS','SUNPHARMA.NS', 'TECHM.NS', 'ULTRACEMCO.NS']
    for name in stock_name:
        #name = i + '_pred'
        data=yf.Ticker(name)
        df = data.history(start='2020-01-01', end=datetime.datetime.today(), interval="1d")[["Open","High","Low","Close","Volume"]]
        df.index = pd.to_datetime(df.index)
        df.set_axis(df.index, inplace=True)
        df.drop(columns=['Open', 'High', 'Low', 'Volume'], inplace=True)

        close_data = df['Close'].values
        close_data = close_data.reshape((-1,1))
        
        close_train = close_data
        date_train = df.index

        look_back = 15

        train_generator = TimeseriesGenerator(close_train, close_train, length=look_back, batch_size=20)

        model = Sequential()
        model.add(
            LSTM(20,
                activation='relu',
                input_shape=(look_back,1))  
        )
        model.add(Dense(1))
        model.compile(optimizer='adam', loss='mse')

        num_epochs = 30
        model.fit_generator(train_generator, epochs=num_epochs, verbose=1)

        close_data = close_data.reshape((-1))


        num_prediction = 10
        forecast = predict(num_prediction, model,close_data,look_back)
        forecast_dates = predict_dates(num_prediction,df.index.values[-1])



        new_array = np.array(df.index.to_pydatetime())

        new_array = [x.strftime('%y-%m-%d') for x in new_array]

        curr_val = close_data[-1]
        diff = curr_val - forecast[0]
        forecast = forecast + diff

        
        trace1 = go.Scatter(
            x=df.index[-150:], y=close_data[-150:],
            mode = 'lines',
            name = 'Data'
        )
        trace2 = go.Scatter(
            x=forecast_dates,y= forecast,
            mode = 'lines',
            name = 'Prediction'
        )
        layout = go.Layout(
            title = name + " Predicted Values",
            xaxis = {'title' : "Date"},
            yaxis = {'title' : "Close"}
        )

        tracefig2 = go.Scatter(
            x=new_array,y= close_data
        )
        layoutfig2 = go.Layout(
            title = name,
            xaxis = {'title' : "Date"},
            yaxis = {'title' : "Close"}
        )
        fig2 = go.Figure(data=[tracefig2], layout=layoutfig2)
        fig = go.Figure(data=[trace1, trace2], layout=layout)

        r = redis.StrictRedis(host='localhost',port='6379',db=0,password='Stock@123')
        i = name + '_pred'
        res = []
        context={}
        context['fig'] = fig.to_html()
        context['fig2'] = fig2.to_html()
        res.append(context)
        x = json.dumps(res)
        r.set(i,x)
        r.save()
        print("Done" + i)
        #print(json.loads(r.get(i))[0]['fig'])

redis_pred()

