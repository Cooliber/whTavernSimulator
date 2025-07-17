<template>
  <div class="map-page relative min-h-screen overflow-hidden">
    <!-- Epic atmospheric background -->
    <InteractiveGridPattern 
      :grid-size="100"
      grid-color="#8b4513"
      :stroke-width="1"
      :proximity-radius="150"
      proximity-color="#ffd700"
      class="absolute inset-0 opacity-10"
    />
    <AuroraBackground 
      :colors="['#2d1b14', '#4a2c1a', '#6b3e1f', '#8b4513']"
      :aurora-width="800"
      :aurora-height="600"
      class="absolute inset-0 opacity-30"
    />
    <Meteors :meteor-count="5" :meteor-speed="0.5" />
    
    <div class="relative z-10 space-y-8 p-8">
      <!-- Header -->
      <section class="text-center space-y-6">
        <Spotlight 
          spotlight-color="rgba(139, 69, 19, 0.6)"
          :spotlight-size="600"
          class="inline-block"
        >
          <div class="space-y-4">
            <SparklesText 
              text="World Map of the Old World"
              class="text-5xl md:text-7xl font-medieval text-foreground"
              :sparkles-count="25"
            />
            <Text3D 
              text="Explore the Realms of Warhammer Fantasy"
              class="text-xl md:text-2xl font-fantasy text-primary"
              :depth="4"
            />
          </div>
        </Spotlight>
      </section>

      <!-- Map Controls -->
      <section>
        <BorderBeam 
          class="map-controls bg-card/80 backdrop-blur-md rounded-xl p-4"
          :border-width="2"
          color-from="#ffd700"
          color-to="#b8860b"
        >
          <div class="flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center space-x-4">
              <HyperText 
                text="Map Controls"
                class="text-lg font-medieval text-foreground"
                :animation-duration="1000"
              />
              
              <!-- Zoom Controls -->
              <div class="flex items-center space-x-2">
                <RippleButton 
                  class="w-10 h-10 rounded-full bg-secondary text-secondary-foreground flex items-center justify-center"
                  ripple-color="rgba(139, 69, 19, 0.5)"
                  @click="zoomOut"
                >
                  <Icon name="minus" class="w-4 h-4" />
                </RippleButton>
                
                <span class="text-sm font-medieval text-muted-foreground px-3">{{ zoomLevel }}%</span>
                
                <RippleButton 
                  class="w-10 h-10 rounded-full bg-secondary text-secondary-foreground flex items-center justify-center"
                  ripple-color="rgba(139, 69, 19, 0.5)"
                  @click="zoomIn"
                >
                  <Icon name="plus" class="w-4 h-4" />
                </RippleButton>
              </div>
            </div>
            
            <!-- Map Filters -->
            <div class="flex items-center space-x-2">
              <RippleButton 
                v-for="filter in mapFilters" 
                :key="filter.id"
                class="px-4 py-2 text-sm font-medieval"
                :class="activeFilters.includes(filter.id) ? 'faction-empire' : 'bg-secondary text-secondary-foreground'"
                :ripple-color="activeFilters.includes(filter.id) ? 'rgb(255, 215, 0)' : 'rgba(139, 69, 19, 0.5)'"
                @click="toggleFilter(filter.id)"
              >
                <Icon :name="filter.icon" class="w-3 h-3 mr-1" />
                {{ filter.name }}
              </RippleButton>
            </div>
          </div>
        </BorderBeam>
      </section>

      <!-- Main Map Container -->
      <section class="relative">
        <BorderBeam 
          class="map-container bg-gradient-to-br from-amber-900/20 to-amber-800/20 backdrop-blur-md rounded-2xl overflow-hidden"
          :border-width="3"
          color-from="#8b4513"
          color-to="#a0522d"
        >
          <div 
            class="map-viewport relative w-full h-[600px] overflow-hidden cursor-grab active:cursor-grabbing"
            :style="{ transform: `scale(${zoomLevel / 100}) translate(${panX}px, ${panY}px)` }"
            @mousedown="startPan"
            @mousemove="handlePan"
            @mouseup="endPan"
            @mouseleave="endPan"
          >
            <!-- Map Background -->
            <div class="absolute inset-0 bg-gradient-to-br from-amber-900/10 to-amber-800/10">
              <!-- Terrain Features -->
              <svg class="w-full h-full" viewBox="0 0 1200 600">
                <!-- Mountains -->
                <path 
                  d="M100,400 L200,200 L300,350 L400,150 L500,300 L600,100 L700,250"
                  stroke="#8b4513"
                  stroke-width="3"
                  fill="none"
                  class="terrain-mountains"
                />
                
                <!-- Rivers -->
                <path 
                  d="M0,300 Q200,280 400,320 T800,300 Q1000,290 1200,310"
                  stroke="#4682b4"
                  stroke-width="4"
                  fill="none"
                  class="terrain-river"
                />
                
                <!-- Forests -->
                <circle cx="300" cy="400" r="80" fill="#228b22" opacity="0.3" class="terrain-forest" />
                <circle cx="800" cy="200" r="100" fill="#228b22" opacity="0.3" class="terrain-forest" />
                <circle cx="1000" cy="450" r="60" fill="#228b22" opacity="0.3" class="terrain-forest" />
              </svg>
            </div>
            
            <!-- Map Locations -->
            <div class="absolute inset-0">
              <div 
                v-for="location in filteredLocations" 
                :key="location.id"
                class="map-location absolute transform -translate-x-1/2 -translate-y-1/2 cursor-pointer"
                :style="{ left: location.x + '%', top: location.y + '%' }"
                @click="selectLocation(location)"
              >
                <Lens 
                  :lens-size="120"
                  :magnification="1.8"
                  class="location-lens"
                >
                  <Card3D 
                    class="location-marker w-12 h-12 rounded-full border-2 border-primary/50 flex items-center justify-center transition-all duration-300"
                    :class="[location.typeClass, { 'scale-125 border-primary': selectedLocation?.id === location.id }]"
                    :rotation-intensity="8"
                  >
                    <Icon :name="location.icon" class="w-6 h-6 text-white drop-shadow-lg" />
                    
                    <!-- Location pulse effect -->
                    <div class="absolute inset-0 rounded-full border-2 border-primary animate-ping opacity-30" />
                  </Card3D>
                  
                  <template #magnified>
                    <div class="location-details bg-black/95 text-white p-3 rounded-lg">
                      <h4 class="font-medieval text-sm mb-1">{{ location.name }}</h4>
                      <p class="text-xs mb-2">{{ location.type }}</p>
                      <div class="space-y-1 text-xs">
                        <p><strong>Faction:</strong> {{ location.faction }}</p>
                        <p><strong>Danger:</strong> {{ location.dangerLevel }}</p>
                        <p><strong>Resources:</strong> {{ location.resources.join(', ') }}</p>
                      </div>
                    </div>
                  </template>
                </Lens>
                
                <!-- Location Label -->
                <div class="absolute top-full left-1/2 transform -translate-x-1/2 mt-2 pointer-events-none">
                  <div class="bg-black/80 text-white px-2 py-1 rounded text-xs font-medieval whitespace-nowrap">
                    {{ location.name }}
                  </div>
                </div>
              </div>
            </div>
            
            <!-- Travel Routes -->
            <svg class="absolute inset-0 w-full h-full pointer-events-none">
              <defs>
                <marker id="arrowhead" markerWidth="10" markerHeight="7" refX="9" refY="3.5" orient="auto">
                  <polygon points="0 0, 10 3.5, 0 7" fill="#ffd700" opacity="0.6" />
                </marker>
              </defs>
              
              <path 
                v-for="route in travelRoutes" 
                :key="route.id"
                :d="route.path"
                stroke="#ffd700"
                stroke-width="2"
                stroke-dasharray="5,5"
                fill="none"
                opacity="0.6"
                marker-end="url(#arrowhead)"
                class="travel-route"
              />
            </svg>
          </div>
        </BorderBeam>
      </section>

      <!-- Location Details Panel -->
      <section v-if="selectedLocation" class="location-details-panel">
        <BorderBeam 
          class="bg-card/90 backdrop-blur-md rounded-2xl p-6"
          :border-width="3"
          :color-from="selectedLocation.typeColor"
          :color-to="selectedLocation.typeColor + '60'"
        >
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Location Info -->
            <div class="lg:col-span-2 space-y-6">
              <div class="space-y-4">
                <div class="flex items-center space-x-4">
                  <div 
                    class="w-16 h-16 rounded-full border-4 border-primary/30 flex items-center justify-center"
                    :class="selectedLocation.typeClass"
                  >
                    <Icon :name="selectedLocation.icon" class="w-8 h-8 text-white" />
                  </div>
                  <div>
                    <SparklesText 
                      :text="selectedLocation.name"
                      class="text-3xl font-medieval text-foreground"
                      :sparkles-count="12"
                    />
                    <p class="text-lg text-muted-foreground">{{ selectedLocation.type }}</p>
                  </div>
                </div>
                
                <TextReveal 
                  :text="selectedLocation.description"
                  class="text-foreground leading-relaxed"
                  :reveal-speed="30"
                  trigger="immediate"
                />
              </div>
              
              <!-- Location Stats -->
              <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                <div 
                  v-for="stat in selectedLocation.stats" 
                  :key="stat.name"
                  class="stat-card text-center p-4 rounded-lg bg-background/30"
                >
                  <Icon :name="stat.icon" class="w-6 h-6 mx-auto mb-2 text-primary" />
                  <NumberTicker 
                    :value="stat.value"
                    class="text-xl font-bold text-foreground"
                  />
                  <p class="text-xs text-muted-foreground font-medieval">{{ stat.name }}</p>
                </div>
              </div>
              
              <!-- Available Actions -->
              <div class="space-y-3">
                <h3 class="text-lg font-medieval text-foreground">Available Actions</h3>
                <div class="flex flex-wrap gap-3">
                  <RippleButton 
                    v-for="action in selectedLocation.actions" 
                    :key="action.id"
                    class="px-4 py-2 text-sm font-medieval"
                    :class="action.buttonClass"
                    :ripple-color="action.rippleColor"
                    @click="performAction(action)"
                  >
                    <Icon :name="action.icon" class="w-4 h-4 mr-2" />
                    {{ action.name }}
                  </RippleButton>
                </div>
              </div>
            </div>
            
            <!-- Quick Travel & Resources -->
            <div class="space-y-6">
              <!-- Quick Travel -->
              <div class="space-y-4">
                <h3 class="text-lg font-medieval text-foreground">Quick Travel</h3>
                <div class="space-y-2">
                  <div 
                    v-for="destination in nearbyLocations" 
                    :key="destination.id"
                    class="travel-option flex items-center justify-between p-3 rounded-lg bg-background/30 hover:bg-background/50 transition-colors cursor-pointer"
                    @click="travelTo(destination)"
                  >
                    <div class="flex items-center space-x-3">
                      <Icon :name="destination.icon" class="w-4 h-4 text-primary" />
                      <span class="text-sm font-medieval text-foreground">{{ destination.name }}</span>
                    </div>
                    <div class="flex items-center space-x-2">
                      <Icon name="clock" class="w-3 h-3 text-muted-foreground" />
                      <span class="text-xs text-muted-foreground">{{ destination.travelTime }}</span>
                    </div>
                  </div>
                </div>
              </div>
              
              <!-- Resources -->
              <div class="space-y-4">
                <h3 class="text-lg font-medieval text-foreground">Local Resources</h3>
                <div class="grid grid-cols-2 gap-2">
                  <div 
                    v-for="resource in selectedLocation.resources" 
                    :key="resource"
                    class="resource-item flex items-center space-x-2 p-2 rounded-lg bg-background/30"
                  >
                    <Icon :name="getResourceIcon(resource)" class="w-4 h-4 text-primary" />
                    <span class="text-xs font-medieval text-foreground">{{ resource }}</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </BorderBeam>
      </section>
    </div>
  </div>
