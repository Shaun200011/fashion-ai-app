# Evaluation Summary

- Samples evaluated: 50

## Per-Attribute Accuracy

### Strict Normalized Accuracy

- `garment_type`: 42.00%
- `style`: 70.59%
- `occasion`: 66.00%
- `season`: 50.00%
- `base_colour`: 82.00%

### Semantic Relaxed Accuracy

- `garment_type`: 56.00%
- `style`: 70.59%
- `occasion`: 80.00%
- `season`: 58.00%
- `base_colour`: 82.00%

## Example Predictions

### 5792.jpg
- Expected: `{"garment_type": "Tops", "season": "spring", "occasion": "casual", "base_colour": "white", "style": "casual"}`
- Predicted: `{"description": "A vibrant V-neck T-shirt featuring a collage of various artistic floral and graphic prints, including an Asian-inspired image, combined with mint green pants.", "garment_type": "T-shirt", "style": "Casual, artistic, eclectic", "material": "Likely cotton or cotton blend", "color_palette": "Bright and varied colors including blue, orange, red, green, yellow, white", "pattern": "Mixed graphic and floral prints with a patchwork effect", "season": "Spring/Summer", "occasion": "Casual wear, day outings, artistic events", "consumer_profile": "Young adults or adults with an interest in unique, colorful, and artistic fashion", "trend_notes": "Patchwork and mixed prints with cultural graphic influences", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "tops", "season": "spring", "occasion": "casual", "base_colour": "white", "style": "casual"}`
- Normalized Predicted: `{"garment_type": "tshirts", "style": "casual", "occasion": "casual", "season": "spring/summer", "base_colour": "white/blue/red/green/yellow/orange"}`
- Semantic Match: `{"garment_type": false, "style": true, "occasion": true, "season": true, "base_colour": true}`

### 27434.jpg
- Expected: `{"garment_type": "Bra", "season": "fall", "occasion": "sports", "base_colour": "black"}`
- Predicted: `{"description": "A simple, black sports bra with a scoop neckline and wide straps, designed for comfort and support during physical activities.", "garment_type": "Sports bra", "style": "Athleisure / Casual", "material": "Cotton blend or synthetic stretch fabric", "color_palette": "['Black']", "pattern": "Solid", "season": "All seasons", "occasion": "Sports, gym, casual wear", "consumer_profile": "Active individuals, fitness enthusiasts, women seeking comfortable everyday support", "trend_notes": "Focus on minimalist design and comfort, functional athleisure trend", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "bra", "season": "fall", "occasion": "sports", "base_colour": "black"}`
- Normalized Predicted: `{"garment_type": "bra", "style": "sporty", "occasion": "sports", "season": "all seasons", "base_colour": "black"}`
- Semantic Match: `{"garment_type": true, "style": false, "occasion": true, "season": true, "base_colour": true}`

### 30917.jpg
- Expected: `{"garment_type": "Trousers", "season": "summer", "occasion": "ethnic", "base_colour": "black"}`
- Predicted: `{"description": "Loose-fitting, crinkled black pants with an elastic waistband and ankle cuffs, styled with a tie drawstring, paired with simple sandals.", "garment_type": "pants", "style": "bohemian, casual, relaxed fit", "material": "lightweight, crinkled fabric, possibly cotton or a cotton blend", "color_palette": "['black', 'red (sandals)']", "pattern": "solid with a natural crinkled texture", "season": "spring, summer", "occasion": "casual, everyday wear, travel", "consumer_profile": "individuals seeking comfort and casual style, possibly young adults or those favoring boho or relaxed aesthetics", "trend_notes": "comfort and relaxed fits are trending; natural textures and adjustable waistbands add practical style points.", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "trousers", "season": "summer", "occasion": "ethnic", "base_colour": "black"}`
- Normalized Predicted: `{"garment_type": "trousers", "style": "casual", "occasion": "travel", "season": "spring/summer", "base_colour": "black/red"}`
- Semantic Match: `{"garment_type": true, "style": false, "occasion": false, "season": true, "base_colour": true}`

### 27433.jpg
- Expected: `{"garment_type": "Bra", "season": "winter", "occasion": "sports", "base_colour": "grey melange"}`
- Predicted: `{"description": "A two-tone sports bra with a grey front panel and black borders and sides, featuring a scoop neckline and wide shoulder straps.", "garment_type": "Sports bra", "style": "Athleisure, casual", "material": "Cotton or cotton blend with elastic trim", "color_palette": "['grey', 'black']", "pattern": "Solid color blocks", "season": "Spring/Summer", "occasion": "Sport, workout, casual wear", "consumer_profile": "Active individuals seeking comfort and support during physical activities", "trend_notes": "Focus on comfort and minimalistic design in athleisure wear", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "bra", "season": "winter", "occasion": "sports", "base_colour": "grey"}`
- Normalized Predicted: `{"garment_type": "bra", "style": "sporty", "occasion": "sports", "season": "spring/summer", "base_colour": "black/grey"}`
- Semantic Match: `{"garment_type": true, "style": false, "occasion": true, "season": false, "base_colour": true}`

### 25895.jpg
- Expected: `{"garment_type": "Camisoles", "season": "summer", "occasion": "casual", "base_colour": "white"}`
- Predicted: `{"description": "Casual summer outfit featuring a white spaghetti strap tank top paired with dark denim shorts and a brown leather belt.", "garment_type": "Tank top and Denim shorts", "style": "Casual, Summer", "material": "Likely cotton or cotton blend for the tank top; denim for the shorts; leather for the belt", "color_palette": "White, Dark blue (denim), Brown", "pattern": "Solid colors with no prominent pattern", "season": "Summer", "occasion": "Casual outings, daywear", "consumer_profile": "Young adults or adults seeking comfortable, casual summer wear", "trend_notes": "Minimalist and classic summer styling with emphasis on comfort and simplicity", "continent": null, "country": null, "city": null}`
- Normalized Expected: `{"garment_type": "camisoles", "season": "summer", "occasion": "casual", "base_colour": "white"}`
- Normalized Predicted: `{"garment_type": "camisoles", "style": "casual", "occasion": "casual", "season": "summer", "base_colour": "white/blue/brown"}`
- Semantic Match: `{"garment_type": true, "style": false, "occasion": true, "season": true, "base_colour": true}`

## Notes

- This report evaluates whichever classifier is currently configured via the backend provider settings.
- The benchmark labels are sourced from the curated 100-image evaluation subset in `eval/labels/candidate_labels.json`.
- `Strict normalized` scores compare canonicalized labels conservatively.
- `Semantic relaxed` scores allow taxonomy-aware overlap so natural-language outputs can be matched more fairly against the dataset labels.