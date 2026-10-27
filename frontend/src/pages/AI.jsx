import React, { useState } from "react";
import {
  Cpu,
  BatteryCharging,
  AlertTriangle,
  ShieldCheck,
  TrendingUp,
  Zap,
  CheckCircle2,
  Clock,
  ArrowRight,
  Terminal,
  Activity
} from "lucide-react";
import "./AI.css";

export default function AI() {
  const [selectedAgent, setSelectedAgent] = useState(null);
  const [tradeAccepted, setTradeAccepted] = useState(false);
  const [logs, setLogs] = useState([
    { id: 1, text: "Forecast Agent updated solar prediction to +5.2kW.", time: "10:42:05 AM", type: "info" },
    { id: 2, text: "Trading Agent matched buyer: Villa 104 @ 2.5 kWh.", time: "10:41:50 AM", type: "info" },
    { id: 3, text: "Battery Agent verified health & depth of discharge (SoC: 82%).", time: "10:40:12 AM", type: "info" },
    { id: 4, text: "Security Agent completed anomaly scan on ESP32 gateway nodes.", time: "10:38:00 AM", type: "info" },
  ]);

  const agents = [
    {
      id: "forecast",
      name: "Forecast Agent",
      icon: <TrendingUp size={32} />,
      status: "Running",
      decision: "High solar generation expected (Peak 13:00)",
      confidence: "96%",
      metric: "Model Loss: 0.024"
    },
    {
      id: "trading",
      name: "Trading Agent",
      icon: <Zap size={32} />,
      status: "Running",
      decision: "Sell 2.5 kWh to Villa 104 @ $0.14/kWh",
      confidence: "93%",
      metric: "Order Matching: Optimal"
    },
    {
      id: "battery",
      name: "Battery Agent",
      icon: <BatteryCharging size={32} />,
      status: "Running",
      decision: "Battery Healthy (82% SoC) - Reserve line maintained",
      confidence: "99%",
      metric: "Degradation Rate: <0.01%"
    },
    {
      id: "fault",
      name: "Fault Detection",
      icon: <AlertTriangle size={32} />,
      status: "Monitoring",
      decision: "No Faults Detected across grid sensors",
      confidence: "100%",
      metric: "PZEM Noise: Normal"
    },
    {
      id: "security",
      name: "Security Agent",
      icon: <ShieldCheck size={32} />,
      status: "Secure",
      decision: "No intrusion threats found on microgrid bus",
      confidence: "100%",
      metric: "TLS Handshake: Verified"
    }
  ];

  const handleAcceptTrade = () => {
    if (tradeAccepted) return;
    setTradeAccepted(true);
    const newLog = {
      id: Date.now(),
      text: "EXECUTION CONFIRMED: Dispatching 2.5 kWh smart contract to Villa 104 via ESP32 Relay.",
      time: new Date().toLocaleTimeString(),
      type: "success"
    };
    setLogs((prevLogs) => [newLog, ...prevLogs]);
  };

  return (
    <div className="ai-page">
      {/* Hero Header */}
      <div className="hero">
        <div className="hero-icon-wrapper">
          <Cpu size={64} className="hero-icon" />
        </div>
        <h1>WATT AI</h1>
        <p>Intelligent Multi-Agent Energy Decision & Autonomous Grid Balancing Engine</p>
      </div>

      {/* Summary KPI Ribbon */}
      <div className="summary">
        <div className="summary-card">
          <h2>AI Status</h2>
          <span className="green">ONLINE</span>
        </div>
        <div className="summary-card">
          <h2>Running Agents</h2>
          <span>{agents.length}</span>
        </div>
        <div className="summary-card">
          <h2>Today's Decisions</h2>
          <span>42</span>
        </div>
        <div className="summary-card">
          <h2>Average Confidence</h2>
          <span>97.6%</span>
        </div>
      </div>

      {/* Agents Grid */}
      <h2 className="section-title">Active AI Agents</h2>
      <div className="agent-grid">
        {agents.map((agent) => (
          <div
            className={`agent-card ${selectedAgent === agent.id ? "selected" : ""}`}
            key={agent.id}
            onClick={() => setSelectedAgent(agent.id === selectedAgent ? null : agent.id)}
          >
            <div className="icon">{agent.icon}</div>
            <h2>{agent.name}</h2>
            <p>{agent.decision}</p>
            <div className="metric-tag">{agent.metric}</div>
            <div className="bottom">
              <span className="status-badge">{agent.status}</span>
              <strong>{agent.confidence}</strong>
            </div>
          </div>
        ))}
      </div>

      {/* Recommendation Card */}
      <div className="recommendation">
        <h2>
          <Activity size={24} color="#00d4ff" /> Top AI Recommendation
        </h2>
        <p>
          Based on battery state-of-charge (<strong>82%</strong>), peak solar generation forecast, and neighborhood demand pricing, the system recommends executing an immediate transfer of{" "}
          <strong>2.5 kWh</strong> to <strong>Villa 104</strong>.
        </p>

        {tradeAccepted ? (
          <div className="trade-success-box">
            <CheckCircle2 color="#22c55e" size={24} />
            <span>Smart Contract Execution Initiated. Microgrid relay engaged.</span>
          </div>
        ) : (
          <button onClick={handleAcceptTrade}>
            Accept & Execute Trade <ArrowRight size={18} style={{ marginLeft: "8px" }} />
          </button>
        )}
      </div>

      {/* Terminal Live Activity Logs */}
      <div className="logs">
        <h2>
          <Terminal size={22} style={{ display: "inline-block", marginRight: "10px", verticalAlign: "middle" }} />
          Live Agent Execution Stream
        </h2>
        <ul>
          {logs.map((log) => (
            <li key={log.id} className={log.type === "success" ? "log-success" : ""}>
              <CheckCircle2 size={16} color={log.type === "success" ? "#22c55e" : "#00d4ff"} />
              <span className="log-time">[{log.time}]</span>
              <span className="log-text">{log.text}</span>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
}