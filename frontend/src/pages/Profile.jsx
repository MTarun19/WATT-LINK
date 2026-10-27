import React, { useState } from "react";
import {
  User,
  Mail,
  Phone,
  Home,
  BatteryCharging,
  Sun,
  Zap,
  IndianRupee,
  ShieldCheck,
  Cpu,
  Edit3,
  Award,
  CheckCircle2,
  Lock,
  Smartphone,
  X,
  Save,
  Activity,
  Key
} from "lucide-react";

import "./Profile.css";

export default function Profile() {
  const [isEditOpen, setIsEditOpen] = useState(false);
  const [toastMessage, setToastMessage] = useState("");

  // User Profile State
  const [userInfo, setUserInfo] = useState({
    name: "Tarun Kumar",
    email: "tarun@wattlink.io",
    phone: "+91 98765 43210",
    villa: "Villa 104, Phase II",
    community: "Green Valley Residency"
  });

  // Security Toggles State
  const [securitySettings, setSecuritySettings] = useState({
    twoFactor: true,
    autoLock: true,
    jwtSession: true
  });

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setUserInfo((prev) => ({ ...prev, [name]: value }));
  };

  const handleSaveProfile = (e) => {
    e.preventDefault();
    setIsEditOpen(false);
    triggerToast("Profile details updated successfully!");
  };

  const toggleSecurity = (key) => {
    setSecuritySettings((prev) => {
      const updated = !prev[key];
      triggerToast(`${key === "twoFactor" ? "2FA" : "Auto-Lock"} turned ${updated ? "ON" : "OFF"}`);
      return { ...prev, [key]: updated };
    });
  };

  const triggerToast = (msg) => {
    setToastMessage(msg);
    setTimeout(() => setToastMessage(""), 3500);
  };

  return (
    <div className="profile-page">
      {/* Notification Toast */}
      {toastMessage && (
        <div className="profile-toast">
          <CheckCircle2 size={18} color="#00d4ff" />
          <span>{toastMessage}</span>
        </div>
      )}

      {/* Profile Header */}
      <div className="profile-header">
        <div className="avatar-wrapper">
          <div className="avatar">
            <User size={64} color="#00d4ff" />
          </div>
          <span className="online-badge"></span>
        </div>

        <div className="header-details">
          <h1>{userInfo.name}</h1>
          <p>
            Resident • <Home size={14} className="inline-icon" /> {userInfo.community}
          </p>
          <div className="badge-row">
            <span className="badge">
              <Award size={15} /> Verified Energy Prosumer
            </span>
            <span className="badge badge-subtle">
              <Activity size={15} /> Microgrid Node #104
            </span>
          </div>
        </div>
      </div>

      {/* Main Grid Section 1 */}
      <div className="profile-grid">
        {/* Card 1: Personal Info */}
        <div className="card">
          <div className="card-header">
            <h2>Personal Information</h2>
            <button className="edit-btn" onClick={() => setIsEditOpen(true)}>
              <Edit3 size={16} /> Edit
            </button>
          </div>

          <div className="info-list">
            <div className="info-item">
              <User size={18} className="info-icon" />
              <div>
                <label>Full Name</label>
                <p>{userInfo.name}</p>
              </div>
            </div>

            <div className="info-item">
              <Mail size={18} className="info-icon" />
              <div>
                <label>Email Address</label>
                <p>{userInfo.email}</p>
              </div>
            </div>

            <div className="info-item">
              <Phone size={18} className="info-icon" />
              <div>
                <label>Phone Number</label>
                <p>{userInfo.phone}</p>
              </div>
            </div>

            <div className="info-item">
              <Home size={18} className="info-icon" />
              <div>
                <label>Residence</label>
                <p>{userInfo.villa}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Card 2: Energy Statistics */}
        <div className="card">
          <div className="card-header">
            <h2>Live Energy Statistics</h2>
            <span className="live-tag">Today</span>
          </div>

          <div className="stats-grid">
            <div className="stat-box">
              <Sun color="#ffd43b" size={26} />
              <div>
                <h3>Solar Gen</h3>
                <span>6.8 kWh</span>
              </div>
            </div>

            <div className="stat-box">
              <BatteryCharging color="#22c55e" size={26} />
              <div>
                <h3>Battery SoC</h3>
                <span>82%</span>
              </div>
            </div>

            <div className="stat-box">
              <Zap color="#00d4ff" size={26} />
              <div>
                <h3>Consumed</h3>
                <span>4.2 kWh</span>
              </div>
            </div>

            <div className="stat-box">
              <IndianRupee color="#22c55e" size={26} />
              <div>
                <h3>Total Saved</h3>
                <span className="green-text">₹845</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Main Grid Section 2 */}
      <div className="profile-grid">
        {/* Card 3: AI Engine Metrics */}
        <div className="card">
          <div className="card-header">
            <h2>
              <Cpu color="#00d4ff" size={20} /> AI Optimization Engine
            </h2>
          </div>

          <ul className="feature-list">
            <li>
              <div className="feature-status">
                <CheckCircle2 size={16} color="#22c55e" />
                <span>Forecast Accuracy</span>
              </div>
              <strong className="metric-val">97%</strong>
            </li>
            <li>
              <div className="feature-status">
                <CheckCircle2 size={16} color="#22c55e" />
                <span>P2P Trading Success</span>
              </div>
              <strong className="metric-val">95%</strong>
            </li>
            <li>
              <div className="feature-status">
                <CheckCircle2 size={16} color="#22c55e" />
                <span>Smart Battery Balancing</span>
              </div>
              <span className="status-tag active">Active</span>
            </li>
            <li>
              <div className="feature-status">
                <CheckCircle2 size={16} color="#22c55e" />
                <span>Dynamic Load Prediction</span>
              </div>
              <span className="status-tag active">Enabled</span>
            </li>
          </ul>
        </div>

        {/* Card 4: Security Control Panel */}
        <div className="card">
          <div className="card-header">
            <h2>
              <ShieldCheck color="#00d4ff" size={20} /> Security & Access
            </h2>
          </div>

          <div className="security-list">
            <div className="security-item">
              <div className="security-text">
                <div className="security-title">
                  <Key size={16} /> Two-Factor Auth (2FA)
                </div>
                <p>Require OTP code for peer-to-peer energy sales</p>
              </div>
              <button
                className={`toggle-switch ${securitySettings.twoFactor ? "on" : "off"}`}
                onClick={() => toggleSecurity("twoFactor")}
              >
                <span className="toggle-handle"></span>
              </button>
            </div>

            <div className="security-item">
              <div className="security-text">
                <div className="security-title">
                  <Lock size={16} /> Session Auto-Lock
                </div>
                <p>Lock grid controls after 15 mins of inactivity</p>
              </div>
              <button
                className={`toggle-switch ${securitySettings.autoLock ? "on" : "off"}`}
                onClick={() => toggleSecurity("autoLock")}
              >
                <span className="toggle-handle"></span>
              </button>
            </div>

            <div className="security-item">
              <div className="security-text">
                <div className="security-title">
                  <Smartphone size={16} /> Active Terminal
                </div>
                <p>Windows Desktop • FastAPI Gateway Node</p>
              </div>
              <span className="status-tag info">Verified</span>
            </div>
          </div>
        </div>
      </div>

      {/* Recent Ledger Activity */}
      <div className="card activity-card">
        <div className="card-header">
          <h2>Recent Energy Transactions & Actions</h2>
          <span className="live-tag">P2P Ledger</span>
        </div>

        <div className="table-responsive">
          <table className="activity-table">
            <thead>
              <tr>
                <th>Date</th>
                <th>Activity Event</th>
                <th>Units / Type</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr>
                <td>24 Jul 2026</td>
                <td>Sold Surplus Power to Villa 108</td>
                <td>3.5 kWh</td>
                <td>
                  <span className="status-chip success">Completed</span>
                </td>
              </tr>
              <tr>
                <td>24 Jul 2026</td>
                <td>Solar Battery Auto-Charge Cycle</td>
                <td>Battery 82%</td>
                <td>
                  <span className="status-chip success">Success</span>
                </td>
              </tr>
              <tr>
                <td>23 Jul 2026</td>
                <td>Accepted AI Trading Strategy recommendation</td>
                <td>Peak Saver</td>
                <td>
                  <span className="status-chip success">Completed</span>
                </td>
              </tr>
              <tr>
                <td>22 Jul 2026</td>
                <td>ESP32 Firmware Auto-Update</td>
                <td>v1.0.4 Patch</td>
                <td>
                  <span className="status-chip info">Updated</span>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

      {/* Edit Profile Modal */}
      {isEditOpen && (
        <div className="modal-overlay">
          <div className="modal-content">
            <div className="modal-header">
              <h2>Edit Profile Information</h2>
              <button className="close-btn" onClick={() => setIsEditOpen(false)}>
                <X size={20} />
              </button>
            </div>

            <form onSubmit={handleSaveProfile} className="modal-form">
              <div className="form-group">
                <label>Full Name</label>
                <input
                  type="text"
                  name="name"
                  value={userInfo.name}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Email Address</label>
                <input
                  type="email"
                  name="email"
                  value={userInfo.email}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Phone Number</label>
                <input
                  type="text"
                  name="phone"
                  value={userInfo.phone}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="form-group">
                <label>Villa / Address</label>
                <input
                  type="text"
                  name="villa"
                  value={userInfo.villa}
                  onChange={handleInputChange}
                  required
                />
              </div>

              <div className="modal-actions">
                <button
                  type="button"
                  className="cancel-btn"
                  onClick={() => setIsEditOpen(false)}
                >
                  Cancel
                </button>
                <button type="submit" className="save-btn">
                  <Save size={16} /> Save Changes
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}