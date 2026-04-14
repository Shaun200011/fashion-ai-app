import json
from pathlib import Path

from sqlmodel import select

from app.db.models import AiMetadata, Image
from app.db.session import get_engine, init_db


PROJECT_ROOT = Path(__file__).resolve().parents[2]
LABELS_PATH = PROJECT_ROOT / "eval" / "labels" / "candidate_labels.json"
IMAGE_DIR = PROJECT_ROOT / "backend" / "data" / "images"

DEMO_FILES = [
    "5792.jpg",
    "19855.jpg",
    "14539.jpg",
    "19167.jpg",
    "20225.jpg",
    "26133.jpg",
    "15039.jpg",
    "41349.jpg",
]


def main() -> None:
    init_db()
    labels = {item["filename"]: item for item in json.loads(LABELS_PATH.read_text())}

    engine = get_engine()
    from sqlmodel import Session

    with Session(engine) as session:
        for filename in DEMO_FILES:
            file_path = IMAGE_DIR / filename
            if not file_path.exists():
                continue

            existing = session.exec(select(Image).where(Image.original_filename == filename)).first()
            if existing:
                continue

            label = labels.get(filename, {})
            metadata = label.get("expected", {})
            image = Image(
                file_path=str(file_path),
                original_filename=filename,
                designer_name="Demo Library",
            )
            session.add(image)
            session.commit()
            session.refresh(image)

            session.add(
                AiMetadata(
                    image_id=image.id or 0,
                    description=label.get("source_metadata", {}).get(
                        "productDisplayName",
                        f"Imported demo image {filename}",
                    ),
                    garment_type=metadata.get("garment_type"),
                    style=metadata.get("style"),
                    material=None,
                    color_palette=metadata.get("base_colour"),
                    pattern=None,
                    season=metadata.get("season"),
                    occasion=metadata.get("occasion"),
                    consumer_profile=None,
                    trend_notes="Imported from the evaluation sample set for demo presentation.",
                    continent=None,
                    country=None,
                    city=None,
                    raw_model_output=json.dumps(metadata),
                )
            )
            session.commit()

    print(f"imported {len(DEMO_FILES)} demo images")


if __name__ == "__main__":
    main()
