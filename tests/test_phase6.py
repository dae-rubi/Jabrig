import pytest

from jabrig_ai.browser.browser_service import BrowserService
from jabrig_ai.browser.browser_bridge import BrowserBridge


@pytest.mark.asyncio
async def test_browser_service_has_required_capabilities():
    service = BrowserService()
    for capability in [
        "browser.open",
        "browser.search",
        "browser.click",
        "browser.type",
        "browser.scroll",
        "browser.extract",
        "browser.screenshot",
        "browser.tabs",
        "browser.close",
    ]:
        assert capability in service.capabilities


@pytest.mark.asyncio
async def test_browser_bridge_requires_authentication_for_browser_endpoints():
    bridge = BrowserBridge()
    payload = {"url": "https://example.com"}
    result = bridge.validate_request(payload, auth_token=None)
    assert result["authorized"] is False

    auth_result = bridge.validate_request(payload, auth_token="token")
    assert auth_result["authorized"] is True
