FROM python:3.12-slim

# Системные зависимости
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Устанавливаем зависимости отдельным слоем (кэшируется)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта
COPY . .

# Uvicorn слушает на 0.0.0.0
EXPOSE 8000

# Запускаем из backend/app, чтобы голые импорты (from config import ...) работали
WORKDIR /app/backend/app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
