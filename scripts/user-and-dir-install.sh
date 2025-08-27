sudo adduser --system --group --home /opt/mqttapp mqttapp
sudo mkdir -p /opt/mqttapp/{src,logs,data,scripts}
sudo chown -R mqttapp:mqttapp /opt/mqttapp
sudo chmod -R 755 /opt/mqttapp
