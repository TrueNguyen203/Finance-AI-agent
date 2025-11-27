from langchain.tools import tool
from vnstock import Company
from vnstock import Quote
import pandas as pd
import numpy as np


@tool
def search_company_overview(ticker: str) -> str:
    """Search for company information and return a string object.
    Args:
        ticker: Stock ticker symbol 
    """
    company = Company(symbol=ticker, source='VCI')
    overview = company.overview()
    return str(overview)


@tool
def search_company_shareholders(ticker: str) -> str:
    """Search for company shareholders and return a string object.
    Args:
        ticker: Stock ticker symbol 
    """
    company = Company(symbol=ticker, source='VCI')
    shareholders = company.shareholders()
    return str(shareholders)


@tool
def search_company_officers(ticker: str) -> str:
    """Search for company officers and return a string object.
    Args:
        ticker: Stock ticker symbol 
    """
    company = Company(symbol=ticker, source='VCI')
    officers = company.officers(filter_by='working')
    return str(officers)


@tool
def search_company_subsidaries(ticker: str) -> str:
    """Search for company subsidaries and return a string Object.
    Args:
        ticker: Stock ticker symbol 
    """
    company = Company(symbol=ticker, source='VCI')
    subsidiaries = company.subsidiaries()
    return str(subsidiaries)


@tool
def search_company_subsidaries(ticker: str) -> str:
    """Search for company subsidaries and return a string Object.
    Args:
        ticker: Stock ticker symbol 
    """
    company = Company(symbol=ticker, source='VCI')
    subsidiaries = company.subsidiaries()
    return str(subsidiaries)

@tool
def search_company_historical_price(ticker: str, start_day: str, end_day: str, interval) -> str:
    """Search for a company stock historical open, high, low, close price and volumne (OHLCV) and return a string Object.
    Args:
        ticker: Stock ticker symbol
        start_day: start day for historical price with the format %Y-%m-%d
        end_day: end day for historical price with the format %Y-%m-%d
        interval: timeframe for historical price
    """
    quote = Quote(symbol=ticker, source='VCI')
    historical_price = quote.history(start=start_day, end=end_day, interval=interval)
    return f"Lịch sử của mã {ticker}:\n" + str(historical_price)


@tool
def calculating_simple_moving_average(ticker: str, start_day: str, end_day: str, interval: str, SMA_window: int) -> str:
    """Retrieve the comanpy stock historical price then calculate the simple moving average (SMA) of a stock and return a string Object.
    Args:
        ticker: Stock ticker symbol
        start_day: start day for historical price with the format %Y-%m-%d
        end_day: end day for historical price with the format %Y-%m-%d
        interval: timeframe for historical price
        RSI_window: the time lags behind the orginal stock
    """
    quote = Quote(symbol=ticker, source='VCI')
    retrived_data = quote.history(start=start_day, end=end_day, interval=interval)
    retrived_data[f'SMA{SMA_window}'] = retrived_data['close'].rolling(window=SMA_window).mean()
    return str(retrived_data)

@tool
def calculating_relative_strength_index(ticker: str, start_day: str, end_day: str, interval: str, RSI_window: int) -> str:
    """Retrieve the comanpy stock historical price then calculate the Relative Strength Index (RSI) of a stock and return a string Object.
    Args:
        ticker: Stock ticker symbol
        start_day: start day for historical price with the format %Y-%m-%d
        end_day: end day for historical price with the format %Y-%m-%d
        interval: timeframe for historical price
        RSI_window: the time lags behind the orginal stock
    """
    quote = Quote(symbol=ticker, source='VCI')
    retrived_data = quote.history(start=start_day, end=end_day, interval=interval)
    # 1. Tính thay đổi giá
    delta = retrived_data['close'].diff()

    # 2. Gain và Loss
    gain = np.where(delta > 0, delta, 0)
    loss = np.where(delta < 0, -delta, 0)

    # 3. SMA gain và SMA loss
    avg_gain = pd.Series(gain).rolling(window=RSI_window).mean()
    avg_loss = pd.Series(loss).rolling(window=RSI_window).mean()

    # 4. Tính RS & RSI
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    retrived_data[f'RSI{RSI_window}'] = pd.Series(rsi)
    return str(retrived_data)
