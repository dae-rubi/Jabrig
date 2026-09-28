from __future__ import annotations

from pathlib import Path

from jabrig_ai.config import RuntimeSettings


def test_runtime_settings_reads_environment(monkeypatch):
    monkeypatch.setenv("APP_ENV", "production")
    monkeypatch.setenv("LOG_LEVEL", "DEBUG")
    monkeypatch.setenv("POSTGRES_HOST", "db")
    monkeypatch.setenv("POSTGRES_PORT", "5432")
    monkeypatch.setenv("POSTGRES_DB", "jabrig")
    monkeypatch.setenv("POSTGRES_USER", "jabrig")
    monkeypatch.setenv("POSTGRES_PASSWORD", "secret")
    monkeypatch.setenv("REDIS_URL", "redis://redis:6379/0")

    settings = RuntimeSettings()

    assert settings.app_env == "production"
    assert settings.log_level == "DEBUG"
    assert settings.postgres.host == "db"
    assert settings.postgres.port == 5432
    assert settings.redis_url == "redis://redis:6379/0"


def test_compose_file_declares_postgres_and_redis():
    compose = Path("docker-compose.yml").read_text()

    assert "postgres" in compose.lower()
    assert "redis" in compose.lower()
