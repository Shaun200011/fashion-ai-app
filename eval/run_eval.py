import json
import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

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


def compute_accuracy(results: List[EvalResult]) -> Dict[str, Dict[str, float]]:
    scores: Dict[str, Dict[str, float]] = {}

    for field in EVAL_FIELDS:
        total = 0
        strict_correct = 0
        semantic_correct = 0
        for result in results:
            if field in result.expected:
                total += 1
                expected = normalize_field_value(field, result.expected.get(field))
                predicted = normalize_field_value(field, _predicted_value_for_field(result.predicted, field))
                if strict_field_values_match(field, expected, predicted):
                    strict_correct += 1
                if semantic_field_values_match(
                    field,
                    result.expected.get(field),
                    _predicted_value_for_field(result.predicted, field),
                ):
                    semantic_correct += 1
        scores[field] = {
            "strict": (strict_correct / total) if total else 0.0,
            "semantic": (semantic_correct / total) if total else 0.0,
        }

    return scores


def build_summary(results: List[EvalResult], scores: Dict[str, Dict[str, float]]) -> str:
    lines = [
        "# Evaluation Summary",
        "",
        f"- Samples evaluated: {len(results)}",
        "",
        "## Per-Attribute Accuracy",
        "",
        "### Strict Normalized Accuracy",
        "",
    ]

    for field, score in scores.items():
        lines.append(f"- `{field}`: {score['strict']:.2%}")

    lines.extend(
        [
            "",
            "### Semantic Relaxed Accuracy",
            "",
        ]
    )

    for field, score in scores.items():
        lines.append(f"- `{field}`: {score['semantic']:.2%}")

    lines.extend(
        [
            "",
            "## Example Predictions",
            "",
        ]
    )

    for result in results[:5]:
        lines.append(f"### {result.filename}")
        normalized_expected = {
            field: normalize_field_value(field, value) for field, value in result.expected.items()
        }
        normalized_predicted = {
            field: normalize_field_value(field, _predicted_value_for_field(result.predicted, field))
            for field in EVAL_FIELDS
        }
        lines.append(f"- Expected: `{json.dumps(result.expected, ensure_ascii=False)}`")
        lines.append(f"- Predicted: `{json.dumps(result.predicted, ensure_ascii=False)}`")
        lines.append(f"- Normalized Expected: `{json.dumps(normalized_expected, ensure_ascii=False)}`")
        lines.append(f"- Normalized Predicted: `{json.dumps(normalized_predicted, ensure_ascii=False)}`")
        semantic_match = {
            field: semantic_field_values_match(
                field,
                result.expected.get(field),
                _predicted_value_for_field(result.predicted, field),
            )
            for field in EVAL_FIELDS
        }
        lines.append(f"- Semantic Match: `{json.dumps(semantic_match, ensure_ascii=False)}`")
        lines.append("")

    lines.extend(
        [
            "## Notes",
            "",
            "- This report evaluates whichever classifier is currently configured via the backend provider settings.",
            "- The benchmark labels are sourced from the curated 100-image evaluation subset in `eval/labels/candidate_labels.json`.",
            "- `Strict normalized` scores compare canonicalized labels conservatively.",
            "- `Semantic relaxed` scores allow taxonomy-aware overlap so natural-language outputs can be matched more fairly against the dataset labels.",
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


def normalize_field_value(field: str, value: Any) -> Optional[str]:
    tokens = _tokenize(value)
    if not tokens:
        return None

    if field == "garment_type":
        return _normalize_garment_type(tokens)
    if field == "occasion":
        return _normalize_occasion(tokens)
    if field == "season":
        return _normalize_season(tokens)
    if field == "style":
        return _normalize_style(tokens)
    if field == "base_colour":
        return _normalize_colour(tokens)

    return tokens[0]


def _predicted_value_for_field(predicted: dict[str, Any], field: str) -> Any:
    if field == "base_colour":
        return predicted.get("base_colour") or predicted.get("color_palette")
    return predicted.get(field)


def strict_field_values_match(field: str, expected: Optional[str], predicted: Optional[str]) -> bool:
    if expected is None or predicted is None:
        return False

    if field == "season":
        expected_set = set(_season_tokens(expected))
        predicted_set = set(_season_tokens(predicted))
        return bool(expected_set & predicted_set)

    if field == "base_colour":
        expected_set = set(_colour_tokens(expected))
        predicted_set = set(_colour_tokens(predicted))
        return bool(expected_set & predicted_set)

    return expected == predicted


def semantic_field_values_match(field: str, expected: Any, predicted: Any) -> bool:
    expected_concepts = semantic_field_concepts(field, expected)
    predicted_concepts = semantic_field_concepts(field, predicted)
    if not expected_concepts or not predicted_concepts:
        return False
    return bool(expected_concepts & predicted_concepts)


def semantic_field_concepts(field: str, value: Any) -> Set[str]:
    tokens = _tokenize(value)
    if not tokens:
        return set()

    if field == "garment_type":
        return set(_garment_type_concepts(tokens))
    if field == "occasion":
        return set(_occasion_concepts(tokens))
    if field == "season":
        return set(_season_concepts(tokens))
    if field == "style":
        return set(_style_concepts(tokens))
    if field == "base_colour":
        return set(_colour_concepts(tokens))

    normalized = normalize_field_value(field, value)
    return {normalized} if normalized else set()


def _tokenize(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        raw_items = value
    else:
        text = str(value).strip()
        if not text:
            return []
        try:
            parsed = ast.literal_eval(text)
            if isinstance(parsed, list):
                raw_items = parsed
            else:
                raw_items = re.split(r"[,/]| and ", text)
        except Exception:
            raw_items = re.split(r"[,/]| and ", text)

    cleaned = []
    for item in raw_items:
        token = str(item).strip().lower()
        if token:
            cleaned.append(token)
    return cleaned


def _normalize_garment_type(tokens: list[str]) -> str:
    concepts = _garment_type_concepts(tokens)
    return concepts[0] if concepts else tokens[0]


def _normalize_occasion(tokens: list[str]) -> str:
    concepts = _occasion_concepts(tokens)
    return concepts[0] if concepts else "casual"


def _occasion_concepts(tokens: list[str]) -> list[str]:
    joined = " ".join(tokens)
    ordered = []
    if any(term in joined for term in ["sport", "gym", "activewear", "athleisure", "workout"]):
        ordered.append("sports")
    if any(term in joined for term in ["ethnic", "festive", "traditional"]):
        ordered.append("ethnic")
    if re.search(r"\b(formal|office|workwear)\b", joined):
        ordered.append("formal")
    if any(term in joined for term in ["party", "evening"]):
        ordered.append("party")
    if any(term in joined for term in ["travel"]):
        ordered.append("travel")
    if any(term in joined for term in ["smart casual"]):
        ordered.append("smart casual")
    if not ordered:
        ordered.append("casual")
    elif "casual" in joined and "casual" not in ordered:
        ordered.append("casual")
    return ordered


def _normalize_season(tokens: list[str]) -> str:
    concepts = _season_concepts(tokens)
    if concepts:
        if "all seasons" in concepts:
            return "all seasons"
        return "/".join(concepts)
    return tokens[0]


def _season_concepts(tokens: list[str]) -> list[str]:
    joined = " ".join(tokens)
    if "all season" in joined or "all seasons" in joined:
        return ["all seasons", "spring", "summer", "fall", "winter"]
    return _season_tokens(joined)


def _normalize_style(tokens: list[str]) -> str:
    concepts = _style_concepts(tokens)
    return concepts[0] if concepts else tokens[0]


def _style_concepts(tokens: list[str]) -> list[str]:
    joined = " ".join(tokens)
    if any(term in joined for term in ["ethnic", "traditional"]):
        return ["ethnic"]
    if any(term in joined for term in ["sport", "athleisure"]):
        return ["sporty"]
    if any(term in joined for term in ["bohemian", "artistic", "minimalist", "casual", "relaxed"]):
        return ["casual"]
    if "contemporary" in joined:
        return ["contemporary"]
    return [tokens[0]]


def _normalize_colour(tokens: list[str]) -> str:
    colour_hits = _colour_concepts(tokens)
    if colour_hits:
        return "/".join(colour_hits)
    return tokens[0]


def _colour_concepts(tokens: list[str]) -> list[str]:
    joined = " ".join(tokens)
    return _colour_tokens(joined)


def _garment_type_concepts(tokens: list[str]) -> list[str]:
    joined = " ".join(tokens)
    ordered = []
    mapping = [
        ("sports bra", "bra"),
        ("bra", "bra"),
        ("camisole", "camisoles"),
        ("tank top", "camisoles"),
        ("spaghetti strap", "camisoles"),
        ("top", "tops"),
        ("t-shirt", "tshirts"),
        ("tee", "tshirts"),
        ("shirt", "shirts"),
        ("jacket", "jackets"),
        ("jean", "jeans"),
        ("trouser", "trousers"),
        ("pants", "trousers"),
        ("pant", "trousers"),
        ("legging", "leggings"),
        ("skirt", "skirts"),
        ("sweater", "sweaters"),
        ("kurti", "kurtis"),
    ]
    for needle, canonical in mapping:
        if needle in joined and canonical not in ordered:
            ordered.append(canonical)
    return ordered or [tokens[0]]


def _season_tokens(text: str) -> list[str]:
    ordered = []
    mapping = [("spring", "spring"), ("summer", "summer"), ("fall", "fall"), ("autumn", "fall"), ("winter", "winter")]
    for needle, canonical in mapping:
        if needle in text and canonical not in ordered:
            ordered.append(canonical)
    return ordered


def _colour_tokens(text: str) -> list[str]:
    normalized = text.lower()
    synonym_rewrites = {
        "grey melange": "grey",
        "heather grey": "grey",
        "heather gray": "grey",
        "light grey": "grey",
        "light gray": "grey",
        "charcoal gray": "charcoal",
        "charcoal grey": "charcoal",
        "off white": "white cream",
        "ivory": "cream",
        "tan": "beige",
        "olive": "green",
        "teal": "blue green",
        "turquoise": "blue",
        "mustard": "yellow",
        "gold": "yellow",
        "burgundy": "maroon",
        "magenta": "pink",
    }
    for source, target in synonym_rewrites.items():
        normalized = normalized.replace(source, target)
    ordered = []
    colour_order = [
        "black",
        "white",
        "navy blue",
        "blue",
        "red",
        "green",
        "yellow",
        "pink",
        "purple",
        "brown",
        "grey",
        "beige",
        "cream",
        "maroon",
        "orange",
        "charcoal",
        "khaki",
    ]
    for colour in colour_order:
        if colour in normalized and colour not in ordered:
            ordered.append(colour)
    return ordered


if __name__ == "__main__":
    main()
