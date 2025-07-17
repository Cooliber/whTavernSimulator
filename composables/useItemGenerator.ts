/**
 * Item Generator Composable
 * Generates weapons, armor, tools, and magical items for the Warhammer Fantasy setting
 */

export interface GeneratedItem {
  id: string
  name: string
  type: 'weapon' | 'armor' | 'tool' | 'consumable' | 'magical' | 'trade_good' | 'treasure'
  subtype: string
  description: string
  price: number
  availability: 'common' | 'scarce' | 'rare' | 'exotic'
  weight: number
  qualities: string[]
  flaws: string[]
  condition: 'poor' | 'average' | 'good' | 'excellent'
  enchantment?: Enchantment
  history?: string
  culturalOrigin: string
  rarity: number // 1-10, 10 being legendary
}

export interface Enchantment {
  name: string
  description: string
  effect: string
  charges?: number
  school: 'fire' | 'ice' | 'lightning' | 'divine' | 'shadow' | 'nature'
  power: 'minor' | 'moderate' | 'major' | 'legendary'
}

export interface WeaponStats {
  damage: string
  reach: string
  group: string
  qualities: string[]
  flaws: string[]
}

export interface ArmorStats {
  armorPoints: number
  locations: string[]
  qualities: string[]
  flaws: string[]
}

