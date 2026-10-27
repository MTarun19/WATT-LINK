"""
load_agent.py
-----------------------------------
WATT LINK - Agentic AI Load Agent

Responsibilities:
1. Monitor current load
2. Classify load level
3. Manage appliance priority
4. Recommend load shedding
5. Optimize power consumption
"""

from datetime import datetime


class LoadAgent:

    def __init__(self):

        self.HIGH_LOAD = 700
        self.MEDIUM_LOAD = 400

    # =====================================================
    # Analyze Load
    # =====================================================

    def analyze(
        self,
        load_power: float,
        solar_power: float,
        battery_level: float
    ):

        result = {

            "timestamp": datetime.now().isoformat(),

            "load_power": load_power,

            "solar_power": solar_power,

            "battery_level": battery_level,

            "load_status": "",

            "action": "",

            "recommendation": "",

            "essential_loads": [
                "Lights",
                "Fan",
                "WiFi Router"
            ],

            "non_essential_loads": [
                "Air Conditioner",
                "Water Heater",
                "Washing Machine"
            ],

            "loads_to_turn_off": [],

            "power_balance": solar_power - load_power

        }

        # -------------------------------------------------
        # Load Classification
        # -------------------------------------------------

        if load_power >= self.HIGH_LOAD:

            result["load_status"] = "HIGH"

        elif load_power >= self.MEDIUM_LOAD:

            result["load_status"] = "MEDIUM"

        else:

            result["load_status"] = "LOW"

        # -------------------------------------------------
        # Decision Logic
        # -------------------------------------------------

        if solar_power >= load_power:

            result["action"] = "NORMAL"

            result["recommendation"] = (
                "Solar generation is sufficient. Keep all loads ON."
            )

        else:

            if battery_level >= 50:

                result["action"] = "USE_BATTERY"

                result["recommendation"] = (
                    "Use battery to meet additional demand."
                )

            elif battery_level >= 20:

                result["action"] = "LIMIT_NON_ESSENTIAL"

                result["recommendation"] = (
                    "Disable non-essential appliances."
                )

                result["loads_to_turn_off"] = [
                    "Air Conditioner",
                    "Water Heater"
                ]

            else:

                result["action"] = "LOAD_SHEDDING"

                result["recommendation"] = (
                    "Battery critically low. Keep only essential loads ON."
                )

                result["loads_to_turn_off"] = [
                    "Air Conditioner",
                    "Water Heater",
                    "Washing Machine",
                    "Television"
                ]

        return result

    # =====================================================
    # Appliance Priority
    # =====================================================

    def prioritize_loads(self):

        return {

            "Lights": 1,

            "Fan": 1,

            "WiFi Router": 1,

            "Refrigerator": 2,

            "Laptop Charger": 3,

            "Television": 3,

            "Air Conditioner": 4,

            "Water Heater": 5,

            "Washing Machine": 6

        }

    # =====================================================
    # Loads to Turn Off
    # =====================================================

    def loads_to_turn_off(self, battery_level):

        if battery_level >= 50:

            return []

        elif battery_level >= 20:

            return [
                "Air Conditioner",
                "Water Heater"
            ]

        else:

            return [
                "Air Conditioner",
                "Water Heater",
                "Washing Machine",
                "Television"
            ]

    # =====================================================
    # Calculate Load Efficiency
    # =====================================================

    def load_efficiency(
        self,
        solar_power,
        load_power
    ):

        if load_power == 0:
            return 100.0

        efficiency = (solar_power / load_power) * 100

        return round(min(efficiency, 100), 2)

    # =====================================================
    # Summary
    # =====================================================

    def summary(
        self,
        solar_power,
        load_power,
        battery_level
    ):

        decision = self.analyze(
            load_power,
            solar_power,
            battery_level
        )

        return {

            "status": decision["load_status"],

            "action": decision["action"],

            "recommendation": decision["recommendation"],

            "efficiency": self.load_efficiency(
                solar_power,
                load_power
            )

        }


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    agent = LoadAgent()

    result = agent.analyze(

        load_power=650,

        solar_power=500,

        battery_level=35

    )

    from pprint import pprint

    pprint(result)

    print("\nPriority List")

    pprint(agent.prioritize_loads())

    print("\nSummary")

    pprint(

        agent.summary(

            solar_power=500,

            load_power=650,

            battery_level=35

        )

    )