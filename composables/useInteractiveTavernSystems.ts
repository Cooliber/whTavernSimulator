/**
 * Interactive Tavern Systems for Warhammer Tavern v3
 * Handles reputation, mini-games, economy, quests, and faction relationships
 */

import type { Quest } from './useQuestGenerator'

export interface PlayerReputation {
  overall: number // -100 to 100
  factions: Record<string, number>
  npcs: Record<string, number>
  achievements: string[]
  notoriety: string[] // negative reputation markers
}

export interface TavernEconomy {
  goldPieces: number
  silverShillings: number
  brassPennies: number
  priceModifiers: Record<string, number> // item type -> price multiplier
  marketTrends: Record<string, 'rising' | 'falling' | 'stable'>
  dailySpecials: string[]
}

export interface MiniGame {
  id: string
  name: string
  type: 'dice' | 'cards' | 'arm_wrestling' | 'storytelling' | 'riddles' | 'drinking'
  difficulty: 'easy' | 'medium' | 'hard'
  stakes: {
    entry: number
    reward: number
    reputationGain?: number
    reputationLoss?: number
  }
  requirements?: {
    skill?: string
    reputation?: number
    items?: string[]
  }
  isActive: boolean
  participants: string[]
}

// Quest interface imported from useQuestGenerator.ts

export interface FactionRelationship {
  factionId: string
  name: string
  standing: number // -100 to 100
  rank: string
  benefits: string[]
  penalties: string[]
  questsAvailable: string[]
  conflictsWith: string[]
}

