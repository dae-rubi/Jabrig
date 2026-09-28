# Jabrig

Jabrig is a modular AI operating-system scaffold built with FastAPI, provider adapters, routing, browser tooling, security guards, and local infrastructure helpers.

## Prerequisites

- Python 3.12+
- pip
- Docker and Docker Compose (for local Postgres/Redis)

## 1) Clone and install

```bash
git clone https://github.com/dae-rubi/Jabrig.git
cd Jabrig
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e .
```

## 2) Configure environment

Copy the example environment file and adjust values as needed:

```bash
cp .env.example .env
```

Key variables include:

- APP_ENV
- LOG_LEVEL
- POSTGRES_HOST
- POSTGRES_PORT
- POSTGRES_DB
- POSTGRES_USER
- POSTGRES_PASSWORD
- REDIS_URL
- Optional model-provider keys such as OPENAI_API_KEY, OPENROUTER_API_KEY, and others used by the provider registry

## 3) Start local infrastructure

This project includes a local Postgres and Redis stack for development:

```bash
docker compose up -d
```

## 4) Run the app

Start the API server:

```bash
uvicorn jabrig_ai.core.app:app --host 0.0.0.0 --port 8000 --reload
```

The main endpoints include:

- http://localhost:8000/health
- http://localhost:8000/ready
- http://localhost:8000/version

If you want to use the authenticated API gateway, the app is also exposed via the API entry point in `jabrig_ai/api/app.py`.

## 5) Run tests

```bash
pytest -q
```

## Project layout

- `jabrig_ai/core/` - runtime core, domain models, planner, executor, policy, verifier
- `jabrig_ai/providers/` - provider registry and gateway adapters
- `jabrig_ai/routing/` - capability matching and routing logic
- `jabrig_ai/security/` - auditing, redaction, permissions, rate limit, and SSRF controls
- `jabrig_ai/storage/` - SQLite persistence layer and migration-safe schema handling
- `jabrig_ai/tools/` - filesystem, terminal, and computer integrations
- `config/` - configuration defaults
- `tests/` - project validation and regression coverage

This configuration is consumed by the runtime settings in `jabrig_ai/config.py`.
