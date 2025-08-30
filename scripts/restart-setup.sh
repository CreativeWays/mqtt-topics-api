# Перезапускаем сервис
sudo systemctl restart mqttapp.service
sudo systemctl restart mqttapp-cleanup.service
sudo systemctl restart mqttapp-cleanup.timer
sudo systemctl restart sensor-api.service
