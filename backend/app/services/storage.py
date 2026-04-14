from pathlib import Path
from uuid import uuid4

from fastapi import UploadFile

from app.core.config import settings


def save_upload_file(upload: UploadFile) -> tuple[str, str]:
    target_dir = Path(settings.local_image_dir)
    target_dir.mkdir(parents=True, exist_ok=True)

    suffix = Path(upload.filename or "").suffix.lower() or ".jpg"
    stored_name = f"{uuid4().hex}{suffix}"
    destination = target_dir / stored_name

    with destination.open("wb") as buffer:
        while chunk := upload.file.read(1024 * 1024):
            buffer.write(chunk)

    return str(destination), stored_name
