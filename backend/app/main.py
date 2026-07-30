import json
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from app.core.logging_config import setup_logging
from app.db.database import engine
from app.routers import resource

load_dotenv()
setup_logging()

app = FastAPI(
    title="SynapseEdu API",
    description="Hub Inteligente de Recursos Educacionais",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "https://synapse-edu-one.vercel.app",  # URL do deploy
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Origens autorizadas por padrão
origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Lê origens do .env caso configurado
raw_origins = os.getenv("BACKEND_CORS_ORIGINS")
if raw_origins:
    clean_raw = raw_origins.strip().strip("\"'")
    if clean_raw.startswith("["):
        try:
            origins.extend(json.loads(clean_raw))
        except json.JSONDecodeError:
            pass
    else:
        parsed = [o.strip(" \"'") for o in clean_raw.split(",") if o.strip()]
        origins.extend(parsed)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
