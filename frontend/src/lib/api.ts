import type { ImageListItem } from "@/lib/types";

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

export { API_BASE_URL };
