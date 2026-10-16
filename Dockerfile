# Используем стабильный и легкий базовый образ Python
FROM python:3.12-slim

# Указываем рабочую директорию внутри контейнера
WORKDIR /app

# Запрещаем Python кешировать байт-код (.pyc) и буферизировать логи
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Сначала копируем только файл зависимостей (для эффективного кэширования слоев Docker)
COPY requirements.txt .

# Обновляем менеджер пакетов pip и устанавливаем библиотеки
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем все остальные файлы проекта (включая картинку ETVmc.jpg и папки)
COPY . .

# Создаём папку для БД (её потом можно смонтировать как volume)
RUN mkdir -p /app/data

# Главная команда для запуска бота при старте контейнера
CMD ["python", "main.py"]
