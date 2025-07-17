/**
 * Warhammer-themed icon mapping system
 * Maps game actions and concepts to appropriate Lucide icons
 */

export interface IconMapping {
  [key: string]: string
}

export const useWarhammerIcons = () => {
  // Core game action icons
  const gameActionIcons: IconMapping = {
    // Combat actions
    attack: 'sword',
    defend: 'shield',
    cast: 'sparkles',
    flee: 'run',
    charge: 'zap',
    parry: 'shield-check',
    dodge: 'wind',
    
    // Weapon types
    sword: 'sword',
    axe: 'axe',
    hammer: 'hammer',
    bow: 'bow',
    crossbow: 'crosshair',
    staff: 'wand-2',
    dagger: 'knife',
    spear: 'spear',
    
    // Armor types
    helmet: 'hard-hat',
    chestplate: 'shield',
    gauntlets: 'hand',
    boots: 'footprints',
    cloak: 'shirt',
    
    // Magic schools
    fire: 'flame',
    ice: 'snowflake',
    lightning: 'zap',
    earth: 'mountain',
    wind: 'wind',
    light: 'sun',
    dark: 'moon',
    healing: 'heart-pulse',
    
    // Character stats
    strength: 'dumbbell',
    dexterity: 'eye',
    intelligence: 'brain',
    wisdom: 'lightbulb',
    constitution: 'heart',
    charisma: 'smile',
    
    // Skills
    stealth: 'eye-off',
    lockpicking: 'key',
    pickpocket: 'hand',
    diplomacy: 'handshake',
    intimidation: 'angry',
    persuasion: 'message-circle',
    
    // Tavern items
    ale: 'beer',
    wine: 'wine',
    bread: 'wheat',
    meat: 'beef',
    cheese: 'circle',
    room: 'bed',
    
    // Quest types
    delivery: 'package',
    escort: 'users',
    hunt: 'target',
    exploration: 'map',
    diplomacy: 'handshake',
    rescue: 'heart-handshake',
    
    // Factions
    empire: 'crown',
    dwarfs: 'mountain',
    elves: 'leaf',
    orcs: 'skull',
    chaos: 'flame',
    undead: 'ghost',
    
    // Status effects
    poisoned: 'droplet',
    blessed: 'sparkles',
    cursed: 'skull',
    stunned: 'dizzy',
    sleeping: 'moon',
    charmed: 'heart',
    
    // Inventory categories
    weapons: 'swords',
    armor: 'shield',
    consumables: 'pill',
    misc: 'package-2',
    quest: 'scroll',
    
    // UI actions
    settings: 'settings',
    help: 'help-circle',
    close: 'x',
    minimize: 'minus',
    maximize: 'maximize',
    refresh: 'refresh-cw',
    
    // Navigation
    home: 'home',
    back: 'arrow-left',
    forward: 'arrow-right',
    up: 'arrow-up',
    down: 'arrow-down',
    
    // Social
    chat: 'message-circle',
    whisper: 'message-square',
    shout: 'megaphone',
    emote: 'smile',
    
    // Economy
    gold: 'coins',
    silver: 'circle',
    copper: 'penny',
    trade: 'handshake',
    shop: 'store',
    
    // Time and weather
    day: 'sun',
    night: 'moon',
    rain: 'cloud-rain',
    snow: 'snowflake',
    storm: 'cloud-lightning',
    
    // Locations
    tavern: 'home',
    dungeon: 'mountain',
    forest: 'trees',
    city: 'building',
    castle: 'castle',
    temple: 'church',
    
    // Character classes
    warrior: 'sword',
    mage: 'sparkles',
    rogue: 'eye-off',
    cleric: 'cross',
    ranger: 'bow',
    paladin: 'shield',
    barbarian: 'axe',
    bard: 'music',
    
    // Conditions
    healthy: 'heart',
    wounded: 'heart-crack',
    dead: 'skull',
    unconscious: 'moon',
    
    // Crafting
    forge: 'hammer',
    alchemy: 'flask-conical',
    enchanting: 'wand-2',
    cooking: 'chef-hat',
    
    // Transportation
    horse: 'horse',
    cart: 'truck',
    ship: 'ship',
    portal: 'circle-dot'
  }

  // Faction-specific color mappings
  const factionColors: IconMapping = {
    empire: 'blue',
    dwarfs: 'orange',
    elves: 'green',
    'high-elves': 'purple',
    'wood-elves': 'emerald',
    'dark-elves': 'violet',
    orcs: 'red',
    chaos: 'red',
    undead: 'gray',
    skaven: 'yellow',
    lizardmen: 'teal',
    'tomb-kings': 'amber',
    'vampire-counts': 'purple',
    'warriors-of-chaos': 'red',
    'daemons-of-chaos': 'pink',
    'beastmen': 'brown'
  }

  // Rarity color mappings
  const rarityColors: IconMapping = {
    common: 'gray',
    uncommon: 'green',
    rare: 'blue',
    epic: 'purple',
    legendary: 'orange',
    artifact: 'red'
  }

  // Difficulty color mappings
  const difficultyColors: IconMapping = {
    easy: 'green',
    medium: 'yellow',
    hard: 'orange',
    legendary: 'red',
    nightmare: 'purple'
  }

  /**
   * Get icon name for a game concept
   */
  const getIcon = (concept: string): string => {
    return gameActionIcons[concept] || 'circle'
  }

  /**
   * Get faction color
   */
  const getFactionColor = (faction: string): string => {
    return factionColors[faction.toLowerCase()] || 'gray'
  }

  /**
   * Get rarity color
   */
  const getRarityColor = (rarity: string): string => {
    return rarityColors[rarity.toLowerCase()] || 'gray'
  }

  /**
   * Get difficulty color
   */
  const getDifficultyColor = (difficulty: string): string => {
    return difficultyColors[difficulty.toLowerCase()] || 'gray'
  }

  /**
   * Get icon with color for a concept
   */
  const getIconWithColor = (concept: string, type: 'faction' | 'rarity' | 'difficulty' = 'faction') => {
    const icon = getIcon(concept)
    let color = 'gray'
    
    switch (type) {
      case 'faction':
        color = getFactionColor(concept)
        break
      case 'rarity':
        color = getRarityColor(concept)
        break
      case 'difficulty':
        color = getDifficultyColor(concept)
        break
    }
    
    return { icon, color }
  }

  /**
   * Get all available icons for a category
   */
  const getIconsForCategory = (category: string): string[] => {
    const categoryMappings: { [key: string]: string[] } = {
      weapons: ['sword', 'axe', 'hammer', 'bow', 'crossbow', 'staff', 'dagger', 'spear'],
      magic: ['fire', 'ice', 'lightning', 'earth', 'wind', 'light', 'dark', 'healing'],
      stats: ['strength', 'dexterity', 'intelligence', 'wisdom', 'constitution', 'charisma'],
      factions: ['empire', 'dwarfs', 'elves', 'orcs', 'chaos', 'undead'],
      classes: ['warrior', 'mage', 'rogue', 'cleric', 'ranger', 'paladin', 'barbarian', 'bard']
    }
    
    return categoryMappings[category] || []
  }

  return {
    gameActionIcons,
    factionColors,
    rarityColors,
    difficultyColors,
    getIcon,
    getFactionColor,
    getRarityColor,
    getDifficultyColor,
    getIconWithColor,
    getIconsForCategory
  }
}
