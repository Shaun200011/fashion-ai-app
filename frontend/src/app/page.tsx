import { LibraryShell } from "@/components/library-shell";
import { fetchImages } from "@/lib/api";
import type { ImageListItem } from "@/lib/types";

export default async function Home() {
  let images: ImageListItem[] = [];
  let hasBackendData = false;

  try {
    images = await fetchImages();
    hasBackendData = true;
  } catch (_error) {
    images = [];
    hasBackendData = false;
  }

  return <LibraryShell initialImages={images} hasBackendData={hasBackendData} />;
}
