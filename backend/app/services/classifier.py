from app.schemas.classification import ClassificationResult


def classify_image_placeholder() -> ClassificationResult:
    return ClassificationResult(
        description="Placeholder result for the garment classification pipeline.",
        garment_type="unknown",
    )
