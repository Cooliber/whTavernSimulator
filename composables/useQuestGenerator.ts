/**
 * Quest Generator Composable
 * Generates dynamic quests and adventures for the Warhammer Fantasy setting
 */

export interface Quest {
  id: string
  title: string
  description: string
  type: 'main' | 'side' | 'tavern' | 'personal' | 'faction'
  difficulty: 'easy' | 'medium' | 'hard' | 'legendary'
  objectives: Objective[]
  rewards: Reward[]
  npcsInvolved: string[] // NPC IDs
  locations: Location[]
  complications: Complication[]
  hooks: string[]
  timeLimit?: number // in days
  prerequisites?: string[]
  status: 'available' | 'active' | 'completed' | 'failed'
  faction?: string
  moralChoice?: boolean
}

export interface Objective {
  id: string
  description: string
  type: 'kill' | 'retrieve' | 'deliver' | 'investigate' | 'protect' | 'negotiate' | 'survive'
  target?: string
  location?: string
  quantity?: number
  completed: boolean
  optional: boolean
}

export interface Reward {
  type: 'gold' | 'item' | 'reputation' | 'information' | 'contact' | 'property'
  amount?: number
  description: string
  faction?: string
}

export interface Location {
  id: string
  name: string
  type: 'tavern' | 'dungeon' | 'city' | 'forest' | 'ruins' | 'manor' | 'temple'
  description: string
  dangers: string[]
  secrets?: string[]
}

export interface Complication {
  type: 'betrayal' | 'ambush' | 'rival' | 'time_pressure' | 'moral_dilemma' | 'false_information'
  description: string
  trigger: string
  effect: string
}

export interface Encounter {
  type: 'combat' | 'social' | 'exploration' | 'puzzle'
  description: string
  difficulty: number
  enemies?: string[]
  skillChecks?: string[]
  rewards?: string[]
}

