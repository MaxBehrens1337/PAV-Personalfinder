/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        // PAV Corporate Identity Colors
        pav: {
          turquoise: '#018A9C',      // Primary: Navigation, Key-UI
          'dark-green': '#009657',   // Buttons (CTA), Akzente
          'light-green': '#50AF31',  // Secondary UI-Akzente
          magenta: '#E62487',        // Badges, Highlights (sparsam!)
          white: '#FFFFFF',          // Haupt-Hintergrund
          ink: '#111111',            // Standard-Fließtext
          'soft-grey': '#F4F6F7',    // Panels, Sektionen, UI-Hintergründe
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'BlinkMacSystemFont', 'Segoe UI', 'sans-serif'],
      },
      letterSpacing: {
        'pav-headline': '0.08em',    // +80
        'pav-nav': '0.06em',         // +60
        'pav-body': '0.02em',        // +20
      },
      borderRadius: {
        'pav-card': '24px',          // Cards/Panels
        'pav-pill': '999px',         // Buttons (vollständig rund)
      },
      strokeWidth: {
        'pav-icon': '2px',           // Icon stroke width
      },
    },
  },
  plugins: [],
}
