import data_download as dd
import data_plotting as dplt
import matplotlib.pyplot as plt


def main():
    """
    Основная функция программы. Запрашивает у пользователя параметры анализа,
    загружает данные, рассчитывает индикаторы, строит графики и сохраняет результаты.
    """
    print("Добро пожаловать в инструмент получения и построения графиков биржевых данных.")
    print("Вот несколько примеров биржевых тикеров, которые вы можете рассмотреть: AAPL (Apple Inc), GOOGL (Alphabet Inc), MSFT (Microsoft Corporation), AMZN (Amazon.com Inc), TSLA (Tesla Inc).")
    print("Общие периоды времени для данных о запасах включают: 1д, 5д, 1мес, 3мес, 6мес, 1г, 2г, 5г, 10л, с начала года, макс.")
    print("Вы также можете указать конкретные даты начала и окончания для анализа в формате YYYY-MM-DD.")
    print("Доступные стили графиков: ", plt.style.available)

    ticker = input("Введите тикер акции (например, «AAPL» для Apple Inc): ")
    
    use_custom_dates = input("Хотите указать конкретные даты начала и окончания? (y/n): ").strip().lower()

    if use_custom_dates == 'y':
        start_date = input("Введите дату начала в формате YYYY-MM-DD: ").strip()
        end_date = input("Введите дату окончания в формате YYYY-MM-DD: ").strip()
        period = None  # Не используется при наличии конкретных дат
    else:
        period = input("Введите период для данных (например, '1mo' для одного месяца): ")
        start_date = None
        end_date = None

    # Fetch stock data
    stock_data = dd.fetch_stock_data(ticker, period, start_date, end_date)

    if stock_data.empty:
        print("Не удалось получить данные о ценах на акции.")
        return

    # Add moving average to the data
    stock_data = dd.add_moving_average(stock_data)

    # Calculate and display the average closing price
    dd.calculate_and_display_average_price(stock_data)

    # Notify if there are strong fluctuations
    try:
        threshold = float(input("Введите пороговое значение процента изменения цены (например, 5 для 5%): "))
    except ValueError:
        print("Некорректный ввод. Будет использовано значение по умолчанию 5%.")
        threshold = 5

    dd.notify_if_strong_fluctuations(stock_data, threshold)

    # Export data to CSV
    csv_filename = f"{ticker}_{period if period else f'{start_date}_{end_date}'}_stock_data.csv"
    dd.export_data_to_csv(stock_data, csv_filename)

    # Add technical indicators
    stock_data = dd.add_rsi(stock_data)
    stock_data = dd.add_macd(stock_data)

    # Choose a style for the plot
    available_styles = plt.style.available
    print(f"Доступные стили: {available_styles}")
    chosen_style = input("Выберите стиль графика: ").strip()
    if chosen_style not in available_styles:
        print(f"Стиль '{chosen_style}' не поддерживается. Будет использован стиль по умолчанию 'default'.")
        chosen_style = 'default'

    # Plot the data with technical indicators
    dplt.create_and_save_plot(stock_data, ticker, period if period else f'{start_date}_{end_date}', chosen_style)


if __name__ == "__main__":
    main()