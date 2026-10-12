from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from database import Base, engine, get_db
import models, schemas, crud
from ai_model import get_signal_for_symbol

Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Trading API", version="0.1.0")

# Allow frontend dev origin
origins = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
]

app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)


@app.get("/health")
def health_check():
        return {"status": "ok"}


@app.get("/trades", response_model=list[schemas.Trade])
def list_trades(db: Session = Depends(get_db)):
        return crud.get_trades(db)


@app.post("/trades", response_model=schemas.Trade)
def create_trade(trade: schemas.TradeCreate, db: Session = Depends(get_db)):
        if trade.side not in ["buy", "sell"]:
                raise HTTPException(status_code=400, detail="side must be 'buy' or 'sell'")
        return crud.create_trade(db, trade)


@app.get("/signals", response_model=list[schemas.Signal])
def list_signals(symbol: str | None = None, db: Session = Depends(get_db)):
        return crud.get_signals(db, symbol)


@app.post("/signals", response_model=schemas.Signal)
def generate_signal(symbol: str, db: Session = Depends(get_db)):
        prediction, recommendation = get_signal_for_symbol(symbol)
        signal = crud.create_signal(db, symbol, prediction, recommendation)
        return signal