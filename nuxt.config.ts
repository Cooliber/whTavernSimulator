// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  compatibilityDate: '2025-07-15',
  devtools: { enabled: true },

  // Modules for Warhammer Tavern v3 with Inspira UI
  modules: [
    '@nuxtjs/tailwindcss',
    '@pinia/nuxt',
    '@vueuse/nuxt',
    '@nuxtjs/google-fonts'
  ],

  // Auto-import components
  components: [
    {
      path: '~/components',
      pathPrefix: false,
    },
  ],

  // CSS Configuration - Removed to fix path resolution issues
  // CSS files are now imported in app.vue
  css: [],

  // Google Fonts for Warhammer theming
  googleFonts: {
    families: {
      'Cinzel': [400, 500, 600, 700],
      'Uncial Antiqua': [400],
      'MedievalSharp': [400],
      'Inter': [300, 400, 500, 600, 700]
    },
    display: 'swap',
    preload: true
  },

  // TypeScript configuration
  typescript: {
    strict: true,
    typeCheck: false // Disabled for faster development
  },

  // Development server configuration
  devServer: {
    port: 5920,
    host: '0.0.0.0'
  },

  // Nitro configuration for server
  nitro: {
    devServer: {
      port: 5920,
      host: '0.0.0.0'
    }
  },

  // Vite configuration for optimizations
  vite: {
    optimizeDeps: {
      include: ['gsap', 'three', 'framer-motion']
    },
    server: {
      port: 5920,
      host: '0.0.0.0'
    }
  },

  // App configuration
  app: {
    head: {
      title: 'Warhammer Tavern Simulator v3',
      meta: [
        { charset: 'utf-8' },
        { name: 'viewport', content: 'width=device-width, initial-scale=1' },
        { name: 'description', content: 'Immersive Warhammer Fantasy Tavern Simulator with AI-powered NPCs' }
      ]
    }
  },

  // Runtime configuration
  runtimeConfig: {
    public: {
      apiBase: process.env.API_BASE || 'http://localhost:8000'
    }
  }
})