</template><script setup lang="ts">
// Page metadata
useHead({
  title: 'World Map - Warhammer Tavern Simulator v3',
  meta: [
    { name: 'description', content: 'Explore the vast world of Warhammer Fantasy. Discover locations, plan journeys, and uncover hidden secrets.' }
  ]
})

// Map state
const zoomLevel = ref(100)
const panX = ref(0)
const panY = ref(0)
const isPanning = ref(false)
const lastPanPosition = ref({ x: 0, y: 0 })
const selectedLocation = ref(null)

// Map filters
const mapFilters = ref([
  { id: 'cities', name: 'Cities', icon: 'home' },
  { id: 'dungeons', name: 'Dungeons', icon: 'skull' },
  { id: 'resources', name: 'Resources', icon: 'hammer' },
  { id: 'quests', name: 'Quests', icon: 'scroll' }
])

const activeFilters = ref(['cities', 'dungeons', 'resources', 'quests'])

// Map locations
const locations = ref([
  {
    id: 'altdorf',
    name: 'Altdorf',
    type: 'Imperial Capital',
    x: 45,
    y: 35,
    icon: 'crown',
    typeClass: 'bg-gradient-to-br from-yellow-600 to-yellow-500',
    typeColor: '#eab308',
    faction: 'Empire',
    dangerLevel: 'Safe',
    category: 'cities',
    description: 'The magnificent capital of the Empire, seat of the Emperor and center of civilization in the Old World. Its towering spires and grand palaces speak of power and prosperity.',
    resources: ['Gold', 'Trade Goods', 'Information', 'Equipment'],
    stats: [
      { name: 'Population', value: 105000, icon: 'users' },
      { name: 'Wealth', value: 95, icon: 'star' },
      { name: 'Defense', value: 88, icon: 'shield' },
      { name: 'Trade', value: 98, icon: 'package' }
    ],
    actions: [
      { id: 'visit', name: 'Visit City', icon: 'home', buttonClass: 'faction-empire', rippleColor: 'rgb(255, 215, 0)' },
      { id: 'trade', name: 'Trade', icon: 'package', buttonClass: 'bg-green-600 text-white', rippleColor: 'rgba(34, 197, 94, 0.6)' },
      { id: 'recruit', name: 'Recruit', icon: 'users', buttonClass: 'bg-blue-600 text-white', rippleColor: 'rgba(59, 130, 246, 0.6)' }
    ]
  },
  {
    id: 'karaz-a-karak',
    name: 'Karaz-a-Karak',
    type: 'Dwarf Hold',
    x: 25,
    y: 55,
    icon: 'hammer',
    typeClass: 'bg-gradient-to-br from-orange-600 to-orange-500',
    typeColor: '#ea580c',
    faction: 'Dwarfs',
    dangerLevel: 'Safe',
    category: 'cities',
    description: 'The ancient capital of the Dwarf realm, carved deep into the World\'s Edge Mountains. Its halls echo with the sound of hammers and the songs of craftsmen.',
    resources: ['Iron', 'Gold', 'Weapons', 'Ale'],
    stats: [
      { name: 'Population', value: 75000, icon: 'users' },
      { name: 'Crafting', value: 98, icon: 'hammer' },
      { name: 'Defense', value: 95, icon: 'shield' },
      { name: 'Mining', value: 92, icon: 'pickaxe' }
    ],
    actions: [
      { id: 'visit', name: 'Enter Hold', icon: 'home', buttonClass: 'bg-orange-600 text-white', rippleColor: 'rgba(234, 88, 12, 0.6)' },
      { id: 'forge', name: 'Commission Weapon', icon: 'hammer', buttonClass: 'bg-red-600 text-white', rippleColor: 'rgba(220, 38, 38, 0.6)' },
      { id: 'mine', name: 'Mining Rights', icon: 'pickaxe', buttonClass: 'bg-gray-600 text-white', rippleColor: 'rgba(75, 85, 99, 0.6)' }
    ]
  },
  {
    id: 'lothern',
    name: 'Lothern',
    type: 'High Elf City',
    x: 15,
    y: 25,
    icon: 'sparkles',
    typeClass: 'bg-gradient-to-br from-blue-600 to-blue-500',
    typeColor: '#2563eb',
    faction: 'High Elves',
    dangerLevel: 'Safe',
    category: 'cities',
    description: 'The shining jewel of Ulthuan, where white towers reach toward the heavens and magic flows like water through crystal channels.',
    resources: ['Magic Items', 'Elven Goods', 'Knowledge', 'Gems'],
    stats: [
      { name: 'Population', value: 85000, icon: 'users' },
      { name: 'Magic', value: 98, icon: 'sparkles' },
      { name: 'Culture', value: 95, icon: 'book' },
      { name: 'Navy', value: 90, icon: 'anchor' }
    ],
    actions: [
      { id: 'visit', name: 'Enter City', icon: 'home', buttonClass: 'bg-blue-600 text-white', rippleColor: 'rgba(37, 99, 235, 0.6)' },
      { id: 'study', name: 'Study Magic', icon: 'sparkles', buttonClass: 'bg-purple-600 text-white', rippleColor: 'rgba(147, 51, 234, 0.6)' },
      { id: 'trade', name: 'Exotic Trade', icon: 'package', buttonClass: 'bg-green-600 text-white', rippleColor: 'rgba(34, 197, 94, 0.6)' }
    ]
  },
  {
    id: 'black-fire-pass',
    name: 'Black Fire Pass',
    type: 'Mountain Pass',
    x: 35,
    y: 65,
    icon: 'flame',
    typeClass: 'bg-gradient-to-br from-red-600 to-red-500',
    typeColor: '#dc2626',
    faction: 'Contested',
    dangerLevel: 'Dangerous',
    category: 'dungeons',
    description: 'A treacherous mountain pass where the forces of Order once held back the tide of Orcs and Goblins. Ancient battlefields and hidden treasures await the brave.',
    resources: ['Ancient Weapons', 'Orc Loot', 'Strategic Position'],
    stats: [
      { name: 'Danger', value: 85, icon: 'skull' },
      { name: 'Treasure', value: 70, icon: 'star' },
      { name: 'Strategic', value: 90, icon: 'map' },
      { name: 'History', value: 95, icon: 'book' }
    ],
    actions: [
      { id: 'explore', name: 'Explore Pass', icon: 'eye', buttonClass: 'bg-red-600 text-white', rippleColor: 'rgba(220, 38, 38, 0.6)' },
      { id: 'battle', name: 'Clear Orcs', icon: 'sword', buttonClass: 'bg-orange-600 text-white', rippleColor: 'rgba(234, 88, 12, 0.6)' },
      { id: 'search', name: 'Search Ruins', icon: 'search', buttonClass: 'bg-gray-600 text-white', rippleColor: 'rgba(75, 85, 99, 0.6)' }
    ]
  },
  {
    id: 'iron-mine',
    name: 'Abandoned Iron Mine',
    type: 'Resource Site',
    x: 55,
    y: 45,
    icon: 'pickaxe',
    typeClass: 'bg-gradient-to-br from-gray-600 to-gray-500',
    typeColor: '#4b5563',
    faction: 'Abandoned',
    dangerLevel: 'Moderate',
    category: 'resources',
    description: 'Once a prosperous iron mine, now overrun by goblins and worse. Rich veins of ore still remain for those brave enough to reclaim them.',
    resources: ['Iron Ore', 'Coal', 'Gems', 'Mining Equipment'],
    stats: [
      { name: 'Iron Quality', value: 80, icon: 'hammer' },
      { name: 'Danger', value: 60, icon: 'skull' },
      { name: 'Yield', value: 75, icon: 'package' },
      { name: 'Depth', value: 85, icon: 'arrow-down' }
    ],
    actions: [
      { id: 'mine', name: 'Start Mining', icon: 'pickaxe', buttonClass: 'bg-gray-600 text-white', rippleColor: 'rgba(75, 85, 99, 0.6)' },
      { id: 'clear', name: 'Clear Goblins', icon: 'sword', buttonClass: 'bg-red-600 text-white', rippleColor: 'rgba(220, 38, 38, 0.6)' },
      { id: 'survey', name: 'Survey Site', icon: 'eye', buttonClass: 'bg-blue-600 text-white', rippleColor: 'rgba(37, 99, 235, 0.6)' }
    ]
  },
  {
    id: 'haunted-forest',
    name: 'Drakwald Forest',
    type: 'Haunted Forest',
    x: 65,
    y: 30,
    icon: 'leaf',
    typeClass: 'bg-gradient-to-br from-green-800 to-green-700',
    typeColor: '#166534',
    faction: 'Wild',
    dangerLevel: 'Very Dangerous',
    category: 'dungeons',
    description: 'A dark and twisted forest where ancient evils lurk among the gnarled trees. Few who enter return unchanged, but great rewards await the worthy.',
    resources: ['Rare Herbs', 'Ancient Artifacts', 'Beast Parts', 'Dark Magic'],
    stats: [
      { name: 'Danger', value: 95, icon: 'skull' },
      { name: 'Magic', value: 88, icon: 'sparkles' },
      { name: 'Herbs', value: 92, icon: 'leaf' },
      { name: 'Beasts', value: 85, icon: 'zap' }
    ],
    actions: [
      { id: 'hunt', name: 'Hunt Beasts', icon: 'bow', buttonClass: 'bg-green-600 text-white', rippleColor: 'rgba(34, 197, 94, 0.6)' },
      { id: 'gather', name: 'Gather Herbs', icon: 'leaf', buttonClass: 'bg-emerald-600 text-white', rippleColor: 'rgba(5, 150, 105, 0.6)' },
      { id: 'investigate', name: 'Investigate Magic', icon: 'sparkles', buttonClass: 'bg-purple-600 text-white', rippleColor: 'rgba(147, 51, 234, 0.6)' }
    ]
  }
])

