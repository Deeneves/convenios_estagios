/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./templates/**/*.html",
    "./apps/**/templates/**/*.html",
    "./apps/**/*.py",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: "#eef4ed",
          100: "#8da9c4",
          200: "#8da9c4",
          300: "#134074",
          400: "#134074",
          500: "#13315c",
          600: "#13315c",
          700: "#0b2545",
          800: "#0b2545",
          900: "#0b2545",
        },
      },
    },
  },
  plugins: [],
};
