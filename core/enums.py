"""
Enumerations for the Warhammer Fantasy Tavern Simulator
"""

from enum import Enum, IntEnum

class Faction(Enum):
    """Character factions in the Warhammer Fantasy universe"""
    EMPIRE = "Empire"
    DWARF = "Dwarf"
    HIGH_ELF = "High Elf"
    WOOD_ELF = "Wood Elf"
    BRETONNIAN = "Bretonnian"
    HALFLING = "Halfling"
    TILEAN = "Tilean"
    ESTALIA = "Estalia"
    KISLEV = "Kislev"
    NORSE = "Norse"
    ARABYAN = "Arabyan"
    CATHAYAN = "Cathayan"
    NIPPONESE = "Nipponese"
    MERCENARY = "Mercenary"
    OUTLAW = "Outlaw"
    CULTIST = "Cultist"
    WITCH_HUNTER = "Witch Hunter"

class CharacterClass(Enum):
    """Character classes/professions"""
    WARRIOR = "Warrior"
    ROGUE = "Rogue"
    WIZARD = "Wizard"
    PRIEST = "Priest"
    MERCHANT = "Merchant"
    CRAFTSMAN = "Craftsman"
    NOBLE = "Noble"
    PEASANT = "Peasant"
    SOLDIER = "Soldier"
    SCOUT = "Scout"
    BARD = "Bard"
    SCHOLAR = "Scholar"
    HUNTER = "Hunter"
    SAILOR = "Sailor"
    INNKEEPER = "Innkeeper"
    WITCH_HUNTER = "Witch Hunter"
    CULTIST = "Cultist"

class Skill(Enum):
    """Character skills"""
    COMBAT = "Combat"
    DIPLOMACY = "Diplomacy"
    INTIMIDATION = "Intimidation"
    DECEPTION = "Deception"
    PERCEPTION = "Perception"
    KNOWLEDGE = "Knowledge"
    TRADE = "Trade"
    STEALTH = "Stealth"
    MAGIC = "Magic"
    FAITH = "Faith"
    LEADERSHIP = "Leadership"
    SURVIVAL = "Survival"
    CRAFTING = "Crafting"
    PERFORMANCE = "Performance"
    GAMBLING = "Gambling"

class RelationshipType(IntEnum):
    """Relationship types with numeric values for easy comparison"""
    HATRED = -3
    DISLIKE = -2
    DISTRUST = -1
    NEUTRAL = 0
    ACQUAINTANCE = 1
    FRIENDSHIP = 2
    LOYALTY = 3

class InteractionType(Enum):
    """Types of character interactions"""
    CONVERSATION = "Conversation"
    TRADE = "Trade"
    GAMBLING = "Gambling"
    INFORMATION = "Information"
    INTIMIDATION = "Intimidation"
    PERSUASION = "Persuasion"
    BRAWL = "Brawl"
    DRINKING = "Drinking"
    STORYTELLING = "Storytelling"

class EventType(Enum):
    """Types of tavern events"""
    BRAWL = "Brawl"
    CELEBRATION = "Celebration"
    MYSTERIOUS_VISITOR = "Mysterious Visitor"
    MERCHANT_ARRIVAL = "Merchant Arrival"
    NEWS_ARRIVAL = "News Arrival"
    DRINKING_CONTEST = "Drinking Contest"
    STORYTELLING = "Storytelling"
    GAMBLING_GAME = "Gambling Game"
    RELIGIOUS_CEREMONY = "Religious Ceremony"
    WEATHER_CHANGE = "Weather Change"

class TavernQuality(IntEnum):
    """Tavern service quality levels"""
    TERRIBLE = 1
    POOR = 2
    AVERAGE = 3
    GOOD = 4
    EXCELLENT = 5

class AtmosphereType(Enum):
    """Tavern atmosphere types"""
    PEACEFUL = "Peaceful"
    LIVELY = "Lively"
    TENSE = "Tense"
    FESTIVE = "Festive"
    GLOOMY = "Gloomy"
    MYSTERIOUS = "Mysterious"
    ROWDY = "Rowdy"
    INTIMATE = "Intimate"
