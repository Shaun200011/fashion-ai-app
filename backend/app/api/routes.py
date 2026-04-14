from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlmodel import Session

from app.db.models import Image
from app.db.session import get_session
from app.schemas.annotation import AnnotationCreate, AnnotationResponse
from app.schemas.classification import ClassificationResponse
from app.schemas.filter import FilterGroup
from app.schemas.health import HealthResponse
from app.schemas.image import ImageListItem, ImageUploadResponse
from app.services.annotations import create_annotation
from app.services.filters import list_filter_groups
from app.services.images import create_image_record, list_images
from app.services.metadata import classify_and_store_metadata

router = APIRouter()


@router.get("/health", response_model=HealthResponse, tags=["system"])
def health_check() -> HealthResponse:
    return HealthResponse(status="ok")


@router.post("/images/upload", response_model=ImageUploadResponse, tags=["images"])
def upload_image(
    file: UploadFile = File(...),
    designer_name: Optional[str] = Form(default=None),
    captured_at: Optional[datetime] = Form(default=None),
    session: Session = Depends(get_session),
) -> ImageUploadResponse:
    return create_image_record(
        session=session,
        file=file,
        designer_name=designer_name,
        captured_at=captured_at,
    )


@router.get("/images", response_model=list[ImageListItem], tags=["images"])
def get_images(
    query: Optional[str] = None,
    garment_type: Optional[str] = None,
    material: Optional[str] = None,
    season: Optional[str] = None,
    occasion: Optional[str] = None,
    session: Session = Depends(get_session),
) -> list[ImageListItem]:
    return list_images(
        session,
        query=query,
        garment_type=garment_type,
        material=material,
        season=season,
        occasion=occasion,
    )


@router.get("/filters", response_model=list[FilterGroup], tags=["images"])
def get_filters(session: Session = Depends(get_session)) -> list[FilterGroup]:
    return list_filter_groups(session)


@router.post(
    "/images/{image_id}/classify",
    response_model=ClassificationResponse,
    tags=["classification"],
)
def classify_image(image_id: int, session: Session = Depends(get_session)) -> ClassificationResponse:
    image = session.get(Image, image_id)
    if image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    result = classify_and_store_metadata(
        session=session,
        image_id=image.id or 0,
        file_path=image.file_path,
        original_filename=image.original_filename,
    )
    return ClassificationResponse(image_id=image.id or 0, **result.model_dump())


@router.post(
    "/images/{image_id}/annotations",
    response_model=AnnotationResponse,
    tags=["annotations"],
)
def create_image_annotation(
    image_id: int,
    payload: AnnotationCreate,
    session: Session = Depends(get_session),
) -> AnnotationResponse:
    try:
        return create_annotation(session, image_id=image_id, payload=payload)
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
