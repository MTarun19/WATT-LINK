import React, { useState, useEffect } from "react";
import {
  Wifi,
  Cpu,
  BatteryCharging,
  Thermometer,
  Gauge,
  Power,
  Activity,
  CheckCircle2,
  RefreshCw,
  Zap,
  Terminal,
  ShieldCheck,
  Radio
} from "lucide-react";

import "./Sensors.css";

export default function Sensors() {
  const [lastUpdated, setLastUpdated] = useState(1);
  const [isRefreshing, setIsRefreshing] = useState(false);

  // Dynamic Telemetry States
  const [telemetry, setTelemetry] = useState({
    pzemVoltage: 230,
    pzemCurrent: 2.35,
    batterySoC: 82,
    temp: 31,
    humidity: 58,
    rssi: -48
  });

  // Relay Module States (4 Channels)
  const [relays, setRelays] = useState([
    { id: 1, name: "Relay 1 (Main Bus)", state: true },
    { id: 2, name: "Relay 2 (Solar Inverter)", state: true },
    { id: 3, name: "Relay 3 (P2P Transfer)", state: true },
    { id: 4, name: "Relay 4 (Aux Battery)", state: true }
  ]);

  // Live Activity Logs
  const [logs, setLogs] = useState([
    { id: 1, text: "ESP32 Gateway connected via MQTT broker", time: "10:45:00 AM", type: "success" },
    { id: 2, text: "PZEM-004T read: 230V / 2.35A (Power Factor: 0.98)", time: "10:44:52 AM", type: "info" },
    { id: 3, text: "INA219 Battery charge level verified at 82%", time: "10:44:30 AM", type: "info" },
    { id: 4, text: "DHT22 Climate Sensor stable (31°C / 58% RH)", time: "10:44:10 AM", type: "info" },
    { id: 5, text: "Relay Module 4/4 outputs engaged", time: "10:43:00 AM", type: "success" }
  ]);

  // Simulate periodic sensor fluctuation
  useEffect(() => {
    const interval = setInterval(() => {
      setTelemetry((prev) => ({
        ...prev,
        pzemVoltage: +(228 + Math.random() * 4).toFixed(1),
        pzemCurrent: +(2.3 + Math.random() * 0.15).toFixed(2),
        batterySoC: Math.min(100, Math.max(10, +(prev.batterySoC + (Math.random() * 0.1 - 0.03)).toFixed(1))),
        temp: +(30.5 + Math.random() * 1).toFixed(1),
        humidity: Math.floor(57 + Math.random() * 3)
      }));
      setLastUpdated(1);
    }, 4000);

    const timer = setInterval(() => {
      setLastUpdated((prev) => prev + 1);
    }, 1000);

    return () => {
      clearInterval(interval);
      clearInterval(timer);
    };
  }, []);

  const handleRefresh = () => {
    setIsRefreshing(true);
    setTimeout(() => {
      setIsRefreshing(false);
      setLastUpdated(1);
      const newLog = {
        id: Date.now(),
        text: "Manual telemetry pull requested from ESP32 node",
        time: new Date().toLocaleTimeString(),
        type: "info"
      };
      setLogs((prev) => [newLog, ...prev]);
    }, 600);
  };

  const toggleRelay = (id) => {
    setRelays((prev) =>
      prev.map((relay) => {
        if (relay.id === id) {
          const newState = !relay.state;
          const newLog = {
            id: Date.now(),
            text: `Command sent: ${relay.name} switched ${newState ? "ON" : "OFF"} via ESP32 GPIO`,
            time: new Date().toLocaleTimeString(),
            type: newState ? "success" : "warning"
          };
          setLogs((prevLogs) => [newLog, ...prevLogs]);
          return { ...relay, state: newState };
        }
        return relay;
      })
    );
  };

  const activeRelayCount = relays.filter((r) => r.state).length;

  const sensors = [
    {
      icon: <Cpu size={38} />,
      name: "ESP32 Controller",
      value: "Online",
      status: "Connected",
      color: "#22c55e",
      subtitle: "IP: 192.168.1.104"
    },
    {
      icon: <Gauge size={38} />,
      name: "PZEM-004T",
      value: `${telemetry.pzemVoltage} V / ${telemetry.pzemCurrent} A`,
      status: "Healthy",
      color: "#00d4ff",
      subtitle: `Power: ${(telemetry.pzemVoltage * telemetry.pzemCurrent).toFixed(0)} W`
    },
    {
      icon: <BatteryCharging size={38} />,
      name: "INA219 Battery",
      value: `${telemetry.batterySoC}%`,
      status: "Charging",
      color: "#22c55e",
      subtitle: "12.6V Lithium Bank"
    },
    {
      icon: <Thermometer size={38} />,
      name: "DHT22 Sensor",
      value: `${telemetry.temp}°C / ${telemetry.humidity}%`,
      status: "Normal",
      color: "#ffd43b",
      subtitle: "Ambient Environment"
    },
    {
      icon: <Power size={38} />,
      name: "Relay Module",
      value: `${activeRelayCount} / ${relays.length} Active`,
      status: activeRelayCount > 0 ? "Running" : "Standby",
      color: "#a855f7",
      subtitle: "Optocoupler Isolated"
    },
    {
      icon: <Wifi size={38} />,
      name: "MQTT Broker",
      value: "Connected",
      status: "Live",
      color: "#06b6d4",
      subtitle: "Latency: 14ms"
    }
  ];

  return (
    <div className="sensor-page">
      {/* Page Header */}
      <div className="sensor-header">
        <div>
          <h1>📡 IoT Telemetry Dashboard</h1>
          <p>Real-Time ESP32 Microgrid Hardware & Sensor Infrastructure</p>
        </div>
        <div className="header-actions">
          <button className={`refresh-btn ${isRefreshing ? "spin" : ""}`} onClick={handleRefresh}>
            <RefreshCw size={16} />
            Refresh Feed
          </button>
          <div className="live">
            <Activity className="live-pulse" size={18} />
            LIVE
          </div>
        </div>
      </div>

      {/* Summary KPI Cards */}
      <div className="summary">
        <div className="summary-card">
          <h2>Connected Nodes</h2>
          <span>6 / 6</span>
        </div>
        <div className="summary-card">
          <h2>System Health</h2>
          <span className="cyan-text">100%</span>
        </div>
        <div className="summary-card">
          <h2>Network Link</h2>
          <span className="green-text">Wi-Fi Stable</span>
        </div>
        <div className="summary-card">
          <h2>Last Update</h2>
          <span>{lastUpdated}s ago</span>
        </div>
      </div>

      {/* Sensor Nodes Grid */}
      <div className="sensor-grid">
        {sensors.map((sensor, index) => (
          <div className="sensor-card" key={index}>
            <div className="sensor-card-top">
              <div className="sensor-icon" style={{ color: sensor.color }}>
                {sensor.icon}
              </div>
              <span className="sensor-subtitle">{sensor.subtitle}</span>
            </div>
            <h2>{sensor.name}</h2>
            <h1>{sensor.value}</h1>
            <div className="status">
              <CheckCircle2 color="#22c55e" size={16} />
              {sensor.status}
            </div>
          </div>
        ))}
      </div>

      {/* Interactive Relay Controls & Live Logs Grid */}
      <div className="bottom-grid">
        {/* Interactive Relay Control Panel */}
        <div className="panel">
          <h2>
            <Zap size={22} color="#00d4ff" /> Hardware Relay Switches
          </h2>
          <p className="panel-desc">Direct GPIO state overrides for microgrid power distribution isolation.</p>

          <div className="relay-list">
            {relays.map((relay) => (
              <div key={relay.id} className="relay-item">
                <div className="relay-info">
                  <span className={`relay-indicator ${relay.state ? "on" : "off"}`}></span>
                  <span className="relay-name">{relay.name}</span>
                </div>
                <button
                  className={`relay-toggle-btn ${relay.state ? "btn-on" : "btn-off"}`}
                  onClick={() => toggleRelay(relay.id)}
                >
                  {relay.state ? "ENABLED" : "DISABLED"}
                </button>
              </div>
            ))}
          </div>
        </div>

        {/* Live Terminal Sensor Stream */}
        <div className="panel">
          <h2>
            <Terminal size={22} color="#00d4ff" /> Live Hardware Terminal
          </h2>
          <ul className="log-list">
            {logs.map((log) => (
              <li key={log.id} className={`log-item log-${log.type}`}>
                <Radio size={14} className="log-icon" />
                <span className="log-timestamp">[{log.time}]</span>
                <span className="log-content">{log.text}</span>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Hardware System Info Table */}
      <div className="panel info-panel">
        <h2>
          <ShieldCheck size={22} color="#00d4ff" /> ESP32 Firmware & Communication Stack
        </h2>
        <div className="table-wrapper">
          <table>
            <tbody>
              <tr>
                <td><strong>Microcontroller</strong></td>
                <td>ESP32-WROOM-32 (Dual-Core 240MHz)</td>
                <td><strong>Firmware Version</strong></td>
                <td>v1.0.4-production</td>
              </tr>
              <tr>
                <td><strong>Wi-Fi SSID</strong></td>
                <td>PayNet_Wi-Fi_Hub</td>
                <td><strong>RSSI Signal</strong></td>
                <td>{telemetry.rssi} dBm (Excellent)</td>
              </tr>
              <tr>
                <td><strong>Primary Protocol</strong></td>
                <td>MQTT over TLS (Port 8883)</td>
                <td><strong>Backend Gateway</strong></td>
                <td>FastAPI Microservice Engine</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}