"""
manager.py
-----------------------------------
WATT LINK - Agentic AI Manager

Purpose:
    Monitor the WATT LINK microgrid by coordinating
    all specialist AI agents.

The manager OBSERVES and ANALYZES the system.
It does not directly control hardware.
"""

from datetime import datetime

from agents.forecast_agent import ForecastAgent
from agents.battery_agent import BatteryAgent
from agents.load_agent import LoadAgent
from agents.trading_agent import TradingAgent
from agents.fault_agent import FaultAgent
from agents.security_agent import SecurityAgent


class AIManager:

    def __init__(self):

        self.forecast_agent = ForecastAgent()
        self.battery_agent = BatteryAgent()
        self.load_agent = LoadAgent()
        self.trading_agent = TradingAgent()
        self.fault_agent = FaultAgent()
        self.security_agent = SecurityAgent()

    # ==========================================================
    # Monitor Complete Microgrid
    # ==========================================================

    def run(self, sensor_data: dict):

        forecast = self.forecast_agent.analyze(
            solar_power=sensor_data["solar_power"],
            load_power=sensor_data["load_power"],
            battery_level=sensor_data["battery_level"],
            hour=sensor_data["hour"]
        )

        battery = self.battery_agent.analyze(
            battery_level=sensor_data["battery_level"],
            solar_power=sensor_data["solar_power"],
            load_power=sensor_data["load_power"]
        )

        load = self.load_agent.analyze(
            load_power=sensor_data["load_power"],
            solar_power=sensor_data["solar_power"],
            battery_level=sensor_data["battery_level"]
        )

        trading = self.trading_agent.analyze(
            solar_power=sensor_data["solar_power"],
            load_power=sensor_data["load_power"],
            battery_level=sensor_data["battery_level"]
        )

        fault = self.fault_agent.analyze(
            voltage=sensor_data["voltage"],
            current=sensor_data["current"],
            battery_level=sensor_data["battery_level"],
            temperature=sensor_data["temperature"],
            communication_status=sensor_data["communication_status"],
            relay_status=sensor_data["relay_status"]
        )

        security = self.security_agent.analyze(
            authenticated=sensor_data["authenticated"]
        )

        monitoring = self.make_decision(
            forecast=forecast,
            battery=battery,
            load=load,
            trading=trading,
            fault=fault,
            security=security
        )

        return {
            "timestamp": datetime.now().isoformat(),

            "mode": "MONITORING",

            "system": {
                "voltage": sensor_data["voltage"],
                "current": sensor_data["current"],
                "temperature": sensor_data["temperature"],
                "solar_power": sensor_data["solar_power"],
                "load_power": sensor_data["load_power"],
                "battery_level": sensor_data["battery_level"],
                "communication_status": sensor_data["communication_status"],
                "relay_status": sensor_data["relay_status"]
            },

            "agents": {
                "forecast": forecast,
                "battery": battery,
                "load": load,
                "trading": trading,
                "fault": fault,
                "security": security
            },

            "monitoring": monitoring
        }

    # ==========================================================
    # AI Monitoring Decision
    # ==========================================================

    def make_decision(
        self,
        forecast,
        battery,
        load,
        trading,
        fault,
        security
    ):

        # ------------------------------------------------------
        # 1. Critical Fault
        # ------------------------------------------------------

        if fault.get("severity") == "CRITICAL":

            return {
                "status": "CRITICAL",
                "recommendation": "EMERGENCY_SHUTDOWN",
                "message": "Critical electrical fault detected."
            }

        # ------------------------------------------------------
        # 2. Security
        # ------------------------------------------------------

        if security.get("status") != "AUTHORIZED":

            return {
                "status": "SECURITY_ALERT",
                "recommendation": "ACCESS_DENIED",
                "message": "Unauthorized access detected."
            }

        # ------------------------------------------------------
        # 3. Battery Monitoring
        # ------------------------------------------------------

        if battery.get("action") == "CHARGE":

            return {
                "status": "NORMAL",
                "recommendation": "CHARGE_BATTERY",
                "message": battery.get("reason")
            }

        if battery.get("action") == "DISCHARGE":

            return {
                "status": "NORMAL",
                "recommendation": "DISCHARGE_BATTERY",
                "message": battery.get("reason")
            }

        # ------------------------------------------------------
        # 4. Trading Monitoring
        # ------------------------------------------------------

        if trading.get("action") == "SELL":

            return {
                "status": "OPPORTUNITY",
                "recommendation": "SELL_ENERGY",
                "message": trading.get("reason")
            }

        if trading.get("action") == "BUY":

            return {
                "status": "OPPORTUNITY",
                "recommendation": "BUY_ENERGY",
                "message": trading.get("reason")
            }

        # ------------------------------------------------------
        # 5. Normal Operation
        # ------------------------------------------------------

        return {
            "status": "NORMAL",
            "recommendation": "NO_ACTION",
            "message": "Microgrid operating normally."
        }


# ==========================================================
# Test
# ==========================================================

if __name__ == "__main__":

    manager = AIManager()

    sample_data = {
        "voltage": 230,
        "current": 5,
        "temperature": 30,

        "solar_power": 850,
        "load_power": 420,
        "battery_level": 70,

        "hour": 12,

        "communication_status": True,
        "relay_status": True,

        "authenticated": True
    }

    result = manager.run(sample_data)

    from pprint import pprint

    pprint(result)