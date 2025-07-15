"""
Main simulator class for the Warhammer Fantasy Tavern Simulator
"""

import random
import json
import pickle
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from .character import Character
from .character_generator import CharacterGenerator
from .tavern import Tavern
from .tavern_generator import TavernGenerator
from .dice_system import DiceSystem, InteractionSystem
from .event import Event, EventGenerator, RumorSystem, Interaction
from .enums import InteractionType, EventType

class TavernSimulator:
    """Main simulator class that orchestrates all tavern activities"""
    
    def __init__(self):
        # Core systems
        self.dice_system = DiceSystem()
        self.interaction_system = InteractionSystem(self.dice_system)
        self.character_generator = CharacterGenerator()
        self.tavern_generator = TavernGenerator()
        self.event_generator = EventGenerator()
        self.rumor_system = RumorSystem()
        
        # Current state
        self.current_tavern: Optional[Tavern] = None
        self.available_characters: Dict[str, Character] = {}
        self.session_log: List[str] = []
        self.interaction_history: List[Interaction] = []
        self.event_history: List[Event] = []
        
        # Session tracking
        self.session_start_time = datetime.now()
        self.turn_counter = 0
        self.auto_events_enabled = True
        
        # Initialize with all characters available
        self.reset_characters()
    
    def reset_characters(self):
        """Reset all characters to their default state"""
        all_chars = self.character_generator.get_all_characters()
        self.available_characters = {char.name: char for char in all_chars}
    
    def generate_new_tavern(self, name: str = None) -> Tavern:
        """Generate a new tavern and populate it with random characters"""
        self.current_tavern = self.tavern_generator.generate_tavern(name)
        
        # Add random characters to the tavern (5-12 characters)
        num_characters = random.randint(5, min(12, len(self.available_characters)))
        selected_chars = random.sample(list(self.available_characters.values()), num_characters)
        
        for char in selected_chars:
            self.current_tavern.add_character(char)
        
        self.log_event(f"Generated new tavern: {self.current_tavern.name}")
        self.log_event(f"Characters present: {', '.join([c.name for c in selected_chars])}")
        
        return self.current_tavern
    
    def add_character_to_tavern(self, character_name: str) -> bool:
        """Add a specific character to the current tavern"""
        if not self.current_tavern:
            return False
        
        character = self.available_characters.get(character_name)
        if not character:
            return False
        
        if character in self.current_tavern.characters:
            return False  # Already in tavern
        
        success = self.current_tavern.add_character(character)
        if success:
            self.log_event(f"{character.name} enters the tavern")
        
        return success
    
    def remove_character_from_tavern(self, character_name: str) -> bool:
        """Remove a character from the current tavern"""
        if not self.current_tavern:
            return False
        
        character = self.current_tavern.get_character_by_name(character_name)
        if not character:
            return False
        
        success = self.current_tavern.remove_character(character)
        if success:
            self.log_event(f"{character.name} leaves the tavern")
        
        return success
    
    def perform_interaction(self, initiator_name: str, target_name: str, interaction_type: InteractionType) -> Optional[Interaction]:
        """Perform an interaction between two characters"""
        if not self.current_tavern:
            return None
        
        initiator = self.current_tavern.get_character_by_name(initiator_name)
        target = self.current_tavern.get_character_by_name(target_name)
        
        if not initiator or not target:
            return None
        
        if not initiator.can_interact_with(target):
            self.log_event(f"{initiator.name} refuses to interact with {target.name}")
            return None
        
        # Perform the interaction
        interaction = self.interaction_system.perform_interaction(initiator, target, interaction_type)
        
        # Log the interaction
        self.interaction_history.append(interaction)
        self.log_event(f"Interaction: {interaction.outcome_description}")
        
        # Update tavern tension based on interaction
        if interaction.success:
            if interaction_type in [InteractionType.CONVERSATION, InteractionType.DRINKING]:
                self.current_tavern.decrease_tension(2)
            elif interaction_type == InteractionType.INTIMIDATION:
                self.current_tavern.increase_tension(5)
        else:
            if interaction_type in [InteractionType.INTIMIDATION, InteractionType.BRAWL]:
                self.current_tavern.increase_tension(8)
            else:
                self.current_tavern.increase_tension(3)
        
        # Chance for rumor spreading
        if random.random() < 0.3:
            rumor = self.rumor_system.spread_rumor(initiator, target)
            if rumor:
                self.log_event(f"Rumor spreads: {rumor}")
        
        return interaction
    
    def trigger_random_event(self) -> Optional[Event]:
        """Trigger a random event in the tavern"""
        if not self.current_tavern:
            return None
        
        event = self.event_generator.generate_random_event(
            self.current_tavern.characters,
            self.current_tavern.tension_level
        )
        
        if event:
            # Apply event effects
            char_dict = {char.name: char for char in self.current_tavern.characters}
            event.apply_effects(self.current_tavern, char_dict)
            
            # Log the event
            self.event_history.append(event)
            self.log_event(f"Event: {event.title} - {event.description}")
            
            # Add to current events
            self.current_tavern.current_events.append(event.title)
        
        return event
    
    def generate_rumor(self) -> Optional[str]:
        """Generate a new rumor"""
        if not self.current_tavern:
            return None
        
        rumor = self.event_generator.generate_rumor(self.current_tavern.characters)
        if rumor:
            self.rumor_system.add_rumor(rumor)
            self.log_event(f"New rumor: {rumor}")
        
        return rumor
    
    def advance_turn(self):
        """Advance the simulation by one turn"""
        self.turn_counter += 1
        
        if not self.current_tavern:
            return
        
        # Characters sober up slightly
        for character in self.current_tavern.characters:
            character.sober_up()
        
        # Decrease tension naturally over time
        self.current_tavern.decrease_tension(1)
        
        # Random events
        if self.auto_events_enabled and random.random() < 0.3:
            self.trigger_random_event()
        
        # Random rumor generation
        if random.random() < 0.2:
            self.generate_rumor()
        
        # Random character interactions
        if len(self.current_tavern.characters) >= 2 and random.random() < 0.4:
            self.trigger_random_interaction()
        
        self.log_event(f"Turn {self.turn_counter} completed")
    
    def trigger_random_interaction(self):
        """Trigger a random interaction between characters"""
        if len(self.current_tavern.characters) < 2:
            return
        
        # Select two random characters
        chars = random.sample(self.current_tavern.characters, 2)
        initiator, target = chars[0], chars[1]
        
        # Select random interaction type (weighted towards peaceful interactions)
        interaction_weights = {
            InteractionType.CONVERSATION: 30,
            InteractionType.DRINKING: 20,
            InteractionType.GAMBLING: 15,
            InteractionType.STORYTELLING: 10,
            InteractionType.TRADE: 10,
            InteractionType.INFORMATION: 8,
            InteractionType.PERSUASION: 5,
            InteractionType.INTIMIDATION: 2
        }
        
        total_weight = sum(interaction_weights.values())
        rand_val = random.randint(1, total_weight)
        current_weight = 0
        
        selected_interaction = InteractionType.CONVERSATION
        for interaction_type, weight in interaction_weights.items():
            current_weight += weight
            if rand_val <= current_weight:
                selected_interaction = interaction_type
                break
        
        self.perform_interaction(initiator.name, target.name, selected_interaction)
    
    def get_character_relationships(self) -> Dict[str, Dict[str, int]]:
        """Get all character relationships as a dictionary"""
        relationships = {}
        
        for char in self.current_tavern.characters if self.current_tavern else []:
            relationships[char.name] = {}
            for other_char in self.current_tavern.characters:
                if other_char != char:
                    rel = char.get_relationship(other_char.name)
                    relationships[char.name][other_char.name] = int(rel)
        
        return relationships
    
    def get_tavern_status(self) -> Dict:
        """Get current tavern status"""
        if not self.current_tavern:
            return {}
        
        return {
            'name': self.current_tavern.name,
            'description': self.current_tavern.description,
            'atmosphere': self.current_tavern.atmosphere.value,
            'atmosphere_description': self.current_tavern.atmosphere_description,
            'tension_level': self.current_tavern.tension_level,
            'occupancy': f"{self.current_tavern.current_occupancy}/{self.current_tavern.capacity}",
            'reputation': self.current_tavern.reputation,
            'current_events': self.current_tavern.current_events,
            'characters': [char.name for char in self.current_tavern.characters]
        }
    
    def log_event(self, message: str):
        """Log an event with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}"
        self.session_log.append(log_entry)
    
    def get_session_log(self) -> List[str]:
        """Get the current session log"""
        return self.session_log.copy()
    
    def export_session_log(self, filename: str = None) -> str:
        """Export session log to file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tavern_session_{timestamp}.txt"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"Warhammer Fantasy Tavern Simulator - Session Log\n")
            f.write(f"Session started: {self.session_start_time}\n")
            f.write(f"Total turns: {self.turn_counter}\n")
            f.write("=" * 50 + "\n\n")
            
            for entry in self.session_log:
                f.write(entry + "\n")
            
            f.write("\n" + "=" * 50 + "\n")
            f.write("Character Relationships:\n")
            relationships = self.get_character_relationships()
            for char, rels in relationships.items():
                f.write(f"\n{char}:\n")
                for other, rel_value in rels.items():
                    f.write(f"  -> {other}: {rel_value}\n")
        
        return filename
    
    def save_session(self, filename: str = None) -> str:
        """Save the current session state"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"tavern_session_{timestamp}.pkl"
        
        session_data = {
            'tavern': self.current_tavern.to_dict() if self.current_tavern else None,
            'characters': {name: char.to_dict() for name, char in self.available_characters.items()},
            'session_log': self.session_log,
            'interaction_history': [
                {
                    'initiator': i.initiator,
                    'target': i.target,
                    'type': i.interaction_type.value,
                    'success': i.success,
                    'description': i.outcome_description,
                    'timestamp': i.timestamp.isoformat()
                } for i in self.interaction_history
            ],
            'turn_counter': self.turn_counter,
            'session_start_time': self.session_start_time.isoformat()
        }
        
        with open(filename, 'wb') as f:
            pickle.dump(session_data, f)
        
        return filename
    
    def load_session(self, filename: str) -> bool:
        """Load a saved session state"""
        try:
            with open(filename, 'rb') as f:
                session_data = pickle.load(f)
            
            # Restore tavern
            if session_data['tavern']:
                self.current_tavern = Tavern.from_dict(session_data['tavern'])
            
            # Restore characters
            self.available_characters = {
                name: Character.from_dict(char_data) 
                for name, char_data in session_data['characters'].items()
            }
            
            # Restore session data
            self.session_log = session_data['session_log']
            self.turn_counter = session_data['turn_counter']
            self.session_start_time = datetime.fromisoformat(session_data['session_start_time'])
            
            return True
        except Exception as e:
            print(f"Error loading session: {e}")
            return False
