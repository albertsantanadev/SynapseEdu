from fastapi import FastAPI

from app.routers import resources

app = FastAPI(
    title="SynapseEdu API",
    description="Hub Inteligente de Recursos Educacionais",
    version="0.1.0",
)

app.include_router(resources.router)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}