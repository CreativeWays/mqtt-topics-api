sudo tail -f /opt/mqttapp/logs/mqttapp-error.log
sudo tail -f /opt/mqttapp/logs/api_server-error.log
journalctl -u mqttapp.service -f # service log
