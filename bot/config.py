import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    bot_token: str
    db_url: str
    postgres_password: str
    postgres_user: str
    postgres_host: str
    postgres_db: str
    postgres_port: int = 5432

    class Config:
        env_file = ".env"


settings = Settings()