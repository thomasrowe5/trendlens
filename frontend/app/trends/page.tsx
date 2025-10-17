"use client";

import { useCallback, useEffect, useState } from "react";

import { fetchTrends, TrendRecord } from "@/lib/api";

export default function Trends() {
  const [tag, setTag] = useState("fitness");
  const [data, setData] = useState<TrendRecord[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const fetchData = useCallback(async () => {
    const cleanedTag = tag.trim();
    if (!cleanedTag) {
      setError("Enter a hashtag to search.");
      setData([]);
      return;
    }

    setLoading(true);
    try {
      const json = await fetchTrends(cleanedTag);
      setData(json);
      setError(null);
    } catch (err: any) {
      setError(err.message || "Unknown error");
      setData([]);
    } finally {
      setLoading(false);
    }
  }, [tag]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

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
          disabled={loading}
        >
          {loading ? "Loading..." : "Search"}
        </button>
      </div>

      {error && (
        <p className="text-red-400 mt-4">Error loading data: {error}</p>
      )}

      <div className="grid md:grid-cols-2 gap-3 mt-6">
        {data.map((v) => (
          <div key={`${v.video_id}-${v.author}`} className="p-3 border border-gray-700 rounded">
            <p className="font-mono break-words">{v.video_id}</p>
            <p className="text-gray-300 text-sm">@{v.author}</p>
            <p className="text-xs mt-1">
              👍 {v.likes} · 👁️ {v.views} · 💬 {v.comments}
            </p>
          </div>
        ))}
        {!loading && !error && data.length === 0 && (
          <p className="text-gray-400">No data yet. Try another hashtag.</p>
        )}
      </div>
    </main>
  );
}
