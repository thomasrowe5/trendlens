"use client";
import { useState, useEffect } from "react";

export default function Trends() {
  const [tag, setTag] = useState("fitness");
  const [data, setData] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  async function fetchData() {
    try {
      // Build a clean, absolute URL (avoids malformed pattern errors)
      const base = "http://localhost:8000";
      const url = `${base}/api/trends?tag=${encodeURIComponent(tag.trim())}`;
      console.log("DEBUG – Fetching:", url);

      const r = await fetch(url, { cache: "no-store" });
      if (!r.ok) throw new Error(`HTTP ${r.status}`);
      const json = await r.json();
      setData(json);
      setError(null);
    } catch (err: any) {
      console.error("Fetch error:", err);
      setError(err.message || "Unknown error");
      setData([]);
    }
  }

  useEffect(() => {
    fetchData();
  }, [tag]);

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold">TikTok Trends</h1>

      <div className="flex gap-2 mt-4">
        <input
          className="px-3 py-2 rounded border border-gray-700 bg-black"
          value={tag}
          onChange={(e) => setTag(e.target.value)}
          placeholder="Enter hashtag..."
        />
        <button
          onClick={fetchData}
          className="px-4 py-2 bg-white text-black rounded"
        >
          Search
        </button>
      </div>

      {error && (
        <p className="text-red-400 mt-4">Error loading data: {error}</p>
      )}

      <div className="grid md:grid-cols-2 gap-3 mt-6">
        {data.map((v, i) => (
          <div key={i} className="p-3 border border-gray-700 rounded">
            <p className="font-mono">{v.video_id}</p>
            <p className="text-gray-300 text-sm">@{v.author}</p>
            <p className="text-xs mt-1">
              👍 {v.likes} · 👁️ {v.views} · 💬 {v.comments}
            </p>
          </div>
        ))}
      </div>
    </main>
  );
}
