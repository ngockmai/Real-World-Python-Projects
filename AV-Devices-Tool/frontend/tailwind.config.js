/** @type {import('tailwindcss').Config} */
export default {
    content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
    extend: {
        colors: {
        'gve-blue': '#1E3A8A', // Approximate blue from the header
        'gve-gray': '#D1D5DB', // Approximate gray for borders
        },
    },
    },
    plugins: [],
}