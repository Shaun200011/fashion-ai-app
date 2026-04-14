import { LibraryShell } from "@/components/library-shell";
import { fetchFilters, fetchImages } from "@/lib/api";
import type { FilterGroup, ImageListItem } from "@/lib/types";

export default async function Home() {
  let images: ImageListItem[] = [];
  let filterGroups: FilterGroup[] = [];
  let hasBackendData = false;

  try {
    [images, filterGroups] = await Promise.all([fetchImages(), fetchFilters()]);
    hasBackendData = true;
  } catch (_error) {
    images = [];
    filterGroups = [];
    hasBackendData = false;
  }

  return (
    <LibraryShell
      initialImages={images}
      hasBackendData={hasBackendData}
      filterGroups={filterGroups}
    />
  );
}
