"""
Character class for the Warhammer Fantasy Tavern Simulator
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import random
from .enums import Faction, CharacterClass, Skill, RelationshipType

@dataclass
class Character:
    """Represents a character in the tavern simulator"""
    
    # Basic Information
    name: str
    faction: Faction
    character_class: CharacterClass
    age: int
    gender: str
    
    # Physical Description
    appearance: str
    distinctive_features: str
    
    # Background
    backstory: str
    motivation: str
    secrets: List[str] = field(default_factory=list)
    
    # Skills and Abilities
    skills: Dict[Skill, int] = field(default_factory=dict)
    special_abilities: List[str] = field(default_factory=list)
    
    # Personality
    personality_traits: List[str] = field(default_factory=list)
    likes: List[str] = field(default_factory=list)
    dislikes: List[str] = field(default_factory=list)
    
    # Social
    relationships: Dict[str, RelationshipType] = field(default_factory=dict)
    reputation: int = 0
    
    # Status
    current_mood: str = "neutral"
    health: int = 100
    wealth: int = 50
    drunk_level: int = 0
    
    # Dialogue
    greeting_phrases: List[str] = field(default_factory=list)
    faction_specific_phrases: List[str] = field(default_factory=list)
    
    def __post_init__(self):
        """Initialize default values after creation"""
        if not self.skills:
            self.initialize_default_skills()
        if not self.greeting_phrases:
            self.initialize_default_phrases()
    
    def initialize_default_skills(self):
        """Initialize default skill values based on character class and faction"""
        # Base skills for all characters
        base_skills = {
            Skill.COMBAT: 5,
            Skill.DIPLOMACY: 5,
            Skill.INTIMIDATION: 5,
            Skill.DECEPTION: 5,
            Skill.PERCEPTION: 5,
            Skill.KNOWLEDGE: 5,
            Skill.TRADE: 5,
            Skill.STEALTH: 5,
            Skill.MAGIC: 1,
            Skill.FAITH: 3,
            Skill.LEADERSHIP: 3,
            Skill.SURVIVAL: 5,
            Skill.CRAFTING: 3,
            Skill.PERFORMANCE: 3,
            Skill.GAMBLING: 3
        }
        
        # Modify based on character class
        class_modifiers = self.get_class_skill_modifiers()
        for skill, modifier in class_modifiers.items():
            base_skills[skill] += modifier
        
        # Modify based on faction
        faction_modifiers = self.get_faction_skill_modifiers()
        for skill, modifier in faction_modifiers.items():
            base_skills[skill] += modifier
        
        # Ensure skills are within valid range (1-20)
        for skill in base_skills:
            base_skills[skill] = max(1, min(20, base_skills[skill]))
        
        self.skills = base_skills
    
    def get_class_skill_modifiers(self) -> Dict[Skill, int]:
        """Get skill modifiers based on character class"""
        modifiers = {
            CharacterClass.WARRIOR: {
                Skill.COMBAT: 5, Skill.INTIMIDATION: 3, Skill.LEADERSHIP: 2
            },
            CharacterClass.ROGUE: {
                Skill.STEALTH: 5, Skill.DECEPTION: 4, Skill.PERCEPTION: 3
            },
            CharacterClass.WIZARD: {
                Skill.MAGIC: 8, Skill.KNOWLEDGE: 5, Skill.PERCEPTION: 2
            },
            CharacterClass.PRIEST: {
                Skill.FAITH: 6, Skill.DIPLOMACY: 4, Skill.LEADERSHIP: 3
            },
            CharacterClass.MERCHANT: {
                Skill.TRADE: 6, Skill.DIPLOMACY: 4, Skill.DECEPTION: 2
            },
            CharacterClass.CRAFTSMAN: {
                Skill.CRAFTING: 6, Skill.TRADE: 3, Skill.KNOWLEDGE: 2
            },
            CharacterClass.NOBLE: {
                Skill.LEADERSHIP: 4, Skill.DIPLOMACY: 4, Skill.KNOWLEDGE: 2
            },
            CharacterClass.PEASANT: {
                Skill.SURVIVAL: 4, Skill.CRAFTING: 2, Skill.TRADE: 1
            },
            CharacterClass.SOLDIER: {
                Skill.COMBAT: 4, Skill.INTIMIDATION: 2, Skill.SURVIVAL: 2
            },
            CharacterClass.SCOUT: {
                Skill.SURVIVAL: 5, Skill.STEALTH: 4, Skill.PERCEPTION: 4
            },
            CharacterClass.BARD: {
                Skill.PERFORMANCE: 6, Skill.DIPLOMACY: 4, Skill.KNOWLEDGE: 3
            },
            CharacterClass.SCHOLAR: {
                Skill.KNOWLEDGE: 6, Skill.MAGIC: 2, Skill.PERCEPTION: 2
            },
            CharacterClass.HUNTER: {
                Skill.SURVIVAL: 5, Skill.COMBAT: 3, Skill.STEALTH: 3
            },
            CharacterClass.SAILOR: {
                Skill.SURVIVAL: 4, Skill.COMBAT: 2, Skill.TRADE: 2
            },
            CharacterClass.INNKEEPER: {
                Skill.DIPLOMACY: 4, Skill.TRADE: 3, Skill.PERCEPTION: 3
            },
            CharacterClass.WITCH_HUNTER: {
                Skill.COMBAT: 4, Skill.FAITH: 5, Skill.INTIMIDATION: 4
            },
            CharacterClass.CULTIST: {
                Skill.MAGIC: 4, Skill.DECEPTION: 5, Skill.STEALTH: 3
            }
        }
        return modifiers.get(self.character_class, {})
    
    def get_faction_skill_modifiers(self) -> Dict[Skill, int]:
        """Get skill modifiers based on faction"""
        modifiers = {
            Faction.EMPIRE: {
                Skill.DIPLOMACY: 2, Skill.TRADE: 2, Skill.LEADERSHIP: 1
            },
            Faction.DWARF: {
                Skill.COMBAT: 2, Skill.CRAFTING: 3, Skill.INTIMIDATION: 1
            },
            Faction.HIGH_ELF: {
                Skill.MAGIC: 3, Skill.KNOWLEDGE: 2, Skill.DIPLOMACY: 1
            },
            Faction.WOOD_ELF: {
                Skill.SURVIVAL: 3, Skill.STEALTH: 2, Skill.PERCEPTION: 2
            },
            Faction.BRETONNIAN: {
                Skill.COMBAT: 2, Skill.LEADERSHIP: 2, Skill.FAITH: 1
            },
            Faction.HALFLING: {
                Skill.STEALTH: 2, Skill.TRADE: 2, Skill.SURVIVAL: 1
            },
            Faction.TILEAN: {
                Skill.TRADE: 3, Skill.DECEPTION: 2, Skill.DIPLOMACY: 1
            },
            Faction.KISLEV: {
                Skill.SURVIVAL: 3, Skill.COMBAT: 2, Skill.INTIMIDATION: 1
            },
            Faction.NORSE: {
                Skill.COMBAT: 3, Skill.SURVIVAL: 2, Skill.INTIMIDATION: 2
            }
        }
        return modifiers.get(self.faction, {})
    
    def initialize_default_phrases(self):
        """Initialize default greeting and faction-specific phrases"""
        self.greeting_phrases = [
            "Well met, stranger.",
            "What brings you to these parts?",
            "Care to join me for a drink?",
            "I haven't seen you around here before.",
            "The road has been long, hasn't it?"
        ]
        
        # Add faction-specific phrases
        faction_phrases = {
            Faction.DWARF: [
                "By Grungni's beard!",
                "The ale here is decent, for manling brew.",
                "I've got grudges to settle.",
                "The mountains call to me."
            ],
            Faction.HIGH_ELF: [
                "How... quaint this establishment is.",
                "I suppose this will suffice for now.",
                "The winds of magic are restless tonight.",
                "Such crude accommodations."
            ],
            Faction.EMPIRE: [
                "Sigmar protect us all.",
                "The Emperor's will be done.",
                "These are troubled times indeed.",
                "For the Empire!"
            ]
        }
        
        self.faction_specific_phrases = faction_phrases.get(self.faction, [])
    
    def get_skill_value(self, skill: Skill) -> int:
        """Get the value of a specific skill"""
        return self.skills.get(skill, 5)
    
    def modify_relationship(self, other_character: str, change: int):
        """Modify relationship with another character"""
        current = self.relationships.get(other_character, RelationshipType.NEUTRAL)
        new_value = max(-3, min(3, int(current) + change))
        self.relationships[other_character] = RelationshipType(new_value)
    
    def get_relationship(self, other_character: str) -> RelationshipType:
        """Get relationship status with another character"""
        return self.relationships.get(other_character, RelationshipType.NEUTRAL)
    
    def can_interact_with(self, other_character: 'Character') -> bool:
        """Check if this character can interact with another"""
        relationship = self.get_relationship(other_character.name)
        return relationship > RelationshipType.HATRED
    
    def get_interaction_modifier(self, other_character: 'Character') -> int:
        """Get modifier for interactions based on relationship"""
        relationship = self.get_relationship(other_character.name)
        return int(relationship)
    
    def is_drunk(self) -> bool:
        """Check if character is drunk"""
        return self.drunk_level > 3
    
    def drink_alcohol(self):
        """Character drinks alcohol, increasing drunk level"""
        self.drunk_level = min(10, self.drunk_level + 1)
        if self.drunk_level > 5:
            self.current_mood = "drunk"
    
    def sober_up(self):
        """Character sobers up over time"""
        if self.drunk_level > 0:
            self.drunk_level = max(0, self.drunk_level - 1)
        if self.drunk_level <= 3:
            self.current_mood = "neutral"
    
    def __str__(self) -> str:
        return f"{self.name} ({self.faction.value} {self.character_class.value})"
    
    def __repr__(self) -> str:
        return self.__str__()

    def to_dict(self) -> dict:
        """Convert character to dictionary for serialization"""
        return {
            'name': self.name,
            'faction': self.faction.value,
            'character_class': self.character_class.value,
            'age': self.age,
            'gender': self.gender,
            'appearance': self.appearance,
            'distinctive_features': self.distinctive_features,
            'backstory': self.backstory,
            'motivation': self.motivation,
            'secrets': self.secrets,
            'skills': {skill.value: value for skill, value in self.skills.items()},
            'special_abilities': self.special_abilities,
            'personality_traits': self.personality_traits,
            'likes': self.likes,
            'dislikes': self.dislikes,
            'relationships': {name: int(rel) for name, rel in self.relationships.items()},
            'reputation': self.reputation,
            'current_mood': self.current_mood,
            'health': self.health,
            'wealth': self.wealth,
            'drunk_level': self.drunk_level,
            'greeting_phrases': self.greeting_phrases,
            'faction_specific_phrases': self.faction_specific_phrases
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Character':
        """Create character from dictionary"""
        character = cls(
            name=data['name'],
            faction=Faction(data['faction']),
            character_class=CharacterClass(data['character_class']),
            age=data['age'],
            gender=data['gender'],
            appearance=data['appearance'],
            distinctive_features=data['distinctive_features'],
            backstory=data['backstory'],
            motivation=data['motivation'],
            secrets=data.get('secrets', []),
            special_abilities=data.get('special_abilities', []),
            personality_traits=data.get('personality_traits', []),
            likes=data.get('likes', []),
            dislikes=data.get('dislikes', []),
            reputation=data.get('reputation', 0),
            current_mood=data.get('current_mood', 'neutral'),
            health=data.get('health', 100),
            wealth=data.get('wealth', 50),
            drunk_level=data.get('drunk_level', 0),
            greeting_phrases=data.get('greeting_phrases', []),
            faction_specific_phrases=data.get('faction_specific_phrases', [])
        )

        # Restore skills
        if 'skills' in data:
            character.skills = {Skill(skill): value for skill, value in data['skills'].items()}

        # Restore relationships
        if 'relationships' in data:
            character.relationships = {name: RelationshipType(rel) for name, rel in data['relationships'].items()}

        return character
