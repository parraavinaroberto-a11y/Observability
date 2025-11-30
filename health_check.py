import json
import socket
import sys
import time
from typing import Dict

import requests


def check_tcp(host: str, port: int, timeout: float = 2.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def check_http(url: str, timeout: float = 2.0) -> bool:
    try:
        resp = requests.get(url, timeout=timeout)
        return 200 <= resp.status_code < 300
    except requests.RequestException:
        return False


def run_health_checks() -> Dict:
    results = {
        "timestamp": time.time(),
        "checks": {
            "db_tcp": check_tcp("localhost", 5432),
            "redis_tcp": check_tcp("localhost", 6379),
            "external_api": check_http("https://api.github.com/"),
        }
    }
    results["status"] = "UP" if all(results["checks"].values()) else "DOWN"
    return results


if __name__ == "__main__":
    health = run_health_checks()
    print(json.dumps(health))
    # exit code para orquestadores / monitoreo
    sys.exit(0 if health["status"] == "UP" else 1)
