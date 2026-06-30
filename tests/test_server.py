import asyncio
import json
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from fastapi.testclient import TestClient

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