export function useItemGenerator() {
  // Base item templates from Warhammer data
  const weaponTemplates = ref({
    melee: [
      { name: 'Sword', damage: 'SB+4', reach: 'Average', group: 'Basic', basePrice: 10 },
      { name: 'Dagger', damage: 'SB+2', reach: 'Very Short', group: 'Basic', basePrice: 2 },
      { name: 'Axe', damage: 'SB+4', reach: 'Average', group: 'Basic', basePrice: 8 },
      { name: 'Hammer', damage: 'SB+3', reach: 'Average', group: 'Basic', basePrice: 6 },
      { name: 'Spear', damage: 'SB+3', reach: 'Long', group: 'Basic', basePrice: 5 },
      { name: 'Halberd', damage: 'SB+5', reach: 'Very Long', group: 'Polearm', basePrice: 15 },
      { name: 'Great Sword', damage: 'SB+6', reach: 'Very Long', group: 'Two-Handed', basePrice: 25 }
    ],
    ranged: [
      { name: 'Bow', damage: 'SB+3', range: '24/48', group: 'Bow', basePrice: 12 },
      { name: 'Crossbow', damage: 'SB+4', range: '30/60', group: 'Crossbow', basePrice: 25 },
      { name: 'Sling', damage: 'SB+1', range: '8/16', group: 'Sling', basePrice: 1 },
      { name: 'Javelin', damage: 'SB+2', range: '6/12', group: 'Thrown', basePrice: 3 }
    ]
  })

  const armorTemplates = ref([
    { name: 'Leather Jerkin', ap: 1, locations: ['Body'], basePrice: 5 },
    { name: 'Leather Leggings', ap: 1, locations: ['Legs'], basePrice: 4 },
    { name: 'Mail Shirt', ap: 2, locations: ['Body', 'Arms'], basePrice: 35 },
    { name: 'Mail Coif', ap: 2, locations: ['Head'], basePrice: 15 },
    { name: 'Plate Breastplate', ap: 5, locations: ['Body'], basePrice: 150 },
    { name: 'Full Plate', ap: 5, locations: ['All'], basePrice: 500 }
  ])

  const toolTemplates = ref([
    { name: 'Blacksmith Tools', profession: 'Blacksmith', basePrice: 20 },
    { name: 'Physician Kit', profession: 'Physician', basePrice: 15 },
    { name: 'Thieves Tools', profession: 'Thief', basePrice: 25 },
    { name: 'Scholar Kit', profession: 'Scholar', basePrice: 10 },
    { name: 'Rope', general: true, basePrice: 2 },
    { name: 'Lantern', general: true, basePrice: 3 },
    { name: 'Grappling Hook', general: true, basePrice: 5 }
  ])

  const consumableTemplates = ref([
    { name: 'Healing Potion', effect: 'Heals wounds', basePrice: 25 },
    { name: 'Antidote', effect: 'Cures poison', basePrice: 15 },
    { name: 'Rations', effect: 'Prevents hunger', basePrice: 1 },
    { name: 'Torch', effect: 'Provides light', basePrice: 1 },
    { name: 'Holy Water', effect: 'Blessed liquid', basePrice: 10 }
  ])

  // Polish cultural elements for authentic naming
  const polishPrefixes = [
    'Stary', 'Nowy', 'Wielki', 'Mały', 'Złoty', 'Srebrny', 'Żelazny', 'Drewniany',
    'Królewski', 'Szlachetny', 'Pradawny', 'Tajemniczy', 'Błogosławiony', 'Przeklęty'
  ]

  const polishSuffixes = [
    'ski', 'cki', 'owski', 'ewski', 'arz', 'nik', 'ak', 'ek', 'ko', 'ło'
  ]

  // Weapon qualities and flaws
  const weaponQualities = [
    'Sharp', 'Balanced', 'Durable', 'Fast', 'Defensive', 'Precise', 'Damaging',
    'Penetrating', 'Pummel', 'Entangle', 'Impact', 'Wrap'
  ]

  const weaponFlaws = [
    'Slow', 'Tiring', 'Undamaging', 'Imprecise', 'Unwieldy', 'Fragile'
  ]

  // Armor qualities and flaws
  const armorQualities = [
    'Durable', 'Fine', 'Lightweight', 'Impenetrable', 'Flexible'
  ]

  const armorFlaws = [
    'Bulky', 'Loud', 'Partial', 'Weakpoints', 'Unreliable'
  ]

  // Enchantment templates
  const enchantmentTemplates = ref({
    weapon: [
      { name: 'Flame Blade', effect: '+1 damage, fire damage', school: 'fire', power: 'minor' },
      { name: 'Frost Edge', effect: 'Slows enemies on hit', school: 'ice', power: 'minor' },
      { name: 'Lightning Strike', effect: 'Chain lightning on critical', school: 'lightning', power: 'moderate' },
      { name: 'Holy Weapon', effect: '+2 damage vs undead', school: 'divine', power: 'moderate' },
      { name: 'Shadow Blade', effect: 'Ignores armor', school: 'shadow', power: 'major' }
    ],
    armor: [
      { name: 'Warding', effect: '+1 armor point', school: 'divine', power: 'minor' },
      { name: 'Fire Resistance', effect: 'Resist fire damage', school: 'fire', power: 'minor' },
      { name: 'Ethereal', effect: 'Ignore some attacks', school: 'shadow', power: 'major' },
      { name: 'Regeneration', effect: 'Slowly heals wounds', school: 'nature', power: 'moderate' }
    ],
    tool: [
      { name: 'Masterwork', effect: '+10 to skill tests', school: 'divine', power: 'minor' },
      { name: 'Unbreaking', effect: 'Never breaks', school: 'nature', power: 'moderate' },
      { name: 'Swift Work', effect: 'Half time required', school: 'lightning', power: 'moderate' }
    ]
  })

  // Generate random weapon
  const generateWeapon = (type: 'melee' | 'ranged' = 'melee'): GeneratedItem => {
    const templates = weaponTemplates.value[type]
    const template = templates[Math.floor(Math.random() * templates.length)]
    
    const item: GeneratedItem = {
      id: `weapon_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name: generateItemName(template.name),
      type: 'weapon',
      subtype: type,
      description: generateWeaponDescription(template),
      price: calculatePrice(template.basePrice),
      availability: generateAvailability(),
      weight: generateWeight(template.basePrice / 5),
      qualities: generateQualities(weaponQualities),
      flaws: generateFlaws(weaponFlaws),
      condition: generateCondition(),
      culturalOrigin: generateCulturalOrigin(),
      rarity: generateRarity()
    }

    // Add enchantment chance
    if (Math.random() > 0.8) {
      item.enchantment = generateEnchantment('weapon')
      item.rarity = Math.min(10, item.rarity + 3)
    }

    // Add history for special items
    if (item.rarity >= 7) {
      item.history = generateItemHistory(item)
    }

    return item
  }

  // Generate random armor
  const generateArmor = (): GeneratedItem => {
    const template = armorTemplates.value[Math.floor(Math.random() * armorTemplates.value.length)]
    
    const item: GeneratedItem = {
      id: `armor_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name: generateItemName(template.name),
      type: 'armor',
      subtype: 'protection',
      description: generateArmorDescription(template),
      price: calculatePrice(template.basePrice),
      availability: generateAvailability(),
      weight: generateWeight(template.basePrice / 3),
      qualities: generateQualities(armorQualities),
      flaws: generateFlaws(armorFlaws),
      condition: generateCondition(),
      culturalOrigin: generateCulturalOrigin(),
      rarity: generateRarity()
    }

    // Add enchantment chance
    if (Math.random() > 0.85) {
      item.enchantment = generateEnchantment('armor')
      item.rarity = Math.min(10, item.rarity + 2)
    }

    return item
  }

  // Generate random tool
  const generateTool = (): GeneratedItem => {
    const template = toolTemplates.value[Math.floor(Math.random() * toolTemplates.value.length)]
    
    const item: GeneratedItem = {
      id: `tool_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name: generateItemName(template.name),
      type: 'tool',
      subtype: template.profession || 'general',
      description: generateToolDescription(template),
      price: calculatePrice(template.basePrice),
      availability: generateAvailability(),
      weight: generateWeight(template.basePrice / 4),
      qualities: generateQualities(['Durable', 'Well-made', 'Precise']),
      flaws: generateFlaws(['Fragile', 'Worn', 'Incomplete']),
      condition: generateCondition(),
      culturalOrigin: generateCulturalOrigin(),
      rarity: generateRarity()
    }

    // Professional tools have higher chance of enchantment
    if (template.profession && Math.random() > 0.7) {
      item.enchantment = generateEnchantment('tool')
      item.rarity = Math.min(10, item.rarity + 1)
    }

    return item
  }

  // Generate random consumable
  const generateConsumable = (): GeneratedItem => {
    const template = consumableTemplates.value[Math.floor(Math.random() * consumableTemplates.value.length)]
    
    return {
      id: `consumable_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
      name: generateItemName(template.name),
      type: 'consumable',
      subtype: 'potion',
      description: generateConsumableDescription(template),
      price: calculatePrice(template.basePrice),
      availability: generateAvailability(),
      weight: 0.1,
      qualities: [],
      flaws: [],
      condition: 'good',
      culturalOrigin: generateCulturalOrigin(),
      rarity: generateRarity()
    }
  }

  // Generate magical item
  const generateMagicalItem = (): GeneratedItem => {
    const baseTypes = ['weapon', 'armor', 'tool']
    const baseType = baseTypes[Math.floor(Math.random() * baseTypes.length)]
    
    let item: GeneratedItem
    
    switch (baseType) {
      case 'weapon':
        item = generateWeapon()
        break
      case 'armor':
        item = generateArmor()
        break
      default:
        item = generateTool()
    }

    // Force magical properties
    item.type = 'magical'
    item.enchantment = generateEnchantment(baseType)
    item.rarity = Math.max(6, item.rarity + 3)
    item.price *= 5 // Magical items are expensive
    item.history = generateItemHistory(item)

    return item
  }

  // Generate item name with Polish influence
  const generateItemName = (baseName: string): string => {
    if (Math.random() > 0.7) {
      const prefix = polishPrefixes[Math.floor(Math.random() * polishPrefixes.length)]
      return `${prefix} ${baseName}`
    }
    
    if (Math.random() > 0.8) {
      const suffix = polishSuffixes[Math.floor(Math.random() * polishSuffixes.length)]
      return `${baseName}${suffix}`
    }

    return baseName
  }

  // Generate item descriptions
  const generateWeaponDescription = (template: any): string => {
    const descriptions = [
      `A well-crafted ${template.name.toLowerCase()} with ${template.damage} damage potential.`,
      `This ${template.name.toLowerCase()} shows signs of skilled craftsmanship.`,
      `A reliable ${template.name.toLowerCase()} suitable for combat.`,
      `An expertly balanced ${template.name.toLowerCase()} with good reach.`
    ]
    return descriptions[Math.floor(Math.random() * descriptions.length)]
  }

  const generateArmorDescription = (template: any): string => {
    const descriptions = [
      `Protective ${template.name.toLowerCase()} offering ${template.ap} armor points.`,
      `Well-made ${template.name.toLowerCase()} that covers vital areas.`,
      `Sturdy ${template.name.toLowerCase()} designed for battlefield protection.`,
      `Quality ${template.name.toLowerCase()} crafted by skilled armorers.`
    ]
    return descriptions[Math.floor(Math.random() * descriptions.length)]
  }

  const generateToolDescription = (template: any): string => {
    const descriptions = [
      `Professional ${template.name.toLowerCase()} used by skilled craftsmen.`,
      `Well-maintained ${template.name.toLowerCase()} in working condition.`,
      `Quality ${template.name.toLowerCase()} suitable for trade work.`,
      `Reliable ${template.name.toLowerCase()} showing signs of regular use.`
    ]
    return descriptions[Math.floor(Math.random() * descriptions.length)]
  }

  const generateConsumableDescription = (template: any): string => {
    return `${template.name} - ${template.effect}. Single use item.`
  }

  // Generate item properties
  const calculatePrice = (basePrice: number): number => {
    const variation = 0.8 + (Math.random() * 0.4) // ±20% variation
    return Math.round(basePrice * variation)
  }

  const generateAvailability = (): 'common' | 'scarce' | 'rare' | 'exotic' => {
    const roll = Math.random()
    if (roll < 0.5) return 'common'
    if (roll < 0.8) return 'scarce'
    if (roll < 0.95) return 'rare'
    return 'exotic'
  }

  const generateWeight = (baseWeight: number): number => {
    return Math.round((baseWeight + (Math.random() * 2 - 1)) * 10) / 10
  }

  const generateQualities = (possibleQualities: string[]): string[] => {
    const numQualities = Math.floor(Math.random() * 3)
    const selected = []
    
    for (let i = 0; i < numQualities; i++) {
      const quality = possibleQualities[Math.floor(Math.random() * possibleQualities.length)]
      if (!selected.includes(quality)) {
        selected.push(quality)
      }
    }
    
    return selected
  }

  const generateFlaws = (possibleFlaws: string[]): string[] => {
    if (Math.random() > 0.7) {
      const flaw = possibleFlaws[Math.floor(Math.random() * possibleFlaws.length)]
      return [flaw]
    }
    return []
  }

  const generateCondition = (): 'poor' | 'average' | 'good' | 'excellent' => {
    const roll = Math.random()
    if (roll < 0.1) return 'poor'
    if (roll < 0.4) return 'average'
    if (roll < 0.8) return 'good'
    return 'excellent'
  }

  const generateRarity = (): number => {
    const roll = Math.random()
    if (roll < 0.4) return Math.floor(Math.random() * 3) + 1 // 1-3
    if (roll < 0.7) return Math.floor(Math.random() * 3) + 4 // 4-6
    if (roll < 0.9) return Math.floor(Math.random() * 2) + 7 // 7-8
    return Math.floor(Math.random() * 2) + 9 // 9-10
  }

  const generateCulturalOrigin = (): string => {
    const origins = [
      'Empire', 'Bretonnian', 'Dwarf', 'Elven', 'Tilean', 'Estalian',
      'Norscan', 'Kislevite', 'Arabian', 'Cathayan'
    ]
    return origins[Math.floor(Math.random() * origins.length)]
  }

  // Generate enchantments
  const generateEnchantment = (itemType: string): Enchantment => {
    const templates = enchantmentTemplates.value[itemType] || enchantmentTemplates.value.weapon
    const template = templates[Math.floor(Math.random() * templates.length)]
    
    return {
      name: template.name,
      description: `Magical enhancement: ${template.effect}`,
      effect: template.effect,
      school: template.school,
      power: template.power,
      charges: template.power === 'minor' ? undefined : Math.floor(Math.random() * 10) + 5
    }
  }

  // Generate item history
  const generateItemHistory = (item: GeneratedItem): string => {
    const histories = [
      `This ${item.name.toLowerCase()} once belonged to a famous hero.`,
      `Forged during the great war, this item has seen many battles.`,
      `A family heirloom passed down through generations.`,
      `Discovered in ancient ruins, its true origin is unknown.`,
      `Blessed by a priest before a crucial battle.`,
      `Crafted by a master artisan at the height of their skill.`,
      `Stolen from a noble's collection years ago.`,
      `Found on a battlefield after a great victory.`
    ]
    return histories[Math.floor(Math.random() * histories.length)]
  }

  // Batch generation
  const generateItemSet = (count: number, type?: string): GeneratedItem[] => {
    const items: GeneratedItem[] = []
    
    for (let i = 0; i < count; i++) {
      switch (type) {
        case 'weapon':
          items.push(generateWeapon())
          break
        case 'armor':
          items.push(generateArmor())
          break
        case 'tool':
          items.push(generateTool())
          break
        case 'consumable':
          items.push(generateConsumable())
          break
        case 'magical':
          items.push(generateMagicalItem())
          break
        default:
          // Random type
          const types = ['weapon', 'armor', 'tool', 'consumable']
          const randomType = types[Math.floor(Math.random() * types.length)]
          switch (randomType) {
            case 'weapon':
              items.push(generateWeapon())
              break
            case 'armor':
              items.push(generateArmor())
              break
            case 'tool':
              items.push(generateTool())
              break
            case 'consumable':
              items.push(generateConsumable())
              break
          }
      }
    }
    
    return items
  }

  return {
    // Generation functions
    generateWeapon,
    generateArmor,
    generateTool,
    generateConsumable,
    generateMagicalItem,
    generateItemSet,
    
    // Utility functions
    generateItemName,
    generateEnchantment,
    calculatePrice,
    
    // Templates
    weaponTemplates: readonly(weaponTemplates),
    armorTemplates: readonly(armorTemplates),
    toolTemplates: readonly(toolTemplates),
    consumableTemplates: readonly(consumableTemplates),
    enchantmentTemplates: readonly(enchantmentTemplates)
  }
}
