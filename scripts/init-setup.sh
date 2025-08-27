# Copy systemd files to /etc/systemd/system
sudo cp /opt/mqttapp/scripts/mqttapp.service /etc/systemd/system/mqttapp.service
sudo cp /opt/mqttapp/scripts/mqttapp-cleanup.timer /etc/systemd/system/mqttapp-cleanup.timer
sudo cp /opt/mqttapp/scripts/mqttapp-cleanup.service /etc/systemd/system/mqttapp-cleanup.service

# Создание пользователя и каталогов
sudo bash /opt/mqttapp/scripts/user-and-dir-install.sh
# Запустите setup скрипт
sudo -u mqttapp bash /opt/mqttapp/scripts/python-venv-setup.sh

# Включите и запустите сервис
sudo systemctl daemon-reload
sudo systemctl enable mqttapp.service
sudo systemctl start mqttapp.service

# Сервис с таймером очистки
sudo systemctl enable mqttapp-cleanup.service
sudo systemctl start mqttapp-cleanup.service
sudo systemctl enable mqttapp-cleanup.timer
sudo systemctl start mqttapp-cleanup.timer

# Проверьте статус
sudo systemctl status mqttapp.service
