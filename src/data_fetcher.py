"""
Модуль для получения данных об акциях из Yahoo Finance API
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
from typing import Optional, Dict, Any


class StockDataFetcher:
    """Класс для получения данных об акциях"""

    def __init__(self):
        self.cache = {}

    def get_stock_data(self, ticker: str, period: str = "1y") -> Optional[pd.DataFrame]:
        """
        Получить исторические данные акции

        Args:
            ticker: Тикер акции (например, 'AAPL', 'GOOGL')
            period: Период данных ('1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y', '10y', 'ytd', 'max')

        Returns:
            DataFrame с историческими данными или None
        """
        try:
            stock = yf.Ticker(ticker)
            df = stock.history(period=period)

            if df.empty:
                print(f"⚠️  Данные для {ticker} не найдены")
                return None

            return df
        except Exception as e:
            print(f"❌ Ошибка при получении данных для {ticker}: {e}")
            return None

    def get_stock_info(self, ticker: str) -> Optional[Dict[str, Any]]:
        """
        Получить информацию о компании

        Args:
            ticker: Тикер акции

        Returns:
            Словарь с информацией о компании
        """
        try:
            stock = yf.Ticker(ticker)
            info = stock.info

            # Извлекаем ключевые метрики
            key_metrics = {
                'symbol': info.get('symbol', ticker),
                'name': info.get('longName', 'N/A'),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A'),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', None),
                'forward_pe': info.get('forwardPE', None),
                'dividend_yield': info.get('dividendYield', None),
                'beta': info.get('beta', None),
                '52_week_high': info.get('fiftyTwoWeekHigh', None),
                '52_week_low': info.get('fiftyTwoWeekLow', None),
                'current_price': info.get('currentPrice', None),
                'target_price': info.get('targetMeanPrice', None),
                'recommendation': info.get('recommendationKey', 'N/A'),
            }

            return key_metrics
        except Exception as e:
            print(f"❌ Ошибка при получении информации для {ticker}: {e}")
            return None

    def get_multiple_stocks(self, tickers: list, period: str = "1y") -> Dict[str, pd.DataFrame]:
        """
        Получить данные для нескольких акций

        Args:
            tickers: Список тикеров
            period: Период данных

        Returns:
            Словарь {ticker: DataFrame}
        """
        result = {}
        for ticker in tickers:
            data = self.get_stock_data(ticker, period)
            if data is not None:
                result[ticker] = data

        return result

    def get_realtime_price(self, ticker: str) -> Optional[float]:
        """
        Получить текущую цену акции

        Args:
            ticker: Тикер акции

        Returns:
            Текущая цена или None
        """
        try:
            stock = yf.Ticker(ticker)
            data = stock.history(period="1d")
            if not data.empty:
                return data['Close'].iloc[-1]
            return None
        except Exception as e:
            print(f"❌ Ошибка при получении цены для {ticker}: {e}")
            return None
