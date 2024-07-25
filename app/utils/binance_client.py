import aiohttp
import asyncio
import websockets
import json


async def fetch_top_symbols():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                sorted_data = sorted(data, key=lambda x: float(x['quoteVolume']), reverse=True)
                top_symbols = [item['symbol'] for item in sorted_data[:20]]
                return top_symbols
            else:
                raise Exception(f"Failed to fetch data from Binance API: {response.status}")


async def kline_stream(symbol, intervals):
    socket_base = 'wss://stream.binance.com:9443/ws'
    sockets = [f"{socket_base}/{symbol}@kline_{interval}" for interval in intervals]

    async def handle_socket(url):
        async with websockets.connect(url) as ws:
            while True:
                data = await ws.recv()
                data = json.loads(data)
                print(f"Received {data['k']['i']} data for {data['k']['s']}: {data}")
                # Here you would normally process and store the data

    await asyncio.gather(*(handle_socket(socket) for socket in sockets))


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
                data = await response.json()
                return data
            else:
                raise Exception(f"Failed to fetch data from Binance API: {response.status}")


async def main():
    top_symbols = await fetch_top_symbols()
    print("Top 20 symbols by trading volume:", top_symbols)
    await kline_stream("btcusdt", ["1m", "5m", "1h"])


if __name__ == "__main__":
    asyncio.run(main())
