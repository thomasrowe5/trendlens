const base = process.env.NEXT_PUBLIC_API_BASE ?? "http://localhost:8000";
const normalizedBase = base.endsWith("/") ? base.slice(0, -1) : base;

async function fetchJson(path: string) {
  const response = await fetch(`${normalizedBase}${path}`, {
    cache: "no-store",
  });
  if (!response.ok) {
    throw new Error(`Request failed: ${response.status}`);
  }
  return response.json();
}

export type TrendRecord = {
  video_id: string;
  author: string;
  likes: number;
  views: number;
  comments: number;
  collected_at?: string | null;
  tag?: string;
};

export async function fetchTrends(tag: string): Promise<TrendRecord[]> {
  return fetchJson(`/api/trends?tag=${encodeURIComponent(tag)}`);
}

export async function fetchTrendHistory(
  tag?: string,
  limit: number = 50
): Promise<TrendRecord[]> {
  const search = new URLSearchParams();
  if (tag) search.set("tag", tag);
  if (limit) search.set("limit", String(limit));
  return fetchJson(`/api/trends/history?${search.toString()}`);
}
