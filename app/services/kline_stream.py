import asyncio
import logging
from datetime import datetime

import websockets
import json

from app.database import SessionLocal
from app.services.crud import insert_kline_data
from app.config import config


async def binance_websocket():
    socket_base = 'wss://stream.binance.com:9443/ws'

    async def handle_socket(symbol, interval):
        url = f"{socket_base}/{symbol.lower()}@kline_{interval}"
        db = SessionLocal()
        while True:
            try:
                async with websockets.connect(url) as ws:
                    while True:
                        data = await ws.recv()
                        data = json.loads(data)
                        await process_and_store_data(db, data, symbol, interval)
            except websockets.exceptions.ConnectionClosed:
                print(f"Connection closed, reconnecting in 5 seconds: {url}")
                await asyncio.sleep(5)
            except Exception as e:
                print(f"Error handling data from {url}: {e}")
                await asyncio.sleep(5)

    tasks = [handle_socket(symbol, interval) for symbol in config.SYMBOLS for interval in config.INTERVALS]
    await asyncio.gather(*tasks)


async def process_and_store_data(db: SessionLocal, data, symbol, interval):
    try:
        candle = data['k']  # Ensure 'k' is a key in the dictionary
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
        insert_kline_data(db, [kline_data], symbol, interval)
    except KeyError as e:
        logging.error(f"Key error: {e} in data: {data}")
    except TypeError as e:
        logging.error(f"Type error: {e} in data: {data}")
    except Exception as e:
        logging.error(f"Unexpected error: {e} in data: {data}")