// Travel routes
const travelRoutes = ref([
  {
    id: 'altdorf-karaz',
    path: 'M 540 210 Q 400 300 300 330',
    from: 'altdorf',
    to: 'karaz-a-karak'
  },
  {
    id: 'altdorf-lothern',
    path: 'M 540 210 Q 300 150 180 150',
    from: 'altdorf',
    to: 'lothern'
  },
  {
    id: 'karaz-pass',
    path: 'M 300 330 Q 350 400 420 390',
    from: 'karaz-a-karak',
    to: 'black-fire-pass'
  }
])

// Computed properties
const filteredLocations = computed(() => {
  return locations.value.filter(location => 
    activeFilters.value.includes(location.category)
  )
})

const nearbyLocations = computed(() => {
  if (!selectedLocation.value) return []
  
  return locations.value
    .filter(loc => loc.id !== selectedLocation.value.id)
    .slice(0, 4)
    .map(loc => ({
      ...loc,
      travelTime: Math.floor(Math.random() * 8 + 2) + 'h'
    }))
})

// Methods
const zoomIn = () => {
  zoomLevel.value = Math.min(200, zoomLevel.value + 25)
}

const zoomOut = () => {
  zoomLevel.value = Math.max(50, zoomLevel.value - 25)
}

const toggleFilter = (filterId: string) => {
  const index = activeFilters.value.indexOf(filterId)
  if (index > -1) {
    activeFilters.value.splice(index, 1)
  } else {
    activeFilters.value.push(filterId)
  }
}

