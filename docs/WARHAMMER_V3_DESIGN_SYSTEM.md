# Warhammer v3 Design System Enhancement Plan
## Inspira UI Integration with Warhammer Aesthetic

### Overview

This document details how to leverage Inspira UI's design system while preserving and enhancing the unique Warhammer Fantasy aesthetic. The goal is to create a cohesive, immersive experience that combines modern UI patterns with medieval fantasy theming.

## Current Warhammer Design Language

### Color Palette Analysis
```css
/* Existing Warhammer Color System */
:root {
  /* Primary Colors */
  --primary-gold: #ffd700;
  --dark-gold: #b8860b;
  
  /* Faction Colors */
  --empire-gold: #ffd700;
  --chaos-red: #8b0000;
  --elves-green: #228b22;
  --dwarfs-bronze: #b8860b;
  
  /* Atmospheric Colors */
  --tavern-wood: #8b4513;
  --tavern-stone: #696969;
  --tavern-fire: #ff4500;
  --tavern-shadow: #2f1b14;
  
  /* UI Colors */
  --secondary-900: #0f172a;
  --secondary-800: #1e293b;
  --secondary-700: #334155;
}
```

### Typography Hierarchy
- **Medieval**: Cinzel (serif) - Headers and titles
- **Fantasy**: Uncial Antiqua (cursive) - Decorative text
- **Sharp**: MedievalSharp (cursive) - Accent text
- **Modern**: Inter (sans-serif) - Body text
- **Code**: JetBrains Mono (monospace) - Technical text

### Visual Elements
- **Textures**: Wood grain, stone, metal
- **Patterns**: Celtic knots, heraldic symbols
- **Effects**: Glowing text, particle effects, shadows
- **Animations**: Flickering flames, floating particles## Inspira UI Design System Integration

### Enhanced Color System
```css
/* Extended Warhammer + Inspira UI Color System */
:root {
  /* Base Inspira UI Variables */
  --background: 47 25 16; /* Dark tavern brown */
  --foreground: 255 215 0; /* Gold text */
  --card: 30 20 10; /* Darker brown cards */
  --card-foreground: 245 245 220; /* Beige text */
  --popover: 20 15 10; /* Very dark brown */
  --popover-foreground: 255 215 0; /* Gold */
  --primary: 255 215 0; /* Empire gold */
  --primary-foreground: 47 25 16; /* Dark brown */
  --secondary: 139 69 19; /* Saddle brown */
  --secondary-foreground: 245 245 220; /* Beige */
  --muted: 74 44 26; /* Muted brown */
  --muted-foreground: 184 134 11; /* Dark gold */
  --accent: 255 69 0; /* Fire orange */
  --accent-foreground: 47 25 16; /* Dark brown */
  --destructive: 139 0 0; /* Chaos red */
  --destructive-foreground: 255 255 255; /* White */
  --border: 139 69 19; /* Saddle brown */
  --input: 74 44 26; /* Muted brown */
  --ring: 255 215 0; /* Gold focus ring */
  
  /* Faction-specific CSS Variables */
  --faction-empire: 255 215 0;
  --faction-chaos: 139 0 0;
  --faction-elves: 34 139 34;
  --faction-dwarfs: 184 134 11;
  --faction-undead: 75 0 130;
  --faction-orcs: 85 107 47;
}
```

### Component Theming Strategy

