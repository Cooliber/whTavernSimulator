<template>
  <div class="accessibility-panel wh-card p-6 space-y-6">
    <div class="flex items-center justify-between">
      <h3 class="wh-title text-xl">Accessibility Settings</h3>
      <Icon name="accessibility" class="w-6 h-6 text-wh-empire-gold" />
    </div>
    
    <!-- Visual Preferences -->
    <div class="visual-section space-y-4">
      <h4 class="wh-subtitle text-lg">Visual Preferences</h4>
      
      <!-- High Contrast Mode -->
      <div class="preference-item flex items-center justify-between p-3 rounded-lg bg-wh-dark-grey/30">
        <div class="flex-1">
          <label for="high-contrast" class="block text-sm font-medieval text-wh-parchment">
            High Contrast Mode
          </label>
          <p class="text-xs text-wh-aged-paper mt-1">
            Increases contrast for better visibility
          </p>
        </div>
        <button
          id="high-contrast"
          class="toggle-switch"
          :class="{ 'active': highContrastMode }"
          :aria-pressed="highContrastMode"
          role="switch"
          @click="toggleHighContrast"
        >
          <span class="toggle-slider" :class="{ 'translate-x-6': highContrastMode }"></span>
          <span class="sr-only">{{ highContrastMode ? 'Disable' : 'Enable' }} high contrast mode</span>
        </button>
      </div>
      
      <!-- Font Size -->
      <div class="preference-item p-3 rounded-lg bg-wh-dark-grey/30">
        <label for="font-size" class="block text-sm font-medieval text-wh-parchment mb-2">
          Font Size
        </label>
        <div class="flex items-center space-x-4">
          <button
            class="wh-btn wh-btn-secondary text-xs px-3 py-1"
            @click="decreaseFontSize"
            :disabled="fontSize <= 12"
            aria-label="Decrease font size"
          >
            A-
          </button>
          <span class="text-sm text-wh-parchment min-w-[60px] text-center">{{ fontSize }}px</span>
          <button
            class="wh-btn wh-btn-secondary text-xs px-3 py-1"
            @click="increaseFontSize"
            :disabled="fontSize >= 24"
            aria-label="Increase font size"
          >
            A+
          </button>
        </div>
        <input
          id="font-size"
          v-model="fontSize"
          type="range"
          min="12"
          max="24"
          step="1"
          class="wh-slider w-full mt-2"
          @input="updateFontSize"
          aria-label="Font size slider"
        />
      </div>
      
      <!-- Color Theme -->
      <div class="preference-item p-3 rounded-lg bg-wh-dark-grey/30">
        <label class="block text-sm font-medieval text-wh-parchment mb-3">
          Color Theme
        </label>
        <div class="grid grid-cols-3 gap-2">
          <button
            v-for="theme in colorThemes"
            :key="theme.id"
            class="theme-option p-2 rounded-md border-2 transition-all"
            :class="{
              'border-wh-empire-gold': selectedTheme === theme.id,
              'border-wh-iron-grey': selectedTheme !== theme.id
            }"
            :style="{ backgroundColor: theme.primary, color: theme.text }"
            @click="selectTheme(theme.id)"
            :aria-label="`Select ${theme.name} theme`"
            :aria-pressed="selectedTheme === theme.id"
          >
            <div class="text-xs font-medieval">{{ theme.name }}</div>
          </button>
        </div>
      </div>
    </div>
    
    <!-- Motion Preferences -->
    <div class="motion-section space-y-4">
      <h4 class="wh-subtitle text-lg">Motion & Animation</h4>
      
      <!-- Reduced Motion -->
      <div class="preference-item flex items-center justify-between p-3 rounded-lg bg-wh-dark-grey/30">
        <div class="flex-1">
          <label for="reduced-motion" class="block text-sm font-medieval text-wh-parchment">
            Reduce Motion
          </label>
          <p class="text-xs text-wh-aged-paper mt-1">
            Minimizes animations and transitions
          </p>
        </div>
        <button
          id="reduced-motion"
          class="toggle-switch"
          :class="{ 'active': prefersReducedMotion }"
          :aria-pressed="prefersReducedMotion"
          role="switch"
          @click="toggleReducedMotion"
        >
          <span class="toggle-slider" :class="{ 'translate-x-6': prefersReducedMotion }"></span>
          <span class="sr-only">{{ prefersReducedMotion ? 'Enable' : 'Disable' }} animations</span>
        </button>
      </div>
      
      <!-- Animation Speed -->
      <div class="preference-item p-3 rounded-lg bg-wh-dark-grey/30">
        <label for="animation-speed" class="block text-sm font-medieval text-wh-parchment mb-2">
          Animation Speed
        </label>
        <div class="flex items-center space-x-4">
          <span class="text-xs text-wh-aged-paper">Slow</span>
          <input
            id="animation-speed"
            v-model="animationSpeed"
            type="range"
            min="0.5"
            max="2"
            step="0.1"
            class="wh-slider flex-1"
            :disabled="prefersReducedMotion"
            @input="updateAnimationSpeed"
            aria-label="Animation speed slider"
          />
          <span class="text-xs text-wh-aged-paper">Fast</span>
        </div>
        <div class="text-center mt-1">
          <span class="text-xs text-wh-parchment">{{ animationSpeed }}x</span>
        </div>
      </div>
    </div>
    
    <!-- Audio Preferences -->
    <div class="audio-section space-y-4">
      <h4 class="wh-subtitle text-lg">Audio & Sound</h4>
      
      <!-- Sound Effects -->
      <div class="preference-item flex items-center justify-between p-3 rounded-lg bg-wh-dark-grey/30">
        <div class="flex-1">
          <label for="sound-effects" class="block text-sm font-medieval text-wh-parchment">
            Sound Effects
          </label>
          <p class="text-xs text-wh-aged-paper mt-1">
            UI interaction sounds and feedback
          </p>
        </div>
        <button
          id="sound-effects"
          class="toggle-switch"
          :class="{ 'active': soundEffectsEnabled }"
          :aria-pressed="soundEffectsEnabled"
          role="switch"
          @click="toggleSoundEffects"
        >
          <span class="toggle-slider" :class="{ 'translate-x-6': soundEffectsEnabled }"></span>
          <span class="sr-only">{{ soundEffectsEnabled ? 'Disable' : 'Enable' }} sound effects</span>
        </button>
      </div>
      
      <!-- Screen Reader Announcements -->
      <div class="preference-item flex items-center justify-between p-3 rounded-lg bg-wh-dark-grey/30">
        <div class="flex-1">
          <label for="screen-reader" class="block text-sm font-medieval text-wh-parchment">
            Enhanced Screen Reader Support
          </label>
          <p class="text-xs text-wh-aged-paper mt-1">
            Additional announcements and descriptions
          </p>
        </div>
        <button
          id="screen-reader"
          class="toggle-switch"
          :class="{ 'active': enhancedScreenReader }"
          :aria-pressed="enhancedScreenReader"
          role="switch"
          @click="toggleScreenReader"
        >
          <span class="toggle-slider" :class="{ 'translate-x-6': enhancedScreenReader }"></span>
          <span class="sr-only">{{ enhancedScreenReader ? 'Disable' : 'Enable' }} enhanced screen reader support</span>
        </button>
      </div>
    </div>
    
    <!-- Keyboard Navigation -->
    <div class="keyboard-section space-y-4">
      <h4 class="wh-subtitle text-lg">Keyboard & Navigation</h4>
      
      <!-- Focus Indicators -->
      <div class="preference-item flex items-center justify-between p-3 rounded-lg bg-wh-dark-grey/30">
        <div class="flex-1">
          <label for="focus-indicators" class="block text-sm font-medieval text-wh-parchment">
            Enhanced Focus Indicators
          </label>
          <p class="text-xs text-wh-aged-paper mt-1">
            More visible keyboard focus outlines
          </p>
        </div>
        <button
          id="focus-indicators"
          class="toggle-switch"
          :class="{ 'active': enhancedFocus }"
          :aria-pressed="enhancedFocus"
          role="switch"
          @click="toggleEnhancedFocus"
        >
          <span class="toggle-slider" :class="{ 'translate-x-6': enhancedFocus }"></span>
          <span class="sr-only">{{ enhancedFocus ? 'Disable' : 'Enable' }} enhanced focus indicators</span>
        </button>
      </div>
      
      <!-- Skip Links -->
      <div class="preference-item p-3 rounded-lg bg-wh-dark-grey/30">
        <div class="text-sm font-medieval text-wh-parchment mb-2">Keyboard Shortcuts</div>
        <div class="space-y-1 text-xs text-wh-aged-paper">
          <div>• <kbd class="kbd">Tab</kbd> - Navigate forward</div>
          <div>• <kbd class="kbd">Shift + Tab</kbd> - Navigate backward</div>
          <div>• <kbd class="kbd">Enter</kbd> or <kbd class="kbd">Space</kbd> - Activate buttons</div>
          <div>• <kbd class="kbd">Escape</kbd> - Close dialogs/menus</div>
          <div>• <kbd class="kbd">Arrow Keys</kbd> - Navigate within components</div>
        </div>
      </div>
    </div>
    
    <!-- Reset and Save -->
    <div class="actions-section flex space-x-4">
      <button
        class="wh-btn wh-btn-secondary flex-1"
        @click="resetToDefaults"
        aria-label="Reset all accessibility settings to defaults"
      >
        <Icon name="refresh-cw" class="w-4 h-4 mr-2" />
        Reset to Defaults
      </button>
      
      <button
        class="wh-btn wh-btn-primary flex-1"
        @click="saveSettings"
        aria-label="Save accessibility settings"
      >
        <Icon name="save" class="w-4 h-4 mr-2" />
        Save Settings
      </button>
    </div>
    
    <!-- Live Region for Announcements -->
    <div
      id="accessibility-announcements"
      class="sr-only"
      aria-live="polite"
      aria-atomic="true"
    >
      {{ announcement }}
    </div>
  </div>
