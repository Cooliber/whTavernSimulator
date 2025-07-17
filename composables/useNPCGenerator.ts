/**
 * NPC Generator Composable
 * Generates Warhammer Fantasy NPCs using the Polish plugin data
 */

export interface WarhammerNPC {
  id: string
  name: string
  career: Career
  characteristics: Characteristics
  skills: Skill[]
  talents: Talent[]
  equipment: Equipment[]
  background: string
  personality: string
  secrets: string[]
  hooks: QuestHook[]
  faction: string
  socialClass: 'peasant' | 'burgher' | 'noble' | 'clergy'
  wealth: number
  age: number
  appearance: string
  motivation: string
  relationships: NPCRelationship[]
}

export interface Career {
  id: string
  name: string
  class: string
  species: string[]
  status: string
  skills: string[]
  talents: string[]
  trappings: string[]
  careerPath: string[]
}

export interface Characteristics {
  weaponSkill: number
  ballisticSkill: number
  strength: number
  toughness: number
  initiative: number
  agility: number
  dexterity: number
  intelligence: number
  willpower: number
  fellowship: number
}

export interface Skill {
  id: string
  name: string
  characteristic: string
  advanced: boolean
  grouped: boolean
}

export interface Talent {
  id: string
  name: string
  description: string
  tests: string
  maxRank: number
}

export interface Equipment {
  id: string
  name: string
  type: string
  description: string
  price: number
  availability: string
  qualities: string[]
  flaws: string[]
}

export interface QuestHook {
  type: 'information' | 'task' | 'conflict' | 'mystery'
  description: string
  difficulty: 'easy' | 'medium' | 'hard'
  reward: string
}

export interface NPCRelationship {
  targetId: string
  type: 'friend' | 'enemy' | 'rival' | 'family' | 'business' | 'romantic'
  strength: number // 1-10
  description: string
}

