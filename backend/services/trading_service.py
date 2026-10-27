"""
trading_service.py
-----------------------------------
WATT LINK Trading Service
"""

from sqlalchemy.orm import Session
from sqlalchemy import func

from models import Trading
from agents.trading_agent import TradingAgent


class TradingService:

    def __init__(self):
        self.agent = TradingAgent()

    # =====================================================
    # Create Trade
    # =====================================================

    def create_trade(
        self,
        db: Session,
        seller_id: int,
        buyer_id: int | None,
        energy: float,
        price: float,
        status: str = "AVAILABLE"
    ):

        trade = Trading(
            seller_id=seller_id,
            buyer_id=buyer_id,
            energy=energy,
            price=price,
            status=status
        )

        db.add(trade)
        db.commit()
        db.refresh(trade)

        return trade

    # =====================================================
    # Get Trade
    # =====================================================

    def get_trade(
        self,
        db: Session,
        trade_id: int
    ):

        return (
            db.query(Trading)
            .filter(Trading.id == trade_id)
            .first()
        )

    # =====================================================
    # Available Trades
    # =====================================================

    def available_trades(
        self,
        db: Session
    ):

        return (
            db.query(Trading)
            .filter(Trading.status == "AVAILABLE")
            .all()
        )

    # =====================================================
    # Buy Energy
    # =====================================================

    def buy_trade(
        self,
        db: Session,
        trade_id: int,
        buyer_id: int
    ):

        trade = self.get_trade(db, trade_id)

        if trade is None:
            return None

        if trade.status != "AVAILABLE":
            return None

        trade.buyer_id = buyer_id
        trade.status = "COMPLETED"

        db.commit()
        db.refresh(trade)

        return trade

    # =====================================================
    # Cancel Trade
    # =====================================================

    def cancel_trade(
        self,
        db: Session,
        trade_id: int
    ):

        trade = self.get_trade(db, trade_id)

        if trade is None:
            return False

        trade.status = "CANCELLED"

        db.commit()

        return True

    # =====================================================
    # Trading History
    # =====================================================

    def history(
        self,
        db: Session,
        limit: int = 100
    ):

        return (
            db.query(Trading)
            .order_by(Trading.id.desc())
            .limit(limit)
            .all()
        )

    # =====================================================
    # AI Trading Decision
    # =====================================================

    def analyze(
        self,
        solar_power: float,
        load_power: float,
        battery_level: float
    ):

        return self.agent.analyze(
            solar_power=solar_power,
            load_power=load_power,
            battery_level=battery_level
        )

    # =====================================================
    # Marketplace Statistics
    # =====================================================

    def statistics(
        self,
        db: Session
    ):

        total = db.query(Trading).count()

        available = (
            db.query(Trading)
            .filter(Trading.status == "AVAILABLE")
            .count()
        )

        completed = (
            db.query(Trading)
            .filter(Trading.status == "COMPLETED")
            .count()
        )

        cancelled = (
            db.query(Trading)
            .filter(Trading.status == "CANCELLED")
            .count()
        )

        total_energy = (
            db.query(func.sum(Trading.energy))
            .scalar()
        ) or 0

        total_value = (
            db.query(func.sum(Trading.price))
            .scalar()
        ) or 0

        return {

            "total_trades": total,

            "available": available,

            "completed": completed,

            "cancelled": cancelled,

            "total_energy_traded": round(total_energy, 2),

            "total_trade_value": round(total_value, 2)

        }

    # =====================================================
    # Delete Trade
    # =====================================================

    def delete_trade(
        self,
        db: Session,
        trade_id: int
    ):

        trade = self.get_trade(db, trade_id)

        if trade is None:
            return False

        db.delete(trade)

        db.commit()

        return True