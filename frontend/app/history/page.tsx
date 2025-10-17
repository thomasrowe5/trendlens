"use client";
import { useState, useEffect } from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
} from "recharts";

export default function HistoryPage() {
  const [data, setData] = useState<any[]>([]);
  const [tag, setTag] = useState("fitness");

  async function load() {
    try {
      const r = await fetch(
        `http://localhost:8000/api/trends/history?tag=${encodeURIComponent(tag)}`
      );
      const json = await r.json();
      setData(json.reverse()); // show oldest first
    } catch (err) {
      console.error("Load error:", err);
      setData([]);
    }
  }

  useEffect(() => {
    load();
  }, [tag]);

  return (
    <main className="p-6">
      <h1 className="text-2xl font-bold mb-4">Trend History</h1>

      <div className="flex gap-2 mb-6">
        <input
          value={tag}
          onChange={(e) => setTag(e.target.value)}
          className="px-3 py-2 rounded border border-gray-700 bg-black"
        />
        <button
          onClick={load}
          className="px-4 py-2 bg-white text-black rounded"
        >
          Refresh
        </button>
      </div>

      <ResponsiveContainer width="100%" height={400}>
        <LineChart data={data}>
          <CartesianGrid strokeDasharray="3 3" stroke="#333" />
          <XAxis
            dataKey="collected_at"
            tick={{ fontSize: 10 }}
            angle={-30}
            textAnchor="end"
          />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line
            type="monotone"
            dataKey="likes"
            stroke="#82ca9d"
            name="Likes"
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="views"
            stroke="#8884d8"
            name="Views"
            dot={false}
          />
          <Line
            type="monotone"
            dataKey="comments"
            stroke="#ff7300"
            name="Comments"
            dot={false}
          />
        </LineChart>
      </ResponsiveContainer>
    </main>
  );
}
