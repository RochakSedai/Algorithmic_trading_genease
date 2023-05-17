from django.shortcuts import render
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import pandas_datareader.data as web
import datetime as dt
import yfinance as yf
import talib
import sys

# Create your views here.
def home(request):
    return render(request, 'home.html')



# SMA trading strategy
class MySMAStrategy(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 = 10
    n2 = 20

    def init(self):
        price = self.data.Close
        self.ma1 = self.I(SMA, price, self.n1)
        self.ma2 = self.I(SMA, price, self.n2)

    def next(self):
        if crossover(self.ma1, self.ma2):
            self.buy()
        elif crossover(self.ma2, self.ma1):
            self.sell()

# MACD Strategy
class MyMACDStrategy(Strategy):

    def init(self):
        price = self.data.Close
        self.macd = self.I(lambda x: talib.MACD(x)[0], price)
        self.macd_signal = self.I(lambda x: talib.MACD(x)[1], price)

    def next(self):
        if crossover(self.macd, self.macd_signal):
            self.buy()
        elif crossover(self.macd_signal, self.macd):
            self.sell()  

# RSIOscillator Strategy
class RsiOscillator(Strategy):
    upper_bound = 70
    lower_bound = 30
    rsi_window = 14

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, self.rsi_window)

    def next(self):
        if crossover(self.rsi, self.upper_bound):
            self.position.close()
        elif crossover(self.lower_bound, self.rsi):
            self.buy()




def backtest(request):
    if request.method == 'POST':
        content = request.POST.dict()
        email  = content.get('email')
        ticker = content.get('stock')
        trading_strategy = content.get('strategy')

    print(ticker)
    print(trading_strategy)
    _start = dt.date(2020, 1, 1)
    _end = dt.date(2022, 1, 1)
    # data = web.DataReader(ticker, data_source="yahoo", start=start, end=end)
    data = yf.download(ticker, start = _start, end = _end)

    if trading_strategy == 'SMA':
        print('Hello')
        backtest_result = Backtest(data, MySMAStrategy, commission=0.002, exclusive_orders=True)
        stats_before = backtest_result.run()
        print(stats_before)
        print("/////////////////////////////////////////////////////////////////////////////")
        stats_after = backtest_result.optimize(n1=range(5, 30, 5),
                    n2=range(10, 70, 5),
                    maximize='Equity Final [$]',
                    constraint=lambda param: param.n1 < param.n2)
        print(stats_after)
        print("-----------------")
        print(stats_after._strategy)
        print(type(stats_after))
      
        context = {
            'Before_return' :  stats_before['Return [%]'],
            'After_return': stats_after['Return [%]'],
            'Buy_and_Hold_return': stats_after['Buy & Hold Return [%]'],
            'trading_strategy': trading_strategy,
        }

    elif trading_strategy ==  'MACD':
        print('HI')
        backtest_result = Backtest(data, MyMACDStrategy, commission=0.002, exclusive_orders=True)
        stats = backtest_result.run()
        print(stats)

    elif trading_strategy == 'RSI':
        backtest_result = Backtest(data, RsiOscillator, commission=0.002, exclusive_orders=True)
        stats = backtest_result.run()
        print(stats)
        print("/////////////////////////////////////////////////////////////////////////////")
        stats = backtest_result.optimize(
            upper_bound = range(55, 85, 5),
            lower_bound = range(10, 85, 5),
            rsi_window = range(10,30,2),
            maximize = 'Equity Final [$]',
            constraint = lambda param: param.lower_bound < param.upper_bound
        )
        print(stats)
        print("-----------------")
        print(stats._strategy)

    return render(request, 'home.html', context)