import React, { useState, useEffect, useRef } from "react";
import { CopyIcon } from "./components/icons";

const PROCESSES = ["sam", "proxy", "tunnel", "build"];

function LogPanel({ label, lines }) {
  const ref = useRef(null);

  useEffect(() => {
    if (ref.current) ref.current.scrollTop = ref.current.scrollHeight;
  }, [lines]);

  return (
    <div className="detail-log-panel">
      <div className="detail-log-label">{label}</div>
      <div ref={ref} className="detail-log-pane">
        {lines.length === 0
          ? <span className="log-empty">— no output —</span>
          : lines.map((line, i) => <div key={i} className="log-line">{line}</div>)
        }
      </div>
    </div>
  );
}

export default function ServiceDetail({ service, onBack, onStart, onStop, onRestart, onBuild, onClean }) {
  const { name, sam_port, proxy_port, status, tunnel_url } = service;
  const [logs, setLogs] = useState({ sam: [], proxy: [], tunnel: [], build: [] });
  const disabled = status === "building";

  useEffect(() => {
    const proto = window.location.protocol === "https:" ? "wss" : "ws";
    const ws = new WebSocket(`${proto}://${window.location.host}/ws/logs/${name}`);
    ws.onmessage = (e) => {
      const msg = JSON.parse(e.data);
      setLogs((prev) => {
        const key = msg.process in prev ? msg.process : "sam";
        return { ...prev, [key]: [...prev[key].slice(-499), msg.line] };
      });
    };
    return () => ws.close();
  }, [name]);

  return (
    <div className="app">
      <button className="detail-back" onClick={onBack}>
        <svg width="12" height="12" viewBox="0 0 12 12" fill="none" stroke="currentColor" strokeWidth="1.8" strokeLinecap="round" strokeLinejoin="round">
          <path d="M8 1L3 6l5 5" />
        </svg>
        All services
      </button>

      <div className="detail-header">
        <div className="detail-title">
          <span className="app-title-mark" style={{ fontSize: 18 }}>⬡</span>
          <span className="detail-name">{name}</span>
          <span className="card-ports" style={{ fontSize: 12, alignSelf: "flex-end", marginBottom: 2 }}>
            :{sam_port} → :{proxy_port}
          </span>
        </div>
        <span className={`status-badge ${status}`} style={{ fontSize: 11, padding: "3px 9px" }}>
          {status === "building" ? "building…" : status}
        </span>
      </div>

      {tunnel_url && (
        <div style={{ marginTop: 6, marginBottom: 16 }}>
          <a href={tunnel_url} target="_blank" rel="noreferrer" className="tunnel-link" style={{ fontSize: 12 }}>
            {tunnel_url}
          </a>
          <button className="btn-copy" onClick={() => navigator.clipboard.writeText(tunnel_url)} title="Copy tunnel URL">
            <CopyIcon />
          </button>
        </div>
      )}

      <div className="detail-actions">
        <button className="btn btn-start" disabled={disabled} onClick={onStart}>Start</button>
        <button className="btn" disabled={disabled} onClick={onStop}>Stop</button>
        <button className="btn" disabled={disabled} onClick={onRestart}>Restart</button>
        <button className="btn" disabled={disabled} onClick={onBuild}>
          {status === "building" ? "Building…" : "Build"}
        </button>
        <button className="btn btn-danger" disabled={disabled} onClick={onClean}>Clean</button>
      </div>

      <div className="detail-log-grid">
        {PROCESSES.map((p) => (
          <LogPanel key={p} label={p} lines={logs[p]} />
        ))}
      </div>
    </div>
  );
}
