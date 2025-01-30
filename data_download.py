import yfinance as yf
import pandas as pd
import numpy as np

def fetch_stock_data(ticker, period='1mo', start_date=None, end_date=None):
    """
    Загружает данные о ценах на акции с использованием библиотеки yfinance.
    
    Параметры:
    ticker (str): Тикер акции (например, 'AAPL').
    period (str): Период загрузки данных (например, '1mo' для одного месяца).
    start_date (str, optional): Начальная дата в формате 'YYYY-MM-DD'.
    end_date (str, optional): Конечная дата в формате 'YYYY-MM-DD'.
    
    Возвращает:
    DataFrame: Данные о ценах на акции.
    """
    stock = yf.Ticker(ticker)
    
    if start_date and end_date:
        # Если указаны конкретные даты начала и окончания, используем их
        data = stock.history(start=start_date, end=end_date)
    else:
        # Иначе используем стандартный период
        data = stock.history(period=period)
    
    return data

def add_moving_average(data, window_size=5):
    """
    Добавляет скользящее среднее значение цены закрытия в DataFrame.
    
    Параметры:
    data (DataFrame): DataFrame с данными о ценах на акции.
    window_size (int, optional): Размер окна для расчета скользящего среднего значения.
    
    Возвращает:
    DataFrame: DataFrame с добавленным столбцом 'Moving_Average'.
    """
    data['Moving_Average'] = data['Close'].rolling(window=window_size).mean()
    return data

def calculate_and_display_average_price(data):
    """
    Вычисляет и выводит среднюю цену закрытия за заданный период.
    
    Параметры:
    data (DataFrame): DataFrame с данными о ценах на акции.
    """
    if 'Close' not in data.columns:
        print("Колонка 'Close' отсутствует в данных.")
        return
    
    average_price = data['Close'].mean()
    print(f"Средняя цена закрытия за заданный период: {average_price:.2f}")

def notify_if_strong_fluctuations(data, threshold):
    """
    Уведомляет пользователя, если цена акций колебалась более чем на заданный процент за период.
    
    Параметры:
    data (DataFrame): DataFrame с данными о ценах на акции.
    threshold (float): Пороговое значение процента изменения цены.
    """
    if 'Close' not in data.columns or data['Close'].empty:
        print("Колонка 'Close' отсутствует или пуста в данных.")
        return
    
    max_price = data['Close'].max()
    min_price = data['Close'].min()
    
    fluctuation = ((max_price - min_price) / min_price) * 100
    
    if fluctuation > threshold:
        print(f"Обнаружены значительные колебания! Максимальная цена: {max_price:.2f}, минимальная цена: {min_price:.2f}. Процентное изменение: {fluctuation:.2f}%")
    else:
        print("Колебания цены находятся в допустимых пределах.")

def export_data_to_csv(data, filename):
    """
    Экспортирует данные в CSV файл.
    
    Параметры:
    data (DataFrame): DataFrame с данными о ценах на акции.
    filename (str): Имя файла для сохранения данных.
    """
    if data.empty:
        print("Данные пусты. Невозможно экспортировать в CSV.")
        return
    
    try:
        data.to_csv(filename)
        print(f"Данные успешно экспортированы в файл {filename}")
    except Exception as e:
        print(f"Ошибка при экспорте данных в CSV: {e}")

def add_rsi(data, window=14):
    """
    Добавляет индикатор RSI (Relative Strength Index) в DataFrame.
    
    Параметры:
    data (DataFrame): DataFrame с данными о ценах на акции.
    window (int, optional): Размер окна для расчета RSI.
    
    Возвращает:
    DataFrame: DataFrame с добавленным столбцом 'RSI'.
    """
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    data['RSI'] = rsi.fillna(50)  # Handle NaN values for initial periods using direct assignment
    return data

def add_macd(data, short_window=12, long_window=26, signal_window=9):
    """
    Добавляет индикатор MACD (Moving Average Convergence Divergence) в DataFrame.
    
    Параметры:
    data (DataFrame): DataFrame с данными о ценах на акции.
    short_window (int, optional): Размер короткого окна для EMA.
    long_window (int, optional): Размер длинного окна для EMA.
    signal_window (int, optional): Размер окна для сигнальной линии MACD.
    
    Возвращает:
    DataFrame: DataFrame с добавленными столбцами 'MACD', 'Signal_Line' и 'MACD_Histogram'.
    """
    short_ema = data['Close'].ewm(span=short_window, adjust=False).mean()
    long_ema = data['Close'].ewm(span=long_window, adjust=False).mean()
    data['MACD'] = short_ema - long_ema
    data['Signal_Line'] = data['MACD'].ewm(span=signal_window, adjust=False).mean()
    data['MACD_Histogram'] = data['MACD'] - data['Signal_Line']
    return data