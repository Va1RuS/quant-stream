from pydantic import BaseModel
from datetime import datetime


class KLineBase(BaseModel):
    symbol: str
    interval: str
    time: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


class KLineCreate(KLineBase):
    pass


class KLine(KLineBase):
    id: int

    class Config:
        from_attributes = True
