import React from "react";
import {
  Bell,
  BatteryCharging,
  Sun,
  Wifi,
  UserCircle,
  Activity,
  Zap,
  LogOut
} from "lucide-react";
import { useNavigate } from "react-router-dom";
import "./Navbar.css";

export default function Navbar() {
  const navigate = useNavigate();

  const handleLogout = () => {
    // Add clear session / auth state logic here if needed
    navigate("/login");
  };

  return (
    <header className="navbar">
      {/* Brand Section */}
      <div className="navbar-left">
        <div className="brand-logo">
          <Zap size={20} className="brand-icon" />
        </div>
        <div className="brand-text">
          <h2>WATT LINK</h2>
          <span>Smart Microgrid Energy Trading Platform</span>
        </div>
      </div>

      {/* Dynamic Telemetry & Actions */}
      <div className="navbar-right">
        {/* Solar Status */}
        <div className="nav-card">
          <Sun size={18} className="icon-yellow" />
          <div>
            <small>Solar</small>
            <h4>5.2 kW</h4>
          </div>
        </div>

        {/* Battery */}
        <div className="nav-card">
          <BatteryCharging size={18} className="icon-green" />
          <div>
            <small>Battery</small>
            <h4>82%</h4>
          </div>
        </div>

        {/* Network */}
        <div className="nav-card">
          <Wifi size={18} className="icon-cyan" />
          <div>
            <small>ESP32</small>
            <h4 className="status-online">
              <span className="dot"></span> Online
            </h4>
          </div>
        </div>

        {/* AI Engine Status */}
        <div className="nav-card">
          <Activity size={18} className="icon-purple" />
          <div>
            <small>AI Status</small>
            <h4>Active</h4>
          </div>
        </div>

        {/* Notification Badge */}
        <button className="notification-btn" title="Notifications">
          <Bell size={20} />
          <span className="badge-count">3</span>
        </button>

        {/* Divider */}
        <div className="nav-divider"></div>

        {/* User Profile & Logout */}
        <div className="user-profile">
          <div className="user-avatar">
            <UserCircle size={36} color="#00D4FF" />
          </div>
          <div className="user-info">
            <h4>Administrator</h4>
            <small>Energy Manager</small>
          </div>

          <button
            className="logout-btn"
            onClick={handleLogout}
            title="Logout of Dashboard"
          >
            <LogOut size={16} />
            <span>Logout</span>
          </button>
        </div>
      </div>
    </header>
  );
}