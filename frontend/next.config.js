const apiBase = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

module.exports = {
  async rewrites() {
    return [
      {
        source: "/api/:path*",
        destination: `${apiBase}/:path*`,
      },
    ];
  },
};
