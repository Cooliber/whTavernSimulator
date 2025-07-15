"""
Wiedźma (Mystic Oracle) Agent
Mystical, prophetic, sees hidden connections
Uses Grok for complex narrative generation and mystical insights
"""

import random
from typing import Dict, List, Optional, Any
from datetime import datetime

from .base_agent import BaseAgent, AgentAction

class WiedzmaAgent(BaseAgent):
    """Mystic Oracle - divines future and interprets omens"""
    
    def __init__(self):
        super().__init__(
            name="Wiedźma",
            role="Mystic Oracle",
            personality="Mystical, prophetic, sees hidden connections"
        )
        
        # Mystic-specific attributes
        self.mystical_knowledge = {
            "omens_observed": [],
            "prophecies_made": [],
            "fate_threads": {},
            "spiritual_insights": []
        }
        
        self.divination_power = 0.7  # Ability to see hidden patterns
        self.prophecy_accuracy = 0.6  # Track prediction success
        
        # Mystic priorities
        self.priorities = [
            "divine_future",
            "interpret_omens", 
            "guide_fate",
            "reveal_hidden_truths",
            "protect_from_chaos"
        ]
    
    def perceive(self, tavern_state: Dict[str, Any]) -> List[str]:
        """Perceive mystical patterns and hidden connections"""
        perceptions = []
        
        # Read omens in tavern atmosphere
        tension = tavern_state.get("tension_level", 0)
        reputation = tavern_state.get("reputation", 50)
        
        # Mystical interpretation of tension patterns
        if tension > 75:
            perceptions.append("OMEN: The winds of chaos stir - violence approaches like storm clouds")
            self.update_emotion("alertness", 0.4)
        elif tension < 25:
            perceptions.append("VISION: Peaceful energies flow - harmony blesses this place")
            self.update_emotion("satisfaction", 0.3)
        
        # Divine character fates
        characters = tavern_state.get("characters", [])
        for char in characters:
            faction = char.get("faction", "")
            drunk_level = char.get("drunk_level", 0)
            
            if faction == "Cultist":
                perceptions.append(f"DARK VISION: {char['name']} carries taint of chaos - corruption spreads")
                self.update_emotion("suspicion", 0.5)
            elif faction == "Witch Hunter":
                perceptions.append(f"DIVINE SIGHT: {char['name']} burns with righteous fire - purification comes")
            elif drunk_level > 8:
                perceptions.append(f"PROPHECY: {char['name']} drowns sorrows - tragedy haunts their past")
        
        # Read mystical patterns in recent events
        recent_events = tavern_state.get("recent_events", [])
        for event in recent_events[-2:]:
            if "brawl" in event.lower():
                perceptions.append("PORTENT: Violence echoes through the ethereal plane - more conflict follows")
            elif "rumor" in event.lower():
                perceptions.append("WHISPER: The web of fate trembles with hidden knowledge")
        
        # Sense supernatural influences
        if len(characters) > 15:
            perceptions.append("MYSTICAL CONVERGENCE: Many souls gather - destiny weaves complex patterns")
        
        return perceptions
    
    def decide(self, perceptions: List[str]) -> Optional[AgentAction]:
        """Make mystical decisions based on divine insights"""
        if not self.can_act():
            return None
        
        self.add_reasoning_step("Consulting the ethereal winds...")
        
        # Assess mystical urgency
        mystical_urgency = self._assess_mystical_urgency(perceptions)
        
        if mystical_urgency > 8:
            self.add_reasoning_step("Urgent mystical intervention required")
            return self._create_prophecy_action(perceptions)
        elif mystical_urgency > 5:
            self.add_reasoning_step("Mystical guidance needed")
            return self._create_divination_action(perceptions)
        elif any("DARK" in p or "chaos" in p for p in perceptions):
            self.add_reasoning_step("Chaos detected - protective measures needed")
            return self._create_protection_action(perceptions)
        else:
            return self._create_observation_action()
    
    def _assess_mystical_urgency(self, perceptions: List[str]) -> int:
        """Assess urgency of mystical intervention"""
        urgency = 0
        
        for perception in perceptions:
            if "DARK VISION" in perception or "chaos" in perception:
                urgency += 9
            elif "OMEN" in perception and "violence" in perception:
                urgency += 7
            elif "PROPHECY" in perception:
                urgency += 5
            elif "MYSTICAL CONVERGENCE" in perception:
                urgency += 6
        
        return urgency
    
    def _create_prophecy_action(self, perceptions: List[str]) -> AgentAction:
        """Create prophetic action to guide fate"""
        prophecy_types = [
            "warn_of_danger",
            "reveal_hidden_truth",
            "guide_decision",
            "predict_outcome",
            "unveil_deception"
        ]
        
        prophecy_type = random.choice(prophecy_types)
        
        reasoning = self.call_llm(
            f"The ethereal winds show urgent visions. I must deliver {prophecy_type} to guide mortals.",
            "You are a mystical oracle who sees beyond the veil. Your prophecies shape destiny.",
            task_type="narrative_generation"
        )
        
        return AgentAction(
            action_type="deliver_prophecy",
            parameters={"prophecy_type": prophecy_type},
            reasoning=reasoning,
            confidence=0.8
        )
    
    def _create_divination_action(self, perceptions: List[str]) -> AgentAction:
        """Create divination action to read omens"""
        divination_methods = [
            "read_tea_leaves",
            "cast_rune_stones",
            "scry_crystal_ball",
            "interpret_flame_patterns",
            "commune_with_spirits"
        ]
        
        method = random.choice(divination_methods)
        
        reasoning = f"The mystical currents call for {method} to reveal hidden truths"
        
        return AgentAction(
            action_type="perform_divination",
            parameters={"method": method},
            reasoning=reasoning,
            confidence=0.7
        )
    
    def _create_protection_action(self, perceptions: List[str]) -> AgentAction:
        """Create protective mystical action"""
        protection_methods = [
            "cast_ward_against_chaos",
            "bless_sacred_space",
            "purify_negative_energy",
            "strengthen_spiritual_barriers",
            "invoke_divine_protection"
        ]
        
        method = random.choice(protection_methods)
        
        return AgentAction(
            action_type="mystical_protection",
            parameters={"method": method},
            reasoning=f"Chaos stirs - {method} needed to protect the innocent",
            confidence=0.6
        )
    
    def _create_observation_action(self) -> AgentAction:
        """Create mystical observation action"""
        return AgentAction(
            action_type="mystical_observation",
            parameters={},
            reasoning="Watching the ethereal currents for signs and portents",
            confidence=0.5
        )
    
    def act(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute mystical actions"""
        self.last_action_time = datetime.now()
        results = {"success": False, "message": "", "effects": {}}
        
        if action.action_type == "deliver_prophecy":
            results = self._execute_prophecy(action, tavern_state)
        elif action.action_type == "perform_divination":
            results = self._execute_divination(action, tavern_state)
        elif action.action_type == "mystical_protection":
            results = self._execute_protection(action, tavern_state)
        elif action.action_type == "mystical_observation":
            results = self._execute_mystical_observation(action, tavern_state)
        else:
            results = {
                "success": True,
                "message": f"{self.name} gazes into the ethereal realm",
                "effects": {}
            }
        
        # Update mystical memory
        self.update_memory(f"Mystical action: {results['message']}")
        
        return results
    
    def _execute_prophecy(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute prophetic revelation"""
        prophecy_type = action.parameters.get("prophecy_type", "predict_outcome")
        
        # Generate mystical prophecy
        prophecy = self._generate_prophecy(prophecy_type, tavern_state)
        
        self.mystical_knowledge["prophecies_made"].append({
            "prophecy": prophecy,
            "type": prophecy_type,
            "timestamp": datetime.now().isoformat()
        })
        
        # Prophecies can influence tavern atmosphere
        tension_change = random.randint(-15, 5)  # Usually calming
        reputation_change = random.randint(1, 8)  # Mystical guidance valued
        
        return {
            "success": True,
            "message": f"{self.name} delivers prophecy: {prophecy}",
            "effects": {
                "tension_change": tension_change,
                "reputation_change": reputation_change,
                "mystical_influence": True
            }
        }
    
    def _generate_prophecy(self, prophecy_type: str, tavern_state: Dict[str, Any]) -> str:
        """Generate contextual prophecy"""
        prophecies = {
            "warn_of_danger": [
                "Beware the stranger who speaks in riddles - deception walks among you",
                "When the moon turns red, violence shall spill like wine upon stone",
                "The shadow that follows has no master - trust not the silent watcher"
            ],
            "reveal_hidden_truth": [
                "What appears as friendship masks bitter rivalry beneath",
                "The loudest voice carries the deepest secrets",
                "Gold changes hands, but loyalty has already been sold"
            ],
            "guide_decision": [
                "Choose the path of wisdom over the road of haste",
                "Sometimes retreat is the greatest victory",
                "Listen to the whispers of your heart, not the shouts of your pride"
            ],
            "predict_outcome": [
                "This night shall end in either celebration or sorrow",
                "Three paths diverge - choose wisely, for fate watches",
                "The seeds planted today will bloom in unexpected gardens"
            ]
        }
        
        return random.choice(prophecies.get(prophecy_type, ["The future remains clouded in mystery"]))

    def _execute_divination(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute divination ritual"""
        method = action.parameters.get("method", "scry_crystal_ball")

        # Generate mystical insight
        insights = [
            "The threads of fate converge on this tavern tonight",
            "A great change approaches from the eastern roads",
            "Someone here carries a burden heavier than gold",
            "The past reaches out to claim what was lost",
            "Destiny has marked three souls for transformation"
        ]

        insight = random.choice(insights)

        self.mystical_knowledge["spiritual_insights"].append({
            "insight": insight,
            "method": method,
            "timestamp": datetime.now().isoformat()
        })

        return {
            "success": True,
            "message": f"{self.name} performs {method}: {insight}",
            "effects": {
                "mystical_knowledge": insight,
                "divination_power": 0.1
            }
        }

    def _execute_protection(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute mystical protection"""
        method = action.parameters.get("method", "cast_ward_against_chaos")

        protection_strength = random.randint(10, 25)

        protection_messages = {
            "cast_ward_against_chaos": f"{self.name} weaves protective wards against chaotic influences",
            "bless_sacred_space": f"{self.name} sanctifies the tavern with ancient blessings",
            "purify_negative_energy": f"{self.name} cleanses the air of malevolent spirits",
            "strengthen_spiritual_barriers": f"{self.name} reinforces the veil between worlds",
            "invoke_divine_protection": f"{self.name} calls upon divine forces for protection"
        }

        return {
            "success": True,
            "message": protection_messages.get(method, f"{self.name} casts mystical protection"),
            "effects": {
                "chaos_resistance": protection_strength,
                "spiritual_protection": True,
                "tension_change": -random.randint(5, 15)
            }
        }

    def _execute_mystical_observation(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute mystical observation"""
        observations = [
            "Sensed disturbance in the ethereal currents",
            "Detected traces of ancient magic lingering in the air",
            "Observed spiritual auras revealing hidden emotions",
            "Felt the presence of otherworldly watchers",
            "Perceived echoes of past events imprinted on this place"
        ]

        observation = random.choice(observations)
        self.mystical_knowledge["omens_observed"].append({
            "omen": observation,
            "timestamp": datetime.now().isoformat()
        })

        return {
            "success": True,
            "message": f"{self.name} observes mystical signs: {observation}",
            "effects": {
                "mystical_awareness": 5
            }
        }

    def get_mystical_summary(self) -> Dict[str, Any]:
        """Get summary of mystical activities"""
        return {
            "prophecies_made": len(self.mystical_knowledge["prophecies_made"]),
            "omens_observed": len(self.mystical_knowledge["omens_observed"]),
            "divination_power": self.divination_power,
            "prophecy_accuracy": self.prophecy_accuracy,
            "recent_insights": self.mystical_knowledge["spiritual_insights"][-3:] if self.mystical_knowledge["spiritual_insights"] else []
        }
