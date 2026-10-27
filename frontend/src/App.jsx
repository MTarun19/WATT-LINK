import { Routes, Route, Navigate } from "react-router-dom";

import Login from "./pages/Login";
import Dashboard from "./pages/Dashboard";
import AI from "./pages/AI";
import Marketplace from "./pages/Marketplace";
import Sensors from "./pages/Sensors";
import Profile from "./pages/Profile";

import Layout from "./Layout";

export default function App() {
  return (
    <Routes>

      {/* Login */}
      <Route path="/" element={<Login />} />

      {/* Protected Layout */}
      <Route element={<Layout />}>

        <Route path="/dashboard" element={<Dashboard />} />

        <Route path="/ai" element={<AI />} />

        <Route path="/marketplace" element={<Marketplace />} />

        <Route path="/sensors" element={<Sensors />} />

        <Route path="/profile" element={<Profile />} />

      </Route>

      <Route path="*" element={<Navigate to="/" replace />} />

    </Routes>
  );
}