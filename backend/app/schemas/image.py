from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemas.annotation import AnnotationResponse
from app.schemas.classification import ClassificationResult


class ImageUploadResponse(BaseModel):
    id: int
    file_path: str
    image_url: str
    original_filename: str
    designer_name: Optional[str] = None
    captured_at: Optional[datetime] = None
    created_at: datetime
    ai_metadata: Optional[ClassificationResult] = None


class ImageListItem(BaseModel):
    id: int
    file_path: str
    image_url: str
    original_filename: str
    designer_name: Optional[str] = None
    captured_at: Optional[datetime] = None
    created_at: datetime
    ai_metadata: Optional[ClassificationResult] = None
    annotations: list[AnnotationResponse] = []
