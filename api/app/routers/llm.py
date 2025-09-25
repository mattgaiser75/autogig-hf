from fastapi import APIRouter
from ..llm import HF_MODELS
from ..config import settings

router = APIRouter(prefix="/llm", tags=["llm"])

@router.get("/models")
def list_models():
    return {
        "provider": settings.LLM_PROVIDER,
        "default": settings.LLM_DEFAULT_MODEL,
        "models": HF_MODELS,
        "api_base": settings.HUGGINGFACE_API_BASE,
    }
