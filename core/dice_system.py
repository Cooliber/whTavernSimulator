"""
Dice rolling and interaction system for the Warhammer Fantasy Tavern Simulator
"""

import random
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass
from .enums import Skill, InteractionType, RelationshipType
from .character import Character
from .event import Interaction

@dataclass
class DiceResult:
    """Result of a dice roll"""
    roll: int
    modifier: int
    total: int
    difficulty: int
    success: bool
    critical_success: bool = False
    critical_failure: bool = False
    
    def __str__(self) -> str:
        crit_text = " (Critical!)" if self.critical_success else " (Fumble!)" if self.critical_failure else ""
        return f"Roll: {self.roll} + {self.modifier} = {self.total} vs {self.difficulty} {'SUCCESS' if self.success else 'FAILURE'}{crit_text}"

class DiceSystem:
    """Handles all dice rolling and skill checks in the simulator"""
    
    def __init__(self):
        self.dice_sides = 20  # Using d20 system
        self.critical_success_threshold = 20
        self.critical_failure_threshold = 1
    
    def roll_dice(self, sides: int = None) -> int:
        """Roll a dice with specified number of sides"""
        if sides is None:
            sides = self.dice_sides
        return random.randint(1, sides)
    
    def roll_multiple_dice(self, count: int, sides: int = None) -> List[int]:
        """Roll multiple dice"""
        if sides is None:
            sides = self.dice_sides
        return [self.roll_dice(sides) for _ in range(count)]
    
    def skill_check(self, character: Character, skill: Skill, difficulty: int = 10, modifier: int = 0) -> DiceResult:
        """Perform a skill check for a character"""
        roll = self.roll_dice()
        skill_value = character.get_skill_value(skill)
        total_modifier = skill_value + modifier
        total = roll + total_modifier
        
        success = total >= difficulty
        critical_success = roll == self.critical_success_threshold
        critical_failure = roll == self.critical_failure_threshold
        
        # Critical success always succeeds, critical failure always fails
        if critical_success:
            success = True
        elif critical_failure:
            success = False
        
        return DiceResult(
            roll=roll,
            modifier=total_modifier,
            total=total,
            difficulty=difficulty,
            success=success,
            critical_success=critical_success,
            critical_failure=critical_failure
        )
    
    def opposed_check(self, char1: Character, skill1: Skill, char2: Character, skill2: Skill) -> Tuple[DiceResult, DiceResult, bool]:
        """Perform an opposed skill check between two characters"""
        result1 = self.skill_check(char1, skill1, difficulty=0)  # No fixed difficulty for opposed checks
        result2 = self.skill_check(char2, skill2, difficulty=0)
        
        # Determine winner
        char1_wins = result1.total > result2.total
        
        # Handle critical results
        if result1.critical_success and not result2.critical_success:
            char1_wins = True
        elif result2.critical_success and not result1.critical_success:
            char1_wins = False
        elif result1.critical_failure and not result2.critical_failure:
            char1_wins = False
        elif result2.critical_failure and not result1.critical_failure:
            char1_wins = True
        
        return result1, result2, char1_wins

