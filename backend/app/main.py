from fastapi import FastAPI
from sqlalchemy import text

from app.core.logging_config import setup_logging
from app.db.database import engine
from app.routers import resource

setup_logging()

app = FastAPI(
    title="SynapseEdu API",
    description="Hub Inteligente de Recursos Educacionais",
    version="0.1.0",
)

app.include_router(resource.router)


@app.get("/health", tags=["health"])
def health_check():
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        db_status = "ok"
    except Exception:
        db_status = "unavailable"

    return {"status": "ok", "database": db_status}