/**
 * Enhanced User Engagement Features for Warhammer Tavern v3
 * Character progression, real-time events, social influence, inventory, and customization
 */

export interface PlayerCharacter {
  id: string
  name: string
  level: number
  experience: number
  experienceToNext: number
  attributes: {
    charisma: number
    intelligence: number
    strength: number
    dexterity: number
    constitution: number
    wisdom: number
  }
  skills: Record<string, number>
  titles: string[]
  backstory: string
  appearance: {
    avatar: string
    clothing: string[]
    accessories: string[]
  }
}

export interface InventoryItem {
  id: string
  name: string
  type: 'weapon' | 'armor' | 'consumable' | 'quest' | 'valuable' | 'tool'
  rarity: 'common' | 'uncommon' | 'rare' | 'epic' | 'legendary'
  description: string
  value: number
  weight: number
  quantity: number
  properties?: Record<string, any>
  isEquipped?: boolean
}

export interface TavernCustomization {
  theme: 'rustic' | 'elegant' | 'mysterious' | 'martial' | 'scholarly'
  decorations: string[]
  furniture: string[]
  lighting: 'dim' | 'warm' | 'bright'
  music: 'tavern_songs' | 'classical' | 'folk' | 'none'
  specialFeatures: string[]
  reputation: number
  patronSatisfaction: number
}

export interface RealTimeEvent {
  id: string
  type: 'social' | 'economic' | 'political' | 'supernatural' | 'weather'
  title: string
  description: string
  startTime: Date
  duration: number // minutes
  effects: {
    reputation?: number
    economy?: Record<string, number>
    npcMoods?: Record<string, string>
    questAvailability?: string[]
    customization?: Partial<TavernCustomization>
  }
  isActive: boolean
  participantCount: number
  playerParticipated: boolean
}

export interface SocialInfluence {
  networkSize: number
  influencePoints: number
  socialConnections: Record<string, {
    strength: number
    type: 'friend' | 'rival' | 'mentor' | 'student' | 'business'
    lastInteraction: Date
  }>
  rumors: {
    id: string
    content: string
    credibility: number
    spread: number
    source: string
  }[]
  socialStatus: 'unknown' | 'known' | 'respected' | 'influential' | 'legendary'
}