class InteractionSystem:
    """Handles character interactions and their outcomes"""
    
    def __init__(self, dice_system: DiceSystem):
        self.dice_system = dice_system
        self.interaction_difficulties = self._initialize_difficulties()
        self.interaction_skills = self._initialize_interaction_skills()
    
    def _initialize_difficulties(self) -> Dict[InteractionType, int]:
        """Initialize base difficulties for different interaction types"""
        return {
            InteractionType.CONVERSATION: 10,
            InteractionType.TRADE: 12,
            InteractionType.GAMBLING: 15,
            InteractionType.INFORMATION: 14,
            InteractionType.INTIMIDATION: 13,
            InteractionType.PERSUASION: 15,
            InteractionType.BRAWL: 12,
            InteractionType.DRINKING: 10,
            InteractionType.STORYTELLING: 11
        }
    
    def _initialize_interaction_skills(self) -> Dict[InteractionType, Skill]:
        """Initialize which skills are used for different interactions"""
        return {
            InteractionType.CONVERSATION: Skill.DIPLOMACY,
            InteractionType.TRADE: Skill.TRADE,
            InteractionType.GAMBLING: Skill.GAMBLING,
            InteractionType.INFORMATION: Skill.PERCEPTION,
            InteractionType.INTIMIDATION: Skill.INTIMIDATION,
            InteractionType.PERSUASION: Skill.DIPLOMACY,
            InteractionType.BRAWL: Skill.COMBAT,
            InteractionType.DRINKING: Skill.SURVIVAL,
            InteractionType.STORYTELLING: Skill.PERFORMANCE
        }
    
    def calculate_interaction_modifier(self, initiator: Character, target: Character, interaction_type: InteractionType) -> int:
        """Calculate modifier for interaction based on relationship and other factors"""
        base_modifier = 0
        
        # Relationship modifier
        relationship = initiator.get_relationship(target.name)
        base_modifier += int(relationship) * 2
        
        # Faction compatibility
        faction_modifier = self.get_faction_interaction_modifier(initiator.faction, target.faction)
        base_modifier += faction_modifier
        
        # Drunk penalty
        if initiator.is_drunk():
            base_modifier -= 3
        
        # Mood modifiers
        mood_modifiers = {
            "happy": 2,
            "angry": -2,
            "drunk": -2,
            "suspicious": -3,
            "friendly": 3,
            "hostile": -5
        }
        base_modifier += mood_modifiers.get(initiator.current_mood, 0)
        
        # Interaction-specific modifiers
        if interaction_type == InteractionType.INTIMIDATION:
            # Size/strength difference (simplified)
            if initiator.character_class.value in ["Warrior", "Soldier", "Norse"]:
                base_modifier += 2
        elif interaction_type == InteractionType.TRADE:
            # Merchant bonus
            if initiator.character_class.value == "Merchant":
                base_modifier += 3
        
        return base_modifier
    
    def get_faction_interaction_modifier(self, faction1, faction2) -> int:
        """Get interaction modifier based on faction relationships"""
        # Simplified faction relationships
        faction_relations = {
            ("Empire", "Dwarf"): 2,
            ("Empire", "High Elf"): 1,
            ("Empire", "Bretonnian"): 1,
            ("Dwarf", "High Elf"): -1,
            ("High Elf", "Wood Elf"): -2,
            ("Empire", "Kislev"): 2,
            ("Norse", "Empire"): -3,
            ("Norse", "Dwarf"): -2,
            ("Cultist", "*"): -5,  # Cultists are generally distrusted
            ("Witch Hunter", "Cultist"): -10
        }
        
        # Check direct relationship
        key1 = (faction1.value, faction2.value)
        key2 = (faction2.value, faction1.value)
        
        if key1 in faction_relations:
            return faction_relations[key1]
        elif key2 in faction_relations:
            return faction_relations[key2]
        
        # Check wildcard relationships
        for (f1, f2), modifier in faction_relations.items():
            if f2 == "*" and f1 == faction1.value:
                return modifier
            elif f1 == "*" and f2 == faction1.value:
                return modifier
        
        return 0  # Neutral by default
    
    def perform_interaction(self, initiator: Character, target: Character, interaction_type: InteractionType) -> Interaction:
        """Perform an interaction between two characters"""
        # Get the skill used for this interaction
        skill_used = self.interaction_skills.get(interaction_type, Skill.DIPLOMACY)
        
        # Calculate modifiers
        modifier = self.calculate_interaction_modifier(initiator, target, interaction_type)
        
        # Get base difficulty
        base_difficulty = self.interaction_difficulties.get(interaction_type, 12)
        
        # Adjust difficulty based on target's relevant defensive skill
        defensive_skills = {
            InteractionType.INTIMIDATION: Skill.INTIMIDATION,
            InteractionType.PERSUASION: Skill.DIPLOMACY,
            InteractionType.TRADE: Skill.TRADE
        }
        
        defensive_skill = defensive_skills.get(interaction_type)
        if defensive_skill:
            target_defense = target.get_skill_value(defensive_skill)
            base_difficulty += (target_defense - 10) // 2  # Adjust difficulty based on target's skill
        
        # Perform the skill check
        result = self.dice_system.skill_check(initiator, skill_used, base_difficulty, modifier)
        
        # Generate outcome description
        outcome_description = self.generate_outcome_description(initiator, target, interaction_type, result)
        
        # Calculate relationship change
        relationship_change = self.calculate_relationship_change(interaction_type, result)
        
        # Apply relationship change
        if relationship_change != 0:
            initiator.modify_relationship(target.name, relationship_change)
            target.modify_relationship(initiator.name, relationship_change)
        
        # Create interaction record
        interaction = Interaction(
            initiator=initiator.name,
            target=target.name,
            interaction_type=interaction_type,
            skill_used=skill_used.value,
            dice_roll=result.roll,
            modifier=result.modifier,
            success=result.success,
            outcome_description=outcome_description,
            relationship_change=relationship_change
        )
        
        return interaction
    
    def calculate_relationship_change(self, interaction_type: InteractionType, result: DiceResult) -> int:
        """Calculate how much the relationship should change based on interaction outcome"""
        base_changes = {
            InteractionType.CONVERSATION: (1, -1),  # (success, failure)
            InteractionType.TRADE: (2, -1),
            InteractionType.GAMBLING: (1, -2),
            InteractionType.INFORMATION: (1, 0),
            InteractionType.INTIMIDATION: (-1, -2),
            InteractionType.PERSUASION: (2, -1),
            InteractionType.BRAWL: (-2, -1),
            InteractionType.DRINKING: (2, 0),
            InteractionType.STORYTELLING: (1, 0)
        }
        
        success_change, failure_change = base_changes.get(interaction_type, (0, 0))
        
        if result.success:
            change = success_change
            if result.critical_success:
                change *= 2
        else:
            change = failure_change
            if result.critical_failure:
                change *= 2
        
        return change
    
    def generate_outcome_description(self, initiator: Character, target: Character, interaction_type: InteractionType, result: DiceResult) -> str:
        """Generate a description of the interaction outcome"""
        success_templates = {
            InteractionType.CONVERSATION: [
                f"{initiator.name} engages {target.name} in pleasant conversation.",
                f"{initiator.name} and {target.name} share an enjoyable chat.",
                f"{initiator.name} finds common ground with {target.name}."
            ],
            InteractionType.TRADE: [
                f"{initiator.name} successfully negotiates a deal with {target.name}.",
                f"{initiator.name} and {target.name} reach a mutually beneficial agreement.",
                f"{initiator.name} convinces {target.name} to make a trade."
            ],
            InteractionType.INTIMIDATION: [
                f"{initiator.name} successfully intimidates {target.name}.",
                f"{target.name} backs down from {initiator.name}'s threatening presence.",
                f"{initiator.name}'s menacing demeanor cows {target.name}."
            ],
            InteractionType.GAMBLING: [
                f"{initiator.name} wins against {target.name} in a game of chance.",
                f"{initiator.name} outplays {target.name} at the gambling table.",
                f"{initiator.name} takes {target.name}'s coins in a lucky game."
            ]
        }
        
        failure_templates = {
            InteractionType.CONVERSATION: [
                f"{initiator.name} fails to connect with {target.name}.",
                f"The conversation between {initiator.name} and {target.name} turns awkward.",
                f"{initiator.name} says something that offends {target.name}."
            ],
            InteractionType.TRADE: [
                f"{initiator.name} fails to convince {target.name} to make a deal.",
                f"{target.name} rejects {initiator.name}'s trade proposal.",
                f"Negotiations between {initiator.name} and {target.name} break down."
            ],
            InteractionType.INTIMIDATION: [
                f"{target.name} stands firm against {initiator.name}'s threats.",
                f"{initiator.name} fails to intimidate {target.name}.",
                f"{target.name} laughs off {initiator.name}'s attempt at intimidation."
            ],
            InteractionType.GAMBLING: [
                f"{initiator.name} loses to {target.name} in a game of chance.",
                f"{target.name} outplays {initiator.name} at the gambling table.",
                f"{initiator.name} loses coins to {target.name} in an unlucky game."
            ]
        }
        
        templates = success_templates if result.success else failure_templates
        interaction_templates = templates.get(interaction_type, [f"{initiator.name} interacts with {target.name}."])
        
        description = random.choice(interaction_templates)
        
        if result.critical_success:
            description += " The outcome exceeds all expectations!"
        elif result.critical_failure:
            description += " Things go terribly wrong!"
        
        return description
