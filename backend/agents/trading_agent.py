"""
trading_agent.py
-----------------------------------
WATT LINK - Agentic AI Trading Agent

Responsibilities:
1. Detect energy surplus/deficit
2. Decide Buy/Sell/Store
3. Recommend peer-to-peer trading
4. Calculate dynamic energy price
"""

from datetime import datetime


class TradingAgent:

    def __init__(self):

        self.base_price = 8.0          # ₹/kWh
        self.min_battery = 30          # %
        self.full_battery = 90         # %

    # =====================================================
    # Trading Analysis
    # =====================================================

    def analyze(
        self,
        solar_power: float,
        load_power: float,
        battery_level: float
    ):

        result = {

            "timestamp": datetime.now().isoformat(),

            "solar_power": solar_power,

            "load_power": load_power,

            "battery_level": battery_level,

            "surplus": 0,

            "deficit": 0,

            "action": "",

            "price": self.base_price,

            "buyer": None,

            "seller": None,

            "market_status": "IDLE",

            "recommendation": "",

            "message": ""

        }

        # -------------------------------------------------
        # Surplus Energy
        # -------------------------------------------------

        if solar_power > load_power:

            surplus = solar_power - load_power

            result["surplus"] = surplus

            if battery_level < self.full_battery:

                result["action"] = "STORE"

                result["market_status"] = "NO_TRADE"

                result["recommendation"] = (
                    "Store surplus energy in battery."
                )

                result["message"] = (
                    "Battery has available capacity."
                )

            else:

                result["action"] = "SELL"

                result["market_status"] = "SELL"

                result["price"] = self.calculate_price(
                    surplus,
                    battery_level
                )

                result["recommendation"] = (
                    "Sell surplus energy to nearby house."
                )

                result["message"] = (
                    "Battery is full. Export energy."
                )

        # -------------------------------------------------
        # Energy Deficit
        # -------------------------------------------------

        elif load_power > solar_power:

            deficit = load_power - solar_power

            result["deficit"] = deficit

            if battery_level > self.min_battery:

                result["action"] = "USE_BATTERY"

                result["market_status"] = "NO_TRADE"

                result["recommendation"] = (
                    "Supply load using battery."
                )

                result["message"] = (
                    "Battery has sufficient charge."
                )

            else:

                result["action"] = "BUY"

                result["market_status"] = "BUY"

                result["price"] = self.calculate_price(
                    deficit,
                    battery_level
                )

                result["recommendation"] = (
                    "Purchase energy from marketplace."
                )

                result["message"] = (
                    "Battery low. Buy energy."
                )

        # -------------------------------------------------
        # Balanced
        # -------------------------------------------------

        else:

            result["action"] = "NO_ACTION"

            result["market_status"] = "BALANCED"

            result["recommendation"] = (
                "No trading required."
            )

            result["message"] = (
                "Generation equals consumption."
            )

        return result

    # =====================================================
    # Dynamic Pricing
    # =====================================================

    def calculate_price(
        self,
        energy: float,
        battery_level: float
    ):

        price = self.base_price

        if energy > 1000:

            price += 2

        elif energy > 500:

            price += 1

        if battery_level < 20:

            price += 2

        return round(price, 2)

    # =====================================================
    # Trade Matching
    # =====================================================

    def match_trade(
        self,
        seller_house: str,
        buyer_house: str,
        energy: float
    ):

        return {

            "seller": seller_house,

            "buyer": buyer_house,

            "energy": energy,

            "status": "MATCHED"

        }

    # =====================================================
    # Market Summary
    # =====================================================

    def market_summary(
        self,
        solar_power,
        load_power,
        battery_level
    ):

        decision = self.analyze(
            solar_power,
            load_power,
            battery_level
        )

        return {

            "action": decision["action"],

            "market_status": decision["market_status"],

            "price": decision["price"],

            "recommendation": decision["recommendation"]

        }

    # =====================================================
    # Trade Profit Estimation
    # =====================================================

    def estimate_profit(
        self,
        energy,
        price
    ):

        return round((energy / 1000) * price, 2)


# =====================================================
# Testing
# =====================================================

if __name__ == "__main__":

    agent = TradingAgent()

    result = agent.analyze(

        solar_power=1200,

        load_power=500,

        battery_level=95

    )

    from pprint import pprint

    pprint(result)

    print("\nTrade Summary")

    pprint(

        agent.market_summary(

            solar_power=1200,

            load_power=500,

            battery_level=95

        )

    )

    print("\nEstimated Profit")

    print(

        agent.estimate_profit(

            result["surplus"],

            result["price"]

        )

    )