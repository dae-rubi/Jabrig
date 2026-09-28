from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Any


class DatabaseAdapter:
    """SQLite-backed persistence adapter for JABRIG local state and future Postgres migration."""

    def __init__(self, db_path: str | None = None) -> None:
        self.db_path = db_path or os.environ.get("JABRIG_DB_PATH") or ":memory:"
        self._ensure_parent_dir()
        self._conn = sqlite3.connect(self.db_path)
        self._conn.row_factory = sqlite3.Row
        self._initialize()

    def _ensure_parent_dir(self) -> None:
        if self.db_path == ":memory:":
            return
        parent = Path(self.db_path).parent
        if parent and not parent.exists():
            parent.mkdir(parents=True, exist_ok=True)

    def _connect(self) -> sqlite3.Connection:
        return self._conn

    def _initialize(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    status TEXT,
                    user_input TEXT,
                    metadata TEXT,
                    name TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS task_steps (
                    id TEXT PRIMARY KEY,
                    task_id TEXT,
                    description TEXT,
                    status TEXT,
                    metadata TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS events (
                    id TEXT PRIMARY KEY,
                    name TEXT,
                    data TEXT,
                    task_id TEXT,
                    user_id TEXT,
                    created_at TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS memory_items (
                    id TEXT PRIMARY KEY,
                    namespace TEXT,
                    content TEXT,
                    metadata TEXT,
                    ttl_seconds INTEGER,
                    created_at TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS skills (
                    name TEXT PRIMARY KEY,
                    description TEXT,
                    risk TEXT,
                    requires TEXT,
                    metadata TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS plugins (
                    name TEXT PRIMARY KEY,
                    type TEXT,
                    manifest TEXT,
                    permissions TEXT,
                    tools TEXT,
                    metadata TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS capabilities (
                    name TEXT PRIMARY KEY,
                    type TEXT,
                    description TEXT,
                    risk TEXT,
                    permissions TEXT,
                    metadata TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS permissions (
                    id TEXT PRIMARY KEY,
                    action TEXT,
                    reason TEXT,
                    risk TEXT,
                    status TEXT,
                    metadata TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS audit_logs (
                    id TEXT PRIMARY KEY,
                    action TEXT,
                    payload TEXT,
                    created_at TEXT
                )
                """
            )
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS sessions (
                    id TEXT PRIMARY KEY,
                    user_id TEXT,
                    metadata TEXT,
                    created_at TEXT
                )
                """
            )
            conn.commit()

    def _serialize_value(self, value: Any) -> str:
        return json.dumps(value, default=str)

    async def insert(self, table: str, record: dict[str, Any]) -> dict[str, Any]:
        columns = [key for key in record.keys()]
        placeholders = ", ".join(["?"] * len(columns))
        values = [record[column] for column in columns]

        with self._connect() as conn:
            self._ensure_columns(conn, table, columns)
            conn.execute(
                f"INSERT OR REPLACE INTO {table} ({', '.join(columns)}) VALUES ({placeholders})",
                values,
            )
            conn.commit()
        return record

    def _ensure_columns(self, conn: sqlite3.Connection, table: str, columns: list[str]) -> None:
        if table not in {"tasks", "task_steps", "events", "memory_items", "skills", "plugins", "capabilities", "permissions", "audit_logs", "sessions"}:
            return

        existing = conn.execute(f"PRAGMA table_info({table})").fetchall()
        current = {row[1] for row in existing}
        for column in columns:
            if column not in current:
                conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} TEXT")

    async def fetch(self, table: str, limit: int = 20, filters: dict[str, Any] | None = None) -> list[dict[str, Any]]:
        filters = filters or {}
        clauses = []
        params: list[Any] = []
        for key, value in filters.items():
            clauses.append(f"{key} = ?")
            params.append(value)

        query = f"SELECT * FROM {table}"
        if clauses:
            query += " WHERE " + " AND ".join(clauses)
        query += " LIMIT ?"
        params.append(limit)

        with self._connect() as conn:
            rows = conn.execute(query, params).fetchall()
        return [dict(row) for row in rows]

    async def update(self, table: str, match: dict[str, Any], values: dict[str, Any]) -> dict[str, Any]:
        if not match:
            raise ValueError("match criteria required for update")

        set_clauses = ", ".join(f"{key} = ?" for key in values.keys())
        where_clauses = " AND ".join(f"{key} = ?" for key in match.keys())
        params = list(values.values()) + list(match.values())

        with self._connect() as conn:
            conn.execute(
                f"UPDATE {table} SET {set_clauses} WHERE {where_clauses}",
                params,
            )
            conn.commit()

        return {**match, **values}
