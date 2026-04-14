from io import BytesIO

from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import app


client = TestClient(app)


def test_upload_image_returns_classification(tmp_path) -> None:
    original_dir = settings.local_image_dir
    original_sqlite_url = settings.sqlite_url
    settings.local_image_dir = str(tmp_path / "images")
    settings.sqlite_url = f"sqlite:///{tmp_path}/test.db"

    try:
        files = {"file": ("linen-shirt.jpg", BytesIO(b"img-bytes"), "image/jpeg")}
        data = {"designer_name": "Alex"}

        response = client.post("/api/images/upload", files=files, data=data)

        assert response.status_code == 200
        payload = response.json()
        assert payload["original_filename"] == "linen-shirt.jpg"
        assert payload["designer_name"] == "Alex"
        assert payload["ai_metadata"]["garment_type"] == "top"
        assert payload["ai_metadata"]["style"] == "contemporary"
    finally:
        settings.local_image_dir = original_dir
        settings.sqlite_url = original_sqlite_url


def test_list_images_includes_saved_metadata(tmp_path) -> None:
    original_dir = settings.local_image_dir
    original_sqlite_url = settings.sqlite_url
    settings.local_image_dir = str(tmp_path / "images")
    settings.sqlite_url = f"sqlite:///{tmp_path}/test.db"

    try:
        files = {"file": ("market-jacket.jpg", BytesIO(b"img-bytes"), "image/jpeg")}
        client.post("/api/images/upload", files=files)

        response = client.get("/api/images")

        assert response.status_code == 200
        payload = response.json()
        assert len(payload) == 1
        assert payload[0]["original_filename"] == "market-jacket.jpg"
        assert payload[0]["ai_metadata"]["garment_type"] == "outerwear"
    finally:
        settings.local_image_dir = original_dir
        settings.sqlite_url = original_sqlite_url


def test_image_search_and_filters_return_matching_items(tmp_path) -> None:
    original_dir = settings.local_image_dir
    original_sqlite_url = settings.sqlite_url
    settings.local_image_dir = str(tmp_path / "images")
    settings.sqlite_url = f"sqlite:///{tmp_path}/test.db"

    try:
        client.post(
            "/api/images/upload",
            files={"file": ("linen-shirt.jpg", BytesIO(b"img-bytes"), "image/jpeg")},
            data={"designer_name": "Alex"},
        )
        client.post(
            "/api/images/upload",
            files={"file": ("market-jacket.jpg", BytesIO(b"img-bytes"), "image/jpeg")},
            data={"designer_name": "Jordan"},
        )

        search_response = client.get("/api/images", params={"query": "linen"})
        filter_response = client.get("/api/images", params={"garment_type": "outerwear"})
        filters_response = client.get("/api/filters")

        assert search_response.status_code == 200
        assert len(search_response.json()) == 1
        assert search_response.json()[0]["original_filename"] == "linen-shirt.jpg"

        assert filter_response.status_code == 200
        assert len(filter_response.json()) == 1
        assert filter_response.json()[0]["original_filename"] == "market-jacket.jpg"

        assert filters_response.status_code == 200
        payload = filters_response.json()
        garment_group = next(group for group in payload if group["key"] == "garment_type")
        option_values = {option["value"] for option in garment_group["options"]}
        assert {"top", "outerwear"}.issubset(option_values)
    finally:
        settings.local_image_dir = original_dir
        settings.sqlite_url = original_sqlite_url
