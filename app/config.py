from pydantic_settings import BaseSettings
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    groq_api_key: Optional[str] = None
    db_url: str = "sqlite+aiosqlite:///./ai_sales_agent.db"
    project_name: str = "AI Sales Agent"
    email_mock_port: int = 1025
    api_host: str = "localhost"
    api_port: int = 8000
    use_mock_ai: bool = False
    followup_interval_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()