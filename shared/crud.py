import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.kline import KLine

from shared.config import settings


def get_klines(db: Session, symbol: str, interval: str):
    return db.query(KLine).filter(
        symbol == KLine.symbol, interval == KLine.interval
    ).limit(settings.LAST_N_CANDLES).all()


def calculate_macd(db: Session, symbol: str, interval: str):
    klines = get_klines(db, symbol, interval)
    if not klines:
        return []

    df = pd.DataFrame([k.__dict__ for k in klines])

    exp1 = df['close'].ewm(span=12, adjust=False).mean()
    exp2 = df['close'].ewm(span=26, adjust=False).mean()
    macd = exp1 - exp2
    signal = macd.ewm(span=9, adjust=False).mean()

    return macd.tolist(), signal.tolist()


def calculate_rsi(db: Session, symbol: str, interval: str):
    klines = get_klines(db, symbol, interval)
    if not klines:
        return []

    df = pd.DataFrame([k.__dict__ for k in klines])

    delta = df['close'].diff()
    gain = (delta.where(delta > 0, 0)).fillna(0)
    loss = (-delta.where(delta < 0, 0)).fillna(0)
    avg_gain = gain.rolling(window=14).mean()
    avg_loss = loss.rolling(window=14).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


def get_symbol_interval_last_timestamp(db: Session, symbol, interval):
    last_timestamp = db.query(KLine).filter(
        KLine.symbol == symbol, KLine.interval == interval
    ).order_by(KLine.timestamp.desc()).first()
    last_timestamp = last_timestamp.timestamp if last_timestamp else None
    return last_timestamp


async def insert_kline_data(db: Session, data, symbol, interval):
    data_list = [
        {
            'timestamp': item['timestamp'],
            'symbol': symbol,
            'interval': interval,
            'open': item['open'],
            'high': item['high'],
            'low': item['low'],
            'close': item['close'],
            'volume': item['volume']
        }
        for item in data
    ]
    stmt = insert(KLine).values(data_list)
    on_conflict_stmt = stmt.on_conflict_do_update(
        index_elements=['timestamp', 'symbol', 'interval'],
        set_={
            'open': stmt.excluded.open,
            'high': stmt.excluded.high,
            'low': stmt.excluded.low,
            'close': stmt.excluded.close,
            'volume': stmt.excluded.volume
        }
    )
    db.execute(on_conflict_stmt)
    db.commit()

