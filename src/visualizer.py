"""
Модуль для визуализации данных об акциях
"""
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from datetime import datetime


class StockVisualizer:
    """Класс для создания графиков"""

    def __init__(self, output_dir: str = 'graphs'):
        """
        Инициализация визуализатора

        Args:
            output_dir: Директория для сохранения графиков
        """
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # Настройка стиля
        sns.set_style("whitegrid")
        plt.rcParams['figure.figsize'] = (14, 8)

    def plot_price_and_volume(self, data: pd.DataFrame, ticker: str, save: bool = True):
        """
        График цены и объема торгов

        Args:
            data: DataFrame с данными
            ticker: Тикер акции
            save: Сохранить график
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10),
                                        gridspec_kw={'height_ratios': [3, 1]})

        # График цены
        ax1.plot(data.index, data['Close'], label='Цена закрытия', linewidth=2)
        ax1.fill_between(data.index, data['Low'], data['High'], alpha=0.3, label='Min-Max')

        ax1.set_title(f'{ticker} - Цена и объем торгов', fontsize=16, fontweight='bold')
        ax1.set_ylabel('Цена ($)', fontsize=12)
        ax1.legend(loc='upper left')
        ax1.grid(True, alpha=0.3)

        # График объема
        colors = ['green' if data['Close'].iloc[i] > data['Open'].iloc[i]
                 else 'red' for i in range(len(data))]
        ax2.bar(data.index, data['Volume'], color=colors, alpha=0.6)
        ax2.set_ylabel('Объем', fontsize=12)
        ax2.set_xlabel('Дата', fontsize=12)
        ax2.grid(True, alpha=0.3)

        plt.tight_layout()

        if save:
            filename = f'{self.output_dir}/{ticker}_price_volume.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ График сохранен: {filename}")

        plt.close()

    def plot_technical_indicators(self, data: pd.DataFrame, ticker: str, save: bool = True):
        """
        График с техническими индикаторами

        Args:
            data: DataFrame с данными и индикаторами
            ticker: Тикер акции
            save: Сохранить график
        """
        fig, axes = plt.subplots(4, 1, figsize=(14, 16))

        # 1. Цена и скользящие средние
        axes[0].plot(data.index, data['Close'], label='Цена', linewidth=2)
        if 'SMA_20' in data.columns:
            axes[0].plot(data.index, data['SMA_20'], label='SMA 20', alpha=0.7)
        if 'SMA_50' in data.columns:
            axes[0].plot(data.index, data['SMA_50'], label='SMA 50', alpha=0.7)
        if 'SMA_200' in data.columns:
            axes[0].plot(data.index, data['SMA_200'], label='SMA 200', alpha=0.7)

        axes[0].set_title(f'{ticker} - Технический анализ', fontsize=16, fontweight='bold')
        axes[0].set_ylabel('Цена ($)', fontsize=12)
        axes[0].legend(loc='upper left')
        axes[0].grid(True, alpha=0.3)

        # 2. Bollinger Bands
        if 'BB_Upper' in data.columns:
            axes[1].plot(data.index, data['Close'], label='Цена', linewidth=2)
            axes[1].plot(data.index, data['BB_Upper'], label='BB Upper', linestyle='--', alpha=0.7)
            axes[1].plot(data.index, data['BB_Middle'], label='BB Middle', linestyle='--', alpha=0.7)
            axes[1].plot(data.index, data['BB_Lower'], label='BB Lower', linestyle='--', alpha=0.7)
            axes[1].fill_between(data.index, data['BB_Lower'], data['BB_Upper'], alpha=0.1)

        axes[1].set_ylabel('Цена ($)', fontsize=12)
        axes[1].set_title('Bollinger Bands', fontsize=12)
        axes[1].legend(loc='upper left')
        axes[1].grid(True, alpha=0.3)

        # 3. RSI
        if 'RSI' in data.columns:
            axes[2].plot(data.index, data['RSI'], label='RSI', linewidth=2, color='purple')
            axes[2].axhline(y=70, color='r', linestyle='--', alpha=0.5, label='Перекупленность')
            axes[2].axhline(y=30, color='g', linestyle='--', alpha=0.5, label='Перепроданность')
            axes[2].fill_between(data.index, 30, 70, alpha=0.1)

        axes[2].set_ylabel('RSI', fontsize=12)
        axes[2].set_title('Relative Strength Index (RSI)', fontsize=12)
        axes[2].legend(loc='upper left')
        axes[2].grid(True, alpha=0.3)
        axes[2].set_ylim([0, 100])

        # 4. MACD
        if 'MACD' in data.columns:
            axes[3].plot(data.index, data['MACD'], label='MACD', linewidth=2)
            axes[3].plot(data.index, data['MACD_Signal'], label='Signal', linewidth=2)
            axes[3].bar(data.index, data['MACD_Diff'], label='Histogram', alpha=0.3)
            axes[3].axhline(y=0, color='black', linestyle='-', alpha=0.3)

        axes[3].set_ylabel('MACD', fontsize=12)
        axes[3].set_xlabel('Дата', fontsize=12)
        axes[3].set_title('MACD', fontsize=12)
        axes[3].legend(loc='upper left')
        axes[3].grid(True, alpha=0.3)

        plt.tight_layout()

        if save:
            filename = f'{self.output_dir}/{ticker}_technical.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ График сохранен: {filename}")

        plt.close()

    def plot_candlestick(self, data: pd.DataFrame, ticker: str, save: bool = True):
        """
        Интерактивный график свечей (candlestick) с индикаторами

        Args:
            data: DataFrame с данными
            ticker: Тикер акции
            save: Сохранить график
        """
        # Создаем subplots
        fig = make_subplots(
            rows=4, cols=1,
            shared_xaxes=True,
            vertical_spacing=0.05,
            row_heights=[0.5, 0.2, 0.15, 0.15],
            subplot_titles=(f'{ticker} - Цена', 'Объем', 'RSI', 'MACD')
        )

        # Candlestick
        fig.add_trace(
            go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Цена'
            ),
            row=1, col=1
        )

        # Скользящие средние
        if 'SMA_20' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['SMA_20'],
                          name='SMA 20', line=dict(color='orange')),
                row=1, col=1
            )
        if 'SMA_50' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['SMA_50'],
                          name='SMA 50', line=dict(color='blue')),
                row=1, col=1
            )

        # Bollinger Bands
        if 'BB_Upper' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['BB_Upper'],
                          name='BB Upper', line=dict(dash='dash', color='gray')),
                row=1, col=1
            )
            fig.add_trace(
                go.Scatter(x=data.index, y=data['BB_Lower'],
                          name='BB Lower', line=dict(dash='dash', color='gray')),
                row=1, col=1
            )

        # Объем
        colors = ['green' if row['Close'] > row['Open'] else 'red'
                 for idx, row in data.iterrows()]
        fig.add_trace(
            go.Bar(x=data.index, y=data['Volume'], name='Объем',
                  marker_color=colors),
            row=2, col=1
        )

        # RSI
        if 'RSI' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['RSI'], name='RSI',
                          line=dict(color='purple')),
                row=3, col=1
            )
            fig.add_hline(y=70, line_dash="dash", line_color="red", row=3, col=1)
            fig.add_hline(y=30, line_dash="dash", line_color="green", row=3, col=1)

        # MACD
        if 'MACD' in data.columns:
            fig.add_trace(
                go.Scatter(x=data.index, y=data['MACD'], name='MACD'),
                row=4, col=1
            )
            fig.add_trace(
                go.Scatter(x=data.index, y=data['MACD_Signal'], name='Signal'),
                row=4, col=1
            )
            fig.add_trace(
                go.Bar(x=data.index, y=data['MACD_Diff'], name='Histogram'),
                row=4, col=1
            )

        # Обновляем layout
        fig.update_layout(
            title=f'{ticker} - Полный технический анализ',
            xaxis_rangeslider_visible=False,
            height=1200,
            showlegend=True
        )

        fig.update_yaxes(title_text="Цена ($)", row=1, col=1)
        fig.update_yaxes(title_text="Объем", row=2, col=1)
        fig.update_yaxes(title_text="RSI", row=3, col=1)
        fig.update_yaxes(title_text="MACD", row=4, col=1)

        if save:
            filename = f'{self.output_dir}/{ticker}_candlestick.html'
            fig.write_html(filename)
            print(f"✅ Интерактивный график сохранен: {filename}")

    def plot_comparison(self, data_dict: dict, save: bool = True):
        """
        Сравнительный график нескольких акций

        Args:
            data_dict: Словарь {ticker: DataFrame}
            save: Сохранить график
        """
        plt.figure(figsize=(14, 8))

        for ticker, data in data_dict.items():
            # Нормализуем к первому значению для сравнения
            normalized = (data['Close'] / data['Close'].iloc[0]) * 100
            plt.plot(data.index, normalized, label=ticker, linewidth=2)

        plt.title('Сравнение акций (нормализовано к 100)', fontsize=16, fontweight='bold')
        plt.xlabel('Дата', fontsize=12)
        plt.ylabel('Относительное изменение (%)', fontsize=12)
        plt.legend(loc='upper left')
        plt.grid(True, alpha=0.3)

        if save:
            filename = f'{self.output_dir}/comparison.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Сравнительный график сохранен: {filename}")

        plt.close()

    def create_analysis_report(self, ticker: str, data: pd.DataFrame,
                              analysis: dict, save: bool = True):
        """
        Создать полный отчет с анализом

        Args:
            ticker: Тикер акции
            data: DataFrame с данными
            analysis: Словарь с результатами анализа
            save: Сохранить отчет
        """
        fig = plt.figure(figsize=(16, 12))
        gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

        # 1. Основной график цены
        ax1 = fig.add_subplot(gs[0, :])
        ax1.plot(data.index, data['Close'], linewidth=2, color='blue')
        if 'SMA_20' in data.columns:
            ax1.plot(data.index, data['SMA_20'], alpha=0.7, label='SMA 20')
        if 'SMA_50' in data.columns:
            ax1.plot(data.index, data['SMA_50'], alpha=0.7, label='SMA 50')

        ax1.set_title(f'{ticker} - Анализ акции', fontsize=18, fontweight='bold')
        ax1.set_ylabel('Цена ($)', fontsize=12)
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. Текстовый блок с анализом
        ax2 = fig.add_subplot(gs[1, 0])
        ax2.axis('off')

        trend_info = analysis.get('trend', {})
        momentum_info = analysis.get('momentum', {})
        signals = analysis.get('signals', {})

        info_text = f"""
        ТЕКУЩАЯ ИНФОРМАЦИЯ:
        Цена: ${trend_info.get('current_price', 0):.2f}

        ТРЕНД:
        Краткосрочный: {trend_info.get('short_term_trend', 'N/A')}
        Долгосрочный: {trend_info.get('long_term_trend', 'N/A')}

        МОМЕНТУМ:
        RSI: {momentum_info.get('rsi', 0):.2f} ({momentum_info.get('rsi_signal', 'N/A')})
        MACD: {momentum_info.get('macd_signal', 'N/A')}

        РЕКОМЕНДАЦИЯ:
        {signals.get('recommendation', 'N/A')}
        Уверенность: {signals.get('confidence', 'N/A')}
        """

        ax2.text(0.1, 0.9, info_text, transform=ax2.transAxes,
                fontsize=11, verticalalignment='top',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5),
                family='monospace')

        # 3. RSI
        ax3 = fig.add_subplot(gs[1, 1])
        if 'RSI' in data.columns:
            ax3.plot(data.index, data['RSI'], color='purple', linewidth=2)
            ax3.axhline(y=70, color='r', linestyle='--', alpha=0.5)
            ax3.axhline(y=30, color='g', linestyle='--', alpha=0.5)
            ax3.fill_between(data.index, 30, 70, alpha=0.1)
            ax3.set_ylim([0, 100])

        ax3.set_title('RSI', fontsize=12)
        ax3.grid(True, alpha=0.3)

        # 4. Объем
        ax4 = fig.add_subplot(gs[2, 0])
        colors = ['green' if data['Close'].iloc[i] > data['Open'].iloc[i]
                 else 'red' for i in range(len(data))]
        ax4.bar(data.index, data['Volume'], color=colors, alpha=0.6)
        ax4.set_title('Объем торгов', fontsize=12)
        ax4.grid(True, alpha=0.3)

        # 5. MACD
        ax5 = fig.add_subplot(gs[2, 1])
        if 'MACD' in data.columns:
            ax5.plot(data.index, data['MACD'], label='MACD', linewidth=2)
            ax5.plot(data.index, data['MACD_Signal'], label='Signal', linewidth=2)
            ax5.bar(data.index, data['MACD_Diff'], alpha=0.3, label='Histogram')
            ax5.axhline(y=0, color='black', linestyle='-', alpha=0.3)

        ax5.set_title('MACD', fontsize=12)
        ax5.legend()
        ax5.grid(True, alpha=0.3)

        plt.suptitle(f'Полный отчет - {ticker}', fontsize=20, fontweight='bold', y=0.995)

        if save:
            filename = f'{self.output_dir}/{ticker}_report.png'
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ Отчет сохранен: {filename}")

        plt.close()
