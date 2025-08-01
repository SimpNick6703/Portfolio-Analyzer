/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class', // Enable class-based dark mode
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // Light theme ('solarized-light')
        'light-base': '#fdf6e3', // The main background
        'light-content': '#eee8d5', // Slightly darker content background
        'light-text': '#657b83', // Main text color
        'light-text-strong': '#073642', // Bolder text
        'light-accent': '#268bd2', // Accent color for links, buttons
        
        // Dark theme ('solarized-dark')
        'dark-base': '#002b36', // The main background
        'dark-content': '#073642', // Slightly lighter content background
        'dark-text': '#839496', // Main text color
        'dark-text-strong': '#fdf6e3', // Bolder text
        'dark-accent': '#268bd2', // Accent color (can be the same or different)
      },
    },
  },
  plugins: [],
}