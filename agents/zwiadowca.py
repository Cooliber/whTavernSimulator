"""
Zwiadowca (Information Gatherer) Agent
Alert, curious, well-traveled
Uses Cerebras for quick information processing and rapid responses
"""

import random
from typing import Dict, List, Optional, Any
from datetime import datetime

from .base_agent import BaseAgent, AgentAction

class ZwiadowcaAgent(BaseAgent):
    """Information Gatherer - reports news and tracks movements"""
    
    def __init__(self):
        super().__init__(
            name="Zwiadowca",
            role="Information Gatherer",
            personality="Alert, curious, well-traveled"
        )
        
        # Scout-specific attributes
        self.intelligence_network = {
            "road_reports": [],
            "merchant_news": [],
            "danger_warnings": [],
            "travel_routes": {},
            "regional_updates": []
        }
        
        self.alertness_level = 0.9  # High awareness of surroundings
        self.travel_experience = 0.8  # Knowledge of roads and regions
        
        # Scout priorities
        self.priorities = [
            "report_news",
            "track_movements",
            "warn_of_dangers",
            "gather_travel_intel",
            "monitor_strangers"
        ]
    
    def perceive(self, tavern_state: Dict[str, Any]) -> List[str]:
        """Perceive with scout's trained awareness"""
        perceptions = []
        
        # Analyze character movements and origins
        characters = tavern_state.get("characters", [])
        for char in characters:
            faction = char.get("faction", "")
            name = char.get("name", "")
            
            # Identify travelers and foreigners
            foreign_factions = ["Arabyan", "Cathayan", "Nipponese", "Norse"]
            if faction in foreign_factions:
                perceptions.append(f"TRAVELER: {name} from {faction} lands - potential news source")
                self.update_emotion("curiosity", 0.3)
            
            # Spot potential threats
            if faction == "Cultist":
                perceptions.append(f"THREAT: Chaos cultist {name} detected - immediate danger")
                self.update_emotion("alertness", 0.5)
            elif faction == "Witch Hunter":
                perceptions.append(f"AUTHORITY: Witch Hunter {name} present - official business likely")
            
            # Notice suspicious behavior
            drunk_level = char.get("drunk_level", 0)
            if drunk_level < 2 and len(characters) > 10:
                perceptions.append(f"ALERT: {name} remains sober while others drink - watching someone")
        
        # Monitor tavern traffic patterns
        character_count = len(characters)
        if character_count > 15:
            perceptions.append("TRAFFIC: Heavy tavern traffic - major event or gathering")
        elif character_count < 5:
            perceptions.append("QUIET: Unusually quiet night - potential danger keeping people away")
        
        # Check tension for conflict indicators
        tension = tavern_state.get("tension_level", 0)
        if tension > 60:
            perceptions.append(f"CONFLICT: Rising tensions at {tension} - violence may erupt")
            self.update_emotion("alertness", 0.2)
        
        # Analyze recent events for patterns
        recent_events = tavern_state.get("recent_events", [])
        for event in recent_events[-3:]:
            if "arrived" in event.lower():
                perceptions.append(f"MOVEMENT: New arrivals detected - {event}")
            elif "left" in event.lower():
                perceptions.append(f"DEPARTURE: Someone departed - {event}")
        
        return perceptions
    
    def decide(self, perceptions: List[str]) -> Optional[AgentAction]:
        """Make quick scout decisions"""
        if not self.can_act():
            return None
        
        self.add_reasoning_step("Scanning for actionable intelligence...")
        
        # Quick threat assessment
        threat_level = self._assess_immediate_threats(perceptions)
        intel_value = self._assess_intelligence_value(perceptions)
        
        if threat_level > 7:
            self.add_reasoning_step("Immediate threat detected - warning needed")
            return self._create_warning_action(perceptions)
        elif intel_value > 6:
            self.add_reasoning_step("Valuable intelligence opportunity")
            return self._create_intelligence_action(perceptions)
        elif any("TRAVELER" in p for p in perceptions):
            self.add_reasoning_step("Foreign travelers present - news gathering opportunity")
            return self._create_news_gathering_action(perceptions)
        else:
            return self._create_patrol_action()
    
    def _assess_immediate_threats(self, perceptions: List[str]) -> int:
        """Quick threat assessment"""
        threat_level = 0
        
        for perception in perceptions:
            if "THREAT" in perception:
                threat_level += 8
            elif "CONFLICT" in perception:
                threat_level += 6
            elif "Chaos cultist" in perception:
                threat_level += 9
            elif "violence may erupt" in perception:
                threat_level += 7
        
        return threat_level
    
    def _assess_intelligence_value(self, perceptions: List[str]) -> int:
        """Assess intelligence gathering opportunities"""
        intel_value = 0
        
        for perception in perceptions:
            if "TRAVELER" in perception:
                intel_value += 5
            elif "AUTHORITY" in perception:
                intel_value += 4
            elif "MOVEMENT" in perception:
                intel_value += 3
            elif "major event" in perception:
                intel_value += 6
        
        return intel_value
    
    def _create_warning_action(self, perceptions: List[str]) -> AgentAction:
        """Create immediate warning action"""
        warning_types = [
            "alert_authorities",
            "warn_patrons",
            "signal_allies",
            "prepare_escape_routes",
            "gather_witnesses"
        ]
        
        warning_type = random.choice(warning_types)
        
        reasoning = self.call_llm(
            f"Immediate threat detected. Considering {warning_type} to protect people.",
            "You are an experienced scout. Quick action saves lives.",
            task_type="quick_response"
        )
        
        return AgentAction(
            action_type="issue_warning",
            parameters={"warning_type": warning_type},
            reasoning=reasoning,
            confidence=0.9
        )
    
    def _create_intelligence_action(self, perceptions: List[str]) -> AgentAction:
        """Create intelligence gathering action"""
        intel_methods = [
            "interview_travelers",
            "map_movement_patterns",
            "track_suspicious_activity",
            "gather_road_reports",
            "collect_regional_news"
        ]
        
        method = random.choice(intel_methods)
        target = self._select_intel_target(perceptions)
        
        reasoning = self.call_llm(
            f"Intelligence opportunity using {method} on {target}",
            "You are a skilled scout. Information is your weapon.",
            task_type="quick_response"
        )
        
        return AgentAction(
            action_type="gather_intelligence",
            target=target,
            parameters={"method": method},
            reasoning=reasoning,
            confidence=0.8
        )
    
    def _create_news_gathering_action(self, perceptions: List[str]) -> AgentAction:
        """Create news gathering action"""
        news_methods = [
            "trade_road_stories",
            "exchange_regional_updates",
            "share_travel_warnings",
            "collect_merchant_reports",
            "gather_political_news"
        ]
        
        method = random.choice(news_methods)
        
        return AgentAction(
            action_type="gather_news",
            parameters={"method": method},
            reasoning=f"Gathering regional news through {method}",
            confidence=0.7
        )
    
    def _select_intel_target(self, perceptions: List[str]) -> str:
        """Select best intelligence target"""
        # Look for specific targets in perceptions
        for perception in perceptions:
            if "TRAVELER:" in perception:
                # Extract traveler name
                words = perception.split()
                for i, word in enumerate(words):
                    if word == "TRAVELER:" and i + 1 < len(words):
                        return words[i + 1]
            elif "AUTHORITY:" in perception:
                words = perception.split()
                for i, word in enumerate(words):
                    if word == "AUTHORITY:" and i + 1 < len(words):
                        return words[i + 1]
        
        return "foreign_traveler"
    
    def _create_patrol_action(self) -> AgentAction:
        """Create general patrol action"""
        return AgentAction(
            action_type="patrol_area",
            parameters={},
            reasoning="Maintaining situational awareness through patrol",
            confidence=0.6
        )
    
    def act(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute scout operations"""
        self.last_action_time = datetime.now()
        results = {"success": False, "message": "", "effects": {}}
        
        if action.action_type == "issue_warning":
            results = self._execute_warning(action, tavern_state)
        elif action.action_type == "gather_intelligence":
            results = self._execute_intelligence_gathering(action, tavern_state)
        elif action.action_type == "gather_news":
            results = self._execute_news_gathering(action, tavern_state)
        elif action.action_type == "patrol_area":
            results = self._execute_patrol(action, tavern_state)
        else:
            results = {
                "success": True,
                "message": f"{self.name} maintains vigilant watch",
                "effects": {}
            }
        
        # Update scout memory
        self.update_memory(f"Scout operation: {results['message']}")

        return results

    def _execute_warning(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute warning action"""
        warning_type = action.parameters.get("warning_type", "warn_patrons")

        warning_messages = {
            "alert_authorities": f"{self.name} discreetly alerts tavern authorities to potential threat",
            "warn_patrons": f"{self.name} subtly warns trusted patrons of danger",
            "signal_allies": f"{self.name} sends coded signals to known allies",
            "prepare_escape_routes": f"{self.name} quietly checks exits and escape routes",
            "gather_witnesses": f"{self.name} positions reliable witnesses strategically"
        }

        # Warnings can reduce tension by preventing escalation
        tension_reduction = random.randint(15, 30)

        return {
            "success": True,
            "message": warning_messages.get(warning_type, f"{self.name} issues warning"),
            "effects": {
                "tension_change": -tension_reduction,
                "threat_mitigation": True,
                "preparedness_bonus": 10
            }
        }

    def _execute_intelligence_gathering(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute intelligence gathering"""
        method = action.parameters.get("method", "interview_travelers")
        target = action.target or "unknown"

        # Scout success based on alertness and experience
        success_chance = (self.alertness_level + self.travel_experience) / 2

        if random.random() < success_chance:
            # Successful intelligence gathering
            intel = self._generate_scout_intelligence(method, target)

            self.intelligence_network["regional_updates"].append({
                "intel": intel,
                "source": target,
                "method": method,
                "timestamp": datetime.now().isoformat()
            })

            return {
                "success": True,
                "message": f"{self.name} gathers intelligence: {intel}",
                "effects": {
                    "intelligence_gained": intel,
                    "network_value": 5
                }
            }
        else:
            return {
                "success": False,
                "message": f"{self.name}'s intelligence gathering attempt yields little information",
                "effects": {
                    "minor_intel": True
                }
            }

    def _execute_news_gathering(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute news gathering"""
        method = action.parameters.get("method", "trade_road_stories")

        # Generate regional news
        news = self._generate_regional_news(method)

        self.intelligence_network["road_reports"].append({
            "news": news,
            "method": method,
            "timestamp": datetime.now().isoformat()
        })

        return {
            "success": True,
            "message": f"{self.name} gathers news: {news}",
            "effects": {
                "regional_knowledge": news,
                "reputation_change": 2
            }
        }

    def _execute_patrol(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute patrol action"""
        patrol_observations = [
            "Noted unusual movement patterns near the entrance",
            "Observed potential security vulnerabilities",
            "Identified escape routes and defensive positions",
            "Catalogued patron behavior and relationships",
            "Assessed crowd dynamics and tension points"
        ]

        observation = random.choice(patrol_observations)
        self.update_memory(observation, "patrol")

        return {
            "success": True,
            "message": f"{self.name} patrols area: {observation}",
            "effects": {
                "situational_awareness": 8,
                "security_assessment": True
            }
        }

    def _generate_scout_intelligence(self, method: str, target: str) -> str:
        """Generate realistic scout intelligence"""
        intel_templates = {
            "interview_travelers": [
                f"{target} reports bandits on the eastern road",
                f"{target} mentions unusual military movements near the border",
                f"{target} describes strange lights seen in the forest",
                f"{target} warns of plague outbreak in distant village"
            ],
            "map_movement_patterns": [
                f"Tracked {target}'s associates - they meet regularly at midnight",
                f"Mapped {target}'s daily routine - vulnerable during morning hours",
                f"Identified {target}'s escape routes and safe houses",
                f"Documented {target}'s communication methods and contacts"
            ],
            "track_suspicious_activity": [
                f"{target} received coded message from unknown sender",
                f"{target} made suspicious payment to local informant",
                f"{target} visited abandoned building after dark",
                f"{target} carried concealed weapon despite peaceful appearance"
            ],
            "gather_road_reports": [
                f"Merchants report increased goblin activity on trade routes",
                f"Travelers warn of bridge collapse blocking main road",
                f"Caravans mention new toll collectors demanding excessive fees",
                f"Pilgrims describe miraculous healing at distant shrine"
            ]
        }

        templates = intel_templates.get(method, ["General intelligence gathered"])
        return random.choice(templates)

    def _generate_regional_news(self, method: str) -> str:
        """Generate regional news and updates"""
        news_templates = {
            "trade_road_stories": [
                "New trade agreement signed between Empire and Bretonnia",
                "Merchant guild reports record profits this season",
                "Rare spices arriving from Araby next month",
                "Trade route reopened after goblin threat eliminated"
            ],
            "exchange_regional_updates": [
                "Border tensions rising between neighboring provinces",
                "Harvest festival preparations underway in capital",
                "New tax policies affecting traveling merchants",
                "Regional lord seeking mercenaries for expedition"
            ],
            "share_travel_warnings": [
                "Wolves spotted near the mountain passes",
                "Flash floods reported in river valleys",
                "Suspicious strangers asking about local defenses",
                "Unusual weather patterns affecting travel schedules"
            ],
            "collect_political_news": [
                "Noble houses forming new alliance",
                "Court intrigue threatens regional stability",
                "New appointments to provincial government",
                "Diplomatic mission arriving from foreign lands"
            ]
        }

        templates = news_templates.get(method, ["Regional news gathered"])
        return random.choice(templates)

    def get_intelligence_summary(self) -> Dict[str, Any]:
        """Get summary of gathered intelligence"""
        return {
            "road_reports": len(self.intelligence_network["road_reports"]),
            "regional_updates": len(self.intelligence_network["regional_updates"]),
            "alertness_level": self.alertness_level,
            "travel_experience": self.travel_experience,
            "recent_intel": self.intelligence_network["regional_updates"][-3:] if self.intelligence_network["regional_updates"] else []
        }
