from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc
from ..database import get_db
from ..models import Opportunity, Influencer
from ..schemas import OpportunityIn, OpportunityOut, PitchComposeRequest, PitchComposeResponse
from ..llm import generate_text, heuristic_pitch

router = APIRouter(prefix="/opportunities", tags=["opportunities"])

@router.get("", response_model=list[OpportunityOut])
def list_opportunities(db: Session = Depends(get_db)):
    items = db.query(Opportunity).order_by(desc(Opportunity.created_at)).all()
    return [_to_out(x) for x in items]

@router.post("", response_model=OpportunityOut)
def create_opportunity(payload: OpportunityIn, db: Session = Depends(get_db)):
    opp = Opportunity(
        title=payload.title,
        description=payload.description,
        source=payload.source,
        budget_min=payload.budget_min,
        budget_max=payload.budget_max,
        semantic_match_score=0.75,
        final_rank_score=0.68,
    )
    db.add(opp)
    db.commit()
    db.refresh(opp)
    return _to_out(opp)

@router.post("/{opportunity_id}/compose_pitch", response_model=PitchComposeResponse)
async def compose_pitch(opportunity_id: str, req: PitchComposeRequest, db: Session = Depends(get_db)):
    opp = db.query(Opportunity).filter(Opportunity.id == opportunity_id).first()
    if not opp:
        raise HTTPException(404, "Opportunity not found")
    inf = db.query(Influencer).filter(Influencer.id == req.influencer_id).first()
    if not inf:
        raise HTTPException(404, "Influencer not found")

    opp_d = {"title": opp.title, "description": opp.description}
    inf_d = {"name": inf.name, "niche": inf.niche, "tone": inf.tone}
    prompt = f"""Write a persuasive {req.style} pitch (120-160 words) for this opportunity using this persona.

Opportunity:
Title: {opp.title}
Description: {opp.description}

Persona:
Name: {inf.name}
Niche: {inf.niche}
Tone: {inf.tone}

Include a short CTA at the end.
"""
    result = await generate_text(prompt, model=req.model)
    if result:
        return PitchComposeResponse(pitch=result, used_llm=True)
    else:
        hp = heuristic_pitch(opp_d, inf_d, req.style)
        return PitchComposeResponse(pitch=hp, used_llm=False)

def _to_out(x: Opportunity) -> OpportunityOut:
    return OpportunityOut(
        id=x.id,
        title=x.title,
        description=x.description,
        source=x.source,
        client_name=x.client_name or None,
        budget_min=x.budget_min,
        budget_max=x.budget_max,
        proposals_count=x.proposals_count,
        semantic_match_score=float(x.semantic_match_score or 0),
        final_rank_score=float(x.final_rank_score or 0),
    )
