/** @type {import('tailwindcss').Config} */
module.exports = {
  darkMode: 'class',
  content: [
    "./src/**/*.{js,jsx,ts,tsx}",
    "./public/index.html"
  ],
  theme: {
    extend: {
      colors: {
        // Light mode - bright candy colors
        candy: {
          pink: '#FF6B9D',
          blue: '#4ECDC4',
          yellow: '#FFE66D',
          green: '#95E1D3',
          purple: '#A8E6CF',
          orange: '#FFB74D'
        },
        // Dark mode - soft, muted colors
        dark: {
          bg: '#1a1b23',
          surface: '#2d2e3a',
          accent: '#4c4d5c',
          text: '#e2e4e8',
          muted: '#9ca3af'
        }
      },
      fontFamily: {
        'candy': ['Comic Neue', 'cursive', 'system-ui'],
        'sans': ['Inter', 'system-ui', 'sans-serif']
      },
      animation: {
        'bounce-slow': 'bounce 2s infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'float': 'float 3s ease-in-out infinite',
        'shimmer': 'shimmer 2s linear infinite',
        'candy-hop': 'candyHop 0.6s ease-in-out',
        'slide-in': 'slideIn 0.5s ease-out',
        'scale-in': 'scaleIn 0.3s ease-out'
      },
      keyframes: {
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' }
        },
        shimmer: {
          '0%': { transform: 'translateX(-100%)' },
          '100%': { transform: 'translateX(100%)' }
        },
        candyHop: {
          '0%': { transform: 'scale(1) translateY(0)' },
          '50%': { transform: 'scale(1.1) translateY(-20px)' },
          '100%': { transform: 'scale(1) translateY(0)' }
        },
        slideIn: {
          '0%': { opacity: '0', transform: 'translateY(20px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' }
        },
        scaleIn: {
          '0%': { opacity: '0', transform: 'scale(0.9)' },
          '100%': { opacity: '1', transform: 'scale(1)' }
        }
      },
      backdropBlur: {
        xs: '2px'
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms')
  ],
} 