/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        brand: {
          50: '#f4f6fe',
          100: '#ebf0fd',
          200: '#dce5fb',
          300: '#c2d2f8',
          400: '#9db4f3',
          500: '#7390ee',
          600: '#546fe6',
          700: '#4157d0',
          800: '#3848ab',
          900: '#323f88',
          950: '#1e2453',
        },
        slate: {
          850: '#151c2c',
        }
      },
      fontFamily: {
        sans: ['Inter', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
