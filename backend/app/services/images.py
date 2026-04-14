from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import UploadFile
from sqlmodel import Session

from app.db.models import Image
from app.schemas.image import ImageUploadResponse
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

    return ImageUploadResponse(
        id=image.id or 0,
        file_path=image.file_path,
        original_filename=image.original_filename,
        designer_name=image.designer_name,
        captured_at=image.captured_at,
        created_at=image.created_at,
    )
