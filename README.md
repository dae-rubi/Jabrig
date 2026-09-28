# Jabrig

Jabrig AI assistant.

## Local infrastructure

The project includes a local PostgreSQL and Redis stack for development.

```bash
cp .env.example .env
docker compose up -d
```

## Quick start

```bash
python -m pip install -e .
uvicorn jabrig_ai.core.app:app --host 0.0.0.0 --port 8000
```

Environment variables:

- POSTGRES_HOST
- POSTGRES_PORT
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- REDIS_URL

This configuration is consumed by the runtime settings in `jabrig_ai/config.py`.
