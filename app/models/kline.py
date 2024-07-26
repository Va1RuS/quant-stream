from sqlalchemy import Column, Float, String, DateTime, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings


Base = declarative_base()


class KLine(Base):
    __tablename__ = 'klines'
    timestamp = Column(DateTime, primary_key=True)
    symbol = Column(String, primary_key=True)
    interval = Column(String, primary_key=True)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(Float)


engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    Base.metadata.create_all(bind=engine)


def create_hypertable():
    from sqlalchemy import text
    with engine.connect() as conn:
        conn.execute(text("SELECT create_hypertable('kline_data', 'time');"))


if __name__ == "__main__":
    create_tables()
    create_hypertable()
