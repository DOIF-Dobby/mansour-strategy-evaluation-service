from dataclasses import dataclass
import json
from typing import Dict
from mansour_strategy_evaluation_service.core.kafka.base_consumer import BaseConsumer
from mansour_strategy_evaluation_service.model.user_strategy_payload import UserStrategyActivatedEventPayload, UserStrategyDeactivatedEventPayload
from mansour_strategy_evaluation_service.service.watchlist_service import watchlist_service

class UserStrategyActivatedEventConsumer(BaseConsumer):
    TOPIC = "outbox.event.UserStrategy.UserStrategyActivatedEvent"

    def __init__(self):
        super().__init__()
        print("UserStrategyEventConsumer initialized.")

    async def handle(self, message):
        try:
            data_dict = json.loads(message.value)
            payload = UserStrategyActivatedEventPayload(**data_dict)
            
            watchlist_service.activate_strategy_for_symbol(
                payload=payload
            )

        except Exception as e:
            print(f"🔥 Error processing message in UserStrategyEventConsumer: {e}")


class UserStrategyDeactivatedEventConsumer(BaseConsumer):
    TOPIC = "outbox.event.UserStrategy.UserStrategyDeactivatedEvent"

    def __init__(self):
        super().__init__()
        print("UserStrategyDeactivatedEventConsumer initialized.")

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
            print(f"🔥 Error processing deactivation message: {e}")