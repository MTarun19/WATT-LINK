"""
battery_service.py
-----------------------------------
WATT LINK Battery Service
"""

from sqlalchemy.orm import Session

from models import Battery
from agents.battery_agent import BatteryAgent


class BatteryService:

    def __init__(self):
        self.agent = BatteryAgent()

    # =====================================================
    # Get Battery by House
    # =====================================================

    def get_battery(self, db: Session, house_id: int):

        battery = db.query(Battery).filter(
            Battery.house_id == house_id
        ).first()

        return battery

    # =====================================================
    # Update Battery Level
    # =====================================================

    def update_battery(
        self,
        db: Session,
        house_id: int,
        battery_level: float
    ):

        battery = self.get_battery(db, house_id)

        if not battery:
            return None

        battery.battery_level = battery_level

        db.commit()

        db.refresh(battery)

        return battery

    # =====================================================
    # Run Battery AI
    # =====================================================

    def analyze(
        self,
        battery_level: float,
        solar_power: float,
        load_power: float
    ):

        return self.agent.analyze(

            battery_level=battery_level,

            solar_power=solar_power,

            load_power=load_power

        )

    # =====================================================
    # Charge Battery
    # =====================================================

    def charge(
        self,
        db: Session,
        house_id: int,
        amount: float
    ):

        battery = self.get_battery(db, house_id)

        if not battery:
            return None

        battery.battery_level += amount

        if battery.battery_level > 100:
            battery.battery_level = 100

        db.commit()

        db.refresh(battery)

        return battery

    # =====================================================
    # Discharge Battery
    # =====================================================

    def discharge(
        self,
        db: Session,
        house_id: int,
        amount: float
    ):

        battery = self.get_battery(db, house_id)

        if not battery:
            return None

        battery.battery_level -= amount

        if battery.battery_level < 0:
            battery.battery_level = 0

        db.commit()

        db.refresh(battery)

        return battery

    # =====================================================
    # Battery Health
    # =====================================================

    def health(
        self,
        battery_level: float
    ):

        return self.agent.battery_health(
            battery_level
        )