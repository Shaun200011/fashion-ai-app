from app.services import classifier


def test_classify_image_falls_back_to_mock_when_provider_fails(monkeypatch, tmp_path) -> None:
    image_path = tmp_path / "look.jpg"
    image_path.write_bytes(b"fake-bytes")

    class BrokenProvider:
        def classify(self, *, file_path: str, original_filename: str):
            raise RuntimeError("boom")

    monkeypatch.setattr(classifier, "get_classification_provider", lambda: BrokenProvider())

    result = classifier.classify_image(
        file_path=str(image_path),
        original_filename="linen-shirt.jpg",
    )

    assert result.garment_type == "top"
    assert "Placeholder classification" in result.description
