"""
Модуль для технического и фундаментального анализа акций
"""
import pandas as pd
import numpy as np
from ta.trend import SMAIndicator, EMAIndicator, MACD
from ta.momentum import RSIIndicator, StochasticOscillator
from ta.volatility import BollingerBands, AverageTrueRange
from ta.volume import OnBalanceVolumeIndicator
from typing import Dict, Any, Optional


class StockAnalyzer:
    """Класс для анализа акций"""

    def __init__(self, data: pd.DataFrame):
        """
        Инициализация анализатора

        Args:
            data: DataFrame с историческими данными (должен содержать OHLCV)
        """
        self.data = data.copy()
        self.signals = {}

    def add_technical_indicators(self) -> pd.DataFrame:
        """
        Добавить технические индикаторы к данным

        Returns:
            DataFrame с добавленными индикаторами
        """
        df = self.data.copy()

        # Простые скользящие средние (SMA)
        df['SMA_20'] = SMAIndicator(close=df['Close'], window=20).sma_indicator()
        df['SMA_50'] = SMAIndicator(close=df['Close'], window=50).sma_indicator()
        df['SMA_200'] = SMAIndicator(close=df['Close'], window=200).sma_indicator()

        # Экспоненциальные скользящие средние (EMA)
        df['EMA_12'] = EMAIndicator(close=df['Close'], window=12).ema_indicator()
        df['EMA_26'] = EMAIndicator(close=df['Close'], window=26).ema_indicator()

        # MACD (Moving Average Convergence Divergence)
        macd = MACD(close=df['Close'])
        df['MACD'] = macd.macd()
        df['MACD_Signal'] = macd.macd_signal()
        df['MACD_Diff'] = macd.macd_diff()

        # RSI (Relative Strength Index)
        df['RSI'] = RSIIndicator(close=df['Close'], window=14).rsi()

        # Bollinger Bands
        bollinger = BollingerBands(close=df['Close'], window=20, window_dev=2)
        df['BB_Upper'] = bollinger.bollinger_hband()
        df['BB_Middle'] = bollinger.bollinger_mavg()
        df['BB_Lower'] = bollinger.bollinger_lband()

        # Stochastic Oscillator
        stoch = StochasticOscillator(
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            window=14,
            smooth_window=3
        )
        df['Stoch_K'] = stoch.stoch()
        df['Stoch_D'] = stoch.stoch_signal()

        # Average True Range (ATR) - волатильность
        df['ATR'] = AverageTrueRange(
            high=df['High'],
            low=df['Low'],
            close=df['Close'],
            window=14
        ).average_true_range()

        # On-Balance Volume
        df['OBV'] = OnBalanceVolumeIndicator(
            close=df['Close'],
            volume=df['Volume']
        ).on_balance_volume()

        # Дневные изменения
        df['Daily_Return'] = df['Close'].pct_change() * 100
        df['Price_Change'] = df['Close'].diff()

        self.data = df
        return df

    def analyze_trend(self) -> Dict[str, Any]:
        """
        Анализ тренда

        Returns:
            Словарь с информацией о тренде
        """
        if 'SMA_20' not in self.data.columns:
            self.add_technical_indicators()

        latest = self.data.iloc[-1]
        prev = self.data.iloc[-2]

        trend_info = {
            'current_price': latest['Close'],
            'sma_20': latest['SMA_20'],
            'sma_50': latest['SMA_50'],
            'sma_200': latest['SMA_200'],
        }

        # Определение тренда
        if latest['Close'] > latest['SMA_20'] > latest['SMA_50']:
            trend_info['short_term_trend'] = 'Восходящий'
        elif latest['Close'] < latest['SMA_20'] < latest['SMA_50']:
            trend_info['short_term_trend'] = 'Нисходящий'
        else:
            trend_info['short_term_trend'] = 'Боковой'

        if latest['SMA_50'] > latest['SMA_200']:
            trend_info['long_term_trend'] = 'Восходящий (Golden Cross)'
        elif latest['SMA_50'] < latest['SMA_200']:
            trend_info['long_term_trend'] = 'Нисходящий (Death Cross)'
        else:
            trend_info['long_term_trend'] = 'Нейтральный'

        return trend_info

    def analyze_momentum(self) -> Dict[str, Any]:
        """
        Анализ моментума

        Returns:
            Словарь с информацией о моментуме
        """
        if 'RSI' not in self.data.columns:
            self.add_technical_indicators()

        latest = self.data.iloc[-1]

        momentum_info = {
            'rsi': latest['RSI'],
            'macd': latest['MACD'],
            'macd_signal': latest['MACD_Signal'],
            'stoch_k': latest['Stoch_K'],
            'stoch_d': latest['Stoch_D'],
        }

        # RSI сигналы
        if latest['RSI'] > 70:
            momentum_info['rsi_signal'] = 'Перекупленность'
        elif latest['RSI'] < 30:
            momentum_info['rsi_signal'] = 'Перепроданность'
        else:
            momentum_info['rsi_signal'] = 'Нейтрально'

        # MACD сигналы
        if latest['MACD'] > latest['MACD_Signal']:
            momentum_info['macd_signal'] = 'Бычий'
        else:
            momentum_info['macd_signal'] = 'Медвежий'

        # Stochastic сигналы
        if latest['Stoch_K'] > 80:
            momentum_info['stoch_signal'] = 'Перекупленность'
        elif latest['Stoch_K'] < 20:
            momentum_info['stoch_signal'] = 'Перепроданность'
        else:
            momentum_info['stoch_signal'] = 'Нейтрально'

        return momentum_info

    def analyze_volatility(self) -> Dict[str, Any]:
        """
        Анализ волатильности

        Returns:
            Словарь с информацией о волатильности
        """
        if 'BB_Upper' not in self.data.columns:
            self.add_technical_indicators()

        latest = self.data.iloc[-1]

        # Расчет исторической волатильности
        returns = self.data['Close'].pct_change().dropna()
        historical_volatility = returns.std() * np.sqrt(252) * 100  # Годовая волатильность

        volatility_info = {
            'current_price': latest['Close'],
            'bb_upper': latest['BB_Upper'],
            'bb_middle': latest['BB_Middle'],
            'bb_lower': latest['BB_Lower'],
            'atr': latest['ATR'],
            'historical_volatility': historical_volatility,
        }

        # Позиция цены относительно Bollinger Bands
        if latest['Close'] > latest['BB_Upper']:
            volatility_info['bb_position'] = 'Выше верхней полосы (перекупленность)'
        elif latest['Close'] < latest['BB_Lower']:
            volatility_info['bb_position'] = 'Ниже нижней полосы (перепроданность)'
        else:
            volatility_info['bb_position'] = 'В пределах полос'

        return volatility_info

    def generate_signals(self) -> Dict[str, str]:
        """
        Генерация торговых сигналов

        Returns:
            Словарь с сигналами
        """
        trend = self.analyze_trend()
        momentum = self.analyze_momentum()
        volatility = self.analyze_volatility()

        signals = {
            'trend': trend['short_term_trend'],
            'momentum': momentum['rsi_signal'],
            'macd': momentum['macd_signal'],
            'volatility': volatility['bb_position'],
        }

        # Общая рекомендация
        buy_signals = 0
        sell_signals = 0

        if trend['short_term_trend'] == 'Восходящий':
            buy_signals += 1
        elif trend['short_term_trend'] == 'Нисходящий':
            sell_signals += 1

        if momentum['rsi_signal'] == 'Перепроданность':
            buy_signals += 1
        elif momentum['rsi_signal'] == 'Перекупленность':
            sell_signals += 1

        if momentum['macd_signal'] == 'Бычий':
            buy_signals += 1
        else:
            sell_signals += 1

        if buy_signals > sell_signals:
            signals['recommendation'] = 'ПОКУПАТЬ'
        elif sell_signals > buy_signals:
            signals['recommendation'] = 'ПРОДАВАТЬ'
        else:
            signals['recommendation'] = 'ДЕРЖАТЬ'

        signals['confidence'] = f"{max(buy_signals, sell_signals)}/3"

        self.signals = signals
        return signals

    def get_summary(self) -> Dict[str, Any]:
        """
        Получить полный анализ

        Returns:
            Словарь с полным анализом
        """
        self.add_technical_indicators()

        return {
            'trend': self.analyze_trend(),
            'momentum': self.analyze_momentum(),
            'volatility': self.analyze_volatility(),
            'signals': self.generate_signals(),
            'latest_data': self.data.iloc[-1].to_dict()
        }
