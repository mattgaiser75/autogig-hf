import uuid
from sqlalchemy import Column, String, Integer, Numeric, Boolean, ForeignKey, DateTime, JSON, Text
from sqlalchemy.dialects.postgresql import UUID, ARRAY
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from .database import Base

def gen_uuid():
    return str(uuid.uuid4())

class User(Base):
    __tablename__ = "users"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    email: Mapped[str] = mapped_column(String, unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Influencer(Base):
    __tablename__ = "influencers"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String, index=True)
    niche: Mapped[str] = mapped_column(String, default="general")
    tone: Mapped[str] = mapped_column(String, default="professional")
    platforms: Mapped[str] = mapped_column(Text, default="[]")  # JSON string list
    avatar_url: Mapped[str] = mapped_column(String, default="")
    bio: Mapped[str] = mapped_column(Text, default="")
    content_pillars: Mapped[str] = mapped_column(Text, default="[]")  # JSON string list
    posting_schedule: Mapped[str] = mapped_column(Text, default="{}")  # JSON string
    hooks_library: Mapped[str] = mapped_column(Text, default="[]")  # JSON string list
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Opportunity(Base):
    __tablename__ = "opportunities"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    source: Mapped[str] = mapped_column(String, default="manual")
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(Text, default="")
    client_name: Mapped[str] = mapped_column(String, default="")
    budget_min: Mapped[int | None] = mapped_column(Integer, nullable=True)
    budget_max: Mapped[int | None] = mapped_column(Integer, nullable=True)
    proposals_count: Mapped[int] = mapped_column(Integer, default=0)
    semantic_match_score: Mapped[float] = mapped_column(Numeric(5,2), default=0)
    final_rank_score: Mapped[float] = mapped_column(Numeric(5,2), default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class PitchTemplate(Base):
    __tablename__ = "pitch_templates"
    id: Mapped[str] = mapped_column(String, primary_key=True, default=gen_uuid)
    name: Mapped[str] = mapped_column(String)
    category: Mapped[str] = mapped_column(String, default="initial")
    template_content: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
