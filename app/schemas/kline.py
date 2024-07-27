from pydantic import BaseModel
from datetime import datetime


class KLineBase(BaseModel):
    timestamp: datetime
    symbol: str
    interval: str
    open: float
    high: float
    low: float
    close: float
    volume: float

    class Config:
        orm_mode: True


class KLineCreate(KLineBase):
    pass


class KLine(KLineBase):
    id: int

    class Config:
        from_attributes = True
