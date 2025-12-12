from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "AI Student Query Chatbot"
    MONGO_URL: Optional[str] = "mongodb://localhost:27017"
    DATABASE_NAME: str = "student_chatbot"
    USE_JSON_DB: bool = False
    Json_DB_PATH: str = "data/db.json"
    
    class Config:
        env_file = ".env"

settings = Settings()
