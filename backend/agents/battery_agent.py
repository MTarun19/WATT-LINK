"""
battery_agent.py
----------------
WATT LINK - Agentic AI Battery Agent

Responsibilities:
1. Monitor battery percentage
2. Decide charging/discharging
3. Protect battery health
4. Return battery decision to AI Manager
"""

from datetime import datetime


class BatteryAgent:

    def __init__(self):
        self.min_battery = 20       # %
        self.max_battery = 90       # %
        self.critical_battery = 10  # %

    def analyze(self, battery_level: float,
                solar_power: float,
                load_power: float):
        """
        Analyze battery state and return decision.

        Parameters
        ----------
        battery_level : float
            Battery percentage (0-100)

        solar_power : float
            Solar generation (Watts)

        load_power : float
            Current load demand (Watts)
        """

        decision = {
            "timestamp": datetime.now().isoformat(),
            "battery_level": battery_level,
            "solar_power": solar_power,
            "load_power": load_power,
            "status": "",
            "action": "",
            "reason": ""
        }

        # ----------------------------------------
        # Critical Battery
        # ----------------------------------------

        if battery_level <= self.critical_battery:

            decision["status"] = "CRITICAL"

            decision["action"] = "CHARGE_IMMEDIATELY"

            decision["reason"] = (
                "Battery below critical level."
            )

            return decision

        # ----------------------------------------
        # Low Battery
        # ----------------------------------------

        if battery_level < self.min_battery:

            if solar_power > load_power:

                decision["status"] = "LOW"

                decision["action"] = "CHARGE"

                decision["reason"] = (
                    "Excess solar available."
                )

            else:

                decision["status"] = "LOW"

                decision["action"] = "USE_GRID"

                decision["reason"] = (
                    "Solar insufficient. Use grid."
                )

            return decision

        # ----------------------------------------
        # High Battery
        # ----------------------------------------

        if battery_level >= self.max_battery:

            decision["status"] = "FULL"

            decision["action"] = "STOP_CHARGING"

            decision["reason"] = (
                "Battery fully charged."
            )

            return decision

        # ----------------------------------------
        # Normal Condition
        # ----------------------------------------

        if solar_power > load_power:

            decision["status"] = "NORMAL"

            decision["action"] = "CHARGE"

            decision["reason"] = (
                "Store excess solar energy."
            )

        elif load_power > solar_power:

            decision["status"] = "NORMAL"

            decision["action"] = "DISCHARGE"

            decision["reason"] = (
                "Supply power from battery."
            )

        else:

            decision["status"] = "STABLE"

            decision["action"] = "IDLE"

            decision["reason"] = (
                "Generation equals consumption."
            )

        return decision

    # ----------------------------------------

    def battery_health(self, battery_level):

        """
        Estimate battery health.
        """

        if battery_level >= 80:
            return "Excellent"

        elif battery_level >= 50:
            return "Good"

        elif battery_level >= 20:
            return "Fair"

        return "Poor"