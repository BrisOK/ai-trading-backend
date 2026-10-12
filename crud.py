from sqlalchemy.orm import Session
from models import Trade, StrategySignal
from schemas import TradeCreate
from typing import List


def create_trade(db: Session, trade: TradeCreate) -> Trade:
        db_trade = Trade(**trade.dict())
        db.add(db_trade)
        db.commit()
        db.refresh(db_trade)
        return db_trade


def get_trades(db: Session, skip: int = 0, limit: int = 100) -> List[Trade]:
        return db.query(Trade).offset(skip).limit(limit).all()


def create_signal(db: Session, symbol: str, prediction: float, recommendation: str) -> StrategySignal:
        db_signal = StrategySignal(
                symbol=symbol,
                prediction=prediction,
                recommendation=recommendation,
        )
        db.add(db_signal)
        db.commit()
        db.refresh(db_signal)
        return db_signal


def get_signals(db: Session, symbol: str | None = None, limit: int = 50):
        query = db.query(StrategySignal).order_by(StrategySignal.created_at.desc())
        if symbol:
                query = query.filter(StrategySignal.symbol == symbol)
        return query.limit(limit).all()