/** @type {import('tailwindcss').Config} */
export default {
  content: [
    ".././network/templates/**/*.{html,js}",
    "network/templates/network/*.html",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin'),
  ],
}

