"""
Event system for the Warhammer Fantasy Tavern Simulator
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Callable
import random
from datetime import datetime
from .enums import EventType, InteractionType
from .character import Character

@dataclass
class Event:
    """Represents an event in the tavern"""
    
    event_type: EventType
    title: str
    description: str
    participants: List[str] = field(default_factory=list)
    effects: Dict[str, any] = field(default_factory=dict)
    duration: int = 1  # Duration in turns/rounds
    timestamp: datetime = field(default_factory=datetime.now)
    resolved: bool = False
    
    def apply_effects(self, tavern, characters: Dict[str, Character]):
        """Apply the event's effects to the tavern and characters"""
        if self.resolved:
            return
        
        # Apply tension changes
        if 'tension_change' in self.effects:
            tavern.increase_tension(self.effects['tension_change'])
        
        # Apply character effects
        for char_name in self.participants:
            if char_name in characters:
                character = characters[char_name]
                self.apply_character_effects(character)
        
        self.resolved = True
    
    def apply_character_effects(self, character: Character):
        """Apply effects to a specific character"""
        if 'mood_change' in self.effects:
            character.current_mood = self.effects['mood_change']
        
        if 'health_change' in self.effects:
            character.health = max(0, min(100, character.health + self.effects['health_change']))
        
        if 'wealth_change' in self.effects:
            character.wealth = max(0, character.wealth + self.effects['wealth_change'])
        
        if 'drunk_change' in self.effects:
            character.drunk_level = max(0, min(10, character.drunk_level + self.effects['drunk_change']))

@dataclass
class Interaction:
    """Represents an interaction between characters"""
    
    initiator: str
    target: str
    interaction_type: InteractionType
    skill_used: str
    dice_roll: int
    modifier: int
    success: bool
    outcome_description: str
    relationship_change: int = 0
    timestamp: datetime = field(default_factory=datetime.now)
    
    def __str__(self) -> str:
        return f"{self.initiator} -> {self.target}: {self.interaction_type.value} ({'Success' if self.success else 'Failure'})"

