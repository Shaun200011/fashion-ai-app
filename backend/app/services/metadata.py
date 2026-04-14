from sqlmodel import Session, select

from app.db.models import AiMetadata
from app.schemas.classification import ClassificationResult
from app.services.classifier import classify_image_placeholder


def classify_and_store_metadata(session: Session, image_id: int, filename: str) -> ClassificationResult:
    result = classify_image_placeholder(filename)

    existing = session.exec(select(AiMetadata).where(AiMetadata.image_id == image_id)).first()
    if existing:
        existing.description = result.description
        existing.garment_type = result.garment_type
        existing.style = result.style
        existing.material = result.material
        existing.color_palette = result.color_palette
        existing.pattern = result.pattern
        existing.season = result.season
        existing.occasion = result.occasion
        existing.consumer_profile = result.consumer_profile
        existing.trend_notes = result.trend_notes
        existing.continent = result.continent
        existing.country = result.country
        existing.city = result.city
        existing.raw_model_output = result.model_dump_json()
        session.add(existing)
    else:
        session.add(
            AiMetadata(
                image_id=image_id,
                description=result.description,
                garment_type=result.garment_type,
                style=result.style,
                material=result.material,
                color_palette=result.color_palette,
                pattern=result.pattern,
                season=result.season,
                occasion=result.occasion,
                consumer_profile=result.consumer_profile,
                trend_notes=result.trend_notes,
                continent=result.continent,
                country=result.country,
                city=result.city,
                raw_model_output=result.model_dump_json(),
            )
        )

    session.commit()
    return result
