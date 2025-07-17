<template>
  <div class="space-y-8">
    <!-- Header -->
    <section class="text-center space-y-6">
      <div class="space-y-4">
        <SparklesText 
          text="Warhammer Content Generators"
          class="text-4xl md:text-5xl font-medieval text-foreground"
          :sparkles-count="25"
        />
        <Text3D 
          text="Create Epic Adventures"
          class="text-2xl font-fantasy text-primary"
          :depth="2"
        />
      </div>
      
      <p class="text-lg text-muted-foreground max-w-3xl mx-auto leading-relaxed">
        Generate authentic Warhammer Fantasy content using the comprehensive Polish plugin data. 
        Create NPCs, quests, items, and narrative elements for your campaigns.
      </p>
    </section>

    <!-- Generator Categories -->
    <section class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
      <Card3D 
        v-for="generator in generators" 
        :key="generator.id"
        class="inspira-card-tavern p-6 cursor-pointer transition-all duration-300"
        :class="{ 'ring-2 ring-primary': selectedGenerator === generator.id }"
        :rotation-intensity="8"
        @click="selectGenerator(generator.id)"
      >
        <div class="text-center space-y-4">
          <div class="w-16 h-16 mx-auto rounded-full bg-gradient-to-r from-primary/20 to-primary/10 flex items-center justify-center">
            <Icon :name="generator.icon" class="w-8 h-8 text-primary" />
          </div>
          <div>
            <h3 class="text-lg font-medieval text-foreground mb-2">{{ generator.name }}</h3>
            <p class="text-sm text-muted-foreground">{{ generator.description }}</p>
          </div>
          <div class="text-xs text-primary font-medieval">
            {{ generator.count }} Generated
          </div>
        </div>
      </Card3D>
    </section>

    <!-- Generator Interface -->
    <section v-if="selectedGenerator" class="space-y-6">
      <BorderBeam 
        class="p-6 bg-gradient-to-br from-primary/10 to-primary/5 rounded-2xl"
        :border-width="2"
        color-from="#ffd700"
        color-to="#b8860b"
      >
        <div class="space-y-6">
          <!-- Generator Controls -->
          <div class="flex flex-col sm:flex-row gap-4 items-center justify-between">
            <div class="space-y-2">
              <h3 class="text-xl font-medieval text-foreground">
                {{ currentGenerator?.name }} Generator
              </h3>
              <p class="text-sm text-muted-foreground">
                {{ currentGenerator?.description }}
              </p>
            </div>
            
            <div class="flex gap-3">
              <RippleButton 
                class="faction-empire px-6 py-3 font-medieval"
                ripple-color="rgb(255, 215, 0)"
                @click="generateContent"
                :disabled="isGenerating"
              >
                {{ isGenerating ? 'Generating...' : 'Generate' }}
              </RippleButton>
              
              <ShimmerButton 
                v-if="generatedContent.length > 0"
                class="px-6 py-3 font-medieval bg-secondary text-secondary-foreground"
                shimmer-color="rgb(139, 69, 19)"
                @click="clearContent"
              >
                Clear All
              </ShimmerButton>
            </div>
          </div>

          <!-- Generation Options -->
          <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div class="space-y-2">
              <label class="text-sm font-medieval text-foreground">Quantity</label>
              <select 
                v-model="generationOptions.quantity"
                class="w-full p-2 rounded bg-background border border-border text-foreground"
              >
                <option value="1">1</option>
                <option value="3">3</option>
                <option value="5">5</option>
                <option value="10">10</option>
              </select>
            </div>
            
            <div class="space-y-2">
              <label class="text-sm font-medieval text-foreground">Quality</label>
              <select 
                v-model="generationOptions.quality"
                class="w-full p-2 rounded bg-background border border-border text-foreground"
              >
                <option value="common">Common</option>
                <option value="uncommon">Uncommon</option>
                <option value="rare">Rare</option>
                <option value="legendary">Legendary</option>
              </select>
            </div>
            
            <div class="space-y-2" v-if="selectedGenerator === 'npc'">
              <label class="text-sm font-medieval text-foreground">Type</label>
              <select 
                v-model="generationOptions.npcType"
                class="w-full p-2 rounded bg-background border border-border text-foreground"
              >
                <option value="random">Random</option>
                <option value="tavern">Tavern Patron</option>
                <option value="merchant">Merchant</option>
                <option value="guard">Guard</option>
              </select>
            </div>
            
            <div class="space-y-2" v-if="selectedGenerator === 'quest'">
              <label class="text-sm font-medieval text-foreground">Type</label>
              <select 
                v-model="generationOptions.questType"
                class="w-full p-2 rounded bg-background border border-border text-foreground"
              >
                <option value="tavern">Tavern Quest</option>
                <option value="faction">Faction Quest</option>
                <option value="personal">Personal Quest</option>
                <option value="random">Random</option>
              </select>
            </div>
            
            <div class="space-y-2" v-if="selectedGenerator === 'item'">
              <label class="text-sm font-medieval text-foreground">Type</label>
              <select 
                v-model="generationOptions.itemType"
                class="w-full p-2 rounded bg-background border border-border text-foreground"
              >
                <option value="random">Random</option>
                <option value="weapon">Weapon</option>
                <option value="armor">Armor</option>
                <option value="tool">Tool</option>
                <option value="consumable">Consumable</option>
                <option value="magical">Magical</option>
              </select>
            </div>
          </div>
        </div>
      </BorderBeam>

      <!-- Generated Content Display -->
      <div v-if="generatedContent.length > 0" class="space-y-4">
        <h3 class="text-xl font-medieval text-foreground">Generated Content</h3>
        
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <Card3D 
            v-for="(content, index) in generatedContent" 
            :key="content.id"
            class="inspira-card-character p-6"
            :rotation-intensity="5"
          >
            <!-- NPC Display -->
            <div v-if="selectedGenerator === 'npc'" class="space-y-4">
              <div class="flex items-center justify-between">
                <h4 class="text-lg font-medieval text-foreground">{{ content.name }}</h4>
                <div class="text-xs text-primary">{{ content.career?.name }}</div>
              </div>
              
              <div class="space-y-2 text-sm">
                <p><span class="font-medieval text-muted-foreground">Class:</span> {{ content.career?.class }}</p>
                <p><span class="font-medieval text-muted-foreground">Faction:</span> {{ content.faction }}</p>
                <p><span class="font-medieval text-muted-foreground">Personality:</span> {{ content.personality }}</p>
                <p><span class="font-medieval text-muted-foreground">Background:</span> {{ content.background }}</p>
              </div>
              
              <div v-if="content.hooks?.length > 0" class="space-y-2">
                <h5 class="font-medieval text-foreground">Quest Hooks:</h5>
                <ul class="text-xs space-y-1">
                  <li v-for="hook in content.hooks" :key="hook.description" class="text-muted-foreground">
                    • {{ hook.description }}
                  </li>
                </ul>
              </div>
            </div>

            <!-- Quest Display -->
            <div v-if="selectedGenerator === 'quest'" class="space-y-4">
              <div class="flex items-center justify-between">
                <h4 class="text-lg font-medieval text-foreground">{{ content.title }}</h4>
                <div class="text-xs text-primary">{{ content.difficulty }}</div>
              </div>
              
              <p class="text-sm text-muted-foreground">{{ content.description }}</p>
              
              <div class="space-y-2">
                <h5 class="font-medieval text-foreground">Objectives:</h5>
                <ul class="text-xs space-y-1">
                  <li v-for="objective in content.objectives" :key="objective.id" class="text-muted-foreground">
                    • {{ objective.description }}
                  </li>
                </ul>
              </div>
              
              <div class="space-y-2">
                <h5 class="font-medieval text-foreground">Rewards:</h5>
                <ul class="text-xs space-y-1">
                  <li v-for="reward in content.rewards" :key="reward.description" class="text-muted-foreground">
                    • {{ reward.description }}
                  </li>
                </ul>
              </div>
            </div>

            <!-- Item Display -->
            <div v-if="selectedGenerator === 'item'" class="space-y-4">
              <div class="flex items-center justify-between">
                <h4 class="text-lg font-medieval text-foreground">{{ content.name }}</h4>
                <div class="text-xs text-primary">{{ content.type }}</div>
              </div>
              
              <p class="text-sm text-muted-foreground">{{ content.description }}</p>
              
              <div class="grid grid-cols-2 gap-2 text-xs">
                <div><span class="font-medieval text-muted-foreground">Price:</span> {{ content.price }}gc</div>
                <div><span class="font-medieval text-muted-foreground">Rarity:</span> {{ content.rarity }}/10</div>
                <div><span class="font-medieval text-muted-foreground">Condition:</span> {{ content.condition }}</div>
                <div><span class="font-medieval text-muted-foreground">Origin:</span> {{ content.culturalOrigin }}</div>
              </div>
              
              <div v-if="content.enchantment" class="space-y-1">
                <h5 class="font-medieval text-foreground text-xs">Enchantment:</h5>
                <p class="text-xs text-primary">{{ content.enchantment.name }}</p>
                <p class="text-xs text-muted-foreground">{{ content.enchantment.description }}</p>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="flex gap-2 pt-4 border-t border-border/40">
              <button 
                @click="exportContent(content)"
                class="flex-1 text-xs px-3 py-2 bg-primary/20 text-primary rounded hover:bg-primary/30 transition-colors"
              >
                Export
              </button>
              <button 
                @click="duplicateContent(content)"
                class="flex-1 text-xs px-3 py-2 bg-secondary/20 text-secondary-foreground rounded hover:bg-secondary/30 transition-colors"
              >
                Duplicate
              </button>
              <button 
                @click="removeContent(index)"
                class="flex-1 text-xs px-3 py-2 bg-destructive/20 text-destructive rounded hover:bg-destructive/30 transition-colors"
              >
                Remove
              </button>
            </div>
          </Card3D>
        </div>
      </div>

      <!-- Empty State -->
      <div v-else class="text-center py-12">
        <Icon name="sparkles" class="w-16 h-16 mx-auto text-muted-foreground mb-4" />
        <h3 class="text-lg font-medieval text-foreground mb-2">No Content Generated</h3>
        <p class="text-muted-foreground">Click "Generate" to create new content using the Warhammer Polish plugin data.</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
