export type ClassificationResult = {
  description: string;
  garment_type?: string | null;
  style?: string | null;
  material?: string | null;
  color_palette?: string | null;
  pattern?: string | null;
  season?: string | null;
  occasion?: string | null;
  consumer_profile?: string | null;
  trend_notes?: string | null;
  continent?: string | null;
  country?: string | null;
  city?: string | null;
};

export type ImageListItem = {
  id: number;
  file_path: string;
  original_filename: string;
  designer_name?: string | null;
  captured_at?: string | null;
  created_at: string;
  ai_metadata?: ClassificationResult | null;
};

export type FilterOption = {
  label: string;
  value: string;
  count: number;
};

export type FilterGroup = {
  key: string;
  label: string;
  options: FilterOption[];
};
