"""
Tavern class for the Warhammer Fantasy Tavern Simulator
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
import random
from .enums import TavernQuality, AtmosphereType, EventType
from .character import Character

@dataclass
class Tavern:
    """Represents a tavern in the simulator"""
    
    # Basic Information
    name: str
    description: str
    location: str
    
    # Quality and Atmosphere
    service_quality: TavernQuality
    atmosphere: AtmosphereType
    atmosphere_description: str
    
    # Physical Properties
    capacity: int
    current_occupancy: int = 0
    rooms_available: int = 5
    
    # Services and Prices
    ale_price: int = 2
    wine_price: int = 5
    food_price: int = 3
    room_price: int = 10
    
    # Characters and Events
    characters: List[Character] = field(default_factory=list)
    current_events: List[str] = field(default_factory=list)
    
    # Tension and Mood
    tension_level: int = 0  # 0-100
    noise_level: int = 30   # 0-100
    
    # History and Reputation
    reputation: int = 50    # 0-100
    notable_events: List[str] = field(default_factory=list)
    
    # Time and Weather
    time_of_day: str = "evening"
    weather: str = "clear"
    
    def __post_init__(self):
        """Initialize tavern after creation"""
        self.current_occupancy = len(self.characters)
    
    def add_character(self, character: Character) -> bool:
        """Add a character to the tavern"""
        if self.current_occupancy < self.capacity:
            self.characters.append(character)
            self.current_occupancy += 1
            self.update_atmosphere()
            return True
        return False
    
    def remove_character(self, character: Character) -> bool:
        """Remove a character from the tavern"""
        if character in self.characters:
            self.characters.remove(character)
            self.current_occupancy -= 1
            self.update_atmosphere()
            return True
        return False
    
    def get_character_by_name(self, name: str) -> Optional[Character]:
        """Get a character by name"""
        for character in self.characters:
            if character.name == name:
                return character
        return None
    
    def update_atmosphere(self):
        """Update tavern atmosphere based on current conditions"""
        # Base atmosphere on occupancy
        occupancy_ratio = self.current_occupancy / self.capacity
        
        if occupancy_ratio < 0.2:
            base_atmosphere = AtmosphereType.PEACEFUL
        elif occupancy_ratio < 0.5:
            base_atmosphere = AtmosphereType.LIVELY
        elif occupancy_ratio < 0.8:
            base_atmosphere = AtmosphereType.ROWDY
        else:
            base_atmosphere = AtmosphereType.TENSE
        
        # Modify based on tension level
        if self.tension_level > 70:
            self.atmosphere = AtmosphereType.TENSE
        elif self.tension_level > 40:
            self.atmosphere = AtmosphereType.ROWDY
        elif len([c for c in self.characters if c.is_drunk()]) > len(self.characters) / 2:
            self.atmosphere = AtmosphereType.FESTIVE
        else:
            self.atmosphere = base_atmosphere
        
        # Update atmosphere description
        self.update_atmosphere_description()
    
    def update_atmosphere_description(self):
        """Update the atmosphere description based on current atmosphere"""
        descriptions = {
            AtmosphereType.PEACEFUL: [
                "The tavern is quiet and serene, with soft conversations and gentle music.",
                "A calm atmosphere pervades the establishment, perfect for quiet contemplation.",
                "The peaceful ambiance is broken only by the crackling of the fireplace."
            ],
            AtmosphereType.LIVELY: [
                "The tavern buzzes with animated conversations and laughter.",
                "A vibrant energy fills the air as patrons enjoy their evening.",
                "The atmosphere is warm and welcoming, with a steady hum of activity."
            ],
            AtmosphereType.TENSE: [
                "An uncomfortable tension hangs in the air, with suspicious glances exchanged.",
                "The atmosphere is thick with unspoken conflicts and brewing trouble.",
                "Conversations are hushed and wary, as if everyone expects trouble."
            ],
            AtmosphereType.FESTIVE: [
                "The tavern erupts with celebration, music, and boisterous laughter.",
                "A party atmosphere dominates, with singing, dancing, and merriment.",
                "The festive mood is infectious, drawing everyone into the celebration."
            ],
            AtmosphereType.GLOOMY: [
                "A somber mood hangs over the tavern like a dark cloud.",
                "The atmosphere is heavy with sadness and melancholy.",
                "Even the flickering candles seem dimmer in the gloomy ambiance."
            ],
            AtmosphereType.MYSTERIOUS: [
                "Shadows dance in the corners, and whispered secrets fill the air.",
                "An air of mystery and intrigue permeates the establishment.",
                "Strange figures huddle in dark corners, speaking in hushed tones."
            ],
            AtmosphereType.ROWDY: [
                "The tavern is loud and boisterous, with raised voices and rough laughter.",
                "A raucous atmosphere prevails, with plenty of drinking and carousing.",
                "The noise level is high, with patrons becoming increasingly animated."
            ],
            AtmosphereType.INTIMATE: [
                "The tavern has a cozy, intimate feel with quiet conversations.",
                "Soft lighting and low voices create a personal, private atmosphere.",
                "The intimate setting encourages deep conversations and close bonds."
            ]
        }
        
        self.atmosphere_description = random.choice(descriptions.get(self.atmosphere, ["The tavern has an unremarkable atmosphere."]))
    
    def increase_tension(self, amount: int = 10):
        """Increase tension in the tavern"""
        self.tension_level = min(100, self.tension_level + amount)
        if self.tension_level > 80:
            self.trigger_brawl_check()
        self.update_atmosphere()
    
    def decrease_tension(self, amount: int = 5):
        """Decrease tension in the tavern"""
        self.tension_level = max(0, self.tension_level - amount)
        self.update_atmosphere()
    
    def trigger_brawl_check(self) -> bool:
        """Check if a brawl should be triggered"""
        brawl_chance = (self.tension_level - 50) / 50.0  # 0-1 based on tension above 50
        drunk_modifier = len([c for c in self.characters if c.is_drunk()]) / len(self.characters) if self.characters else 0
        
        final_chance = min(0.8, brawl_chance + drunk_modifier * 0.3)
        
        if random.random() < final_chance:
            self.trigger_brawl()
            return True
        return False
    
    def trigger_brawl(self):
        """Trigger a tavern brawl"""
        self.current_events.append("A brawl has broken out!")
        self.tension_level = max(0, self.tension_level - 30)  # Tension releases after brawl
        self.reputation = max(0, self.reputation - 10)  # Reputation suffers
        self.notable_events.append(f"A massive brawl erupted in the tavern at {self.time_of_day}")
        
        # Randomly injure some characters
        for character in self.characters:
            if random.random() < 0.3:  # 30% chance of injury
                character.health = max(10, character.health - random.randint(10, 30))
    
    def serve_drink(self, character: Character, drink_type: str = "ale") -> bool:
        """Serve a drink to a character"""
        prices = {"ale": self.ale_price, "wine": self.wine_price}
        price = prices.get(drink_type, self.ale_price)
        
        if character.wealth >= price:
            character.wealth -= price
            character.drink_alcohol()
            self.noise_level = min(100, self.noise_level + 2)
            return True
        return False
    
    def get_occupancy_ratio(self) -> float:
        """Get the current occupancy ratio"""
        return self.current_occupancy / self.capacity if self.capacity > 0 else 0
    
    def is_crowded(self) -> bool:
        """Check if the tavern is crowded"""
        return self.get_occupancy_ratio() > 0.8
    
    def get_status_summary(self) -> str:
        """Get a summary of the tavern's current status"""
        occupancy_desc = "crowded" if self.is_crowded() else "moderately busy" if self.get_occupancy_ratio() > 0.5 else "quiet"
        tension_desc = "very tense" if self.tension_level > 70 else "tense" if self.tension_level > 40 else "calm"
        
        return f"The {self.name} is {occupancy_desc} and {tension_desc}. {self.atmosphere_description}"
    
    def to_dict(self) -> dict:
        """Convert tavern to dictionary for serialization"""
        return {
            'name': self.name,
            'description': self.description,
            'location': self.location,
            'service_quality': self.service_quality.value,
            'atmosphere': self.atmosphere.value,
            'atmosphere_description': self.atmosphere_description,
            'capacity': self.capacity,
            'current_occupancy': self.current_occupancy,
            'rooms_available': self.rooms_available,
            'ale_price': self.ale_price,
            'wine_price': self.wine_price,
            'food_price': self.food_price,
            'room_price': self.room_price,
            'characters': [char.to_dict() for char in self.characters],
            'current_events': self.current_events,
            'tension_level': self.tension_level,
            'noise_level': self.noise_level,
            'reputation': self.reputation,
            'notable_events': self.notable_events,
            'time_of_day': self.time_of_day,
            'weather': self.weather
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Tavern':
        """Create tavern from dictionary"""
        from .character import Character
        
        tavern = cls(
            name=data['name'],
            description=data['description'],
            location=data['location'],
            service_quality=TavernQuality(data['service_quality']),
            atmosphere=AtmosphereType(data['atmosphere']),
            atmosphere_description=data['atmosphere_description'],
            capacity=data['capacity'],
            current_occupancy=data.get('current_occupancy', 0),
            rooms_available=data.get('rooms_available', 5),
            ale_price=data.get('ale_price', 2),
            wine_price=data.get('wine_price', 5),
            food_price=data.get('food_price', 3),
            room_price=data.get('room_price', 10),
            current_events=data.get('current_events', []),
            tension_level=data.get('tension_level', 0),
            noise_level=data.get('noise_level', 30),
            reputation=data.get('reputation', 50),
            notable_events=data.get('notable_events', []),
            time_of_day=data.get('time_of_day', 'evening'),
            weather=data.get('weather', 'clear')
        )
        
        # Restore characters
        if 'characters' in data:
            tavern.characters = [Character.from_dict(char_data) for char_data in data['characters']]
            tavern.current_occupancy = len(tavern.characters)
        
        return tavern
