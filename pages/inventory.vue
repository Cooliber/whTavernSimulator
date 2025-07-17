<template>
  <div class="inventory-page relative min-h-screen overflow-hidden">
    <!-- Atmospheric background -->
    <AuroraBackground 
      :colors="['#8b4513', '#a0522d', '#cd853f', '#daa520']"
      :aurora-width="600"
      :aurora-height="400"
      class="absolute inset-0 opacity-20"
    />
    <ParticlesBg 
      :particle-count="25"
      particle-color="#ffd700"
      :particle-size="1"
      :animation-speed="0.3"
      class="opacity-40"
    />
    
    <div class="relative z-10 space-y-8 p-8">
      <!-- Header -->
      <section class="text-center space-y-6">
        <Spotlight 
          spotlight-color="rgba(255, 215, 0, 0.4)"
          :spotlight-size="400"
          class="inline-block"
        >
          <SparklesText 
            text="Character Inventory"
            class="text-5xl md:text-7xl font-medieval text-foreground"
            :sparkles-count="20"
          />
        </Spotlight>
        
        <Text3D 
          text="Manage Your Equipment & Items"
          class="text-xl md:text-2xl font-fantasy text-primary"
          :depth="3"
        />
      </section>

      <!-- Main Inventory Layout -->
      <div class="grid grid-cols-1 xl:grid-cols-3 gap-8">
        <!-- Character Equipment Panel -->
        <div class="xl:col-span-1">
          <BorderBeam 
            class="equipment-panel bg-card/80 backdrop-blur-md rounded-2xl p-6"
            :border-width="3"
            color-from="#ffd700"
            color-to="#b8860b"
          >
            <div class="space-y-6">
              <HyperText 
                text="Equipment"
                class="text-2xl font-medieval text-foreground text-center"
                :animation-duration="1200"
              />
              
              <!-- Character Model -->
              <div class="character-model relative mx-auto w-64 h-80 bg-gradient-to-b from-amber-900/30 to-amber-800/30 rounded-lg border-2 border-primary/30">
                <!-- Equipment Slots -->
                <div 
                  v-for="slot in equipmentSlots" 
                  :key="slot.id"
                  class="equipment-slot absolute border-2 border-dashed border-primary/50 rounded-lg transition-all duration-300"
                  :class="[slot.position, { 'border-solid border-primary': slot.item }]"
                  :style="slot.style"
                  @dragover.prevent
                  @drop="handleDrop($event, slot)"
                >
                  <Lens 
                    v-if="slot.item"
                    :lens-size="80"
                    :magnification="1.5"
                    class="w-full h-full"
                  >
                    <Card3D 
                      class="item-card w-full h-full bg-gradient-to-br from-amber-700/50 to-amber-800/50 rounded-lg flex items-center justify-center"
                      :rotation-intensity="8"
                    >
                      <Icon :name="slot.item.icon" class="w-6 h-6 text-primary" />
                    </Card3D>
                    
                    <template #magnified>
                      <div class="item-details bg-black/95 text-white p-3 rounded-lg">
                        <h4 class="font-medieval text-sm mb-1">{{ slot.item.name }}</h4>
                        <p class="text-xs mb-2">{{ slot.item.type }}</p>
                        <div class="space-y-1 text-xs">
                          <p><strong>Damage:</strong> {{ slot.item.damage || 'N/A' }}</p>
                          <p><strong>Defense:</strong> {{ slot.item.defense || 'N/A' }}</p>
                          <p><strong>Durability:</strong> {{ slot.item.durability }}%</p>
                        </div>
                      </div>
                    </template>
                  </Lens>
                  
                  <div v-else class="w-full h-full flex items-center justify-center">
                    <Icon :name="slot.defaultIcon" class="w-6 h-6 text-muted-foreground/50" />
                  </div>
                  
                  <!-- Slot Label -->
                  <div class="absolute -bottom-6 left-1/2 transform -translate-x-1/2">
                    <span class="text-xs font-medieval text-muted-foreground">{{ slot.name }}</span>
                  </div>
                </div>
                
                <!-- Character Stats Display -->
                <div class="absolute -bottom-16 left-0 right-0 grid grid-cols-3 gap-2 text-center">
                  <div class="stat-display">
                    <Icon name="sword" class="w-4 h-4 text-red-400 mx-auto" />
                    <NumberTicker 
                      :value="totalAttack"
                      class="text-sm font-bold text-red-400"
                    />
                  </div>
                  <div class="stat-display">
                    <Icon name="shield" class="w-4 h-4 text-blue-400 mx-auto" />
                    <NumberTicker 
                      :value="totalDefense"
                      class="text-sm font-bold text-blue-400"
                    />
                  </div>
                  <div class="stat-display">
                    <Icon name="sparkles" class="w-4 h-4 text-purple-400 mx-auto" />
                    <NumberTicker 
                      :value="totalMagic"
                      class="text-sm font-bold text-purple-400"
                    />
                  </div>
                </div>
              </div>
            </div>
          </BorderBeam>
        </div>
        
        <!-- Inventory Grid -->
        <div class="xl:col-span-2">
          <BorderBeam 
            class="inventory-grid-panel bg-card/80 backdrop-blur-md rounded-2xl p-6"
            :border-width="2"
            color-from="#8b4513"
            color-to="#a0522d"
          >
            <div class="space-y-6">
              <!-- Inventory Header -->
              <div class="flex items-center justify-between">
                <HyperText 
                  text="Inventory"
                  class="text-2xl font-medieval text-foreground"
                  :animation-duration="1200"
                />
                
                <div class="flex items-center space-x-4">
                  <!-- Sort Options -->
                  <select 
                    v-model="sortBy"
                    class="bg-background/50 border border-border rounded-lg px-3 py-2 text-sm font-medieval text-foreground"
                  >
                    <option value="name">Sort by Name</option>
                    <option value="type">Sort by Type</option>
                    <option value="rarity">Sort by Rarity</option>
                    <option value="value">Sort by Value</option>
                  </select>
                  
                  <!-- Filter Options -->
                  <div class="flex space-x-2">
                    <RippleButton 
                      v-for="filter in itemFilters" 
                      :key="filter.id"
                      class="px-3 py-2 text-xs font-medieval"
                      :class="selectedFilter === filter.id ? 'faction-empire' : 'bg-secondary text-secondary-foreground'"
                      :ripple-color="selectedFilter === filter.id ? 'rgb(255, 215, 0)' : 'rgba(139, 69, 19, 0.5)'"
                      @click="setFilter(filter.id)"
                    >
                      <Icon :name="filter.icon" class="w-3 h-3 mr-1" />
                      {{ filter.name }}
                    </RippleButton>
                  </div>
                </div>
              </div>
              
              <!-- Inventory Grid -->
              <div class="inventory-grid grid grid-cols-8 md:grid-cols-10 lg:grid-cols-12 gap-2">
                <div 
                  v-for="(item, index) in filteredInventory" 
                  :key="index"
                  class="inventory-slot relative aspect-square border-2 border-border rounded-lg transition-all duration-300 hover:border-primary/50"
                  :class="{ 'border-primary bg-primary/10': item }"
                  @dragover.prevent
                  @drop="handleInventoryDrop($event, index)"
                >
                  <DirectionAwareHover 
                    v-if="item"
                    class="w-full h-full"
                  >
                    <template #content>
                      <Card3D 
                        class="item-card w-full h-full bg-gradient-to-br rounded-lg flex items-center justify-center cursor-grab active:cursor-grabbing"
                        :class="item.rarityBg"
                        :rotation-intensity="5"
                        draggable="true"
                        @dragstart="handleDragStart($event, item, index)"
                      >
                        <Icon :name="item.icon" class="w-6 h-6" :class="item.rarityText" />
                        
                        <!-- Stack count -->
                        <div v-if="item.quantity > 1" class="absolute bottom-0 right-0 bg-primary text-primary-foreground text-xs rounded-tl-lg px-1">
                          {{ item.quantity }}
                        </div>
                        
                        <!-- Durability indicator -->
                        <div v-if="item.durability < 100" class="absolute bottom-0 left-0 right-0 h-1 bg-background/50">
                          <div 
                            class="h-full transition-all duration-300"
                            :class="item.durability > 50 ? 'bg-green-500' : item.durability > 25 ? 'bg-yellow-500' : 'bg-red-500'"
                            :style="{ width: item.durability + '%' }"
                          />
                        </div>
                      </Card3D>
                    </template>
                    
                    <template #hover>
                      <div class="absolute inset-0 bg-black/90 text-white p-2 rounded-lg flex flex-col justify-center">
                        <div class="text-center space-y-1">
                          <h4 class="font-medieval text-sm" :class="item.rarityText">{{ item.name }}</h4>
                          <p class="text-xs text-gray-300">{{ item.type }}</p>
                          <div v-if="item.damage || item.defense" class="text-xs space-y-1">
                            <p v-if="item.damage" class="text-red-400">⚔️ {{ item.damage }}</p>
                            <p v-if="item.defense" class="text-blue-400">🛡️ {{ item.defense }}</p>
                          </div>
                          <p class="text-xs text-yellow-400">💰 {{ item.value }}g</p>
                        </div>
                      </div>
                    </template>
                  </DirectionAwareHover>
                  
                  <!-- Empty slot indicator -->
                  <div v-else class="w-full h-full flex items-center justify-center">
                    <div class="w-8 h-8 rounded-full bg-muted/20 flex items-center justify-center">
                      <Icon name="plus" class="w-4 h-4 text-muted-foreground/30" />
                    </div>
                  </div>
                </div>
                
                <!-- Empty slots to fill the grid -->
                <div 
                  v-for="i in Math.max(0, 96 - filteredInventory.length)" 
                  :key="`empty-${i}`"
                  class="inventory-slot aspect-square border-2 border-dashed border-border/30 rounded-lg flex items-center justify-center"
                >
                  <Icon name="plus" class="w-4 h-4 text-muted-foreground/20" />
                </div>
              </div>
            </div>
          </BorderBeam>
        </div>
      </div>
      
      <!-- Quick Actions Bar -->
      <section>
        <BorderBeam 
          class="quick-actions bg-card/60 backdrop-blur-md rounded-xl p-4"
          :border-width="1"
          color-from="#ffd700"
          color-to="#b8860b"
        >
          <div class="flex items-center justify-between">
            <div class="flex items-center space-x-4">
              <HyperText 
                text="Quick Actions"
                class="text-lg font-medieval text-foreground"
                :animation-duration="1000"
              />
            </div>
            
            <div class="flex space-x-3">
              <ShimmerButton 
                class="px-4 py-2 text-sm font-medieval bg-secondary text-secondary-foreground"
                shimmer-color="rgba(139, 69, 19, 0.5)"
                @click="sortInventory"
              >
                <Icon name="sort" class="w-4 h-4 mr-2" />
                Auto Sort
              </ShimmerButton>
              
              <RippleButton 
                class="px-4 py-2 text-sm font-medieval faction-empire"
                ripple-color="rgb(255, 215, 0)"
                @click="sellJunk"
              >
                <Icon name="trash" class="w-4 h-4 mr-2" />
                Sell Junk
              </RippleButton>
              
              <RainbowButton 
                :colors="['#22c55e', '#16a34a', '#15803d']"
                class="px-4 py-2 text-sm font-medieval"
                @click="repairAll"
              >
                <Icon name="hammer" class="w-4 h-4 mr-2" />
                Repair All
              </RainbowButton>
            </div>
          </div>
        </BorderBeam>
      </section>
    </div>
  </div>