const startPan = (event: MouseEvent) => {
  isPanning.value = true
  lastPanPosition.value = { x: event.clientX, y: event.clientY }
}

const handlePan = (event: MouseEvent) => {
  if (!isPanning.value) return
  
  const deltaX = event.clientX - lastPanPosition.value.x
  const deltaY = event.clientY - lastPanPosition.value.y
  
  panX.value += deltaX
  panY.value += deltaY
  
  lastPanPosition.value = { x: event.clientX, y: event.clientY }
}

const endPan = () => {
  isPanning.value = false
}

const selectLocation = (location: any) => {
  selectedLocation.value = location
  console.log('Selected location:', location.name)
}

const performAction = (action: any) => {
  console.log('Performing action:', action.name, 'at', selectedLocation.value?.name)
  
  // Add action-specific logic here
  switch (action.id) {
    case 'visit':
      alert(`Traveling to ${selectedLocation.value?.name}...`)
      break
    case 'trade':
      alert(`Opening trade interface for ${selectedLocation.value?.name}...`)
      break
    case 'explore':
      alert(`Beginning exploration of ${selectedLocation.value?.name}...`)
      break
    default:
      alert(`Executing ${action.name}...`)
  }
}

const travelTo = (destination: any) => {
  console.log('Traveling to:', destination.name)
  selectedLocation.value = destination
}

