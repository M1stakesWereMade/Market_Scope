import matplotlib.pyplot as plt
import pandas as pd

def create_and_save_plot(data, ticker, period, style='default', filename=None):
    """
    Создает график и сохраняет его в файл.
    
    Параметры:
    data (DataFrame): DataFrame с данными о ценах на акции.
    ticker (str): Тикер акции (например, 'AAPL').
    period (str): Период анализа данных.
    style (str, optional): Стиль графика из доступных стилей matplotlib.
    filename (str, optional): Имя файла для сохранения графика.
    """
    plt.style.use(style)  # Apply the chosen style to the plot
    
    fig, axs = plt.subplots(3, 1, figsize=(10, 12))

    if 'Date' not in data:
        if pd.api.types.is_datetime64_any_dtype(data.index):
            dates = data.index.to_numpy()
            axs[0].plot(dates, data['Close'].values, label='Close Price')
            axs[0].plot(dates, data['Moving_Average'].values, label='Moving Average')
            if 'MACD' in data.columns:
                axs[1].plot(dates, data['MACD'], label='MACD')
                axs[1].plot(dates, data['Signal_Line'], label='Signal Line')
                axs[1].bar(dates, data['MACD_Histogram'], label='MACD Histogram', color='gray')
            if 'RSI' in data.columns:
                axs[2].plot(dates, data['RSI'], label='RSI')
                axs[2].axhline(70, linestyle='--', alpha=0.7, color='r')
                axs[2].axhline(30, linestyle='--', alpha=0.7, color='g')
        else:
            print("Информация о дате отсутствует или не имеет распознаваемого формата.")
            return
    else:
        if not pd.api.types.is_datetime64_any_dtype(data['Date']):
            data['Date'] = pd.to_datetime(data['Date'])
        axs[0].plot(data['Date'], data['Close'], label='Close Price')
        axs[0].plot(data['Date'], data['Moving_Average'], label='Moving Average')
        if 'MACD' in data.columns:
            axs[1].plot(data['Date'], data['MACD'], label='MACD')
            axs[1].plot(data['Date'], data['Signal_Line'], label='Signal Line')
            axs[1].bar(data['Date'], data['MACD_Histogram'], label='MACD Histogram', color='gray')
        if 'RSI' in data.columns:
            axs[2].plot(data['Date'], data['RSI'], label='RSI')
            axs[2].axhline(70, linestyle='--', alpha=0.7, color='r')
            axs[2].axhline(30, linestyle='--', alpha=0.7, color='g')

    axs[0].set_title(f"{ticker} Цена акций с течением времени")
    axs[0].set_xlabel("Дата")
    axs[0].set_ylabel("Цена")
    axs[0].legend()

    if 'MACD' in data.columns:
        axs[1].set_title(f"{ticker} MACD и Signal Line")
        axs[1].set_xlabel("Дата")
        axs[1].set_ylabel("Значение")
        axs[1].legend()

    if 'RSI' in data.columns:
        axs[2].set_title(f"{ticker} RSI")
        axs[2].set_xlabel("Дата")
        axs[2].set_ylabel("Значение")
        axs[2].legend()

    if filename is None:
        filename = f"{ticker}_{period}_stock_price_chart.png"

    plt.tight_layout()
    plt.savefig(filename)
    print(f"График сохранен как {filename}")