from pathlib import Path

from app.schemas.classification import ClassificationResult


def classify_image_placeholder(filename: str) -> ClassificationResult:
    stem = Path(filename).stem.replace("-", " ").replace("_", " ").strip() or "garment"
    lower_name = stem.lower()

    garment_type = "dress"
    if any(token in lower_name for token in ["jacket", "coat", "outerwear"]):
        garment_type = "outerwear"
    elif any(token in lower_name for token in ["shirt", "top", "blouse"]):
        garment_type = "top"
    elif any(token in lower_name for token in ["pant", "trouser", "jean"]):
        garment_type = "bottom"

    return ClassificationResult(
        description=f"Placeholder classification for {stem}. This will be replaced by a multimodal model response.",
        garment_type=garment_type,
        style="contemporary",
        material="unknown",
        color_palette="neutral",
        pattern="solid",
        season="transitional",
        occasion="daywear",
        consumer_profile="fashion-conscious shopper",
        trend_notes="Placeholder metadata pending model integration.",
    )
