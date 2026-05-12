import requests


BASE_URL = "http://localhost:8080"


def send_log(service, level, message):
    response = requests.post(
        f"{BASE_URL}/logs",
        json={
            "service": service,
            "level": level,
            "message": message,
        },
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def main():
    print("Checking service health...")
    health = requests.get(f"{BASE_URL}/health", timeout=10)
    health.raise_for_status()
    print(health.json())

    print("\nSending 5 ERROR logs...")
    for i in range(5):
        result = send_log(
            service="payment-api",
            level="ERROR",
            message=f"Database timeout #{i + 1}",
        )
        print(result)

    print("\nChecking alerts...")
    alerts = requests.get(f"{BASE_URL}/alerts", timeout=10)
    alerts.raise_for_status()
    print(alerts.json())


if __name__ == "__main__":
    main()