#!/bin/bash
set -e

APP_DIR="/opt/mqttapp"
VENV_DIR="$APP_DIR/venv"

echo "Setting up MQTT Application..."

# Создаем виртуальное окружение если не существует
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment..."
    python3 -m venv "$VENV_DIR"
fi

# Активируем venv и устанавливаем зависимости
echo "Installing dependencies..."
source "$VENV_DIR/bin/activate"
pip install --upgrade pip
pip install -r "$APP_DIR/requirements.txt"

echo "Setup completed successfully!"
