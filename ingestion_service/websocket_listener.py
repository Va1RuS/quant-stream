import asyncio
import logging
from datetime import datetime

import aiohttp
import websockets
import json
from sqlalchemy.orm import Session
from app.models.kline import SessionLocal
from shared.config import settings
from shared.crud import insert_kline_data

logging.basicConfig(level=logging.INFO)


async def fetch_historic_kline_data(symbol, interval, start_time, end_time):
    url = settings.KLINES_URL
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': int(start_time.timestamp() * 1000),
        'endTime': int(end_time.timestamp() * 1000)
    }
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                raw_data = await response.json()
                data = [
                    {
                        'timestamp': datetime.fromtimestamp(item[0] / 1000),
                        'open': float(item[1]),
                        'high': float(item[2]),
                        'low': float(item[3]),
                        'close': float(item[4]),
                        'volume': float(item[5])
                    }
                    for item in raw_data
                ]
                return data
            else:
                raise Exception(f"Failed to fetch data from Binance API: {response.status}")


async def handle_socket(symbol, interval):
    url = f"{settings.WEBSOCKET_URL}/{symbol.lower()}@kline_{interval}"
    db = SessionLocal()
    while True:
        try:
            async with websockets.connect(url) as ws:
                logging.info(f"Connected to WebSocket for {symbol} {interval}")
                while True:
                    data = await ws.recv()
                    data = json.loads(data)
                    # logging.info(f"Received data from WebSocket: {data}")
                    await process_and_store_data(db, data, symbol, interval)
        except websockets.exceptions.ConnectionClosed:
            logging.error(f"Connection closed, reconnecting in 5 seconds: {url}")
            await asyncio.sleep(5)
        except Exception as e:
            logging.error(f"Error handling data from {url}: {e}")
            await asyncio.sleep(5)


async def process_and_store_data(db: Session, data, symbol, interval):
    try:
        candle = data.get('k')
        if not candle:
            logging.error(f"Received data does not contain 'k': {data}")
            return
        kline_data = {
            'timestamp': datetime.fromtimestamp(candle['t'] / 1000),
            'symbol': symbol,
            'interval': interval,
            'open': float(candle['o']),
            'high': float(candle['h']),
            'low': float(candle['l']),
            'close': float(candle['c']),
            'volume': float(candle['v'])
        }
        # logging.info(f"Storing data to database: {kline_data}")
        await insert_kline_data(db, [kline_data], symbol, interval)
    except KeyError as e:
        logging.error(f"Key error: {e} in data: {data}")
    except TypeError as e:
        logging.error(f"Type error: {e} in data: {data}")
    except Exception as e:
        logging.error(f"Unexpected error: {e} in data: {data}")


async def binance_websocket():
    tasks = [handle_socket(symbol, interval) for symbol in settings.SYMBOLS for interval in
             settings.INTERVALS]
    await asyncio.gather(*tasks)
