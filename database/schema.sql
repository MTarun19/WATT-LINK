CREATE DATABASE IF NOT EXISTS watt_link;
USE watt_link;

-- ===========================================
-- Residences
-- ===========================================

CREATE TABLE residences (
    id INT AUTO_INCREMENT PRIMARY KEY,
    residence_name VARCHAR(100) NOT NULL,
    block_name VARCHAR(50),
    house_number VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ===========================================
-- Users
-- ===========================================

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    role VARCHAR(30) DEFAULT 'Resident',
    residence_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (residence_id)
    REFERENCES residences(id)
);

-- ===========================================
-- Sensors
-- ===========================================

CREATE TABLE sensors (

    id INT AUTO_INCREMENT PRIMARY KEY,

    house_number VARCHAR(20),

    sensor_name VARCHAR(50),

    sensor_type VARCHAR(50),

    status VARCHAR(20),

    last_seen DATETIME

);

-- ===========================================
-- Sensor Data
-- ===========================================

CREATE TABLE sensor_data (

    id INT AUTO_INCREMENT PRIMARY KEY,

    sensor_id INT,

    voltage FLOAT,

    current FLOAT,

    power FLOAT,

    energy FLOAT,

    battery FLOAT,

    solar FLOAT,

    temperature FLOAT,

    humidity FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(sensor_id)
    REFERENCES sensors(id)

);

-- ===========================================
-- Energy Trading
-- ===========================================

CREATE TABLE energy_trading (

    id INT AUTO_INCREMENT PRIMARY KEY,

    seller VARCHAR(100),

    buyer VARCHAR(100),

    energy FLOAT,

    price FLOAT,

    status VARCHAR(30),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ===========================================
-- AI Agents
-- ===========================================

CREATE TABLE ai_agents (

    id INT AUTO_INCREMENT PRIMARY KEY,

    agent_name VARCHAR(100),

    decision TEXT,

    confidence FLOAT,

    status VARCHAR(30),

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ===========================================
-- Alerts
-- ===========================================

CREATE TABLE alerts (

    id INT AUTO_INCREMENT PRIMARY KEY,

    sensor_name VARCHAR(100),

    severity VARCHAR(20),

    message TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ===========================================
-- Relay Status
-- ===========================================

CREATE TABLE relay_status (

    id INT AUTO_INCREMENT PRIMARY KEY,

    relay_name VARCHAR(50),

    relay_state VARCHAR(10),

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ===========================================
-- User Activity
-- ===========================================

CREATE TABLE user_activity (

    id INT AUTO_INCREMENT PRIMARY KEY,

    user_name VARCHAR(100),

    activity TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ===========================================
-- Notifications
-- ===========================================

CREATE TABLE notifications (

    id INT AUTO_INCREMENT PRIMARY KEY,

    title VARCHAR(100),

    description TEXT,

    status VARCHAR(20),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);

-- ===========================================
-- Dashboard Summary
-- ===========================================

CREATE TABLE dashboard (

    id INT AUTO_INCREMENT PRIMARY KEY,

    house_number VARCHAR(20),

    power_generation FLOAT,

    power_consumption FLOAT,

    battery FLOAT,

    solar FLOAT,

    trading_status VARCHAR(30),

    grid_status VARCHAR(30),

    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

);