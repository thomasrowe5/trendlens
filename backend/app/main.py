from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .db import Base, engine
from .models import TrendSample
from .routers import history, trends
from .settings import settings

app = FastAPI(title="TrendLens API")

# Ensure tables exist on startup
Base.metadata.create_all(bind=engine)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.ALLOWED_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(trends.router)
app.include_router(history.router)

@app.get("/healthz")
def health():
    return {"ok": True}