class EventGenerator:
    """Generates random events for the tavern"""
    
    def __init__(self):
        self.event_templates = self._initialize_event_templates()
    
    def _initialize_event_templates(self) -> Dict[EventType, List[Dict]]:
        """Initialize event templates"""
        return {
            EventType.BRAWL: [
                {
                    'title': 'Tavern Brawl',
                    'description': 'A heated argument escalates into a full tavern brawl!',
                    'effects': {'tension_change': -20, 'health_change': -15},
                    'min_participants': 2
                },
                {
                    'title': 'Drunken Scuffle',
                    'description': 'Two drunk patrons start throwing punches over a spilled drink.',
                    'effects': {'tension_change': -10, 'health_change': -5},
                    'min_participants': 2
                }
            ],
            EventType.CELEBRATION: [
                {
                    'title': 'Victory Celebration',
                    'description': 'News of a military victory reaches the tavern, sparking celebration!',
                    'effects': {'tension_change': -15, 'mood_change': 'festive', 'drunk_change': 2},
                    'min_participants': 3
                },
                {
                    'title': 'Birthday Celebration',
                    'description': 'A patron celebrates their birthday with drinks for everyone!',
                    'effects': {'tension_change': -10, 'mood_change': 'happy', 'drunk_change': 1},
                    'min_participants': 1
                }
            ],
            EventType.MYSTERIOUS_VISITOR: [
                {
                    'title': 'Hooded Stranger',
                    'description': 'A mysterious hooded figure enters the tavern, drawing suspicious glances.',
                    'effects': {'tension_change': 10, 'mood_change': 'suspicious'},
                    'min_participants': 0
                },
                {
                    'title': 'Witch Hunter Arrival',
                    'description': 'A grim Witch Hunter enters, causing unease among the patrons.',
                    'effects': {'tension_change': 20, 'mood_change': 'nervous'},
                    'min_participants': 0
                }
            ],
            EventType.MERCHANT_ARRIVAL: [
                {
                    'title': 'Traveling Merchant',
                    'description': 'A merchant arrives with exotic goods and tales from distant lands.',
                    'effects': {'tension_change': -5, 'mood_change': 'curious'},
                    'min_participants': 1
                }
            ],
            EventType.NEWS_ARRIVAL: [
                {
                    'title': 'War News',
                    'description': 'A messenger brings disturbing news from the front lines.',
                    'effects': {'tension_change': 15, 'mood_change': 'worried'},
                    'min_participants': 0
                },
                {
                    'title': 'Good Harvest News',
                    'description': 'Word spreads of an excellent harvest, lifting spirits.',
                    'effects': {'tension_change': -10, 'mood_change': 'optimistic'},
                    'min_participants': 0
                }
            ],
            EventType.DRINKING_CONTEST: [
                {
                    'title': 'Drinking Contest',
                    'description': 'A drinking contest begins, with patrons cheering on the participants.',
                    'effects': {'tension_change': -5, 'drunk_change': 3, 'mood_change': 'competitive'},
                    'min_participants': 2
                }
            ],
            EventType.STORYTELLING: [
                {
                    'title': 'Bard\'s Tale',
                    'description': 'A skilled bard captivates the audience with an epic tale.',
                    'effects': {'tension_change': -10, 'mood_change': 'entertained'},
                    'min_participants': 1
                }
            ],
            EventType.GAMBLING_GAME: [
                {
                    'title': 'Dice Game',
                    'description': 'A high-stakes dice game draws a crowd of spectators.',
                    'effects': {'tension_change': 5, 'mood_change': 'excited'},
                    'min_participants': 2
                }
            ],
            EventType.RELIGIOUS_CEREMONY: [
                {
                    'title': 'Prayer Circle',
                    'description': 'A priest leads the faithful in prayer for protection.',
                    'effects': {'tension_change': -15, 'mood_change': 'peaceful'},
                    'min_participants': 1
                }
            ],
            EventType.WEATHER_CHANGE: [
                {
                    'title': 'Storm Arrives',
                    'description': 'A fierce storm begins, trapping everyone inside the tavern.',
                    'effects': {'tension_change': 10, 'mood_change': 'restless'},
                    'min_participants': 0
                }
            ]
        }
    
    def generate_random_event(self, available_characters: List[Character], current_tension: int) -> Optional[Event]:
        """Generate a random event based on current conditions"""
        # Weight event types based on current tension
        event_weights = {
            EventType.BRAWL: max(0, current_tension - 30),
            EventType.CELEBRATION: max(0, 50 - current_tension),
            EventType.MYSTERIOUS_VISITOR: 20,
            EventType.MERCHANT_ARRIVAL: 15,
            EventType.NEWS_ARRIVAL: 25,
            EventType.DRINKING_CONTEST: 20,
            EventType.STORYTELLING: 15,
            EventType.GAMBLING_GAME: 20,
            EventType.RELIGIOUS_CEREMONY: max(0, 30 - current_tension),
            EventType.WEATHER_CHANGE: 10
        }
        
        # Select event type based on weights
        total_weight = sum(event_weights.values())
        if total_weight == 0:
            return None
        
        rand_val = random.randint(1, total_weight)
        current_weight = 0
        selected_event_type = None
        
        for event_type, weight in event_weights.items():
            current_weight += weight
            if rand_val <= current_weight:
                selected_event_type = event_type
                break
        
        if not selected_event_type:
            return None
        
        # Select specific event template
        templates = self.event_templates.get(selected_event_type, [])
        if not templates:
            return None
        
        template = random.choice(templates)
        
        # Select participants
        participants = []
        min_participants = template.get('min_participants', 0)
        max_participants = min(len(available_characters), min_participants + 3)
        
        if min_participants > 0 and available_characters:
            num_participants = random.randint(min_participants, max_participants)
            participants = random.sample([char.name for char in available_characters], 
                                       min(num_participants, len(available_characters)))
        
        # Create event
        event = Event(
            event_type=selected_event_type,
            title=template['title'],
            description=template['description'],
            participants=participants,
            effects=template.get('effects', {}),
            duration=template.get('duration', 1)
        )
        
        return event
    
    def generate_rumor(self, characters: List[Character]) -> Optional[str]:
        """Generate a random rumor"""
        if not characters:
            return None
        
        rumor_templates = [
            "I heard {char1} has been seen talking to suspicious figures.",
            "They say {char1} owes money to dangerous people.",
            "Word is that {char1} knows secrets about the local nobility.",
            "I've heard {char1} and {char2} have been meeting in secret.",
            "There are whispers that {char1} practices forbidden magic.",
            "Some say {char1} is not who they claim to be.",
            "I heard {char1} has a bounty on their head.",
            "They say {char1} once saved the life of an important person.",
            "Word is spreading that {char1} has found treasure.",
            "I've heard {char1} is planning to leave town soon."
        ]
        
        template = random.choice(rumor_templates)
        char1 = random.choice(characters)
        
        if '{char2}' in template:
            other_chars = [c for c in characters if c != char1]
            if other_chars:
                char2 = random.choice(other_chars)
                return template.format(char1=char1.name, char2=char2.name)
            else:
                return None
        else:
            return template.format(char1=char1.name)

class RumorSystem:
    """Manages the spread of rumors and gossip in the tavern"""
    
    def __init__(self):
        self.active_rumors: List[str] = []
        self.rumor_spread_chance = 0.3
    
    def add_rumor(self, rumor: str):
        """Add a new rumor to the system"""
        if rumor and rumor not in self.active_rumors:
            self.active_rumors.append(rumor)
            # Keep only the most recent 10 rumors
            if len(self.active_rumors) > 10:
                self.active_rumors.pop(0)
    
    def spread_rumor(self, speaker: Character, listener: Character) -> Optional[str]:
        """Attempt to spread a rumor between characters"""
        if not self.active_rumors:
            return None
        
        if random.random() < self.rumor_spread_chance:
            rumor = random.choice(self.active_rumors)
            # Modify relationship slightly based on rumor content
            if listener.name in rumor:
                speaker.modify_relationship(listener.name, -1)
            return rumor
        
        return None
    
    def get_random_rumor(self) -> Optional[str]:
        """Get a random active rumor"""
        return random.choice(self.active_rumors) if self.active_rumors else None
