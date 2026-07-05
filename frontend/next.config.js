/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: "export",           // static export - no Node server needed at runtime
  images: { unoptimized: true },
  trailingSlash: true,        // "/dashboard/" -> dashboard/index.html, matches static hosting
};

module.exports = nextConfig;