</template><script setup lang="ts">
// Page metadata
useHead({
  title: 'Inventory - Warhammer Tavern Simulator v3',
  meta: [
    { name: 'description', content: 'Manage your character equipment and inventory with advanced drag-and-drop interface.' }
  ]
})

// Equipment slots configuration
const equipmentSlots = ref([
  {
    id: 'helmet',
    name: 'Helmet',
    position: 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2',
    style: { top: '10px', left: '50%', transform: 'translateX(-50%)', width: '40px', height: '40px' },
    defaultIcon: 'crown',
    item: {
      name: 'Iron Helmet',
      type: 'Helmet',
      icon: 'crown',
      defense: 15,
      durability: 85,
      rarity: 'common'
    }
  },
  {
    id: 'armor',
    name: 'Armor',
    position: 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2',
    style: { top: '80px', left: '50%', transform: 'translateX(-50%)', width: '60px', height: '80px' },
    defaultIcon: 'shield',
    item: {
      name: 'Chainmail Armor',
      type: 'Armor',
      icon: 'shield',
      defense: 35,
      durability: 92,
      rarity: 'uncommon'
    }
  },
  {
    id: 'weapon',
    name: 'Weapon',
    position: 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2',
    style: { top: '100px', left: '20px', width: '40px', height: '60px' },
    defaultIcon: 'sword',
    item: {
      name: 'Steel Sword',
      type: 'Weapon',
      icon: 'sword',
      damage: 45,
      durability: 78,
      rarity: 'rare'
    }
  },
  {
    id: 'shield',
    name: 'Shield',
    position: 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2',
    style: { top: '100px', right: '20px', width: '40px', height: '60px' },
    defaultIcon: 'shield',
    item: null
  },
  {
    id: 'boots',
    name: 'Boots',
    position: 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2',
    style: { bottom: '10px', left: '50%', transform: 'translateX(-50%)', width: '50px', height: '30px' },
    defaultIcon: 'footprints',
    item: {
      name: 'Leather Boots',
      type: 'Boots',
      icon: 'footprints',
      defense: 8,
      durability: 65,
      rarity: 'common'
    }
  },
  {
    id: 'gloves',
    name: 'Gloves',
    position: 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2',
    style: { top: '140px', left: '10px', width: '30px', height: '30px' },
    defaultIcon: 'hand',
    item: null
  },
  {
    id: 'ring',
    name: 'Ring',
    position: 'top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2',
    style: { top: '140px', right: '10px', width: '30px', height: '30px' },
    defaultIcon: 'circle',
    item: null
  }
])

