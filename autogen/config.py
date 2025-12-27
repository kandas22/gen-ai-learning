"""Configuration management for SEO Content Generator"""
import os
from typing import Tuple, Optional
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    SERPAPI_API_KEY: str = os.getenv("SERPAPI_API_KEY", "")
    
    # Email
    SMTP_SERVER: str = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USERNAME: str = os.getenv("SMTP_USERNAME", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")
    
    # Model
    DEFAULT_MODEL: str = os.getenv("DEFAULT_MODEL", "gpt-4o-mini")
    
    @classmethod
    def validate(cls) -> Tuple[bool, Optional[str]]:
        """Validate configuration"""
        if not cls.OPENAI_API_KEY:
            return False, "OPENAI_API_KEY missing in .env file"
        if not cls.SERPAPI_API_KEY:
            return False, "SERPAPI_API_KEY missing in .env file"
        # SMTP settings are optional; if missing, email delivery will be disabled
        if not cls.SMTP_USERNAME or not cls.SMTP_PASSWORD:
            return True, "SMTP credentials missing; email delivery will be disabled"

        return True, None
