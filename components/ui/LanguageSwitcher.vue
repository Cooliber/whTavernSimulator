<template>
  <div class="relative">
    <button
      @click="toggleDropdown"
      @keydown.escape="closeDropdown"
      class="flex items-center space-x-2 px-3 py-2 rounded-lg bg-background/50 border border-border hover:bg-background/80 transition-colors duration-200 focus:outline-none focus:ring-2 focus:ring-primary focus:ring-offset-2"
      :aria-label="$t('accessibility.languageSelector')"
      :aria-expanded="isOpen"
      aria-haspopup="true"
    >
      <Icon name="globe" class="w-4 h-4 text-muted-foreground" />
      <span class="text-sm font-medieval text-foreground">{{ currentLocale.name }}</span>
      <Icon 
        name="chevron-down" 
        class="w-4 h-4 text-muted-foreground transition-transform duration-200"
        :class="{ 'rotate-180': isOpen }"
      />
    </button>

    <Transition
      enter-active-class="transition ease-out duration-200"
      enter-from-class="opacity-0 scale-95"
      enter-to-class="opacity-100 scale-100"
      leave-active-class="transition ease-in duration-150"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-95"
    >
      <div
        v-if="isOpen"
        class="absolute right-0 mt-2 w-48 bg-background border border-border rounded-lg shadow-lg z-50"
        role="menu"
        :aria-label="$t('accessibility.languageSelector')"
      >
        <div class="py-1">
          <button
            v-for="locale in availableLocales"
            :key="locale.code"
            @click="switchLanguage(locale.code)"
            class="w-full text-left px-4 py-2 text-sm font-medieval text-foreground hover:bg-primary/10 transition-colors duration-200 focus:outline-none focus:bg-primary/10"
            :class="{ 'bg-primary/20 text-primary': locale.code === currentLocale.code }"
            role="menuitem"
          >
            <div class="flex items-center space-x-3">
              <span class="text-lg">{{ locale.flag }}</span>
              <div>
                <div class="font-medium">{{ locale.name }}</div>
                <div class="text-xs text-muted-foreground">{{ locale.nativeName }}</div>
              </div>
            </div>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
// Composables
const { locale, locales } = useI18n()

// State
const isOpen = ref(false)

// Computed
const availableLocales = computed(() => [
  {
    code: 'pl',
    name: 'Polski',
    nativeName: 'Polish',
    flag: '🇵🇱'
  },
  {
    code: 'en',
    name: 'English',
    nativeName: 'English',
    flag: '🇺🇸'
  }
])

const currentLocale = computed(() => {
  return availableLocales.value.find(l => l.code === locale.value) || availableLocales.value[0]
})

// Methods
const toggleDropdown = () => {
  isOpen.value = !isOpen.value
}

const closeDropdown = () => {
  isOpen.value = false
}

const switchLanguage = async (newLocale: string) => {
  await navigateTo(switchLocalePath(newLocale))
  closeDropdown()
}

// Close dropdown when clicking outside
onClickOutside(templateRef, closeDropdown)

// Close dropdown on route change
watch(() => locale.value, () => {
  closeDropdown()
})
</script>

<style scoped>
/* Additional styles for enhanced accessibility */
@media (prefers-reduced-motion: reduce) {
  .transition {
    transition: none !important;
  }
}

/* High contrast mode support */
@media (prefers-contrast: high) {
  button {
    border-width: 2px;
  }
  
  .bg-primary\/10:hover {
    background-color: var(--primary) !important;
    color: var(--primary-foreground) !important;
  }
}

/* Focus improvements for keyboard navigation */
button:focus-visible {
  outline: 2px solid var(--primary);
  outline-offset: 2px;
}
</style>
