"""
battery_router.py
-----------------------------------
WATT LINK Battery Management Router
"""

from datetime import datetime
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/battery",
    tags=["Battery Management"]
)

# =====================================================
# Simulated Battery
# =====================================================

battery = {
    "battery_id": 1,
    "capacity": 10.0,
    "current_level": 7.5,
    "percentage": 75.0,
    "voltage": 48.2,
    "current": 8.6,
    "temperature": 29.5,
    "status": "Charging",
    "health": "Good",
    "last_updated": datetime.utcnow()
}


# =====================================================
# Schemas
# =====================================================

class BatteryUpdate(BaseModel):
    current_level: float
    voltage: float
    current: float
    temperature: float


class BatteryAction(BaseModel):
    action: str


# =====================================================
# Internal Functions
# =====================================================

def calculate_percentage():

    battery["percentage"] = round(
        (battery["current_level"] / battery["capacity"]) * 100,
        2
    )


def update_health():

    if battery["temperature"] >= 50:
        battery["health"] = "Critical"

    elif battery["temperature"] >= 40:
        battery["health"] = "Warning"

    else:
        battery["health"] = "Good"


def update_status():

    if battery["current_level"] == battery["capacity"]:
        battery["status"] = "Full"

    elif battery["current_level"] <= 0:
        battery["status"] = "Empty"


# =====================================================
# Battery Status
# =====================================================

@router.get("/")
def get_battery():

    calculate_percentage()

    update_health()

    update_status()

    battery["last_updated"] = datetime.utcnow()

    return battery


# =====================================================
# Update Battery
# =====================================================

@router.put("/update")
def update_battery(data: BatteryUpdate):

    if data.current_level < 0:

        raise HTTPException(
            status_code=400,
            detail="Battery level cannot be negative."
        )

    if data.current_level > battery["capacity"]:

        raise HTTPException(
            status_code=400,
            detail="Battery exceeds capacity."
        )

    battery["current_level"] = data.current_level
    battery["voltage"] = data.voltage
    battery["current"] = data.current
    battery["temperature"] = data.temperature

    calculate_percentage()
    update_health()
    update_status()

    battery["last_updated"] = datetime.utcnow()

    return {
        "message": "Battery updated successfully.",
        "battery": battery
    }


# =====================================================
# Charge / Discharge
# =====================================================

@router.post("/action")
def battery_action(data: BatteryAction):

    action = data.action.upper()

    if action == "CHARGE":

        battery["status"] = "Charging"

    elif action == "DISCHARGE":

        battery["status"] = "Discharging"

    elif action == "IDLE":

        battery["status"] = "Idle"

    else:

        raise HTTPException(
            status_code=400,
            detail="Allowed actions: CHARGE, DISCHARGE, IDLE"
        )

    battery["last_updated"] = datetime.utcnow()

    return {
        "message": "Battery action updated.",
        "status": battery["status"]
    }


# =====================================================
# Battery Percentage
# =====================================================

@router.get("/percentage")
def battery_percentage():

    calculate_percentage()

    return {
        "battery_percentage": battery["percentage"]
    }


# =====================================================
# Battery Health
# =====================================================

@router.get("/health")
def battery_health():

    calculate_percentage()

    update_health()

    return {
        "health": battery["health"],
        "temperature": battery["temperature"],
        "voltage": battery["voltage"],
        "current": battery["current"],
        "percentage": battery["percentage"]
    }


# =====================================================
# AI Recommendation
# =====================================================

@router.get("/recommendation")
def battery_recommendation():

    calculate_percentage()

    percentage = battery["percentage"]

    if percentage < 20:

        recommendation = "Charge immediately."

    elif percentage < 50:

        recommendation = "Charge when solar power is available."

    elif percentage < 90:

        recommendation = "Battery operating normally."

    else:

        recommendation = "Battery is almost full."

    return {
        "battery_percentage": percentage,
        "recommendation": recommendation
    }


# =====================================================
# Statistics
# =====================================================

@router.get("/stats")
def battery_stats():

    calculate_percentage()

    update_health()

    update_status()

    return {

        "battery_id": battery["battery_id"],

        "capacity": battery["capacity"],

        "available_energy": battery["current_level"],

        "percentage": battery["percentage"],

        "status": battery["status"],

        "health": battery["health"],

        "voltage": battery["voltage"],

        "current": battery["current"],

        "temperature": battery["temperature"],

        "last_updated": datetime.utcnow()

    }