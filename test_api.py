import json

import requests


BASE_URL = "http://localhost:8080"


def send_log(log):
    response = requests.post(
        f"{BASE_URL}/logs",
        json=log,
        timeout=10,
    )
    response.raise_for_status()
    return response.json()


def main():
    print("Clearing old logs...")
    cleanup = requests.delete(f"{BASE_URL}/logs", timeout=10)
    cleanup.raise_for_status()
    print(cleanup.json())

    print("\nChecking service health...")
    health = requests.get(f"{BASE_URL}/health", timeout=10)
    health.raise_for_status()
    print(health.json())

    print("\nLoading example logs...")
    with open("example_logs.json", "r", encoding="utf-8") as file:
        example_logs = json.load(file)

    print(f"Sending {len(example_logs)} example logs...")
    for log in example_logs:
        result = send_log(log)
        print(result)

    print("\nChecking metrics...")
    metrics = requests.get(f"{BASE_URL}/metrics", timeout=10)
    metrics.raise_for_status()
    print(metrics.json())

    print("\nChecking alerts...")
    alerts = requests.get(f"{BASE_URL}/alerts", timeout=10)
    alerts.raise_for_status()
    print(alerts.json())


if __name__ == "__main__":
    main()