from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas
from .dependencies import get_db

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/klines/{symbol}/{interval}", response_model=list[schemas.KLine])
async def read_klines(symbol: str, interval: str, db: Session = Depends(get_db)):
    klines = crud.get_klines(db, symbol=symbol, interval=interval)
    return klines


@router.get("/indicators/macd/{symbol}/{interval}")
async def read_macd(symbol: str, interval: str, db: Session = Depends(get_db)):
    macd_values = crud.calculate_macd(db, symbol=symbol, interval=interval)
    return {"symbol": symbol, "interval": interval, "MACD": macd_values}


@router.get("/indicators/rsi/{symbol}/{interval}")
async def read_rsi(symbol: str, interval: str, db: Session = Depends(get_db)):
    rsi_values = crud.calculate_rsi(db, symbol=symbol, interval=interval)
    return {"symbol": symbol, "interval": interval, "RSI": rsi_values}
