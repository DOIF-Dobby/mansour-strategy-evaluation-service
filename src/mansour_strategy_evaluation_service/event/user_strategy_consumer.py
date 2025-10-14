from dataclasses import dataclass
import json
import logging
from typing import Dict
from mansour_strategy_evaluation_service.core.kafka.base_consumer import BaseConsumer
from mansour_strategy_evaluation_service.model.user_strategy_payload import UserStrategyActivatedEventPayload, UserStrategyDeactivatedEventPayload
from mansour_strategy_evaluation_service.service.watchlist_service import watchlist_service

logger = logging.getLogger(__name__)

class UserStrategyActivatedEventConsumer(BaseConsumer):
    TOPIC = "outbox.event.UserStrategy.UserStrategyActivatedEvent"

    def __init__(self):
        super().__init__()
        logger.info("UserStrategyActivatedEventConsumer initialized.")

    async def handle(self, message):
        try:
            data_dict = json.loads(message.value)
            payload = UserStrategyActivatedEventPayload(**data_dict)
            
            watchlist_service.activate_strategy_for_symbol(
                payload=payload
            )

        except Exception as e:
            logger.error(f"🔥 Error processing message in UserStrategyActivatedEventConsumer: {e}")


class UserStrategyDeactivatedEventConsumer(BaseConsumer):
    TOPIC = "outbox.event.UserStrategy.UserStrategyDeactivatedEvent"

    def __init__(self):
        super().__init__()
        logger.info("UserStrategyDeactivatedEventConsumer initialized.")

    async def handle(self, message):
        try:
            data_dict = json.loads(message.value)
            payload = UserStrategyDeactivatedEventPayload(**data_dict)
            
            # WatchlistService의 deactivate 메서드를 호출
            watchlist_service.deactivate_strategy_for_symbol(
                symbol=payload.symbol,
                user_strategy_id=payload.userStrategyId
            )

        except Exception as e:
            logger.error(f"🔥 Error processing deactivation message: {e}")