import yfinance as y_fin

def get_stock(stock_symbol: str):
    stock_ticker_data = y_fin.Ticker(stock_symbol)
    stock_data = stock_ticker_data.info
    return stock_data

def check_symbol(stock_symbol: str):
    try: 
        stock_data = get_stock(stock_symbol)
        price = stock_data['currentPrice']
        return True
    except:
        return False 
    

    