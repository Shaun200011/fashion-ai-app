import { fetchImages } from "@/lib/api";
import type { ImageListItem } from "@/lib/types";

const sampleLooks = [
  {
    title: "Market embroidery study",
    place: "Marrakesh, Morocco",
    garment: "Top",
    palette: "Saffron, cream, charcoal",
  },
  {
    title: "Soft tailored street layer",
    place: "Copenhagen, Denmark",
    garment: "Outerwear",
    palette: "Stone, navy, silver",
  },
  {
    title: "Utility denim proportion",
    place: "Tokyo, Japan",
    garment: "Bottom",
    palette: "Indigo, rust, black",
  },
];

const filterGroups = [
  { label: "Garment", value: "Outerwear" },
  { label: "Material", value: "Cotton" },
  { label: "Season", value: "Transitional" },
  { label: "Context", value: "Street market" },
];

function getLocationLabel(image: ImageListItem): string {
  const locationParts = [
    image.ai_metadata?.city,
    image.ai_metadata?.country,
    image.ai_metadata?.continent,
  ].filter(Boolean);

  return locationParts.length > 0 ? locationParts.join(", ") : "Location pending";
}

function getPaletteLabel(image: ImageListItem): string {
  return image.ai_metadata?.color_palette ?? "Palette pending";
}

function getDesignerNote(image: ImageListItem): string {
  if (image.designer_name) {
    return `${image.designer_name} uploaded this look for later review.`;
  }

  return "Designer note capture will be added in the next iteration.";
}

export default async function Home() {
  let images: ImageListItem[] = [];

  try {
    images = await fetchImages();
  } catch (_error) {
    images = [];
  }

  const hasImages = images.length > 0;

  return (
    <main className="page-shell">
      <section className="hero">
        <div className="hero-copy">
          <p className="eyebrow">Fashion Inspiration Intelligence</p>
          <h1>Turn field photos into a searchable design memory.</h1>
          <p className="hero-text">
            Upload garment imagery, generate structured AI metadata, and layer in
            designer observations without losing the editorial feel of the source.
          </p>
          <div className="hero-actions">
            <button className="primary-button">Upload New Look</button>
            <button className="secondary-button">Browse Library</button>
          </div>
        </div>
        <div className="hero-panel">
          <div className="hero-stat">
            <span>Library Size</span>
            <strong>126 looks</strong>
          </div>
          <div className="hero-stat">
            <span>Top Trend Signal</span>
            <strong>Artisan neckline details</strong>
          </div>
          <div className="hero-stat">
            <span>Latest Capture</span>
            <strong>Tokyo utility denim study</strong>
          </div>
        </div>
      </section>

      <section className="content-grid">
        <div className="upload-card">
          <div className="card-head">
            <p className="section-label">Ingestion</p>
            <h2>Drop in new inspiration</h2>
          </div>
          <div className="upload-zone">
            <p>Drag garment photos here</p>
            <span>or choose files from your archive</span>
          </div>
          <div className="meta-row">
            <div>
              <label>Designer</label>
              <div className="fake-input">Womenswear Team</div>
            </div>
            <div>
              <label>Capture Date</label>
              <div className="fake-input">April 2026</div>
            </div>
          </div>
        </div>

        <div className="filter-card">
          <div className="card-head">
            <p className="section-label">Discovery</p>
            <h2>Dynamic filters</h2>
          </div>
          <div className="filter-list">
            {filterGroups.map((filter) => (
              <div className="filter-pill" key={filter.label}>
                <span>{filter.label}</span>
                <strong>{filter.value}</strong>
              </div>
            ))}
          </div>
          <div className="search-box">
            <span>Try “embroidered neckline”</span>
          </div>
        </div>
      </section>

      <section className="library-section">
        <div className="section-header">
          <div>
            <p className="section-label">Library</p>
            <h2>{hasImages ? "Live inspiration library" : "Recent inspiration captures"}</h2>
          </div>
          <p className="section-note">
            AI metadata remains separate from human notes so designers can trust
            and refine the library over time.
          </p>
        </div>

        <div className="look-grid">
          {hasImages
            ? images.map((image, index) => (
                <article className="look-card" key={image.id}>
                  <div className={`look-visual look-tone-${(index % 3) + 1}`}>
                    <span>{getLocationLabel(image)}</span>
                  </div>
                  <div className="look-body">
                    <div className="look-heading">
                      <h3>{image.original_filename}</h3>
                      <p>{image.ai_metadata?.garment_type ?? "Unknown garment"}</p>
                    </div>
                    <dl className="look-meta">
                      <div>
                        <dt>Palette</dt>
                        <dd>{getPaletteLabel(image)}</dd>
                      </div>
                      <div>
                        <dt>AI Note</dt>
                        <dd>
                          {image.ai_metadata?.description ??
                            "AI description will appear after classification."}
                        </dd>
                      </div>
                      <div>
                        <dt>Designer Note</dt>
                        <dd>{getDesignerNote(image)}</dd>
                      </div>
                    </dl>
                  </div>
                </article>
              ))
            : sampleLooks.map((look, index) => (
                <article className="look-card" key={look.title}>
                  <div className={`look-visual look-tone-${index + 1}`}>
                    <span>{look.place}</span>
                  </div>
                  <div className="look-body">
                    <div className="look-heading">
                      <h3>{look.title}</h3>
                      <p>{look.garment}</p>
                    </div>
                    <dl className="look-meta">
                      <div>
                        <dt>Palette</dt>
                        <dd>{look.palette}</dd>
                      </div>
                      <div>
                        <dt>AI Note</dt>
                        <dd>Contemporary silhouette with tactile detailing.</dd>
                      </div>
                      <div>
                        <dt>Designer Note</dt>
                        <dd>Strong neckline story worth revisiting for resort.</dd>
                      </div>
                    </dl>
                  </div>
                </article>
              ))}
        </div>
      </section>
    </main>
  );
}
