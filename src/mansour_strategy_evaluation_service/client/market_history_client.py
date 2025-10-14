import httpx
from typing import List

from mansour_strategy_evaluation_service.client.base_client import BaseApiClient
from mansour_strategy_evaluation_service.model.candle import Candle, ContentCandleResponse

class MarketHistoryClient(BaseApiClient):
    """
    market-history-service와 통신하는 클라이언트
    """
    
    def __init__(self):
        super().__init__(service_name="market-history-service")
        self.http_client = httpx.AsyncClient()

    async def get_recent_candles(self, symbol: str, limit: int) -> List[Candle]:
        try:
            base_url = await self._get_base_url()
            url = f"{base_url}/stock/recent/{symbol}"
            params = {"limit": limit}

            response = await self.http_client.get(url, params=params)
            response.raise_for_status()

            api_response = ContentCandleResponse(**response.json())

            return api_response.data.content

        except httpx.HTTPError as e:
            # 3. 부모의 공통 예외 처리 로직을 호출합니다.
            self._handle_request_exception(e)
            return []

# 다른 곳에서 사용할 수 있도록 인스턴스 생성
market_history_client = MarketHistoryClient()