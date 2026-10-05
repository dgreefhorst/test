"""Minimal stdio smoke test for server.py (no MCP client dependency)."""

import json
import subprocess
import sys

proc = subprocess.Popen(
    [sys.executable, "server.py"],
    stdin=subprocess.PIPE,
    stdout=subprocess.PIPE,
    text=True,
)


def send(message: dict) -> None:
    proc.stdin.write(json.dumps(message) + "\n")
    proc.stdin.flush()


def recv() -> dict:
    return json.loads(proc.stdout.readline())


send(
    {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "smoke-test", "version": "0.1.0"},
        },
    }
)
print("initialize:", recv())

send({"jsonrpc": "2.0", "method": "notifications/initialized"})

send({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
print("tools/list:", recv())

send(
    {
        "jsonrpc": "2.0",
        "id": 3,
        "method": "tools/call",
        "params": {"name": "hello", "arguments": {"name": "Daan"}},
    }
)
print("tools/call:", recv())

proc.terminate()
proc.wait(timeout=5)