// Page metadata
useHead({
  title: 'Content Generators - Warhammer Tavern Simulator v3',
  meta: [
    { name: 'description', content: 'Generate authentic Warhammer Fantasy content including NPCs, quests, items, and narrative elements using comprehensive Polish plugin data.' }
  ]
})

// Import composables
const { generateRandomNPC, generateTavernPatron, generateMerchant, generateGuard } = useNPCGenerator()
const { generateRandomQuest, generateTavernQuest, generateCareerQuest } = useQuestGenerator()
const { generateWeapon, generateArmor, generateTool, generateConsumable, generateMagicalItem } = useItemGenerator()

// Generator definitions
const generators = ref([
  {
    id: 'npc',
    name: 'NPC Generator',
    description: 'Create detailed NPCs with careers, personalities, and quest hooks',
    icon: 'users',
    count: 0
  },
  {
    id: 'quest',
    name: 'Quest Generator',
    description: 'Generate dynamic quests and adventures with objectives and rewards',
    icon: 'scroll',
    count: 0
  },
  {
    id: 'item',
    name: 'Item Generator',
    description: 'Create weapons, armor, tools, and magical items with authentic properties',
    icon: 'sword',
    count: 0
  },
  {
    id: 'narrative',
    name: 'Narrative Generator',
    description: 'Generate rumors, atmosphere, and story elements for immersion',
    icon: 'book-open',
    count: 0
  }
])

