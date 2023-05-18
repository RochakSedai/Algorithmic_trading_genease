# ALGORITHMIC TRADING PLATFORM WITH BACKTESTING AND OPTIMIZATION
## Introduction
The purpose of this project is to develop an algorithmic trading platform that enables users to create, backtest, and optimize trading strategies. The platform will integrate with market data APIs like <a href="https:/finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC"> YahooFinance </a> , provide comprehensive backtesting capabilities, and offer optimization  strategy refinement. Alse user will come to know how their strategy return will get higher than the buy and hold method. 

<b>P.S:<i>  This is just a simple prototype for the given topic</i></b><br>  


## System Overview
  1.  Market Data Integration: This component will handle the retrieval and processing of historical and real-time market data from market data APIs <a href="https:/finance.yahoo.com/quote/%5EGSPC/history?p=%5EGSPC"> YahooFinance </a>. It will ensure efficient retrieval of data to support strategy backtesting and optimization.

   2. Backtesting and Optimization Engine: This component will provide the necessary backend functionality to support strategy creation, backtesting against historical data, and paramter optimization for the given strategy. It will leverage historical data to simulate the performance of trading strategies and identify optimal parameter settings.

   3. User Interface: The platform will feature a user-friendly web interface that allows users to define trading strategies using a domain-specific language (DSL). Users will be able to run backtests on historical data, analyze performance metrics and risk statistics, and visualize the results.


## How to use this project locally?
You can clone this branch and use it right now using the steps given below.  

### Building Locally
It is best to use python **virtualenv** tool to build locally and use Python 3.10.6 and pip 23.1.2:  
> virtualenv venv  
> source venv/bin/activate  
> git clone https://github.com/RochakSedai/Algorithmic_trading_genease.git

Then you navigate to the base directory of the project and install the requirements in your vitual environment  
> pip install -r requirements.txt  

Yo can get the build error while installing TA-Lib. You can solve this problem by following these steps in ubuntu terminal.
>wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz  \
> tar -xzf ta-lib-0.4.0-src.tar.gz\
> cd ta-lib/ \
>sudo ./configure \
>sudo make\
>sudo make install\
>pip install ta-lib


And finally you make migration to the database, create a super user, and run the server  
> python manage.py makemigrations  
>python manage.py migrate  
> python manage.py createsuperuser  
> python manage.py runserver  



## Developed by:
- Rochak Sedai
