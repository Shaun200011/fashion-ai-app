from typing import Any, Optional

from app.schemas.classification import ClassificationResult


CANONICAL_DEFAULTS = {
    "style": "contemporary",
    "material": "unknown",
    "color_palette": "neutral",
    "pattern": "solid",
    "season": "transitional",
    "occasion": "daywear",
    "consumer_profile": "fashion-conscious shopper",
}


def parse_classification_payload(payload: dict[str, Any]) -> ClassificationResult:
    cleaned = {
        "description": _normalize_text(payload.get("description")) or "No description generated.",
        "garment_type": _normalize_text(payload.get("garment_type")) or "unknown",
        "style": _normalize_text(payload.get("style")) or CANONICAL_DEFAULTS["style"],
        "material": _normalize_text(payload.get("material")) or CANONICAL_DEFAULTS["material"],
        "color_palette": _normalize_text(payload.get("color_palette")) or CANONICAL_DEFAULTS["color_palette"],
        "pattern": _normalize_text(payload.get("pattern")) or CANONICAL_DEFAULTS["pattern"],
        "season": _normalize_text(payload.get("season")) or CANONICAL_DEFAULTS["season"],
        "occasion": _normalize_text(payload.get("occasion")) or CANONICAL_DEFAULTS["occasion"],
        "consumer_profile": _normalize_text(payload.get("consumer_profile"))
        or CANONICAL_DEFAULTS["consumer_profile"],
        "trend_notes": _normalize_text(payload.get("trend_notes")),
        "continent": _normalize_text(payload.get("continent")),
        "country": _normalize_text(payload.get("country")),
        "city": _normalize_text(payload.get("city")),
    }
    return ClassificationResult(**cleaned)


def _normalize_text(value: Any) -> Optional[str]:
    if value is None:
        return None
    text = str(value).strip()
    return text or None
