import asyncio
import logging
from datetime import datetime, timedelta

from app.database import SessionLocal
from app.services.binance_client import fetch_historic_kline_data
from app.services.crud import insert_kline_data, get_symbol_interval_last_timestamp
from app.config import config


async def backfill_symbol_interval(db, symbol, interval, last_timestamp):
    logging.info(f"Backfilling {symbol} {interval} from {last_timestamp}")
    current_time = datetime.utcnow()
    start_time = last_timestamp

    end_time = current_time
    data = await fetch_historic_kline_data(symbol, interval, start_time, end_time)
    if data:
        logging.info(f"Inserting {len(data)} rows into the database for {symbol} {interval}")
        insert_kline_data(db, data, symbol, interval)


async def backfill():
    logging.info("Starting backfill")
    db = SessionLocal()
    symbol_interval_timestamp = get_symbol_interval_last_timestamp(db)
    tasks = [backfill_symbol_interval(db, symbol, interval, last_timestamp)
             for symbol, interval, last_timestamp in symbol_interval_timestamp]

    if not tasks:  # If there is no data in the database, backfill the last day. First time running the app
        start_time = datetime.utcnow() - timedelta(days=1)
        for symbol in config.SYMBOLS:
            for interval in config.INTERVALS:
                tasks.append(backfill_symbol_interval(db, symbol, interval, start_time))

    await asyncio.gather(*tasks)
    logging.info("Backfill complete")
    db.close()
