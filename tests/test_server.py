import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport

def test_get_services_returns_list(tmp_path, monkeypatch):
    services_data = {
        "services": [
            {"name": "email-bot", "sam_port": 3001, "proxy_port": 8080, "function_name": "FunctionImp"},
            {"name": "utils", "sam_port": 3005, "proxy_port": 8084, "function_name": "FunctionImp"},
        ]
    }
    svc_file = tmp_path / "services.json"
    svc_file.write_text(json.dumps(services_data))

    env_file = tmp_path / ".overmind.env"
    env_file.write_text("BACKEND_PATH=/tmp/backend\nDEV_PATH=/tmp/dev\n")

    monkeypatch.chdir(tmp_path)
    import importlib, sys
    sys.modules.pop("server", None)
    import server
    importlib.reload(server)

    client = TestClient(server.app)
    resp = client.get("/api/services")
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 2
    assert data[0]["name"] == "email-bot"
    assert data[0]["sam_port"] == 3001
    assert data[0]["proxy_port"] == 8080
    assert data[0]["status"] == "stopped"
    assert data[0]["tunnel_url"] is None


def _setup_files(tmp_path, monkeypatch):
    services_data = {
        "services": [
            {"name": "email-bot", "sam_port": 3001, "proxy_port": 8080, "function_name": "FunctionImp"},
        ]
    }
    (tmp_path / "services.json").write_text(json.dumps(services_data))
    (tmp_path / ".overmind.env").write_text("BACKEND_PATH=/tmp/b\nDEV_PATH=/tmp/d\n")
    monkeypatch.chdir(tmp_path)


def test_stop_unknown_service_returns_404(monkeypatch, tmp_path):
    _setup_files(tmp_path, monkeypatch)
    import importlib, sys
    sys.modules.pop("server", None)
    import server
    importlib.reload(server)
    client = TestClient(server.app)
    resp = client.post("/api/services/nonexistent/stop")
    assert resp.status_code == 404


def test_start_unknown_service_returns_404(monkeypatch, tmp_path):
    _setup_files(tmp_path, monkeypatch)
    import importlib, sys
    sys.modules.pop("server", None)
    import server
    importlib.reload(server)
    client = TestClient(server.app)
    resp = client.post("/api/services/nonexistent/start")
    assert resp.status_code == 404


def test_build_unknown_service_returns_404(monkeypatch, tmp_path):
    _setup_files(tmp_path, monkeypatch)
    import importlib, sys
    sys.modules.pop("server", None)
    import server
    importlib.reload(server)
    client = TestClient(server.app)
    resp = client.post("/api/services/nonexistent/build")
    assert resp.status_code == 404

def test_websocket_log_replay(monkeypatch, tmp_path):
    _setup_files(tmp_path, monkeypatch)
    import importlib, sys
    sys.modules.pop("server", None)
    import server
    importlib.reload(server)
    # seed the buffer
    server.LOG_BUFFER["email-bot"].append({"process": "sam", "line": "hello"})
    client = TestClient(server.app)
    with client.websocket_connect("/ws/logs/email-bot") as ws:
        msg = ws.receive_json()
        assert msg == {"process": "sam", "line": "hello"}


def test_kill_ports_unknown_service_returns_404(monkeypatch, tmp_path):
    _setup_files(tmp_path, monkeypatch)
    import importlib, sys
    sys.modules.pop("server", None)
    import server
    importlib.reload(server)
    client = TestClient(server.app)
    resp = client.post("/api/services/nonexistent/kill-ports")
    assert resp.status_code == 404


def test_kill_ports_known_service_returns_ok(monkeypatch, tmp_path):
    _setup_files(tmp_path, monkeypatch)
    import importlib, sys
    sys.modules.pop("server", None)
    import server
    importlib.reload(server)

    async def async_lines():
        yield b"killed port 3001 8080\n"

    async def fake_exec(*args, **kwargs):
        mock_proc = AsyncMock()
        mock_proc.stdout = async_lines()
        mock_proc.wait = AsyncMock(return_value=0)
        return mock_proc

    with patch("asyncio.create_subprocess_exec", side_effect=fake_exec):
        client = TestClient(server.app)
        resp = client.post("/api/services/email-bot/kill-ports")
    assert resp.status_code == 200
    assert resp.json()["ok"] is True


