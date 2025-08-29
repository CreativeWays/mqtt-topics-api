sudo adduser --system --group --home /opt/mqttapp mqttapp
sudo mkdir -p /opt/mqttapp/{app,logs,data,scripts}
sudo chown -R mqttapp:mqttapp /opt/mqttapp
sudo chown -R mqttapp:mqttapp /opt/mqttapp/src
sudo chown -R mqttapp:mqttapp /opt/mqttapp/scripts
sudo -u mqttapp chmod -R 755 /opt/mqttapp
