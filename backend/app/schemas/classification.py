from typing import Optional

from pydantic import BaseModel


class ClassificationResult(BaseModel):
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

