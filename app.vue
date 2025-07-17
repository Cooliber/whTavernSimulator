<template>
  <div>
    <NuxtLayout>
      <NuxtPage />
    </NuxtLayout>
  </div>
</template>

<script setup lang="ts">
import { useHead } from '#app';
import { onErrorCaptured } from 'vue';
// Import CSS files directly to avoid path resolution issues
import './assets/css/main.css'
import './assets/css/warhammer-theme.css'
import './assets/css/inspira-ui.css'

// Page metadata
useHead({
  title: 'Warhammer Tavern Simulator v3',
  meta: [
    { name: 'description', content: 'Immersive Warhammer Fantasy Tavern Simulator with AI-powered NPCs and advanced atmospheric systems' },
    { name: 'keywords', content: 'warhammer, fantasy, tavern, simulator, rpg, ai, npc, atmospheric' },
    { name: 'author', content: 'Warhammer Tavern Simulator Team' },
    { property: 'og:title', content: 'Warhammer Tavern Simulator v3' },
    { property: 'og:description', content: 'Experience the ultimate fantasy tavern simulation with dynamic weather, lighting, and AI-powered characters' },
    { property: 'og:type', content: 'website' },
    { name: 'twitter:card', content: 'summary_large_image' },
    { name: 'twitter:title', content: 'Warhammer Tavern Simulator v3' },
    { name: 'twitter:description', content: 'Immersive fantasy tavern experience with advanced atmospheric systems' }
  ],
  link: [
    { rel: 'icon', type: 'image/x-icon', href: '/favicon.ico' },
    { rel: 'canonical', href: 'https://warhammer-tavern-simulator.com' }
  ]
})

// Global error handling
onErrorCaptured((error) => {
  console.error('Global error captured:', error)
  return false
})
</script>

<style>
/* Global styles that need to be available everywhere */
html {
  scroll-behavior: smooth;
}

body {
  margin: 0;
  padding: 0;
  overflow-x: hidden;
}

/* Ensure proper font loading */
.font-medieval {
  font-family: 'Cinzel', serif;
}

.font-fantasy {
  font-family: 'Uncial Antiqua', cursive;
}

.font-sharp {
  font-family: 'MedievalSharp', cursive;
}

/* Performance optimizations */
* {
  box-sizing: border-box;
}

/* Smooth transitions for better UX */
*,
*::before,
*::after {
  transition-property: color, background-color, border-color, text-decoration-color, fill, stroke, opacity, box-shadow, transform, filter, backdrop-filter;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
  transition-duration: 150ms;
}

/* Accessibility improvements */
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}

/* Focus styles for better accessibility */
:focus-visible {
  outline: 2px solid #ffd700;
  outline-offset: 2px;
}

/* Loading states */
.loading {
  opacity: 0.7;
  pointer-events: none;
}

/* Error states */
.error {
  color: #ef4444;
  border-color: #ef4444;
}

/* Success states */
.success {
  color: #10b981;
  border-color: #10b981;
}
</style>
