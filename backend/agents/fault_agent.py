"""
fault_agent.py
-----------------------------------
WATT LINK - Agentic AI Fault Detection Agent

Responsibilities:
1. Detect voltage abnormalities
2. Detect current overload
3. Detect battery issues
4. Detect temperature issues
5. Detect communication failure
6. Detect relay failure
7. Generate alerts
"""

from datetime import datetime


class FaultAgent:

    def __init__(self):

        self.MIN_VOLTAGE = 180
        self.MAX_VOLTAGE = 260

        self.MAX_CURRENT = 15

        self.MAX_TEMPERATURE = 60

        self.MIN_BATTERY = 15

    # ==========================================================
    # Analyze System Faults
    # ==========================================================

    def analyze(
        self,
        voltage: float,
        current: float,
        battery_level: float,
        temperature: float,
        communication_status: bool,
        relay_status: bool
    ):

        faults = []

        severity = "NORMAL"

        action = "NONE"

        reason = "System operating normally."

        # ------------------------------------------------------
        # Voltage Check
        # ------------------------------------------------------

        if voltage < self.MIN_VOLTAGE:

            faults.append({
                "type": "LOW_VOLTAGE",
                "message": "Voltage is below safe operating range."
            })

        elif voltage > self.MAX_VOLTAGE:

            faults.append({
                "type": "HIGH_VOLTAGE",
                "message": "Voltage exceeds safe operating range."
            })

        # ------------------------------------------------------
        # Current Check
        # ------------------------------------------------------

        if current > self.MAX_CURRENT:

            faults.append({
                "type": "OVER_CURRENT",
                "message": "Current exceeds safe operating limit."
            })

        # ------------------------------------------------------
        # Battery Check
        # ------------------------------------------------------

        if battery_level < self.MIN_BATTERY:

            faults.append({
                "type": "LOW_BATTERY",
                "message": "Battery level is critically low."
            })

        # ------------------------------------------------------
        # Temperature Check
        # ------------------------------------------------------

        if temperature > self.MAX_TEMPERATURE:

            faults.append({
                "type": "HIGH_TEMPERATURE",
                "message": "Temperature exceeds safe limit."
            })

        # ------------------------------------------------------
        # Communication Check
        # ------------------------------------------------------

        if not communication_status:

            faults.append({
                "type": "COMMUNICATION_FAILURE",
                "message": "ESP32 communication lost."
            })

        # ------------------------------------------------------
        # Relay Check
        # ------------------------------------------------------

        if not relay_status:

            faults.append({
                "type": "RELAY_FAILURE",
                "message": "Relay is not responding."
            })

        # ------------------------------------------------------
        # Calculate Severity
        # ------------------------------------------------------

        count = len(faults)

        if count == 0:

            severity = "NORMAL"

            action = "NONE"

            reason = "No faults detected."

        elif count == 1:

            severity = "LOW"

            action = "MONITOR"

            reason = "Minor fault detected. Monitor the system."

        elif count <= 3:

            severity = "MEDIUM"

            action = "WARNING"

            reason = "Multiple faults detected. Maintenance recommended."

        else:

            severity = "CRITICAL"

            action = "SHUTDOWN"

            reason = "Critical faults detected. Emergency shutdown required."

        # ------------------------------------------------------
        # Return Result
        # ------------------------------------------------------

        return {

            "timestamp": datetime.now().isoformat(),

            "severity": severity,

            "action": action,

            "reason": reason,

            "fault_count": count,

            "faults": faults,

            "system_status": (
                "HEALTHY"
                if count == 0
                else "FAULT_DETECTED"
            )

        }

    # ==========================================================
    # Utility Function
    # ==========================================================

    def has_critical_fault(self, result):

        return result.get("severity") == "CRITICAL"


# ==========================================================
# Testing
# ==========================================================

if __name__ == "__main__":

    agent = FaultAgent()

    result = agent.analyze(

        voltage=270,

        current=18,

        battery_level=10,

        temperature=70,

        communication_status=False,

        relay_status=False

    )

    from pprint import pprint

    pprint(result)