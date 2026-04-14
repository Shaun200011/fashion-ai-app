"use client";

import { useState, useTransition } from "react";

import {
  buildAssetUrl,
  createAnnotation,
  fetchFilteredImages,
  uploadImage,
} from "@/lib/api";
import type { FilterGroup, ImageListItem } from "@/lib/types";

type Props = {
  initialImages: ImageListItem[];
  hasBackendData: boolean;
  filterGroups: FilterGroup[];
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

const fallbackFilterGroups: FilterGroup[] = [
  {
    key: "garment_type",
    label: "Garment",
    options: [{ label: "Outerwear", value: "outerwear", count: 3 }],
  },
  {
    key: "material",
    label: "Material",
    options: [{ label: "Cotton", value: "cotton", count: 2 }],
  },
  {
    key: "season",
    label: "Season",
    options: [{ label: "Transitional", value: "transitional", count: 3 }],
  },
  {
    key: "occasion",
    label: "Occasion",
    options: [{ label: "Daywear", value: "daywear", count: 3 }],
  },
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
  if (image.annotations.length > 0) {
    const latest = image.annotations[0];
    return latest.author ? `${latest.author}: ${latest.content}` : latest.content;
  }

  if (image.designer_name) {
    return `${image.designer_name} uploaded this look for later review.`;
  }

  return "Designer note capture will be added in the next iteration.";
}

function getDisplayTitle(filename: string): string {
  const stem = filename.replace(/\.[^/.]+$/, "");
  if (/^\d+$/.test(stem)) {
    return "Curated fashion reference";
  }
  const cleaned = stem
    .replace(/[_-]+/g, " ")
    .replace(/\s+/g, " ")
    .trim();

  if (/^截屏\d+/i.test(cleaned) || /^screenshot/i.test(cleaned)) {
    return "Captured field reference";
  }

  return cleaned || filename;
}

function getAiSummary(image: ImageListItem): string {
  return image.ai_metadata?.description ?? "AI description will appear after classification.";
}

export function LibraryShell({ initialImages, hasBackendData, filterGroups }: Props) {
  const [images, setImages] = useState(initialImages);
  const [designerName, setDesignerName] = useState("Womenswear Team");
  const [capturedAt, setCapturedAt] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [feedback, setFeedback] = useState<string | null>(null);
  const [query, setQuery] = useState("");
  const [activeFilters, setActiveFilters] = useState<Record<string, string>>({});
  const [noteDrafts, setNoteDrafts] = useState<Record<number, string>>({});
  const [isPending, startTransition] = useTransition();

  const hasImages = images.length > 0;
  const isUsingFallback = !hasImages && !hasBackendData;
  const visibleFilterGroups = filterGroups.length > 0 ? filterGroups : fallbackFilterGroups;

  function refreshImages(nextQuery: string, nextFilters: Record<string, string>) {
    startTransition(async () => {
      try {
        const nextImages = await fetchFilteredImages({
          query: nextQuery || undefined,
          garment_type: nextFilters.garment_type,
          material: nextFilters.material,
          season: nextFilters.season,
          occasion: nextFilters.occasion,
        });
        setImages(nextImages);
      } catch (_error) {
        setFeedback("Could not refresh the library from the backend.");
      }
    });
  }

  function handleSearchSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    refreshImages(query, activeFilters);
  }

  function handleFilterToggle(groupKey: string, value: string) {
    const nextFilters = {
      ...activeFilters,
      [groupKey]: activeFilters[groupKey] === value ? "" : value,
    };

    setActiveFilters(nextFilters);
    refreshImages(query, nextFilters);
  }

  function handleUploadSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();

    if (!selectedFile) {
      setFeedback("Choose an image before uploading.");
      return;
    }

    setFeedback(null);

    startTransition(async () => {
      try {
        await uploadImage({
          file: selectedFile,
          designerName: designerName.trim() || undefined,
          capturedAt: capturedAt || undefined,
        });

        setSelectedFile(null);
        setCapturedAt("");
        setFeedback("Upload complete. Placeholder AI metadata has been added.");
        const nextImages = await fetchFilteredImages({
          query: query || undefined,
          garment_type: activeFilters.garment_type,
          material: activeFilters.material,
          season: activeFilters.season,
          occasion: activeFilters.occasion,
        });
        setImages(nextImages);
      } catch (_error) {
        setFeedback("Upload failed. Make sure the backend is running on port 8000.");
      }
    });
  }

  function handleAnnotationSubmit(imageId: number) {
    const content = (noteDrafts[imageId] ?? "").trim();
    if (!content) {
      setFeedback("Write a short designer note before saving.");
      return;
    }

    setFeedback(null);

    startTransition(async () => {
      try {
        await createAnnotation({
          imageId,
          content,
          author: designerName.trim() || "Designer",
        });
        const nextImages = await fetchFilteredImages({
          query: query || undefined,
          garment_type: activeFilters.garment_type,
          material: activeFilters.material,
          season: activeFilters.season,
          occasion: activeFilters.occasion,
        });
        setImages(nextImages);
        setNoteDrafts((current) => ({ ...current, [imageId]: "" }));
        setFeedback("Designer note saved.");
      } catch (_error) {
        setFeedback("Could not save the note. Make sure the backend is running.");
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
              {hasImages
                ? getDisplayTitle(images[0]?.original_filename ?? "Awaiting upload")
                : "Tokyo utility denim study"}
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
          <form className="search-form" onSubmit={handleSearchSubmit}>
            <input
              className="text-input search-input"
              aria-label="Search library"
              value={query}
              onChange={(event) => setQuery(event.target.value)}
              placeholder="Search phrases like embroidered neckline or artisan market"
            />
            <button className="secondary-button" type="submit" disabled={isPending}>
              Search
            </button>
          </form>
          <div className="filter-groups">
            {visibleFilterGroups.map((group) => (
              <div className="filter-group" key={group.key}>
                <p className="filter-group-label">{group.label}</p>
                <div className="filter-list">
                  {group.options.length > 0 ? (
                    group.options.map((option) => {
                      const isActive = activeFilters[group.key] === option.value;
                      return (
                        <button
                          className={`filter-pill ${isActive ? "filter-pill-active" : ""}`}
                          key={`${group.key}-${option.value}`}
                          type="button"
                          onClick={() => handleFilterToggle(group.key, option.value)}
                        >
                          <span>{option.label}</span>
                          <strong>{option.count}</strong>
                        </button>
                      );
                    })
                  ) : (
                    <div className="search-box">
                      <span>No values yet</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
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

        {isUsingFallback ? (
          <p className="library-banner">
            Backend not connected yet. Showing editorial sample content.
          </p>
        ) : null}

        <div className="look-grid">
          {hasImages
            ? images.map((image, index) => (
                <article className="look-card look-card-live" key={image.id}>
                  <div className="look-media">
                    <img
                      alt={getDisplayTitle(image.original_filename)}
                      className="look-thumbnail"
                      src={buildAssetUrl(image.image_url)}
                    />
                    <div className="look-media-overlay">
                      <span>{getLocationLabel(image)}</span>
                      <strong>{image.ai_metadata?.garment_type ?? "Unknown garment"}</strong>
                    </div>
                  </div>
                  <div className="look-body">
                    <div className="look-heading">
                      <div>
                        <h3>{getDisplayTitle(image.original_filename)}</h3>
                        <p>{image.original_filename}</p>
                      </div>
                      <div className="look-chip-stack">
                        <span className="look-chip">{getPaletteLabel(image)}</span>
                        <span className="look-chip look-chip-accent">
                          {image.ai_metadata?.season ?? "Season pending"}
                        </span>
                      </div>
                    </div>

                    <div className="insight-grid">
                      <section className="insight-panel">
                        <p className="panel-kicker">AI Metadata</p>
                        <p className="panel-copy">{getAiSummary(image)}</p>
                        <dl className="look-meta">
                          <div>
                            <dt>Material</dt>
                            <dd>{image.ai_metadata?.material ?? "Unknown"}</dd>
                          </div>
                          <div>
                            <dt>Occasion</dt>
                            <dd>{image.ai_metadata?.occasion ?? "Not inferred"}</dd>
                          </div>
                        </dl>
                      </section>

                      <section className="insight-panel insight-panel-human">
                        <p className="panel-kicker">Designer Notes</p>
                        <p className="panel-copy">{getDesignerNote(image)}</p>
                        <div className="annotation-composer">
                          <textarea
                            className="annotation-input"
                            value={noteDrafts[image.id] ?? ""}
                            onChange={(event) =>
                              setNoteDrafts((current) => ({
                                ...current,
                                [image.id]: event.target.value,
                              }))
                            }
                            placeholder="Add a designer observation or follow-up note"
                            rows={3}
                          />
                          <button
                            className="secondary-button annotation-button"
                            type="button"
                            onClick={() => handleAnnotationSubmit(image.id)}
                            disabled={isPending}
                          >
                            Save note
                          </button>
                        </div>
                      </section>
                    </div>
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
