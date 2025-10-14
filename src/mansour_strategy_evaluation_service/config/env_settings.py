from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env", override=False)

profile = os.getenv("PROFILE", "local")
load_dotenv(dotenv_path=f".env.{profile}", override=True)  # ✅ 덮어쓰기 활성화!

class Settings(BaseSettings):
    PROFILE: str = profile
    SERVER_PORT: int
    EUREKA_SERVER_URL: str
    KAFKA_SERVER_HOST: str
    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(env_file_encoding="utf-8")

env = Settings()
