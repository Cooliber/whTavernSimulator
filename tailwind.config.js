/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./components/**/*.{js,vue,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./plugins/**/*.{js,ts}",
    "./app.vue",
    "./error.vue"
  ],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Inspira UI Base Colors with Warhammer Theme
        border: "hsl(var(--border))",
        input: "hsl(var(--input))",
        ring: "hsl(var(--ring))",
        background: "hsl(var(--background))",
        foreground: "hsl(var(--foreground))",
        primary: {
          DEFAULT: "hsl(var(--primary))",
          foreground: "hsl(var(--primary-foreground))",
        },
        secondary: {
          DEFAULT: "hsl(var(--secondary))",
          foreground: "hsl(var(--secondary-foreground))",
        },
        destructive: {
          DEFAULT: "hsl(var(--destructive))",
          foreground: "hsl(var(--destructive-foreground))",
        },
        muted: {
          DEFAULT: "hsl(var(--muted))",
          foreground: "hsl(var(--muted-foreground))",
        },
        accent: {
          DEFAULT: "hsl(var(--accent))",
          foreground: "hsl(var(--accent-foreground))",
        },
        popover: {
          DEFAULT: "hsl(var(--popover))",
          foreground: "hsl(var(--popover-foreground))",
        },
        card: {
          DEFAULT: "hsl(var(--card))",
          foreground: "hsl(var(--card-foreground))",
        },
        
        // Warhammer Faction Colors
        faction: {
          empire: {
            50: '#fffbeb',
            100: '#fef3c7',
            200: '#fde68a',
            300: '#fcd34d',
            400: '#fbbf24',
            500: '#f59e0b',
            600: '#d97706',
            700: '#b45309',
            800: '#92400e',
            900: '#78350f',
          },
          chaos: {
            50: '#fef2f2',
            100: '#fee2e2',
            200: '#fecaca',
            300: '#fca5a5',
            400: '#f87171',
            500: '#ef4444',
            600: '#dc2626',
            700: '#b91c1c',
            800: '#991b1b',
            900: '#7f1d1d',
          },
          elves: {
            50: '#f0fdf4',
            100: '#dcfce7',
            200: '#bbf7d0',
            300: '#86efac',
            400: '#4ade80',
            500: '#22c55e',
            600: '#16a34a',
            700: '#15803d',
            800: '#166534',
            900: '#14532d',
          },
          dwarfs: {
            50: '#fffbeb',
            100: '#fef3c7',
            200: '#fde68a',
            300: '#fcd34d',
            400: '#fbbf24',
            500: '#f59e0b',
            600: '#d97706',
            700: '#b45309',
            800: '#92400e',
            900: '#78350f',
          },
          undead: {
            50: '#faf5ff',
            100: '#f3e8ff',
            200: '#e9d5ff',
            300: '#d8b4fe',
            400: '#c084fc',
            500: '#a855f7',
            600: '#9333ea',
            700: '#7c3aed',
            800: '#6b21a8',
            900: '#581c87',
          },
          orcs: {
            50: '#f7fee7',
            100: '#ecfccb',
            200: '#d9f99d',
            300: '#bef264',
            400: '#a3e635',
            500: '#84cc16',
            600: '#65a30d',
            700: '#4d7c0f',
            800: '#365314',
            900: '#1a2e05',
          }
        },
        
        // Tavern Atmosphere Colors
        tavern: {
          wood: {
            50: '#fdf8f6',
            100: '#f2e8e5',
            200: '#eaddd7',
            300: '#e0cec7',
            400: '#d2bab0',
            500: '#bfa094',
            600: '#a18072',
            700: '#977669',
            800: '#846358',
            900: '#43302b',
          },
          stone: {
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
          },
          fire: {
            50: '#fff7ed',
            100: '#ffedd5',
            200: '#fed7aa',
            300: '#fdba74',
            400: '#fb923c',
            500: '#f97316',
            600: '#ea580c',
            700: '#c2410c',
            800: '#9a3412',
            900: '#7c2d12',
          }
        }
      },
      
      fontFamily: {
        'medieval': ['Cinzel', 'serif'],
        'fantasy': ['Uncial Antiqua', 'cursive'],
        'sharp': ['MedievalSharp', 'cursive'],
        'sans': ['Inter', 'sans-serif'],
      },
      
      animation: {
        'flicker': 'flicker 2s ease-in-out infinite',
        'glow-pulse': 'glow-pulse 3s ease-in-out infinite',
        'float': 'float 6s ease-in-out infinite',
        'medieval-entrance': 'medieval-entrance 0.6s cubic-bezier(0.4, 0, 0.2, 1) forwards',
        'gradient-shift': 'gradient-shift 4s ease infinite',
        'fire-flicker': 'fire-flicker 2s ease-in-out infinite alternate',
        'candle-flicker': 'candle-flicker 3s ease-in-out infinite',
        'ember-rise': 'ember-rise 4s ease-in-out infinite',
        'shadow-dance': 'shadow-dance 6s ease-in-out infinite',
        'sparkle': 'sparkle 4s linear infinite',
        'beam-slide': 'beam-slide 2s linear infinite',
        'aurora-shift': 'aurora-shift 8s ease-in-out infinite',
      },
      
      keyframes: {
        flicker: {
          '0%, 100%': { opacity: '1' },
          '50%': { opacity: '0.8' },
        },
        'glow-pulse': {
          '0%, 100%': { 
            textShadow: '0 0 5px rgba(255, 215, 0, 0.5)' 
          },
          '50%': { 
            textShadow: '0 0 20px rgba(255, 215, 0, 0.8), 0 0 30px rgba(255, 215, 0, 0.6)' 
          },
        },
        float: {
          '0%, 100%': { transform: 'translateY(0px)' },
          '50%': { transform: 'translateY(-10px)' },
        },
        'medieval-entrance': {
          '0%': {
            opacity: '0',
            transform: 'translateY(30px) scale(0.9)',
          },
          '100%': {
            opacity: '1',
            transform: 'translateY(0px) scale(1)',
          },
        },
        'gradient-shift': {
          '0%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
          '100%': { backgroundPosition: '0% 50%' },
        },
        'fire-flicker': {
          '0%': {
            boxShadow: '0 0 20px rgba(255, 69, 0, 0.4), 0 0 40px rgba(255, 69, 0, 0.2)'
          },
          '100%': {
            boxShadow: '0 0 30px rgba(255, 69, 0, 0.6), 0 0 50px rgba(255, 69, 0, 0.3)'
          },
        },
        'candle-flicker': {
          '0%, 100%': { opacity: '1', transform: 'scale(1)' },
          '50%': { opacity: '0.8', transform: 'scale(0.98)' },
          '75%': { opacity: '0.9', transform: 'scale(1.02)' }
        },
        'ember-rise': {
          '0%': {
            transform: 'translateY(0px) scale(1)',
            opacity: '0.7'
          },
          '50%': {
            transform: 'translateY(-20px) scale(1.1)',
            opacity: '1'
          },
          '100%': {
            transform: 'translateY(-40px) scale(0.8)',
            opacity: '0'
          }
        },
        'shadow-dance': {
          '0%, 100%': { transform: 'scaleX(1) scaleY(1)' },
          '25%': { transform: 'scaleX(1.1) scaleY(0.9)' },
          '50%': { transform: 'scaleX(0.9) scaleY(1.1)' },
          '75%': { transform: 'scaleX(1.05) scaleY(0.95)' }
        },
        sparkle: {
          '0%': { transform: 'translateY(0px)', opacity: '1' },
          '100%': { transform: 'translateY(-100px)', opacity: '0' },
        },
        'beam-slide': {
          '0%': { left: '-100%' },
          '100%': { left: '100%' },
        },
        'aurora-shift': {
          '0%, 100%': { backgroundPosition: '0% 50%' },
          '50%': { backgroundPosition: '100% 50%' },
        },
      },
      
      borderRadius: {
        lg: "var(--radius)",
        md: "calc(var(--radius) - 2px)",
        sm: "calc(var(--radius) - 4px)",
      },
      
      boxShadow: {
        'tavern': '0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 215, 0, 0.1)',
        'character': '0 10px 25px -5px rgba(0, 0, 0, 0.5), 0 0 0 1px rgba(255, 215, 0, 0.1)',
        'fire': '0 0 20px rgba(255, 69, 0, 0.4), 0 0 40px rgba(255, 69, 0, 0.2)',
        'gold': '0 4px 14px 0 rgba(255, 215, 0, 0.3)',
      },
      
      backdropBlur: {
        'tavern': '12px',
      }
    },
  },
  plugins: [],
}