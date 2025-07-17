<template>
  <div class="space-y-8">
    <!-- Header -->
    <section class="text-center space-y-4">
      <HyperText 
        text="Tavern Settings"
        class="text-4xl font-medieval text-foreground"
        :animation-duration="1500"
      />
      <p class="text-muted-foreground max-w-2xl mx-auto">
        Customize your Warhammer Fantasy tavern experience to your preferences
      </p>
    </section>

    <!-- Settings Categories -->
    <div class="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-8">
      <!-- Accessibility Settings -->
      <div class="lg:col-span-2 xl:col-span-1">
        <AccessibilityPanel
          @settings-changed="handleAccessibilityChange"
        />
      </div>
      <!-- Audio Settings -->
      <Card3D class="inspira-card-tavern p-6" :rotation-intensity="5">
        <div class="space-y-6">
          <div class="flex items-center space-x-3">
            <Icon name="volume-2" class="w-6 h-6 text-primary" />
            <h3 class="text-xl font-medieval text-foreground">Audio Settings</h3>
          </div>
          
          <div class="space-y-4">
            <div class="space-y-2">
              <label class="text-sm font-medieval text-foreground">Master Volume</label>
              <input 
                v-model="settings.audio.masterVolume"
                type="range" 
                min="0" 
                max="100" 
                class="w-full accent-primary"
              />
              <div class="flex justify-between text-xs text-muted-foreground">
                <span>0%</span>
                <span>{{ settings.audio.masterVolume }}%</span>
                <span>100%</span>
              </div>
            </div>
            
            <div class="space-y-2">
              <label class="text-sm font-medieval text-foreground">Ambient Sounds</label>
              <input 
                v-model="settings.audio.ambientVolume"
                type="range" 
                min="0" 
                max="100" 
                class="w-full accent-primary"
              />
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm font-medieval text-foreground">Spatial Audio</span>
              <input 
                v-model="settings.audio.spatialAudio"
                type="checkbox" 
                class="accent-primary"
              />
            </div>
          </div>
        </div>
      </Card3D>

      <!-- Visual Settings -->
      <Card3D class="inspira-card-tavern p-6" :rotation-intensity="5">
        <div class="space-y-6">
          <div class="flex items-center space-x-3">
            <Icon name="eye" class="w-6 h-6 text-primary" />
            <h3 class="text-xl font-medieval text-foreground">Visual Settings</h3>
          </div>
          
          <div class="space-y-4">
            <div class="space-y-2">
              <label class="text-sm font-medieval text-foreground">Animation Quality</label>
              <select 
                v-model="settings.visual.animationQuality"
                class="w-full p-2 rounded bg-background border border-border text-foreground"
              >
                <option value="low">Low</option>
                <option value="medium">Medium</option>
                <option value="high">High</option>
                <option value="ultra">Ultra</option>
              </select>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm font-medieval text-foreground">Particle Effects</span>
              <input 
                v-model="settings.visual.particleEffects"
                type="checkbox" 
                class="accent-primary"
              />
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm font-medieval text-foreground">Reduced Motion</span>
              <input 
                v-model="settings.visual.reducedMotion"
                type="checkbox" 
                class="accent-primary"
              />
            </div>
          </div>
        </div>
      </Card3D>

      <!-- Gameplay Settings -->
      <Card3D class="inspira-card-tavern p-6" :rotation-intensity="5">
        <div class="space-y-6">
          <div class="flex items-center space-x-3">
            <Icon name="gamepad-2" class="w-6 h-6 text-primary" />
            <h3 class="text-xl font-medieval text-foreground">Gameplay Settings</h3>
          </div>
          
          <div class="space-y-4">
            <div class="space-y-2">
              <label class="text-sm font-medieval text-foreground">Difficulty Level</label>
              <select 
                v-model="settings.gameplay.difficulty"
                class="w-full p-2 rounded bg-background border border-border text-foreground"
              >
                <option value="easy">Easy</option>
                <option value="normal">Normal</option>
                <option value="hard">Hard</option>
                <option value="nightmare">Nightmare</option>
              </select>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm font-medieval text-foreground">Auto-Save</span>
              <input 
                v-model="settings.gameplay.autoSave"
                type="checkbox" 
                class="accent-primary"
              />
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm font-medieval text-foreground">Tutorial Tips</span>
              <input 
                v-model="settings.gameplay.tutorialTips"
                type="checkbox" 
                class="accent-primary"
              />
            </div>
          </div>
        </div>
      </Card3D>

      <!-- Accessibility Settings -->
      <Card3D class="inspira-card-tavern p-6" :rotation-intensity="5">
        <div class="space-y-6">
          <div class="flex items-center space-x-3">
            <Icon name="accessibility" class="w-6 h-6 text-primary" />
            <h3 class="text-xl font-medieval text-foreground">Accessibility</h3>
          </div>
          
          <div class="space-y-4">
            <div class="space-y-2">
              <label class="text-sm font-medieval text-foreground">Font Size</label>
              <select 
                v-model="settings.accessibility.fontSize"
                class="w-full p-2 rounded bg-background border border-border text-foreground"
              >
                <option value="small">Small</option>
                <option value="medium">Medium</option>
                <option value="large">Large</option>
                <option value="extra-large">Extra Large</option>
              </select>
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm font-medieval text-foreground">High Contrast</span>
              <input 
                v-model="settings.accessibility.highContrast"
                type="checkbox" 
                class="accent-primary"
              />
            </div>
            
            <div class="flex items-center justify-between">
              <span class="text-sm font-medieval text-foreground">Screen Reader Support</span>
              <input 
                v-model="settings.accessibility.screenReader"
                type="checkbox" 
                class="accent-primary"
              />
            </div>
          </div>
        </div>
      </Card3D>
    </div>

    <!-- Action Buttons -->
    <div class="flex flex-col sm:flex-row gap-4 justify-center items-center pt-8">
      <RippleButton 
        class="faction-empire px-8 py-3 text-lg font-medieval"
        ripple-color="rgb(255, 215, 0)"
        @click="saveSettings"
      >
        Save Settings
      </RippleButton>
      
      <ShimmerButton 
        class="px-8 py-3 text-lg font-medieval bg-secondary text-secondary-foreground"
        shimmer-color="rgb(139, 69, 19)"
        @click="resetSettings"
      >
        Reset to Defaults
      </ShimmerButton>
    </div>
  </div>
