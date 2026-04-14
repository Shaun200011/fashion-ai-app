from pathlib import Path
from typing import Optional, Protocol

from app.core.config import settings


class ClassificationProvider(Protocol):
    def classify(self, *, file_path: str, original_filename: str) -> dict[str, Optional[str]]:
        ...


class MockClassificationProvider:
    def classify(self, *, file_path: str, original_filename: str) -> dict[str, Optional[str]]:
        stem = Path(original_filename).stem.replace("-", " ").replace("_", " ").strip() or "garment"
        lower_name = stem.lower()

        garment_type = "dress"
        if any(token in lower_name for token in ["jacket", "coat", "outerwear"]):
            garment_type = "outerwear"
        elif any(token in lower_name for token in ["shirt", "top", "blouse"]):
            garment_type = "top"
        elif any(token in lower_name for token in ["pant", "trouser", "jean"]):
            garment_type = "bottom"

        return {
            "description": (
                f"Placeholder classification for {stem}. "
                "This will be replaced by a multimodal model response."
            ),
            "garment_type": garment_type,
            "style": "contemporary",
            "material": "unknown",
            "color_palette": "neutral",
            "pattern": "solid",
            "season": "transitional",
            "occasion": "daywear",
            "consumer_profile": "fashion-conscious shopper",
            "trend_notes": "Placeholder metadata pending model integration.",
            "continent": None,
            "country": None,
            "city": None,
        }


def get_classification_provider() -> ClassificationProvider:
    if settings.ai_provider == "mock":
        return MockClassificationProvider()

    raise ValueError(f"Unsupported AI provider: {settings.ai_provider}")
