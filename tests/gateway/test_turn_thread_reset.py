import sys
import threading
import types

from gateway.turn_thread_reset import reset_reused_thread_state


def test_reset_skips_partially_imported_sudo_module():
    partial = types.ModuleType("tools.terminal_tool_sudo")
    partial._sudo_password_cache = {"thread:1": "old"}
    old = sys.modules.get("tools.terminal_tool_sudo")
    sys.modules["tools.terminal_tool_sudo"] = partial
    try:
        assert reset_reused_thread_state() is None
    finally:
        if old is None:
            sys.modules.pop("tools.terminal_tool_sudo", None)
        else:
            sys.modules["tools.terminal_tool_sudo"] = old
