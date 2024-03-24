# Используйте официальный образ Python
FROM python:3.10

# Установите рабочую директорию в контейнере
WORKDIR /app

# Скопируйте файл requirements.txt в контейнер
COPY requirements.txt .

RUN apt-get update
RUN apt-get install -y redis

RUN pip install --upgrade pip \
  && pip install --no-cache-dir --index-url https://pypi.python.org/simple/ -r requirements.txt

# Скопируйте все остальное в контейнер
COPY . .

# Запустите ваше приложение
CMD gunicorn main:app --workers 1 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000
