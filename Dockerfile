FROM python:3.12

# Рабочая директория
WORKDIR /app

# Устанавливаем зависимости (слой кэшируется пока не изменится requirements.txt)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код приложения
COPY . .

# Запускаем uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]