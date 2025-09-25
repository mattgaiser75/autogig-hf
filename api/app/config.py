from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    DATABASE_URL: str = Field(..., description="SQLAlchemy URL, e.g. postgresql+psycopg://...")
    REDIS_URL: str = "redis://localhost:6379/0"
    JWT_SECRET: str = "change-me"
    ENCRYPTION_KEY: str = "change-me-32bytes"
    # LLM settings
    LLM_PROVIDER: str = "huggingface"  # "huggingface" | "ollama" | "openai" | "openrouter" | "none"
    LLM_DEFAULT_MODEL: str = "microsoft/Phi-3-mini-4k-instruct"

    # Hugging Face Inference API
    HUGGINGFACE_API_BASE: str = "https://api-inference.huggingface.co/models"
    HUGGINGFACE_API_KEY: str | None = None

    # (legacy/optional) other providers
    OLLAMA_BASE: str = "http://localhost:11434"
    OPENAI_API_BASE: str = "https://api.openai.com/v1"
    OPENAI_API_KEY: str | None = None
    OPENROUTER_API_BASE: str = "https://openrouter.ai/api/v1"
    OPENROUTER_API_KEY: str | None = None

settings = Settings()