</template>

<script setup lang="ts">
interface ColorTheme {
  id: string
  name: string
  primary: string
  text: string
}

// Props
interface Props {
  modelValue?: boolean
}

const props = withDefaults(defineProps<Props>(), {
  modelValue: false
})

// Emits
const emit = defineEmits<{
  'update:modelValue': [value: boolean]
  'settings-changed': [settings: AccessibilitySettings]
}>()

interface AccessibilitySettings {
  highContrastMode: boolean
  prefersReducedMotion: boolean
  fontSize: number
  selectedTheme: string
  animationSpeed: number
  soundEffectsEnabled: boolean
  enhancedScreenReader: boolean
  enhancedFocus: boolean
}

// Reactive state
const highContrastMode = ref(false)
const prefersReducedMotion = ref(false)
const fontSize = ref(16)
const selectedTheme = ref('default')
const animationSpeed = ref(1)
const soundEffectsEnabled = ref(true)
const enhancedScreenReader = ref(false)
const enhancedFocus = ref(false)
const announcement = ref('')

// Color themes
const colorThemes: ColorTheme[] = [
  { id: 'default', name: 'Default', primary: '#8b4513', text: '#f4f1e8' },
  { id: 'high-contrast', name: 'High Contrast', primary: '#000000', text: '#ffffff' },
  { id: 'dark', name: 'Dark', primary: '#1a1a1a', text: '#e8dcc0' },
  { id: 'light', name: 'Light', primary: '#f4f1e8', text: '#1a1a1a' },
  { id: 'sepia', name: 'Sepia', primary: '#f4ecd8', text: '#5d4e37' },
  { id: 'blue', name: 'Blue', primary: '#1e3a8a', text: '#dbeafe' }
]

