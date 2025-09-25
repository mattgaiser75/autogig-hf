from celery import Celery
from .config import settings

celery_app = Celery(
    "autogig",
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL,
)

@celery_app.task
def ping():
    return "pong"

@celery_app.task
def scout_leads():
    # TODO: Implement real connectors (Upwork API, Fiverr, etc.) with compliance.
    # For now, this just returns a stub result.
    return {"status": "ok", "found": 3, "notes": "Stubbed scout run."}
