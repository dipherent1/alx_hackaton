from pydantic_settings import BaseSettings
from functools import lru_cache
from dotenv import load_dotenv
import os

# Explicitly load the .env file
load_dotenv(".env")
# Load environment variables from the .env file
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")
os.environ["DB_CONNECTION_URI"] = os.getenv("DB_CONNECTION_URI")

# class Settings(BaseSettings):
#     GOOGLE_API_KEY: str
#     DB_CONNECTION_URI: str

#     class Config:
#         env_file = ".env"  # Specify the .env file to load variables from


# @lru_cache()
# def get_settings():
#     return Settings()