export function useNPCGenerator() {
  // Load Warhammer data from Polish plugin
  const warhammerData = ref<any>({})
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Polish names for authentic feel
  const polishNames = {
    male: [
      'Aleksander', 'Bartosz', 'Czesław', 'Damian', 'Emil', 'Filip', 'Grzegorz', 'Henryk',
      'Igor', 'Jakub', 'Kamil', 'Łukasz', 'Marcin', 'Norbert', 'Oskar', 'Paweł',
      'Radosław', 'Sebastian', 'Tomasz', 'Wojciech', 'Zbigniew'
    ],
    female: [
      'Agnieszka', 'Barbara', 'Celina', 'Dorota', 'Ewa', 'Franciszka', 'Grażyna', 'Halina',
      'Irena', 'Joanna', 'Katarzyna', 'Lidia', 'Magdalena', 'Natalia', 'Olga', 'Paulina',
      'Regina', 'Sylwia', 'Teresa', 'Wanda', 'Zofia'
    ],
    surnames: [
      'Kowalski', 'Nowak', 'Wiśniewski', 'Dąbrowski', 'Lewandowski', 'Wójcik', 'Kamiński',
      'Kowalczyk', 'Zieliński', 'Szymański', 'Woźniak', 'Kozłowski', 'Jankowski', 'Mazur',
      'Krawczyk', 'Piotrowski', 'Grabowski', 'Nowakowski', 'Pawłowski', 'Michalski'
    ]
  }

  // Load Warhammer plugin data
  const loadWarhammerData = async () => {
    isLoading.value = true
    error.value = null

    try {
      // Load from actual plugin files using fetch
      const [careers, talents, skills, trappings, bestiary, tables] = await Promise.all([
        fetch('/plugins/warhammer-pl/compendium/wfrp4e-core.careers.json').then(r => r.json()),
        fetch('/plugins/warhammer-pl/compendium/wfrp4e-core.talents.json').then(r => r.json()),
        fetch('/plugins/warhammer-pl/compendium/wfrp4e-core.skills.json').then(r => r.json()),
        fetch('/plugins/warhammer-pl/compendium/wfrp4e-core.trappings.json').then(r => r.json()),
        fetch('/plugins/warhammer-pl/compendium/wfrp4e-core.bestiary.json').then(r => r.json()),
        fetch('/plugins/warhammer-pl/compendium/wfrp4e-core.tables.json').then(r => r.json())
      ])

      warhammerData.value = {
        careers,
        talents,
        skills,
        trappings,
        bestiary,
        tables
      }
    } catch (err) {
      error.value = 'Failed to load Warhammer data'
      console.error('Error loading Warhammer data:', err)
    } finally {
      isLoading.value = false
    }
  }

  // Generate random characteristics
  const generateCharacteristics = (career: Career): Characteristics => {
    const base = {
      weaponSkill: 20 + Math.floor(Math.random() * 20),
      ballisticSkill: 20 + Math.floor(Math.random() * 20),
      strength: 20 + Math.floor(Math.random() * 20),
      toughness: 20 + Math.floor(Math.random() * 20),
      initiative: 20 + Math.floor(Math.random() * 20),
      agility: 20 + Math.floor(Math.random() * 20),
      dexterity: 20 + Math.floor(Math.random() * 20),
      intelligence: 20 + Math.floor(Math.random() * 20),
      willpower: 20 + Math.floor(Math.random() * 20),
      fellowship: 20 + Math.floor(Math.random() * 20)
    }

    // Apply career modifiers
    if (career.class === 'Warrior') {
      base.weaponSkill += 10
      base.strength += 5
      base.toughness += 5
    } else if (career.class === 'Ranger') {
      base.ballisticSkill += 10
      base.agility += 5
      base.initiative += 5
    } else if (career.class === 'Academic') {
      base.intelligence += 10
      base.willpower += 5
    } else if (career.class === 'Burgher') {
      base.fellowship += 10
      base.intelligence += 5
    }

    return base
  }

  // Generate random name
  const generateName = (gender?: 'male' | 'female'): string => {
    const selectedGender = gender || (Math.random() > 0.5 ? 'male' : 'female')
    const firstName = polishNames[selectedGender][Math.floor(Math.random() * polishNames[selectedGender].length)]
    const surname = polishNames.surnames[Math.floor(Math.random() * polishNames.surnames.length)]
    return `${firstName} ${surname}`
  }

  // Generate personality traits
  const generatePersonality = (): string => {
    const traits = [
      'honorable and just', 'cunning and ambitious', 'loyal but naive', 'wise but cynical',
      'brave but reckless', 'cautious and methodical', 'charming but deceptive', 'gruff but kind-hearted',
      'scholarly and absent-minded', 'practical and down-to-earth', 'mysterious and aloof', 'jovial and friendly',
      'stern and disciplined', 'creative and eccentric', 'superstitious and fearful', 'proud and arrogant'
    ]
    return traits[Math.floor(Math.random() * traits.length)]
  }

  // Generate background story
  const generateBackground = (career: Career): string => {
    const backgrounds = {
      'Warrior': [
        'A veteran of many battles who seeks peace in retirement',
        'A former soldier turned mercenary looking for steady work',
        'A knight errant seeking to prove their worth',
        'A guard captain who lost their position due to politics'
      ],
      'Academic': [
        'A scholar researching ancient texts and forgotten lore',
        'A former university professor seeking practical experience',
        'A scribe who discovered dangerous knowledge',
        'A physician traveling to help those in need'
      ],
      'Burgher': [
        'A merchant seeking new trade opportunities',
        'A craftsman looking to establish a workshop',
        'A former guild member who fell from grace',
        'An innkeeper with dreams of expansion'
      ],
      'Ranger': [
        'A hunter who knows the local wilderness like the back of their hand',
        'A former scout for the military',
        'A guide who has seen too much in the deep forests',
        'A trapper seeking to trade their wares'
      ]
    }

    const careerBackgrounds = backgrounds[career.class] || backgrounds['Burgher']
    return careerBackgrounds[Math.floor(Math.random() * careerBackgrounds.length)]
  }

  // Generate secrets
  const generateSecrets = (): string[] => {
    const secrets = [
      'Has a hidden stash of coins buried outside town',
      'Is secretly in debt to dangerous people',
      'Witnessed a crime but is too afraid to report it',
      'Has a family member involved with criminals',
      'Knows the location of a lost treasure',
      'Is being blackmailed by someone in town',
      'Has a romantic affair with someone inappropriate',
      'Is secretly practicing forbidden magic',
      'Has connections to a rebel organization',
      'Knows about corruption in the local government'
    ]

    const numSecrets = Math.floor(Math.random() * 3) + 1
    const selectedSecrets = []
    for (let i = 0; i < numSecrets; i++) {
      const secret = secrets[Math.floor(Math.random() * secrets.length)]
      if (!selectedSecrets.includes(secret)) {
        selectedSecrets.push(secret)
      }
    }
    return selectedSecrets
  }

  // Generate quest hooks
  const generateQuestHooks = (npc: Partial<WarhammerNPC>): QuestHook[] => {
    const hooks: QuestHook[] = []

    // Career-based hooks
    if (npc.career?.class === 'Warrior') {
      hooks.push({
        type: 'task',
        description: 'Needs help dealing with bandits threatening local trade routes',
        difficulty: 'medium',
        reward: 'Gold and reputation with local merchants'
      })
    } else if (npc.career?.class === 'Academic') {
      hooks.push({
        type: 'information',
        description: 'Seeks adventurers to retrieve a rare book from dangerous ruins',
        difficulty: 'hard',
        reward: 'Ancient knowledge and magical components'
      })
    }

    // Secret-based hooks
    if (npc.secrets?.includes('Knows the location of a lost treasure')) {
      hooks.push({
        type: 'mystery',
        description: 'Will share treasure location in exchange for protection',
        difficulty: 'medium',
        reward: 'Share of the treasure'
      })
    }

    return hooks
  }

  // Main NPC generation function
  const generateRandomNPC = (): WarhammerNPC => {
    // Select random career (simplified for demo)
    const careers = [
      { id: 'soldier', name: 'Soldier', class: 'Warrior', species: ['Human'], status: 'Bronze', skills: ['Melee (Basic)', 'Ranged (Bow)'], talents: ['Combat Aware'], trappings: ['Sword', 'Leather Armor'], careerPath: ['Sergeant', 'Officer'] },
      { id: 'scholar', name: 'Scholar', class: 'Academic', species: ['Human'], status: 'Silver', skills: ['Language', 'Lore'], talents: ['Read/Write'], trappings: ['Books', 'Writing Kit'], careerPath: ['Wizard', 'Physician'] },
      { id: 'merchant', name: 'Merchant', class: 'Burgher', species: ['Human'], status: 'Silver', skills: ['Charm', 'Evaluate'], talents: ['Dealmaker'], trappings: ['Trade Goods'], careerPath: ['Guild Master', 'Noble'] },
      { id: 'hunter', name: 'Hunter', class: 'Ranger', species: ['Human'], status: 'Bronze', skills: ['Track', 'Survival'], talents: ['Marksman'], trappings: ['Bow', 'Hunting Knife'], careerPath: ['Scout', 'Bounty Hunter'] }
    ]

    const career = careers[Math.floor(Math.random() * careers.length)]
    const characteristics = generateCharacteristics(career)
    const name = generateName()
    const personality = generatePersonality()
    const background = generateBackground(career)
    const secrets = generateSecrets()

    const npc: WarhammerNPC = {
      id: `npc_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name,
      career,
      characteristics,
      skills: [], // Would be populated from actual data
      talents: [], // Would be populated from actual data
      equipment: [], // Would be populated from actual data
      background,
      personality,
      secrets,
      hooks: [],
      faction: 'Empire', // Default faction
      socialClass: career.status === 'Bronze' ? 'peasant' : career.status === 'Silver' ? 'burgher' : 'noble',
      wealth: Math.floor(Math.random() * 100) + (career.status === 'Bronze' ? 10 : career.status === 'Silver' ? 50 : 200),
      age: Math.floor(Math.random() * 40) + 20,
      appearance: `A ${Math.random() > 0.5 ? 'tall' : 'average height'} ${Math.random() > 0.5 ? 'human' : 'person'} with ${Math.random() > 0.5 ? 'brown' : 'blonde'} hair`,
      motivation: 'Seeking adventure and fortune',
      relationships: []
    }

    npc.hooks = generateQuestHooks(npc)

    return npc
  }

  // Generate NPC by career
  const generateNPCByCareer = (careerName: string): WarhammerNPC => {
    // This would use the actual career data from the plugin
    return generateRandomNPC() // Simplified for demo
  }

  // Generate specific tavern NPCs
  const generateTavernPatron = (): WarhammerNPC => {
    const npc = generateRandomNPC()
    npc.motivation = 'Enjoying a drink and sharing stories'
    npc.hooks.push({
      type: 'information',
      description: 'Has heard rumors about strange happenings in the area',
      difficulty: 'easy',
      reward: 'Local gossip and rumors'
    })
    return npc
  }

  const generateMerchant = (): WarhammerNPC => {
    const npc = generateRandomNPC()
    npc.career = { id: 'merchant', name: 'Merchant', class: 'Burgher', species: ['Human'], status: 'Silver', skills: ['Charm', 'Evaluate'], talents: ['Dealmaker'], trappings: ['Trade Goods'], careerPath: ['Guild Master'] }
    npc.motivation = 'Making profitable deals and expanding trade network'
    npc.wealth = Math.floor(Math.random() * 500) + 100
    return npc
  }

  const generateGuard = (): WarhammerNPC => {
    const npc = generateRandomNPC()
    npc.career = { id: 'guard', name: 'Guard', class: 'Warrior', species: ['Human'], status: 'Bronze', skills: ['Melee (Basic)', 'Intimidate'], talents: ['Combat Aware'], trappings: ['Sword', 'Uniform'], careerPath: ['Sergeant'] }
    npc.motivation = 'Maintaining order and protecting citizens'
    return npc
  }

  // Batch generation
  const generateNPCGroup = (count: number, type?: string): WarhammerNPC[] => {
    const npcs: WarhammerNPC[] = []
    for (let i = 0; i < count; i++) {
      switch (type) {
        case 'tavern':
          npcs.push(generateTavernPatron())
          break
        case 'merchant':
          npcs.push(generateMerchant())
          break
        case 'guard':
          npcs.push(generateGuard())
          break
        default:
          npcs.push(generateRandomNPC())
      }
    }
    return npcs
  }

  // Initialize
  onMounted(() => {
    loadWarhammerData()
  })

  return {
    // State
    warhammerData: readonly(warhammerData),
    isLoading: readonly(isLoading),
    error: readonly(error),

    // Generation functions
    generateRandomNPC,
    generateNPCByCareer,
    generateTavernPatron,
    generateMerchant,
    generateGuard,
    generateNPCGroup,

    // Utility functions
    generateName,
    generateCharacteristics,
    generatePersonality,
    generateBackground,
    generateSecrets,
    generateQuestHooks,

    // Data loading
    loadWarhammerData
  }
}
