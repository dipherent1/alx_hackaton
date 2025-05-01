from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):

    GOOGLE_API_KEY: str
    DB_CONNECTION_URI: str

    

    class Config:
        env_file = ".env"  # Specify the .env file to load variables from


def get_settings():
    return Settings()