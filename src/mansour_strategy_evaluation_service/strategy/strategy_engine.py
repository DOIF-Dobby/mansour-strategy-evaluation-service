import logging
from mansour_strategy_evaluation_service.client.market_history_client import MarketHistoryClient, market_history_client
from mansour_strategy_evaluation_service.model.one_minute_candle import OneMinuteCandle
from mansour_strategy_evaluation_service.strategy.base_strategy import Signal, TradingStrategy

logger = logging.getLogger(__name__)


class StrategyEngine:
    def __init__(self, history_client: MarketHistoryClient):
        self.history_client = history_client
        self.strategies = {cls().get_name(): cls() for cls in TradingStrategy.__subclasses__()}
        logger.info(f"✅ Registered strategies: {list(self.strategies.keys())}")

    async def evaluate(self, strategy_details: dict, current_candle: OneMinuteCandle) -> Signal:
        """
        주어진 전략 정보와 현재 캔들을 바탕으로,
        필요한 모든 작업을 스스로 수행하여 최종 신호를 반환합니다.
        """
        strategy_name = strategy_details.get("strategyId")
        params = strategy_details.get("parameters", {})
        
        strategy = self.strategies.get(strategy_name)

        if not strategy:
            return Signal.HOLD
        
        # 필요한 데이터 개수를 파악합니다.
        required_count = strategy.get_required_candle_count(params)
        
        # 필요한 데이터 조회
        candles_raw = await self.history_client.get_recent_candles(current_candle.symbol, required_count)
        
        if len(candles_raw) < required_count:
            return Signal.HOLD

        # 3. 전문가(Engine)가 최종 분석을 수행하고 결과를 반환합니다.
        return strategy.evaluate(candles_raw, params)

strategy_engine = StrategyEngine(history_client=market_history_client)