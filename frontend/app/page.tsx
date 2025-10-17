import Link from "next/link";

export default function Home() {
  return (
    <main className="p-8">
      <h1 className="text-4xl font-bold">TrendLens</h1>
      <p className="text-gray-400 mt-2">Discover rising TikTok trends in real time.</p>
      <Link href="/trends" className="inline-block mt-6 px-4 py-2 bg-white text-black rounded">Open Dashboard</Link>
    </main>
  );
}
