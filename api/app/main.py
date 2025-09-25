from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from .database import Base, engine, SessionLocal
from .models import User
from .security import hash_password
from .routers import auth, influencers, opportunities, automation, analytics, llm

app = FastAPI(title="AutoGig Platform API", version="2.0.0", docs_url="/docs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create tables on startup and seed admin
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)
    db: Session = SessionLocal()
    try:
        if not db.query(User).filter(User.email=="admin@example.com").first():
            db.add(User(email="admin@example.com", password_hash=hash_password("admin123")))
            db.commit()
    finally:
        db.close()

@app.get("/health")
def health():
    return {"ok": True}

app.include_router(auth.router, prefix="/auth")
app.include_router(influencers.router)
app.include_router(opportunities.router)
app.include_router(automation.router)
app.include_router(analytics.router)
app.include_router(llm.router)
