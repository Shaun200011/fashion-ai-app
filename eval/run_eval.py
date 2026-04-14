import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List

from app.services.classifier import classify_image


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LABELS_PATH = PROJECT_ROOT / "eval" / "labels" / "candidate_labels.json"
DEFAULT_DATASET_DIR = PROJECT_ROOT / "eval" / "dataset"
DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "eval" / "summary.md"

EVAL_FIELDS = [
    "garment_type",
    "style",
    "occasion",
    "season",
    "base_colour",
]


@dataclass
class EvalResult:
    filename: str
    expected: Dict[str, Any]
    predicted: Dict[str, Any]


def load_labels(path: Path) -> List[Dict[str, Any]]:
    return json.loads(path.read_text())


def evaluate(labels_path: Path, dataset_dir: Path) -> List[EvalResult]:
    labels = load_labels(labels_path)
    results: List[EvalResult] = []

    for item in labels:
        filename = item["filename"]
        file_path = dataset_dir / filename
        prediction = classify_image(
            file_path=str(file_path),
            original_filename=filename,
        )
        results.append(
            EvalResult(
                filename=filename,
                expected=item["expected"],
                predicted=prediction.model_dump(),
            )
        )

    return results


def compute_accuracy(results: List[EvalResult]) -> Dict[str, float]:
    scores: Dict[str, float] = {}

    for field in EVAL_FIELDS:
        total = 0
        correct = 0
        for result in results:
            if field in result.expected:
                total += 1
                if result.predicted.get(field) == result.expected[field]:
                    correct += 1
        scores[field] = (correct / total) if total else 0.0

    return scores


def build_summary(results: List[EvalResult], scores: Dict[str, float]) -> str:
    lines = [
        "# Evaluation Summary",
        "",
        f"- Samples evaluated: {len(results)}",
        "",
        "## Per-Attribute Accuracy",
        "",
    ]

    for field, score in scores.items():
        lines.append(f"- `{field}`: {score:.2%}")

    lines.extend(
        [
            "",
            "## Example Predictions",
            "",
        ]
    )

    for result in results[:5]:
        lines.append(f"### {result.filename}")
        lines.append(f"- Expected: `{json.dumps(result.expected, ensure_ascii=False)}`")
        lines.append(f"- Predicted: `{json.dumps(result.predicted, ensure_ascii=False)}`")
        lines.append("")

    lines.extend(
        [
            "## Notes",
            "",
            "- This scaffold currently evaluates the configured classifier, which may still be the mock provider in local development.",
            "- Replace `sample_labels.json` with a 50-100 image labeled set for final submission.",
        ]
    )

    return "\n".join(lines)


def main() -> None:
    labels_path = DEFAULT_LABELS_PATH
    dataset_dir = DEFAULT_DATASET_DIR
    output_path = DEFAULT_OUTPUT_PATH

    results = evaluate(labels_path=labels_path, dataset_dir=dataset_dir)
    scores = compute_accuracy(results)
    summary = build_summary(results, scores)
    output_path.write_text(summary)
    print(summary)


if __name__ == "__main__":
    main()
