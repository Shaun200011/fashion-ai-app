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
