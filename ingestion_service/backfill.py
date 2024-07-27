import logging
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.models.kline import SessionLocal
from shared.config import settings

from shared.binance import fetch_historic_kline_data
from shared.crud import insert_kline_data, get_symbol_interval_last_timestamp

logging.basicConfig(level=logging.INFO)


async def backfill_symbol_interval(db: Session, symbol: str, interval: str, last_timestamp):
    logging.info(f"Backfilling {symbol} {interval} from {last_timestamp}")
    current_time = datetime.utcnow()
    start_time = last_timestamp if last_timestamp else current_time - timedelta(days=1)
    end_time = current_time
    data = await fetch_historic_kline_data(symbol, interval, start_time, end_time)
    if data:
        logging.info(f"Inserting {len(data)} rows into the database for {symbol} {interval}")
        await insert_kline_data(db, data, symbol, interval)


async def backfill():
    logging.info("Starting backfill")
    db = SessionLocal()
    try:
        for symbol in settings.SYMBOLS:
            for interval in settings.INTERVALS:
                last_timestamp = get_symbol_interval_last_timestamp(db, symbol, interval)
                await backfill_symbol_interval(db, symbol, interval, last_timestamp)
    finally:
        db.close()
    logging.info("Backfill complete")
