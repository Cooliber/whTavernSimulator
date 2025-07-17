/**
 * Warhammer Fantasy Data Management Composable
 * Provides access to careers, trappings, bestiary, and other game data
 */

export interface WarhammerCareer {
  id: string
  name: string
  skills: string[]
  talents: string[]
  trappings: string[]
  description: string
  class?: string
  careergroup?: string
}

export interface WarhammerTrapping {
  id: string
  name: string
  description: string
  type?: string
  cost?: string
  availability?: string
}

export interface WarhammerCreature {
  id: string
  name: string
  characteristics?: {
    ws?: number
    bs?: number
    s?: number
    t?: number
    i?: number
    ag?: number
    dex?: number
    int?: number
    wp?: number
    fel?: number
  }
  traits?: string[]
  skills?: string[]
  talents?: string[]
  description?: string
}

export interface WarhammerSpell {
  id: string
  name: string
  cn?: number
  range?: string
  target?: string
  duration?: string
  description: string
  lore?: string
}

export interface TavernItem {
  id: string
  name: string
  description: string
  price?: string
  type: 'drink' | 'food' | 'service' | 'room' | 'entertainment'
  availability?: 'common' | 'uncommon' | 'rare' | 'exotic'
}

export const useWarhammerData = () => {
  // Reactive data stores
  const careers = ref<WarhammerCareer[]>([])
  const trappings = ref<WarhammerTrapping[]>([])
  const creatures = ref<WarhammerCreature[]>([])
  const spells = ref<WarhammerSpell[]>([])
  const tavernItems = ref<TavernItem[]>([])
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Load careers data
  const loadCareers = async () => {
    try {
      isLoading.value = true
      const { data } = await $fetch('/api/warhammer/careers')
      
      if (data?.entries) {
        careers.value = data.entries.map((entry: any) => ({
          id: entry.id,
          name: entry.name,
          skills: Array.isArray(entry.skills) ? entry.skills : [],
          talents: Array.isArray(entry.talents) ? entry.talents : [],
          trappings: Array.isArray(entry.trappings) ? entry.trappings : [],
          description: entry.description || '',
          class: entry.class,
          careergroup: entry.careergroup
        }))
      }
    } catch (err) {
      error.value = 'Failed to load careers data'
      console.error('Error loading careers:', err)
    } finally {
      isLoading.value = false
    }
  }

  // Load trappings (tavern items, equipment, etc.)
  const loadTrappings = async () => {
    try {
      isLoading.value = true
      const { data } = await $fetch('/api/warhammer/trappings')
      
      if (data?.entries) {
        trappings.value = data.entries.map((entry: any) => ({
          id: entry.id,
          name: entry.name,
          description: entry.description || '',
          type: entry.type,
          cost: entry.cost,
          availability: entry.availability
        }))

        // Create tavern-specific items from trappings
        tavernItems.value = createTavernItems(trappings.value)
      }
    } catch (err) {
      error.value = 'Failed to load trappings data'
      console.error('Error loading trappings:', err)
    } finally {
      isLoading.value = false
    }
  }

  // Load bestiary data
  const loadBestiary = async () => {
    try {
      isLoading.value = true
      const { data } = await $fetch('/api/warhammer/bestiary')
      
      if (data?.entries) {
        creatures.value = data.entries.map((entry: any) => ({
          id: entry.id,
          name: entry.name,
          characteristics: entry.characteristics,
          traits: Array.isArray(entry.traits) ? entry.traits : [],
          skills: Array.isArray(entry.skills) ? entry.skills : [],
          talents: Array.isArray(entry.talents) ? entry.talents : [],
          description: entry.description || ''
        }))
      }
    } catch (err) {
      error.value = 'Failed to load bestiary data'
      console.error('Error loading bestiary:', err)
    } finally {
      isLoading.value = false
    }
  }

  // Load spells data
  const loadSpells = async () => {
    try {
      isLoading.value = true
      const { data } = await $fetch('/api/warhammer/spells')
      
      if (data?.entries) {
        spells.value = data.entries.map((entry: any) => ({
          id: entry.id,
          name: entry.name,
          cn: entry.cn,
          range: entry.range,
          target: entry.target,
          duration: entry.duration,
          description: entry.description || '',
          lore: entry.lore
        }))
      }
    } catch (err) {
      error.value = 'Failed to load spells data'
      console.error('Error loading spells:', err)
    } finally {
      isLoading.value = false
    }
  }

  // Create tavern-specific items from trappings
  const createTavernItems = (trappings: WarhammerTrapping[]): TavernItem[] => {
    const tavernKeywords = ['ale', 'beer', 'wine', 'bread', 'meal', 'room', 'bed', 'entertainment']
    
    return trappings
      .filter(item => 
        tavernKeywords.some(keyword => 
          item.name.toLowerCase().includes(keyword) || 
          item.description.toLowerCase().includes(keyword)
        )
      )
      .map(item => ({
        id: item.id,
        name: item.name,
        description: item.description,
        price: item.cost,
        type: determineTavernItemType(item),
        availability: determineAvailability(item)
      }))
  }

  // Determine tavern item type
  const determineTavernItemType = (item: WarhammerTrapping): TavernItem['type'] => {
    const name = item.name.toLowerCase()
    const desc = item.description.toLowerCase()
    
    if (name.includes('ale') || name.includes('beer') || name.includes('wine')) return 'drink'
    if (name.includes('bread') || name.includes('meal') || name.includes('food')) return 'food'
    if (name.includes('room') || name.includes('bed')) return 'room'
    if (name.includes('entertainment') || name.includes('music')) return 'entertainment'
    return 'service'
  }

  // Determine item availability
  const determineAvailability = (item: WarhammerTrapping): TavernItem['availability'] => {
    const desc = item.description.toLowerCase()
    if (desc.includes('rare') || desc.includes('exotic')) return 'rare'
    if (desc.includes('uncommon')) return 'uncommon'
    return 'common'
  }

  // Search functions
  const searchCareers = (query: string) => {
    return careers.value.filter(career =>
      career.name.toLowerCase().includes(query.toLowerCase()) ||
      career.skills.some(skill => skill.toLowerCase().includes(query.toLowerCase())) ||
      career.talents.some(talent => talent.toLowerCase().includes(query.toLowerCase()))
    )
  }

  const searchCreatures = (query: string) => {
    return creatures.value.filter(creature =>
      creature.name.toLowerCase().includes(query.toLowerCase()) ||
      creature.traits?.some(trait => trait.toLowerCase().includes(query.toLowerCase()))
    )
  }

  const searchTavernItems = (query: string, type?: TavernItem['type']) => {
    let filtered = tavernItems.value.filter(item =>
      item.name.toLowerCase().includes(query.toLowerCase()) ||
      item.description.toLowerCase().includes(query.toLowerCase())
    )
    
    if (type) {
      filtered = filtered.filter(item => item.type === type)
    }
    
    return filtered
  }

  // Get random items for tavern atmosphere
  const getRandomTavernItems = (count: number = 5, type?: TavernItem['type']) => {
    let items = type ? tavernItems.value.filter(item => item.type === type) : tavernItems.value
    return items.sort(() => Math.random() - 0.5).slice(0, count)
  }

  // Get career by ID
  const getCareerById = (id: string) => {
    return careers.value.find(career => career.id === id)
  }

  // Get creature by ID
  const getCreatureById = (id: string) => {
    return creatures.value.find(creature => creature.id === id)
  }

  // Initialize all data
  const initializeData = async () => {
    await Promise.all([
      loadCareers(),
      loadTrappings(),
      loadBestiary(),
      loadSpells()
    ])
  }

  return {
    // Data
    careers: readonly(careers),
    trappings: readonly(trappings),
    creatures: readonly(creatures),
    spells: readonly(spells),
    tavernItems: readonly(tavernItems),
    isLoading: readonly(isLoading),
    error: readonly(error),
    
    // Methods
    loadCareers,
    loadTrappings,
    loadBestiary,
    loadSpells,
    initializeData,
    searchCareers,
    searchCreatures,
    searchTavernItems,
    getRandomTavernItems,
    getCareerById,
    getCreatureById
  }
}
