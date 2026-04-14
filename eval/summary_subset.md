# Evaluation Summary

- Samples evaluated: 10

## Per-Attribute Accuracy

### Strict Normalized Accuracy

- `garment_type`: 90.00%
- `style`: 100.00%
- `occasion`: 70.00%
- `season`: 30.00%
- `base_colour`: 80.00%

### Semantic Relaxed Accuracy

- `garment_type`: 100.00%
- `style`: 100.00%
- `occasion`: 70.00%
- `season`: 60.00%
- `base_colour`: 80.00%

## Example Predictions

### 5792.jpg
- Expected: `{"garment_type": "Tops", "season": "spring", "occasion": "casual", "base_colour": "white", "style": "casual"}`
- Predicted: `{"description": "A vibrant, multi-patterned short-sleeve V-neck top featuring a patchwork design with floral motifs and an artistic portrait, paired with light-colored pants.", "garment_type": "Top / T-shirt", "style": "Casual, Artistic, Bohemian", "material": "Cotton or Cotton Blend (assumed from appearance)", "color_palette": "Bright and varied including blues, reds, greens, oranges, yellows, and blacks", "pattern": "Patchwork with floral prints and an illustrative portrait", "season": "Spring/Summer", "occasion": "Casual, Daywear", "consumer_profile": "Young adult women interested in colorful, artistic, and casual fashion", "trend_notes": "Patchwork and mixed prints with cultural/ethnic elements; emphasis on artistry and bold colors", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "tops", "season": "spring", "occasion": "casual", "base_colour": "white", "style": "casual"}`
- Normalized Predicted: `{"garment_type": "tops", "style": "casual", "occasion": "casual", "season": "spring/summer", "base_colour": "black/blue/red/green/yellow/orange"}`
- Semantic Match: `{"garment_type": true, "style": true, "occasion": true, "season": true, "base_colour": false}`

### 27434.jpg
- Expected: `{"garment_type": "Bra", "season": "fall", "occasion": "sports", "base_colour": "black"}`
- Predicted: `{"description": "A black sports bra with a scoop neckline, wide shoulder straps, and a supportive band underneath the bust. It features minimalist design with subtle stitching details and a small brand label at the center front.", "garment_type": "sports bra", "style": "athleisure, minimalist", "material": "likely cotton or a cotton blend with elastane for stretch", "color_palette": "['black']", "pattern": "solid", "season": "all seasons", "occasion": "sports, fitness, casual wear", "consumer_profile": "active individuals who prefer comfort and minimalistic athletic wear", "trend_notes": "sustainable materials and comfort-focused activewear continue to grow in popularity, with minimalist design elements", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "bra", "season": "fall", "occasion": "sports", "base_colour": "black"}`
- Normalized Predicted: `{"garment_type": "bra", "style": "sporty", "occasion": "sports", "season": "all seasons", "base_colour": "black"}`
- Semantic Match: `{"garment_type": true, "style": false, "occasion": true, "season": true, "base_colour": true}`

### 30917.jpg
- Expected: `{"garment_type": "Trousers", "season": "summer", "occasion": "ethnic", "base_colour": "black"}`
- Predicted: `{"description": "Loose-fitting, high-waisted pants with an elastic waistband and drawstring. The pants taper at the ankle with gathered cuffs.", "garment_type": "pants", "style": "casual, relaxed, bohemian", "material": "lightweight fabric, likely cotton or a cotton blend", "color_palette": "['black']", "pattern": "solid", "season": "spring, summer", "occasion": "casual, everyday wear", "consumer_profile": "comfort-seeking, casual dressers, possibly younger adults or those valuing relaxed fits", "trend_notes": "Focus on comfort, loose silhouettes, and breathable fabrics. Aligns with increasing demand for relaxed, versatile clothing.", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "trousers", "season": "summer", "occasion": "ethnic", "base_colour": "black"}`
- Normalized Predicted: `{"garment_type": "trousers", "style": "casual", "occasion": "casual", "season": "spring/summer", "base_colour": "black"}`
- Semantic Match: `{"garment_type": true, "style": false, "occasion": false, "season": true, "base_colour": true}`

### 27433.jpg
- Expected: `{"garment_type": "Bra", "season": "winter", "occasion": "sports", "base_colour": "grey melange"}`
- Predicted: `{"description": "A seamless, sports bra featuring a scoop neckline and wide straps with a contrasting color trim.", "garment_type": "sports bra", "style": "athleisure, casual", "material": "cotton blend with stretch fabric", "color_palette": "['grey', 'black']", "pattern": "solid color with contrast trim", "season": "all seasons", "occasion": "workout, casual wear", "consumer_profile": "active individuals looking for comfort and support", "trend_notes": "Minimalistic athleisure is popular, focusing on comfort and versatile styling.", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "bra", "season": "winter", "occasion": "sports", "base_colour": "grey"}`
- Normalized Predicted: `{"garment_type": "bra", "style": "sporty", "occasion": "sports", "season": "all seasons", "base_colour": "black/grey"}`
- Semantic Match: `{"garment_type": true, "style": false, "occasion": true, "season": true, "base_colour": true}`

### 25895.jpg
- Expected: `{"garment_type": "Camisoles", "season": "summer", "occasion": "casual", "base_colour": "white"}`
- Predicted: `{"description": "Casual summer outfit featuring a white spaghetti strap tank top paired with rolled-up dark denim shorts and a brown leather belt.", "garment_type": "Tank top and denim shorts", "style": "Casual, summer", "material": "Cotton (tank top), denim (shorts), leather (belt)", "color_palette": "White, dark blue, brown", "pattern": "Solid colors", "season": "Summer", "occasion": "Casual daywear", "consumer_profile": "Young adult female, relaxed style, warm weather", "trend_notes": "Minimalist, comfortable, and versatile summer staple", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "camisoles", "season": "summer", "occasion": "casual", "base_colour": "white"}`
- Normalized Predicted: `{"garment_type": "camisoles", "style": "casual", "occasion": "casual", "season": "summer", "base_colour": "white/blue/brown"}`
- Semantic Match: `{"garment_type": true, "style": false, "occasion": true, "season": true, "base_colour": true}`

## Notes

- This report evaluates whichever classifier is currently configured via the backend provider settings.
- The benchmark labels are sourced from the curated 100-image evaluation subset in `eval/labels/candidate_labels.json`.
- `Strict normalized` scores compare canonicalized labels conservatively.
- `Semantic relaxed` scores allow taxonomy-aware overlap so natural-language outputs can be matched more fairly against the dataset labels.