import json
import time
from pathlib import Path
from typing import Any, Dict, List
from urllib.parse import urlencode
from urllib.request import Request, urlopen


PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATASET_DIR = PROJECT_ROOT / "eval" / "dataset"
LABELS_PATH = PROJECT_ROOT / "eval" / "labels" / "candidate_labels.json"

API_URL = "https://commons.wikimedia.org/w/api.php"
CATEGORIES = [
    "Category:Street fashion",
    "Category:Street Style (fashion)",
    "Category:Fashion streets",
]
TARGET_COUNT = 40
USER_AGENT = "Mozilla/5.0 (compatible; CodexCommonsEvalDownloader/1.0)"
THUMB_WIDTH = 768


def api_get(params: Dict[str, Any]) -> Dict[str, Any]:
    query = urlencode(params)
    request = Request(f"{API_URL}?{query}", headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def get_category_files(category: str, limit: int = 50) -> List[Dict[str, Any]]:
    response = api_get(
        {
            "action": "query",
            "format": "json",
            "list": "categorymembers",
            "cmtitle": category,
            "cmtype": "file",
            "cmlimit": str(limit),
        }
    )
    return response.get("query", {}).get("categorymembers", [])


def get_image_info(title: str) -> Dict[str, Any]:
    response = api_get(
        {
            "action": "query",
            "format": "json",
            "prop": "imageinfo",
            "titles": title,
            "iiprop": "url",
            "iiurlwidth": str(THUMB_WIDTH),
        }
    )
    pages = response.get("query", {}).get("pages", {})
    return next(iter(pages.values()), {})


def download_bytes(url: str) -> bytes:
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=60) as response:
        return response.read()


def sanitize_filename(title: str) -> str:
    raw_name = title.removeprefix("File:")
    safe = raw_name.replace("/", "_")
    return safe


def main() -> None:
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    LABELS_PATH.parent.mkdir(parents=True, exist_ok=True)

    if LABELS_PATH.exists():
        downloaded = json.loads(LABELS_PATH.read_text())
    else:
        downloaded = []

    seen_titles = {item.get("source_page", "").rsplit("/", 1)[-1].replace("_", " ") for item in downloaded}

    for category in CATEGORIES:
        for item in get_category_files(category):
            if len(downloaded) >= TARGET_COUNT:
                break

            title = item.get("title")
            if not title or title in seen_titles:
                continue

            try:
                page = get_image_info(title)
                imageinfo = page.get("imageinfo", [])
                if not imageinfo:
                    continue

                image_url = imageinfo[0].get("thumburl") or imageinfo[0].get("url")
                if not image_url:
                    continue

                filename = sanitize_filename(title)
                file_path = DATASET_DIR / filename
                file_path.write_bytes(download_bytes(image_url))
                downloaded.append(
                    {
                        "filename": filename,
                        "source_page": f"https://commons.wikimedia.org/wiki/{title.replace(' ', '_')}",
                        "image_url": image_url,
                        "expected": {},
                    }
                )
                seen_titles.add(title)
                print(f"downloaded {filename}")
                time.sleep(1.0)
            except Exception as exc:
                print(f"skipped {title}: {exc}")
                time.sleep(1.2)

        if len(downloaded) >= TARGET_COUNT:
            break

    LABELS_PATH.write_text(json.dumps(downloaded, indent=2))
    print(f"saved {len(downloaded)} images to {DATASET_DIR}")
    print(f"wrote label template to {LABELS_PATH}")


if __name__ == "__main__":
    main()
