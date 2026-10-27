"""
crud.py
------------------------------------
WATT LINK Database Operations
"""

from sqlalchemy.orm import Session
from models import (
    User,
    Residence,
    Sensor,
    SensorData,
    Trading,
    AIAgent,
    Alert,
    UserActivity,
)


# =====================================================
# USER CRUD
# =====================================================

def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def create_user(db: Session, user):

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_user(db: Session, user):

    db.commit()
    db.refresh(user)

    return user


def delete_user(db: Session, user):

    db.delete(user)
    db.commit()


# =====================================================
# RESIDENCE CRUD
# =====================================================

def create_residence(db: Session, residence):

    db.add(residence)
    db.commit()
    db.refresh(residence)

    return residence


def get_all_residences(db: Session):

    return db.query(Residence).all()


def get_residence(db: Session, residence_id: int):

    return (
        db.query(Residence)
        .filter(Residence.id == residence_id)
        .first()
    )


# =====================================================
# SENSOR CRUD
# =====================================================

def create_sensor(db: Session, sensor):

    db.add(sensor)
    db.commit()
    db.refresh(sensor)

    return sensor


def get_all_sensors(db: Session):

    return db.query(Sensor).all()


def get_sensor(db: Session, sensor_id: int):

    return (
        db.query(Sensor)
        .filter(Sensor.id == sensor_id)
        .first()
    )


def update_sensor(db: Session, sensor):

    db.commit()
    db.refresh(sensor)

    return sensor


# =====================================================
# SENSOR DATA
# =====================================================

def create_sensor_data(db: Session, data):

    db.add(data)
    db.commit()
    db.refresh(data)

    return data


def get_latest_sensor_data(db: Session, sensor_id: int):

    return (
        db.query(SensorData)
        .filter(SensorData.sensor_id == sensor_id)
        .order_by(SensorData.created_at.desc())
        .first()
    )


def get_sensor_history(db: Session, sensor_id: int):

    return (
        db.query(SensorData)
        .filter(SensorData.sensor_id == sensor_id)
        .all()
    )


# =====================================================
# ENERGY TRADING
# =====================================================

def create_trade(db: Session, trade):

    db.add(trade)
    db.commit()
    db.refresh(trade)

    return trade


def get_all_trades(db: Session):

    return db.query(Trading).all()


def get_trade(db: Session, trade_id: int):

    return (
        db.query(Trading)
        .filter(Trading.id == trade_id)
        .first()
    )


def update_trade(db: Session, trade):

    db.commit()
    db.refresh(trade)

    return trade


# =====================================================
# AI AGENTS
# =====================================================

def save_ai_decision(db: Session, decision):

    db.add(decision)
    db.commit()
    db.refresh(decision)

    return decision


def get_ai_history(db: Session):

    return (
        db.query(AIAgent)
        .order_by(AIAgent.updated_at.desc())
        .all()
    )


# =====================================================
# ALERTS
# =====================================================

def create_alert(db: Session, alert):

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def get_alerts(db: Session):

    return (
        db.query(Alert)
        .order_by(Alert.created_at.desc())
        .all()
    )


# =====================================================
# USER ACTIVITY
# =====================================================

def log_activity(db: Session, activity):

    db.add(activity)
    db.commit()
    db.refresh(activity)

    return activity


def get_user_activity(db: Session):

    return (
        db.query(UserActivity)
        .order_by(UserActivity.created_at.desc())
        .all()
    )