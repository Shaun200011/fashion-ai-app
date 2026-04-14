from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Image(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    file_path: str
    original_filename: str
    designer_name: Optional[str] = None
    captured_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class AiMetadata(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    image_id: int = Field(index=True, foreign_key="image.id")
    description: str
    garment_type: Optional[str] = None
    style: Optional[str] = None
    material: Optional[str] = None
    color_palette: Optional[str] = None
    pattern: Optional[str] = None
    season: Optional[str] = None
    occasion: Optional[str] = None
    consumer_profile: Optional[str] = None
    trend_notes: Optional[str] = None
    continent: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    raw_model_output: Optional[str] = None


class Annotation(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    image_id: int = Field(index=True, foreign_key="image.id")
    kind: str
    content: str
    author: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
