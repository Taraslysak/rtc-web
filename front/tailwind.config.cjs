/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./index.html", "./src/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {
      colors:{
        'fiord': {
          '50': '#f6f7f9',
          '100': '#ebeef3',
          '200': '#d3dae4',
          '300': '#acbbcd',
          '400': '#7f97b1',
          '500': '#5f7a98',
          '600': '#4b627e',
          '700': '#3f5169',
          '800': '#364456',
          '900': '#303a4a',
        },
      }
    },

  },
  plugins: [],
};

