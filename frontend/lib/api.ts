export async function fetchVelocity(tag: string) {
  const base =
    process.env.NEXT_PUBLIC_API_BASE?.replace(/\/$/, "") ||
    "http://localhost:8000";
  const url = `${base}/api/trends?tag=${encodeURIComponent(tag)}`;
  const r = await fetch(url, { cache: "no-store" });
  if (!r.ok) throw new Error(`Request failed: ${r.status}`);
  return await r.json();
}

export async function fetchTop(tag: string) {
  const base =
    process.env.NEXT_PUBLIC_API_BASE?.replace(/\/$/, "") ||
    "http://localhost:8000";
  const url = `${base}/api/trends/top?tag=${encodeURIComponent(tag)}`;
  const r = await fetch(url, { cache: "no-store" });
  if (!r.ok) throw new Error(`Request failed: ${r.status}`);
  return await r.json();
}
