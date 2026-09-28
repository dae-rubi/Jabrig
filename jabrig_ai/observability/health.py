from __future__ import annotations

import os
import socket
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class HealthStatus(str, Enum):
    HEALTHY = "healthy"
    DEGRADED = "degraded"
    UNHEALTHY = "unhealthy"


@dataclass
class HealthCheckReport:
    name: str
    status: HealthStatus = HealthStatus.HEALTHY
    details: dict[str, Any] = field(default_factory=dict)


def _tcp_connect(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


def collect_health_snapshot() -> dict[str, Any]:
    checks = [
        HealthCheckReport("core", HealthStatus.HEALTHY, {"service": "jabrig-ai"}),
    ]

    db_host = os.getenv("POSTGRES_HOST", "localhost")
    db_port = int(os.getenv("POSTGRES_PORT", "5432"))
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    database_ok = _tcp_connect(db_host, db_port)
    checks.append(
        HealthCheckReport(
            "database",
            HealthStatus.HEALTHY if database_ok else HealthStatus.DEGRADED,
            {"detail": "postgres-reachable" if database_ok else "postgres-not-connected"},
        )
    )

    try:
        from urllib.parse import urlparse

        parsed = urlparse(redis_url)
        redis_host = parsed.hostname or "localhost"
        redis_port = parsed.port or 6379
        redis_ok = _tcp_connect(redis_host, redis_port)
    except Exception:
        redis_ok = False

    checks.append(
        HealthCheckReport(
            "redis",
            HealthStatus.HEALTHY if redis_ok else HealthStatus.DEGRADED,
            {"detail": "redis-reachable" if redis_ok else "redis-not-connected"},
        )
    )

    return {
        "status": "healthy" if all(item.status == HealthStatus.HEALTHY for item in checks) else "degraded",
        "checks": [
            {"name": item.name, "status": item.status.value, "details": item.details}
            for item in checks
        ],
    }
