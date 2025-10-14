import json
from redis import Redis
from mansour_strategy_evaluation_service.config.redis_client import redis_client
from mansour_strategy_evaluation_service.model.user_strategy_payload import UserStrategyActivatedEventPayload

class RedisKeys:
    """Redis 키를 중앙에서 관리하는 클래스"""
    @staticmethod
    def active_watchlist() -> str:
        return "strategy-evaluation:watchlist:active_symbols"

    @staticmethod
    def evaluators_for_symbol(symbol: str) -> str:
        return f"strategy-evaluation:watchlist:{symbol}:evaluators"

    @staticmethod
    def strategy_details(user_strategy_id: int) -> str:
        return f"strategy-evaluation:config:{user_strategy_id}"

class WatchlistRepository:
    def __init__(self, client: Redis):
        self.redis = client

    def add_evaluator(self, symbol: str, user_strategy_id: int) -> int:
        """특정 종목의 평가자 Set에 사용자 전략 ID를 추가합니다."""
        key = RedisKeys.evaluators_for_symbol(symbol)
        # sadd는 새로 추가된 요소의 개수(0 또는 1)를 반환합니다.
        return self.redis.sadd(key, str(user_strategy_id))

    def get_evaluator_count(self, symbol: str) -> int:
        """특정 종목의 현재 평가자 수를 반환합니다."""
        key = RedisKeys.evaluators_for_symbol(symbol)
        return self.redis.scard(key)

    def add_to_active_watchlist(self, symbol: str):
        """활성 감시 목록 Set에 종목을 추가합니다."""
        key = RedisKeys.active_watchlist()
        self.redis.sadd(key, symbol)
    
    def remove_evaluator(self, symbol: str, user_strategy_id: int) -> int:
        """특정 종목의 평가자 Set에서 사용자 전략 ID를 제거합니다."""
        key = RedisKeys.evaluators_for_symbol(symbol)
        # srem은 성공적으로 제거된 요소의 개수(0 또는 1)를 반환합니다.
        return self.redis.srem(key, str(user_strategy_id))

    def remove_from_active_watchlist(self, symbol: str):
        """활성 감시 목록 Set에서 종목을 제거합니다."""
        key = RedisKeys.active_watchlist()
        self.redis.srem(key, symbol)

    def save_strategy_details(self, payload: UserStrategyActivatedEventPayload):
        """사용자 전략의 상세 정보를 Hash로 저장합니다."""
        key = RedisKeys.strategy_details(payload.userStrategyId)
        
        # 데이터클래스를 딕셔너리로 변환한 뒤, HSET으로 저장
        # parameters는 딕셔너리이므로 JSON 문자열로 변환하여 저장
        strategy_map = {
            "userStrategyId": payload.userStrategyId,
            "userId": payload.userId,
            "strategyId": payload.strategyId,
            "symbol": payload.symbol,
            "parameters": json.dumps(payload.parameters)
        }
        self.redis.hset(key, mapping=strategy_map)

    def remove_strategy_details(self, user_strategy_id: int):
        """사용자 전략 상세 정보를 삭제합니다."""
        key = RedisKeys.strategy_details(user_strategy_id)
        self.redis.delete(key)

    def is_symbol_in_active_watchlist(self, symbol: str) -> bool:
        """해당 종목이 활성 감시 목록에 있는지 확인합니다."""
        key = RedisKeys.active_watchlist()
        return self.redis.sismember(key, symbol)

    def get_evaluators_for_symbol(self, symbol: str) -> set:
        """특정 종목을 평가해야 하는 모든 사용자 전략 ID 목록을 반환합니다."""
        key = RedisKeys.evaluators_for_symbol(symbol)
        return self.redis.smembers(key)

    def get_strategy_details(self, user_strategy_id: int) -> dict:
        """사용자 전략의 상세 정보를 Hash에서 가져옵니다."""
        key = RedisKeys.strategy_details(user_strategy_id)
        details = self.redis.hgetall(key)
        # HGETALL은 parameters를 JSON 문자열로 반환하므로, 다시 딕셔너리로 파싱해줍니다.
        if 'parameters' in details:
            details['parameters'] = json.loads(details['parameters'])
        return details
    
# Repository 인스턴스를 미리 생성하여 다른 곳에서 가져다 쓸 수 있도록 함
watchlist_repository = WatchlistRepository(client=redis_client)