import asyncio

from .services.backfill import backfill
from .services.kline_stream import binance_websocket


async def on_startup():
    print("Running startup tasks...")
    await backfill()
    await asyncio.create_task((binance_websocket()))


async def on_shutdown():
    print("Running shutdown tasks...")
