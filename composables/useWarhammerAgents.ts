/**
 * Warhammer Fantasy AI Agents System
 * 17 distinct NPCs with unique personalities, backgrounds, and specializations
 */

import { extendedAgents } from './useWarhammerAgentsExtended'

export interface WarhammerAgent {
  id: string
  name: string
  species: 'human' | 'elf' | 'dwarf' | 'halfling' | 'ogre'
  career: string
  faction: 'empire' | 'chaos' | 'elves' | 'dwarfs' | 'undead' | 'orcs' | 'neutral'
  role: 'bartender' | 'merchant' | 'guard' | 'scholar' | 'entertainer' | 'noble' | 'commoner' | 'mystic' | 'warrior' | 'artisan'
  
  // Personality traits
  personality: {
    traits: string[]
    conversationStyle: 'verbose' | 'terse' | 'cryptic' | 'boastful' | 'scholarly' | 'friendly' | 'suspicious'
    mood: 'cheerful' | 'melancholy' | 'neutral' | 'aggressive' | 'drunk' | 'contemplative'
    intelligence: number // 1-10
    charisma: number // 1-10
    trustworthiness: number // 1-10
  }
  
  // Knowledge and expertise
  knowledge: {
    domains: string[]
    specialties: string[]
    secrets: string[]
    rumors: string[]
  }
  
  // Relationships and politics
  relationships: {
    allies: string[] // Agent IDs
    rivals: string[] // Agent IDs
    neutral: string[] // Agent IDs
    romanticInterests?: string[] // Agent IDs
  }
  
  // Background and lore
  background: {
    origin: string
    motivation: string
    fears: string[]
    goals: string[]
    pastEvents: string[]
  }
  
  // Conversation patterns
  conversationPatterns: {
    greetings: string[]
    farewells: string[]
    topics: Record<string, string[]>
    catchphrases: string[]
    speechPatterns: string[]
  }
  
  // Game mechanics
  gameStats: {
    reputation: number
    wealth: number
    influence: number
    combatSkill: number
    magicalAbility: number
  }
}

