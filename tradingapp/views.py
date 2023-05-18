from django.shortcuts import render
from django.template.loader import get_template
from django.views.generic.base import View
from django.http import HttpResponse
from django.contrib import messages
from backtesting import Backtest, Strategy
from backtesting.lib import crossover
from backtesting.test import SMA, GOOG
import pandas_datareader.data as web
import datetime as dt
import yfinance as yf
import talib
from .checker import check_symbol

# Create your views here.
def home(request):
    return render(request, 'home.html')

# SMA trading strategy
class MySMAStrategy(Strategy):
    # Define the two MA lags as *class variables*
    # for later optimization
    n1 =  15
    n2 = 10

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

    # getting the form input
    if request.method == 'POST':
        content = request.POST.dict()
        email  = content.get('email')
        ticker = content.get('stock')
        trading_strategy = content.get('strategy')
    
    # checking whether the ticker symbol is valid or not
    result = check_symbol(ticker)
    if not result:
        messages.error(request, 'Invalid stock symbol....')
        return render(request, 'home.html')

    print(ticker)
    print(trading_strategy)

    # fetching data from the yfinance api with the respective start and end date
    _start = dt.date(2020, 1, 1)
    _end = dt.date(2022, 12, 1)
    data = yf.download(ticker, start = _start, end = _end)

    
    if trading_strategy == 'SMA':
        print('Hello')
        # performing backtesting
        backtest_result = Backtest(data, MySMAStrategy, commission=0.002, exclusive_orders=True)
        stats_before = backtest_result.run()
        backtest_result.plot(filename='/home/sedairochak/Algorithmic_Trading_Platform/algorithmic_trading/tradingapp/templates/plot_before.html')
        print(stats_before)
        print("/////////////////////////////////////////////////////////////////////////////")

        # performing optimization and optimizing Equity Final
        stats_after = backtest_result.optimize(n1=range(5, 30, 5),
                    n2=range(10, 70, 5),
                    maximize='Equity Final [$]',
                    constraint=lambda param: param.n1 < param.n2)
        print(stats_after)
        print("-----------------")
        print(stats_after._strategy)
        backtest_result.plot(filename='/home/sedairochak/Algorithmic_Trading_Platform/algorithmic_trading/tradingapp/templates/plot_after.html')
      
      # returning some of the performance metrices in the form of context dictionary
        context = {
            'Before_return' :  stats_before['Return [%]'],
            'After_return': stats_after['Return [%]'],
            'Buy_and_Hold_return': stats_after['Buy & Hold Return [%]'],
            'trading_strategy': trading_strategy,
            'Before_equity_final': stats_before['Equity Final [$]'],
            'After_equity_final': stats_after['Equity Final [$]'],
            'optimized_parameter': stats_after._strategy,
        }

    elif trading_strategy ==  'MACD':
        print('HI')
        # performing backtesting
        backtest_result = Backtest(data, MyMACDStrategy, commission=0.002, exclusive_orders=True)
        stats_before = backtest_result.run()
        backtest_result.plot(filename='/home/sedairochak/Algorithmic_Trading_Platform/algorithmic_trading/tradingapp/templates/plot_before.html')
        print(stats_before)

        # returning some of the performance metrices in the form of context dictionary
        context = {
            'Before_return' :  stats_before['Return [%]'],
            'Buy_and_Hold_return': stats_before['Buy & Hold Return [%]'],
            'trading_strategy': trading_strategy,
            'Before_equity_final': stats_before['Equity Final [$]'],
        }

    elif trading_strategy == 'RSI':
        # performing backtesting
        backtest_result = Backtest(data, RsiOscillator, commission=0.002, exclusive_orders=True)
        stats_before = backtest_result.run()

        # plotting the backtest result in graph
        backtest_result.plot(filename='/home/sedairochak/Algorithmic_Trading_Platform/algorithmic_trading/tradingapp/templates/plot_before.html')
        print(stats_before)
        print("/////////////////////////////////////////////////////////////////////////////")

        # performing optimization and optimizing Equity Final
        stats_after = backtest_result.optimize(
            upper_bound = range(55, 85, 5),
            lower_bound = range(10, 85, 5),
            rsi_window = range(10,30,2),
            maximize = 'Equity Final [$]',
            constraint = lambda param: param.lower_bound < param.upper_bound
        )
        print(stats_after)
        print("-----------------")
        print(stats_after._strategy.upper_bound)

        #plotting the optimized result in graph
        backtest_result.plot(filename='/home/sedairochak/Algorithmic_Trading_Platform/algorithmic_trading/tradingapp/templates/plot_after.html')
        
        # returning some of the performance metrices in the form of context dictionary
        context = {
            'Before_return' :  stats_before['Return [%]'],
            'After_return': stats_after['Return [%]'],
            'Buy_and_Hold_return': stats_after['Buy & Hold Return [%]'],
            'trading_strategy': trading_strategy,
            'Before_equity_final': stats_before['Equity Final [$]'],
            'After_equity_final': stats_after['Equity Final [$]'],
            'optimized_parameter': stats_after._strategy,
        }

    return render(request, 'home.html', context)
