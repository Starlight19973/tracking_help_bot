import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    bot_token: str
    db_url: str

    class Config:
        env_file = ".env"


settings = Settings()