from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base


class Trade(Base):
        __tablename__ = "trades"

        id = Column(Integer, primary_key=True, index=True)
        symbol = Column(String, index=True)
        side = Column(String)    # "buy" or "sell"
        quantity = Column(Float)
        price = Column(Float)
        created_at = Column(DateTime(timezone=True), server_default=func.now())


class StrategySignal(Base):
        __tablename__ = "strategy_signals"

        id = Column(Integer, primary_key=True, index=True)
        symbol = Column(String, index=True)
        prediction = Column(Float)    # e.g., expected return
        recommendation = Column(String)    # "buy", "sell", "hold"
        created_at = Column(DateTime(timezone=True), server_default=func.now())