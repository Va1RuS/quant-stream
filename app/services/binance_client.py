from datetime import datetime

import aiohttp
import asyncio
import websockets
import json
import requests


def fetch_top_symbols():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        sorted_data = sorted(data, key=lambda x: float(x['quoteVolume']), reverse=True)
        top_symbols = [item['symbol'] for item in sorted_data[:5]]
        return top_symbols
    else:
        raise Exception(f"Failed to fetch data from Binance API: {response.status_code}")


async def fetch_historic_kline_data(symbol, interval, start_time, end_time):
    url = "https://api.binance.com/api/v3/klines"
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': int(start_time.timestamp() * 1000),  # converting to milliseconds
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


async def main():
    print("Top 20 symbols by trading volume:", fetch_top_symbols)

if __name__ == "__main__":
    asyncio.run(main())
