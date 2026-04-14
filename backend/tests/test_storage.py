from io import BytesIO

from fastapi import UploadFile

from app.core.config import settings
from app.services.storage import save_upload_file


def test_save_upload_file_persists_bytes(tmp_path) -> None:
    original_dir = settings.local_image_dir
    settings.local_image_dir = str(tmp_path)

    try:
        upload = UploadFile(filename="look.jpg", file=BytesIO(b"fake-image-bytes"))

        file_path, stored_name = save_upload_file(upload)

        assert stored_name.endswith(".jpg")
        assert tmp_path.joinpath(stored_name).exists()
        assert tmp_path.joinpath(stored_name).read_bytes() == b"fake-image-bytes"
        assert file_path.endswith(stored_name)
    finally:
        settings.local_image_dir = original_dir
