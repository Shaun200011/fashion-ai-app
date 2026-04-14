from app.schemas.classification import ClassificationResult
from app.services.classification_parser import parse_classification_payload
from app.services.classification_provider import (
    MockClassificationProvider,
    get_classification_provider,
)


def classify_image(file_path: str, original_filename: str) -> ClassificationResult:
    try:
        provider = get_classification_provider()
        raw_payload = provider.classify(file_path=file_path, original_filename=original_filename)
    except Exception:
        fallback_provider = MockClassificationProvider()
        raw_payload = fallback_provider.classify(
            file_path=file_path,
            original_filename=original_filename,
        )

    return parse_classification_payload(raw_payload)
