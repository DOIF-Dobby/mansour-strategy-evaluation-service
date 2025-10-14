import abc
import asyncio
from mansour_strategy_evaluation_service.core.kafka.async_kafka_consumer import AsyncKafkaConsumer

class BaseConsumer(abc.ABC):
    """모든 Kafka 이벤트 컨슈머를 위한 추상 베이스 클래스"""
    
    # 각 컨슈머는 자신의 토픽과 그룹 ID를 반드시 정의해야 함
    @property
    @abc.abstractmethod
    def TOPIC(self) -> str:
        raise NotImplementedError

    def __init__(self):
        self.consumer = AsyncKafkaConsumer(
            topics=[self.TOPIC],
        )
        self.task = None

    # 각 컨슈머는 메시지를 처리하는 handle 메서드를 반드시 구현해야 함
    @abc.abstractmethod
    async def handle(self, message):
        raise NotImplementedError

    def start(self):
        """컨슈머를 백그라운드 태스크로 시작합니다."""
        loop = asyncio.get_event_loop()
        self.task = loop.create_task(self.consumer.start(self.handle))

    async def stop(self):
        """컨슈머 태스크를 안전하게 중지합니다."""
        if self.task:
            self.task.cancel()
            await asyncio.gather(self.task, return_exceptions=True)