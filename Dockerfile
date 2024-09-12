# Используем официальный образ Python
FROM python:3.10-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл с зависимостями в контейнер
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальную часть приложения в рабочую директорию
COPY . .

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Открываем порт, на котором работает бот (если нужно)
EXPOSE 8080

# Запуск приложения
CMD ["python", "bot/main.py"]
