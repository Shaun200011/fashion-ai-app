# Evaluation Summary

- Samples evaluated: 2

## Per-Attribute Accuracy

- `garment_type`: 100.00%
- `style`: 100.00%
- `material`: 0.00%
- `occasion`: 100.00%
- `season`: 50.00%

## Example Predictions

### linen-shirt.jpg
- Expected: `{"garment_type": "top", "style": "contemporary", "material": "linen", "occasion": "daywear", "season": "summer"}`
- Predicted: `{"description": "Placeholder classification for linen shirt. This will be replaced by a multimodal model response.", "garment_type": "top", "style": "contemporary", "material": "unknown", "color_palette": "neutral", "pattern": "solid", "season": "transitional", "occasion": "daywear", "consumer_profile": "fashion-conscious shopper", "trend_notes": "Placeholder metadata pending model integration.", "continent": null, "country": null, "city": null}`

### market-jacket.jpg
- Expected: `{"garment_type": "outerwear", "style": "contemporary", "material": "cotton", "occasion": "daywear", "season": "transitional"}`
- Predicted: `{"description": "Placeholder classification for market jacket. This will be replaced by a multimodal model response.", "garment_type": "outerwear", "style": "contemporary", "material": "unknown", "color_palette": "neutral", "pattern": "solid", "season": "transitional", "occasion": "daywear", "consumer_profile": "fashion-conscious shopper", "trend_notes": "Placeholder metadata pending model integration.", "continent": null, "country": null, "city": null}`

## Notes

- This scaffold currently evaluates the configured classifier, which may still be the mock provider in local development.
- Replace `sample_labels.json` with a 50-100 image labeled set for final submission.