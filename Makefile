install:
	pip install -r requirements.txt

run:
	uvicorn main:app --reload

docker-build:
	docker build -t cloud-log-monitoring-api .

docker-run:
	docker run -p 8080:8080 cloud-log-monitoring-api

compose-up:
	docker compose up --build

compose-down:
	docker compose down

test-api:
	python test_api.py

test:
	pytest

check:
	pytest