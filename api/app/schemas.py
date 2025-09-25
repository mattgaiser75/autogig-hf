from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict, Optional

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class InfluencerCreate(BaseModel):
    name: str
    niche: str = "general"
    tone: str = "professional"
    platforms: List[str] = []
    brand_keywords: List[str] = []
    goals: List[str] = []
    model: Optional[str] = None  # LLM model id (e.g., 'phi3:mini')

class InfluencerOut(BaseModel):
    id: str
    name: str
    niche: str
    tone: str
    platforms: List[str]
    avatar_url: str
    bio: str
    content_pillars: List[str]
    posting_schedule: Dict[str, str]
    hooks_library: List[str]

class OpportunityIn(BaseModel):
    title: str
    description: str
    source: str = "manual"
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None

class OpportunityOut(BaseModel):
    id: str
    title: str
    description: str
    source: str
    client_name: str | None = None
    budget_min: Optional[int] = None
    budget_max: Optional[int] = None
    proposals_count: int
    semantic_match_score: float
    final_rank_score: float

class PitchComposeRequest(BaseModel):
    influencer_id: str
    style: str = "professional"
    model: Optional[str] = None  # LLM model id

class PitchComposeResponse(BaseModel):
    pitch: str
    used_llm: bool
