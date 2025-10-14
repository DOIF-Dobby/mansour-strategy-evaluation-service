from datetime import datetime
from decimal import Decimal
from mansour_strategy_evaluation_service.core.kafka.base_consumer import BaseConsumer
from mansour_strategy_evaluation_service.model.one_minute_candle import OneMinuteCandle
from mansour_strategy_evaluation_service.service.evaluation_coordinator import evaluation_coordinator

class OneMinuteCandleConsumer(BaseConsumer):
    TOPIC = "marketdata.candles.1m"

    def __init__(self):
        super().__init__()
        print("OneMinuteCandleConsumer initialized.")

    async def handle(self, message):
        try:
            print(f"message.value: {message.value}")
            
            data_dict = message.value

            candle = OneMinuteCandle(
                symbol=data_dict['symbol'],
                open=Decimal(str(data_dict['open'])),
                high=Decimal(str(data_dict['high'])),
                low=Decimal(str(data_dict['low'])),
                close=Decimal(str(data_dict['close'])),
                volume=int(data_dict['volume']),
                windowStartTime=datetime.fromtimestamp(data_dict['windowStartTime']),
                windowEndTime=datetime.fromtimestamp(data_dict['windowEndTime'])
            )

            print(f"🕯️ Successfully parsed candle: {candle}")

            await evaluation_coordinator.process_candle(candle)

        except Exception as e:
            print(f"🔥 Error processing message in UserStrategyEventConsumer: {e}")