from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from agents.manager import AIManager

router = APIRouter(
    prefix="/ai",
    tags=["Agentic AI"]
)

manager = AIManager()


# ==========================================================
# Request Model
# ==========================================================

class SensorInput(BaseModel):
    voltage: float
    current: float
    temperature: float
    solar_power: float
    load_power: float
    battery_level: float
    hour: int
    communication_status: bool
    relay_status: bool
    authenticated: bool


# ==========================================================
# Run Complete AI Engine
# ==========================================================

@router.post("/run")
def run_ai(data: SensorInput):

    try:

        result = manager.run(data.dict())

        return {
            "success": True,
            "message": "AI executed successfully.",
            "data": result
        }

    except Exception as e:

        raise HTTPException(
            status_code=500,
            detail=str(e)
        )


# ==========================================================
# Forecast Agent
# ==========================================================

@router.post("/forecast")
def forecast(data: SensorInput):

    return manager.forecast_agent.analyze(
        solar_power=data.solar_power,
        load_power=data.load_power,
        battery_level=data.battery_level,
        hour=data.hour
    )


# ==========================================================
# Battery Agent
# ==========================================================

@router.post("/battery")
def battery(data: SensorInput):

    return manager.battery_agent.analyze(
        battery_level=data.battery_level,
        solar_power=data.solar_power,
        load_power=data.load_power
    )


# ==========================================================
# Load Agent
# ==========================================================

@router.post("/load")
def load(data: SensorInput):

    return manager.load_agent.analyze(
        load_power=data.load_power,
        solar_power=data.solar_power,
        battery_level=data.battery_level
    )


# ==========================================================
# Trading Agent
# ==========================================================

@router.post("/trading")
def trading(data: SensorInput):

    return manager.trading_agent.analyze(
        solar_power=data.solar_power,
        load_power=data.load_power,
        battery_level=data.battery_level
    )


# ==========================================================
# Fault Agent
# ==========================================================

@router.post("/fault")
def fault(data: SensorInput):

    return manager.fault_agent.analyze(
        voltage=data.voltage,
        current=data.current,
        battery_level=data.battery_level,
        temperature=data.temperature,
        communication_status=data.communication_status,
        relay_status=data.relay_status
    )


# ==========================================================
# Security Agent
# ==========================================================

@router.post("/security")
def security(data: SensorInput):

    return manager.security_agent.analyze(
        authenticated=data.authenticated
    )


# ==========================================================
# AI Status
# ==========================================================

@router.get("/status")
def status():

    return {
        "status": "ONLINE",
        "engine": "WATT LINK Agentic AI",
        "agents": [
            "Forecast Agent",
            "Battery Agent",
            "Load Agent",
            "Trading Agent",
            "Fault Agent",
            "Security Agent"
        ]
    }