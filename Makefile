install:
	pip install -e .[mqtt_logger,mqtt_logs_api,shared]

install-logger:
	pip install -e .[mqtt_logger,shared]

install-api:
	pip install -e .[mqtt_logs_api,shared]

runl:
	python -m src.mqtt_logger.main

runa:
	python -m src.mqtt_logs_api.main
	
runc:
	python -m src.mqtt_logs_cleaner.main

dbrunl:
	docker build -t mqtt_logger -f src/mqtt_logger/Dockerfile .

dbruna:
	docker build -t mqtt_logs_api -f src/mqtt_logs_api/Dockerfile .

dbrunc:
	docker build -t mqtt_logs_cleaner -f src/mqtt_logs_cleaner/Dockerfile .

drunl:
	docker run -it --rm -v sqlite-data:/app/data mqtt_logger

druna:
	docker run -it --rm -v sqlite-data:/app/data -p 5283:5283 -e UNICORN_PORT=5283 mqtt_logs_api

drunc:
	docker run -it --rm -v sqlite-data:/app/data mqtt_logs_cleaner