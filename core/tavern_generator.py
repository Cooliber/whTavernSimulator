"""
Tavern generation system for the Warhammer Fantasy Tavern Simulator
"""

import random
from typing import List, Dict
from .tavern import Tavern
from .enums import TavernQuality, AtmosphereType

class TavernGenerator:
    """Generates randomized taverns with Warhammer Fantasy flavor"""
    
    def __init__(self):
        self.tavern_names = self._initialize_tavern_names()
        self.location_types = self._initialize_locations()
        self.description_templates = self._initialize_descriptions()
    
    def _initialize_tavern_names(self) -> List[str]:
        """Initialize list of tavern names with Warhammer Fantasy flavor"""
        return [
            "The Prancing Pony",
            "The Drunken Dragon",
            "The Hammer and Anvil",
            "The Bloody Crown",
            "The Sigmar's Rest",
            "The Golden Griffin",
            "The Crooked Billet",
            "The Red Moon Rising",
            "The Slaughtered Lamb",
            "The Boar's Head",
            "The Crossed Swords",
            "The Weary Traveler",
            "The Black Powder Inn",
            "The Merchant's Rest",
            "The Chaos Moon",
            "The Emperor's Grace",
            "The Dwarf's Beard",
            "The Elf's Bane",
            "The Witch's Cauldron",
            "The Goblin's Demise",
            "The Orc's Folly",
            "The Rat Catcher",
            "The Plague Doctor",
            "The Burning Heretic",
            "The Faithful Servant",
            "The Noble's Purse",
            "The Peasant's Dream",
            "The Soldier's Return",
            "The Merchant's Gold",
            "The Thief's Haven",
            "The Scholar's Quill",
            "The Bard's Tale",
            "The Hunter's Lodge",
            "The Sailor's Rest",
            "The Pilgrim's Path",
            "The Wanderer's End",
            "The Last Stand",
            "The First Light",
            "The Broken Shield",
            "The Mended Sword",
            "The Lucky Coin",
            "The Cursed Chalice",
            "The Sacred Flame",
            "The Dark Corner",
            "The Bright Hope",
            "The Storm's End",
            "The Calm Harbor",
            "The Wild Hunt",
            "The Tame Beast",
            "The Free Company"
        ]
    
    def _initialize_locations(self) -> List[Dict[str, str]]:
        """Initialize location types and descriptions"""
        return [
            {
                "type": "City District",
                "description": "Located in the bustling merchant quarter of a major city"
            },
            {
                "type": "Village Center",
                "description": "The heart of a small farming village"
            },
            {
                "type": "Crossroads",
                "description": "At the intersection of two major trade routes"
            },
            {
                "type": "River Port",
                "description": "Along a busy river used for trade and transport"
            },
            {
                "type": "Mountain Pass",
                "description": "A welcome rest stop in treacherous mountain terrain"
            },
            {
                "type": "Forest Edge",
                "description": "On the border between civilization and the wild woods"
            },
            {
                "type": "Border Town",
                "description": "In a fortified town near hostile territory"
            },
            {
                "type": "Mining Settlement",
                "description": "Serving the workers of nearby mines and quarries"
            },
            {
                "type": "Pilgrimage Route",
                "description": "Along a path traveled by religious pilgrims"
            },
            {
                "type": "University District",
                "description": "Near a center of learning and scholarship"
            }
        ]
    
    def _initialize_descriptions(self) -> Dict[TavernQuality, List[str]]:
        """Initialize description templates based on tavern quality"""
        return {
            TavernQuality.TERRIBLE: [
                "A ramshackle establishment with rotting timbers and a leaking roof. The ale is watered down and the food questionable.",
                "This dive is barely standing, with broken furniture and suspicious stains everywhere. Only the desperate drink here.",
                "A wretched hovel masquerading as a tavern. The smell alone is enough to turn stomachs.",
                "This place has seen better days - much better days. Everything seems to be falling apart."
            ],
            TavernQuality.POOR: [
                "A run-down tavern with creaky floors and dim lighting. The service is slow and the atmosphere unwelcoming.",
                "This establishment has clearly seen better times. The furniture is worn and the ale is cheap.",
                "A modest tavern that struggles to maintain basic standards. The food is edible but uninspiring.",
                "This place serves its purpose but little more. Don't expect luxury or even basic comfort."
            ],
            TavernQuality.AVERAGE: [
                "A typical tavern with decent ale and simple food. Nothing special, but it serves its purpose well.",
                "This establishment offers standard fare at reasonable prices. The atmosphere is comfortable if unremarkable.",
                "A solid, dependable tavern that caters to common folk. The service is adequate and the prices fair.",
                "This place provides exactly what you'd expect - no more, no less. A reliable stop for travelers."
            ],
            TavernQuality.GOOD: [
                "A well-maintained tavern with quality ale and hearty food. The atmosphere is warm and welcoming.",
                "This establishment takes pride in its service and offerings. The rooms are clean and the staff friendly.",
                "A respectable tavern that attracts a better class of clientele. The food is well-prepared and the ale fresh.",
                "This place has earned a good reputation through consistent quality and fair dealing."
            ],
            TavernQuality.EXCELLENT: [
                "A premier establishment with the finest ales, exquisite food, and impeccable service. A true gem.",
                "This tavern sets the standard for excellence. Every detail is perfect, from the polished floors to the vintage wines.",
                "A luxurious establishment that caters to nobles and wealthy merchants. The service is exceptional.",
                "This place is renowned throughout the region for its quality. Even royalty has been known to visit."
            ]
        }
    
    def generate_tavern(self, name: str = None, quality: TavernQuality = None) -> Tavern:
        """Generate a randomized tavern"""
        # Select or generate name
        if name is None:
            name = random.choice(self.tavern_names)
        
        # Select or generate quality
        if quality is None:
            quality = random.choice(list(TavernQuality))
        
        # Select location
        location_info = random.choice(self.location_types)
        location = f"{location_info['type']}: {location_info['description']}"
        
        # Generate description based on quality
        base_description = random.choice(self.description_templates[quality])
        
        # Add atmospheric details
        atmospheric_details = self._generate_atmospheric_details(quality)
        description = f"{base_description} {atmospheric_details}"
        
        # Generate capacity based on quality
        capacity_ranges = {
            TavernQuality.TERRIBLE: (8, 15),
            TavernQuality.POOR: (12, 20),
            TavernQuality.AVERAGE: (15, 25),
            TavernQuality.GOOD: (20, 35),
            TavernQuality.EXCELLENT: (25, 50)
        }
        min_cap, max_cap = capacity_ranges[quality]
        capacity = random.randint(min_cap, max_cap)
        
        # Generate prices based on quality
        base_prices = {
            TavernQuality.TERRIBLE: {"ale": 1, "wine": 2, "food": 1, "room": 3},
            TavernQuality.POOR: {"ale": 1, "wine": 3, "food": 2, "room": 5},
            TavernQuality.AVERAGE: {"ale": 2, "wine": 5, "food": 3, "room": 8},
            TavernQuality.GOOD: {"ale": 3, "wine": 7, "food": 5, "room": 12},
            TavernQuality.EXCELLENT: {"ale": 5, "wine": 12, "food": 8, "room": 20}
        }
        prices = base_prices[quality]
        
        # Generate initial atmosphere
        atmosphere = self._generate_initial_atmosphere()
        
        # Create the tavern
        tavern = Tavern(
            name=name,
            description=description,
            location=location,
            service_quality=quality,
            atmosphere=atmosphere,
            atmosphere_description="",
            capacity=capacity,
            ale_price=prices["ale"],
            wine_price=prices["wine"],
            food_price=prices["food"],
            room_price=prices["room"],
            reputation=self._generate_initial_reputation(quality)
        )
        
        # Update atmosphere description
        tavern.update_atmosphere_description()
        
        return tavern
    
    def _generate_atmospheric_details(self, quality: TavernQuality) -> str:
        """Generate atmospheric details based on quality"""
        details = {
            TavernQuality.TERRIBLE: [
                "Rats scurry in the corners and the floorboards creak ominously.",
                "The windows are grimy and the air thick with smoke and unwashed bodies.",
                "Suspicious characters lurk in dark corners, and fights break out regularly.",
                "The place reeks of stale ale and worse things."
            ],
            TavernQuality.POOR: [
                "The common room is dimly lit by flickering candles.",
                "Rough wooden tables bear the scars of countless knife games.",
                "The hearth smokes badly, filling the room with haze.",
                "Patrons speak in hushed tones and eye strangers suspiciously."
            ],
            TavernQuality.AVERAGE: [
                "A warm fire crackles in the stone hearth.",
                "Simple wooden furniture fills the common room.",
                "Local folk gather here to share news and gossip.",
                "The atmosphere is comfortable and unpretentious."
            ],
            TavernQuality.GOOD: [
                "Polished wooden tables gleam in the lamplight.",
                "Comfortable chairs and benches invite long conversations.",
                "The walls are decorated with local artwork and trophies.",
                "A sense of prosperity and contentment pervades the establishment."
            ],
            TavernQuality.EXCELLENT: [
                "Crystal chandeliers cast warm light over marble floors.",
                "Rich tapestries and fine artwork adorn the walls.",
                "Servants in livery attend to every need with practiced efficiency.",
                "The atmosphere speaks of wealth, power, and refined taste."
            ]
        }
        
        return random.choice(details[quality])
    
    def _generate_initial_atmosphere(self) -> AtmosphereType:
        """Generate initial atmosphere type"""
        # Weight different atmospheres
        atmosphere_weights = {
            AtmosphereType.PEACEFUL: 20,
            AtmosphereType.LIVELY: 25,
            AtmosphereType.TENSE: 10,
            AtmosphereType.FESTIVE: 15,
            AtmosphereType.GLOOMY: 10,
            AtmosphereType.MYSTERIOUS: 8,
            AtmosphereType.ROWDY: 10,
            AtmosphereType.INTIMATE: 12
        }
        
        # Select based on weights
        total_weight = sum(atmosphere_weights.values())
        rand_val = random.randint(1, total_weight)
        current_weight = 0
        
        for atmosphere, weight in atmosphere_weights.items():
            current_weight += weight
            if rand_val <= current_weight:
                return atmosphere
        
        return AtmosphereType.LIVELY  # Default fallback
    
    def _generate_initial_reputation(self, quality: TavernQuality) -> int:
        """Generate initial reputation based on quality"""
        reputation_ranges = {
            TavernQuality.TERRIBLE: (5, 25),
            TavernQuality.POOR: (20, 40),
            TavernQuality.AVERAGE: (40, 60),
            TavernQuality.GOOD: (60, 80),
            TavernQuality.EXCELLENT: (80, 95)
        }
        
        min_rep, max_rep = reputation_ranges[quality]
        return random.randint(min_rep, max_rep)
    
    def get_random_tavern_name(self) -> str:
        """Get a random tavern name"""
        return random.choice(self.tavern_names)
