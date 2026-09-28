from __future__ import annotations

import os
from typing import Any


class FilesystemTool:
    """Filesystem tool with canonical path validation and allowed root enforcement."""

    def __init__(self, allowed_roots: list[str] | None = None) -> None:
        self.allowed_roots = [os.path.abspath(path) for path in (allowed_roots or ["./workspace", "./projects"])]

    async def read(self, path: str) -> dict[str, Any]:
        canonical = os.path.abspath(path)
        if not self._is_allowed(canonical):
            return {"status": "denied", "reason": "Path traversal or outside allowed roots."}
        return {"status": "ok", "path": canonical, "content": "example-content"}

    async def write(self, path: str, content: str) -> dict[str, Any]:
        canonical = os.path.abspath(path)
        if not self._is_allowed(canonical):
            return {"status": "denied", "reason": "Path traversal or outside allowed roots."}
        return {"status": "ok", "path": canonical, "bytes_written": len(content.encode())}

    def _is_allowed(self, path: str) -> bool:
        resolved = os.path.realpath(path)
        return any(os.path.commonpath([resolved, root]) == root for root in self.allowed_roots)
