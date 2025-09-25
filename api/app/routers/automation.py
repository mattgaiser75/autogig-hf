from fastapi import APIRouter
from ..celery_app import scout_leads

router = APIRouter(prefix="/automation", tags=["automation"])

@router.post("/run_scout")
def run_scout():
    task = scout_leads.delay()
    return {"status": "queued", "task_id": task.id}
