"use client";

import { useState, useTransition } from "react";

import { uploadImage } from "@/lib/api";
import type { ImageListItem } from "@/lib/types";

type Props = {
  initialImages: ImageListItem[];
  hasBackendData: boolean;
};

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

export function LibraryShell({ initialImages, hasBackendData }: Props) {
  const [images, setImages] = useState(initialImages);
  const [designerName, setDesignerName] = useState("Womenswear Team");
  const [capturedAt, setCapturedAt] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [isPending, startTransition] = useTransition();

  const hasImages = images.length > 0;
  const isUsingFallback = !hasImages && !hasBackendData;

  function handleUploadSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile) {
      setFeedback("Choose an image before uploading.");
      return;
    }

    setFeedback(null);

    startTransition(async () => {
      try {
        const uploaded = await uploadImage({
          file: selectedFile,
          designerName: designerName.trim() || undefined,
          capturedAt: capturedAt || undefined,
        });

        setImages((current) => [uploaded, ...current]);
        setSelectedFile(null);
        setCapturedAt("");
        setFeedback("Upload complete. Placeholder AI metadata has been added.");
      } catch (_error) {
        setFeedback("Upload failed. Make sure the backend is running on port 8000.");
      }
    });
  }

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
            <button className="primary-button" type="button">
              Upload New Look
            </button>
            <button className="secondary-button" type="button">
              Browse Library
            </button>
          </div>
        </div>
        <div className="hero-panel">
          <div className="hero-stat">
            <span>Library Size</span>
            <strong>{hasImages ? `${images.length} looks` : "126 looks"}</strong>
          </div>
          <div className="hero-stat">
            <span>Top Trend Signal</span>
            <strong>
              {hasImages
                ? images[0]?.ai_metadata?.trend_notes ?? "Metadata incoming"
                : "Artisan neckline details"}
            </strong>
          </div>
          <div className="hero-stat">
            <span>Latest Capture</span>
            <strong>
              {hasImages ? images[0]?.original_filename ?? "Awaiting upload" : "Tokyo utility denim study"}
            </strong>
          </div>
        </div>
      </section>

      <section className="content-grid">
        <div className="upload-card">
          <div className="card-head">
            <p className="section-label">Ingestion</p>
            <h2>Drop in new inspiration</h2>
          </div>
          <form className="upload-form" onSubmit={handleUploadSubmit}>
            <label className="upload-zone" htmlFor="file-upload">
              <input
                id="file-upload"
                className="file-input"
                type="file"
                accept="image/*"
                onChange={(event) => setSelectedFile(event.target.files?.[0] ?? null)}
              />
              <p>{selectedFile ? selectedFile.name : "Drag garment photos here"}</p>
              <span>
                {selectedFile ? "Ready to upload" : "or choose files from your archive"}
              </span>
            </label>
            <div className="meta-row">
              <div>
                <label htmlFor="designer-name">Designer</label>
                <input
                  id="designer-name"
                  className="text-input"
                  value={designerName}
                  onChange={(event) => setDesignerName(event.target.value)}
                  placeholder="Womenswear Team"
                />
              </div>
              <div>
                <label htmlFor="captured-at">Capture Date</label>
                <input
                  id="captured-at"
                  className="text-input"
                  type="datetime-local"
                  value={capturedAt}
                  onChange={(event) => setCapturedAt(event.target.value)}
                />
              </div>
            </div>
            <div className="upload-actions">
              <button className="primary-button" type="submit" disabled={isPending}>
                {isPending ? "Uploading..." : "Upload and classify"}
              </button>
              {feedback ? <p className="feedback-message">{feedback}</p> : null}
            </div>
          </form>
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
            <span>
              {hasImages
                ? "Live data loaded from the backend image library."
                : "Try “embroidered neckline”"}
            </span>
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

        {isUsingFallback ? <p className="library-banner">Backend not connected yet. Showing editorial sample content.</p> : null}

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
