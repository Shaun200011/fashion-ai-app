import json
import sys
from pathlib import Path

from run_eval import build_summary, compute_accuracy, evaluate


PROJECT_ROOT = Path(__file__).resolve().parents[1]
LABELS_PATH = PROJECT_ROOT / "eval" / "labels" / "candidate_labels.json"
DATASET_DIR = PROJECT_ROOT / "eval" / "dataset"
OUTPUT_PATH = PROJECT_ROOT / "eval" / "summary_subset.md"
SUBSET_SIZE = 10


def main() -> None:
    subset_size = int(sys.argv[1]) if len(sys.argv) > 1 else SUBSET_SIZE
    output_path = (
        PROJECT_ROOT / "eval" / f"summary_subset_{subset_size}.md"
        if subset_size != SUBSET_SIZE
        else OUTPUT_PATH
    )

    labels = json.loads(LABELS_PATH.read_text())
    subset_path = PROJECT_ROOT / "eval" / "labels" / f"candidate_labels_subset_{subset_size}.json"
    subset_path.write_text(json.dumps(labels[:subset_size], indent=2, ensure_ascii=False))

    results = evaluate(labels_path=subset_path, dataset_dir=DATASET_DIR)
    scores = compute_accuracy(results)
    summary = build_summary(results, scores)
    output_path.write_text(summary)
    print(summary)


if __name__ == "__main__":
    main()