// Methods
const toggleHighContrast = () => {
  highContrastMode.value = !highContrastMode.value
  announce(`High contrast mode ${highContrastMode.value ? 'enabled' : 'disabled'}`)
  saveToStorage()
  emitSettingsChange()
}

const toggleReducedMotion = () => {
  prefersReducedMotion.value = !prefersReducedMotion.value
  announce(`Animations ${prefersReducedMotion.value ? 'reduced' : 'enabled'}`)
  saveToStorage()
  emitSettingsChange()
}

const increaseFontSize = () => {
  if (fontSize.value < 24) {
    fontSize.value += 1
    updateFontSize()
  }
}

const decreaseFontSize = () => {
  if (fontSize.value > 12) {
    fontSize.value -= 1
    updateFontSize()
  }
}

const updateFontSize = () => {
  document.documentElement.style.fontSize = `${fontSize.value}px`
  announce(`Font size changed to ${fontSize.value} pixels`)
  saveToStorage()
  emitSettingsChange()
}

const selectTheme = (themeId: string) => {
  selectedTheme.value = themeId
  const theme = colorThemes.find(t => t.id === themeId)
  if (theme) {
    announce(`${theme.name} theme selected`)
  }
  saveToStorage()
  emitSettingsChange()
}

const updateAnimationSpeed = () => {
  document.documentElement.style.setProperty('--animation-speed', animationSpeed.value.toString())
  announce(`Animation speed set to ${animationSpeed.value}x`)
  saveToStorage()
  emitSettingsChange()
}

const toggleSoundEffects = () => {
  soundEffectsEnabled.value = !soundEffectsEnabled.value
  announce(`Sound effects ${soundEffectsEnabled.value ? 'enabled' : 'disabled'}`)
  saveToStorage()
  emitSettingsChange()
}

const toggleScreenReader = () => {
  enhancedScreenReader.value = !enhancedScreenReader.value
  announce(`Enhanced screen reader support ${enhancedScreenReader.value ? 'enabled' : 'disabled'}`)
  saveToStorage()
  emitSettingsChange()
}

