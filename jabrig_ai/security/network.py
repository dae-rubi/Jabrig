from __future__ import annotations

from urllib.parse import urlparse


class SSRFGuard:
    """Reject obvious SSRF targets such as localhost and private network addresses."""

    def is_allowed(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
        except ValueError:
            return False

        host = parsed.hostname or ""
        if not host:
            return False

        host_lower = host.lower()
        blocked = {
            "localhost",
            "127.0.0.1",
            "::1",
            "169.254.169.254",
            "0.0.0.0",
            "10.",
            "172.",
            "192.168.",
        }

        if host_lower == "localhost":
            return False
        if host_lower.startswith("127.") or host_lower.startswith("::1"):
            return False
        if host_lower.startswith("10.") or host_lower.startswith("192.168."):
            return False
        if host_lower.startswith("172."):
            parts = host_lower.split(".")
            if len(parts) >= 2 and parts[1].isdigit():
                try:
                    if 16 <= int(parts[1]) <= 31:
                        return False
                except ValueError:
                    pass
        if host_lower.startswith("169.254."):
            return False

        return True
