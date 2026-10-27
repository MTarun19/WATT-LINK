"""
sensor_router.py
-----------------------------------
WATT LINK Sensor Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import SensorData
from schemas import (
    SensorDataCreate,
    SensorDataResponse,
)

router = APIRouter(
    prefix="/sensor",
    tags=["Sensors"]
)

# =====================================================
# Add Sensor Reading
# =====================================================

@router.post("/data", response_model=SensorDataResponse)
def add_sensor_data(
    sensor: SensorDataCreate,
    db: Session = Depends(get_db)
):

    new_data = SensorData(

        sensor_id=sensor.sensor_id,

        voltage=sensor.voltage,

        current=sensor.current,

        power=sensor.power,

        battery=sensor.battery,

        solar=sensor.solar,

        temperature=sensor.temperature

    )

    db.add(new_data)

    db.commit()

    db.refresh(new_data)

    return new_data


# =====================================================
# Latest Reading
# =====================================================

@router.get("/latest", response_model=SensorDataResponse)
def latest_sensor_data(

    db: Session = Depends(get_db)

):

    sensor = (

        db.query(SensorData)

        .order_by(SensorData.id.desc())

        .first()

    )

    if sensor is None:

        raise HTTPException(

            status_code=404,

            detail="No sensor data found."

        )

    return sensor


# =====================================================
# History
# =====================================================

@router.get("/history", response_model=list[SensorDataResponse])
def sensor_history(

    limit: int = 100,

    db: Session = Depends(get_db)

):

    return (

        db.query(SensorData)

        .order_by(SensorData.id.desc())

        .limit(limit)

        .all()

    )


# =====================================================
# Get by ID
# =====================================================

@router.get("/{sensor_id}", response_model=SensorDataResponse)
def sensor_by_id(

    sensor_id: int,

    db: Session = Depends(get_db)

):

    sensor = (

        db.query(SensorData)

        .filter(SensorData.id == sensor_id)

        .first()

    )

    if sensor is None:

        raise HTTPException(

            status_code=404,

            detail="Sensor record not found."

        )

    return sensor


# =====================================================
# Delete
# =====================================================

@router.delete("/{sensor_id}")
def delete_sensor(

    sensor_id: int,

    db: Session = Depends(get_db)

):

    sensor = (

        db.query(SensorData)

        .filter(SensorData.id == sensor_id)

        .first()

    )

    if sensor is None:

        raise HTTPException(

            status_code=404,

            detail="Sensor record not found."

        )

    db.delete(sensor)

    db.commit()

    return {

        "message": "Sensor record deleted successfully."

    }


# =====================================================
# Statistics
# =====================================================

@router.get("/statistics")
def statistics(

    db: Session = Depends(get_db)

):

    total = db.query(SensorData).count()

    latest = (

        db.query(SensorData)

        .order_by(SensorData.id.desc())

        .first()

    )

    if latest is None:

        return {

            "total_records": 0,

            "latest_voltage": 0,

            "latest_current": 0,

            "latest_power": 0,

            "battery": 0,

            "solar": 0,

            "temperature": 0

        }

    return {

        "total_records": total,

        "latest_voltage": latest.voltage,

        "latest_current": latest.current,

        "latest_power": latest.power,

        "battery": latest.battery,

        "solar": latest.solar,

        "temperature": latest.temperature

    }