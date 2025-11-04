#!/usr/bin/env python3
"""
Главный скрипт для анализа акций
"""
import argparse
import os
import sys
from datetime import datetime
import pandas as pd
from dotenv import load_dotenv

from src.data_fetcher import StockDataFetcher
from src.sheets_integration import GoogleSheetsIntegration
from src.analyzer import StockAnalyzer
from src.visualizer import StockVisualizer


def print_banner():
    """Вывести баннер приложения"""
    banner = """
    ╔═══════════════════════════════════════════════════════════╗
    ║         СИСТЕМА АНАЛИЗА АКЦИЙ                             ║
    ║         Stock Analysis System v1.0                        ║
    ╚═══════════════════════════════════════════════════════════╝
    """
    print(banner)


def analyze_single_stock(ticker: str, period: str = '1y', visualize: bool = True):
    """
    Анализ одной акции

    Args:
        ticker: Тикер акции
        period: Период анализа
        visualize: Создавать ли графики
    """
    print(f"\n{'='*60}")
    print(f"Анализ акции: {ticker}")
    print(f"{'='*60}\n")

    # Получение данных
    fetcher = StockDataFetcher()
    print(f"📊 Загрузка данных для {ticker}...")
    data = fetcher.get_stock_data(ticker, period)

    if data is None or data.empty:
        print(f"❌ Не удалось получить данные для {ticker}")
        return None

    print(f"✅ Загружено {len(data)} записей")

    # Получение информации о компании
    info = fetcher.get_stock_info(ticker)
    if info:
        print(f"\n📈 Информация о компании:")
        print(f"   Название: {info['name']}")
        print(f"   Сектор: {info['sector']}")
        print(f"   Индустрия: {info['industry']}")
        print(f"   Рыночная капитализация: ${info['market_cap']:,.0f}")
        print(f"   P/E Ratio: {info['pe_ratio']}")
        print(f"   Дивидендная доходность: {info['dividend_yield']}")
        print(f"   Текущая цена: ${info['current_price']:.2f}")
        print(f"   Целевая цена: ${info['target_price']:.2f}" if info['target_price'] else "")
        print(f"   Рекомендация: {info['recommendation'].upper()}")

    # Анализ
    print(f"\n🔍 Проведение технического анализа...")
    analyzer = StockAnalyzer(data)
    analysis = analyzer.get_summary()

    # Вывод результатов анализа
    print(f"\n{'='*60}")
    print(f"РЕЗУЛЬТАТЫ АНАЛИЗА")
    print(f"{'='*60}")

    # Тренд
    trend = analysis['trend']
    print(f"\n📊 ТРЕНД:")
    print(f"   Текущая цена: ${trend['current_price']:.2f}")
    print(f"   SMA 20: ${trend['sma_20']:.2f}")
    print(f"   SMA 50: ${trend['sma_50']:.2f}")
    print(f"   SMA 200: ${trend['sma_200']:.2f}")
    print(f"   Краткосрочный тренд: {trend['short_term_trend']}")
    print(f"   Долгосрочный тренд: {trend['long_term_trend']}")

    # Моментум
    momentum = analysis['momentum']
    print(f"\n⚡ МОМЕНТУМ:")
    print(f"   RSI: {momentum['rsi']:.2f} - {momentum['rsi_signal']}")
    print(f"   MACD: {momentum['macd']:.2f}")
    print(f"   MACD Signal: {momentum['macd_signal']}")
    print(f"   Stochastic: {momentum['stoch_k']:.2f} - {momentum['stoch_signal']}")

    # Волатильность
    volatility = analysis['volatility']
    print(f"\n📉 ВОЛАТИЛЬНОСТЬ:")
    print(f"   Историческая волатильность: {volatility['historical_volatility']:.2f}%")
    print(f"   ATR: {volatility['atr']:.2f}")
    print(f"   Bollinger Bands: {volatility['bb_position']}")
    print(f"   BB Upper: ${volatility['bb_upper']:.2f}")
    print(f"   BB Lower: ${volatility['bb_lower']:.2f}")

    # Сигналы
    signals = analysis['signals']
    print(f"\n🎯 ТОРГОВЫЕ СИГНАЛЫ:")
    print(f"   Рекомендация: {signals['recommendation']}")
    print(f"   Уверенность: {signals['confidence']}")

    # Визуализация
    if visualize:
        print(f"\n📊 Создание графиков...")
        visualizer = StockVisualizer()

        # Добавляем индикаторы к данным
        data_with_indicators = analyzer.data

        # Создаем графики
        visualizer.plot_price_and_volume(data_with_indicators, ticker)
        visualizer.plot_technical_indicators(data_with_indicators, ticker)
        visualizer.plot_candlestick(data_with_indicators, ticker)
        visualizer.create_analysis_report(ticker, data_with_indicators, analysis)

        print(f"✅ Графики сохранены в директории 'graphs/'")

    return {
        'ticker': ticker,
        'info': info,
        'analysis': analysis,
        'data': data
    }