#### 1. Button Variants
```vue
<!-- Faction-themed Inspira UI buttons -->
<template>
  <!-- Empire Button -->
  <ShimmerButton 
    class="faction-empire bg-gradient-to-r from-yellow-600 to-yellow-400"
    shimmer-color="rgb(255, 215, 0)"
  >
    <span class="font-medieval">Empire Command</span>
  </ShimmerButton>
  
  <!-- Chaos Button -->
  <RippleButton 
    class="faction-chaos bg-gradient-to-r from-red-900 to-red-700"
    ripple-color="rgb(139, 0, 0)"
  >
    <span class="font-medieval text-red-100">Chaos Ritual</span>
  </RippleButton>
  
  <!-- Elves Button -->
  <RainbowButton 
    class="faction-elves"
    colors="['#228b22', '#32cd32', '#90ee90']"
  >
    <span class="font-fantasy">Elven Magic</span>
  </RainbowButton>
</template>
```
#### 2. Card Components
```vue
<!-- Character Cards with Warhammer theming -->
<template>
  <!-- 3D Character Card -->
  <Card3D 
    class="character-card bg-gradient-to-br from-amber-900 to-amber-800"
    :rotation-intensity="15"
  >
    <div class="p-6 space-y-4">
      <div class="flex items-center space-x-3">
        <div class="w-12 h-12 rounded-full bg-gradient-to-r from-yellow-600 to-yellow-400 flex items-center justify-center">
          <Icon name="sword" class="w-6 h-6 text-amber-900" />
        </div>
        <div>
          <h3 class="font-medieval text-lg text-yellow-100">Sir Marcus</h3>
          <p class="text-sm text-amber-300">Empire Knight</p>
        </div>
      </div>
      <div class="space-y-2">
        <div class="flex justify-between">
          <span class="text-amber-200">Strength:</span>
          <span class="text-yellow-100 font-bold">85</span>
        </div>
        <div class="flex justify-between">
          <span class="text-amber-200">Loyalty:</span>
          <span class="text-yellow-100 font-bold">92</span>
        </div>
      </div>
    </div>
  </Card3D>
  
  <!-- Spotlight Card for Important NPCs -->
  <CardSpotlight 
    class="tavern-card bg-gradient-to-br from-stone-800 to-stone-900"
    spotlight-color="rgba(255, 215, 0, 0.3)"
  >
    <div class="p-8">
      <HyperText 
        text="The Mysterious Stranger"
        class="text-2xl font-fantasy text-yellow-100 mb-4"
        animation-duration="2000"
      />
      <p class="text-stone-300 leading-relaxed">
        A hooded figure sits in the corner, nursing a tankard of ale. 
        Their eyes gleam with ancient knowledge...
      </p>
    </div>
  </CardSpotlight>
</template>
```#### 2. Card Components
```vue
<!-- Character Cards with Warhammer theming -->
<template>
  <!-- 3D Character Card -->
  <Card3D 
    class="character-card bg-gradient-to-br from-amber-900 to-amber-800"
    :rotation-intensity="15"
  >
    <div class="p-6 space-y-4">
      <div class="flex items-center space-x-3">
        <div class="w-12 h-12 rounded-full bg-gradient-to-r from-yellow-600 to-yellow-400 flex items-center justify-center">
          <Icon name="sword" class="w-6 h-6 text-amber-900" />
        </div>
        <div>
          <h3 class="font-medieval text-lg text-yellow-100">Sir Marcus</h3>
          <p class="text-sm text-amber-300">Empire Knight</p>
        </div>
      </div>
      <div class="space-y-2">
        <div class="flex justify-between">
          <span class="text-amber-200">Strength:</span>
          <span class="text-yellow-100 font-bold">85</span>
        </div>
        <div class="flex justify-between">
          <span class="text-amber-200">Loyalty:</span>
          <span class="text-yellow-100 font-bold">92</span>
        </div>
      </div>
    </div>
  </Card3D>
  
  <!-- Spotlight Card for Important NPCs -->
  <CardSpotlight 
    class="tavern-card bg-gradient-to-br from-stone-800 to-stone-900"
    spotlight-color="rgba(255, 215, 0, 0.3)"
  >
    <div class="p-8">
      <HyperText 
        text="The Mysterious Stranger"
        class="text-2xl font-fantasy text-yellow-100 mb-4"
        animation-duration="2000"
      />
      <p class="text-stone-300 leading-relaxed">
        A hooded figure sits in the corner, nursing a tankard of ale. 
        Their eyes gleam with ancient knowledge...
      </p>
    </div>
  </CardSpotlight>
</template>
```