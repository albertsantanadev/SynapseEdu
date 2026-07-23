import uuid

from sqlalchemy.orm import Session

from app.db.models import Resource
from app.schemas.resource import ResourceCreate


def create_resource(db: Session, resource_in: ResourceCreate) -> Resource:
    db_resource = Resource(**resource_in.model_dump(mode="json"))
    db.add(db_resource)
    db.commit()
    db.refresh(db_resource)
    return db_resource


def get_resource(db: Session, resource_id: uuid.UUID) -> Resource | None:
    return db.query(Resource).filter(Resource.id == resource_id).first()


def get_resources(db: Session, skip: int = 0, limit: int = 10) -> tuple[list[Resource], int]:
    total = db.query(Resource).count()
    items = db.query(Resource).offset(skip).limit(limit).all()
    return items, total