// Inventory items
const inventory = ref([
  {
    name: 'Health Potion',
    type: 'Consumable',
    icon: 'heart',
    quantity: 5,
    value: 25,
    durability: 100,
    rarity: 'common',
    rarityBg: 'from-gray-600/50 to-gray-700/50',
    rarityText: 'text-gray-300'
  },
  {
    name: 'Mana Potion',
    type: 'Consumable',
    icon: 'sparkles',
    quantity: 3,
    value: 40,
    durability: 100,
    rarity: 'common',
    rarityBg: 'from-blue-600/50 to-blue-700/50',
    rarityText: 'text-blue-300'
  },
  {
    name: 'Dragon Scale',
    type: 'Material',
    icon: 'shield',
    quantity: 1,
    value: 500,
    durability: 100,
    rarity: 'legendary',
    rarityBg: 'from-purple-600/50 to-purple-700/50',
    rarityText: 'text-purple-300'
  },
  {
    name: 'Iron Ore',
    type: 'Material',
    icon: 'hammer',
    quantity: 12,
    value: 15,
    durability: 100,
    rarity: 'common',
    rarityBg: 'from-gray-600/50 to-gray-700/50',
    rarityText: 'text-gray-300'
  },
  {
    name: 'Magic Scroll',
    type: 'Consumable',
    icon: 'scroll',
    quantity: 2,
    value: 150,
    durability: 100,
    rarity: 'rare',
    rarityBg: 'from-yellow-600/50 to-yellow-700/50',
    rarityText: 'text-yellow-300'
  },
  {
    name: 'Elven Bow',
    type: 'Weapon',
    icon: 'bow',
    quantity: 1,
    damage: 55,
    value: 800,
    durability: 95,
    rarity: 'epic',
    rarityBg: 'from-orange-600/50 to-orange-700/50',
    rarityText: 'text-orange-300'
  },
  {
    name: 'Ancient Tome',
    type: 'Book',
    icon: 'book',
    quantity: 1,
    value: 1200,
    durability: 100,
    rarity: 'legendary',
    rarityBg: 'from-purple-600/50 to-purple-700/50',
    rarityText: 'text-purple-300'
  },
  {
    name: 'Gold Coins',
    type: 'Currency',
    icon: 'star',
    quantity: 2847,
    value: 1,
    durability: 100,
    rarity: 'common',
    rarityBg: 'from-yellow-600/50 to-yellow-700/50',
    rarityText: 'text-yellow-300'
  }
])

