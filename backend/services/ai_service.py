"""
ai_service.py
-----------------------------------
WATT LINK AI Service

Responsibilities
1. Execute AI Manager
2. Execute individual AI agents
3. Return AI decisions
"""

from agents.manager import AIManager


class AIService:

    def __init__(self):
        self.manager = AIManager()

    # =====================================================
    # Run Complete AI Engine
    # =====================================================

    def run_ai(self, sensor_data: dict):

        return self.manager.run(sensor_data)

    # =====================================================
    # Forecast Agent
    # =====================================================

    def forecast(self, sensor_data: dict):

        return self.manager.forecast_agent.analyze(

            solar_power=sensor_data["solar_power"],

            load_power=sensor_data["load_power"],

            battery_level=sensor_data["battery_level"],

            hour=sensor_data["hour"]

        )

    # =====================================================
    # Battery Agent
    # =====================================================

    def battery(self, sensor_data: dict):

        return self.manager.battery_agent.analyze(

            battery_level=sensor_data["battery_level"],

            solar_power=sensor_data["solar_power"],

            load_power=sensor_data["load_power"]

        )

    # =====================================================
    # Load Agent
    # =====================================================

    def load(self, sensor_data: dict):

        return self.manager.load_agent.analyze(

            load_power=sensor_data["load_power"],

            solar_power=sensor_data["solar_power"],

            battery_level=sensor_data["battery_level"]

        )

    # =====================================================
    # Trading Agent
    # =====================================================

    def trading(self, sensor_data: dict):

        return self.manager.trading_agent.analyze(

            solar_power=sensor_data["solar_power"],

            load_power=sensor_data["load_power"],

            battery_level=sensor_data["battery_level"]

        )

    # =====================================================
    # Fault Agent
    # =====================================================

    def fault(self, sensor_data: dict):

        return self.manager.fault_agent.analyze(

            voltage=sensor_data["voltage"],

            current=sensor_data["current"],

            battery_level=sensor_data["battery_level"],

            temperature=sensor_data["temperature"],

            communication_status=sensor_data["communication_status"],

            relay_status=sensor_data["relay_status"]

        )

    # =====================================================
    # Security Agent
    # =====================================================

    def security(self, sensor_data: dict):

        return self.manager.security_agent.analyze(

            authenticated=sensor_data["authenticated"]

        )

    # =====================================================
    # AI System Status
    # =====================================================

    def status(self):

        return {

            "status": "ONLINE",

            "engine": "WATT LINK Agentic AI",

            "agents": [

                "Forecast Agent",

                "Battery Agent",

                "Trading Agent",

                "Load Agent",

                "Fault Agent",

                "Security Agent"

            ]

        }