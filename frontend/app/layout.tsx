import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ChiefFlow AI - The AI Chief of Staff for Modern Businesses",
  description: "Transform emails, documents, meetings, and business operations into autonomous workflows powered by AI Agents.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="bg-bg text-text min-h-screen">{children}</body>
    </html>
  );
}
