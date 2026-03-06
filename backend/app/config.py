import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "CV Craft"
    DATABASE_URL: str = "sqlite:///./data/cvcraft.db"
    SECRET_KEY: str = "change-me-in-production-use-env-var"
    OPENAI_API_KEY: str = ""
    OPENAI_BASE_URL: str = "https://api.openai.com/v1"
    AI_MODEL: str = "gpt-4o-mini"
    AI_MODEL_SMART: str = "gpt-4o"
    UPLOAD_DIR: str = "./data/uploads"
    CV_OUTPUT_DIR: str = "./data/cvs"
    MAX_CONTEXT_MESSAGES: int = 20
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    class Config:
        env_file = ".env"


settings = Settings()

os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
os.makedirs(settings.CV_OUTPUT_DIR, exist_ok=True)
os.makedirs("./data", exist_ok=True)
