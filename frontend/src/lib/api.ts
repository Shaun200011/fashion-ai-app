import type { FilterGroup, ImageListItem } from "@/lib/types";

const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL ?? "http://127.0.0.1:8000/api";

export async function fetchImages(): Promise<ImageListItem[]> {
  const response = await fetch(`${API_BASE_URL}/images`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch image library.");
  }

  return response.json();
}

export async function fetchFilteredImages(params: {
  query?: string;
  garment_type?: string;
  material?: string;
  season?: string;
  occasion?: string;
}): Promise<ImageListItem[]> {
  const searchParams = new URLSearchParams();

  Object.entries(params).forEach(([key, value]) => {
    if (value) {
      searchParams.set(key, value);
    }
  });

  const suffix = searchParams.toString() ? `?${searchParams.toString()}` : "";
  const response = await fetch(`${API_BASE_URL}/images${suffix}`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch filtered images.");
  }

  return response.json();
}

export async function fetchFilters(): Promise<FilterGroup[]> {
  const response = await fetch(`${API_BASE_URL}/filters`, {
    cache: "no-store",
  });

  if (!response.ok) {
    throw new Error("Failed to fetch filter groups.");
  }

  return response.json();
}

export async function uploadImage(input: {
  file: File;
  designerName?: string;
  capturedAt?: string;
}): Promise<ImageListItem> {
  const formData = new FormData();
  formData.append("file", input.file);

  if (input.designerName) {
    formData.append("designer_name", input.designerName);
  }

  if (input.capturedAt) {
    formData.append("captured_at", input.capturedAt);
  }

  const response = await fetch(`${API_BASE_URL}/images/upload`, {
    method: "POST",
    body: formData,
  });

  if (!response.ok) {
    throw new Error("Failed to upload image.");
  }

  return response.json();
}

export async function createAnnotation(input: {
  imageId: number;
  kind?: string;
  content: string;
  author?: string;
}) {
  const response = await fetch(`${API_BASE_URL}/images/${input.imageId}/annotations`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      kind: input.kind ?? "note",
      content: input.content,
      author: input.author,
    }),
  });

  if (!response.ok) {
    throw new Error("Failed to create annotation.");
  }

  return response.json();
}

export { API_BASE_URL };
