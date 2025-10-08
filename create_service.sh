#!/bin/bash
# Останавливаем и удаляем старый сервис
sudo systemctl stop farm
sudo systemctl disable farm
sudo rm -f /etc/systemd/system/farm.service

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

APP_DIR="$(dirname "$SCRIPT_DIR")"
SERVICE_NAME="farm"
USER_NAME=$(whoami)

if [[ $EUID -ne 0 ]]; then
    echo "Error: Run with sudo!"
    exit 1
fi

if systemctl list-unit-files | grep -q "${SERVICE_NAME}.service"; then
    echo "Service ${SERVICE_NAME} already exists!"
    systemctl status "${SERVICE_NAME}"
    exit 0
fi

# Находим виртуальное окружение (предполагаем, что оно в проекте)
VENV_PATH="${APP_DIR}/venv"
if [[ ! -d "$VENV_PATH" ]]; then
    VENV_PATH="${APP_DIR}/.venv"
fi

if [[ ! -d "$VENV_PATH" ]]; then
    echo "Error: Virtual environment not found in $APP_DIR"
    echo "Please create virtual environment first:"
    echo "cd $APP_DIR && python -m venv venv"
    exit 1
fi

# Читаем настройки из .env файла если он есть
if [ -f "$APP_DIR/.env.dev" ]; then
    echo "Found .env.dev file, reading settings..."
    source "$APP_DIR/.env.dev"
    HOST=${HOST:-0.0.0.0}
    PORT=${PORT:-8000}
else
    # Или из settings.py если нет .env
    HOST="0.0.0.0"
    PORT="7001"  # ваш порт по умолчанию
    echo "Using default settings: host=$HOST, port=$PORT"
fi

PYTHON_PATH="${VENV_PATH}/bin/python"
UVICORN_PATH="${VENV_PATH}/bin/uvicorn"

# Проверяем что uvicorn установлен
if [[ ! -f "$UVICORN_PATH" ]]; then
    echo "Error: uvicorn not found in virtual environment"
    echo "Please install: $PYTHON_PATH -m pip install uvicorn"
    exit 1
fi

cat > "/etc/systemd/system/${SERVICE_NAME}.service" << EOF
[Unit]
Description=My FastAPI Application
After=network.target

[Service]
Type=exec
User=${USER_NAME}
Group=${USER_NAME}
WorkingDirectory=${APP_DIR}
ExecStart=$(which uvicorn) app.main:create_app --host ${HOST} --port ${PORT}
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable "${SERVICE_NAME}"
systemctl start "${SERVICE_NAME}"

echo "Service ${SERVICE_NAME} created and started!"
systemctl status "${SERVICE_NAME}"
