/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
    "./js/**/*.{js,ts,jsx,tsx}"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Warhammer Fantasy color palette
        primary: {
          50: '#fef7ee',
          100: '#fdecd3',
          200: '#fbd5a5',
          300: '#f7b76d',
          400: '#f29332',
          500: '#ee770a',
          600: '#df5f05',
          700: '#b94708',
          800: '#94380e',
          900: '#792f0f',
          950: '#411505',
        },
        secondary: {
          50: '#f8fafc',
          100: '#f1f5f9',
          200: '#e2e8f0',
          300: '#cbd5e1',
          400: '#94a3b8',
          500: '#64748b',
          600: '#475569',
          700: '#334155',
          800: '#1e293b',
          900: '#0f172a',
          950: '#020617',
        },
        // Faction colors
        empire: {
          light: '#ffd700',
          DEFAULT: '#b8860b',
          dark: '#8b6914'
        },
        chaos: {
          light: '#ff6b6b',
          DEFAULT: '#8b0000',
          dark: '#4a0000'
        },
        elves: {
          light: '#98fb98',
          DEFAULT: '#228b22',
          dark: '#006400'
        },
        dwarfs: {
          light: '#daa520',
          DEFAULT: '#b8860b',
          dark: '#8b6914'
        },
        // UI colors
        tavern: {
          wood: '#8b4513',
          stone: '#696969',
          fire: '#ff4500',
          shadow: '#2f1b14'
        }
      },
      fontFamily: {
        'medieval': ['Cinzel', 'serif'],
        'fantasy': ['Uncial Antiqua', 'cursive'],
        'sharp': ['MedievalSharp', 'cursive'],
        'sans': ['Inter', 'system-ui', 'sans-serif'],
        'mono': ['JetBrains Mono', 'monospace']
      },
      animation: {
        'fade-in': 'fadeIn 0.5s ease-in-out',
        'slide-up': 'slideUp 0.3s ease-out',
        'slide-down': 'slideDown 0.3s ease-out',
        'scale-in': 'scaleIn 0.2s ease-out',
        'bounce-subtle': 'bounceSubtle 0.6s ease-in-out',
        'glow': 'glow 2s ease-in-out infinite alternate',
        'flicker': 'flicker 1.5s ease-in-out infinite',
        'float': 'float 3s ease-in-out infinite',
        'pulse-slow': 'pulse 3s cubic-bezier(0.4, 0, 0.6, 1) infinite'
      },
      keyframes: {
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' }
        },
        slideUp: {
          '0%': { transform: 'translateY(10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        slideDown: {
          '0%': { transform: 'translateY(-10px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' }
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' }
        },
        bounceSubtle: {
          '0%, 100%': { transform: 'translateY(0)' },
          '50%': { transform: 'translateY(-5px)' }
        },
        glow: {
          '0%': { boxShadow: '0 0 5px rgba(255, 215, 0, 0.5)' },
          '100%': { boxShadow: '0 0 20px rgba(255, 215, 0, 0.8)' }
        },
        flicker: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.8' }
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' }
        }
      },
      backdropBlur: {
        xs: '2px'
      },
      spacing: {
        '18': '4.5rem',
        '88': '22rem',
        '128': '32rem'
      },
      borderRadius: {
        '4xl': '2rem'
      },
      boxShadow: {
        'glow': '0 0 20px rgba(255, 215, 0, 0.3)',
        'glow-lg': '0 0 40px rgba(255, 215, 0, 0.4)',
        'inner-glow': 'inset 0 0 20px rgba(255, 215, 0, 0.2)',
        'tavern': '0 8px 32px rgba(0, 0, 0, 0.4)',
        'character': '0 4px 16px rgba(0, 0, 0, 0.3)'
      },
      backgroundImage: {
        'gradient-radial': 'radial-gradient(var(--tw-gradient-stops))',
        'gradient-conic': 'conic-gradient(from 180deg at 50% 50%, var(--tw-gradient-stops))',
        'tavern-wood': 'linear-gradient(45deg, #8b4513, #a0522d)',
        'fire-glow': 'radial-gradient(circle, #ff4500, #ff6347, transparent)'
      }
    },
  },
  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
    require('@tailwindcss/aspect-ratio'),
    // Custom plugin for Warhammer-specific utilities
    function({ addUtilities, theme }) {
      const newUtilities = {
        '.text-glow': {
          textShadow: '0 0 10px currentColor'
        },
        '.text-glow-lg': {
          textShadow: '0 0 20px currentColor'
        },
        '.bg-tavern-pattern': {
          backgroundImage: `
            radial-gradient(circle at 25% 25%, rgba(139, 69, 19, 0.1) 0%, transparent 50%),
            radial-gradient(circle at 75% 75%, rgba(160, 82, 45, 0.1) 0%, transparent 50%)
          `
        },
        '.faction-empire': {
          '--faction-color': theme('colors.empire.DEFAULT'),
          color: 'var(--faction-color)',
          borderColor: 'var(--faction-color)'
        },
        '.faction-chaos': {
          '--faction-color': theme('colors.chaos.DEFAULT'),
          color: 'var(--faction-color)',
          borderColor: 'var(--faction-color)'
        },
        '.faction-elves': {
          '--faction-color': theme('colors.elves.DEFAULT'),
          color: 'var(--faction-color)',
          borderColor: 'var(--faction-color)'
        },
        '.faction-dwarfs': {
          '--faction-color': theme('colors.dwarfs.DEFAULT'),
          color: 'var(--faction-color)',
          borderColor: 'var(--faction-color)'
        }
      }
      addUtilities(newUtilities)
    }
  ],
}
