# Cloud Log Monitoring API

A small cloud engineering project that simulates log ingestion, health checks, metrics, persistence, and alert detection for application reliability.

## Overview

This project is a Dockerized FastAPI service that accepts logs from services, stores them in SQLite, exposes health and metrics endpoints, and detects a basic high-error-rate alert condition.

I built this project to practice cloud engineering fundamentals: API deployment, containerization, health checks, environment-based configuration, persistent storage, observability, and reliability thinking.

## Architecture

Client → FastAPI API → SQLite database → Metrics and alert detection

## Features

- REST API built with FastAPI
- Log ingestion endpoint
- Health check endpoint
- Basic alert detection
- SQLite persistence using SQLAlchemy
- Metrics endpoint for basic observability
- Log cleanup endpoint for repeatable testing
- Environment-based database configuration
- Dockerized application
- Docker Compose support
- Makefile for common development commands
- Ready for deployment to a cloud container runtime

## Endpoints

### GET /

Returns basic project information.

### GET /health

Returns service health, current log count, and storage backend.

### POST /logs

Ingests a log entry.

Example request:

```json
{
  "service": "payment-api",
  "level": "ERROR",
  "message": "Database timeout"
}
```

### GET /logs

Returns all received logs.

### DELETE /logs

Deletes all stored logs so the API can be tested from a clean state.

### GET /alerts

Returns alerts when a service has 5 or more ERROR logs in the last 10 minutes.

### GET /metrics

Returns basic operational metrics:

- Total logs
- Logs by severity level
- Logs by service

## Run locally

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn main:app --reload
```

Open the interactive docs:

```text
http://127.0.0.1:8000/docs
```

## Run with Docker

Build the image:

```bash
docker build -t cloud-log-monitoring-api .
```

Run the container:

```bash
docker run -p 8080:8080 cloud-log-monitoring-api
```

Open:

```text
http://localhost:8080/docs
```

## Run with Docker Compose

Start the service:

```bash
docker compose up --build
```

Open:

```text
http://localhost:8080/docs
```

Stop the service:

```bash
docker compose down
```

## Common commands

```bash
make install
make run
make compose-up
make test-api
make compose-down
```

## Example test

Send one error log:

```bash
curl -X POST http://localhost:8080/logs \
  -H "Content-Type: application/json" \
  -d '{"service":"payment-api","level":"ERROR","message":"Database timeout"}'
```

After sending 5 ERROR logs for the same service, check alerts:

```bash
curl http://localhost:8080/alerts
```

Expected result:

```json
{
  "alert_count": 1,
  "alerts": [
    {
      "service": "payment-api",
      "alert": "High error rate detected",
      "error_count": 5,
      "window": "10 minutes",
      "severity": "high"
    }
  ]
}
```

## What I learned

- How to build a small API for operational data
- How health checks are used in cloud services
- How to containerize a Python application
- How to persist data with SQLite and SQLAlchemy
- How alert rules can detect reliability issues
- How metrics endpoints support basic observability
- How to think about cloud application deployment and runtime configuration

## Future improvements

- Replace SQLite with PostgreSQL or Cloud SQL
- Add authentication for log ingestion
- Add structured JSON logging
- Add CI/CD with GitHub Actions
- Define infrastructure with Terraform
- Add metrics dashboards and alert notifications