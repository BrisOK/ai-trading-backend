from pydantic import BaseModel
from datetime import datetime


class TradeBase(BaseModel):
        symbol: str
        side: str
        quantity: float
        price: float


class TradeCreate(TradeBase):
        pass


class Trade(TradeBase):
        id: int
        created_at: datetime

        class Config:
                orm_mode = True


class SignalBase(BaseModel):
        symbol: str


class Signal(SignalBase):
        id: int
        prediction: float
        recommendation: str
        created_at: datetime

        class Config:
                orm_mode = True