const getResourceIcon = (resource: string) => {
  const iconMap = {
    'Gold': 'star',
    'Iron': 'hammer',
    'Coal': 'flame',
    'Gems': 'sparkles',
    'Weapons': 'sword',
    'Ale': 'cup',
    'Magic Items': 'sparkles',
    'Knowledge': 'book',
    'Trade Goods': 'package',
    'Information': 'eye',
    'Equipment': 'shield',
    'Ancient Weapons': 'sword',
    'Orc Loot': 'skull',
    'Strategic Position': 'map',
    'Iron Ore': 'hammer',
    'Mining Equipment': 'pickaxe',
    'Rare Herbs': 'leaf',
    'Ancient Artifacts': 'scroll',
    'Beast Parts': 'zap',
    'Dark Magic': 'flame',
    'Elven Goods': 'sparkles'
  }
  
  return iconMap[resource] || 'package'
}

// Lifecycle
onMounted(() => {
  console.log('World Map loaded with', locations.value.length, 'locations')
  
  // Auto-select first location
  if (locations.value.length > 0) {
    selectedLocation.value = locations.value[0]
  }
})
</script>

<style scoped>
/* Map specific styles */
.map-page {
  background-attachment: fixed;
}

.map-viewport {
  transition: transform 0.3s ease;
  transform-origin: center center;
}

