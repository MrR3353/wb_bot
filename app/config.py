import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

DOTENV_PATH = os.path.join(Path(os.path.dirname(__file__)).parent, ".env")


class Settings(BaseSettings):
    BOT_TOKEN: str
    SCHEDULER_INTERVAL: int = 30
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    model_config = SettingsConfigDict(env_file=DOTENV_PATH)


settings = Settings()
