from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, File, Form, UploadFile
from sqlmodel import Session

from app.db.session import get_session
from app.schemas.health import HealthResponse
from app.schemas.image import ImageUploadResponse
from app.services.images import create_image_record

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