// State
const selectedGenerator = ref<string>('')
const generatedContent = ref<any[]>([])
const isGenerating = ref(false)

const generationOptions = ref({
  quantity: 1,
  quality: 'common',
  npcType: 'random',
  questType: 'tavern',
  itemType: 'random'
})

// Computed
const currentGenerator = computed(() => 
  generators.value.find(g => g.id === selectedGenerator.value)
)

// Methods
const selectGenerator = (id: string) => {
  selectedGenerator.value = id
  generatedContent.value = []
}

const generateContent = async () => {
  if (!selectedGenerator.value) return
  
  isGenerating.value = true
  
  try {
    const quantity = parseInt(generationOptions.value.quantity.toString())
    const newContent = []
    
    for (let i = 0; i < quantity; i++) {
      let content
      
      switch (selectedGenerator.value) {
        case 'npc':
          content = generateNPC()
          break
        case 'quest':
          content = generateQuest()
          break
        case 'item':
          content = generateItem()
          break
        case 'narrative':
          content = generateNarrative()
          break
      }
      
      if (content) {
        newContent.push(content)
      }
    }
    
    generatedContent.value.push(...newContent)
    
    // Update count
    const generator = generators.value.find(g => g.id === selectedGenerator.value)
    if (generator) {
      generator.count += newContent.length
    }
    
  } catch (error) {
    console.error('Generation error:', error)
  } finally {
    isGenerating.value = false
  }
}

