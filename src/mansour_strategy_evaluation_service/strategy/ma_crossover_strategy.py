import logging
from typing import List
from mansour_strategy_evaluation_service.model.candle import Candle
from mansour_strategy_evaluation_service.strategy.base_strategy import Signal, TradingStrategy
import pandas as pd
import talib

logger = logging.getLogger(__name__)


class MovingAverageCrossoverStrategy(TradingStrategy):
    """이동평균선 교차 전략 구현체"""

    def get_name(self) -> str:
        return "MA_CROSSOVER"

    def evaluate(self, candles: List[Candle], params: dict) -> Signal:
        short_period = int(params.get("short_period", 5))
        long_period = int(params.get("long_period", 20))

        if len(candles) < long_period:
            return Signal.HOLD

        # 캔들 리스트를 시간 오름차순(과거 -> 현재)으로 정렬합니다.
        sorted_candles = sorted(candles, key=lambda c: c.time)

        # 캔들 리스트를 Pandas DataFrame으로 변환합니다.
        df = pd.DataFrame([c.__dict__ for c in sorted_candles])
        
        # TA-Lib를 사용하여 이동평균선을 계산합니다.
        # 'close' 컬럼의 데이터를 사용하여 계산합니다.
        short_ma = talib.SMA(df['close'], timeperiod=short_period)
        long_ma = talib.SMA(df['close'], timeperiod=long_period)
        
        # 3. 마지막 두 지점의 이동평균 값을 가져옵니다.
        #    -2는 직전 값, -1은 현재 값입니다.
        previous_short_ma = short_ma.iloc[-2]
        current_short_ma = short_ma.iloc[-1]
        previous_long_ma = long_ma.iloc[-2]
        current_long_ma = long_ma.iloc[-1]

        logger.info(f"previous_short_ma: {previous_short_ma}")
        logger.info(f"current_short_ma: {current_short_ma}")
        logger.info(f"previous_long_ma: {previous_long_ma}")
        logger.info(f"current_long_ma: {current_long_ma}")
        
        # 4. 골든크로스 / 데드크로스를 판단합니다.
        is_golden_cross = previous_short_ma <= previous_long_ma and current_short_ma > current_long_ma
        is_dead_cross = previous_short_ma >= previous_long_ma and current_short_ma < current_long_ma

        logger.info(f"is_golden_cross: {is_golden_cross}")
        logger.info(f"is_dead_cross: {is_dead_cross}")

        if is_golden_cross:
            return Signal.BUY
        elif is_dead_cross:
            return Signal.SELL
        else:
            return Signal.HOLD
    
    def get_required_candle_count(self, params: dict) -> int:
        # 이 전략은 '장기 이동평균 기간'만큼의 데이터가 필요합니다.
        return int(params.get("long_period", 20)) + 1