export const useInteractiveTavernSystems = () => {
  // Reactive state
  const playerReputation = ref<PlayerReputation>({
    overall: 0,
    factions: {},
    npcs: {},
    achievements: [],
    notoriety: []
  })

  const tavernEconomy = ref<TavernEconomy>({
    goldPieces: 10,
    silverShillings: 50,
    brassPennies: 100,
    priceModifiers: {},
    marketTrends: {},
    dailySpecials: []
  })

  const availableMiniGames = ref<MiniGame[]>([])
  const activeQuests = ref<Quest[]>([])
  const completedQuests = ref<Quest[]>([])
  const factionRelationships = ref<FactionRelationship[]>([])
  const isPlayingMiniGame = ref(false)
  const currentMiniGame = ref<MiniGame | null>(null)

  // Initialize faction relationships
  const initializeFactionRelationships = () => {
    const factions: FactionRelationship[] = [
      {
        factionId: 'empire',
        name: 'The Empire',
        standing: 0,
        rank: 'Citizen',
        benefits: ['Access to Empire merchants', 'Safe passage in Empire lands'],
        penalties: [],
        questsAvailable: [],
        conflictsWith: ['chaos', 'orcs']
      },
      {
        factionId: 'dwarfs',
        name: 'Dwarf Holds',
        standing: 0,
        rank: 'Outsider',
        benefits: ['Quality crafted goods', 'Dwarf ale discounts'],
        penalties: [],
        questsAvailable: [],
        conflictsWith: ['orcs', 'undead']
      },
      {
        factionId: 'elves',
        name: 'Elven Realms',
        standing: 0,
        rank: 'Unknown',
        benefits: ['Magical knowledge', 'Elven wine access'],
        penalties: [],
        questsAvailable: [],
        conflictsWith: ['chaos', 'undead']
      }
    ]

    factionRelationships.value = factions
    
    // Initialize faction reputation
    factions.forEach(faction => {
      playerReputation.value.factions[faction.factionId] = 0
    })
  }

  // Initialize mini-games
  const initializeMiniGames = () => {
    const games: MiniGame[] = [
      {
        id: 'dice_game',
        name: 'Crown and Anchor',
        type: 'dice',
        difficulty: 'easy',
        stakes: { entry: 5, reward: 15, reputationGain: 1 },
        isActive: true,
        participants: []
      },
      {
        id: 'arm_wrestling',
        name: 'Test of Strength',
        type: 'arm_wrestling',
        difficulty: 'medium',
        stakes: { entry: 10, reward: 25, reputationGain: 2 },
        requirements: { skill: 'Strength' },
        isActive: true,
        participants: []
      },
      {
        id: 'storytelling',
        name: 'Tale Weaving Contest',
        type: 'storytelling',
        difficulty: 'hard',
        stakes: { entry: 15, reward: 50, reputationGain: 3 },
        requirements: { skill: 'Fellowship' },
        isActive: false,
        participants: []
      },
      {
        id: 'drinking_contest',
        name: 'Ale Drinking Contest',
        type: 'drinking',
        difficulty: 'medium',
        stakes: { entry: 8, reward: 20, reputationGain: 2 },
        requirements: { skill: 'Toughness' },
        isActive: true,
        participants: []
      }
    ]

    availableMiniGames.value = games
  }

  // Reputation management
  const modifyReputation = (change: number, target?: string, faction?: string) => {
    if (faction) {
      playerReputation.value.factions[faction] = Math.max(-100, Math.min(100, 
        (playerReputation.value.factions[faction] || 0) + change
      ))
      updateFactionStanding(faction)
    } else if (target) {
      playerReputation.value.npcs[target] = Math.max(-100, Math.min(100,
        (playerReputation.value.npcs[target] || 0) + change
      ))
    } else {
      playerReputation.value.overall = Math.max(-100, Math.min(100,
        playerReputation.value.overall + change
      ))
    }

    // Check for achievements
    checkReputationAchievements()
  }

  // Update faction standing based on reputation
  const updateFactionStanding = (factionId: string) => {
    const faction = factionRelationships.value.find(f => f.factionId === factionId)
    if (!faction) return

    const standing = playerReputation.value.factions[factionId] || 0
    
    if (standing >= 75) {
      faction.rank = 'Champion'
      faction.benefits.push('Exclusive faction quests', 'Significant discounts')
    } else if (standing >= 50) {
      faction.rank = 'Ally'
      faction.benefits.push('Faction quests', 'Good discounts')
    } else if (standing >= 25) {
      faction.rank = 'Friend'
      faction.benefits.push('Minor quests', 'Small discounts')
    } else if (standing >= 0) {
      faction.rank = 'Neutral'
    } else if (standing >= -25) {
      faction.rank = 'Distrusted'
      faction.penalties.push('Higher prices')
    } else if (standing >= -50) {
      faction.rank = 'Enemy'
      faction.penalties.push('Refused service', 'Hostile NPCs')
    } else {
      faction.rank = 'Hated'
      faction.penalties.push('Kill on sight', 'Bounty on head')
    }

    faction.standing = standing
  }

  // Check for reputation achievements
  const checkReputationAchievements = () => {
    const achievements = playerReputation.value.achievements
    
    if (playerReputation.value.overall >= 50 && !achievements.includes('well_known')) {
      achievements.push('well_known')
    }
    
    if (playerReputation.value.overall >= 75 && !achievements.includes('famous')) {
      achievements.push('famous')
    }

    // Faction-specific achievements
    Object.entries(playerReputation.value.factions).forEach(([faction, rep]) => {
      if (rep >= 75 && !achievements.includes(`${faction}_champion`)) {
        achievements.push(`${faction}_champion`)
      }
    })
  }

  // Economy system
  const canAfford = (cost: number): boolean => {
    const totalCopper = 
      tavernEconomy.value.goldPieces * 240 + 
      tavernEconomy.value.silverShillings * 12 + 
      tavernEconomy.value.brassPennies
    
    return totalCopper >= cost
  }

  const spendMoney = (cost: number): boolean => {
    if (!canAfford(cost)) return false
    
    let remaining = cost
    
    // Spend gold first
    const goldToSpend = Math.min(Math.floor(remaining / 240), tavernEconomy.value.goldPieces)
    tavernEconomy.value.goldPieces -= goldToSpend
    remaining -= goldToSpend * 240
    
    // Then silver
    const silverToSpend = Math.min(Math.floor(remaining / 12), tavernEconomy.value.silverShillings)
    tavernEconomy.value.silverShillings -= silverToSpend
    remaining -= silverToSpend * 12
    
    // Finally brass
    tavernEconomy.value.brassPennies -= remaining
    
    return true
  }

  const earnMoney = (amount: number) => {
    // Convert to appropriate denominations
    const gold = Math.floor(amount / 240)
    const silver = Math.floor((amount % 240) / 12)
    const brass = amount % 12
    
    tavernEconomy.value.goldPieces += gold
    tavernEconomy.value.silverShillings += silver
    tavernEconomy.value.brassPennies += brass
  }

  // Mini-game system
  const startMiniGame = async (gameId: string): Promise<boolean> => {
    const game = availableMiniGames.value.find(g => g.id === gameId)
    if (!game || !game.isActive) return false
    
    if (!canAfford(game.stakes.entry)) return false
    
    // Check requirements
    if (game.requirements) {
      // This would check player skills, items, etc.
      // For now, we'll assume requirements are met
    }
    
    spendMoney(game.stakes.entry)
    currentMiniGame.value = game
    isPlayingMiniGame.value = true
    
    return true
  }

  const playMiniGame = async (gameId: string, playerAction: any): Promise<{
    success: boolean
    result: string
    rewards?: any
  }> => {
    const game = currentMiniGame.value
    if (!game || game.id !== gameId) {
      return { success: false, result: 'Game not active' }
    }

    // Simulate game logic based on type
    const success = await simulateGameplay(game, playerAction)
    
    if (success) {
      earnMoney(game.stakes.reward)
      if (game.stakes.reputationGain) {
        modifyReputation(game.stakes.reputationGain)
      }
      
      return {
        success: true,
        result: `You won! Earned ${game.stakes.reward} coins.`,
        rewards: { coins: game.stakes.reward, reputation: game.stakes.reputationGain }
      }
    } else {
      if (game.stakes.reputationLoss) {
        modifyReputation(-game.stakes.reputationLoss)
      }
      
      return {
        success: false,
        result: 'You lost. Better luck next time!',
        rewards: { reputation: -game.stakes.reputationLoss }
      }
    }
  }

  const endMiniGame = () => {
    currentMiniGame.value = null
    isPlayingMiniGame.value = false
  }

  // Simulate gameplay for different mini-game types
  const simulateGameplay = async (game: MiniGame, playerAction: any): Promise<boolean> => {
    // This would contain actual game logic
    // For now, we'll use simple probability based on difficulty
    
    const successChances = {
      easy: 0.7,
      medium: 0.5,
      hard: 0.3
    }
    
    const baseChance = successChances[game.difficulty]
    
    // Add some skill-based modifiers (simplified)
    let finalChance = baseChance
    
    if (game.type === 'dice') {
      // Dice games are mostly luck
      finalChance = baseChance
    } else if (game.type === 'arm_wrestling') {
      // Strength-based
      finalChance += 0.1 // Would check actual strength stat
    } else if (game.type === 'storytelling') {
      // Fellowship-based
      finalChance += 0.15 // Would check fellowship stat
    }
    
    return Math.random() < finalChance
  }

  // Quest system
  const generateQuest = (npcId: string, questType?: Quest['type']): Quest => {
    const questTemplates = {
      delivery: {
        titles: ['Urgent Delivery', 'Package for a Friend', 'Secret Message'],
        descriptions: ['Deliver this package to {target}', 'Take this message to {target}']
      },
      investigation: {
        titles: ['Missing Person', 'Strange Occurrences', 'Mysterious Disappearance'],
        descriptions: ['Investigate the disappearance of {target}', 'Look into strange happenings at {location}']
      },
      collection: {
        titles: ['Herb Gathering', 'Rare Materials', 'Lost Items'],
        descriptions: ['Collect {amount} {item} from {location}', 'Find my lost {item}']
      }
    }
    
    const type = questType || (['delivery', 'investigation', 'collection'] as const)[Math.floor(Math.random() * 3)]
    const template = questTemplates[type]
    const title = template.titles[Math.floor(Math.random() * template.titles.length)]
    const description = template.descriptions[Math.floor(Math.random() * template.descriptions.length)]
    
    return {
      id: `quest_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      title,
      description,
      giver: npcId,
      type,
      difficulty: (['trivial', 'easy', 'moderate'] as const)[Math.floor(Math.random() * 3)],
      status: 'available',
      requirements: {
        reputation: type === 'investigation' ? 10 : 0
      },
      rewards: {
        gold: Math.floor(Math.random() * 50) + 10,
        reputation: Math.floor(Math.random() * 5) + 1
      },
      progress: {},
      createdAt: new Date(),
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000) // 24 hours
    }
  }

  const acceptQuest = (questId: string): boolean => {
    const questIndex = activeQuests.value.findIndex(q => q.id === questId && q.status === 'available')
    if (questIndex === -1) return false
    
    const quest = activeQuests.value[questIndex]
    
    // Check requirements
    if (quest.requirements.reputation && playerReputation.value.overall < quest.requirements.reputation) {
      return false
    }
    
    quest.status = 'active'
    return true
  }

  const completeQuest = (questId: string): boolean => {
    const questIndex = activeQuests.value.findIndex(q => q.id === questId && q.status === 'active')
    if (questIndex === -1) return false
    
    const quest = activeQuests.value[questIndex]
    quest.status = 'completed'
    
    // Apply rewards
    if (quest.rewards.gold) {
      earnMoney(quest.rewards.gold)
    }
    
    if (quest.rewards.reputation) {
      modifyReputation(quest.rewards.reputation)
    }
    
    if (quest.rewards.faction) {
      Object.entries(quest.rewards.faction).forEach(([faction, rep]) => {
        modifyReputation(rep, undefined, faction)
      })
    }
    
    // Move to completed quests
    completedQuests.value.push(quest)
    activeQuests.value.splice(questIndex, 1)
    
    return true
  }

  // Real-time events
  const triggerRandomEvent = () => {
    const events = [
      {
        name: 'Merchant Caravan Arrives',
        effect: () => {
          tavernEconomy.value.dailySpecials.push('Exotic Spices', 'Fine Silks')
        }
      },
      {
        name: 'Brawl Breaks Out',
        effect: () => {
          modifyReputation(-2)
        }
      },
      {
        name: 'Traveling Minstrel Performs',
        effect: () => {
          modifyReputation(1)
          availableMiniGames.value.find(g => g.id === 'storytelling')!.isActive = true
        }
      }
    ]
    
    const event = events[Math.floor(Math.random() * events.length)]
    event.effect()
    
    return event.name
  }

  // Initialize all systems
  const initializeSystems = () => {
    initializeFactionRelationships()
    initializeMiniGames()
    
    // Generate some initial quests
    const initialQuests = [
      generateQuest('npc_merchant_1', 'delivery'),
      generateQuest('npc_guard_1', 'investigation'),
      generateQuest('npc_farmer_1', 'collection')
    ]
    
    activeQuests.value = initialQuests
  }

  return {
    // State
    playerReputation: readonly(playerReputation),
    tavernEconomy: readonly(tavernEconomy),
    availableMiniGames: readonly(availableMiniGames),
    activeQuests: readonly(activeQuests),
    completedQuests: readonly(completedQuests),
    factionRelationships: readonly(factionRelationships),
    isPlayingMiniGame: readonly(isPlayingMiniGame),
    currentMiniGame: readonly(currentMiniGame),
    
    // Methods
    modifyReputation,
    canAfford,
    spendMoney,
    earnMoney,
    startMiniGame,
    playMiniGame,
    endMiniGame,
    generateQuest,
    acceptQuest,
    completeQuest,
    triggerRandomEvent,
    initializeSystems
  }
}
