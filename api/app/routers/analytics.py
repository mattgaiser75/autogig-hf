from fastapi import APIRouter

router = APIRouter(prefix="/analytics", tags=["analytics"])

@router.get("/insights")
def insights():
    return {
        "win_rate": 0.42,
        "avg_response_time_hours": 6.1,
        "active_opportunities": 7,
        "automation_health": "green"
    }
