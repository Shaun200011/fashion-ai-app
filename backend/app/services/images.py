from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import UploadFile
from sqlmodel import Session, select

from app.db.models import AiMetadata, Image
from app.schemas.classification import ClassificationResult
from app.schemas.image import ImageListItem, ImageUploadResponse
from app.services.metadata import classify_and_store_metadata
from app.services.storage import save_upload_file


def create_image_record(
    session: Session,
    file: UploadFile,
    designer_name: Optional[str] = None,
    captured_at: Optional[datetime] = None,
) -> ImageUploadResponse:
    file_path, _stored_name = save_upload_file(file)

    image = Image(
        file_path=file_path,
        original_filename=file.filename or Path(file_path).name,
        designer_name=designer_name,
        captured_at=captured_at,
    )
    session.add(image)
    session.commit()
    session.refresh(image)
    ai_metadata = classify_and_store_metadata(
        session=session,
        image_id=image.id or 0,
        filename=image.original_filename,
    )

    return ImageUploadResponse(
        id=image.id or 0,
        file_path=image.file_path,
        original_filename=image.original_filename,
        designer_name=image.designer_name,
        captured_at=image.captured_at,
        created_at=image.created_at,
        ai_metadata=ai_metadata,
    )


def _matches_query(image: Image, metadata: Optional[AiMetadata], query: str) -> bool:
    haystacks = [
        image.original_filename,
        image.designer_name or "",
        metadata.description if metadata else "",
        metadata.garment_type if metadata else "",
        metadata.material if metadata else "",
        metadata.season if metadata else "",
        metadata.occasion if metadata else "",
        metadata.trend_notes if metadata else "",
        metadata.city if metadata else "",
        metadata.country if metadata else "",
        metadata.continent if metadata else "",
    ]
    normalized_query = query.strip().lower()
    return any(normalized_query in value.lower() for value in haystacks if value)


def _matches_exact_filter(metadata: Optional[AiMetadata], field_name: str, expected: Optional[str]) -> bool:
    if not expected:
        return True
    if metadata is None:
        return False
    current = getattr(metadata, field_name, None)
    return current == expected


def list_images(
    session: Session,
    query: Optional[str] = None,
    garment_type: Optional[str] = None,
    material: Optional[str] = None,
    season: Optional[str] = None,
    occasion: Optional[str] = None,
) -> list[ImageListItem]:
    images = session.exec(select(Image).order_by(Image.created_at.desc())).all()
    metadata_rows = session.exec(select(AiMetadata)).all()
    metadata_by_image_id = {row.image_id: row for row in metadata_rows}
    items: list[ImageListItem] = []

    for image in images:
        metadata_row = metadata_by_image_id.get(image.id or 0)

        if query and not _matches_query(image, metadata_row, query):
            continue
        if not _matches_exact_filter(metadata_row, "garment_type", garment_type):
            continue
        if not _matches_exact_filter(metadata_row, "material", material):
            continue
        if not _matches_exact_filter(metadata_row, "season", season):
            continue
        if not _matches_exact_filter(metadata_row, "occasion", occasion):
            continue

        classification = (
            ClassificationResult(
                description=metadata_row.description,
                garment_type=metadata_row.garment_type,
                style=metadata_row.style,
                material=metadata_row.material,
                color_palette=metadata_row.color_palette,
                pattern=metadata_row.pattern,
                season=metadata_row.season,
                occasion=metadata_row.occasion,
                consumer_profile=metadata_row.consumer_profile,
                trend_notes=metadata_row.trend_notes,
                continent=metadata_row.continent,
                country=metadata_row.country,
                city=metadata_row.city,
            )
            if metadata_row
            else None
        )

        items.append(
            ImageListItem(
                id=image.id or 0,
                file_path=image.file_path,
                original_filename=image.original_filename,
                designer_name=image.designer_name,
                captured_at=image.captured_at,
                created_at=image.created_at,
                ai_metadata=classification,
            )
        )

    return items