// Filter and sort options
const itemFilters = ref([
  { id: 'all', name: 'All', icon: 'grid' },
  { id: 'weapons', name: 'Weapons', icon: 'sword' },
  { id: 'armor', name: 'Armor', icon: 'shield' },
  { id: 'consumables', name: 'Consumables', icon: 'heart' },
  { id: 'materials', name: 'Materials', icon: 'hammer' }
])

const selectedFilter = ref('all')
const sortBy = ref('name')

// Computed properties
const totalAttack = computed(() => {
  return equipmentSlots.value.reduce((total, slot) => {
    return total + (slot.item?.damage || 0)
  }, 0)
})

const totalDefense = computed(() => {
  return equipmentSlots.value.reduce((total, slot) => {
    return total + (slot.item?.defense || 0)
  }, 0)
})

const totalMagic = computed(() => {
  return equipmentSlots.value.reduce((total, slot) => {
    return total + (slot.item?.magic || 0)
  }, 25) // Base magic value
})

const filteredInventory = computed(() => {
  let filtered = inventory.value

  // Apply filter
  if (selectedFilter.value !== 'all') {
    filtered = filtered.filter(item => {
      switch (selectedFilter.value) {
        case 'weapons':
          return item.type === 'Weapon'
        case 'armor':
          return ['Helmet', 'Armor', 'Boots', 'Gloves'].includes(item.type)
        case 'consumables':
          return item.type === 'Consumable'
        case 'materials':
          return item.type === 'Material'
        default:
          return true
      }
    })
  }

  // Apply sort
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'name':
        return a.name.localeCompare(b.name)
      case 'type':
        return a.type.localeCompare(b.type)
      case 'rarity':
        const rarityOrder = { common: 1, uncommon: 2, rare: 3, epic: 4, legendary: 5 }
        return (rarityOrder[b.rarity] || 0) - (rarityOrder[a.rarity] || 0)
      case 'value':
        return b.value - a.value
      default:
        return 0
    }
  })

  return filtered
})

