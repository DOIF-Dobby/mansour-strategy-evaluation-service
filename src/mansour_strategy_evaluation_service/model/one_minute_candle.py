from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class OneMinuteCandle:
    """1분 단위로 집계된 OHLCV 캔들 데이터 모델"""
    symbol: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int
    windowStartTime: datetime
    windowEndTime: datetime