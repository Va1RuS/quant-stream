from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.kline import KLineBase
from shared.database import get_db
from shared.crud import get_klines, calculate_macd, calculate_rsi
from utils.utils import uppercase

router = APIRouter()


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/klines/{symbol}/{interval}", response_model=list[KLineBase])
async def read_klines(symbol: str, interval: str,  db: Session = Depends(get_db)):
    klines = get_klines(db, symbol.upper(), interval=interval)
    return klines


@router.get("/indicators/macd/{symbol}/{interval}")
async def read_macd(symbol: str, interval: str, db: Session = Depends(get_db)):
    macd_values = calculate_macd(db, symbol=symbol.upper(), interval=interval)
    return {"symbol": symbol, "interval": interval, "MACD": macd_values}


@router.get("/indicators/rsi/{symbol}/{interval}")
async def read_rsi(symbol: str, interval: str,  db: Session = Depends(get_db)):
    rsi_values = calculate_rsi(db, symbol=symbol.upper(), interval=interval)
    return {"symbol": symbol, "interval": interval, "RSI": rsi_values}
