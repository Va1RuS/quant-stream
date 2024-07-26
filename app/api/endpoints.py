from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.kline import KLine
from app.database import get_db
from app.services.crud import get_klines, calculate_macd, calculate_rsi
from app.lifespan import on_startup, on_shutdown

router = APIRouter()

router.add_event_handler("startup", on_startup)
router.add_event_handler("shutdown", on_shutdown)


@router.get("/")
def read_root():
    return {"Hello": "World"}


@router.get("/klines/{symbol}/{interval}", response_model=list[KLine])
async def read_klines(symbol: str, interval: str, db: Session = Depends(get_db)):
    klines = get_klines(db, symbol=symbol, interval=interval)
    return klines


@router.get("/indicators/macd/{symbol}/{interval}")
async def read_macd(symbol: str, interval: str, db: Session = Depends(get_db)):
    macd_values = calculate_macd(db, symbol=symbol, interval=interval)
    return {"symbol": symbol, "interval": interval, "MACD": macd_values}


@router.get("/indicators/rsi/{symbol}/{interval}")
async def read_rsi(symbol: str, interval: str, db: Session = Depends(get_db)):
    rsi_values = calculate_rsi(db, symbol=symbol, interval=interval)
    return {"symbol": symbol, "interval": interval, "RSI": rsi_values}
