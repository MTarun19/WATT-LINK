"""
relay_router.py
-----------------------------------
WATT LINK Relay Control Router
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(
    prefix="/relay",
    tags=["Relay Control"]
)

# =====================================================
# Relay Data (Simulation)
# =====================================================

relay_states = {
    1: {
        "name": "Living Room Light",
        "status": "OFF"
    },
    2: {
        "name": "Fan",
        "status": "OFF"
    },
    3: {
        "name": "Charging Circuit",
        "status": "OFF"
    },
    4: {
        "name": "Water Pump",
        "status": "OFF"
    }
}


# =====================================================
# Request Model
# =====================================================

class RelayRequest(BaseModel):
    relay_id: int
    status: str


# =====================================================
# Helper Function
# =====================================================

def relay_exists(relay_id: int):

    if relay_id not in relay_states:

        raise HTTPException(
            status_code=404,
            detail="Relay not found."
        )


# =====================================================
# Get All Relays
# =====================================================

@router.get("/")
def get_relays():

    return {

        "timestamp": datetime.utcnow(),

        "total_relays": len(relay_states),

        "relays": relay_states

    }


# =====================================================
# Get Single Relay
# =====================================================

@router.get("/{relay_id}")
def get_relay(relay_id: int):

    relay_exists(relay_id)

    return relay_states[relay_id]


# =====================================================
# Control Relay
# =====================================================

@router.post("/control")
def control_relay(request: RelayRequest):

    relay_exists(request.relay_id)

    status = request.status.upper()

    if status not in ["ON", "OFF"]:

        raise HTTPException(
            status_code=400,
            detail="Status must be ON or OFF."
        )

    relay_states[request.relay_id]["status"] = status

    return {

        "message": "Relay updated successfully.",

        "relay": relay_states[request.relay_id],

        "updated_at": datetime.utcnow()

    }


# =====================================================
# Toggle Relay
# =====================================================

@router.put("/toggle/{relay_id}")
def toggle_relay(relay_id: int):

    relay_exists(relay_id)

    current = relay_states[relay_id]["status"]

    relay_states[relay_id]["status"] = (
        "OFF"
        if current == "ON"
        else "ON"
    )

    return {

        "message": "Relay toggled successfully.",

        "relay": relay_states[relay_id],

        "updated_at": datetime.utcnow()

    }


# =====================================================
# Turn ON All Relays
# =====================================================

@router.post("/all-on")
def all_on():

    for relay in relay_states.values():

        relay["status"] = "ON"

    return {

        "message": "All relays turned ON.",

        "relays": relay_states

    }


# =====================================================
# Turn OFF All Relays
# =====================================================

@router.post("/all-off")
def all_off():

    for relay in relay_states.values():

        relay["status"] = "OFF"

    return {

        "message": "All relays turned OFF.",

        "relays": relay_states

    }


# =====================================================
# Emergency Shutdown
# =====================================================

@router.post("/shutdown")
def emergency_shutdown():

    for relay in relay_states.values():

        relay["status"] = "OFF"

    return {

        "message": "Emergency shutdown completed.",

        "timestamp": datetime.utcnow(),

        "relays": relay_states

    }


# =====================================================
# Reset Relays
# =====================================================

@router.post("/reset")
def reset_relays():

    for relay in relay_states.values():

        relay["status"] = "OFF"

    return {

        "message": "Relays reset successfully.",

        "relays": relay_states

    }


# =====================================================
# Relay Statistics
# =====================================================

@router.get("/stats")
def relay_statistics():

    active = sum(
        relay["status"] == "ON"
        for relay in relay_states.values()
    )

    inactive = len(relay_states) - active

    return {

        "total_relays": len(relay_states),

        "active_relays": active,

        "inactive_relays": inactive,

        "timestamp": datetime.utcnow()

    }


# =====================================================
# AI Recommended Relay Control
# =====================================================

@router.post("/ai-control")
def ai_control(relay_id: int, action: str):

    relay_exists(relay_id)

    action = action.upper()

    if action not in ["ON", "OFF"]:

        raise HTTPException(
            status_code=400,
            detail="Action must be ON or OFF."
        )

    relay_states[relay_id]["status"] = action

    return {

        "message": "Relay updated by AI.",

        "relay": relay_states[relay_id],

        "timestamp": datetime.utcnow()

    }