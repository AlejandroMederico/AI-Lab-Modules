from pydantic_settings import BaseSettings
from typing import Optional


class IndeedConfig(BaseSettings):
    INDEED_API_KEY: Optional[str] = None
    INDEED_BASE_URL: str = "https://api.indeed.com"
    
    class Config:
        env_prefix = "INDEED_"

indeed_config = IndeedConfig()
