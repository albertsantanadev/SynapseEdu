from fastapi import FastAPI

from app.routers import resource

app = FastAPI(
    title="SynapseEdu API",
    description="Hub Inteligente de Recursos Educacionais",
    version="0.1.0",
)

from app.db.database import Base, engine
from app.db import models  # necessário para o Base "conhecer" a classe Resource

Base.metadata.create_all(bind=engine)

app.include_router(resource.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}