const generateNPC = () => {
  switch (generationOptions.value.npcType) {
    case 'tavern':
      return generateTavernPatron()
    case 'merchant':
      return generateMerchant()
    case 'guard':
      return generateGuard()
    default:
      return generateRandomNPC()
  }
}

const generateQuest = () => {
  switch (generationOptions.value.questType) {
    case 'tavern':
      return generateTavernQuest()
    case 'faction':
      return generateRandomQuest('faction')
    case 'personal':
      return generateRandomQuest('personal')
    default:
      return generateRandomQuest()
  }
}

const generateItem = () => {
  switch (generationOptions.value.itemType) {
    case 'weapon':
      return generateWeapon()
    case 'armor':
      return generateArmor()
    case 'tool':
      return generateTool()
    case 'consumable':
      return generateConsumable()
    case 'magical':
      return generateMagicalItem()
    default:
      // Random type
      const types = ['weapon', 'armor', 'tool', 'consumable']
      const randomType = types[Math.floor(Math.random() * types.length)]
      switch (randomType) {
        case 'weapon': return generateWeapon()
        case 'armor': return generateArmor()
        case 'tool': return generateTool()
        case 'consumable': return generateConsumable()
      }
  }
}

const generateNarrative = () => {
  // Placeholder for narrative generator
  return {
    id: `narrative_${Date.now()}`,
    type: 'rumor',
    content: 'Strange lights have been seen in the old forest at night...',
    mood: 'mysterious',
    source: 'tavern gossip'
  }
}

const clearContent = () => {
  generatedContent.value = []
}

const exportContent = (content: any) => {
  const dataStr = JSON.stringify(content, null, 2)
  const dataBlob = new Blob([dataStr], { type: 'application/json' })
  const url = URL.createObjectURL(dataBlob)
  const link = document.createElement('a')
  link.href = url
  link.download = `${selectedGenerator.value}_${content.name || content.title || content.id}.json`
  link.click()
  URL.revokeObjectURL(url)
}

const duplicateContent = (content: any) => {
  const duplicate = { ...content, id: `${content.id}_copy_${Date.now()}` }
  generatedContent.value.push(duplicate)
}

const removeContent = (index: number) => {
  generatedContent.value.splice(index, 1)
}

// Initialize with NPC generator
onMounted(() => {
  selectedGenerator.value = 'npc'
})
</script>

<style scoped>
.inspira-card-character {
  background: linear-gradient(135deg, 
    rgba(139, 69, 19, 0.1), 
    rgba(160, 82, 45, 0.1));
  border: 1px solid rgba(255, 215, 0, 0.2);
}

.inspira-card-character:hover {
  border-color: rgba(255, 215, 0, 0.4);
  box-shadow: 0 8px 32px rgba(255, 215, 0, 0.1);
}

select {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' fill='none' viewBox='0 0 20 20'%3e%3cpath stroke='%236b7280' stroke-linecap='round' stroke-linejoin='round' stroke-width='1.5' d='m6 8 4 4 4-4'/%3e%3c/svg%3e");
  background-position: right 0.5rem center;
  background-repeat: no-repeat;
  background-size: 1.5em 1.5em;
  padding-right: 2.5rem;
}
</style>
