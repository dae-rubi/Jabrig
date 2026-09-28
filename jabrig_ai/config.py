from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Mapping


@dataclass
class PostgreSQLSettings:
    host: str = "localhost"
    port: int = 5432
    db: str = "jabrig"
    user: str = "jabrig"
    password: str = "jabrig"


@dataclass
class RuntimeSettings:
    app_env: str = "development"
    log_level: str = "INFO"
    postgres: PostgreSQLSettings = field(default_factory=PostgreSQLSettings)
    redis_url: str = "redis://localhost:6379/0"

    def __init__(self, env: Mapping[str, str] | None = None) -> None:
        source = dict(os.environ if env is None else env)
        self.app_env = source.get("APP_ENV", "development")
        self.log_level = source.get("LOG_LEVEL", "INFO")
        self.postgres = PostgreSQLSettings(
            host=source.get("POSTGRES_HOST", "localhost"),
            port=int(source.get("POSTGRES_PORT", "5432")),
            db=source.get("POSTGRES_DB", "jabrig"),
            user=source.get("POSTGRES_USER", "jabrig"),
            password=source.get("POSTGRES_PASSWORD", "jabrig"),
        )
        self.redis_url = source.get("REDIS_URL", "redis://localhost:6379/0")


__all__ = ["RuntimeSettings", "PostgreSQLSettings"]
