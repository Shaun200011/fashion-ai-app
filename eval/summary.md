# Evaluation Summary

- Samples evaluated: 100

## Per-Attribute Accuracy

- `garment_type`: 0.00%
- `style`: 3.12%
- `occasion`: 0.00%
- `season`: 0.00%
- `base_colour`: 0.00%

## Example Predictions

### 5792.jpg
- Expected: `{"garment_type": "Tops", "season": "spring", "occasion": "casual", "base_colour": "white", "style": "casual"}`
- Predicted: `{"description": "Placeholder classification for 5792. This will be replaced by a multimodal model response.", "garment_type": "dress", "style": "contemporary", "material": "unknown", "color_palette": "neutral", "pattern": "solid", "season": "transitional", "occasion": "daywear", "consumer_profile": "fashion-conscious shopper", "trend_notes": "Placeholder metadata pending model integration.", "continent": null, "country": null, "city": null}`

### 27434.jpg
- Expected: `{"garment_type": "Bra", "season": "fall", "occasion": "sports", "base_colour": "black"}`
- Predicted: `{"description": "Placeholder classification for 27434. This will be replaced by a multimodal model response.", "garment_type": "dress", "style": "contemporary", "material": "unknown", "color_palette": "neutral", "pattern": "solid", "season": "transitional", "occasion": "daywear", "consumer_profile": "fashion-conscious shopper", "trend_notes": "Placeholder metadata pending model integration.", "continent": null, "country": null, "city": null}`

### 30917.jpg
- Expected: `{"garment_type": "Trousers", "season": "summer", "occasion": "ethnic", "base_colour": "black"}`
- Predicted: `{"description": "Placeholder classification for 30917. This will be replaced by a multimodal model response.", "garment_type": "dress", "style": "contemporary", "material": "unknown", "color_palette": "neutral", "pattern": "solid", "season": "transitional", "occasion": "daywear", "consumer_profile": "fashion-conscious shopper", "trend_notes": "Placeholder metadata pending model integration.", "continent": null, "country": null, "city": null}`

### 27433.jpg
- Expected: `{"garment_type": "Bra", "season": "winter", "occasion": "sports", "base_colour": "grey melange"}`
- Predicted: `{"description": "Placeholder classification for 27433. This will be replaced by a multimodal model response.", "garment_type": "dress", "style": "contemporary", "material": "unknown", "color_palette": "neutral", "pattern": "solid", "season": "transitional", "occasion": "daywear", "consumer_profile": "fashion-conscious shopper", "trend_notes": "Placeholder metadata pending model integration.", "continent": null, "country": null, "city": null}`

### 25895.jpg
- Expected: `{"garment_type": "Camisoles", "season": "summer", "occasion": "casual", "base_colour": "white"}`
- Predicted: `{"description": "Placeholder classification for 25895. This will be replaced by a multimodal model response.", "garment_type": "dress", "style": "contemporary", "material": "unknown", "color_palette": "neutral", "pattern": "solid", "season": "transitional", "occasion": "daywear", "consumer_profile": "fashion-conscious shopper", "trend_notes": "Placeholder metadata pending model integration.", "continent": null, "country": null, "city": null}`

## Notes

- This scaffold currently evaluates the configured classifier, which may still be the mock provider in local development.
- Replace `sample_labels.json` with a 50-100 image labeled set for final submission.