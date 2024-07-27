import os

from shared.binance import fetch_top_symbols


class Settings:
    PROJECT_NAME: str = "Quant-Stream"
    PROJECT_VERSION: str = "1.0"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://quantstream:quantstream@localhost:5432/quantstream")

    WEBSOCKET_URL: str = "wss://stream.binance.com:9443/ws"
    KLINES_URL: str = "https://api.binance.com/api/v3/klines"

    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

    INTERVALS = ['1m', '15m', '1h']
    SYMBOLS = fetch_top_symbols()

    LAST_N_CANDLES = 100


settings = Settings()
