"""
Agent Manager for orchestrating multiple AI agents in the tavern
Handles agent lifecycle, communication, and coordination
"""

import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass

from agents.base_agent import BaseAgent, AgentAction
from services.llm_service import llm_service, LLMRequest, LLMProvider
from config import agent_config

@dataclass
class AgentCommunication:
    """Structure for inter-agent communication"""
    sender: str
    receiver: str
    message: str
    message_type: str  # "warning", "information", "request", "response"
    timestamp: datetime
    priority: int = 1  # 1-10, higher is more urgent

class AgentManager:
    """Manages all AI agents in the tavern simulation"""
    
    def __init__(self):
        self.agents: Dict[str, BaseAgent] = {}
        self.communication_log: List[AgentCommunication] = []
        self.agent_actions_history: List[Dict[str, Any]] = []
        self.coordination_rules = self._initialize_coordination_rules()
        
        # Initialize default agents
        self._initialize_agents()
    
    def _initialize_agents(self):
        """Initialize all tavern agents"""
        from agents.karczmarz import KarczmarzAgent
        from agents.skrytobojca import SkrytobojcaAgent
        from agents.wiedzma import WiedzmaAgent
        from agents.zwiadowca import ZwiadowcaAgent
        from agents.czempion import CzempionAgent

        # Create all 5 agents
        self.agents["Karczmarz"] = KarczmarzAgent()
        self.agents["Skrytobójca"] = SkrytobojcaAgent()
        self.agents["Wiedźma"] = WiedzmaAgent()
        self.agents["Zwiadowca"] = ZwiadowcaAgent()
        self.agents["Czempion"] = CzempionAgent()

        print(f"✅ Initialized {len(self.agents)} agents: {list(self.agents.keys())}")
    
    def _initialize_coordination_rules(self) -> Dict[str, Any]:
        """Initialize rules for agent coordination"""
        return {
            "communication_triggers": {
                "high_tension": ["Karczmarz", "Skrytobójca"],  # These agents communicate during high tension
                "threat_detected": ["Skrytobójca", "Karczmarz"],  # Shadow agent warns tavern keeper
                "valuable_information": ["Skrytobójca", "Wiedźma"],  # Information sharing
                "chaos_activity": ["Wiedźma", "Karczmarz"]  # Mystic warns of chaos
            },
            "action_priorities": {
                "emergency": ["Karczmarz", "Skrytobójca", "Zwiadowca"],
                "information": ["Skrytobójca", "Zwiadowca", "Wiedźma"],
                "social": ["Karczmarz", "Wiedźma"],
                "combat": ["Czempion", "Karczmarz"]
            },
            "cooperation_matrix": {
                # Who works well together (positive values) or conflicts (negative)
                ("Karczmarz", "Skrytobójca"): 0.7,  # Mutual benefit
                ("Karczmarz", "Wiedźma"): 0.5,      # Cautious cooperation
                ("Skrytobójca", "Wiedźma"): 0.3,    # Limited trust
                ("Karczmarz", "Czempion"): -0.8,    # Natural enemies
                ("Skrytobójca", "Czempion"): -0.3   # Professional rivalry
            }
        }
    
    def process_turn(self, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Process one turn for all agents"""
        turn_results = {
            "agent_actions": {},
            "communications": [],
            "coordination_events": [],
            "tavern_effects": {}
        }
        
        # Step 1: All agents perceive the current state
        agent_perceptions = {}
        for agent_name, agent in self.agents.items():
            if agent.active:
                perceptions = agent.perceive(tavern_state)
                agent_perceptions[agent_name] = perceptions
        
        # Step 2: Check for coordination triggers
        coordination_events = self._check_coordination_triggers(agent_perceptions, tavern_state)
        turn_results["coordination_events"] = coordination_events
        
        # Step 3: Process inter-agent communications
        communications = self._process_communications(coordination_events)
        turn_results["communications"] = communications
        
        # Step 4: Agents decide on actions
        agent_decisions = {}
        for agent_name, agent in self.agents.items():
            if agent.active and agent.can_act():
                # Include communications in decision making
                relevant_comms = [c for c in communications if c.receiver == agent_name]
                enhanced_perceptions = agent_perceptions.get(agent_name, [])
                
                # Add communication content to perceptions
                for comm in relevant_comms:
                    enhanced_perceptions.append(f"COMMUNICATION from {comm.sender}: {comm.message}")
                
                decision = agent.decide(enhanced_perceptions)
                if decision:
                    agent_decisions[agent_name] = decision
        
        # Step 5: Execute actions with coordination
        for agent_name, action in agent_decisions.items():
            agent = self.agents[agent_name]
            
            # Check if action needs coordination
            if self._requires_coordination(action, agent_name):
                action = self._coordinate_action(action, agent_name, tavern_state)
            
            # Execute action
            result = agent.act(action, tavern_state)
            turn_results["agent_actions"][agent_name] = {
                "action": action.action_type,
                "result": result,
                "reasoning": action.reasoning
            }
            
            # Apply effects to tavern state
            if result.get("effects"):
                for effect_type, effect_value in result["effects"].items():
                    if effect_type not in turn_results["tavern_effects"]:
                        turn_results["tavern_effects"][effect_type] = 0
                    turn_results["tavern_effects"][effect_type] += effect_value
        
        # Step 6: Log actions for history
        self.agent_actions_history.append({
            "timestamp": datetime.now().isoformat(),
            "turn_results": turn_results,
            "tavern_state_snapshot": {
                "tension": tavern_state.get("tension_level", 0),
                "character_count": len(tavern_state.get("characters", [])),
                "reputation": tavern_state.get("reputation", 50)
            }
        })
        
        return turn_results
    
    def _check_coordination_triggers(self, agent_perceptions: Dict[str, List[str]], tavern_state: Dict[str, Any]) -> List[str]:
        """Check if any coordination triggers are activated"""
        triggers = []
        
        # High tension trigger
        if tavern_state.get("tension_level", 0) > 70:
            triggers.append("high_tension")
        
        # Threat detection trigger
        for agent_name, perceptions in agent_perceptions.items():
            for perception in perceptions:
                if "THREAT" in perception or "DANGER" in perception:
                    triggers.append("threat_detected")
                    break
        
        # Valuable information trigger
        for agent_name, perceptions in agent_perceptions.items():
            for perception in perceptions:
                if "VALUABLE" in perception or "INTEL" in perception:
                    triggers.append("valuable_information")
                    break
        
        # Chaos activity trigger
        characters = tavern_state.get("characters", [])
        for char in characters:
            if char.get("faction") == "Cultist":
                triggers.append("chaos_activity")
                break
        
        return list(set(triggers))  # Remove duplicates
    
    def _process_communications(self, coordination_events: List[str]) -> List[AgentCommunication]:
        """Process inter-agent communications based on coordination events"""
        communications = []
        
        for event in coordination_events:
            if event in self.coordination_rules["communication_triggers"]:
                agents_to_communicate = self.coordination_rules["communication_triggers"][event]
                
                if len(agents_to_communicate) >= 2:
                    sender_name = agents_to_communicate[0]
                    receiver_name = agents_to_communicate[1]
                    
                    if sender_name in self.agents and receiver_name in self.agents:
                        message = self._generate_communication_message(sender_name, receiver_name, event)
                        
                        comm = AgentCommunication(
                            sender=sender_name,
                            receiver=receiver_name,
                            message=message,
                            message_type=self._get_message_type(event),
                            timestamp=datetime.now(),
                            priority=self._get_message_priority(event)
                        )
                        
                        communications.append(comm)
                        self.communication_log.append(comm)
        
        return communications
    
    def _generate_communication_message(self, sender: str, receiver: str, event: str) -> str:
        """Generate appropriate communication message"""
        message_templates = {
            "high_tension": {
                ("Karczmarz", "Skrytobójca"): "Tension is rising. Keep watch for trouble.",
                ("Skrytobójca", "Karczmarz"): "I sense danger brewing. Be ready to act."
            },
            "threat_detected": {
                ("Skrytobójca", "Karczmarz"): "Threat identified. Recommend increased vigilance.",
                ("Karczmarz", "Skrytobójca"): "Acknowledged. Monitoring situation closely."
            },
            "valuable_information": {
                ("Skrytobójca", "Wiedźma"): "Gathered intelligence that may interest you.",
                ("Wiedźma", "Skrytobójca"): "The spirits whisper of hidden truths."
            },
            "chaos_activity": {
                ("Wiedźma", "Karczmarz"): "Dark energies stir. Chaos corruption detected.",
                ("Karczmarz", "Wiedźma"): "Understood. Will take protective measures."
            }
        }
        
        template_key = (sender, receiver)
        if event in message_templates and template_key in message_templates[event]:
            return message_templates[event][template_key]
        else:
            return f"{sender} communicates with {receiver} about {event}"
    
    def _get_message_type(self, event: str) -> str:
        """Get message type based on event"""
        type_mapping = {
            "high_tension": "warning",
            "threat_detected": "warning", 
            "valuable_information": "information",
            "chaos_activity": "warning"
        }
        return type_mapping.get(event, "information")
    
    def _get_message_priority(self, event: str) -> int:
        """Get message priority based on event"""
        priority_mapping = {
            "high_tension": 8,
            "threat_detected": 9,
            "valuable_information": 5,
            "chaos_activity": 10
        }
        return priority_mapping.get(event, 5)
    
    def _requires_coordination(self, action: AgentAction, agent_name: str) -> bool:
        """Check if action requires coordination with other agents"""
        coordination_actions = [
            "defuse_tension",
            "manage_crowd", 
            "protect_reputation",
            "gather_intelligence"
        ]
        return action.action_type in coordination_actions
    
    def _coordinate_action(self, action: AgentAction, agent_name: str, tavern_state: Dict[str, Any]) -> AgentAction:
        """Coordinate action with other agents if needed"""
        # For now, just add coordination note to reasoning
        action.reasoning += f" [Coordinated with other agents]"
        action.confidence *= 1.1  # Coordination increases confidence
        return action
    
    def get_agent_status_summary(self) -> Dict[str, Any]:
        """Get summary of all agent statuses"""
        summary = {}
        
        for agent_name, agent in self.agents.items():
            summary[agent_name] = {
                "active": agent.active,
                "emotional_state": agent.get_emotional_state(),
                "emotion_emoji": agent.get_emotion_emoji(),
                "status": agent.get_status_summary(),
                "recent_actions": len([a for a in self.agent_actions_history[-5:] 
                                    if agent_name in a.get("turn_results", {}).get("agent_actions", {})])
            }
        
        return summary
    
    def get_communication_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent communication history"""
        recent_comms = self.communication_log[-limit:]
        return [
            {
                "sender": comm.sender,
                "receiver": comm.receiver,
                "message": comm.message,
                "type": comm.message_type,
                "priority": comm.priority,
                "timestamp": comm.timestamp.strftime("%H:%M:%S")
            }
            for comm in recent_comms
        ]
    
    def add_agent(self, agent: BaseAgent) -> bool:
        """Add new agent to the manager"""
        if len(self.agents) >= agent_config.max_agents:
            return False
        
        if agent.name not in self.agents:
            self.agents[agent.name] = agent
            return True
        
        return False
    
    def remove_agent(self, agent_name: str) -> bool:
        """Remove agent from the manager"""
        if agent_name in self.agents:
            del self.agents[agent_name]
            return True
        return False
    
    def get_agent_reasoning_traces(self) -> Dict[str, List[str]]:
        """Get reasoning traces for all agents"""
        traces = {}
        for agent_name, agent in self.agents.items():
            traces[agent_name] = agent.memory.reasoning_trace[-5:]  # Last 5 reasoning steps
        return traces

# Global agent manager instance
agent_manager = AgentManager()
