import base64
import json
import re
from pathlib import Path
from typing import Any, Optional, Protocol
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

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


class OpenAIClassificationProvider:
    def classify(self, *, file_path: str, original_filename: str) -> dict[str, Optional[str]]:
        with open(file_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

        suffix = Path(original_filename).suffix.lower()
        mime_type = _guess_mime_type(suffix)
        prompt = (
            "Analyze this fashion inspiration image and return JSON only with these keys: "
            "description, garment_type, style, material, color_palette, pattern, season, "
            "occasion, consumer_profile, trend_notes, continent, country, city. "
            "Use null for unknown fields."
        )
        payload = {
            "model": settings.openai_model,
            "input": [
                {
                    "role": "user",
                    "content": [
                        {"type": "input_text", "text": prompt},
                        {
                            "type": "input_image",
                            "image_url": f"data:{mime_type};base64,{encoded_image}",
                            "detail": settings.openai_image_detail,
                        },
                    ],
                }
            ],
        }

        request = Request(
            settings.openai_base_url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {settings.openai_api_key}",
            },
            method="POST",
        )

        try:
            with urlopen(request, timeout=settings.openai_timeout_seconds) as response:
                raw_response = json.loads(response.read().decode("utf-8"))
        except (HTTPError, URLError, TimeoutError) as exc:
            raise RuntimeError(f"OpenAI classification request failed: {exc}") from exc

        return _extract_json_payload(raw_response)


def get_classification_provider() -> ClassificationProvider:
    if settings.ai_provider == "mock":
        return MockClassificationProvider()
    if settings.ai_provider == "openai":
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY is required when AI_PROVIDER=openai")
        return OpenAIClassificationProvider()
    if settings.ai_provider == "auto":
        if settings.openai_api_key:
            return OpenAIClassificationProvider()
        return MockClassificationProvider()

    raise ValueError(f"Unsupported AI provider: {settings.ai_provider}")


def _extract_json_payload(raw_response: dict[str, Any]) -> dict[str, Optional[str]]:
    if isinstance(raw_response.get("output_text"), str):
        try:
            return json.loads(_strip_json_fences(raw_response["output_text"]))
        except json.JSONDecodeError as exc:
            raise RuntimeError("OpenAI response did not contain valid JSON in output_text") from exc

    for output_item in raw_response.get("output", []):
        for content_item in output_item.get("content", []):
            if content_item.get("type") == "output_text" and isinstance(content_item.get("text"), str):
                try:
                    return json.loads(_strip_json_fences(content_item["text"]))
                except json.JSONDecodeError as exc:
                    raise RuntimeError("OpenAI response text was not valid JSON") from exc

    raise RuntimeError("OpenAI response did not contain parsable JSON output")


def _guess_mime_type(suffix: str) -> str:
    if suffix in {".png"}:
        return "image/png"
    if suffix in {".webp"}:
        return "image/webp"
    if suffix in {".gif"}:
        return "image/gif"
    return "image/jpeg"


def _strip_json_fences(text: str) -> str:
    stripped = text.strip()
    fenced = re.match(r"^```(?:json)?\s*(.*?)\s*```$", stripped, re.DOTALL)
    if fenced:
        return fenced.group(1).strip()
    return stripped