.map-location {
  animation: location-pulse 2s ease-in-out infinite;
}

.location-marker {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.location-marker:hover {
  transform: scale(1.2);
  box-shadow: 0 0 20px rgba(255, 215, 0, 0.6);
}

.terrain-mountains {
  filter: drop-shadow(2px 2px 4px rgba(0, 0, 0, 0.3));
}

.terrain-river {
  filter: drop-shadow(0 0 4px rgba(70, 130, 180, 0.5));
  animation: river-flow 4s ease-in-out infinite;
}

.terrain-forest {
  animation: forest-sway 6s ease-in-out infinite;
}

.travel-route {
  animation: route-dash 2s linear infinite;
}

.stat-card {
  transition: all 0.3s ease;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

.travel-option:hover {
  transform: translateX(4px);
}

.resource-item {
  transition: all 0.2s ease;
}

.resource-item:hover {
  transform: scale(1.05);
  background-color: rgba(255, 215, 0, 0.1);
}

/* Custom animations */
@keyframes location-pulse {
  0%, 100% {
    opacity: 1;
  }
  50% {
    opacity: 0.7;
  }
}

@keyframes river-flow {
  0%, 100% {
    stroke-dashoffset: 0;
  }
  50% {
    stroke-dashoffset: 20;
  }
}

@keyframes forest-sway {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.05);
  }
}

@keyframes route-dash {
  0% {
    stroke-dashoffset: 0;
  }
  100% {
    stroke-dashoffset: 20;
  }
}

/* Responsive design */
@media (max-width: 768px) {
  .map-viewport {
    height: 400px;
  }
  
  .location-marker {
    width: 2rem;
    height: 2rem;
  }
}

/* Performance optimizations */
.map-location,
.location-marker,
.stat-card,
.travel-option {
  will-change: transform;
}
</style>