</template>

<script setup lang="ts">
// Page metadata
useHead({
  title: 'Settings - Warhammer Tavern Simulator v3',
  meta: [
    { name: 'description', content: 'Customize your Warhammer Fantasy tavern experience with audio, visual, gameplay, and accessibility settings.' }
  ]
})

// Settings state
const settings = ref({
  audio: {
    masterVolume: 75,
    ambientVolume: 60,
    spatialAudio: true
  },
  visual: {
    animationQuality: 'high',
    particleEffects: true,
    reducedMotion: false
  },
  gameplay: {
    difficulty: 'normal',
    autoSave: true,
    tutorialTips: true
  },
  accessibility: {
    fontSize: 'medium',
    highContrast: false,
    screenReader: false
  }
})

// Methods
const saveSettings = () => {
  // Save settings to localStorage or API
  localStorage.setItem('warhammer-tavern-settings', JSON.stringify(settings.value))
  
  // Show success notification
  console.log('Settings saved successfully!')
  
  // Apply settings immediately
  applySettings()
}

const resetSettings = () => {
  // Reset to default values
  settings.value = {
    audio: {
      masterVolume: 75,
      ambientVolume: 60,
      spatialAudio: true
    },
    visual: {
      animationQuality: 'high',
      particleEffects: true,
      reducedMotion: false
    },
    gameplay: {
      difficulty: 'normal',
      autoSave: true,
      tutorialTips: true
    },
    accessibility: {
      fontSize: 'medium',
      highContrast: false,
      screenReader: false
    }
  }
  
  console.log('Settings reset to defaults!')
}

const applySettings = () => {
  // Apply visual settings
  if (settings.value.accessibility.highContrast) {
    document.documentElement.classList.add('high-contrast')
  } else {
    document.documentElement.classList.remove('high-contrast')
  }
  
  // Apply font size
  document.documentElement.setAttribute('data-font-size', settings.value.accessibility.fontSize)
  
  // Apply reduced motion
  if (settings.value.visual.reducedMotion) {
    document.documentElement.classList.add('reduce-motion')
  } else {
    document.documentElement.classList.remove('reduce-motion')
  }
}

const loadSettings = () => {
  const savedSettings = localStorage.getItem('warhammer-tavern-settings')
  if (savedSettings) {
    try {
      settings.value = { ...settings.value, ...JSON.parse(savedSettings) }
    } catch (error) {
      console.error('Failed to load settings:', error)
    }
  }
}

// Accessibility settings handler
const handleAccessibilityChange = (accessibilitySettings: any) => {
  console.log('Accessibility settings changed:', accessibilitySettings)

  // Apply accessibility settings to the application
  if (typeof document !== 'undefined') {
    // Apply high contrast mode
    if (accessibilitySettings.highContrastMode) {
      document.documentElement.classList.add('high-contrast')
    } else {
      document.documentElement.classList.remove('high-contrast')
    }

    // Apply reduced motion
    if (accessibilitySettings.prefersReducedMotion) {
      document.documentElement.classList.add('reduce-motion')
    } else {
      document.documentElement.classList.remove('reduce-motion')
    }

    // Apply font size
    document.documentElement.style.fontSize = `${accessibilitySettings.fontSize}px`

    // Apply animation speed
    document.documentElement.style.setProperty('--animation-speed', accessibilitySettings.animationSpeed.toString())
  }

  // Save to settings
  settings.value.accessibility = accessibilitySettings
  saveSettings()
}

// Lifecycle
onMounted(() => {
  loadSettings()
  applySettings()
})
</script>

<style scoped>
/* Component-specific styles */
input[type="range"] {
  height: 6px;
  border-radius: 3px;
  background: rgba(255, 255, 255, 0.1);
  outline: none;
}

input[type="range"]::-webkit-slider-thumb {
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ffd700;
  cursor: pointer;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

input[type="range"]::-moz-range-thumb {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ffd700;
  cursor: pointer;
  border: none;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);
}

select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}
</style>
