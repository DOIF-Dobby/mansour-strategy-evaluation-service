import redis
from mansour_strategy_evaluation_service.config.env_settings import env

redis_client = redis.Redis(host=env.REDIS_HOST, port=env.REDIS_PORT, decode_responses=True)
