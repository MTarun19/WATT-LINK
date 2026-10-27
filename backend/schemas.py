from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


# =====================================================
# User Schemas
# =====================================================

class UserCreate(BaseModel):
    full_name: str
    email: EmailStr
    password: str
    phone: str
    residence_id: int


class UserRegister(UserCreate):
    pass


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class ChangePassword(BaseModel):
    old_password: str
    new_password: str


class UserResponse(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    phone: str
    role: str
    residence_id: Optional[int] = None

    class Config:
        from_attributes = True


# =====================================================
# Profile Update
# =====================================================

class ProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


# =====================================================
# JWT Token
# =====================================================

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


# =====================================================
# Residence Schemas
# =====================================================

class ResidenceCreate(BaseModel):
    residence_name: str
    block: str
    house_no: str
    address: str


class ResidenceResponse(ResidenceCreate):
    id: int

    class Config:
        from_attributes = True


# =====================================================
# Sensor Schemas
# =====================================================

class SensorCreate(BaseModel):
    sensor_name: str
    sensor_type: str
    status: str
    house_no: str


class SensorUpdate(BaseModel):
    sensor_name: Optional[str] = None
    sensor_type: Optional[str] = None
    status: Optional[str] = None
    house_no: Optional[str] = None


class SensorResponse(BaseModel):
    id: int
    sensor_name: str
    sensor_type: str
    status: str
    house_no: str
    last_seen: Optional[datetime]

    class Config:
        from_attributes = True


# =====================================================
# Sensor Data Schemas
# =====================================================

class SensorDataCreate(BaseModel):
    sensor_id: int
    voltage: float
    current: float
    power: float
    battery: float
    solar: float
    temperature: float


class SensorDataResponse(SensorDataCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# Trading Schemas
# =====================================================

class TradingCreate(BaseModel):
    seller: str
    buyer: str
    energy: float
    price: float


class TradingUpdate(BaseModel):
    status: str


class TradingResponse(BaseModel):
    id: int
    seller: str
    buyer: str
    energy: float
    price: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# Battery Schemas
# =====================================================

class BatteryStatus(BaseModel):
    percentage: float
    voltage: float
    current: float
    health: str


# =====================================================
# Relay Schemas
# =====================================================

class RelayControl(BaseModel):
    relay_id: int
    status: str


class RelayStatus(BaseModel):
    relay_id: int
    relay_name: str
    status: str


# =====================================================
# AI Agent Schemas
# =====================================================

class AgentRequest(BaseModel):
    house_no: str


class AgentResponse(BaseModel):
    agent_name: str
    decision: str
    confidence: float
    status: str

    class Config:
        from_attributes = True


# =====================================================
# Dashboard
# =====================================================

class DashboardResponse(BaseModel):
    residence: str
    house: str
    power_generation: float
    power_consumption: float
    battery: float
    solar: float
    grid: str
    trading: str


# =====================================================
# Alerts
# =====================================================

class AlertResponse(BaseModel):
    sensor_name: str
    severity: str
    message: str
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# User Activity
# =====================================================

class ActivityResponse(BaseModel):
    user_name: str
    activity: str
    created_at: datetime

    class Config:
        from_attributes = True


# =====================================================
# Marketplace
# =====================================================

class MarketplaceOffer(BaseModel):
    seller: str
    energy: float
    price: float


# =====================================================
# AI Decision
# =====================================================

class AIDecision(BaseModel):
    decision: str
    confidence: float
    explanation: str


# =====================================================
# API Response
# =====================================================

class MessageResponse(BaseModel):
    message: str