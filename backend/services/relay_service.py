"""
relay_service.py
-----------------------------------
WATT LINK Relay Service
"""

from sqlalchemy.orm import Session

from models import Relay
from agents.load_agent import LoadAgent
from agents.fault_agent import FaultAgent


class RelayService:

    def __init__(self):
        self.load_agent = LoadAgent()
        self.fault_agent = FaultAgent()

    # =====================================================
    # Get Relay
    # =====================================================

    def get_relay(self, db: Session, relay_id: int):

        return db.query(Relay).filter(
            Relay.id == relay_id
        ).first()

    # =====================================================
    # Get All Relays
    # =====================================================

    def get_all_relays(self, db: Session):

        return db.query(Relay).all()

    # =====================================================
    # Turn Relay ON
    # =====================================================

    def turn_on(
        self,
        db: Session,
        relay_id: int
    ):

        relay = self.get_relay(db, relay_id)

        if not relay:
            return None

        relay.status = True

        db.commit()

        db.refresh(relay)

        return relay

    # =====================================================
    # Turn Relay OFF
    # =====================================================

    def turn_off(
        self,
        db: Session,
        relay_id: int
    ):

        relay = self.get_relay(db, relay_id)

        if not relay:
            return None

        relay.status = False

        db.commit()

        db.refresh(relay)

        return relay

    # =====================================================
    # Toggle Relay
    # =====================================================

    def toggle(
        self,
        db: Session,
        relay_id: int
    ):

        relay = self.get_relay(db, relay_id)

        if not relay:
            return None

        relay.status = not relay.status

        db.commit()

        db.refresh(relay)

        return relay

    # =====================================================
    # AI Load Control
    # =====================================================

    def load_decision(
        self,
        load_power: float,
        solar_power: float,
        battery_level: float
    ):

        return self.load_agent.analyze(
            load_power=load_power,
            solar_power=solar_power,
            battery_level=battery_level
        )

    # =====================================================
    # Emergency Shutdown
    # =====================================================

    def emergency_shutdown(
        self,
        db: Session
    ):

        relays = db.query(Relay).all()

        for relay in relays:
            relay.status = False

        db.commit()

        return {
            "status": "SUCCESS",
            "message": "All relays turned OFF."
        }

    # =====================================================
    # Fault Protection
    # =====================================================

    def fault_protection(
        self,
        voltage: float,
        current: float,
        battery_level: float,
        temperature: float,
        communication_status: bool,
        relay_status: bool
    ):

        return self.fault_agent.analyze(
            voltage=voltage,
            current=current,
            battery_level=battery_level,
            temperature=temperature,
            communication_status=communication_status,
            relay_status=relay_status
        )

    # =====================================================
    # Generate ESP32 Relay Command
    # =====================================================

    def relay_command(
        self,
        relay_id: int,
        status: bool
    ):

        return {
            "relay_id": relay_id,
            "command": "ON" if status else "OFF"
        }