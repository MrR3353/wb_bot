import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = os.path.join(Path(os.path.dirname(__file__)).parent, ".env")


class Settings(BaseSettings):
    SCHEDULER_INTERVAL: float = 30
    BEARER_TOKEN: str
    BOT_TOKEN: str
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    model_config = SettingsConfigDict(env_file=DOTENV_PATH)


settings = Settings()
