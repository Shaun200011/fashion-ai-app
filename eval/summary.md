# Evaluation Summary

- Samples evaluated: 100

## Per-Attribute Accuracy

### Strict Normalized Accuracy

- `garment_type`: 43.00%
- `style`: 78.12%
- `occasion`: 56.00%
- `season`: 48.00%
- `base_colour`: 87.00%

### Semantic Relaxed Accuracy

- `garment_type`: 52.00%
- `style`: 78.12%
- `occasion`: 74.00%
- `season`: 54.00%
- `base_colour`: 87.00%

## Example Predictions

### 5792.jpg
- Expected: `{"garment_type": "Tops", "season": "spring", "occasion": "casual", "base_colour": "white", "style": "casual"}`
- Predicted: `{"description": "A vibrant, short-sleeved V-neck top featuring a patchwork of colorful and artistic prints including floral motifs and an artistic face illustration.", "garment_type": "Top", "style": "Casual, Artistic, Bohemian", "material": "Cotton or cotton blend", "color_palette": "['blue', 'orange', 'red', 'green', 'white', 'yellow', 'black']", "pattern": "Mixed prints including floral, abstract, and artistic face illustration", "season": "Spring/Summer", "occasion": "Casual outings, Everyday wear", "consumer_profile": "Young adults and artistic individuals who enjoy bold and unique fashion statements", "trend_notes": "Eclectic mix of prints and vibrant colors with a bohemian, artistic vibe.", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "tops", "season": "spring", "occasion": "casual", "base_colour": "white", "style": "casual"}`
- Normalized Predicted: `{"garment_type": "tops", "style": "casual", "occasion": "casual", "season": "spring/summer", "base_colour": "black/white/blue/red/green/yellow/orange"}`
- Semantic Match: `{"garment_type": true, "style": true, "occasion": true, "season": true, "base_colour": true}`

### 27434.jpg
- Expected: `{"garment_type": "Bra", "season": "fall", "occasion": "sports", "base_colour": "black"}`
- Predicted: `{"description": "A simple and functional black sports bra with a scoop neckline and wide straps. It provides medium support and has a smooth finish with a small brand label on the band.", "garment_type": "sports bra", "style": "athleisure, minimalistic", "material": "likely cotton or a cotton blend with elastane for flexibility", "color_palette": "black", "pattern": "solid", "season": "all seasons", "occasion": "casual, sports, workout", "consumer_profile": "active individuals looking for comfortable, supportive undergarments", "trend_notes": "Focus on comfort and functionality in activewear, minimal branding, and versatile basic colors.", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "bra", "season": "fall", "occasion": "sports", "base_colour": "black"}`
- Normalized Predicted: `{"garment_type": "bra", "style": "sporty", "occasion": "sports", "season": "all seasons", "base_colour": "black"}`
- Semantic Match: `{"garment_type": true, "style": false, "occasion": true, "season": true, "base_colour": true}`

### 30917.jpg
- Expected: `{"garment_type": "Trousers", "season": "summer", "occasion": "ethnic", "base_colour": "black"}`
- Predicted: `{"description": "Loose-fitting, crinkled black pants with an elastic waistband and drawstring, featuring gathered cuffs at the ankles. Paired with casual flat sandals.", "garment_type": "pants", "style": "casual, bohemian", "material": "lightweight, crinkled fabric (likely cotton or a cotton blend)", "color_palette": "black", "pattern": "solid", "season": "spring/summer", "occasion": "casual/outdoor wear", "consumer_profile": "person seeking comfort and relaxed fit, possibly interested in bohemian or laid-back style", "trend_notes": "comfort-focused fashion with breathable fabrics and loose silhouettes", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "trousers", "season": "summer", "occasion": "ethnic", "base_colour": "black"}`
- Normalized Predicted: `{"garment_type": "trousers", "style": "casual", "occasion": "casual", "season": "spring/summer", "base_colour": "black"}`
- Semantic Match: `{"garment_type": true, "style": false, "occasion": false, "season": true, "base_colour": true}`

### 27433.jpg
- Expected: `{"garment_type": "Bra", "season": "winter", "occasion": "sports", "base_colour": "grey melange"}`
- Predicted: `{"description": "A simple, sporty bra featuring a scoop neckline and wide straps, designed for comfort and light support.", "garment_type": "bra", "style": "sportswear", "material": "cotton blend", "color_palette": "['grey', 'black']", "pattern": "solid", "season": "all seasons", "occasion": "casual, athletic, everyday wear", "consumer_profile": "active women, comfort-focused, sporty lifestyle", "trend_notes": "Minimalistic design with color-blocking contrast trim.", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "bra", "season": "winter", "occasion": "sports", "base_colour": "grey"}`
- Normalized Predicted: `{"garment_type": "bra", "style": "sporty", "occasion": "casual", "season": "all seasons", "base_colour": "black/grey"}`
- Semantic Match: `{"garment_type": true, "style": false, "occasion": false, "season": true, "base_colour": true}`

### 25895.jpg
- Expected: `{"garment_type": "Camisoles", "season": "summer", "occasion": "casual", "base_colour": "white"}`
- Predicted: `{"description": "A casual and simple outfit featuring a fitted white spaghetti strap tank top paired with dark denim rolled-up shorts and a brown leather belt.", "garment_type": "tank top and denim shorts", "style": "casual, minimalist", "material": "cotton (tank top), denim (shorts), leather (belt)", "color_palette": "white, dark blue, brown", "pattern": "solid colors", "season": "summer", "occasion": "casual day out, informal gatherings", "consumer_profile": "young adults, trend-conscious individuals seeking comfort and simplicity", "trend_notes": "Classic summer casual wear with emphasis on comfort and minimalism. Denim shorts with a basic tank top remain timeless and versatile.", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "camisoles", "season": "summer", "occasion": "casual", "base_colour": "white"}`
- Normalized Predicted: `{"garment_type": "camisoles", "style": "casual", "occasion": "casual", "season": "summer", "base_colour": "white/blue/brown"}`
- Semantic Match: `{"garment_type": true, "style": false, "occasion": true, "season": true, "base_colour": true}`

## Notes

- This report evaluates whichever classifier is currently configured via the backend provider settings.
- The benchmark labels are sourced from the curated 100-image evaluation subset in `eval/labels/candidate_labels.json`.
- `Strict normalized` scores compare canonicalized labels conservatively.
- `Semantic relaxed` scores allow taxonomy-aware overlap so natural-language outputs can be matched more fairly against the dataset labels.