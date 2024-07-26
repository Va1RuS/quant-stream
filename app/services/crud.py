from sqlalchemy import func
import pandas as pd
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import Session

from app.models.kline import KLine


def get_klines(db: Session, symbol: str, interval: str):
    return db.query(KLine).filter(
        symbol == KLine.symbol, interval == KLine.interval
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


def get_symbol_interval_last_timestamp(db: Session):
    result = db.query(
        KLine.symbol,
        KLine.interval,
        func.max(KLine.timestamp).label("last_timestamp")
    ).group_by(KLine.symbol, KLine.interval).all()

    return [(row.symbol, row.interval, row.last_timestamp if row.last_timestamp else None) for row in result]


def construct_on_conflict_set(model):
    return {col.name: getattr(insert(model).excluded, col.name)
            for col in model.__table__.columns if col.name not in ['timestamp', 'symbol', 'interval']}


def insert_kline_data(db: Session, data, symbol, interval):
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
        set_=construct_on_conflict_set(KLine)
    )
    db.execute(on_conflict_stmt)
    db.commit()

