from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.crud import resource as crud
from app.db.database import get_db
from app.schemas.resource import ResourceCreate, ResourceOut, PaginatedResources

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