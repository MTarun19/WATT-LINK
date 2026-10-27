"""
marketplace_router.py
-----------------------------------
WATT LINK Marketplace Router
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import get_db
from models import Trading, User
from schemas import TradingCreate, TradingResponse
from auth import get_current_user

router = APIRouter(
    prefix="/marketplace",
    tags=["Marketplace"]
)


# ==========================================================
# Create Energy Trade
# ==========================================================

@router.post("/sell", response_model=TradingResponse)
def create_trade(
    trade: TradingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_trade = Trading(

        seller=current_user.full_name,

        buyer=trade.buyer,

        energy=trade.energy,

        price=trade.price,

        status="AVAILABLE"

    )

    db.add(new_trade)
    db.commit()
    db.refresh(new_trade)

    return new_trade


# ==========================================================
# View Marketplace
# ==========================================================

@router.get("/", response_model=list[TradingResponse])
def view_marketplace(
    db: Session = Depends(get_db)
):

    return db.query(Trading).all()


# ==========================================================
# Buy Energy
# ==========================================================

@router.put("/buy/{trade_id}")
def buy_energy(
    trade_id: int,
    buyer_name: str,
    db: Session = Depends(get_db)
):

    trade = db.query(Trading).filter(
        Trading.id == trade_id
    ).first()

    if trade is None:
        raise HTTPException(
            status_code=404,
            detail="Trade not found"
        )

    trade.buyer = buyer_name
    trade.status = "SOLD"

    db.commit()

    return {
        "message": "Energy purchased successfully"
    }


# ==========================================================
# My Trades
# ==========================================================

@router.get("/my-trades", response_model=list[TradingResponse])
def my_trades(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    return db.query(Trading).filter(
        Trading.seller == current_user.full_name
    ).all()


# ==========================================================
# Delete Trade
# ==========================================================

@router.delete("/{trade_id}")
def delete_trade(
    trade_id: int,
    db: Session = Depends(get_db)
):

    trade = db.query(Trading).filter(
        Trading.id == trade_id
    ).first()

    if trade is None:
        raise HTTPException(
            status_code=404,
            detail="Trade not found"
        )

    db.delete(trade)
    db.commit()

    return {
        "message": "Trade deleted successfully"
    }


# ==========================================================
# Marketplace Statistics
# ==========================================================

@router.get("/statistics")
def statistics(
    db: Session = Depends(get_db)
):

    total = db.query(Trading).count()

    available = db.query(Trading).filter(
        Trading.status == "AVAILABLE"
    ).count()

    sold = db.query(Trading).filter(
        Trading.status == "SOLD"
    ).count()

    return {
        "total_trades": total,
        "available": available,
        "sold": sold
    }