from fastapi.testclient import TestClient

from main import app


client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_readiness_check():
    response = client.get("/ready")

    assert response.status_code == 200
    assert response.json()["status"] == "ready"
    assert response.json()["database"] == "reachable"


def test_log_ingestion_and_alerting():
    client.delete("/logs")

    for i in range(5):
        response = client.post(
            "/logs",
            json={
                "service": "payment-api",
                "level": "ERROR",
                "message": f"Database timeout #{i + 1}",
            },
        )

        assert response.status_code == 200
        assert response.json()["status"] == "received"

    alerts_response = client.get("/alerts")

    assert alerts_response.status_code == 200
    assert alerts_response.json()["alert_count"] == 1
    assert alerts_response.json()["alerts"][0]["service"] == "payment-api"


def test_metrics_endpoint():
    client.delete("/logs")

    client.post(
        "/logs",
        json={
            "service": "user-api",
            "level": "INFO",
            "message": "User profile loaded successfully",
        },
    )

    client.post(
        "/logs",
        json={
            "service": "payment-api",
            "level": "ERROR",
            "message": "Database timeout",
        },
    )

    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.json()["total_logs"] == 2
    assert response.json()["logs_by_level"]["INFO"] == 1
    assert response.json()["logs_by_level"]["ERROR"] == 1