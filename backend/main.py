"""
main.py
-----------------------------------
WATT LINK Backend
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

# ============================
# Import Routers
# ============================

from routers.auth_router import router as auth_router
from routers.profile_router import router as profile_router
from routers.sensor_router import router as sensor_router
from routers.ai_router import router as ai_router
from routers.marketplace_router import router as marketplace_router
from routers.relay_router import router as relay_router
from routers.battery_router import router as battery_router

# ============================
# Create Database Tables
# ============================

Base.metadata.create_all(bind=engine)

# ============================
# FastAPI App
# ============================

app = FastAPI(
    title="WATT LINK API",
    description="Agentic AI Smart Microgrid & Peer-to-Peer Energy Trading Platform",
    version="1.0.0"
)

# ============================
# CORS Configuration
# ============================

origins = [
    "http://localhost:3000",
    "http://localhost:5173",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============================
# Register Routers
# ============================

app.include_router(auth_router, prefix="/auth", tags=["Authentication"])
app.include_router(profile_router, prefix="/profile", tags=["Profile"])
app.include_router(sensor_router, prefix="/sensor", tags=["Sensors"])
app.include_router(ai_router, prefix="/ai", tags=["AI"])
app.include_router(marketplace_router, prefix="/marketplace", tags=["Marketplace"])
app.include_router(relay_router, prefix="/relay", tags=["Relay"])
app.include_router(battery_router, prefix="/battery", tags=["Battery"])

# ============================
# Root Endpoint
# ============================

@app.get("/")
def root():
    return {
        "project": "WATT LINK",
        "version": "1.0.0",
        "status": "Running",
        "description": "Agentic AI Smart Microgrid Backend"
    }

# ============================
# Health Check
# ============================

@app.get("/health")
def health():
    return {
        "status": "Healthy",
        "database": "Connected",
        "api": "Running"
    }

# ============================
# API Information
# ============================

@app.get("/info")
def info():
    return {
        "Project": "WATT LINK",
        "Framework": "FastAPI",
        "Database": "PostgreSQL",
        "AI": "Agentic AI",
        "Microgrid": "Enabled",
        "Marketplace": "Enabled"
    }