// Drag and drop functionality
let draggedItem = null
let draggedFromIndex = null

const handleDragStart = (event: DragEvent, item: any, index: number) => {
  draggedItem = item
  draggedFromIndex = index
  event.dataTransfer!.effectAllowed = 'move'
}

const handleDrop = (event: DragEvent, slot: any) => {
  event.preventDefault()
  
  if (draggedItem && canEquipItem(draggedItem, slot)) {
    // Unequip current item if any
    if (slot.item) {
      inventory.value.push(slot.item)
    }
    
    // Equip new item
    slot.item = { ...draggedItem }
    
    // Remove from inventory
    if (draggedFromIndex !== null) {
      inventory.value.splice(draggedFromIndex, 1)
    }
    
    console.log(`Equipped ${draggedItem.name} to ${slot.name}`)
  }
  
  draggedItem = null
  draggedFromIndex = null
}

const handleInventoryDrop = (event: DragEvent, index: number) => {
  event.preventDefault()
  
  if (draggedItem && draggedFromIndex !== null && draggedFromIndex !== index) {
    // Swap items in inventory
    const temp = inventory.value[index]
    inventory.value[index] = draggedItem
    if (temp) {
      inventory.value[draggedFromIndex] = temp
    } else {
      inventory.value.splice(draggedFromIndex, 1)
    }
  }
  
  draggedItem = null
  draggedFromIndex = null
}

const canEquipItem = (item: any, slot: any) => {
  // Check if item type matches slot
  const typeMapping = {
    helmet: ['Helmet'],
    armor: ['Armor'],
    weapon: ['Weapon'],
    shield: ['Shield'],
    boots: ['Boots'],
    gloves: ['Gloves'],
    ring: ['Ring']
  }
  
  return typeMapping[slot.id]?.includes(item.type) || false
}

