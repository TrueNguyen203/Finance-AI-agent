from langchain.tools import tool
from vnstock import Company
from vnstock import Quote
import pandas as pd

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
    return str(historical_price)

