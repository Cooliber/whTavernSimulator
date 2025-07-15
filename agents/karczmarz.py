"""
Karczmarz (Tavern Keeper) Agent
Wise, observant, protective of patrons
Uses Grok for complex management decisions
"""

import random
from typing import Dict, List, Optional, Any
from datetime import datetime

from .base_agent import BaseAgent, AgentAction

class KarczmarzAgent(BaseAgent):
    """Tavern Keeper - manages tavern operations and maintains order"""
    
    def __init__(self):
        super().__init__(
            name="Karczmarz",
            role="Tavern Keeper", 
            personality="Wise, observant, protective of patrons"
        )
        
        # Karczmarz-specific attributes
        self.tavern_knowledge = {
            "regular_customers": [],
            "troublemakers": [],
            "profitable_interactions": [],
            "reputation_threats": []
        }
        
        # Management priorities
        self.priorities = [
            "maintain_order",
            "protect_reputation", 
            "maximize_profit",
            "gather_information",
            "prevent_violence"
        ]
    
    def perceive(self, tavern_state: Dict[str, Any]) -> List[str]:
        """Perceive tavern state from management perspective"""
        perceptions = []
        
        # Monitor tension levels
        tension = tavern_state.get("tension_level", 0)
        if tension > 70:
            perceptions.append(f"ALERT: Tavern tension dangerously high at {tension}")
            self.update_emotion("alertness", 0.3)
        elif tension > 50:
            perceptions.append(f"WARNING: Rising tension detected at {tension}")
            self.update_emotion("alertness", 0.1)
        
        # Monitor character interactions
        characters = tavern_state.get("characters", [])
        if len(characters) > tavern_state.get("capacity", 20) * 0.8:
            perceptions.append("Tavern approaching capacity - monitor for overcrowding")
        
        # Check for known troublemakers
        for char in characters:
            if char.get("name") in self.tavern_knowledge["troublemakers"]:
                perceptions.append(f"Known troublemaker {char['name']} present")
                self.update_emotion("suspicion", 0.2)
        
        # Monitor reputation
        reputation = tavern_state.get("reputation", 50)
        if reputation < 40:
            perceptions.append(f"Tavern reputation concerning at {reputation}")
            self.update_emotion("satisfaction", -0.2)
        
        # Check recent events
        recent_events = tavern_state.get("recent_events", [])
        for event in recent_events[-3:]:
            if "brawl" in event.lower():
                perceptions.append(f"Recent violence detected: {event}")
                self.update_emotion("aggression", 0.1)
            elif "profit" in event.lower() or "sale" in event.lower():
                perceptions.append(f"Business opportunity: {event}")
                self.update_emotion("satisfaction", 0.1)
        
        return perceptions
    
    def decide(self, perceptions: List[str]) -> Optional[AgentAction]:
        """Make management decisions based on perceptions"""
        if not self.can_act():
            return None
        
        self.add_reasoning_step("Analyzing tavern situation...")
        
        # Prioritize actions based on current situation
        action_priorities = self._assess_action_priorities(perceptions)
        
        if not action_priorities:
            return None
        
        # Select highest priority action
        top_priority = action_priorities[0]
        action_type = top_priority["type"]
        
        self.add_reasoning_step(f"Decided on action: {action_type}")
        
        # Create appropriate action
        if action_type == "defuse_tension":
            return self._create_defuse_action(perceptions)
        elif action_type == "gather_information":
            return self._create_information_action(perceptions)
        elif action_type == "manage_crowd":
            return self._create_crowd_management_action(perceptions)
        elif action_type == "protect_reputation":
            return self._create_reputation_action(perceptions)
        else:
            return self._create_observation_action()
    
    def _assess_action_priorities(self, perceptions: List[str]) -> List[Dict[str, Any]]:
        """Assess and prioritize possible actions"""
        priorities = []
        
        # Check for immediate threats
        for perception in perceptions:
            if "ALERT" in perception or "tension dangerously high" in perception:
                priorities.append({
                    "type": "defuse_tension",
                    "urgency": 10,
                    "reasoning": "Immediate intervention required to prevent violence"
                })
            elif "troublemaker" in perception:
                priorities.append({
                    "type": "manage_crowd", 
                    "urgency": 8,
                    "reasoning": "Monitor known troublemaker closely"
                })
            elif "reputation" in perception:
                priorities.append({
                    "type": "protect_reputation",
                    "urgency": 6,
                    "reasoning": "Reputation management needed"
                })
            elif "capacity" in perception:
                priorities.append({
                    "type": "manage_crowd",
                    "urgency": 5,
                    "reasoning": "Crowd control needed"
                })
        
        # Always consider information gathering
        priorities.append({
            "type": "gather_information",
            "urgency": 3,
            "reasoning": "Continuous situational awareness"
        })
        
        # Sort by urgency
        return sorted(priorities, key=lambda x: x["urgency"], reverse=True)
    
    def _create_defuse_action(self, perceptions: List[str]) -> AgentAction:
        """Create action to defuse tension"""
        strategies = [
            "offer_free_drinks",
            "tell_calming_story", 
            "separate_antagonists",
            "call_for_order",
            "distract_with_entertainment"
        ]
        
        strategy = random.choice(strategies)
        
        reasoning = self.call_llm(
            f"Tavern tension is high. I'm considering {strategy}. What's the best approach?",
            "You are a wise tavern keeper who knows how to manage difficult situations.",
            task_type="strategic_planning"
        )
        
        return AgentAction(
            action_type="defuse_tension",
            parameters={"strategy": strategy},
            reasoning=reasoning,
            confidence=0.8
        )
    
    def _create_information_action(self, perceptions: List[str]) -> AgentAction:
        """Create action to gather information"""
        info_targets = [
            "listen_to_conversations",
            "observe_character_interactions", 
            "check_with_staff",
            "review_recent_transactions",
            "assess_customer_satisfaction"
        ]
        
        target = random.choice(info_targets)
        
        reasoning = f"Gathering intelligence through {target} to better understand tavern dynamics"
        
        return AgentAction(
            action_type="gather_information",
            parameters={"method": target},
            reasoning=reasoning,
            confidence=0.6
        )
    
    def _create_crowd_management_action(self, perceptions: List[str]) -> AgentAction:
        """Create crowd management action"""
        management_strategies = [
            "redirect_traffic_flow",
            "encourage_table_sharing",
            "suggest_outdoor_seating",
            "limit_new_admissions",
            "offer_takeaway_service"
        ]
        
        strategy = random.choice(management_strategies)
        
        return AgentAction(
            action_type="manage_crowd",
            parameters={"strategy": strategy},
            reasoning=f"Managing crowd through {strategy}",
            confidence=0.7
        )
    
    def _create_reputation_action(self, perceptions: List[str]) -> AgentAction:
        """Create reputation protection action"""
        reputation_strategies = [
            "address_customer_complaints",
            "improve_service_quality",
            "offer_compensation",
            "spread_positive_rumors",
            "showcase_tavern_strengths"
        ]
        
        strategy = random.choice(reputation_strategies)
        
        return AgentAction(
            action_type="protect_reputation",
            parameters={"strategy": strategy},
            reasoning=f"Protecting tavern reputation through {strategy}",
            confidence=0.6
        )
    
    def _create_observation_action(self) -> AgentAction:
        """Create general observation action"""
        return AgentAction(
            action_type="observe",
            parameters={},
            reasoning="Maintaining general awareness of tavern situation",
            confidence=0.5
        )
    
    def act(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the decided action"""
        self.last_action_time = datetime.now()
        results = {"success": False, "message": "", "effects": {}}
        
        if action.action_type == "defuse_tension":
            results = self._execute_defuse_tension(action, tavern_state)
        elif action.action_type == "gather_information":
            results = self._execute_gather_information(action, tavern_state)
        elif action.action_type == "manage_crowd":
            results = self._execute_manage_crowd(action, tavern_state)
        elif action.action_type == "protect_reputation":
            results = self._execute_protect_reputation(action, tavern_state)
        else:
            results = {
                "success": True,
                "message": f"{self.name} observes the tavern carefully",
                "effects": {}
            }
        
        # Update memory with action results
        self.update_memory(f"Executed {action.action_type}: {results['message']}")
        
        return results
    
    def _execute_defuse_tension(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute tension defusing action"""
        strategy = action.parameters.get("strategy", "call_for_order")
        
        # Simulate tension reduction
        tension_reduction = random.randint(10, 25)
        
        messages = {
            "offer_free_drinks": f"{self.name} offers a round of drinks on the house to calm tensions",
            "tell_calming_story": f"{self.name} tells an engaging story to distract from conflicts",
            "separate_antagonists": f"{self.name} diplomatically separates potential troublemakers",
            "call_for_order": f"{self.name} calls for order with authoritative presence",
            "distract_with_entertainment": f"{self.name} arranges entertainment to lighten the mood"
        }
        
        return {
            "success": True,
            "message": messages.get(strategy, f"{self.name} takes action to defuse tension"),
            "effects": {
                "tension_change": -tension_reduction,
                "reputation_change": 2
            }
        }
    
    def _execute_gather_information(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute information gathering"""
        method = action.parameters.get("method", "observe")
        
        # Simulate information discovery
        info_gained = random.choice([
            "Overheard discussion about merchant caravan arriving tomorrow",
            "Noticed suspicious character asking about local officials", 
            "Customer complained about ale quality",
            "Regular patron mentioned family troubles",
            "Stranger inquired about room availability for extended stay"
        ])
        
        self.update_memory(info_gained, "information")
        
        return {
            "success": True,
            "message": f"{self.name} gathers information: {info_gained}",
            "effects": {
                "information_gained": info_gained
            }
        }
    
    def _execute_manage_crowd(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute crowd management"""
        strategy = action.parameters.get("strategy", "redirect_traffic_flow")
        
        return {
            "success": True,
            "message": f"{self.name} manages crowd through {strategy}",
            "effects": {
                "crowd_satisfaction": 5,
                "efficiency_bonus": 3
            }
        }
    
    def _execute_protect_reputation(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute reputation protection"""
        strategy = action.parameters.get("strategy", "improve_service_quality")
        
        reputation_boost = random.randint(3, 8)
        
        return {
            "success": True,
            "message": f"{self.name} protects tavern reputation through {strategy}",
            "effects": {
                "reputation_change": reputation_boost
            }
        }
