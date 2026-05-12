from datetime import datetime, timedelta, timezone
from typing import Literal
import logging
import os
from fastapi import Depends, FastAPI
from pydantic import BaseModel, Field
from sqlalchemy import Column, DateTime, Integer, String, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)

logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./logs.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

Base = declarative_base()


class LogRecord(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    service = Column(String, index=True, nullable=False)
    level = Column(String, index=True, nullable=False)
    message = Column(String, nullable=False)
    timestamp = Column(DateTime, nullable=False)


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="Cloud Log Monitoring API",
    description="A small cloud engineering project for log ingestion, health checks, and alert detection.",
    version="1.0.0",
)


class LogEntry(BaseModel):
    service: str = Field(..., min_length=1, example="payment-api")
    level: Literal["INFO", "WARNING", "ERROR"] = Field(..., example="ERROR")
    message: str = Field(..., min_length=1, example="Database timeout")
    timestamp: datetime | None = None
      
class LogResponse(BaseModel):
    id: int
    service: str
    level: str
    message: str
    timestamp: datetime

    class Config:
        from_attributes = True


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
def root():
    return {
        "message": "Cloud Log Monitoring API",
        "docs": "/docs",
        "health": "/health",
    }


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    log_count = db.query(LogRecord).count()

    return {
        "status": "healthy",
        "timestamp": datetime.now(timezone.utc),
        "log_count": log_count,
        "storage": "sqlite",
    }


@app.post("/logs")
def ingest_log(log: LogEntry, db: Session = Depends(get_db)):
    timestamp = log.timestamp or datetime.now(timezone.utc)

    record = LogRecord(
        service=log.service,
        level=log.level,
        message=log.message,
        timestamp=timestamp,
    )

    db.add(record)
    db.commit()
    db.refresh(record)
    logger.info(
        "Ingested log service=%s level=%s id=%s",
        record.service,
        record.level,
        record.id,
    )

    return {
        "status": "received",
        "log": LogResponse.model_validate(record),
    }


@app.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    records = db.query(LogRecord).order_by(LogRecord.timestamp.desc()).all()

    return {
        "count": len(records),
        "logs": [LogResponse.model_validate(record) for record in records],
    }


@app.get("/alerts")
def get_alerts(db: Session = Depends(get_db)):
    now = datetime.now(timezone.utc)
    window_start = now - timedelta(minutes=10)

    recent_errors = (
        db.query(LogRecord)
        .filter(LogRecord.level == "ERROR")
        .filter(LogRecord.timestamp >= window_start)
        .all()
    )

    error_counts = {}

    for log in recent_errors:
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


@app.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    records = db.query(LogRecord).all()

    total_logs = len(records)
    error_logs = sum(1 for record in records if record.level == "ERROR")
    warning_logs = sum(1 for record in records if record.level == "WARNING")
    info_logs = sum(1 for record in records if record.level == "INFO")

    logs_by_service = {}

    for record in records:
        logs_by_service[record.service] = logs_by_service.get(record.service, 0) + 1

    return {
        "total_logs": total_logs,
        "logs_by_level": {
            "INFO": info_logs,
            "WARNING": warning_logs,
            "ERROR": error_logs,
        },
        "logs_by_service": logs_by_service,
    }
@app.delete("/logs")
def delete_logs(db: Session = Depends(get_db)):
    deleted_count = db.query(LogRecord).count()
    db.query(LogRecord).delete()
    db.commit()
    logger.info("Deleted logs count=%s", deleted_count)
    return {
        "status": "deleted",
        "deleted_logs": deleted_count,
    }