export function useQuestGenerator() {
  // Quest templates and data
  const questTemplates = ref({
    tavern: [
      {
        title: 'Missing Person',
        description: 'A local has gone missing and their family seeks help',
        objectives: ['investigate', 'retrieve'],
        complications: ['false_information', 'rival']
      },
      {
        title: 'Merchant Protection',
        description: 'A merchant needs protection for a dangerous journey',
        objectives: ['protect', 'deliver'],
        complications: ['ambush', 'betrayal']
      },
      {
        title: 'Pest Problem',
        description: 'Creatures are threatening the local area',
        objectives: ['kill', 'investigate'],
        complications: ['time_pressure']
      }
    ],
    faction: [
      {
        title: 'Political Intrigue',
        description: 'Navigate the dangerous waters of noble politics',
        objectives: ['negotiate', 'investigate'],
        complications: ['betrayal', 'moral_dilemma']
      },
      {
        title: 'Military Campaign',
        description: 'Join a military operation against enemies of the realm',
        objectives: ['kill', 'protect'],
        complications: ['ambush', 'time_pressure']
      }
    ],
    personal: [
      {
        title: 'Family Honor',
        description: 'Restore honor to a disgraced family name',
        objectives: ['investigate', 'negotiate'],
        complications: ['moral_dilemma', 'rival']
      },
      {
        title: 'Lost Heritage',
        description: 'Discover the truth about mysterious ancestry',
        objectives: ['investigate', 'retrieve'],
        complications: ['false_information']
      }
    ]
  })

  // Location templates
  const locationTemplates = ref({
    tavern: {
      name: 'The Prancing Pony',
      description: 'A warm, welcoming tavern filled with locals and travelers',
      dangers: ['pickpockets', 'drunk patrons'],
      secrets: ['hidden room', 'smuggling operation']
    },
    dungeon: {
      name: 'Ancient Crypt',
      description: 'A dark, foreboding underground complex',
      dangers: ['undead', 'traps', 'cave-ins'],
      secrets: ['treasure chamber', 'ancient texts']
    },
    forest: {
      name: 'Drakwald Forest',
      description: 'A dense, dark forest known for its dangers',
      dangers: ['wild animals', 'bandits', 'beastmen'],
      secrets: ['druid grove', 'hidden path']
    },
    ruins: {
      name: 'Forgotten Temple',
      description: 'The crumbling remains of an ancient place of worship',
      dangers: ['unstable structure', 'guardian spirits'],
      secrets: ['holy relic', 'forbidden knowledge']
    }
  })

  // NPC motivations and quest hooks
  const questHooks = ref([
    'A desperate plea for help from a stranger',
    'Overhearing a conversation about trouble',
    'A mysterious letter delivered by a hooded figure',
    'A dying person\'s last words',
    'A reward poster on the tavern wall',
    'A chance encounter with someone in need',
    'A rumor spreading through the tavern',
    'A merchant offering a lucrative job'
  ])

  // Generate random quest
  const generateRandomQuest = (type: string = 'tavern'): Quest => {
    const templates = questTemplates.value[type] || questTemplates.value.tavern
    const template = templates[Math.floor(Math.random() * templates.length)]
    
    const quest: Quest = {
      id: `quest_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      title: generateQuestTitle(template.title),
      description: generateQuestDescription(template.description),
      type: type as any,
      difficulty: generateDifficulty(),
      objectives: generateObjectives(template.objectives),
      rewards: generateRewards(),
      npcsInvolved: [],
      locations: generateLocations(),
      complications: generateComplications(template.complications),
      hooks: generateHooks(),
      status: 'available'
    }

    // Add moral choice for certain quest types
    if (type === 'faction' || type === 'personal') {
      quest.moralChoice = Math.random() > 0.5
    }

    return quest
  }

  // Generate quest title variations
  const generateQuestTitle = (baseTitle: string): string => {
    const variations = {
      'Missing Person': [
        'The Vanished Merchant',
        'Where is the Miller\'s Daughter?',
        'The Disappeared Scholar',
        'Missing: Local Blacksmith'
      ],
      'Merchant Protection': [
        'Safe Passage Required',
        'Escort to Altdorf',
        'Dangerous Roads Ahead',
        'Caravan Guard Needed'
      ],
      'Pest Problem': [
        'Rat Infestation',
        'Wolf Pack Threat',
        'Giant Spider Menace',
        'Goblin Raiders'
      ]
    }

    const titleVariations = variations[baseTitle]
    return titleVariations 
      ? titleVariations[Math.floor(Math.random() * titleVariations.length)]
      : baseTitle
  }

  // Generate detailed quest description
  const generateQuestDescription = (baseDescription: string): string => {
    const details = [
      'The situation has become desperate.',
      'Time is running short.',
      'The local authorities are overwhelmed.',
      'Strange circumstances surround this matter.',
      'There may be more to this than meets the eye.',
      'The reward is substantial for those brave enough.',
      'Previous attempts have ended in failure.',
      'Discretion is of utmost importance.'
    ]

    const detail = details[Math.floor(Math.random() * details.length)]
    return `${baseDescription}. ${detail}`
  }

  // Generate quest difficulty
  const generateDifficulty = (): 'easy' | 'medium' | 'hard' | 'legendary' => {
    const roll = Math.random()
    if (roll < 0.4) return 'easy'
    if (roll < 0.7) return 'medium'
    if (roll < 0.9) return 'hard'
    return 'legendary'
  }

  // Generate quest objectives
  const generateObjectives = (types: string[]): Objective[] => {
    const objectives: Objective[] = []
    
    types.forEach((type, index) => {
      const objective: Objective = {
        id: `obj_${index}`,
        description: generateObjectiveDescription(type),
        type: type as any,
        completed: false,
        optional: Math.random() > 0.8 // 20% chance of optional objective
      }

      if (type === 'kill' || type === 'retrieve') {
        objective.quantity = Math.floor(Math.random() * 5) + 1
      }

      objectives.push(objective)
    })

    return objectives
  }

  // Generate objective descriptions
  const generateObjectiveDescription = (type: string): string => {
    const descriptions = {
      kill: [
        'Eliminate the threat',
        'Defeat the monsters',
        'Clear out the bandits',
        'Destroy the undead'
      ],
      retrieve: [
        'Recover the stolen goods',
        'Find the missing item',
        'Collect the evidence',
        'Gather the required materials'
      ],
      deliver: [
        'Transport the package safely',
        'Escort the person to safety',
        'Deliver the message',
        'Bring the supplies'
      ],
      investigate: [
        'Uncover the truth',
        'Gather information',
        'Solve the mystery',
        'Find the clues'
      ],
      protect: [
        'Keep the target safe',
        'Defend the location',
        'Guard the caravan',
        'Ensure safe passage'
      ],
      negotiate: [
        'Broker a peace deal',
        'Convince the parties',
        'Arrange the terms',
        'Mediate the dispute'
      ]
    }

    const typeDescriptions = descriptions[type] || ['Complete the task']
    return typeDescriptions[Math.floor(Math.random() * typeDescriptions.length)]
  }

  // Generate quest rewards
  const generateRewards = (): Reward[] => {
    const rewards: Reward[] = []
    
    // Always include gold
    rewards.push({
      type: 'gold',
      amount: Math.floor(Math.random() * 100) + 50,
      description: 'Gold crowns for your service'
    })

    // Random additional rewards
    if (Math.random() > 0.5) {
      const rewardTypes = ['item', 'reputation', 'information', 'contact']
      const type = rewardTypes[Math.floor(Math.random() * rewardTypes.length)]
      
      rewards.push({
        type: type as any,
        description: generateRewardDescription(type)
      })
    }

    return rewards
  }

  // Generate reward descriptions
  const generateRewardDescription = (type: string): string => {
    const descriptions = {
      item: [
        'A fine weapon from the armory',
        'Magical components',
        'A valuable piece of jewelry',
        'Useful equipment'
      ],
      reputation: [
        'Increased standing with the local guild',
        'Recognition from the authorities',
        'Respect among the common folk',
        'Favor with the nobility'
      ],
      information: [
        'Knowledge of hidden treasures',
        'Secrets about local politics',
        'Maps to dangerous locations',
        'Ancient lore and legends'
      ],
      contact: [
        'Introduction to a powerful ally',
        'Access to exclusive services',
        'Membership in a secret organization',
        'Connection to influential people'
      ]
    }

    const typeDescriptions = descriptions[type] || ['Something valuable']
    return typeDescriptions[Math.floor(Math.random() * typeDescriptions.length)]
  }

  // Generate quest locations
  const generateLocations = (): Location[] => {
    const locationTypes = Object.keys(locationTemplates.value)
    const selectedType = locationTypes[Math.floor(Math.random() * locationTypes.length)]
    const template = locationTemplates.value[selectedType]

    return [{
      id: `loc_${Date.now()}`,
      name: template.name,
      type: selectedType as any,
      description: template.description,
      dangers: [...template.dangers],
      secrets: template.secrets ? [...template.secrets] : undefined
    }]
  }

  // Generate quest complications
  const generateComplications = (types: string[]): Complication[] => {
    return types.map(type => ({
      type: type as any,
      description: generateComplicationDescription(type),
      trigger: generateComplicationTrigger(type),
      effect: generateComplicationEffect(type)
    }))
  }

  // Generate complication descriptions
  const generateComplicationDescription = (type: string): string => {
    const descriptions = {
      betrayal: 'Someone you trusted has their own agenda',
      ambush: 'Enemies lie in wait along your path',
      rival: 'Another group seeks the same goal',
      time_pressure: 'The situation grows more urgent',
      moral_dilemma: 'The right choice is not clear',
      false_information: 'Not everything is as it seems'
    }

    return descriptions[type] || 'An unexpected complication arises'
  }

  // Generate complication triggers
  const generateComplicationTrigger = (type: string): string => {
    const triggers = {
      betrayal: 'When you least expect it',
      ambush: 'At a vulnerable moment',
      rival: 'When you make progress',
      time_pressure: 'As time passes',
      moral_dilemma: 'When you learn the truth',
      false_information: 'Upon investigation'
    }

    return triggers[type] || 'At a critical moment'
  }

  // Generate complication effects
  const generateComplicationEffect = (type: string): string => {
    const effects = {
      betrayal: 'Trust is broken and plans must change',
      ambush: 'Combat becomes unavoidable',
      rival: 'Competition increases difficulty',
      time_pressure: 'Hasty decisions may be required',
      moral_dilemma: 'Your reputation may be affected',
      false_information: 'Previous assumptions are wrong'
    }

    return effects[type] || 'The situation becomes more complex'
  }

  // Generate quest hooks
  const generateHooks = (): string[] => {
    const numHooks = Math.floor(Math.random() * 2) + 1
    const selectedHooks = []
    
    for (let i = 0; i < numHooks; i++) {
      const hook = questHooks.value[Math.floor(Math.random() * questHooks.value.length)]
      if (!selectedHooks.includes(hook)) {
        selectedHooks.push(hook)
      }
    }
    
    return selectedHooks
  }

  // Generate career-specific quests
  const generateCareerQuest = (careerClass: string): Quest => {
    const quest = generateRandomQuest('personal')
    
    // Customize based on career
    if (careerClass === 'Warrior') {
      quest.objectives.push({
        id: 'warrior_obj',
        description: 'Prove your combat prowess',
        type: 'kill',
        completed: false,
        optional: false
      })
    } else if (careerClass === 'Academic') {
      quest.objectives.push({
        id: 'academic_obj',
        description: 'Research ancient knowledge',
        type: 'investigate',
        completed: false,
        optional: false
      })
    }

    return quest
  }

  // Generate tavern-specific quest
  const generateTavernQuest = (): Quest => {
    const quest = generateRandomQuest('tavern')
    quest.hooks = ['A patron approaches you with a worried expression']
    return quest
  }

  // Generate random encounter
  const generateRandomEncounter = (): Encounter => {
    const types = ['combat', 'social', 'exploration', 'puzzle']
    const type = types[Math.floor(Math.random() * types.length)]
    
    return {
      type: type as any,
      description: generateEncounterDescription(type),
      difficulty: Math.floor(Math.random() * 10) + 1,
      enemies: type === 'combat' ? generateEnemies() : undefined,
      skillChecks: generateSkillChecks(type),
      rewards: generateEncounterRewards()
    }
  }

  // Generate encounter descriptions
  const generateEncounterDescription = (type: string): string => {
    const descriptions = {
      combat: 'Hostile creatures block your path',
      social: 'You encounter someone who might help or hinder',
      exploration: 'An interesting location catches your attention',
      puzzle: 'A mysterious challenge requires solving'
    }

    return descriptions[type] || 'Something unexpected happens'
  }

  // Generate enemies for combat encounters
  const generateEnemies = (): string[] => {
    const enemies = ['Bandits', 'Goblins', 'Wild Animals', 'Undead', 'Cultists']
    const count = Math.floor(Math.random() * 3) + 1
    const selected = []
    
    for (let i = 0; i < count; i++) {
      selected.push(enemies[Math.floor(Math.random() * enemies.length)])
    }
    
    return selected
  }

  // Generate skill checks
  const generateSkillChecks = (type: string): string[] => {
    const skillsByType = {
      combat: ['Weapon Skill', 'Ballistic Skill', 'Athletics'],
      social: ['Charm', 'Intimidate', 'Gossip'],
      exploration: ['Perception', 'Survival', 'Climb'],
      puzzle: ['Intelligence', 'Lore', 'Trade']
    }

    return skillsByType[type] || ['Basic Skills']
  }

  // Generate encounter rewards
  const generateEncounterRewards = (): string[] => {
    const rewards = ['Experience', 'Small treasure', 'Useful information', 'New contact']
    return [rewards[Math.floor(Math.random() * rewards.length)]]
  }

  return {
    // Generation functions
    generateRandomQuest,
    generateCareerQuest,
    generateTavernQuest,
    generateRandomEncounter,
    
    // Utility functions
    generateQuestTitle,
    generateObjectives,
    generateRewards,
    generateComplications,
    
    // Templates
    questTemplates: readonly(questTemplates),
    locationTemplates: readonly(locationTemplates),
    questHooks: readonly(questHooks)
  }
}
