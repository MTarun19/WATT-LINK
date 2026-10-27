"""
sensor_service.py
-----------------------------------
WATT LINK Sensor Service
"""

from sqlalchemy.orm import Session
from sqlalchemy import func

from models import SensorData


class SensorService:

    # =====================================================
    # Save Sensor Data
    # =====================================================

    def save_sensor_data(
        self,
        db: Session,
        sensor_data: dict
    ):

        sensor = SensorData(
            voltage=sensor_data["voltage"],
            current=sensor_data["current"],
            power=sensor_data["power"],
            energy=sensor_data["energy"],
            solar_power=sensor_data["solar_power"],
            load_power=sensor_data["load_power"],
            battery_level=sensor_data["battery_level"],
            temperature=sensor_data["temperature"],
            humidity=sensor_data["humidity"]
        )

        db.add(sensor)
        db.commit()
        db.refresh(sensor)

        return sensor

    # =====================================================
    # Latest Sensor Reading
    # =====================================================

    def get_latest(self, db: Session):

        return (
            db.query(SensorData)
            .order_by(SensorData.id.desc())
            .first()
        )

    # =====================================================
    # Sensor History
    # =====================================================

    def get_history(
        self,
        db: Session,
        limit: int = 100
    ):

        return (
            db.query(SensorData)
            .order_by(SensorData.id.desc())
            .limit(limit)
            .all()
        )

    # =====================================================
    # Get Sensor by ID
    # =====================================================

    def get_by_id(
        self,
        db: Session,
        sensor_id: int
    ):

        return (
            db.query(SensorData)
            .filter(SensorData.id == sensor_id)
            .first()
        )

    # =====================================================
    # Delete Sensor Record
    # =====================================================

    def delete(
        self,
        db: Session,
        sensor_id: int
    ):

        sensor = self.get_by_id(db, sensor_id)

        if not sensor:
            return False

        db.delete(sensor)
        db.commit()

        return True

    # =====================================================
    # Dashboard Statistics
    # =====================================================

    def statistics(
        self,
        db: Session
    ):

        total_records = db.query(SensorData).count()

        latest = self.get_latest(db)

        avg_voltage = db.query(
            func.avg(SensorData.voltage)
        ).scalar()

        avg_current = db.query(
            func.avg(SensorData.current)
        ).scalar()

        avg_power = db.query(
            func.avg(SensorData.power)
        ).scalar()

        return {

            "total_records": total_records,

            "latest": latest,

            "average_voltage": round(avg_voltage or 0, 2),

            "average_current": round(avg_current or 0, 2),

            "average_power": round(avg_power or 0, 2)
        }

    # =====================================================
    # AI Input
    # =====================================================

    def get_ai_input(
        self,
        db: Session
    ):

        latest = self.get_latest(db)

        if latest is None:
            return None

        return {

            "voltage": latest.voltage,

            "current": latest.current,

            "power": latest.power,

            "energy": latest.energy,

            "solar_power": latest.solar_power,

            "load_power": latest.load_power,

            "battery_level": latest.battery_level,

            "temperature": latest.temperature,

            "humidity": latest.humidity,

            "hour": latest.created_at.hour,

            "communication_status": True,

            "relay_status": True,

            "authenticated": True
        }