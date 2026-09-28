from __future__ import annotations

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


def collect_health_snapshot() -> dict[str, Any]:
    checks = [
        HealthCheckReport("core", HealthStatus.HEALTHY, {"service": "jabrig-ai"}),
        HealthCheckReport("database", HealthStatus.DEGRADED, {"detail": "sqlite-memory-ready"}),
        HealthCheckReport("redis", HealthStatus.DEGRADED, {"detail": "not-connected"}),
    ]
    return {
        "status": "healthy" if all(item.status == HealthStatus.HEALTHY for item in checks) else "degraded",
        "checks": [
            {"name": item.name, "status": item.status.value, "details": item.details}
            for item in checks
        ],
    }
