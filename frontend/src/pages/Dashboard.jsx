import React, { useState, useEffect } from "react";
import {
  BatteryCharging,
  Sun,
  Zap,
  TrendingUp,
  Bell,
  Cpu,
  Activity,
  ShieldCheck,
  ArrowRight,
  Home,
  HandCoins,
  Bot,
  Sparkles,
  CheckCircle2,
  Building2,
  ArrowUpRight
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import "./Dashboard.css";
import AIAssistant from "../components/AIAssistant";

export default function Dashboard() {
  const navigate = useNavigate();

  // Dynamic Telemetry State Updates
  const [voltage, setVoltage] = useState(230.4);
  const [frequency, setFrequency] = useState(50.0);

  useEffect(() => {
    const interval = setInterval(() => {
      setVoltage((229.5 + Math.random() * 1.8).toFixed(1));
      setFrequency((49.95 + Math.random() * 0.1).toFixed(2));
    }, 2500);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="dashboard">
      {/* Dynamic Background Mesh Glows */}
      <div className="bg-glow bg-glow-1"></div>
      <div className="bg-glow bg-glow-2"></div>

      {/* High-Tech Topbar */}
      <header className="topbar">
        <div className="brand">
          <div className="brand-icon">
            <Zap size={22} color="#050814" fill="#00D4FF" />
          </div>
          <div>
            <div className="title-row">
              <h1>WATT LINK</h1>
              <span className="live-pill">
                <span className="pulse-dot"></span> LIVE
              </span>
            </div>
            <p>Smart Microgrid Energy Platform</p>
          </div>
        </div>

        {/* Live Grid Telemetry */}
        <div className="topbar-stats">
          <div className="telemetry-item">
            <span className="telemetry-label">GRID VOLTAGE</span>
            <span className="telemetry-value">{voltage} V</span>
          </div>
          <div className="telemetry-divider"></div>
          <div className="telemetry-item">
            <span className="telemetry-label">FREQUENCY</span>
            <span className="telemetry-value">{frequency} Hz</span>
          </div>
        </div>

        {/* User Profile Controls */}
        <div className="user">
          <button className="icon-btn" title="Alerts">
            <Bell size={18} color="#9CA3AF" />
            <span className="notification-dot"></span>
          </button>
          <div className="user-profile">
            <div className="avatar">T</div>
            <div className="user-info">
              <span className="user-name">Tarun</span>
              <span className="user-role">System Admin</span>
            </div>
          </div>
        </div>
      </header>

      {/* Summary Stat Cards */}
      <div className="cards">
        <div className="card">
          <div className="card-header">
            <Sun size={28} color="#FFD43B" />
            <span className="badge badge-yellow">Live Generation</span>
          </div>
          <h2>Solar</h2>
          <h1>1.42 <small>kW</small></h1>
        </div>

        <div className="card">
          <div className="card-header">
            <BatteryCharging size={28} color="#10B981" />
            <span className="badge badge-green">Healthy</span>
          </div>
          <h2>Battery</h2>
          <h1>82<small>%</small></h1>
        </div>

        <div className="card">
          <div className="card-header">
            <Zap size={28} color="#00D4FF" />
            <span className="badge badge-cyan">Active Load</span>
          </div>
          <h2>Consumption</h2>
          <h1>0.92 <small>kW</small></h1>
        </div>

        <div className="card">
          <div className="card-header">
            <TrendingUp size={28} color="#8B5CF6" />
            <span className="badge badge-purple">+14.2% Today</span>
          </div>
          <h2>Savings</h2>
          <h1>₹62</h1>
        </div>
      </div>

      {/* Live Energy Flow & AI Panel */}
      <div className="grid">
        <div className="panel">
          <h2>
            <Zap color="#00D4FF" size={20} /> Live Energy Flow
          </h2>
          <div className="flow">
            <div className="flow-item">
              <Sun size={32} color="#FFD43B" />
              <h4>Solar</h4>
              <small>1.42 kW</small>
            </div>
            <ArrowRight className="flow-arrow" size={20} />
            <div className="flow-item">
              <BatteryCharging size={32} color="#10B981" />
              <h4>Battery</h4>
              <small>82%</small>
            </div>
            <ArrowRight className="flow-arrow" size={20} />
            <div className="flow-item">
              <Home size={32} color="#00D4FF" />
              <h4>House</h4>
              <small>0.92 kW</small>
            </div>
            <ArrowRight className="flow-arrow" size={20} />
            <div className="flow-item">
              <HandCoins size={32} color="#8B5CF6" />
              <h4>Trading</h4>
              <small>2.5 kWh</small>
            </div>
            <ArrowRight className="flow-arrow" size={20} />
            <div className="flow-item">
              <Zap size={32} color="#00D4FF" />
              <h4>Grid</h4>
              <small>Export</small>
            </div>
          </div>
        </div>

        <div className="panel ai-panel">
          <h2>
            <Bot color="#8B5CF6" size={22} /> AI Recommendation
          </h2>
          <div className="ai-content">
            <p>Battery capacity optimal at <strong>82%</strong> with elevated solar output.</p>
            <h3>Sell 2.5 kWh to Energy Marketplace</h3>
          </div>
          <button onClick={() => navigate("/ai")}>
            <Sparkles size={16} />
            Open AI Assistant
          </button>
        </div>
      </div>

      {/* Sensors & System Alerts Grid */}
      <div className="grid">
        <div className="panel">
          <h2>
            <Cpu color="#00D4FF" size={20} /> Connected Sensors
          </h2>
          <ul className="status-list">
            <li>
              <span>PZEM-004T</span>
              <span className="status-tag"><span className="status-dot green"></span> ONLINE</span>
            </li>
            <li>
              <span>INA219</span>
              <span className="status-tag"><span className="status-dot green"></span> ONLINE</span>
            </li>
            <li>
              <span>DHT22</span>
              <span className="status-tag"><span className="status-dot green"></span> ONLINE</span>
            </li>
            <li>
              <span>Relay Module</span>
              <span className="status-tag"><span className="status-dot green"></span> ONLINE</span>
            </li>
            <li>
              <span>MQTT Broker</span>
              <span className="status-tag"><span className="status-dot green"></span> ONLINE</span>
            </li>
            <li>
              <span>ESP32 Core</span>
              <span className="status-tag"><span className="status-dot green"></span> ONLINE</span>
            </li>
          </ul>
        </div>

        <div className="panel">
          <h2>
            <Activity color="#10B981" size={20} /> System Health & Alerts
          </h2>
          <ul className="alert-list">
            <li>
              <CheckCircle2 size={16} color="#10B981" /> All Sensors Functioning Normally
            </li>
            <li>
              <CheckCircle2 size={16} color="#10B981" /> AI Engine Running Normally
            </li>
            <li>
              <CheckCircle2 size={16} color="#10B981" /> Automated P2P Trading Enabled
            </li>
          </ul>
        </div>
      </div>

      {/* Marketplace & Transactions Grid */}
      <div className="grid">
        <div
          className="panel"
          onClick={() => navigate("/marketplace")}
          style={{ cursor: "pointer" }}
        >
          <div className="panel-title-row">
            <h2>Marketplace</h2>
            <ArrowUpRight size={18} color="#9CA3AF" />
          </div>

          <table>
            <thead>
              <tr>
                <th>Seller</th>
                <th>Energy</th>
                <th>Price</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td><Building2 size={14} className="inline-icon" /> Villa 102</td>
                <td>3.5 kWh</td>
                <td className="price-tag">₹8/kWh</td>
              </tr>
              <tr>
                <td><Building2 size={14} className="inline-icon" /> Villa 109</td>
                <td>2.1 kWh</td>
                <td className="price-tag">₹7/kWh</td>
              </tr>
            </tbody>
          </table>

          <button
            onClick={(e) => {
              e.stopPropagation();
              navigate("/marketplace");
            }}
          >
            Open Marketplace
          </button>
        </div>

        <div className="panel">
          <h2>
            <ShieldCheck color="#10B981" size={20} /> Recent Transactions
          </h2>

          <ul className="tx-list">
            <li>
              <div className="tx-details">
                <span className="tx-route">Villa 101 <ArrowRight size={12} /> Villa 104</span>
                <span className="tx-sub">2.5 kWh</span>
              </div>
              <span className="tx-amount">₹20</span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  );
}