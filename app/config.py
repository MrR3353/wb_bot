import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = os.path.join(Path(os.path.dirname(__file__)).parent, ".env")


class Settings(BaseSettings):
    SCHEDULER_INTERVAL: float = 30
    BOT_TOKEN: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    model_config = SettingsConfigDict(env_file=DOTENV_PATH)


settings = Settings()
