import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import {
  Zap,
  ShieldCheck,
  Lock,
  Mail,
  Eye,
  EyeOff,
  Cpu,
  BatteryCharging,
  Sun
} from "lucide-react";

import "./Login.css";

export default function Login() {

  const navigate = useNavigate();

  const [showPassword, setShowPassword] = useState(false);

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = (e) => {
    e.preventDefault();

    // Temporary login (replace with API later)
    if (email.trim() !== "" && password.trim() !== "") {
      navigate("/dashboard");
    } else {
      alert("Please enter Email and Password");
    }
  };

  return (

    <div className="login-container">

      {/* LEFT PANEL */}

      <div className="left-panel">

        <div className="overlay">

          <h1>⚡ WATT LINK</h1>

          <p className="subtitle">
            Smart Microgrid & Peer-to-Peer Energy Trading Platform
          </p>

          <div className="features">

            <div className="feature">
              <Sun size={30} />
              <span>Renewable Energy Management</span>
            </div>

            <div className="feature">
              <BatteryCharging size={30} />
              <span>Battery Optimization</span>
            </div>

            <div className="feature">
              <Cpu size={30} />
              <span>Agentic AI Decision Engine</span>
            </div>

            <div className="feature">
              <ShieldCheck size={30} />
              <span>Secure Energy Marketplace</span>
            </div>

          </div>

          <div className="stats">

            <div>
              <h2>3</h2>
              <span>Connected Houses</span>
            </div>

            <div>
              <h2>12</h2>
              <span>Smart Sensors</span>
            </div>

            <div>
              <h2>99.9%</h2>
              <span>System Availability</span>
            </div>

          </div>

        </div>

      </div>

      {/* RIGHT PANEL */}

      <div className="right-panel">

        <div className="login-card">

          <Zap size={55} color="#00d4ff" />

          <h2>Welcome Back</h2>

          <p>Login to your WATT LINK account</p>

          <form onSubmit={handleLogin}>

            <div className="input-box">

              <Mail />

              <input
                type="email"
                placeholder="Email Address"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
              />

            </div>

            <div className="input-box">

              <Lock />

              <input
                type={showPassword ? "text" : "password"}
                placeholder="Password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />

              <button
                type="button"
                className="eye-btn"
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
              </button>

            </div>

            <button
              type="submit"
              className="login-btn"
            >
              Login
            </button>

          </form>

          <div className="links">

            <a href="#">Forgot Password?</a>

            <a href="#">Create Account</a>
            

          </div>

          <div className="security">

            <ShieldCheck color="lime" />

            <span>
              Protected with JWT Authentication & AES Encryption
            </span>

          </div>

        </div>

      </div>

    </div>

  );
}