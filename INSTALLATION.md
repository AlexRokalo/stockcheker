# Инструкции по установке

## Проблема с Python 3.13

Если вы используете Python 3.13 и получаете ошибку при установке pandas, есть несколько решений:

### Решение 1: Обновить pandas (РЕКОМЕНДУЕТСЯ)

```bash
# Обновите pip до последней версии
pip install --upgrade pip

# Установите зависимости (pandas >= 2.2.0 поддерживает Python 3.13)
pip install -r requirements.txt
```

### Решение 2: Использовать Python 3.11 или 3.12 (если проблема остается)

Создайте виртуальное окружение с Python 3.11/3.12:

**С помощью pyenv:**
```bash
# Установить pyenv (если еще не установлен)
# На Mac:
brew install pyenv

# На Linux:
curl https://pyenv.run | bash

# Установить Python 3.12
pyenv install 3.12.0

# Создать виртуальное окружение
pyenv virtualenv 3.12.0 stockcheker
pyenv activate stockcheker

# Установить зависимости
pip install -r requirements.txt
```

**С помощью conda (если у вас Miniconda/Anaconda):**
```bash
# Создать окружение с Python 3.12
conda create -n stockcheker python=3.12

# Активировать окружение
conda activate stockcheker

# Установить зависимости
pip install -r requirements.txt
```

**Стандартный venv с системным Python 3.12:**
```bash
# Если у вас установлен Python 3.12
python3.12 -m venv venv
source venv/bin/activate  # На Linux/Mac
# venv\Scripts\activate  # На Windows

pip install -r requirements.txt
```

### Решение 3: Установка без pandas (для быстрого теста)

Если хотите просто протестировать без pandas:

```bash
pip install yfinance matplotlib plotly ta
```

Но это не даст полного функционала.

## Минимальные требования

- Python: 3.9+ (рекомендуется 3.11 или 3.12)
- pip: 21.0+
- ОС: Windows, macOS, Linux

## Полная установка (шаг за шагом)

### 1. Проверить версию Python

```bash
python --version
# или
python3 --version
```

### 2. Обновить pip

```bash
pip install --upgrade pip
```

### 3. (Опционально) Создать виртуальное окружение

```bash
python -m venv venv
source venv/bin/activate  # На Linux/Mac
# venv\Scripts\activate  # На Windows
```

### 4. Установить зависимости

```bash
pip install -r requirements.txt
```

### 5. Проверить установку

```bash
python -c "import pandas; import yfinance; import matplotlib; print('Все установлено!')"
```

## Альтернативный requirements.txt для старых версий Python

Если у вас Python 3.9-3.10, создайте файл `requirements-old.txt`:

```
yfinance>=0.2.0
gspread>=5.0.0
oauth2client>=4.1.3
pandas>=1.5.0,<2.0.0
matplotlib>=3.5.0
seaborn>=0.12.0
numpy>=1.23.0
plotly>=5.10.0
ta>=0.10.0
python-dotenv>=0.20.0
```

И установите:
```bash
pip install -r requirements-old.txt
```

## Решение распространенных проблем

### Ошибка: "No module named 'numpy'"

```bash
pip install numpy --upgrade
```

### Ошибка: "Microsoft Visual C++ 14.0 or greater is required" (Windows)

Установите Visual C++ Build Tools:
https://visualstudio.microsoft.com/visual-cpp-build-tools/

### Ошибка: "Command 'gcc' failed" (Linux)

```bash
# Ubuntu/Debian
sudo apt-get install python3-dev build-essential

# Fedora/CentOS
sudo yum install python3-devel gcc
```

### Ошибка: "SSL: CERTIFICATE_VERIFY_FAILED" (Mac)

```bash
# Для Mac с Homebrew Python
/Applications/Python\ 3.*/Install\ Certificates.command

# Или установите certifi
pip install --upgrade certifi
```

### Медленная установка pandas

```bash
# Используйте предкомпилированные бинарники
pip install pandas --only-binary :all:

# Или используйте conda (быстрее)
conda install pandas
```

## Проверка совместимости

Запустите этот скрипт для проверки:

```python
import sys
print(f"Python версия: {sys.version}")

try:
    import pandas
    print(f"✅ pandas {pandas.__version__}")
except ImportError:
    print("❌ pandas не установлен")

try:
    import yfinance
    print(f"✅ yfinance установлен")
except ImportError:
    print("❌ yfinance не установлен")

try:
    import matplotlib
    print(f"✅ matplotlib {matplotlib.__version__}")
except ImportError:
    print("❌ matplotlib не установлен")

try:
    import plotly
    print(f"✅ plotly {plotly.__version__}")
except ImportError:
    print("❌ plotly не установлен")

print("\nГотово к использованию!" if all([pandas, yfinance, matplotlib, plotly]) else "\nНекоторые модули отсутствуют")
```

## Быстрая установка (все в одном)

**Для Python 3.11-3.13:**
```bash
python3 -m pip install --upgrade pip && \
pip install yfinance gspread oauth2client "pandas>=2.2.0" matplotlib seaborn numpy plotly ta python-dotenv
```

**Для Python 3.9-3.10:**
```bash
python3 -m pip install --upgrade pip && \
pip install yfinance gspread oauth2client "pandas<2.2.0" matplotlib seaborn numpy plotly ta python-dotenv
```

## Поддержка

Если проблемы продолжаются:
1. Создайте issue в репозитории с описанием ошибки
2. Укажите версию Python (`python --version`)
3. Укажите ОС
4. Приложите полный текст ошибки
