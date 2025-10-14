from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

from mansour_strategy_evaluation_service.model.api_response import ApiResponse, Content

class Candle(BaseModel):
    time: datetime
    symbol: str
    open: Decimal
    high: Decimal
    low: Decimal
    close: Decimal
    volume: int


ContentCandleResponse = ApiResponse[Content[Candle]]