import json
import re
import time
from pathlib import Path
from typing import Iterable, Optional
from urllib.parse import urljoin
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = PROJECT_ROOT / "eval" / "dataset"
LABELS_PATH = PROJECT_ROOT / "eval" / "labels" / "candidate_labels.json"

SEARCH_PATHS = [
    "https://www.pexels.com/search/fashion/",
    "https://www.pexels.com/search/street%20style/",
    "https://www.pexels.com/search/garment/",
]

PAGE_LIMIT = 3
TARGET_COUNT = 36
USER_AGENT = "Mozilla/5.0 (compatible; CodexEvalDownloader/1.0)"


def fetch_text(url: str) -> str:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return response.read().decode("utf-8", errors="ignore")


def fetch_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:
        return response.read()


def iter_photo_pages(search_url: str) -> Iterable[str]:
    for page in range(1, PAGE_LIMIT + 1):
        url = f"{search_url}?page={page}"
        html = fetch_text(url)
        matches = re.findall(r'href="(/photo/[^"]+/)"', html)
        seen = set()
        for match in matches:
            full_url = urljoin("https://www.pexels.com", match)
            if full_url not in seen:
                seen.add(full_url)
                yield full_url


def parse_image_url(photo_html: str) -> Optional[str]:
    og_match = re.search(r'<meta property="og:image" content="([^"]+)"', photo_html)
    if og_match:
        return og_match.group(1)
    return None


def main() -> None:
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    LABELS_PATH.parent.mkdir(parents=True, exist_ok=True)

    downloaded = []
    seen_images = set()

    for search_url in SEARCH_PATHS:
        for photo_page in iter_photo_pages(search_url):
            if len(downloaded) >= TARGET_COUNT:
                break

            try:
                photo_html = fetch_text(photo_page)
                image_url = parse_image_url(photo_html)
                if not image_url or image_url in seen_images:
                    continue

                seen_images.add(image_url)
                image_bytes = fetch_bytes(image_url)
                photo_id = photo_page.rstrip("/").split("-")[-1]
                suffix = ".jpg"
                filename = f"pexels-fashion-{photo_id}{suffix}"
                file_path = DATASET_DIR / filename
                file_path.write_bytes(image_bytes)
                downloaded.append(
                    {
                        "filename": filename,
                        "source_page": photo_page,
                        "image_url": image_url,
                        "expected": {},
                    }
                )
                print(f"downloaded {filename}")
                time.sleep(0.2)
            except Exception as exc:
                print(f"skipped {photo_page}: {exc}")

        if len(downloaded) >= TARGET_COUNT:
            break

    LABELS_PATH.write_text(json.dumps(downloaded, indent=2))
    print(f"saved {len(downloaded)} images to {DATASET_DIR}")
    print(f"wrote label template to {LABELS_PATH}")


if __name__ == "__main__":
    main()
