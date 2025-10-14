import asyncio
from contextlib import asynccontextmanager
from fastapi import FastAPI
import py_eureka_client.eureka_client as eureka_client
from mansour_strategy_evaluation_service.config.env_settings import env
import uvicorn

from mansour_strategy_evaluation_service.event.one_minute_candle_consumer import OneMinuteCandleConsumer
from mansour_strategy_evaluation_service.event.user_strategy_consumer import UserStrategyActivatedEventConsumer, UserStrategyDeactivatedEventConsumer

APP_NAME = "strategy-evaluation-service"
consumers = []

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- 애플리케이션 시작 시 실행될 코드 ---
    print("Initializing Eureka client...")
    await eureka_client.init_async(
        eureka_server=env.EUREKA_SERVER_URL,
        app_name=APP_NAME,
        instance_port=env.SERVER_PORT,
        instance_host="localhost"
    )
    print("✅ Eureka client initialized and service registered.")

    consumers.append(UserStrategyActivatedEventConsumer())
    consumers.append(UserStrategyDeactivatedEventConsumer())
    consumers.append(OneMinuteCandleConsumer())

    # 모든 컨슈머를 시작
    for consumer in consumers:
        consumer.start()
    
    yield # 이 지점에서 애플리케이션이 실행됩니다.
    
    # 모든 컨슈머를 중지
    for consumer in consumers:
        if consumer:
            await consumer.stop()

    # --- 애플리케이션 종료 시 실행될 코드 ---
    print("Stopping Eureka client...")
    await eureka_client.stop_async()
    print("✅ Eureka client stopped and service deregistered.")


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