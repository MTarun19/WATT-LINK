import React, { useState } from "react";
import { NavLink, useNavigate } from "react-router-dom";
import {
  LayoutDashboard,
  Cpu,
  ShoppingCart,
  Radio,
  User,
  Zap,
  LogOut,
  ChevronLeft,
  ChevronRight,
  ShieldCheck
} from "lucide-react";

import "./Sidebar.css";

export default function Sidebar() {
  const navigate = useNavigate();
  const [isCollapsed, setIsCollapsed] = useState(false);

  const menu = [
    {
      title: "Dashboard",
      icon: <LayoutDashboard size={20} />,
      path: "/dashboard",
    },
    {
      title: "AI Engine",
      icon: <Cpu size={20} />,
      path: "/ai",
    },
    {
      title: "Marketplace",
      icon: <ShoppingCart size={20} />,
      path: "/marketplace",
    },
    {
      title: "Sensors",
      icon: <Radio size={20} />,
      path: "/sensors",
    },
    {
      title: "Profile",
      icon: <User size={20} />,
      path: "/profile",
    },
  ];

  const handleLogout = () => {
    // Session cleanup logic can be placed here
    navigate("/login");
  };

  return (
    <aside className={`sidebar ${isCollapsed ? "collapsed" : ""}`}>
      {/* Collapse / Expand Toggle Button */}
      <button 
        className="sidebar-toggle-btn" 
        onClick={() => setIsCollapsed(!isCollapsed)}
        title={isCollapsed ? "Expand Sidebar" : "Collapse Sidebar"}
      >
        {isCollapsed ? <ChevronRight size={16} /> : <ChevronLeft size={16} />}
      </button>

      {/* Brand Header */}
      <div className="sidebar-logo">
        <div className="logo-icon-wrapper">
          <Zap size={26} className="logo-icon" />
        </div>
        {!isCollapsed && (
          <div className="logo-text">
            <h2>WATT LINK</h2>
            <span>Smart Microgrid</span>
          </div>
        )}
      </div>

      {/* Main Navigation Menu */}
      <nav className="sidebar-menu">
        <div className="menu-label">{!isCollapsed && "Navigation"}</div>
        {menu.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              isActive ? "menu-item active" : "menu-item"
            }
            title={isCollapsed ? item.title : ""}
          >
            <div className="menu-icon">{item.icon}</div>
            {!isCollapsed && <span className="menu-title">{item.title}</span>}
            <div className="active-pill"></div>
          </NavLink>
        ))}
      </nav>

      {/* Sidebar Footer & System Status */}
      <div className="sidebar-footer-container">
        {!isCollapsed && (
          <div className="sidebar-status-card">
            <div className="status-header">
              <div className="status-dot"></div>
              <span>Grid Node Connected</span>
            </div>
            <div className="status-details">
              <ShieldCheck size={14} color="#00d4ff" />
              <span>TLS 1.3 Active</span>
            </div>
          </div>
        )}

        <button 
          className="sidebar-logout-btn" 
          onClick={handleLogout} 
          title="Logout"
        >
          <LogOut size={18} />
          {!isCollapsed && <span>Logout</span>}
        </button>
      </div>
    </aside>
  );
}