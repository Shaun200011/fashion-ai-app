import json
from pathlib import Path
from typing import Dict, List


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = PROJECT_ROOT / "eval" / "dataset"
LABELS_PATH = PROJECT_ROOT / "eval" / "labels" / "candidate_labels.json"

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}


def load_existing() -> List[Dict]:
    if LABELS_PATH.exists():
        return json.loads(LABELS_PATH.read_text())
    return []


def main() -> None:
    existing = load_existing()
    by_filename = {item["filename"]: item for item in existing}

    for file_path in sorted(DATASET_DIR.iterdir()):
        if file_path.suffix.lower() not in IMAGE_EXTENSIONS:
            continue

        if file_path.name not in by_filename:
            by_filename[file_path.name] = {
                "filename": file_path.name,
                "source_page": "",
                "image_url": "",
                "expected": {},
            }

    merged = [by_filename[name] for name in sorted(by_filename.keys())]
    LABELS_PATH.write_text(json.dumps(merged, indent=2))
    print(f"wrote {len(merged)} label entries to {LABELS_PATH}")


if __name__ == "__main__":
    main()
