"""
helpers.py
-----------------------------------
WATT LINK Helper Functions
"""

from datetime import datetime
import uuid


# =====================================================
# Current Timestamp
# =====================================================

def current_timestamp():
    """
    Returns current timestamp.
    """
    return datetime.now()


# =====================================================
# Generate Transaction ID
# =====================================================

def generate_transaction_id():

    return f"TXN-{uuid.uuid4().hex[:10].upper()}"


# =====================================================
# Round Float Values
# =====================================================

def round_value(value, digits=2):

    if value is None:
        return 0

    return round(value, digits)


# =====================================================
# Battery Percentage Validation
# =====================================================

def validate_battery(level):

    if level < 0:
        return 0

    if level > 100:
        return 100

    return level


# =====================================================
# Voltage Status
# =====================================================

def voltage_status(voltage):

    if voltage < 180:
        return "LOW"

    elif voltage > 250:
        return "HIGH"

    return "NORMAL"


# =====================================================
# Temperature Status
# =====================================================

def temperature_status(temp):

    if temp < 15:
        return "LOW"

    elif temp > 45:
        return "HIGH"

    return "NORMAL"


# =====================================================
# Calculate Power
# =====================================================

def calculate_power(voltage, current):

    return round(voltage * current, 2)


# =====================================================
# Energy Cost
# =====================================================

def calculate_cost(energy, price_per_kwh):

    return round(energy * price_per_kwh, 2)


# =====================================================
# Energy Surplus
# =====================================================

def energy_surplus(solar_power, load_power):

    return round(solar_power - load_power, 2)


# =====================================================
# Energy Deficit
# =====================================================

def energy_deficit(solar_power, load_power):

    return round(load_power - solar_power, 2)


# =====================================================
# Battery Health
# =====================================================

def battery_health(level):

    if level >= 80:
        return "EXCELLENT"

    elif level >= 60:
        return "GOOD"

    elif level >= 30:
        return "LOW"

    return "CRITICAL"


# =====================================================
# Generate AI Response
# =====================================================

def ai_response(status, action, message):

    return {

        "status": status,

        "action": action,

        "message": message,

        "timestamp": current_timestamp()

    }


# =====================================================
# Success Response
# =====================================================

def success_response(message, data=None):

    return {

        "success": True,

        "message": message,

        "data": data

    }


# =====================================================
# Error Response
# =====================================================

def error_response(message):

    return {

        "success": False,

        "message": message

    }


# =====================================================
# Relay Command
# =====================================================

def relay_command(relay_id, status):

    return {

        "relay_id": relay_id,

        "command": "ON" if status else "OFF"

    }


# =====================================================
# House Name
# =====================================================

def house_name(house_id):

    houses = {

        1: "House A",

        2: "House B",

        3: "House C"

    }

    return houses.get(house_id, "Unknown House")