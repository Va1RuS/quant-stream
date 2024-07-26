import os

from app.services.binance_client import fetch_top_symbols


class Settings:
    PROJECT_NAME: str = "Quant-Stream"
    PROJECT_VERSION: str = "1.0"

    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql://quantstream:quantstream@localhost:5432/quantstream")

    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


class Config:
    INTERVALS = ['1m', '15m', '1h']
    SYMBOLS = fetch_top_symbols()


settings = Settings()
config = Config()