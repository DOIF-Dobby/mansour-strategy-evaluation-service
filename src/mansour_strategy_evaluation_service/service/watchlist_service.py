import logging
from mansour_strategy_evaluation_service.model.user_strategy_payload import UserStrategyActivatedEventPayload
from mansour_strategy_evaluation_service.repository.watchlist_repository import WatchlistRepository, watchlist_repository

logger = logging.getLogger(__name__)

class WatchlistService:
    def __init__(self, repository: WatchlistRepository):
        self.repo = repository

    def activate_strategy_for_symbol(self, payload: UserStrategyActivatedEventPayload):
        """새로운 사용자 전략을 활성화하고, 필요시 감시 목록에 추가합니다."""
        
        symbol = payload.symbol
        user_strategy_id = payload.userStrategyId

        # 평가자 Set에 사용자 전략 ID 추가
        is_new_evaluator = self.repo.add_evaluator(symbol, user_strategy_id) == 1
        
        # 전략 상세 정보를 Hash에 저장
        self.repo.save_strategy_details(payload)

        # 새로운 평가자인 경우에만 로직 실행
        if is_new_evaluator:
            # 현재 평가자 수를 확인
            evaluator_count = self.repo.get_evaluator_count(symbol)
            
            # 이 전략이 이 종목의 첫 번째 평가자라면, 활성 감시 목록에 추가
            if evaluator_count == 1:
                logger.info(f"🌟 First evaluator for {symbol}. Adding to active watchlist.")
                self.repo.add_to_active_watchlist(symbol)

    def deactivate_strategy_for_symbol(self, symbol: str, user_strategy_id: int):
        """사용자 전략을 비활성화하고, 필요시 감시 목록에서 제거합니다."""
        
        # 평가자 Set에서 사용자 전략 ID 제거
        was_evaluator = self.repo.remove_evaluator(symbol, user_strategy_id) == 1

        # 전략 상세 정보 삭제
        self.repo.remove_strategy_details(user_strategy_id)
        
        # 실제로 평가자 목록에 있었던 경우에만 로직 실행
        if was_evaluator:
            # 현재 남은 평가자 수를 확인
            evaluator_count = self.repo.get_evaluator_count(symbol)
            
            # 이 전략이 이 종목의 마지막 평가자였다면, 활성 감시 목록에서 제거
            if evaluator_count == 0:
                logger.info(f"👋 Last evaluator for {symbol}. Removing from active watchlist.")
                self.repo.remove_from_active_watchlist(symbol)

# Service 인스턴스를 미리 생성
watchlist_service = WatchlistService(repository=watchlist_repository)