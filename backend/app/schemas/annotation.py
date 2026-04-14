from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class AnnotationCreate(BaseModel):
    kind: str = "note"
    content: str
    author: Optional[str] = None


class AnnotationResponse(BaseModel):
    id: int
    image_id: int
    kind: str
    content: str
    author: Optional[str] = None
    created_at: datetime
