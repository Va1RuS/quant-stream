from sqlalchemy.orm import Session
from . import models
import pandas as pd


def get_klines(db: Session, symbol: str, interval: str):
    return db.query(models.KLine).filter(
        symbol == models.KLine.symbol, interval == models.KLine.interval
    ).all()


def calculate_macd(db: Session, symbol: str, interval: str):
    klines = get_klines(db, symbol, interval)
    df = pd.DataFrame(klines)
    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()
    return macd - signal


def calculate_rsi(db: Session, symbol: str, interval: str):
    klines = get_klines(db, symbol, interval)
    df = pd.DataFrame(klines)
    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi
