from __future__ import annotations


class PermissionManager:
    """Simple permission registry keyed by entity and action."""

    def __init__(self) -> None:
        self._grants: dict[str, set[str]] = {}

    def grant(self, permission: str, subject: str) -> None:
        self._grants.setdefault(subject, set()).add(permission)

    def check(self, permission: str, subject: str) -> bool:
        return permission in self._grants.get(subject, set())
