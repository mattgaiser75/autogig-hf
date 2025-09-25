import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Influencer
from ..schemas import InfluencerCreate, InfluencerOut
from ..llm import generate_text

router = APIRouter(prefix="/influencers", tags=["influencers"])

@router.get("", response_model=list[InfluencerOut])
def list_influencers(db: Session = Depends(get_db)):
    items = db.query(Influencer).order_by(Influencer.created_at.desc()).all()
    out = []
    for f in items:
        out.append(_to_out(f))
    return out

@router.post("", response_model=InfluencerOut)
async def create_influencer(payload: InfluencerCreate, db: Session = Depends(get_db)):
    # Heuristic defaults
    avatar = f"https://api.dicebear.com/7.x/shapes/svg?seed={payload.name.replace(' ','%20')}"
    pillars = [
        f"{payload.niche} tips",
        f"Behind-the-scenes in {payload.niche}",
        "Case studies / transformations",
        "Tool breakdowns & workflows"
    ]
    schedule = {"Mon": "2 posts", "Wed": "1 post + 1 short", "Fri": "2 shorts", "Sun": "1 longform"}
    hooks = ["You won't believe this trick…", "The fastest way to…", "What nobody tells you about…"]

    persona_bio = f"{payload.name} is a {payload.niche} creator with a {payload.tone} voice helping clients win more with smart systems."

    # If LLM available, enrich the bio + hooks
    prompt = f"""Create a 90-word bio, 6 content pillars, and 8 strong hooks for an influencer persona.
Name: {payload.name}
Niche: {payload.niche}
Tone: {payload.tone}
Platforms: {', '.join(payload.platforms)}
Brand keywords: {', '.join(payload.brand_keywords)}
Goals: {', '.join(payload.goals)}
Return as JSON with keys: bio, pillars, hooks."""
    enriched = await generate_text(prompt, model=payload.model)
    if enriched:
        try:
            data = json.loads(enriched)
            persona_bio = data.get("bio", persona_bio)
            pillars = data.get("pillars", pillars)
            hooks = data.get("hooks", hooks)
        except Exception:
            pass

    inf = Influencer(
        name=payload.name,
        niche=payload.niche,
        tone=payload.tone,
        platforms=json.dumps(payload.platforms),
        avatar_url=avatar,
        bio=persona_bio,
        content_pillars=json.dumps(pillars),
        posting_schedule=json.dumps(schedule),
        hooks_library=json.dumps(hooks)
    )
    db.add(inf)
    db.commit()
    db.refresh(inf)
    return _to_out(inf)

def _to_out(f: Influencer) -> InfluencerOut:
    return InfluencerOut(
        id=f.id,
        name=f.name,
        niche=f.niche,
        tone=f.tone,
        platforms=json.loads(f.platforms or "[]"),
        avatar_url=f.avatar_url or "",
        bio=f.bio or "",
        content_pillars=json.loads(f.content_pillars or "[]"),
        posting_schedule=json.loads(f.posting_schedule or "{}"),
        hooks_library=json.loads(f.hooks_library or "[]"),
    )
