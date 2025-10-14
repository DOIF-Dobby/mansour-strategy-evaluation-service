import abc
from enum import Enum
from typing import List

from mansour_strategy_evaluation_service.model.candle import Candle

# 모든 전략이 반환할 매매 신호
class Signal(Enum):
    BUY = "BUY"
    SELL = "SELL"
    HOLD = "HOLD"

class TradingStrategy(abc.ABC):
    """모든 트레이딩 전략이 구현해야 하는 추상 베이스 클래스 (인터페이스 역할)"""

    @abc.abstractmethod
    def get_name(self) -> str:
        """이 전략을 식별하는 고유한 이름 (e.g., "MA_CROSSOVER")"""
        raise NotImplementedError

    @abc.abstractmethod
    def evaluate(self, candles: List[Candle], params: dict) -> Signal:
        """주어진 데이터를 바탕으로 매매 신호를 결정합니다."""
        raise NotImplementedError

    @abc.abstractmethod
    def get_required_candle_count(self, params: dict) -> int:
        """
        이 전략을 평가하는 데 필요한 최소 캔들 데이터 개수를 반환합니다.
        """
        raise NotImplementedError