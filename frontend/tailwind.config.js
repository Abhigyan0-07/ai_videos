/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        dark: "#0f0f12",
        primary: "#6366f1", // Indigo 500
        accent: "#a855f7", // Purple 500
      }
    },
  },
  plugins: [],
}
