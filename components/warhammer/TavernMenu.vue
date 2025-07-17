<template>
  <div class="tavern-menu">
    <!-- Menu Header -->
    <div class="menu-header text-center mb-8">
      <h2 class="font-fantasy text-3xl text-primary heading-glow mb-2">
        The Warhammer Tavern
      </h2>
      <p class="font-medieval text-muted-foreground">
        "Where heroes gather and tales are told"
      </p>
      <div class="w-24 h-1 bg-gradient-to-r from-transparent via-primary to-transparent mx-auto mt-4"></div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state text-center py-12">
      <div class="animate-spin w-8 h-8 border-2 border-primary border-t-transparent rounded-full mx-auto mb-4"></div>
      <p class="font-medieval text-muted-foreground">Loading tavern offerings...</p>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error-state text-center py-12">
      <Icon name="alert-triangle" class="w-12 h-12 text-destructive mx-auto mb-4" />
      <p class="font-medieval text-destructive">{{ error }}</p>
      <button @click="initializeData" class="btn-enhanced mt-4">
        <Icon name="refresh" class="w-4 h-4 mr-2" />
        Try Again
      </button>
    </div>

    <!-- Menu Content -->
    <div v-else class="menu-content">
      <!-- Category Tabs -->
      <div class="category-tabs mb-8">
        <div class="flex flex-wrap justify-center gap-2">
          <button
            v-for="category in categories"
            :key="category.type"
            @click="activeCategory = category.type"
            :class="[
              'category-tab px-4 py-2 rounded-lg font-medieval transition-all duration-200',
              activeCategory === category.type
                ? 'bg-primary text-primary-foreground shadow-lg'
                : 'bg-card/50 text-muted-foreground hover:bg-card hover:text-foreground'
            ]"
          >
            <Icon :name="category.icon" class="w-4 h-4 mr-2" />
            {{ category.label }}
            <span class="ml-2 text-xs opacity-75">({{ getCategoryItems(category.type).length }})</span>
          </button>
        </div>
      </div>

      <!-- Menu Items -->
      <div class="menu-items">
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          <div
            v-for="item in getCategoryItems(activeCategory)"
            :key="item.id"
            class="menu-item card-enhanced hover:shadow-xl transition-all duration-300"
          >
            <!-- Item Header -->
            <div class="item-header flex justify-between items-start mb-3">
              <div class="item-info flex-1">
                <h3 class="font-medieval text-lg text-foreground">{{ item.name }}</h3>
                <div class="flex items-center space-x-2 mt-1">
                  <span 
                    :class="[
                      'availability-badge text-xs px-2 py-1 rounded-full font-sharp',
                      getAvailabilityClass(item.availability)
                    ]"
                  >
                    {{ item.availability || 'common' }}
                  </span>
                  <span 
                    :class="[
                      'type-badge text-xs px-2 py-1 rounded-full font-sharp',
                      getTypeClass(item.type)
                    ]"
                  >
                    {{ item.type }}
                  </span>
                </div>
              </div>
              <div class="item-price text-right">
                <span class="font-medieval text-primary font-bold">
                  {{ item.price || 'Ask' }}
                </span>
              </div>
            </div>

            <!-- Item Description -->
            <div class="item-description mb-4">
              <p class="text-muted-foreground font-sharp text-sm leading-relaxed">
                {{ item.description || 'A fine offering from our tavern.' }}
              </p>
            </div>

            <!-- Item Actions -->
            <div class="item-actions flex space-x-2">
              <button class="btn-enhanced text-xs flex-1">
                <Icon name="plus" class="w-3 h-3 mr-1" />
                Order
              </button>
              <button class="btn-enhanced text-xs bg-secondary/90 hover:bg-secondary">
                <Icon name="info" class="w-3 h-3" />
              </button>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-if="getCategoryItems(activeCategory).length === 0" class="empty-state text-center py-12">
          <Icon name="package" class="w-16 h-16 text-muted-foreground/50 mx-auto mb-4" />
          <h3 class="font-medieval text-lg text-muted-foreground mb-2">No items available</h3>
          <p class="font-sharp text-muted-foreground/75">
            The tavern keeper is restocking this category.
          </p>
        </div>
      </div>

      <!-- Random Daily Specials -->
      <div v-if="dailySpecials.length > 0" class="daily-specials mt-12 pt-8 border-t border-border/30">
        <h3 class="font-medieval text-xl text-foreground heading-glow text-center mb-6">
          Today's Specials
        </h3>
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          <div
            v-for="special in dailySpecials"
            :key="special.id"
            class="special-item p-4 bg-gradient-to-br from-accent/10 to-accent/5 rounded-lg border border-accent/20"
          >
            <div class="flex justify-between items-center">
              <h4 class="font-medieval text-accent">{{ special.name }}</h4>
              <span class="text-accent font-bold">{{ special.price }}</span>
            </div>
            <p class="text-muted-foreground font-sharp text-sm mt-1">{{ special.description }}</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
const { tavernItems, isLoading, error, initializeData, getRandomTavernItems } = useWarhammerData()

// Initialize data on component mount
onMounted(() => {
  initializeData()
})

// Category configuration
const categories = [
  { type: 'drink', label: 'Drinks', icon: 'wine' },
  { type: 'food', label: 'Food', icon: 'bread' },
  { type: 'room', label: 'Rooms', icon: 'bed' },
  { type: 'service', label: 'Services', icon: 'hammer' },
  { type: 'entertainment', label: 'Entertainment', icon: 'music' }
] as const

// Active category
const activeCategory = ref<'drink' | 'food' | 'room' | 'service' | 'entertainment'>('drink')

// Daily specials (random items)
const dailySpecials = computed(() => getRandomTavernItems(3))

// Get items for specific category
const getCategoryItems = (category: string) => {
  return tavernItems.value.filter(item => item.type === category)
}

// Get availability styling class
const getAvailabilityClass = (availability?: string) => {
  switch (availability) {
    case 'rare':
      return 'bg-destructive/20 text-destructive'
    case 'uncommon':
      return 'bg-accent/20 text-accent'
    case 'exotic':
      return 'bg-purple-500/20 text-purple-400'
    default:
      return 'bg-secondary/20 text-secondary'
  }
}

// Get type styling class
const getTypeClass = (type: string) => {
  switch (type) {
    case 'drink':
      return 'bg-blue-500/20 text-blue-400'
    case 'food':
      return 'bg-green-500/20 text-green-400'
    case 'room':
      return 'bg-purple-500/20 text-purple-400'
    case 'service':
      return 'bg-orange-500/20 text-orange-400'
    case 'entertainment':
      return 'bg-pink-500/20 text-pink-400'
    default:
      return 'bg-muted/20 text-muted-foreground'
  }
}
</script>

<style scoped>
.tavern-menu {
  @apply max-w-7xl mx-auto;
}

.category-tab {
  @apply flex items-center;
}

.category-tab:hover {
  @apply transform -translate-y-px;
}

.menu-item {
  @apply relative overflow-hidden;
}

.menu-item::before {
  content: '';
  @apply absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-primary/50 to-accent/50 transform scale-x-0 transition-transform duration-300;
}

.menu-item:hover::before {
  @apply scale-x-100;
}

.special-item {
  @apply transition-all duration-200;
}

.special-item:hover {
  @apply transform -translate-y-0.5 shadow-lg;
}

/* Responsive adjustments */
@media (max-width: 768px) {
  .menu-items {
    @apply grid-cols-1;
  }
  
  .category-tabs {
    @apply flex-col space-y-2;
  }
  
  .category-tab {
    @apply w-full justify-center;
  }
}
</style>
