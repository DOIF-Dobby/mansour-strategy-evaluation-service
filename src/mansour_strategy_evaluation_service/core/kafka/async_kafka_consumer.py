import logging
from aiokafka import AIOKafkaConsumer
from typing import Callable
import json

from mansour_strategy_evaluation_service.config.env_settings import env

logger = logging.getLogger(__name__)

class AsyncKafkaConsumer:
    def __init__(self, topics: list[str]):
        self.topics = topics
        self.bootstrap_servers = env.KAFKA_SERVER_HOST
        self.consumer = None
    
    async def start(self, message_handler: Callable):
        self.consumer = AIOKafkaConsumer(
            *self.topics,
            bootstrap_servers=self.bootstrap_servers,
            group_id='strategy-evaluation-service',
            auto_offset_reset='latest',
            value_deserializer=lambda x: json.loads(x.decode('utf-8'))
        )
        
        await self.consumer.start()
        logger.info(f"🎧 Started consuming from {self.topics}")
        
        try:
            async for message in self.consumer:
                await message_handler(message)
        finally:
            await self.stop()
    
    async def stop(self):
        if self.consumer:
            await self.consumer.stop()
            logger.info(f"✅ Consumer '{self.topics}' stopped")