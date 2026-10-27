from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    ForeignKey,
    Text
)

from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base


# ==========================================================
# Residence
# ==========================================================

class Residence(Base):

    __tablename__ = "residences"

    id = Column(Integer, primary_key=True, index=True)
    residence_name = Column(String(100))
    block = Column(String(50))
    house_no = Column(String(30))
    address = Column(Text)

    users = relationship("User", back_populates="residence")


# ==========================================================
# User
# ==========================================================

class User(Base):

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    full_name = Column(String(100))

    email = Column(String(100), unique=True)

    password = Column(String(255))

    phone = Column(String(20))

    role = Column(String(20), default="Resident")

    residence_id = Column(Integer, ForeignKey("residences.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    residence = relationship("Residence", back_populates="users")


# ==========================================================
# Sensor
# ==========================================================

class Sensor(Base):

    __tablename__ = "sensors"

    id = Column(Integer, primary_key=True)

    sensor_name = Column(String(50))

    sensor_type = Column(String(50))

    status = Column(String(20))

    last_seen = Column(DateTime)

    house_no = Column(String(30))


# ==========================================================
# Sensor Data
# ==========================================================

class SensorData(Base):

    __tablename__ = "sensor_data"

    id = Column(Integer, primary_key=True)

    sensor_id = Column(Integer)

    voltage = Column(Float)

    current = Column(Float)

    power = Column(Float)

    battery = Column(Float)

    solar = Column(Float)

    temperature = Column(Float)

    created_at = Column(DateTime, default=datetime.utcnow)


# ==========================================================
# Marketplace
# ==========================================================

class Marketplace(Base):

    __tablename__ = "marketplace"

    id = Column(Integer, primary_key=True, index=True)

    seller_id = Column(Integer, ForeignKey("users.id"))

    buyer_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    energy = Column(Float)

    price = Column(Float)

    status = Column(String(30), default="AVAILABLE")

    created_at = Column(DateTime, default=datetime.utcnow)

    seller = relationship(
        "User",
        foreign_keys=[seller_id]
    )

    buyer = relationship(
        "User",
        foreign_keys=[buyer_id]
    )


# ==========================================================
# Energy Trading
# ==========================================================

class Trading(Base):

    __tablename__ = "energy_trading"

    id = Column(Integer, primary_key=True)

    seller = Column(String(50))

    buyer = Column(String(50))

    energy = Column(Float)

    price = Column(Float)

    status = Column(String(30))

    created_at = Column(DateTime, default=datetime.utcnow)


# ==========================================================
# AI Agents
# ==========================================================

class AIAgent(Base):

    __tablename__ = "ai_agents"

    id = Column(Integer, primary_key=True)

    agent_name = Column(String(100))

    decision = Column(Text)

    confidence = Column(Float)

    status = Column(String(30))

    updated_at = Column(DateTime, default=datetime.utcnow)


# ==========================================================
# Alerts
# ==========================================================

class Alert(Base):

    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True)

    sensor_name = Column(String(50))

    severity = Column(String(20))

    message = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)


# ==========================================================
# User Activity
# ==========================================================

class UserActivity(Base):

    __tablename__ = "user_activity"

    id = Column(Integer, primary_key=True)

    user_name = Column(String(100))

    activity = Column(Text)

    created_at = Column(DateTime, default=datetime.utcnow)