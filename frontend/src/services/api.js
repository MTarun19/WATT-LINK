import axios from "axios";

// ================================
// API Configuration
// ================================

const API_BASE_URL =
  import.meta.env.VITE_API_URL || "http://localhost:8000";

const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    "Content-Type": "application/json",
  },
});

// ================================
// Attach JWT Token Automatically
// ================================

api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem("access_token");

    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }

    return config;
  },
  (error) => Promise.reject(error)
);

// ================================
// Authentication APIs
// ================================

export const login = (data) =>
  api.post("/login", data);

export const register = (data) =>
  api.post("/register", data);

export const getProfile = () =>
  api.get("/profile");

// ================================
// Dashboard APIs
// ================================

export const getDashboard = () =>
  api.get("/dashboard");

export const getSystemStatus = () =>
  api.get("/system/health");

// ================================
// Sensor APIs
// ================================

export const getSensors = () =>
  api.get("/sensor/live");

export const getBattery = () =>
  api.get("/sensor/battery");

export const getSolar = () =>
  api.get("/sensor/solar");

export const getEnergy = () =>
  api.get("/sensor/energy");

// ================================
// AI APIs
// ================================

export const getAIStatus = () =>
  api.get("/ai/status");

export const getAIRecommendation = () =>
  api.get("/ai/recommendation");

// ================================
// Marketplace APIs
// ================================

export const getMarketplace = () =>
  api.get("/trading/marketplace");

export const getTradingHistory = () =>
  api.get("/trading/history");

export const getTradingSummary = () =>
  api.get("/trading/summary");

export const buyEnergy = (data) =>
  api.post("/trading/buy", data);

export const sellEnergy = (data) =>
  api.post("/trading/sell", data);

// ================================
// Relay APIs
// ================================

export const getRelayStatus = () =>
  api.get("/relay/status");

export const controlRelay = (data) =>
  api.post("/relay/control", data);

// ================================
// Public APIs
// ================================

export const getPublicDashboard = () =>
  api.get("/public/dashboard");

export const getPublicAlerts = () =>
  api.get("/public/alerts");

export const getPublicSensors = () =>
  api.get("/public/sensors");

// ================================
// Notification APIs
// ================================

export const getNotifications = () =>
  api.get("/notifications");

// ================================
// Reports APIs
// ================================

export const getDailyReport = () =>
  api.get("/reports/daily");

export const getWeeklyReport = () =>
  api.get("/reports/weekly");

export const getMonthlyReport = () =>
  api.get("/reports/monthly");

// ================================
// Default Export
// ================================

export default api;