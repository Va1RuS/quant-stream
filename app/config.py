import os


class Settings:
    PROJECT_NAME: str = "Quant-Stream"
    PROJECT_VERSION: str = "1.0"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "quantstream")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "quantstream")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")  # default postgres port
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "quantstream")
    DATABASE_URL: str = (f"postgresql://"
                         f"{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DB}")

    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"


settings = Settings()
