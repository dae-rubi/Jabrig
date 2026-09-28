import pytest

from jabrig_ai.tools.filesystem import FilesystemTool
from jabrig_ai.tools.terminal import TerminalTool
from jabrig_ai.tools.computer import ComputerAdapter


@pytest.mark.asyncio
async def test_filesystem_tool_restricts_path_traversal():
    tool = FilesystemTool(allowed_roots=["/tmp/jabrig-safe"])
    blocked = await tool.read("../../etc/passwd")
    assert blocked["status"] == "denied"


@pytest.mark.asyncio
async def test_terminal_tool_blocks_dangerous_commands():
    tool = TerminalTool()
    result = await tool.execute("rm -rf /")
    assert result["status"] == "denied"


@pytest.mark.asyncio
async def test_computer_adapter_supports_platform_adapters():
    adapter = ComputerAdapter()
    assert hasattr(adapter, "platform_adapters")
    assert "linux" in adapter.platform_adapters
