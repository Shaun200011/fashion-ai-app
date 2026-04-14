# Evaluation

This directory contains the labeled dataset format, evaluation script, and per-attribute accuracy summary output.

## Contents

- `dataset/`: place evaluation images here
- `labels/sample_labels.json`: starter label format
- `labels/candidate_labels.json`: generated candidate label manifest for local images
- `run_eval.py`: runs the configured classifier against the labeled set
- `summary.md`: generated accuracy summary
- `scripts/bootstrap_labels.py`: scans `dataset/` and creates blank label entries
- `scripts/download_commons_fashion.py`: optional helper for downloading a small public-image seed set

## Expected Label Format

```json
[
  {
    "filename": "linen-shirt.jpg",
    "expected": {
      "garment_type": "top",
      "style": "contemporary",
      "material": "linen",
      "occasion": "daywear",
      "season": "summer"
    }
  }
]
```

## Run

From the project root:

```bash
cd /Users/yuxiang/fashion-ai-app/backend
PYTHONPATH=/Users/yuxiang/fashion-ai-app/backend:/Users/yuxiang/fashion-ai-app python ../eval/run_eval.py
```

## Practical Workflow

1. Put your chosen 50-100 evaluation images into `eval/dataset/`
2. Run:

```bash
cd /Users/yuxiang/fashion-ai-app
python eval/scripts/bootstrap_labels.py
```

3. Open `eval/labels/candidate_labels.json` and fill the `expected` fields manually
4. Run the evaluation script to generate `eval/summary.md`
