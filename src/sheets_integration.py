"""
Модуль для интеграции с Google Sheets
"""
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from typing import Optional, List
import os


class GoogleSheetsIntegration:
    """Класс для работы с Google Sheets"""

    def __init__(self, credentials_file: str = 'credentials.json'):
        """
        Инициализация подключения к Google Sheets

        Args:
            credentials_file: Путь к файлу с credentials
        """
        self.credentials_file = credentials_file
        self.client = None
        self.connect()

    def connect(self):
        """Подключиться к Google Sheets API"""
        try:
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]

            if not os.path.exists(self.credentials_file):
                print(f"⚠️  Файл credentials не найден: {self.credentials_file}")
                print("Инструкция по получению credentials:")
                print("1. Перейдите в Google Cloud Console")
                print("2. Создайте проект или выберите существующий")
                print("3. Включите Google Sheets API")
                print("4. Создайте Service Account и скачайте JSON ключ")
                print("5. Сохраните файл как 'credentials.json'")
                return

            creds = ServiceAccountCredentials.from_json_keyfile_name(
                self.credentials_file, scope
            )
            self.client = gspread.authorize(creds)
            print("✅ Подключение к Google Sheets установлено")
        except Exception as e:
            print(f"❌ Ошибка подключения к Google Sheets: {e}")

    def read_sheet(self, sheet_id: str, worksheet_name: str = None) -> Optional[pd.DataFrame]:
        """
        Прочитать данные из Google Sheets

        Args:
            sheet_id: ID таблицы Google Sheets
            worksheet_name: Имя листа (если None, берется первый лист)

        Returns:
            DataFrame с данными из таблицы
        """
        try:
            if not self.client:
                print("❌ Нет подключения к Google Sheets")
                return None

            sheet = self.client.open_by_key(sheet_id)

            if worksheet_name:
                worksheet = sheet.worksheet(worksheet_name)
            else:
                worksheet = sheet.get_worksheet(0)

            data = worksheet.get_all_records()
            df = pd.DataFrame(data)

            print(f"✅ Загружено {len(df)} строк из Google Sheets")
            return df
        except Exception as e:
            print(f"❌ Ошибка чтения Google Sheets: {e}")
            return None

    def write_analysis_results(self, sheet_id: str, results: pd.DataFrame,
                               worksheet_name: str = "Analysis Results"):
        """
        Записать результаты анализа в Google Sheets

        Args:
            sheet_id: ID таблицы
            results: DataFrame с результатами
            worksheet_name: Имя листа для записи
        """
        try:
            if not self.client:
                print("❌ Нет подключения к Google Sheets")
                return

            sheet = self.client.open_by_key(sheet_id)

            # Попытка получить существующий лист или создать новый
            try:
                worksheet = sheet.worksheet(worksheet_name)
                worksheet.clear()
            except:
                worksheet = sheet.add_worksheet(
                    title=worksheet_name,
                    rows=len(results) + 1,
                    cols=len(results.columns)
                )

            # Записываем заголовки
            worksheet.update([results.columns.values.tolist()] + results.values.tolist())

            print(f"✅ Результаты записаны в лист '{worksheet_name}'")
        except Exception as e:
            print(f"❌ Ошибка записи в Google Sheets: {e}")

    def get_tickers_from_sheet(self, sheet_id: str,
                               ticker_column: str = 'Ticker',
                               worksheet_name: str = None) -> List[str]:
        """
        Получить список тикеров из таблицы

        Args:
            sheet_id: ID таблицы
            ticker_column: Название колонки с тикерами
            worksheet_name: Имя листа

        Returns:
            Список тикеров
        """
        df = self.read_sheet(sheet_id, worksheet_name)
        if df is not None and ticker_column in df.columns:
            tickers = df[ticker_column].dropna().unique().tolist()
            return [str(t).strip().upper() for t in tickers if str(t).strip()]
        return []
