from mansour_strategy_evaluation_service.model.one_minute_candle import OneMinuteCandle
from mansour_strategy_evaluation_service.repository.watchlist_repository import WatchlistRepository, watchlist_repository
from mansour_strategy_evaluation_service.strategy.base_strategy import Signal
from mansour_strategy_evaluation_service.strategy.strategy_engine import strategy_engine

class EvaluationCoordinator:
    def __init__(self, repository: WatchlistRepository):
        self.repo = repository

    async def process_candle(self, candle: OneMinuteCandle):
        """새로운 캔들을 받아, 평가가 필요한 모든 전략을 실행시킵니다."""
        symbol = candle.symbol

        # 이 캔들의 종목이 활성 감시 목록에 있는지 확인합니다.
        if not self.repo.is_symbol_in_active_watchlist(symbol):
            return # 감시 대상이 아니면 아무것도 하지 않음

        # 이 종목을 감시하고 있는 모든 '사용자 전략 ID' 목록을 가져옵니다.
        user_strategy_ids = self.repo.get_evaluators_for_symbol(symbol)
        
        print(f"🕯️ Found {len(user_strategy_ids)} active strategies for {symbol}. Evaluating...")

        # 각 사용자 전략에 대해 평가를 진행합니다.
        for user_strategy_id in user_strategy_ids:
            # Redis에서 해당 전략의 상세 설정(파라미터 등)을 가져옵니다.
            strategy_details = self.repo.get_strategy_details(int(user_strategy_id))
            
            if not strategy_details:
                print(f"⚠️ Strategy details not found for id: {user_strategy_id}. Skipping.")
                continue

            print(f"   -> Evaluating strategy: {strategy_details}")

            # 전략 평가
            signal = await strategy_engine.evaluate(strategy_details, candle)
            
            print(f"signal: {signal.value}")

            if signal in [Signal.BUY, Signal.SELL]:
                print(f"🚀 {signal.value} signal generated for {candle.symbol}!")
                # TODO: 신호 발행 로직


# 다른 곳에서 사용할 수 있도록 인스턴스 생성
evaluation_coordinator = EvaluationCoordinator(repository=watchlist_repository)
