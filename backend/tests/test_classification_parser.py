from app.services.classification_parser import parse_classification_payload


def test_parse_classification_payload_applies_defaults() -> None:
    result = parse_classification_payload(
        {
            "description": "  Soft tailored jacket with a clean front.  ",
            "garment_type": "outerwear",
            "style": "",
            "material": None,
        }
    )

    assert result.description == "Soft tailored jacket with a clean front."
    assert result.garment_type == "outerwear"
    assert result.style == "contemporary"
    assert result.material == "unknown"
    assert result.color_palette == "neutral"


def test_parse_classification_payload_normalizes_empty_description() -> None:
    result = parse_classification_payload({})

    assert result.description == "No description generated."
    assert result.garment_type == "unknown"
