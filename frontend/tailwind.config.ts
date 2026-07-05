import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: "#040811",
        surface: "#0B1220",
        card: "#101826",
        card2: "#0F1B2E",
        border: "#1E293B",
        primary: "#2563EB",
        primaryHover: "#104DB8",
        secondary: "#16A34A",
        accent: "#EA580C",
        text: "#F8FAFC",
        muted: "#94A3B8",
      },
      fontFamily: {
        sans: ["Inter", "ui-sans-serif", "system-ui", "sans-serif"],
      },
      borderRadius: {
        card: "16px",
      },
      boxShadow: {
        card: "0 4px 24px rgba(0,0,0,0.35)",
        glow: "0 0 40px rgba(37,99,235,0.35)",
      },
      keyframes: {
        pulseSoft: {
          "0%,100%": { opacity: "1" },
          "50%": { opacity: "0.55" },
        },
        fadeInUp: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      animation: {
        pulseSoft: "pulseSoft 1.6s ease-in-out infinite",
        fadeInUp: "fadeInUp 0.4s ease-out",
      },
    },
  },
  plugins: [],
};
export default config;
