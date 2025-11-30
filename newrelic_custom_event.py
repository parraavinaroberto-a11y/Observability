import os
import time
import json
import requests
from typing import Dict

NEW_RELIC_INSERT_KEY = os.getenv("NEW_RELIC_INSERT_KEY")
NEW_RELIC_ACCOUNT_ID = os.getenv("NEW_RELIC_ACCOUNT_ID")  # Ej: "1234567"

NEW_RELIC_EVENTS_URL = (
    f"https://insights-collector.newrelic.com/v1/accounts/{NEW_RELIC_ACCOUNT_ID}/events"
)


def send_custom_event(event_type: str, attributes: Dict):
    if not NEW_RELIC_INSERT_KEY or not NEW_RELIC_ACCOUNT_ID:
        raise RuntimeError("Faltan NEW_RELIC_INSERT_KEY o NEW_RELIC_ACCOUNT_ID")

    headers = {
        "Content-Type": "application/json",
        "Api-Key": NEW_RELIC_INSERT_KEY,
    }

    payload = {
        "eventType": event_type,
        "timestamp": int(time.time() * 1000),
        **attributes,
    }

    resp = requests.post(NEW_RELIC_EVENTS_URL, headers=headers, data=json.dumps(payload))
    resp.raise_for_status()
    return resp.status_code


if __name__ == "__main__":
    os.environ.setdefault("NEW_RELIC_ACCOUNT_ID", "TU_ACCOUNT_ID")
    os.environ.setdefault("NEW_RELIC_INSERT_KEY", "TU_INSERT_KEY")

    status = send_custom_event(
        "PythonObservabilityEvent",
        {
            "serviceName": "python-demo-service",
            "env": "dev",
            "latency_ms": 123,
            "success": True,
        },
    )
    print(f"Evento enviado a New Relic con status HTTP {status}")
