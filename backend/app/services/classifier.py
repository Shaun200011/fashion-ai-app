from app.schemas.classification import ClassificationResult
from app.services.classification_parser import parse_classification_payload
from app.services.classification_provider import get_classification_provider


def classify_image(file_path: str, original_filename: str) -> ClassificationResult:
    provider = get_classification_provider()
    raw_payload = provider.classify(file_path=file_path, original_filename=original_filename)
    return parse_classification_payload(raw_payload)
