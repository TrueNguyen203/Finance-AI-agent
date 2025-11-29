from langchain.tools import tool
import pandas as pd
import numpy as np
from io import StringIO

def df_from_string(df_string: str) -> pd.DataFrame:
    # Loại bỏ khoảng trắng dư thừa đầu dòng
    df_string = df_string.strip()
    
    # Đọc từ chuỗi bằng read_csv với delimiter là khoảng trắng
    df = pd.read_csv(StringIO(df_string), sep=r"\s+", engine="python")
    return df[:-1] # Loại bỏ dòng cuối cùng nếu nó rỗng hoặc không cần thiết


@tool
def calculating_simple_moving_average(data: str, SMA_window: int) -> str:
    """Calculate the simple moving average (SMA) of a stock and return a string Object.
    Args:
        data: historical price data of a stock as a string taken from tool 'search_company_historical_price'
        SMA_window: the time lags behind the orginal stock
    """
    data = df_from_string(data)
    retrived_data = data
    retrived_data[f'SMA{SMA_window}'] = retrived_data['close'].rolling(window=SMA_window).mean()
    return str(retrived_data)

@tool
def calculating_relative_strength_index(data: str, RSI_window: int) -> str:
    """Calculate the Relative Strength Index (RSI) of a stock and return a string Object.
    Args:
        data: historical price data of a stock as a string taken from tool 'search_company_historical_price'
        RSI_window: the time lags behind the orginal stock
    """
    data = df_from_string(data)
    retrived_data = data
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


@tool
def calculating_moving_average_convergence_divergence(data: str, short_span: int = 12, long_span: int = 26, signal_span: int = 9) -> str:
    """Calculate the Moving Average Convergence Divergence (MACD) of a stock and return a string Object.
    Args:
        data: historical price data of a stock as a string taken from tool 'search_company_historical_price'
        short_span: the short time lags behind the orginal stock (default is 12)
        long_span: the long time lags behind the orginal stock (default is 26)
        signal_span: the signal time lags behind the orginal stock (default is 9)
    """
    data = df_from_string(data)
    # EMA short
    ema_short = data["close"].ewm(span=short_span, adjust=False).mean()
    # EMA long
    ema_long = data["close"].ewm(span=long_span, adjust=False).mean()

    # MACD line
    macd_line = ema_short - ema_long

    # Signal line (EMA 9 của MACD)
    signal_line = macd_line.ewm(span=signal_span, adjust=False).mean()

    # Histogram
    histogram = macd_line - signal_line

    # Trả về DataFrame
    return str({
        "MACD": macd_line,
        "Signal": signal_line,
        "Histogram": histogram
    })