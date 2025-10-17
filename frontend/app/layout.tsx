export const metadata = { title: "TrendLens" };
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body className="bg-black text-white">{children}</body></html>;
}