@pytest.mark.anyio
async def test_kill_ports_logs_emitted(monkeypatch, tmp_path):
    _setup_files(tmp_path, monkeypatch)
    import importlib, sys
    sys.modules.pop("server", None)
    import server
    importlib.reload(server)

    async def async_lines():
        yield b"killed port 3001 8080\n"

    async def fake_exec(*args, **kwargs):
        mock_proc = AsyncMock()
        mock_proc.stdout = async_lines()
        mock_proc.wait = AsyncMock(return_value=0)
        return mock_proc

    with patch("asyncio.create_subprocess_exec", side_effect=fake_exec):
        async with AsyncClient(transport=ASGITransport(app=server.app), base_url="http://test") as ac:
            resp = await ac.post("/api/services/email-bot/kill-ports")
        await asyncio.sleep(0)  # drain inside the patch so the background task runs with the mock
    assert resp.status_code == 200
    assert {"process": "build", "line": "killed port 3001 8080"} in list(server.LOG_BUFFER["email-bot"])


@pytest.mark.anyio
async def test_restart_service_only_sam_retains_tunnel_url(monkeypatch, tmp_path):
    _setup_files(tmp_path, monkeypatch)
    import importlib, sys
    sys.modules.pop("server", None)
    import server
    importlib.reload(server)

    class MockStreamReader:
        def __init__(self, lines):
            self._lines = lines
            self._index = 0

        async def readline(self):
            if self._index < len(self._lines):
                line = self._lines[self._index]
                self._index += 1
                return line
            return b'' # EOF

    # Mock subprocess execution for SAM, proxy, and tunnel
    mock_sam_proc = AsyncMock()
    mock_sam_proc.stdout = MockStreamReader([b"SAM output\n"])
    mock_sam_proc.wait = AsyncMock(return_value=0)
    mock_sam_proc.terminate = MagicMock()
    mock_sam_proc.kill = MagicMock()

    mock_proxy_proc = AsyncMock()
    mock_proxy_proc.stdout = MockStreamReader([b"Proxy output\n"])
    mock_proxy_proc.wait = AsyncMock(return_value=0)
    mock_proxy_proc.terminate = MagicMock()
    mock_proxy_proc.kill = MagicMock()

    mock_tunnel_proc = AsyncMock()
    mock_tunnel_proc.stdout = MockStreamReader([
        b"cloudflared output: https://test-tunnel.trycloudflare.com\n"
    ])
    mock_tunnel_proc.wait = AsyncMock(return_value=0)
    mock_tunnel_proc.terminate = MagicMock()
    mock_tunnel_proc.kill = MagicMock()

    # Use a side effect to return different mocks for different commands
    def fake_exec(*args, **kwargs):
        command = args[0]
        if "sam" in command:
            return mock_sam_proc
        elif "python3" in command and "proxy.py" in args[1]:
            return mock_proxy_proc
        elif "cloudflared" in command:
            return mock_tunnel_proc
        raise ValueError(f"Unexpected command: {command}")

    with patch("asyncio.create_subprocess_exec", side_effect=fake_exec) as mock_create_subprocess_exec:
        async with AsyncClient(transport=ASGITransport(app=server.app), base_url="http://test") as ac:
            # 1. Start the service initially
            resp = await ac.post("/api/services/email-bot/start")
            assert resp.status_code == 200
            await asyncio.sleep(0.1) # Allow background tasks to run
            initial_tunnel_url = server.TUNNEL_URLS.get("email-bot")
            assert initial_tunnel_url == "https://test-tunnel.trycloudflare.com"

            # Reset mocks for restart, but keep tunnel mock state
            mock_create_subprocess_exec.reset_mock()
            mock_sam_proc.reset_mock()
            mock_proxy_proc.reset_mock()
            mock_tunnel_proc.reset_mock()

            # 2. Call the new restart-sam-only endpoint
            resp = await ac.post("/api/services/email-bot/restart-sam-only")
            assert resp.status_code == 200
            await asyncio.sleep(0.1) # Allow background tasks to run

            # Assert that SAM and proxy were restarted (stopped and started)
            # The mock_create_subprocess_exec should have been called twice: once for sam, once for proxy
            assert mock_create_subprocess_exec.call_count == 2
            # Assert that the tunnel URL remains the same
            current_tunnel_url = server.TUNNEL_URLS.get("email-bot")
            assert current_tunnel_url == initial_tunnel_url