const toggleEnhancedFocus = () => {
  enhancedFocus.value = !enhancedFocus.value
  announce(`Enhanced focus indicators ${enhancedFocus.value ? 'enabled' : 'disabled'}`)
  saveToStorage()
  emitSettingsChange()
}

const resetToDefaults = () => {
  highContrastMode.value = false
  prefersReducedMotion.value = false
  fontSize.value = 16
  selectedTheme.value = 'default'
  animationSpeed.value = 1
  soundEffectsEnabled.value = true
  enhancedScreenReader.value = false
  enhancedFocus.value = false
  
  // Reset DOM changes
  document.documentElement.style.fontSize = '16px'
  document.documentElement.style.setProperty('--animation-speed', '1')
  
  announce('All accessibility settings reset to defaults')
  saveToStorage()
  emitSettingsChange()
}

const saveSettings = () => {
  saveToStorage()
  announce('Accessibility settings saved')
}

const announce = (message: string) => {
  announcement.value = message
  // Clear after a delay to allow for new announcements
  setTimeout(() => {
    announcement.value = ''
  }, 1000)
}

const saveToStorage = () => {
  if (typeof window !== 'undefined') {
    const settings: AccessibilitySettings = {
      highContrastMode: highContrastMode.value,
      prefersReducedMotion: prefersReducedMotion.value,
      fontSize: fontSize.value,
      selectedTheme: selectedTheme.value,
      animationSpeed: animationSpeed.value,
      soundEffectsEnabled: soundEffectsEnabled.value,
      enhancedScreenReader: enhancedScreenReader.value,
      enhancedFocus: enhancedFocus.value
    }
    
    localStorage.setItem('accessibility-settings', JSON.stringify(settings))
  }
}

const loadFromStorage = () => {
  if (typeof window !== 'undefined') {
    const saved = localStorage.getItem('accessibility-settings')
    if (saved) {
      try {
        const settings: AccessibilitySettings = JSON.parse(saved)
        
        highContrastMode.value = settings.highContrastMode
        prefersReducedMotion.value = settings.prefersReducedMotion
        fontSize.value = settings.fontSize
        selectedTheme.value = settings.selectedTheme
        animationSpeed.value = settings.animationSpeed
        soundEffectsEnabled.value = settings.soundEffectsEnabled
        enhancedScreenReader.value = settings.enhancedScreenReader
        enhancedFocus.value = settings.enhancedFocus
        
        // Apply settings to DOM
        document.documentElement.style.fontSize = `${fontSize.value}px`
        document.documentElement.style.setProperty('--animation-speed', animationSpeed.value.toString())
        
        emitSettingsChange()
      } catch (error) {
        console.warn('Failed to load accessibility settings:', error)
      }
    }
  }
}

const emitSettingsChange = () => {
  const settings: AccessibilitySettings = {
    highContrastMode: highContrastMode.value,
    prefersReducedMotion: prefersReducedMotion.value,
    fontSize: fontSize.value,
    selectedTheme: selectedTheme.value,
    animationSpeed: animationSpeed.value,
    soundEffectsEnabled: soundEffectsEnabled.value,
    enhancedScreenReader: enhancedScreenReader.value,
    enhancedFocus: enhancedFocus.value
  }
  
  emit('settings-changed', settings)
}

// Lifecycle
onMounted(() => {
  loadFromStorage()
})
</script>

<style scoped>
/* Toggle Switch Styles */
.toggle-switch {
  position: relative;
  width: 48px;
  height: 24px;
  background-color: var(--wh-iron-grey);
  border-radius: 12px;
  transition: background-color 0.3s ease;
  border: none;
  cursor: pointer;
  outline: none;
}

.toggle-switch:focus {
  box-shadow: 0 0 0 2px var(--wh-empire-gold);
}

.toggle-switch.active {
  background-color: var(--wh-empire-gold);
}

.toggle-slider {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}

/* Keyboard shortcut styling */
.kbd {
  background-color: var(--wh-grey);
  border: 1px solid var(--wh-iron-grey);
  border-radius: 3px;
  padding: 2px 4px;
  font-family: monospace;
  font-size: 0.75rem;
  color: var(--wh-parchment);
}

/* Theme option styling */
.theme-option {
  min-height: 44px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
}

.theme-option:hover {
  transform: scale(1.05);
}

.theme-option:focus {
  outline: 2px solid var(--wh-empire-gold);
  outline-offset: 2px;
}

/* Preference item hover effects */
.preference-item {
  transition: background-color 0.2s ease;
}

.preference-item:hover {
  background-color: var(--wh-grey);
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .actions-section {
    flex-direction: column;
    space-x: 0;
    gap: 1rem;
  }
  
  .grid-cols-3 {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
