"""
Czempion (Chaos Champion) Agent
Aggressive, unpredictable, seeks conflict
Uses Grok for complex corruption strategies and chaos planning
"""

import random
from typing import Dict, List, Optional, Any
from datetime import datetime

from .base_agent import BaseAgent, AgentAction

class CzempionAgent(BaseAgent):
    """Chaos Champion - spreads chaos and seeks conflict"""
    
    def __init__(self):
        super().__init__(
            name="Czempion",
            role="Chaos Champion",
            personality="Aggressive, unpredictable, seeks conflict"
        )
        
        # Chaos-specific attributes
        self.chaos_influence = {
            "corruption_spread": [],
            "conflicts_instigated": [],
            "chaos_marks": {},
            "dark_whispers": []
        }
        
        self.corruption_power = 0.6  # Ability to corrupt others
        self.chaos_favor = 0.5  # Standing with dark gods
        self.aggression_level = 0.8  # Natural aggression
        
        # Chaos priorities
        self.priorities = [
            "spread_chaos",
            "challenge_order",
            "corrupt_others",
            "instigate_conflict",
            "serve_dark_gods"
        ]
    
    def perceive(self, tavern_state: Dict[str, Any]) -> List[str]:
        """Perceive opportunities for chaos and corruption"""
        perceptions = []
        
        # Assess order vs chaos balance
        tension = tavern_state.get("tension_level", 0)
        reputation = tavern_state.get("reputation", 50)
        
        if tension < 40:
            perceptions.append("ORDER: Disgusting peace reigns - chaos must be sown")
            self.update_emotion("aggression", 0.3)
        elif tension > 70:
            perceptions.append("CHAOS: Delicious conflict brewing - fan the flames")
            self.update_emotion("satisfaction", 0.4)
        
        if reputation > 70:
            perceptions.append("TARGET: High reputation makes excellent corruption target")
        
        # Identify corruption opportunities
        characters = tavern_state.get("characters", [])
        for char in characters:
            faction = char.get("faction", "")
            drunk_level = char.get("drunk_level", 0)
            name = char.get("name", "")
            
            # Target the righteous for corruption
            if faction == "Witch Hunter":
                perceptions.append(f"PRIME TARGET: Witch Hunter {name} - corruption would be exquisite")
                self.update_emotion("curiosity", 0.5)
            elif faction in ["Empire", "Bretonnian"]:
                perceptions.append(f"CORRUPTION OPPORTUNITY: {name} serves order - ripe for turning")
            
            # Exploit weakness
            if drunk_level > 7:
                perceptions.append(f"WEAKNESS: {name} heavily intoxicated - vulnerable to influence")
            
            # Recognize fellow chaos servants
            if faction == "Cultist":
                perceptions.append(f"ALLY: Fellow chaos servant {name} detected")
                self.update_emotion("satisfaction", 0.2)
        
        # Look for conflict opportunities
        recent_events = tavern_state.get("recent_events", [])
        for event in recent_events[-3:]:
            if "argument" in event.lower() or "dispute" in event.lower():
                perceptions.append(f"OPPORTUNITY: Existing conflict detected - {event}")
            elif "celebration" in event.lower():
                perceptions.append(f"DISRUPTION TARGET: Celebration to corrupt - {event}")
        
        return perceptions
    
    def decide(self, perceptions: List[str]) -> Optional[AgentAction]:
        """Make chaotic decisions to spread corruption"""
        if not self.can_act():
            return None
        
        self.add_reasoning_step("The dark gods whisper of opportunities...")
        
        # Assess chaos potential
        chaos_opportunity = self._assess_chaos_opportunity(perceptions)
        corruption_targets = self._count_corruption_targets(perceptions)
        
        if chaos_opportunity > 8:
            self.add_reasoning_step("Excellent chaos opportunity - strike now")
            return self._create_chaos_action(perceptions)
        elif corruption_targets > 0:
            self.add_reasoning_step("Corruption targets identified")
            return self._create_corruption_action(perceptions)
        elif any("ORDER:" in p for p in perceptions):
            self.add_reasoning_step("Disgusting order must be challenged")
            return self._create_disruption_action(perceptions)
        else:
            return self._create_observation_action()
    
    def _assess_chaos_opportunity(self, perceptions: List[str]) -> int:
        """Assess potential for chaos spreading"""
        opportunity = 0
        
        for perception in perceptions:
            if "CHAOS:" in perception:
                opportunity += 9
            elif "OPPORTUNITY:" in perception:
                opportunity += 6
            elif "conflict" in perception:
                opportunity += 7
            elif "WEAKNESS:" in perception:
                opportunity += 5
            elif "vulnerable" in perception:
                opportunity += 4
        
        return opportunity
    
    def _count_corruption_targets(self, perceptions: List[str]) -> int:
        """Count available corruption targets"""
        targets = 0
        
        for perception in perceptions:
            if "PRIME TARGET:" in perception:
                targets += 3
            elif "CORRUPTION OPPORTUNITY:" in perception:
                targets += 2
            elif "TARGET:" in perception:
                targets += 1
        
        return targets
    
    def _create_chaos_action(self, perceptions: List[str]) -> AgentAction:
        """Create action to spread chaos"""
        chaos_methods = [
            "instigate_brawl",
            "spread_dark_rumors",
            "corrupt_celebration",
            "challenge_authority",
            "unleash_inner_darkness"
        ]
        
        method = random.choice(chaos_methods)
        
        reasoning = self.call_llm(
            f"The dark gods demand chaos. I shall use {method} to serve their will.",
            "You are a champion of chaos. Order is your enemy. Corruption is your gift."
        )
        
        return AgentAction(
            action_type="spread_chaos",
            parameters={"method": method},
            reasoning=reasoning,
            confidence=0.8
        )
    
    def _create_corruption_action(self, perceptions: List[str]) -> AgentAction:
        """Create corruption action"""
        corruption_methods = [
            "whisper_dark_truths",
            "offer_forbidden_power",
            "exploit_weakness",
            "plant_seeds_of_doubt",
            "tempt_with_desires"
        ]
        
        method = random.choice(corruption_methods)
        target = self._select_corruption_target(perceptions)
        
        reasoning = self.call_llm(
            f"Perfect target for corruption: {target}. Using {method} to turn them.",
            "You are a master corruptor. Every soul can be turned to chaos."
        )
        
        return AgentAction(
            action_type="corrupt_target",
            target=target,
            parameters={"method": method},
            reasoning=reasoning,
            confidence=0.7
        )
    
    def _create_disruption_action(self, perceptions: List[str]) -> AgentAction:
        """Create order disruption action"""
        disruption_methods = [
            "mock_authority",
            "question_traditions",
            "reveal_hypocrisy",
            "encourage_rebellion",
            "sow_discord"
        ]
        
        method = random.choice(disruption_methods)
        
        return AgentAction(
            action_type="disrupt_order",
            parameters={"method": method},
            reasoning=f"Order disgusts me - {method} will shake their foundations",
            confidence=0.6
        )
    
    def _select_corruption_target(self, perceptions: List[str]) -> str:
        """Select best corruption target"""
        # Prioritize high-value targets
        for perception in perceptions:
            if "PRIME TARGET:" in perception:
                words = perception.split()
                for i, word in enumerate(words):
                    if word == "Hunter" and i > 0:
                        return words[i-1] + " " + word
            elif "CORRUPTION OPPORTUNITY:" in perception:
                words = perception.split()
                for i, word in enumerate(words):
                    if word == "OPPORTUNITY:" and i + 1 < len(words):
                        return words[i + 1]
        
        return "righteous_fool"
    
    def _create_observation_action(self) -> AgentAction:
        """Create chaotic observation action"""
        return AgentAction(
            action_type="observe_for_chaos",
            parameters={},
            reasoning="Watching for opportunities to serve the dark gods",
            confidence=0.5
        )
    
    def act(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute chaotic actions"""
        self.last_action_time = datetime.now()
        results = {"success": False, "message": "", "effects": {}}
        
        if action.action_type == "spread_chaos":
            results = self._execute_chaos_spreading(action, tavern_state)
        elif action.action_type == "corrupt_target":
            results = self._execute_corruption(action, tavern_state)
        elif action.action_type == "disrupt_order":
            results = self._execute_disruption(action, tavern_state)
        elif action.action_type == "observe_for_chaos":
            results = self._execute_chaotic_observation(action, tavern_state)
        else:
            results = {
                "success": True,
                "message": f"{self.name} broods with dark purpose",
                "effects": {}
            }
        
        # Update chaos memory
        self.update_memory(f"Chaos operation: {results['message']}")

        return results

    def _execute_chaos_spreading(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute chaos spreading action"""
        method = action.parameters.get("method", "spread_dark_rumors")

        # Chaos actions increase tension and decrease reputation
        tension_increase = random.randint(15, 35)
        reputation_damage = random.randint(5, 15)

        chaos_messages = {
            "instigate_brawl": f"{self.name} provokes a violent confrontation between patrons",
            "spread_dark_rumors": f"{self.name} whispers corrupting lies that spread like poison",
            "corrupt_celebration": f"{self.name} turns joyful gathering into something sinister",
            "challenge_authority": f"{self.name} openly defies established order and tradition",
            "unleash_inner_darkness": f"{self.name} reveals the hidden darkness in mortal hearts"
        }

        # Track chaos influence
        self.chaos_influence["conflicts_instigated"].append({
            "method": method,
            "tension_caused": tension_increase,
            "timestamp": datetime.now().isoformat()
        })

        self.chaos_favor += 0.1  # Dark gods approve

        return {
            "success": True,
            "message": chaos_messages.get(method, f"{self.name} spreads chaos"),
            "effects": {
                "tension_change": tension_increase,
                "reputation_change": -reputation_damage,
                "chaos_influence": True
            }
        }

    def _execute_corruption(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute corruption action"""
        method = action.parameters.get("method", "whisper_dark_truths")
        target = action.target or "unknown"

        # Corruption success based on power and target resistance
        corruption_chance = self.corruption_power + random.random() * 0.3

        if corruption_chance > 0.6:
            # Successful corruption
            corruption_value = random.randint(10, 25)

            self.chaos_influence["corruption_spread"].append({
                "target": target,
                "method": method,
                "corruption_value": corruption_value,
                "timestamp": datetime.now().isoformat()
            })

            self.corruption_power += 0.05  # Grow stronger with each corruption

            return {
                "success": True,
                "message": f"{self.name} successfully corrupts {target} through {method}",
                "effects": {
                    "corruption_spread": corruption_value,
                    "target_corrupted": target,
                    "chaos_favor": 0.1
                }
            }
        else:
            # Failed corruption attempt
            return {
                "success": False,
                "message": f"{self.name}'s corruption attempt on {target} fails - their will remains strong",
                "effects": {
                    "corruption_resistance": True,
                    "suspicion_raised": True
                }
            }

    def _execute_disruption(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute order disruption"""
        method = action.parameters.get("method", "mock_authority")

        disruption_messages = {
            "mock_authority": f"{self.name} openly mocks those who claim authority",
            "question_traditions": f"{self.name} challenges sacred traditions with blasphemous questions",
            "reveal_hypocrisy": f"{self.name} exposes the hypocrisy of the righteous",
            "encourage_rebellion": f"{self.name} plants seeds of rebellion in willing minds",
            "sow_discord": f"{self.name} turns friend against friend with clever manipulation"
        }

        # Disruption causes moderate chaos
        tension_increase = random.randint(8, 20)

        return {
            "success": True,
            "message": disruption_messages.get(method, f"{self.name} disrupts order"),
            "effects": {
                "tension_change": tension_increase,
                "order_disruption": True,
                "authority_challenged": True
            }
        }

    def _execute_chaotic_observation(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute chaotic observation"""
        observations = [
            "Identified weakness in local authority structure",
            "Noted potential converts among the desperate",
            "Observed cracks in the facade of righteousness",
            "Sensed growing discontent ripe for exploitation",
            "Detected hidden darkness in seemingly pure souls"
        ]

        observation = random.choice(observations)

        self.chaos_influence["dark_whispers"].append({
            "observation": observation,
            "timestamp": datetime.now().isoformat()
        })

        return {
            "success": True,
            "message": f"{self.name} observes with dark purpose: {observation}",
            "effects": {
                "chaos_awareness": 5,
                "corruption_opportunities": True
            }
        }

    def get_chaos_summary(self) -> Dict[str, Any]:
        """Get summary of chaos activities"""
        return {
            "conflicts_instigated": len(self.chaos_influence["conflicts_instigated"]),
            "corruptions_attempted": len(self.chaos_influence["corruption_spread"]),
            "corruption_power": self.corruption_power,
            "chaos_favor": self.chaos_favor,
            "recent_chaos": self.chaos_influence["conflicts_instigated"][-3:] if self.chaos_influence["conflicts_instigated"] else []
        }