export const useEnhancedUserEngagement = () => {
  // Reactive state
  const playerCharacter = ref<PlayerCharacter>({
    id: 'player_1',
    name: 'Adventurer',
    level: 1,
    experience: 0,
    experienceToNext: 100,
    attributes: {
      charisma: 10,
      intelligence: 10,
      strength: 10,
      dexterity: 10,
      constitution: 10,
      wisdom: 10
    },
    skills: {
      'Persuasion': 0,
      'Intimidation': 0,
      'Deception': 0,
      'Investigation': 0,
      'Insight': 0,
      'Performance': 0
    },
    titles: [],
    backstory: '',
    appearance: {
      avatar: 'default',
      clothing: ['simple_tunic', 'leather_boots'],
      accessories: []
    }
  })

  const inventory = ref<InventoryItem[]>([
    {
      id: 'starting_coin_purse',
      name: 'Coin Purse',
      type: 'valuable',
      rarity: 'common',
      description: 'A simple leather purse containing your starting funds.',
      value: 50,
      weight: 0.5,
      quantity: 1
    },
    {
      id: 'traveler_cloak',
      name: 'Traveler\'s Cloak',
      type: 'armor',
      rarity: 'common',
      description: 'A worn but serviceable cloak for protection against the elements.',
      value: 15,
      weight: 2,
      quantity: 1,
      isEquipped: true
    }
  ])

  const tavernCustomization = ref<TavernCustomization>({
    theme: 'rustic',
    decorations: ['wooden_tables', 'stone_fireplace'],
    furniture: ['oak_bar', 'simple_stools'],
    lighting: 'warm',
    music: 'tavern_songs',
    specialFeatures: [],
    reputation: 50,
    patronSatisfaction: 75
  })

  const activeEvents = ref<RealTimeEvent[]>([])
  const eventHistory = ref<RealTimeEvent[]>([])
  const socialInfluence = ref<SocialInfluence>({
    networkSize: 0,
    influencePoints: 0,
    socialConnections: {},
    rumors: [],
    socialStatus: 'unknown'
  })

  const isLevelingUp = ref(false)
  const availableUpgrades = ref<string[]>([])

  // Character progression
  const gainExperience = (amount: number, source: string = 'general') => {
    playerCharacter.value.experience += amount
    
    // Check for level up
    while (playerCharacter.value.experience >= playerCharacter.value.experienceToNext) {
      levelUp()
    }
    
    // Track experience sources for analytics
    console.log(`Gained ${amount} XP from ${source}`)
  }

  const levelUp = () => {
    isLevelingUp.value = true
    playerCharacter.value.level++
    playerCharacter.value.experience -= playerCharacter.value.experienceToNext
    playerCharacter.value.experienceToNext = Math.floor(playerCharacter.value.experienceToNext * 1.2)
    
    // Generate available upgrades
    generateUpgradeOptions()
  }

  const generateUpgradeOptions = () => {
    const options = [
      'increase_charisma',
      'increase_intelligence', 
      'increase_strength',
      'improve_persuasion',
      'improve_investigation',
      'new_title',
      'special_ability'
    ]
    
    availableUpgrades.value = options
      .sort(() => Math.random() - 0.5)
      .slice(0, 3)
  }

  const selectUpgrade = (upgrade: string) => {
    switch (upgrade) {
      case 'increase_charisma':
        playerCharacter.value.attributes.charisma += 1
        break
      case 'increase_intelligence':
        playerCharacter.value.attributes.intelligence += 1
        break
      case 'increase_strength':
        playerCharacter.value.attributes.strength += 1
        break
      case 'improve_persuasion':
        playerCharacter.value.skills.Persuasion += 5
        break
      case 'improve_investigation':
        playerCharacter.value.skills.Investigation += 5
        break
      case 'new_title':
        const titles = ['Storyteller', 'Peacemaker', 'Investigator', 'Diplomat']
        const newTitle = titles[Math.floor(Math.random() * titles.length)]
        if (!playerCharacter.value.titles.includes(newTitle)) {
          playerCharacter.value.titles.push(newTitle)
        }
        break
    }
    
    isLevelingUp.value = false
    availableUpgrades.value = []
  }

  // Inventory management
  const addItem = (item: Omit<InventoryItem, 'id'>): string => {
    const newItem: InventoryItem = {
      ...item,
      id: `item_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`
    }
    
    // Check if item already exists and is stackable
    const existingItem = inventory.value.find(i => 
      i.name === item.name && 
      i.type === item.type && 
      i.rarity === item.rarity
    )
    
    if (existingItem && ['consumable', 'valuable'].includes(item.type)) {
      existingItem.quantity += item.quantity
      return existingItem.id
    } else {
      inventory.value.push(newItem)
      return newItem.id
    }
  }

  const removeItem = (itemId: string, quantity: number = 1): boolean => {
    const itemIndex = inventory.value.findIndex(i => i.id === itemId)
    if (itemIndex === -1) return false
    
    const item = inventory.value[itemIndex]
    
    if (item.quantity <= quantity) {
      inventory.value.splice(itemIndex, 1)
    } else {
      item.quantity -= quantity
    }
    
    return true
  }

  const equipItem = (itemId: string): boolean => {
    const item = inventory.value.find(i => i.id === itemId)
    if (!item || !['weapon', 'armor'].includes(item.type)) return false
    
    // Unequip other items of same type
    inventory.value.forEach(i => {
      if (i.type === item.type && i.isEquipped) {
        i.isEquipped = false
      }
    })
    
    item.isEquipped = true
    return true
  }

  const getInventoryValue = (): number => {
    return inventory.value.reduce((total, item) => total + (item.value * item.quantity), 0)
  }

  const getInventoryWeight = (): number => {
    return inventory.value.reduce((total, item) => total + (item.weight * item.quantity), 0)
  }

  // Tavern customization
  const upgradeTavern = (upgrade: keyof TavernCustomization, value: any): boolean => {
    const upgradeCosts = {
      theme: 100,
      lighting: 50,
      music: 30,
      decorations: 75,
      furniture: 150
    }
    
    const cost = upgradeCosts[upgrade as keyof typeof upgradeCosts] || 50
    
    // Check if player can afford (would integrate with economy system)
    // For now, assume they can afford it
    
    if (upgrade === 'decorations' || upgrade === 'furniture') {
      const currentArray = tavernCustomization.value[upgrade] as string[]
      if (!currentArray.includes(value)) {
        currentArray.push(value)
      }
    } else {
      (tavernCustomization.value as any)[upgrade] = value
    }
    
    // Increase tavern reputation
    tavernCustomization.value.reputation += 5
    
    return true
  }

  const calculateTavernEffects = () => {
    const customization = tavernCustomization.value
    let effects = {
      reputationBonus: 0,
      economyBonus: 0,
      npcMoodBonus: 0
    }
    
    // Theme effects
    switch (customization.theme) {
      case 'elegant':
        effects.reputationBonus += 10
        effects.economyBonus += 0.2
        break
      case 'martial':
        effects.npcMoodBonus += 5
        break
      case 'scholarly':
        effects.reputationBonus += 5
        break
    }
    
    // Decoration effects
    effects.reputationBonus += customization.decorations.length * 2
    effects.economyBonus += customization.furniture.length * 0.05
    
    return effects
  }

  // Real-time events
  const generateRandomEvent = (): RealTimeEvent => {
    const eventTemplates = [
      {
        type: 'social' as const,
        title: 'Traveling Merchant Arrives',
        description: 'A wealthy merchant has arrived with exotic goods and tales from distant lands.',
        duration: 60,
        effects: {
          economy: { 'exotic_goods': 0.8 },
          npcMoods: { 'merchant_npcs': 'excited' }
        }
      },
      {
        type: 'weather' as const,
        title: 'Heavy Rain Storm',
        description: 'A fierce storm drives more patrons inside, creating a cozy but crowded atmosphere.',
        duration: 120,
        effects: {
          reputation: 5,
          customization: { patronSatisfaction: 85 }
        }
      },
      {
        type: 'political' as const,
        title: 'News from the Capital',
        description: 'A messenger brings important news that has everyone talking.',
        duration: 90,
        effects: {
          npcMoods: { 'all': 'curious' },
          questAvailability: ['political_intrigue_quest']
        }
      },
      {
        type: 'supernatural' as const,
        title: 'Strange Lights in the Sky',
        description: 'Mysterious lights appear overhead, causing unease among the patrons.',
        duration: 45,
        effects: {
          npcMoods: { 'superstitious_npcs': 'nervous' },
          questAvailability: ['investigate_lights_quest']
        }
      }
    ]
    
    const template = eventTemplates[Math.floor(Math.random() * eventTemplates.length)]
    
    return {
      id: `event_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      ...template,
      startTime: new Date(),
      isActive: true,
      participantCount: 0,
      playerParticipated: false
    }
  }

  const startRandomEvent = () => {
    const event = generateRandomEvent()
    activeEvents.value.push(event)
    
    // Set timer to end event
    setTimeout(() => {
      endEvent(event.id)
    }, event.duration * 60 * 1000)
    
    return event
  }

  const participateInEvent = (eventId: string): boolean => {
    const event = activeEvents.value.find(e => e.id === eventId)
    if (!event || !event.isActive || event.playerParticipated) return false
    
    event.playerParticipated = true
    event.participantCount++
    
    // Apply event effects
    if (event.effects.reputation) {
      // Would integrate with reputation system
      gainExperience(10, 'event_participation')
    }
    
    // Gain social influence
    socialInfluence.value.influencePoints += 5
    
    return true
  }

  const endEvent = (eventId: string) => {
    const eventIndex = activeEvents.value.findIndex(e => e.id === eventId)
    if (eventIndex === -1) return
    
    const event = activeEvents.value[eventIndex]
    event.isActive = false
    
    // Move to history
    eventHistory.value.push(event)
    activeEvents.value.splice(eventIndex, 1)
    
    // Keep only last 50 events in history
    if (eventHistory.value.length > 50) {
      eventHistory.value = eventHistory.value.slice(-50)
    }
  }

  // Social influence system
  const addSocialConnection = (npcId: string, type: SocialInfluence['socialConnections'][string]['type'], strength: number = 1) => {
    socialInfluence.value.socialConnections[npcId] = {
      strength,
      type,
      lastInteraction: new Date()
    }
    
    socialInfluence.value.networkSize = Object.keys(socialInfluence.value.socialConnections).length
    updateSocialStatus()
  }

  const strengthenConnection = (npcId: string, amount: number = 1) => {
    const connection = socialInfluence.value.socialConnections[npcId]
    if (connection) {
      connection.strength = Math.min(100, connection.strength + amount)
      connection.lastInteraction = new Date()
      socialInfluence.value.influencePoints += amount
    }
  }

  const spreadRumor = (content: string, source: string = 'player') => {
    const rumor = {
      id: `rumor_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      content,
      credibility: Math.floor(Math.random() * 100),
      spread: 1,
      source
    }
    
    socialInfluence.value.rumors.push(rumor)
    
    // Rumors spread based on social network
    const spreadRate = Math.min(socialInfluence.value.networkSize * 0.1, 1)
    rumor.spread = Math.floor(rumor.spread * (1 + spreadRate))
    
    return rumor.id
  }

  const updateSocialStatus = () => {
    const influence = socialInfluence.value
    
    if (influence.influencePoints >= 1000) {
      influence.socialStatus = 'legendary'
    } else if (influence.influencePoints >= 500) {
      influence.socialStatus = 'influential'
    } else if (influence.influencePoints >= 200) {
      influence.socialStatus = 'respected'
    } else if (influence.influencePoints >= 50) {
      influence.socialStatus = 'known'
    } else {
      influence.socialStatus = 'unknown'
    }
  }

  // Achievement system
  const checkAchievements = () => {
    const achievements: string[] = []
    
    // Level-based achievements
    if (playerCharacter.value.level >= 5) achievements.push('experienced_adventurer')
    if (playerCharacter.value.level >= 10) achievements.push('veteran_patron')
    
    // Social achievements
    if (socialInfluence.value.networkSize >= 10) achievements.push('social_butterfly')
    if (socialInfluence.value.influencePoints >= 100) achievements.push('influential_figure')
    
    // Inventory achievements
    if (inventory.value.length >= 20) achievements.push('collector')
    if (inventory.value.some(i => i.rarity === 'legendary')) achievements.push('legendary_owner')
    
    // Tavern achievements
    if (tavernCustomization.value.reputation >= 100) achievements.push('renowned_establishment')
    
    return achievements
  }

  // Auto-save progress
  const saveProgress = () => {
    const saveData = {
      playerCharacter: playerCharacter.value,
      inventory: inventory.value,
      tavernCustomization: tavernCustomization.value,
      socialInfluence: socialInfluence.value,
      timestamp: new Date()
    }
    
    localStorage.setItem('warhammer_tavern_save', JSON.stringify(saveData))
  }

  const loadProgress = () => {
    const saveData = localStorage.getItem('warhammer_tavern_save')
    if (saveData) {
      try {
        const parsed = JSON.parse(saveData)
        playerCharacter.value = parsed.playerCharacter
        inventory.value = parsed.inventory
        tavernCustomization.value = parsed.tavernCustomization
        socialInfluence.value = parsed.socialInfluence
      } catch (error) {
        console.error('Failed to load save data:', error)
      }
    }
  }

  // Initialize systems
  const initializeEngagementSystems = () => {
    loadProgress()
    
    // Start periodic events
    setInterval(() => {
      if (Math.random() < 0.3) { // 30% chance every interval
        startRandomEvent()
      }
    }, 5 * 60 * 1000) // Every 5 minutes
    
    // Auto-save every 30 seconds
    setInterval(saveProgress, 30 * 1000)
  }

  return {
    // State
    playerCharacter: readonly(playerCharacter),
    inventory: readonly(inventory),
    tavernCustomization: readonly(tavernCustomization),
    activeEvents: readonly(activeEvents),
    eventHistory: readonly(eventHistory),
    socialInfluence: readonly(socialInfluence),
    isLevelingUp: readonly(isLevelingUp),
    availableUpgrades: readonly(availableUpgrades),
    
    // Methods
    gainExperience,
    selectUpgrade,
    addItem,
    removeItem,
    equipItem,
    getInventoryValue,
    getInventoryWeight,
    upgradeTavern,
    calculateTavernEffects,
    startRandomEvent,
    participateInEvent,
    addSocialConnection,
    strengthenConnection,
    spreadRumor,
    checkAchievements,
    saveProgress,
    loadProgress,
    initializeEngagementSystems
  }
}
