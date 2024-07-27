import asyncio
import logging
from ingestion_service.backfill import backfill
from ingestion_service.websocket_listener import binance_websocket

logging.basicConfig(level=logging.INFO)


async def main():
    await backfill()
    websocket_task = asyncio.create_task(binance_websocket())
    await websocket_task

if __name__ == "__main__":
    asyncio.run(main())
