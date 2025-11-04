#!/usr/bin/env python3
"""
Пример использования системы анализа акций
Простой скрипт для быстрого старта
"""

from src.data_fetcher import StockDataFetcher
from src.analyzer import StockAnalyzer
from src.visualizer import StockVisualizer


def quick_analysis_example():
    """Пример быстрого анализа акции"""

    print("=" * 60)
    print("ПРИМЕР АНАЛИЗА АКЦИИ")
    print("=" * 60)

    # 1. Получение данных
    ticker = "AAPL"
    print(f"\n1. Получаем данные для {ticker}...")

    fetcher = StockDataFetcher()
    data = fetcher.get_stock_data(ticker, period="1y")

    if data is None:
        print("Ошибка получения данных")
        return

    print(f"   ✅ Получено {len(data)} записей")
    print(f"   Период: {data.index[0].date()} - {data.index[-1].date()}")
    print(f"   Текущая цена: ${data['Close'].iloc[-1]:.2f}")

    # 2. Получение информации о компании
    print(f"\n2. Получаем информацию о компании...")
    info = fetcher.get_stock_info(ticker)

    if info:
        print(f"   Название: {info['name']}")
        print(f"   Сектор: {info['sector']}")
        print(f"   P/E Ratio: {info['pe_ratio']}")
        print(f"   Рыночная кап.: ${info['market_cap']:,.0f}")

    # 3. Технический анализ
    print(f"\n3. Проводим технический анализ...")

    analyzer = StockAnalyzer(data)
    analysis = analyzer.get_summary()

    # Выводим результаты
    print("\n" + "=" * 60)
    print("РЕЗУЛЬТАТЫ АНАЛИЗА")
    print("=" * 60)

    # Тренд
    trend = analysis['trend']
    print(f"\nТРЕНД:")
    print(f"  • Краткосрочный: {trend['short_term_trend']}")
    print(f"  • Долгосрочный: {trend['long_term_trend']}")
    print(f"  • SMA 20: ${trend['sma_20']:.2f}")
    print(f"  • SMA 50: ${trend['sma_50']:.2f}")

    # Моментум
    momentum = analysis['momentum']
    print(f"\nМОМЕНТУМ:")
    print(f"  • RSI: {momentum['rsi']:.2f} ({momentum['rsi_signal']})")
    print(f"  • MACD: {momentum['macd_signal']}")
    print(f"  • Stochastic: {momentum['stoch_signal']}")

    # Волатильность
    volatility = analysis['volatility']
    print(f"\nВОЛАТИЛЬНОСТЬ:")
    print(f"  • Годовая: {volatility['historical_volatility']:.2f}%")
    print(f"  • Bollinger Bands: {volatility['bb_position']}")

    # Сигналы
    signals = analysis['signals']
    print(f"\nТОРГОВЫЕ СИГНАЛЫ:")
    print(f"  • Рекомендация: {signals['recommendation']}")
    print(f"  • Уверенность: {signals['confidence']}")

    # 4. Создание графиков
    print(f"\n4. Создаем графики...")

    visualizer = StockVisualizer()
    data_with_indicators = analyzer.data

    # Создаем все виды графиков
    visualizer.plot_price_and_volume(data_with_indicators, ticker)
    visualizer.plot_technical_indicators(data_with_indicators, ticker)
    visualizer.plot_candlestick(data_with_indicators, ticker)
    visualizer.create_analysis_report(ticker, data_with_indicators, analysis)

    print(f"\n   ✅ Графики сохранены в папке 'graphs/':")
    print(f"      • {ticker}_price_volume.png")
    print(f"      • {ticker}_technical.png")
    print(f"      • {ticker}_candlestick.html (интерактивный)")
    print(f"      • {ticker}_report.png")

    print("\n" + "=" * 60)
    print("АНАЛИЗ ЗАВЕРШЕН!")
    print("=" * 60)


def compare_stocks_example():
    """Пример сравнения нескольких акций"""

    print("\n" + "=" * 60)
    print("ПРИМЕР СРАВНЕНИЯ АКЦИЙ")
    print("=" * 60)

    tickers = ["AAPL", "GOOGL", "MSFT"]
    print(f"\nСравниваем: {', '.join(tickers)}")

    fetcher = StockDataFetcher()
    data_dict = fetcher.get_multiple_stocks(tickers, period="6mo")

    print(f"✅ Загружены данные для {len(data_dict)} акций")

    # Анализ каждой акции
    results = []
    for ticker, data in data_dict.items():
        analyzer = StockAnalyzer(data)
        analysis = analyzer.get_summary()
        results.append({
            'ticker': ticker,
            'price': analysis['trend']['current_price'],
            'trend': analysis['trend']['short_term_trend'],
            'rsi': analysis['momentum']['rsi'],
            'recommendation': analysis['signals']['recommendation']
        })

    # Вывод сводки
    print("\nСводная таблица:")
    print("-" * 60)
    print(f"{'Тикер':<10} {'Цена':<12} {'Тренд':<15} {'RSI':<8} {'Сигнал':<12}")
    print("-" * 60)

    for r in results:
        print(f"{r['ticker']:<10} ${r['price']:<11.2f} {r['trend']:<15} "
              f"{r['rsi']:<8.2f} {r['recommendation']:<12}")

    print("-" * 60)

    # Создание сравнительного графика
    visualizer = StockVisualizer()
    visualizer.plot_comparison(data_dict)

    print("\n✅ Сравнительный график сохранен: graphs/comparison.png")


if __name__ == '__main__':
    # Запускаем примеры
    quick_analysis_example()

    print("\n\n")

    # Раскомментируйте для сравнения акций
    # compare_stocks_example()
