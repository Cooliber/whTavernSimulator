"""
Skrytobójca (Shadow Agent) 
Mysterious, calculating, information broker
Uses Cerebras for fast stealth responses
"""

import random
from typing import Dict, List, Optional, Any
from datetime import datetime

from .base_agent import BaseAgent, AgentAction

class SkrytobojcaAgent(BaseAgent):
    """Shadow Agent - gathers secrets and monitors threats"""
    
    def __init__(self):
        super().__init__(
            name="Skrytobójca",
            role="Shadow Agent",
            personality="Mysterious, calculating, information broker"
        )
        
        # Shadow-specific attributes
        self.secrets_database = {
            "character_secrets": {},
            "overheard_conversations": [],
            "suspicious_activities": [],
            "valuable_information": []
        }
        
        self.stealth_level = 0.8  # How hidden the agent is
        self.information_value = 0.0  # Accumulated value of gathered intel
        
        # Shadow priorities
        self.priorities = [
            "gather_secrets",
            "monitor_threats",
            "trade_information",
            "remain_hidden",
            "execute_contracts"
        ]
    
    def perceive(self, tavern_state: Dict[str, Any]) -> List[str]:
        """Perceive from shadows - notice what others miss"""
        perceptions = []
        
        # Monitor character interactions for secrets
        characters = tavern_state.get("characters", [])
        for char in characters:
            # Look for suspicious behavior
            if char.get("drunk_level", 0) > 7:
                perceptions.append(f"INTEL: {char['name']} heavily intoxicated - vulnerable to information extraction")
            
            if char.get("faction") == "Cultist":
                perceptions.append(f"THREAT: Chaos cultist {char['name']} detected")
                self.update_emotion("alertness", 0.4)
            
            if char.get("faction") == "Witch Hunter":
                perceptions.append(f"DANGER: Witch Hunter {char['name']} present - maintain deep cover")
                self.update_emotion("fear", 0.3)
        
        # Monitor conversations and interactions
        recent_interactions = tavern_state.get("recent_interactions", [])
        for interaction in recent_interactions[-3:]:
            if interaction.get("type") == "information":
                perceptions.append(f"INTEL: Information exchange detected between {interaction.get('initiator')} and {interaction.get('target')}")
            elif interaction.get("type") == "trade":
                perceptions.append(f"TRANSACTION: Trade occurring - potential blackmail material")
        
        # Check for valuable rumors
        rumors = tavern_state.get("current_rumors", [])
        for rumor in rumors:
            if any(keyword in rumor.lower() for keyword in ["secret", "hidden", "conspiracy", "plot"]):
                perceptions.append(f"VALUABLE: High-value rumor detected: {rumor}")
                self.information_value += 10
        
        # Monitor tension for opportunities
        tension = tavern_state.get("tension_level", 0)
        if tension > 60:
            perceptions.append("OPPORTUNITY: High tension creates information gathering opportunities")
        
        return perceptions
    
    def decide(self, perceptions: List[str]) -> Optional[AgentAction]:
        """Make calculated decisions from the shadows"""
        if not self.can_act():
            return None
        
        self.add_reasoning_step("Analyzing shadows for opportunities...")
        
        # Assess threats and opportunities
        threat_level = self._assess_threat_level(perceptions)
        opportunity_value = self._assess_opportunities(perceptions)
        
        if threat_level > 7:
            self.add_reasoning_step("High threat detected - prioritizing stealth")
            return self._create_stealth_action()
        elif opportunity_value > 5:
            self.add_reasoning_step("Valuable opportunity identified")
            return self._create_intelligence_action(perceptions)
        else:
            return self._create_observation_action()
    
    def _assess_threat_level(self, perceptions: List[str]) -> int:
        """Assess current threat level"""
        threat_level = 0
        
        for perception in perceptions:
            if "DANGER" in perception:
                threat_level += 8
            elif "THREAT" in perception:
                threat_level += 5
            elif "Witch Hunter" in perception:
                threat_level += 10
        
        return threat_level
    
    def _assess_opportunities(self, perceptions: List[str]) -> int:
        """Assess information gathering opportunities"""
        opportunity_value = 0
        
        for perception in perceptions:
            if "INTEL" in perception:
                opportunity_value += 3
            elif "VALUABLE" in perception:
                opportunity_value += 5
            elif "OPPORTUNITY" in perception:
                opportunity_value += 4
            elif "vulnerable" in perception:
                opportunity_value += 6
        
        return opportunity_value
    
    def _create_stealth_action(self) -> AgentAction:
        """Create action to maintain stealth"""
        stealth_strategies = [
            "blend_into_shadows",
            "change_position_quietly",
            "create_distraction",
            "assume_disguise",
            "exit_temporarily"
        ]
        
        strategy = random.choice(stealth_strategies)
        
        reasoning = self.call_llm(
            f"Threat detected. Considering {strategy} to maintain cover.",
            "You are a master of stealth and deception. Survival is paramount.",
            task_type="quick_response"
        )
        
        return AgentAction(
            action_type="maintain_stealth",
            parameters={"strategy": strategy},
            reasoning=reasoning,
            confidence=0.9
        )
    
    def _create_intelligence_action(self, perceptions: List[str]) -> AgentAction:
        """Create intelligence gathering action"""
        intel_methods = [
            "eavesdrop_conversation",
            "pickpocket_documents", 
            "seduce_information",
            "bribe_for_secrets",
            "follow_target",
            "plant_listening_device"
        ]
        
        method = random.choice(intel_methods)
        
        # Select target based on perceptions
        target = self._select_intel_target(perceptions)
        
        reasoning = self.call_llm(
            f"Opportunity for intelligence gathering using {method} on {target}",
            "You are a skilled information broker. Every secret has value.",
            task_type="quick_response"
        )
        
        return AgentAction(
            action_type="gather_intelligence",
            target=target,
            parameters={"method": method},
            reasoning=reasoning,
            confidence=0.7
        )
    
    def _select_intel_target(self, perceptions: List[str]) -> str:
        """Select best target for intelligence gathering"""
        # Look for vulnerable or valuable targets in perceptions
        for perception in perceptions:
            if "vulnerable" in perception or "intoxicated" in perception:
                # Extract character name from perception
                words = perception.split()
                for word in words:
                    if word.endswith("'s") or word.isupper():
                        return word.replace("'s", "")
        
        return "random_patron"
    
    def _create_observation_action(self) -> AgentAction:
        """Create general observation action"""
        return AgentAction(
            action_type="observe_shadows",
            parameters={},
            reasoning="Maintaining surveillance from the shadows",
            confidence=0.6
        )
    
    def act(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute shadow operations"""
        self.last_action_time = datetime.now()
        results = {"success": False, "message": "", "effects": {}}
        
        if action.action_type == "maintain_stealth":
            results = self._execute_stealth(action, tavern_state)
        elif action.action_type == "gather_intelligence":
            results = self._execute_intelligence_gathering(action, tavern_state)
        elif action.action_type == "observe_shadows":
            results = self._execute_shadow_observation(action, tavern_state)
        else:
            results = {
                "success": True,
                "message": f"{self.name} melts into the shadows",
                "effects": {}
            }
        
        # Update memory with action results
        self.update_memory(f"Shadow operation: {results['message']}")
        
        return results
    
    def _execute_stealth(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute stealth maintenance"""
        strategy = action.parameters.get("strategy", "blend_into_shadows")
        
        # Increase stealth level
        self.stealth_level = min(1.0, self.stealth_level + 0.1)
        
        stealth_messages = {
            "blend_into_shadows": f"{self.name} becomes one with the darkness",
            "change_position_quietly": f"{self.name} silently relocates to a better vantage point",
            "create_distraction": f"{self.name} creates a subtle distraction to mask movement",
            "assume_disguise": f"{self.name} adopts a different persona",
            "exit_temporarily": f"{self.name} vanishes from sight temporarily"
        }
        
        return {
            "success": True,
            "message": stealth_messages.get(strategy, f"{self.name} maintains stealth"),
            "effects": {
                "stealth_increase": 0.1,
                "detection_risk": -0.2
            }
        }
    
    def _execute_intelligence_gathering(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute intelligence gathering operation"""
        method = action.parameters.get("method", "eavesdrop_conversation")
        target = action.target or "unknown"
        
        # Simulate intelligence gathering success
        success_chance = self.stealth_level * 0.8 + random.random() * 0.2
        
        if success_chance > 0.6:
            # Successful intelligence gathering
            intel_gained = self._generate_intelligence(method, target)
            self.secrets_database["valuable_information"].append({
                "intel": intel_gained,
                "source": target,
                "method": method,
                "timestamp": datetime.now().isoformat()
            })
            
            self.information_value += random.randint(5, 15)
            
            return {
                "success": True,
                "message": f"{self.name} successfully gathers intelligence: {intel_gained}",
                "effects": {
                    "intelligence_gained": intel_gained,
                    "information_value": self.information_value
                }
            }
        else:
            # Failed attempt - risk exposure
            self.stealth_level = max(0.3, self.stealth_level - 0.2)
            
            return {
                "success": False,
                "message": f"{self.name}'s intelligence gathering attempt was nearly detected",
                "effects": {
                    "stealth_decrease": -0.2,
                    "suspicion_raised": True
                }
            }
    
    def _generate_intelligence(self, method: str, target: str) -> str:
        """Generate realistic intelligence based on method and target"""
        intel_templates = {
            "eavesdrop_conversation": [
                f"{target} mentioned a secret meeting at midnight",
                f"{target} revealed financial troubles with local merchants",
                f"{target} spoke of hidden treasure in the old ruins",
                f"{target} discussed plans to leave town suddenly"
            ],
            "pickpocket_documents": [
                f"Found letter revealing {target}'s true identity",
                f"Discovered map to {target}'s hidden cache",
                f"Obtained contract showing {target}'s illegal dealings",
                f"Found evidence of {target}'s debts to dangerous people"
            ],
            "seduce_information": [
                f"{target} revealed family secrets under influence",
                f"{target} confessed to past crimes",
                f"{target} shared knowledge of local corruption",
                f"{target} disclosed information about rival factions"
            ],
            "bribe_for_secrets": [
                f"Paid informant revealed {target}'s weaknesses",
                f"Bought information about {target}'s associates",
                f"Purchased details of {target}'s daily routine",
                f"Acquired knowledge of {target}'s fears"
            ]
        }
        
        templates = intel_templates.get(method, ["Generic intelligence gathered"])
        return random.choice(templates)
    
    def _execute_shadow_observation(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute general shadow observation"""
        # Gather general intelligence
        observations = [
            "Noted unusual patron behavior patterns",
            "Observed potential security vulnerabilities", 
            "Identified valuable conversation targets",
            "Mapped tavern's hidden passages and exits",
            "Catalogued patron relationships and hierarchies"
        ]
        
        observation = random.choice(observations)
        self.update_memory(observation, "observation")
        
        return {
            "success": True,
            "message": f"{self.name} observes from shadows: {observation}",
            "effects": {
                "situational_awareness": 5
            }
        }
    
    def get_intelligence_summary(self) -> Dict[str, Any]:
        """Get summary of gathered intelligence"""
        return {
            "total_secrets": len(self.secrets_database["valuable_information"]),
            "information_value": self.information_value,
            "stealth_level": self.stealth_level,
            "recent_intel": self.secrets_database["valuable_information"][-3:] if self.secrets_database["valuable_information"] else []
        }