// Methods
const setFilter = (filterId: string) => {
  selectedFilter.value = filterId
}

const sortInventory = () => {
  console.log('Auto-sorting inventory...')
  // Inventory is automatically sorted via computed property
}

const sellJunk = () => {
  const junkItems = inventory.value.filter(item => 
    item.rarity === 'common' && item.type !== 'Currency'
  )
  
  const totalValue = junkItems.reduce((sum, item) => sum + (item.value * item.quantity), 0)
  
  // Remove junk items
  inventory.value = inventory.value.filter(item => 
    !(item.rarity === 'common' && item.type !== 'Currency')
  )
  
  // Add gold
  const goldItem = inventory.value.find(item => item.type === 'Currency')
  if (goldItem) {
    goldItem.quantity += totalValue
  }
  
  console.log(`Sold junk items for ${totalValue} gold`)
}

const repairAll = () => {
  // Repair all equipped items
  equipmentSlots.value.forEach(slot => {
    if (slot.item) {
      slot.item.durability = 100
    }
  })
  
  // Repair all items in inventory
  inventory.value.forEach(item => {
    item.durability = 100
  })
  
  console.log('All items repaired!')
}

// Lifecycle
onMounted(() => {
  console.log('Inventory system loaded')
})
</script>

<style scoped>
/* Inventory specific styles */
.inventory-page {
  background-attachment: fixed;
}

.equipment-panel {
  animation: panel-slide-in-left 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.inventory-grid-panel {
  animation: panel-slide-in-right 0.8s cubic-bezier(0.4, 0, 0.2, 1) forwards;
}

.character-model {
  position: relative;
  background-image: 
    radial-gradient(circle at 30% 20%, rgba(255, 215, 0, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 70% 80%, rgba(139, 69, 19, 0.1) 0%, transparent 50%);
}

.equipment-slot {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.equipment-slot:hover {
  border-color: rgb(255, 215, 0);
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.3);
  transform: scale(1.05);
}

.inventory-slot {
  transition: all 0.2s ease;
}

.inventory-slot:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}

.item-card {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.item-card:hover {
  transform: scale(1.1) rotateY(5deg);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.4);
}

.stat-display {
  animation: stat-bounce 0.6s ease-out forwards;
}

/* Custom animations */
@keyframes panel-slide-in-left {
  0% {
    opacity: 0;
    transform: translateX(-50px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes panel-slide-in-right {
  0% {
    opacity: 0;
    transform: translateX(50px);
  }
  100% {
    opacity: 1;
    transform: translateX(0);
  }
}

@keyframes stat-bounce {
  0% {
    opacity: 0;
    transform: translateY(20px) scale(0.8);
  }
  60% {
    transform: translateY(-5px) scale(1.1);
  }
  100% {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

/* Drag and drop visual feedback */
.equipment-slot.drag-over {
  border-color: rgb(34, 197, 94);
  background-color: rgba(34, 197, 94, 0.1);
}

.inventory-slot.drag-over {
  border-color: rgb(34, 197, 94);
  background-color: rgba(34, 197, 94, 0.1);
}

/* Rarity glow effects */
.item-card[data-rarity="legendary"] {
  box-shadow: 0 0 20px rgba(147, 51, 234, 0.5);
}

.item-card[data-rarity="epic"] {
  box-shadow: 0 0 15px rgba(249, 115, 22, 0.5);
}

.item-card[data-rarity="rare"] {
  box-shadow: 0 0 10px rgba(234, 179, 8, 0.5);
}

/* Responsive design */
@media (max-width: 1280px) {
  .character-model {
    width: 200px;
    height: 300px;
  }
  
  .equipment-slot {
    transform: scale(0.8);
  }
}

@media (max-width: 768px) {
  .inventory-grid {
    grid-template-columns: repeat(6, 1fr);
  }
  
  .character-model {
    width: 180px;
    height: 250px;
  }
}

/* Performance optimizations */
.item-card,
.equipment-slot,
.inventory-slot {
  will-change: transform;
}
</style>