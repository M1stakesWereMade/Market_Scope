# MarketScope

MarketScope — это инструмент для анализа данных о ценах на акции, который позволяет загружать исторические данные, рассчитывать технические индикаторы, строить графики и экспортировать данные в CSV формат.

## Описание проекта

MarketScope предоставляет следующие возможности:
- Загрузка исторических данных о ценах на акции через библиотеку yfinance.
- Расчет и отображение скользящего среднего значения.
- Вычисление и вывод средней цены закрытия за заданный период.
- Уведомление пользователя о значительных колебаниях цен на акции.
- Экспорт данных в CSV файл.
- Расчет и отображение технических индикаторов RSI и MACD.
- Построение графиков с возможностью выбора стиля оформления.

## Установка

### Требования

- Python 3.x
- Библиотеки: `yfinance`, `pandas`, `numpy`, `matplotlib`

### Установка зависимостей

Для установки необходимых библиотек используйте следующую команду:

```bash
pip install -r requirements.txt
```
## Использование
Запустите основной скрипт **`[main.py](main.py)`**:
```python
python main.py
```

Следуйте инструкциям в консоли:
1. Введите тикер акции (например, 'AAPL' для Apple Inc).
2. Укажите период или конкретные даты начала и окончания для анализа.
3. Выберите пороговое значение процента изменения цены для уведомлений о сильных колебаниях.
4. Выберите стиль оформления графика из доступных стилей matplotlib.

Программа выполнит анализ данных, построит графики и сохранит результаты в CSV файл.

## Пример использования
Ввод данных
```bash
Введите тикер акции (например, «AAPL» для Apple Inc): AAPL
Хотите указать конкретные даты начала и окончания? (y/n): n
Введите период для данных (например, '1mo' для одного месяца): 6mo
Введите пороговое значение процента изменения цены (например, 5 для 5%): 10
Выберите стиль графика: ggplot
```

### Результат

Программа выведет среднюю цену закрытия, проверит наличие значительных колебаний, построит график и сохранит данные в CSV файл.
