from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlmodel import Session

from app.db.models import Image
from app.db.session import get_session
from app.schemas.classification import ClassificationResponse
from app.schemas.health import HealthResponse
from app.schemas.image import ImageListItem, ImageUploadResponse
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
def get_images(session: Session = Depends(get_session)) -> list[ImageListItem]:
    return list_images(session)


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
        filename=image.original_filename,
    )
    return ClassificationResponse(image_id=image.id or 0, **result.model_dump())
