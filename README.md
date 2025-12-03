# mqtt-topics-api

1new text
Local testing:

```
python -m pip install -e ".[mqtt_logger,mqtt_logs_api,shared]"

cd src && python -m mqtt_logger.main
cd src && python -m mqtt_logs_api.main
cd src && python -m mqtt_logs_cleaner.main
```

Docker:

```
docker build -t mqtt_logger -f mqtt_logger/Dockerfile .
docker build -t mqtt_logs_api -f mqtt_logs_api/Dockerfile .
docker build -t mqtt_logs_cleaner -f mqtt_logs_cleaner/Dockerfile .
```

Docker launch:

```
docker run mqtt_logger
docker run -p 5283:5283 mqtt_logs_api
docker run mqtt_logs_cleaner
```

K8s:

```
Use yandex.disk from k8s.docx
```

Validate before commit:

```
helm template ./helm/mqtt-topics-api
```
