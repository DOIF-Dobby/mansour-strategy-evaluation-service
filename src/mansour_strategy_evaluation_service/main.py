import asyncio
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
import py_eureka_client.eureka_client as eureka_client
from mansour_strategy_evaluation_service.config.env_settings import env
from mansour_strategy_evaluation_service.config.logging_config import setup_logging, get_logger
import uvicorn

from mansour_strategy_evaluation_service.event.one_minute_candle_consumer import OneMinuteCandleConsumer
from mansour_strategy_evaluation_service.event.user_strategy_consumer import UserStrategyActivatedEventConsumer, UserStrategyDeactivatedEventConsumer

# 로깅 설정
setup_logging()
logger = get_logger(__name__)

APP_NAME = "strategy-evaluation-service"

class ConsumerManager:
    """Kafka 컨슈머들을 관리하는 클래스"""
    
    def __init__(self):
        self.consumers = [
            UserStrategyActivatedEventConsumer(),
            UserStrategyDeactivatedEventConsumer(),
            OneMinuteCandleConsumer()
        ]
    
    async def start_all(self):
        """모든 컨슈머 시작"""
        for consumer in self.consumers:
            consumer.start()
        logger.info(f"✅ Started {len(self.consumers)} consumers")
    
    async def stop_all(self):
        """모든 컨슈머 중지"""
        await asyncio.gather(*(consumer.stop() for consumer in self.consumers if consumer))
        logger.info("✅ All consumers stopped")

@asynccontextmanager
async def lifespan(app: FastAPI):
    consumer_manager = ConsumerManager()
    
    # --- 애플리케이션 시작 시 실행될 코드 ---
    logger.info("Initializing Eureka client...")
    await eureka_client.init_async(
        eureka_server=env.EUREKA_SERVER_URL,
        app_name=APP_NAME,
        instance_port=env.SERVER_PORT,
        instance_host="localhost"
    )
    logger.info("✅ Eureka client initialized and service registered.")

    await consumer_manager.start_all()
    
    yield # 이 지점에서 애플리케이션이 실행됩니다.
    
    await consumer_manager.stop_all()

    # --- 애플리케이션 종료 시 실행될 코드 ---
    logger.info("Stopping Eureka client...")
    await eureka_client.stop_async()
    logger.info("✅ Eureka client stopped and service deregistered.")


app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health_check():
    return {"status": "UP"}

def start():
    uvicorn.run(
        "mansour_strategy_evaluation_service.main:app",
        host="0.0.0.0",
        port=env.SERVER_PORT,
        reload=True
    )

if __name__ == "__main__":
    start()