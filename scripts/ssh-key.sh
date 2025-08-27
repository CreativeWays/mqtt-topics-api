sudo -u mqttapp ssh-keygen -t ed25519 -C "mqttapp@server" -f /opt/mqttapp/.ssh/id_ed25519 -N ""
sudo cat /opt/mqttapp/.ssh/id_ed25519.pub