export const useWarhammerAgents = () => {
  // The 17 distinct Warhammer Fantasy agents
  const agents = ref<WarhammerAgent[]>([
    // 1. The Bartender - Heart of the tavern
    {
      id: 'agent_bartender_wilhelm',
      name: 'Wilhelm Steinhart',
      species: 'human',
      career: 'Innkeeper',
      faction: 'empire',
      role: 'bartender',
      personality: {
        traits: ['wise', 'observant', 'diplomatic', 'patient'],
        conversationStyle: 'friendly',
        mood: 'cheerful',
        intelligence: 7,
        charisma: 8,
        trustworthiness: 9
      },
      knowledge: {
        domains: ['local politics', 'trade routes', 'tavern management', 'brewing'],
        specialties: ['reading people', 'conflict resolution', 'local gossip'],
        secrets: ['knows about smuggling operations', 'aware of noble scandals'],
        rumors: ['strange lights in the forest', 'missing merchant caravans']
      },
      relationships: {
        allies: ['agent_merchant_greta', 'agent_guard_marcus'],
        rivals: ['agent_noble_von_carstein'],
        neutral: ['agent_scholar_elara', 'agent_entertainer_finn']
      },
      background: {
        origin: 'Born in Altdorf, inherited the tavern from his father',
        motivation: 'Maintain peace and prosperity in his establishment',
        fears: ['losing his tavern', 'violence in his establishment'],
        goals: ['expand the tavern', 'retire comfortably'],
        pastEvents: ['survived the Storm of Chaos', 'helped refugees during the war']
      },
      conversationPatterns: {
        greetings: ['Welcome to the Golden Griffin!', 'What can I get you, friend?'],
        farewells: ['Safe travels!', 'Come back soon!'],
        topics: {
          drinks: ['Our ale is brewed with the finest hops', 'Try our special mulled wine'],
          news: ['I hear many things behind this bar', 'Travelers bring interesting tales']
        },
        catchphrases: ['A good drink solves most problems', 'Everyone\'s welcome here'],
        speechPatterns: ['speaks with authority', 'uses tavern metaphors']
      },
      gameStats: {
        reputation: 75,
        wealth: 60,
        influence: 70,
        combatSkill: 40,
        magicalAbility: 10
      }
    },

    // 2. The Merchant - Trade and commerce
    {
      id: 'agent_merchant_greta',
      name: 'Greta Goldweaver',
      species: 'human',
      career: 'Merchant',
      faction: 'empire',
      role: 'merchant',
      personality: {
        traits: ['shrewd', 'ambitious', 'calculating', 'charming'],
        conversationStyle: 'verbose',
        mood: 'neutral',
        intelligence: 8,
        charisma: 7,
        trustworthiness: 6
      },
      knowledge: {
        domains: ['trade routes', 'economics', 'foreign cultures', 'luxury goods'],
        specialties: ['negotiation', 'market trends', 'rare items'],
        secrets: ['black market connections', 'noble debt information'],
        rumors: ['new trade opportunities', 'bandit activity on roads']
      },
      relationships: {
        allies: ['agent_bartender_wilhelm', 'agent_noble_von_carstein'],
        rivals: ['agent_merchant_dwarf_thorek'],
        neutral: ['agent_guard_marcus', 'agent_scholar_elara']
      },
      background: {
        origin: 'Marienburg merchant family, traveled extensively',
        motivation: 'Accumulate wealth and establish trade empire',
        fears: ['economic collapse', 'losing her fortune'],
        goals: ['monopolize luxury trade', 'gain noble title'],
        pastEvents: ['survived pirate attack', 'discovered new trade route']
      },
      conversationPatterns: {
        greetings: ['Ah, a potential customer!', 'Looking for quality goods?'],
        farewells: ['Pleasure doing business', 'Remember my prices are fair'],
        topics: {
          trade: ['I have connections across the Old World', 'Quality costs, but it\'s worth it'],
          money: ['Gold opens all doors', 'Investment is the key to prosperity']
        },
        catchphrases: ['Everything has a price', 'Quality over quantity'],
        speechPatterns: ['uses trade terminology', 'mentions prices frequently']
      },
      gameStats: {
        reputation: 65,
        wealth: 85,
        influence: 60,
        combatSkill: 30,
        magicalAbility: 15
      }
    },

    // 3. The Guard - Security and law
    {
      id: 'agent_guard_marcus',
      name: 'Marcus Ironwall',
      species: 'human',
      career: 'Soldier',
      faction: 'empire',
      role: 'guard',
      personality: {
        traits: ['loyal', 'disciplined', 'protective', 'stern'],
        conversationStyle: 'terse',
        mood: 'neutral',
        intelligence: 6,
        charisma: 5,
        trustworthiness: 9
      },
      knowledge: {
        domains: ['military tactics', 'law enforcement', 'weapons', 'empire politics'],
        specialties: ['combat training', 'threat assessment', 'investigation'],
        secrets: ['corruption in the guard', 'planned military operations'],
        rumors: ['chaos cult activity', 'deserters in the area']
      },
      relationships: {
        allies: ['agent_bartender_wilhelm', 'agent_noble_von_carstein'],
        rivals: ['agent_rogue_shadow'],
        neutral: ['agent_merchant_greta', 'agent_entertainer_finn']
      },
      background: {
        origin: 'Recruited from Nuln, served in multiple campaigns',
        motivation: 'Protect the innocent and uphold the law',
        fears: ['failing in his duty', 'chaos corruption'],
        goals: ['promotion to sergeant', 'retire with honor'],
        pastEvents: ['fought against Beastmen', 'saved village from raiders']
      },
      conversationPatterns: {
        greetings: ['State your business', 'Everything in order here?'],
        farewells: ['Stay out of trouble', 'Keep the peace'],
        topics: {
          law: ['Order must be maintained', 'Justice will prevail'],
          combat: ['Training keeps you alive', 'Always be prepared']
        },
        catchphrases: ['For the Empire!', 'Duty before self'],
        speechPatterns: ['military terminology', 'short, direct sentences']
      },
      gameStats: {
        reputation: 70,
        wealth: 40,
        influence: 55,
        combatSkill: 85,
        magicalAbility: 5
      }
    },

    // 4. The Scholar - Knowledge and magic
    {
      id: 'agent_scholar_elara',
      name: 'Elara Moonwhisper',
      species: 'elf',
      career: 'Scholar',
      faction: 'elves',
      role: 'scholar',
      personality: {
        traits: ['intelligent', 'curious', 'aloof', 'perfectionist'],
        conversationStyle: 'scholarly',
        mood: 'contemplative',
        intelligence: 10,
        charisma: 6,
        trustworthiness: 8
      },
      knowledge: {
        domains: ['magic theory', 'ancient history', 'languages', 'astronomy'],
        specialties: ['arcane research', 'translation', 'prophecy interpretation'],
        secrets: ['forbidden magical knowledge', 'location of ancient artifacts'],
        rumors: ['magical disturbances', 'ancient prophecies awakening']
      },
      relationships: {
        allies: ['agent_mystic_seraphina'],
        rivals: ['agent_witch_hunter_johann'],
        neutral: ['agent_bartender_wilhelm', 'agent_merchant_greta']
      },
      background: {
        origin: 'Ulthuan, came to study human magical traditions',
        motivation: 'Advance magical knowledge and understanding',
        fears: ['magical catastrophe', 'loss of knowledge'],
        goals: ['complete her research', 'prevent magical disasters'],
        pastEvents: ['witnessed daemon summoning', 'discovered lost spell']
      },
      conversationPatterns: {
        greetings: ['Greetings, seeker of knowledge', 'What brings you to my studies?'],
        farewells: ['May wisdom guide you', 'Knowledge is eternal'],
        topics: {
          magic: ['Magic is both beautiful and dangerous', 'Understanding requires patience'],
          history: ['The past holds many lessons', 'Ancient wisdom should not be forgotten']
        },
        catchphrases: ['Knowledge is power', 'The winds of magic are stirring'],
        speechPatterns: ['uses archaic terms', 'speaks in measured tones']
      },
      gameStats: {
        reputation: 60,
        wealth: 50,
        influence: 65,
        combatSkill: 25,
        magicalAbility: 90
      }
    },

    // 5. The Entertainer - Music and stories
    {
      id: 'agent_entertainer_finn',
      name: 'Finn Lightfinger',
      species: 'halfling',
      career: 'Entertainer',
      faction: 'neutral',
      role: 'entertainer',
      personality: {
        traits: ['charismatic', 'witty', 'mischievous', 'optimistic'],
        conversationStyle: 'friendly',
        mood: 'cheerful',
        intelligence: 7,
        charisma: 9,
        trustworthiness: 7
      },
      knowledge: {
        domains: ['music', 'storytelling', 'local legends', 'social dynamics'],
        specialties: ['performance', 'crowd reading', 'information gathering'],
        secrets: ['affairs of the nobility', 'hidden talents of patrons'],
        rumors: ['romantic scandals', 'upcoming celebrations']
      },
      relationships: {
        allies: ['agent_bartender_wilhelm', 'agent_rogue_shadow'],
        rivals: ['agent_noble_von_carstein'],
        neutral: ['agent_guard_marcus', 'agent_merchant_greta']
      },
      background: {
        origin: 'Traveling performer from the Moot',
        motivation: 'Bring joy and laughter to others',
        fears: ['losing his voice', 'being forgotten'],
        goals: ['become famous bard', 'write the perfect song'],
        pastEvents: ['performed for Emperor', 'escaped angry husband']
      },
      conversationPatterns: {
        greetings: ['Well met, friend!', 'Care for a song or tale?'],
        farewells: ['Until we meet again!', 'May your days be filled with music!'],
        topics: {
          music: ['Music soothes the savage beast', 'Every heart has its own rhythm'],
          stories: ['Every person has a story worth telling', 'Truth is stranger than fiction']
        },
        catchphrases: ['Life\'s too short for sadness', 'There\'s always a song in my heart'],
        speechPatterns: ['uses musical metaphors', 'speaks rhythmically']
      },
      gameStats: {
        reputation: 80,
        wealth: 35,
        influence: 70,
        combatSkill: 40,
        magicalAbility: 20
      }
    },

    // 6. The Noble - Politics and intrigue
    {
      id: 'agent_noble_von_carstein',
      name: 'Baron Heinrich von Carstein',
      species: 'human',
      career: 'Noble',
      faction: 'empire',
      role: 'noble',
      personality: {
        traits: ['arrogant', 'manipulative', 'sophisticated', 'ambitious'],
        conversationStyle: 'verbose',
        mood: 'neutral',
        intelligence: 8,
        charisma: 7,
        trustworthiness: 4
      },
      knowledge: {
        domains: ['politics', 'nobility', 'court intrigue', 'law'],
        specialties: ['manipulation', 'social climbing', 'blackmail'],
        secrets: ['noble conspiracies', 'tax evasion schemes'],
        rumors: ['succession disputes', 'arranged marriages']
      },
      relationships: {
        allies: ['agent_merchant_greta'],
        rivals: ['agent_bartender_wilhelm', 'agent_entertainer_finn'],
        neutral: ['agent_guard_marcus', 'agent_scholar_elara']
      },
      background: {
        origin: 'Minor noble family from Stirland',
        motivation: 'Increase family power and influence',
        fears: ['losing noble status', 'public scandal'],
        goals: ['gain higher title', 'arrange advantageous marriage'],
        pastEvents: ['inherited debt-ridden estate', 'survived court intrigue']
      },
      conversationPatterns: {
        greetings: ['Ah, a commoner approaches', 'Do you know who I am?'],
        farewells: ['Remember your place', 'You may go'],
        topics: {
          politics: ['The Empire needs strong leadership', 'Common folk don\'t understand governance'],
          nobility: ['Breeding tells', 'Noble blood carries responsibility']
        },
        catchphrases: ['Know your betters', 'Nobility obliges'],
        speechPatterns: ['uses formal language', 'mentions titles frequently']
      },
      gameStats: {
        reputation: 45,
        wealth: 70,
        influence: 85,
        combatSkill: 50,
        magicalAbility: 10
      }
    },

    // 7. The Dwarf Artisan - Craftsmanship and tradition
    {
      id: 'agent_merchant_dwarf_thorek',
      name: 'Thorek Ironforge',
      species: 'dwarf',
      career: 'Artisan',
      faction: 'dwarfs',
      role: 'artisan',
      personality: {
        traits: ['stubborn', 'proud', 'skilled', 'traditional'],
        conversationStyle: 'boastful',
        mood: 'neutral',
        intelligence: 8,
        charisma: 6,
        trustworthiness: 9
      },
      knowledge: {
        domains: ['metalworking', 'engineering', 'dwarf lore', 'mining'],
        specialties: ['weapon crafting', 'armor making', 'gem cutting'],
        secrets: ['ancient dwarf techniques', 'location of rare ores'],
        rumors: ['orc movements in mountains', 'lost dwarf holds']
      },
      relationships: {
        allies: ['agent_guard_marcus'],
        rivals: ['agent_merchant_greta'],
        neutral: ['agent_bartender_wilhelm', 'agent_scholar_elara']
      },
      background: {
        origin: 'Karaz-a-Karak, master craftsman lineage',
        motivation: 'Preserve dwarf traditions and craftsmanship',
        fears: ['dishonoring ancestors', 'shoddy workmanship'],
        goals: ['create masterwork weapon', 'train worthy apprentice'],
        pastEvents: ['fought in Goblin Wars', 'created weapon for king']
      },
      conversationPatterns: {
        greetings: ['What brings you to my forge?', 'Looking for quality work?'],
        farewells: ['May your axe stay sharp', 'Good craftsmanship to you'],
        topics: {
          crafting: ['Dwarf work lasts forever', 'No shortcuts to quality'],
          tradition: ['The old ways are best', 'Ancestors guide my hammer']
        },
        catchphrases: ['By my beard!', 'Khazad ai-mênu!'],
        speechPatterns: ['uses dwarf expressions', 'mentions ancestors']
      },
      gameStats: {
        reputation: 75,
        wealth: 65,
        influence: 50,
        combatSkill: 70,
        magicalAbility: 5
      }
    },

    // 8. The Rogue - Shadows and secrets
    {
      id: 'agent_rogue_shadow',
      name: 'Shadow',
      species: 'human',
      career: 'Rogue',
      faction: 'neutral',
      role: 'commoner',
      personality: {
        traits: ['secretive', 'cunning', 'independent', 'pragmatic'],
        conversationStyle: 'cryptic',
        mood: 'neutral',
        intelligence: 8,
        charisma: 6,
        trustworthiness: 5
      },
      knowledge: {
        domains: ['underworld', 'stealth', 'lockpicking', 'street politics'],
        specialties: ['information brokering', 'smuggling', 'assassination'],
        secrets: ['criminal networks', 'hidden passages', 'corrupt officials'],
        rumors: ['heist plans', 'gang wars', 'missing persons']
      },
      relationships: {
        allies: ['agent_entertainer_finn'],
        rivals: ['agent_guard_marcus', 'agent_witch_hunter_johann'],
        neutral: ['agent_bartender_wilhelm', 'agent_merchant_greta']
      },
      background: {
        origin: 'Unknown, appeared in city five years ago',
        motivation: 'Survive and profit in the shadows',
        fears: ['capture by authorities', 'betrayal by allies'],
        goals: ['build criminal empire', 'retire wealthy'],
        pastEvents: ['escaped from prison', 'witnessed noble murder']
      },
      conversationPatterns: {
        greetings: ['...', 'You didn\'t see me here'],
        farewells: ['Watch your back', 'Trust no one'],
        topics: {
          secrets: ['Information has value', 'Everyone has something to hide'],
          danger: ['The shadows have eyes', 'Danger lurks everywhere']
        },
        catchphrases: ['Silence is golden', 'Nothing is as it seems'],
        speechPatterns: ['speaks in whispers', 'uses criminal slang']
      },
      gameStats: {
        reputation: 30,
        wealth: 55,
        influence: 40,
        combatSkill: 75,
        magicalAbility: 15
      }
    },

    // 9. The Witch Hunter - Faith and purification
    {
      id: 'agent_witch_hunter_johann',
      name: 'Johann Brenner',
      species: 'human',
      career: 'Witch Hunter',
      faction: 'empire',
      role: 'warrior',
      personality: {
        traits: ['zealous', 'paranoid', 'righteous', 'uncompromising'],
        conversationStyle: 'terse',
        mood: 'aggressive',
        intelligence: 7,
        charisma: 5,
        trustworthiness: 8
      },
      knowledge: {
        domains: ['chaos lore', 'religion', 'investigation', 'torture'],
        specialties: ['detecting corruption', 'interrogation', 'purification'],
        secrets: ['chaos cult locations', 'heretical activities'],
        rumors: ['witch sightings', 'daemon manifestations']
      },
      relationships: {
        allies: ['agent_guard_marcus'],
        rivals: ['agent_scholar_elara', 'agent_rogue_shadow', 'agent_mystic_seraphina'],
        neutral: ['agent_bartender_wilhelm']
      },
      background: {
        origin: 'Templars of Sigmar, lost family to chaos',
        motivation: 'Purge corruption and protect the faithful',
        fears: ['chaos corruption spreading', 'failing Sigmar'],
        goals: ['eliminate all heretics', 'achieve sainthood'],
        pastEvents: ['burned chaos cultists', 'survived daemon attack']
      },
      conversationPatterns: {
        greetings: ['Sigmar protects', 'Have you seen any corruption?'],
        farewells: ['Stay pure', 'Sigmar watch over you'],
        topics: {
          faith: ['Sigmar is our salvation', 'Faith purifies the soul'],
          corruption: ['Chaos must be destroyed', 'Heresy spreads like disease']
        },
        catchphrases: ['Burn the heretic!', 'Sigmar\'s will be done'],
        speechPatterns: ['quotes religious texts', 'speaks with conviction']
      },
      gameStats: {
        reputation: 55,
        wealth: 40,
        influence: 60,
        combatSkill: 80,
        magicalAbility: 25
      }
    },

    // 10. The Mystic - Spiritual guidance
    {
      id: 'agent_mystic_seraphina',
      name: 'Seraphina the Seer',
      species: 'human',
      career: 'Mystic',
      faction: 'neutral',
      role: 'mystic',
      personality: {
        traits: ['mystical', 'wise', 'enigmatic', 'compassionate'],
        conversationStyle: 'cryptic',
        mood: 'contemplative',
        intelligence: 9,
        charisma: 8,
        trustworthiness: 7
      },
      knowledge: {
        domains: ['divination', 'spirits', 'prophecy', 'healing'],
        specialties: ['fortune telling', 'spirit communication', 'dream interpretation'],
        secrets: ['future visions', 'spirit messages', 'hidden destinies'],
        rumors: ['prophetic dreams', 'spiritual disturbances']
      },
      relationships: {
        allies: ['agent_scholar_elara'],
        rivals: ['agent_witch_hunter_johann'],
        neutral: ['agent_bartender_wilhelm', 'agent_entertainer_finn']
      },
      background: {
        origin: 'Wandering mystic from Kislev',
        motivation: 'Guide others through spiritual wisdom',
        fears: ['losing connection to spirits', 'dark prophecies'],
        goals: ['prevent prophesied disaster', 'help lost souls'],
        pastEvents: ['predicted plague outbreak', 'communed with ancient spirits']
      },
      conversationPatterns: {
        greetings: ['The spirits whisper of your coming', 'Your aura speaks volumes'],
        farewells: ['May the spirits guide you', 'Your path is written in stars'],
        topics: {
          future: ['The future is mutable', 'Destiny can be changed'],
          spirits: ['The dead have much to teach', 'Spirits walk among us']
        },
        catchphrases: ['The veil grows thin', 'All is connected'],
        speechPatterns: ['speaks in riddles', 'references spiritual concepts']
      },
      gameStats: {
        reputation: 65,
        wealth: 30,
        influence: 55,
        combatSkill: 20,
        magicalAbility: 85
      }
    },

    // 11. The Veteran - War stories and experience
    {
      id: 'agent_veteran_klaus',
      name: 'Klaus Grimwald',
      species: 'human',
      career: 'Veteran',
      faction: 'empire',
      role: 'warrior',
      personality: {
        traits: ['gruff', 'experienced', 'loyal', 'haunted'],
        conversationStyle: 'terse',
        mood: 'melancholy',
        intelligence: 6,
        charisma: 4,
        trustworthiness: 9
      },
      knowledge: {
        domains: ['warfare', 'survival', 'military history', 'weapons'],
        specialties: ['battlefield tactics', 'wound treatment', 'leadership'],
        secrets: ['military failures', 'cowardly officers', 'war crimes'],
        rumors: ['upcoming conflicts', 'veteran benefits', 'old enemies']
      },
      relationships: {
        allies: ['agent_guard_marcus', 'agent_witch_hunter_johann'],
        rivals: [],
        neutral: ['agent_bartender_wilhelm', 'agent_noble_von_carstein']
      },
      background: {
        origin: 'Career soldier, fought in multiple campaigns',
        motivation: 'Find peace after years of war',
        fears: ['nightmares of battle', 'dying forgotten'],
        goals: ['train young soldiers', 'write war memoirs'],
        pastEvents: ['survived Siege of Praag', 'lost entire unit to ambush']
      },
      conversationPatterns: {
        greetings: ['Soldier', 'What do you want?'],
        farewells: ['Stay alive', 'Watch your six'],
        topics: {
          war: ['War is hell', 'Only the dead see the end of war'],
          survival: ['Adapt or die', 'Trust your instincts']
        },
        catchphrases: ['I\'ve seen worse', 'War never changes'],
        speechPatterns: ['uses military jargon', 'speaks from experience']
      },
      gameStats: {
        reputation: 70,
        wealth: 35,
        influence: 45,
        combatSkill: 90,
        magicalAbility: 5
      }
    },

    // Add the extended agents (12-17)
    ...extendedAgents
  ])

  // Agent management functions
  const getAgentById = (id: string): WarhammerAgent | undefined => {
    return agents.value.find(agent => agent.id === id)
  }

  const getAgentsByRole = (role: WarhammerAgent['role']): WarhammerAgent[] => {
    return agents.value.filter(agent => agent.role === role)
  }

  const getAgentsByFaction = (faction: WarhammerAgent['faction']): WarhammerAgent[] => {
    return agents.value.filter(agent => agent.faction === faction)
  }

  const getAgentRelationships = (agentId: string) => {
    const agent = getAgentById(agentId)
    if (!agent) return null

    return {
      allies: agent.relationships.allies.map(id => getAgentById(id)).filter(Boolean),
      rivals: agent.relationships.rivals.map(id => getAgentById(id)).filter(Boolean),
      neutral: agent.relationships.neutral.map(id => getAgentById(id)).filter(Boolean)
    }
  }

  const updateAgentRelationship = (
    agentId: string, 
    targetId: string, 
    newRelationType: 'allies' | 'rivals' | 'neutral'
  ) => {
    const agent = getAgentById(agentId)
    if (!agent) return

    // Remove from all relationship arrays
    agent.relationships.allies = agent.relationships.allies.filter(id => id !== targetId)
    agent.relationships.rivals = agent.relationships.rivals.filter(id => id !== targetId)
    agent.relationships.neutral = agent.relationships.neutral.filter(id => id !== targetId)

    // Add to new relationship type
    agent.relationships[newRelationType].push(targetId)
  }

  const getAgentKnowledgeByDomain = (agentId: string, domain: string): string[] => {
    const agent = getAgentById(agentId)
    if (!agent) return []

    if (agent.knowledge.domains.includes(domain)) {
      return agent.knowledge.specialties.filter(specialty => 
        specialty.toLowerCase().includes(domain.toLowerCase())
      )
    }

    return []
  }

  const generateAgentResponse = (
    agentId: string, 
    topic: string, 
    context?: any
  ): string => {
    const agent = getAgentById(agentId)
    if (!agent) return "I don't understand."

    // Check if agent has specific knowledge about the topic
    const topicResponses = agent.conversationPatterns.topics[topic.toLowerCase()]
    if (topicResponses && topicResponses.length > 0) {
      return topicResponses[Math.floor(Math.random() * topicResponses.length)]
    }

    // Use catchphrases as fallback
    if (agent.conversationPatterns.catchphrases.length > 0) {
      return agent.conversationPatterns.catchphrases[
        Math.floor(Math.random() * agent.conversationPatterns.catchphrases.length)
      ]
    }

    return "That's interesting. Tell me more."
  }

  const getRandomAgent = (): WarhammerAgent => {
    return agents.value[Math.floor(Math.random() * agents.value.length)]
  }

  const getAvailableAgents = (): WarhammerAgent[] => {
    // In a real implementation, this would check if agents are currently busy
    return agents.value
  }

  return {
    // Data
    agents: readonly(agents),
    
    // Methods
    getAgentById,
    getAgentsByRole,
    getAgentsByFaction,
    getAgentRelationships,
    updateAgentRelationship,
    getAgentKnowledgeByDomain,
    generateAgentResponse,
    getRandomAgent,
    getAvailableAgents
  }
}
