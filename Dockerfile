# Используем официальный образ Python
FROM python:3.11.4-slim

# Устанавливаем зависимости
RUN apt-get update \
    && apt-get install -y gcc \
    && apt-get clean

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Копируем файл зависимостей в контейнер
COPY requirements.txt /app/

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем всё содержимое проекта в контейнер
COPY . /app/

# Открываем порт, на котором будет работать приложение
EXPOSE 8000

# Команда для запуска сервера Django
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
