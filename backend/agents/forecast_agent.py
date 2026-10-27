"""
forecast_agent.py
----------------------------------
WATT LINK - Agentic AI Forecast Agent

Responsibilities:
1. Forecast solar generation
2. Forecast energy demand
3. Recommend energy actions
4. Predict energy surplus/deficit
"""

from datetime import datetime


class ForecastAgent:

    def __init__(self):

        self.HIGH_SOLAR = 800      # Watts
        self.MEDIUM_SOLAR = 400

        self.HIGH_LOAD = 700
        self.MEDIUM_LOAD = 350

    # ---------------------------------------------

    def analyze(
        self,
        solar_power: float,
        load_power: float,
        battery_level: float,
        hour: int
    ):
        """
        Analyze the current energy conditions and
        forecast the next action.
        """

        result = {

            "timestamp": datetime.now().isoformat(),

            "solar_power": solar_power,

            "load_power": load_power,

            "battery_level": battery_level,

            "forecast": "",

            "recommendation": "",

            "surplus": 0,

            "deficit": 0
        }

        # -----------------------------------------
        # Solar Forecast
        # -----------------------------------------

        if solar_power >= self.HIGH_SOLAR:

            solar_status = "HIGH"

        elif solar_power >= self.MEDIUM_SOLAR:

            solar_status = "MEDIUM"

        else:

            solar_status = "LOW"

        # -----------------------------------------
        # Load Forecast
        # -----------------------------------------

        if load_power >= self.HIGH_LOAD:

            load_status = "HIGH"

        elif load_power >= self.MEDIUM_LOAD:

            load_status = "MEDIUM"

        else:

            load_status = "LOW"

        # -----------------------------------------
        # Energy Balance
        # -----------------------------------------

        if solar_power > load_power:

            surplus = solar_power - load_power

            result["surplus"] = surplus

            result["forecast"] = "ENERGY_SURPLUS"

            if battery_level < 90:

                result["recommendation"] = (
                    "Charge Battery"
                )

            else:

                result["recommendation"] = (
                    "Sell Excess Energy"
                )

        elif load_power > solar_power:

            deficit = load_power - solar_power

            result["deficit"] = deficit

            result["forecast"] = "ENERGY_DEFICIT"

            if battery_level > 30:

                result["recommendation"] = (
                    "Use Battery"
                )

            else:

                result["recommendation"] = (
                    "Use Grid Power"
                )

        else:

            result["forecast"] = "BALANCED"

            result["recommendation"] = "No Action"

        # -----------------------------------------
        # Time-based Forecast
        # -----------------------------------------

        if 6 <= hour <= 10:

            result["next_period"] = (
                "Morning solar generation increasing."
            )

        elif 11 <= hour <= 15:

            result["next_period"] = (
                "Peak solar generation expected."
            )

        elif 16 <= hour <= 18:

            result["next_period"] = (
                "Solar generation decreasing."
            )

        else:

            result["next_period"] = (
                "Nighttime - rely on battery or grid."
            )

        # -----------------------------------------

        result["solar_status"] = solar_status

        result["load_status"] = load_status

        return result

    # ---------------------------------------------

    def predict_next_hour(
        self,
        solar_power: float,
        load_power: float
    ):
        """
        Simple next-hour prediction.
        Replace with ML model later.
        """

        predicted_solar = solar_power * 0.95

        predicted_load = load_power * 1.05

        return {

            "predicted_solar": round(predicted_solar, 2),

            "predicted_load": round(predicted_load, 2)

        }