#!/bin/bash

APP_DIR=$(pwd)
PID_FILE="/tmp/gunicorn.pid"

# Функция для запуска приложения
start_app() {
    echo "Starting application..."

    # Проверяем, не запущено ли уже приложение
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "Application is already running with PID $(cat $PID_FILE)"
        exit 1
    fi

    # Читаем настройки из .env файла если он есть
    if [ -f "$APP_DIR/.env.dev" ]; then
        echo "Found .env.dev file, reading settings..."
        source "$APP_DIR/.env.dev"
        HOST=${HOST}
        PORT=${PORT}
    else
        # Или из settings.py если нет .env
        HOST="0.0.0.0"
        PORT="7001"  # ваш порт по умолчанию
        echo "Using default settings: host=$HOST, port=$PORT"
    fi

    echo "Using settings: host=$HOST, port=$PORT"
    # активируем окружение, нужно что бы была папка venv
    source "$APP_DIR/venv/bin/activate"
#    gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b ${HOST}:${PORT} app.main:create_app --pid $PID_FILE
    # Запускаем gunicorn в фоновом режиме
    gunicorn -w 4 -k uvicorn.workers.UvicornWorker -b ${HOST}:${PORT} app.main:create_app --daemon --pid $PID_FILE

    if [ $? -eq 0 ]; then
        echo "Application started successfully with PID $(cat $PID_FILE)"
    else
        echo "Failed to start application"
        exit 1
    fi
}

# Функция для остановки приложения
stop_app() {
    echo "Stopping application..."

    if [ -f "$PID_FILE" ]; then
        PID=$(cat "$PID_FILE")
        echo "Application is not running, but PID file exists. Removing PID file."
        kill "$PID" && rm "$PID_FILE"
    else
        echo "Application is not running (PID file not found)"
    fi

}

# Функция для показа статуса
status_app() {
    if [ -f "$PID_FILE" ] && kill -0 $(cat "$PID_FILE") 2>/dev/null; then
        echo "Application is running with PID $(cat $PID_FILE)"
    else
        echo "Application is not running"
    fi
}

# Обработка аргументов командной строки
case "$1" in
    start)
        start_app
        ;;
    stop)
        stop_app
        ;;
    status)
        status_app
        ;;
    restart)
        stop_app
        sleep 2
        start_app
        ;;
    *)
        echo "Usage: $0 {start|stop|status|restart}"
        echo "  start   - Start the application"
        echo "  stop    - Stop the application and print 'hello world'"
        echo "  status  - Check application status"
        echo "  restart - Restart the application"
        exit 1
        ;;
esac
