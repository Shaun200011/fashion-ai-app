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


def list_images(session: Session) -> list[ImageListItem]:
    images = session.exec(select(Image).order_by(Image.created_at.desc())).all()
    metadata_rows = session.exec(select(AiMetadata)).all()
    metadata_by_image_id = {
        row.image_id: ClassificationResult(
            description=row.description,
            garment_type=row.garment_type,
            style=row.style,
            material=row.material,
            color_palette=row.color_palette,
            pattern=row.pattern,
            season=row.season,
            occasion=row.occasion,
            consumer_profile=row.consumer_profile,
            trend_notes=row.trend_notes,
            continent=row.continent,
            country=row.country,
            city=row.city,
        )
        for row in metadata_rows
    }

    return [
        ImageListItem(
            id=image.id or 0,
            file_path=image.file_path,
            original_filename=image.original_filename,
            designer_name=image.designer_name,
            captured_at=image.captured_at,
            created_at=image.created_at,
            ai_metadata=metadata_by_image_id.get(image.id or 0),
        )
        for image in images
    ]
