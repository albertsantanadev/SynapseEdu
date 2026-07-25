import uuid

from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.orm import Session

from app.crud import resource as crud
from app.db.database import get_db
from app.schemas.resource import (
    ResourceCreate,
    ResourceUpdate,
    ResourceOut,
    PaginatedResources,
    SmartAssistRequest,
    SmartAssistResponse,
)
from app.services.ai_service import generate_description, AIServiceError

router = APIRouter(prefix="/api/v1/resources", tags=["resources"])


@router.post("", response_model=ResourceOut, status_code=201)
def create_resource(resource_in: ResourceCreate, db: Session = Depends(get_db)):
    return crud.create_resource(db, resource_in)


@router.get("", response_model=PaginatedResources)
def list_resources(
    page: int = Query(default=1, ge=1),
    size: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    skip = (page - 1) * size
    items, total = crud.get_resources(db, skip=skip, limit=size)
    return {"items": items, "total": total, "page": page}


@router.post("/smart-assist", response_model=SmartAssistResponse)
def smart_assist(payload: SmartAssistRequest):
    try:
        result = generate_description(payload.title, payload.type.value)
    except AIServiceError:
        raise HTTPException(status_code=502, detail="Não foi possível gerar sugestão da IA no momento")
    return result


@router.get("/{resource_id}", response_model=ResourceOut)
def get_resource(resource_id: uuid.UUID, db: Session = Depends(get_db)):
    db_resource = crud.get_resource(db, resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    return db_resource


@router.put("/{resource_id}", response_model=ResourceOut)
def update_resource(resource_id: uuid.UUID, resource_in: ResourceUpdate, db: Session = Depends(get_db)):
    db_resource = crud.get_resource(db, resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    return crud.update_resource(db, db_resource, resource_in)


@router.delete("/{resource_id}", status_code=204)
def delete_resource(resource_id: uuid.UUID, db: Session = Depends(get_db)):
    db_resource = crud.get_resource(db, resource_id)
    if db_resource is None:
        raise HTTPException(status_code=404, detail="Recurso não encontrado")
    crud.delete_resource(db, db_resource)