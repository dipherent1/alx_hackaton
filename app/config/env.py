from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    token: str 
    endpoint: str 
    model_name: str

    

    class Config:
        env_file = ".env"  # Specify the .env file to load variables from


def get_settings():
    return Settings()
