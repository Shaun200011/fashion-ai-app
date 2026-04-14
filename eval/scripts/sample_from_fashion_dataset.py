import csv
import json
import random
import shutil
from collections import defaultdict
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
TARGET_DATASET_DIR = PROJECT_ROOT / "eval" / "dataset"
TARGET_LABELS_PATH = PROJECT_ROOT / "eval" / "labels" / "candidate_labels.json"

SOURCE_ROOT = Path("/Users/yuxiang/Desktop/fashion-dataset")
SOURCE_IMAGES_DIR = SOURCE_ROOT / "images"
SOURCE_STYLES_CSV = SOURCE_ROOT / "styles.csv"

TARGET_COUNT = 100
RANDOM_SEED = 7

STYLE_HINTS = {
    "Kurtas": "ethnic",
    "Kurtis": "ethnic",
    "Sarees": "ethnic",
    "Tshirts": "casual",
    "Shirts": "casual",
    "Jeans": "casual",
    "Track Pants": "sporty",
    "Sports Shoes": "sporty",
    "Casual Shoes": "casual",
    "Tops": "casual",
    "Dresses": "contemporary",
}


def map_row_to_expected(row: dict[str, str]) -> dict[str, str]:
    expected: dict[str, str] = {}

    article_type = row.get("articleType", "").strip()
    season = row.get("season", "").strip()
    usage = row.get("usage", "").strip()
    base_colour = row.get("baseColour", "").strip()

    if article_type:
        expected["garment_type"] = article_type
    if season:
        expected["season"] = season.lower()
    if usage and usage != "NA":
        expected["occasion"] = usage.lower()
    if base_colour:
        expected["base_colour"] = base_colour.lower()
    if article_type in STYLE_HINTS:
        expected["style"] = STYLE_HINTS[article_type]

    return expected


def is_usable_row(row: dict[str, str]) -> bool:
    article_type = row.get("articleType", "").strip()
    usage = row.get("usage", "").strip()
    season = row.get("season", "").strip()
    master_category = row.get("masterCategory", "").strip()

    return bool(
        article_type
        and usage
        and usage != "NA"
        and season
        and master_category == "Apparel"
        and (SOURCE_IMAGES_DIR / f"{row['id']}.jpg").exists()
    )


def sample_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rng = random.Random(RANDOM_SEED)
    buckets: dict[tuple[str, str, str], list[dict[str, str]]] = defaultdict(list)

    for row in rows:
        key = (
            row.get("articleType", "").strip(),
            row.get("usage", "").strip(),
            row.get("season", "").strip(),
        )
        buckets[key].append(row)

    sampled: list[dict[str, str]] = []
    bucket_keys = list(buckets.keys())
    rng.shuffle(bucket_keys)

    while len(sampled) < TARGET_COUNT and bucket_keys:
        next_round = []
        for key in bucket_keys:
            bucket = buckets[key]
            if not bucket:
                continue
            sampled.append(bucket.pop(rng.randrange(len(bucket))))
            if len(sampled) >= TARGET_COUNT:
                break
            if bucket:
                next_round.append(key)
        bucket_keys = next_round

    return sampled


def main() -> None:
    TARGET_DATASET_DIR.mkdir(parents=True, exist_ok=True)
    TARGET_LABELS_PATH.parent.mkdir(parents=True, exist_ok=True)

    with SOURCE_STYLES_CSV.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = [row for row in reader if is_usable_row(row)]

    existing_labels = []
    existing_ids = set()
    if TARGET_LABELS_PATH.exists():
        existing_labels = json.loads(TARGET_LABELS_PATH.read_text())
        existing_ids = {item.get("source_id") for item in existing_labels if item.get("source_id")}

    remaining_rows = [row for row in rows if row["id"] not in existing_ids]
    sampled_rows = sample_rows(remaining_rows)
    needed = max(TARGET_COUNT - len(existing_labels), 0)
    sampled_rows = sampled_rows[:needed]

    labels = list(existing_labels)
    for row in sampled_rows:
        source_image = SOURCE_IMAGES_DIR / f"{row['id']}.jpg"
        target_name = f"{row['id']}.jpg"
        target_image = TARGET_DATASET_DIR / target_name
        shutil.copy2(source_image, target_image)

        labels.append(
            {
                "filename": target_name,
                "source_id": row["id"],
                "source_page": "",
                "image_url": "",
                "expected": map_row_to_expected(row),
                "source_metadata": {
                    "gender": row.get("gender", ""),
                    "masterCategory": row.get("masterCategory", ""),
                    "subCategory": row.get("subCategory", ""),
                    "articleType": row.get("articleType", ""),
                    "baseColour": row.get("baseColour", ""),
                    "season": row.get("season", ""),
                    "usage": row.get("usage", ""),
                    "productDisplayName": row.get("productDisplayName", ""),
                },
            }
        )

    TARGET_LABELS_PATH.write_text(json.dumps(labels, indent=2, ensure_ascii=False))
    print(f"sampled {len(labels)} images into {TARGET_DATASET_DIR}")
    print(f"wrote labels to {TARGET_LABELS_PATH}")


if __name__ == "__main__":
    main()
