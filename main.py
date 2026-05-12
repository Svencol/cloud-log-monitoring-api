from datetime import datetime, timedelta, timezone
from typing import List, Literal

from fastapi import FastAPI
from pydantic import BaseModel, Field


app = FastAPI(
    title="Cloud Log Monitoring API",
    description="A small cloud engineering project for log ingestion, health checks, and alert detection.",
    version="1.0.0",
)


class LogEntry(BaseModel):
    service: str = Field(..., example="payment-api")
    level: Literal["INFO", "WARNING", "ERROR"] = Field(..., example="ERROR")
    message: str = Field(..., example="Database timeout")
    timestamp: datetime | None = None


logs: List[LogEntry] = []


@app.get("/")
def root():
    return {
        "message": "Cloud Log Monitoring API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc),
        "log_count": len(logs),
    }


@app.post("/logs")
def ingest_log(log: LogEntry):
    if log.timestamp is None:
        log.timestamp = datetime.now(timezone.utc)

    logs.append(log)

    return {
        "status": "received",
        "log": log,
    }


@app.get("/logs")
def get_logs():
    return {
        "count": len(logs),
        "logs": logs,
    }


@app.get("/alerts")
def get_alerts():
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=10)

    error_counts = {}

    for log in logs:
        if log.level == "ERROR" and log.timestamp >= window_start:
            error_counts[log.service] = error_counts.get(log.service, 0) + 1

    alerts = []

    for service, count in error_counts.items():
        if count >= 5:
            alerts.append(
                {
                    "service": service,
                    "alert": "High error rate detected",
                    "error_count": count,
                    "window": "10 minutes",
                    "severity": "high",
                }
            )

    return {
        "alert_count": len(alerts),
        "alerts": alerts,
    }
