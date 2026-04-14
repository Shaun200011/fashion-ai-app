from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class ImageUploadResponse(BaseModel):
    id: int
    file_path: str
    original_filename: str
    designer_name: Optional[str] = None
    captured_at: Optional[datetime] = None
    created_at: datetime