def analyze_from_sheet(sheet_id: str, period: str = '1y', visualize: bool = True):
    """
    Анализ акций из Google Sheets

    Args:
        sheet_id: ID Google Sheets таблицы
        period: Период анализа
        visualize: Создавать ли графики
    """
    print(f"\n{'='*60}")
    print(f"Анализ акций из Google Sheets")
    print(f"{'='*60}\n")

    # Подключение к Google Sheets
    sheets = GoogleSheetsIntegration()
    tickers = sheets.get_tickers_from_sheet(sheet_id)

    if not tickers:
        print("❌ Не найдены тикеры в таблице")
        return

    print(f"✅ Найдено {len(tickers)} тикеров: {', '.join(tickers)}\n")

    # Анализ каждой акции
    results = []
    for ticker in tickers:
        result = analyze_single_stock(ticker, period, visualize)
        if result:
            results.append(result)

    # Создание сводного отчета
    if results:
        print(f"\n{'='*60}")
        print(f"СВОДНЫЙ ОТЧЕТ")
        print(f"{'='*60}\n")

        summary_data = []
        for result in results:
            signals = result['analysis']['signals']
            trend = result['analysis']['trend']
            momentum = result['analysis']['momentum']

            summary_data.append({
                'Тикер': result['ticker'],
                'Цена': f"${trend['current_price']:.2f}",
                'Тренд': trend['short_term_trend'],
                'RSI': f"{momentum['rsi']:.2f}",
                'Рекомендация': signals['recommendation'],
                'Уверенность': signals['confidence']
            })

        summary_df = pd.DataFrame(summary_data)
        print(summary_df.to_string(index=False))

        # Сохранение результатов обратно в Google Sheets
        try:
            sheets.write_analysis_results(sheet_id, summary_df)
        except Exception as e:
            print(f"⚠️  Не удалось записать результаты в Google Sheets: {e}")

        # Создание сравнительного графика
        if visualize and len(results) > 1:
            print(f"\n📊 Создание сравнительного графика...")
            visualizer = StockVisualizer()
            data_dict = {r['ticker']: r['data'] for r in results}
            visualizer.plot_comparison(data_dict)


def main():
    """Главная функция"""
    load_dotenv()

    parser = argparse.ArgumentParser(
        description='Система анализа акций',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Примеры использования:

  # Анализ одной акции
  python main.py --ticker AAPL

  # Анализ с периодом 6 месяцев
  python main.py --ticker GOOGL --period 6mo

  # Анализ из Google Sheets
  python main.py --sheet YOUR_SHEET_ID

  # Анализ нескольких акций
  python main.py --tickers AAPL GOOGL MSFT TSLA

  # Без создания графиков (только анализ)
  python main.py --ticker AAPL --no-visualize

Периоды: 1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max
        """
    )

    parser.add_argument('--ticker', type=str, help='Тикер акции для анализа')
    parser.add_argument('--tickers', nargs='+', help='Несколько тикеров для анализа')
    parser.add_argument('--sheet', type=str, help='ID Google Sheets таблицы')
    parser.add_argument('--period', type=str, default='1y', help='Период анализа (по умолчанию: 1y)')
    parser.add_argument('--no-visualize', action='store_true', help='Не создавать графики')

    args = parser.parse_args()

    print_banner()

    # Проверка аргументов
    if not (args.ticker or args.tickers or args.sheet):
        parser.print_help()
        sys.exit(1)

    visualize = not args.no_visualize

    # Анализ
    if args.sheet:
        analyze_from_sheet(args.sheet, args.period, visualize)
    elif args.tickers:
        for ticker in args.tickers:
            analyze_single_stock(ticker.upper(), args.period, visualize)
    elif args.ticker:
        analyze_single_stock(args.ticker.upper(), args.period, visualize)

    print(f"\n{'='*60}")
    print(f"✅ Анализ завершен!")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
