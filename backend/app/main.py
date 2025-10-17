from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .routers import trends, history
from .settings import settings

app = FastAPI(title="TrendLens API")

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
