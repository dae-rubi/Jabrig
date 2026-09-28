import pytest

from jabrig_ai.security.network import SSRFGuard
from jabrig_ai.security.permissions import PermissionManager
from jabrig_ai.security.rate_limit import RateLimiter


def test_ssrf_guard_blocks_private_network_targets():
    guard = SSRFGuard()

    assert guard.is_allowed("https://example.com") is True
    assert guard.is_allowed("http://localhost:3000") is False
    assert guard.is_allowed("http://127.0.0.1:8000") is False
    assert guard.is_allowed("http://169.254.169.254/latest/meta-data") is False


def test_permission_manager_grants_and_checks_permissions():
    manager = PermissionManager()
    manager.grant("browser.read", "research")
    manager.grant("filesystem.write", "reporting")

    assert manager.check("browser.read", "research") is True
    assert manager.check("filesystem.write", "research") is False
    assert manager.check("unknown", "research") is False


def test_rate_limiter_blocks_excess_requests():
    limiter = RateLimiter(limit=2, window_seconds=60)

    assert limiter.allow("user-1") is True
    assert limiter.allow("user-1") is True
    assert limiter.allow("user-1") is False
