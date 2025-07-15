"""
Narrative Engine for dynamic storytelling, quest generation, and adaptive narrative
Orchestrates agents, memory, and LLM services for immersive Warhammer Fantasy experiences
"""

import time
import random
import uuid
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from enum import Enum

from .llm_service import LLMService, LLMRequest, LLMProvider
from .cerebras_service import CerebrasService, CerebrasRequest, ResponseType
from .agent_memory import AgentMemorySystem, MemoryType, MemoryImportance

class NarrativeEvent(Enum):
    TAVERN_ENTRANCE = "tavern_entrance"
    MYSTERIOUS_STRANGER = "mysterious_stranger"
    BRAWL_BREWING = "brawl_brewing"
    RUMOR_SPREADING = "rumor_spreading"
    QUEST_OPPORTUNITY = "quest_opportunity"
    THREAT_DETECTED = "threat_detected"
    ALLIANCE_FORMING = "alliance_forming"
    BETRAYAL_REVEALED = "betrayal_revealed"

class QuestType(Enum):
    INVESTIGATION = "investigation"
    RESCUE_MISSION = "rescue_mission"
    TREASURE_HUNT = "treasure_hunt"
    DIPLOMATIC_MISSION = "diplomatic_mission"
    COMBAT_CHALLENGE = "combat_challenge"
    MYSTICAL_RITUAL = "mystical_ritual"

@dataclass
class NarrativeState:
    """Current state of the narrative"""
    tension_level: int = 0  # 0-100
    active_events: List[str] = None
    active_quests: List[str] = None
    character_relationships: Dict[str, Dict[str, float]] = None
    tavern_atmosphere: str = "calm"
    time_of_day: str = "evening"
    weather: str = "clear"
    
    def __post_init__(self):
        if self.active_events is None:
            self.active_events = []
        if self.active_quests is None:
            self.active_quests = []
        if self.character_relationships is None:
            self.character_relationships = {}

@dataclass
class Quest:
    """Quest structure"""
    id: str
    quest_type: QuestType
    title: str
    description: str
    objectives: List[str]
    rewards: List[str]
    difficulty: int  # 1-10
    time_limit: Optional[int] = None  # minutes
    required_agents: List[str] = None
    status: str = "available"  # available, active, completed, failed
    progress: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.required_agents is None:
            self.required_agents = []
        if self.progress is None:
            self.progress = {}

class NarrativeEngine:
    """Main narrative engine orchestrating dynamic storytelling"""

    def __init__(self, economy_system=None):
        self.llm_service = LLMService()
        self.cerebras_service = CerebrasService()
        self.memory_system = AgentMemorySystem()

        # Import here to avoid circular imports
        if economy_system is None:
            from .tavern_economy import tavern_economy
            self.economy_system = tavern_economy
        else:
            self.economy_system = economy_system
        
        self.narrative_state = NarrativeState()
        self.active_quests: Dict[str, Quest] = {}
        self.event_history: List[Dict[str, Any]] = []
        
        # Agent roles and capabilities (17 agents organized by factions)
        self.agent_roles = self._initialize_17_agents()

        # Faction organization for sub-crew coordination
        self.faction_crews = {
            "Empire": ["Karczmarz", "Kapitan_Straży", "Kupiec_Imperialny", "Czarodziej_Jasności"],
            "Chaos": ["Czempion", "Kultista_Nurgle", "Berserker_Khorne", "Mag_Tzeentch"],
            "Elves": ["Zwiadowca", "Mag_Wysokich_Elfów", "Strażnik_Lasu", "Tancerz_Cieni"],
            "Dwarfs": ["Kowal_Krasnoludzki", "Górnik_Karak", "Inżynier_Gildii"],
            "Neutrals": ["Wiedźma", "Łowca_Nagród", "Handlarz_Halfling"]
        }
        
        # Narrative templates
        self.event_templates = self._load_event_templates()
        self.quest_templates = self._load_quest_templates()

    def _initialize_17_agents(self) -> Dict[str, Dict[str, Any]]:
        """Initialize all 17 agents with their roles and capabilities"""
        return {
            # Empire Faction (4 agents)
            "Karczmarz": {
                "primary_role": "information_hub",
                "capabilities": ["social_interaction", "local_knowledge", "resource_management"],
                "narrative_function": "quest_giver",
                "faction": "Empire",
                "sub_crew": "Empire"
            },
            "Kapitan_Straży": {
                "primary_role": "law_enforcement",
                "capabilities": ["combat", "leadership", "investigation"],
                "narrative_function": "authority_figure",
                "faction": "Empire",
                "sub_crew": "Empire"
            },
            "Kupiec_Imperialny": {
                "primary_role": "trade_coordinator",
                "capabilities": ["negotiation", "economics", "networking"],
                "narrative_function": "resource_provider",
                "faction": "Empire",
                "sub_crew": "Empire"
            },
            "Czarodziej_Jasności": {
                "primary_role": "light_magic_user",
                "capabilities": ["healing", "divination", "protection_magic"],
                "narrative_function": "support_caster",
                "faction": "Empire",
                "sub_crew": "Empire"
            },

            # Chaos Faction (4 agents)
            "Czempion": {
                "primary_role": "chaos_agent",
                "capabilities": ["corruption", "combat", "intimidation"],
                "narrative_function": "antagonist",
                "faction": "Chaos",
                "sub_crew": "Chaos"
            },
            "Kultista_Nurgle": {
                "primary_role": "plague_spreader",
                "capabilities": ["disease_magic", "resilience", "corruption"],
                "narrative_function": "chaos_support",
                "faction": "Chaos",
                "sub_crew": "Chaos"
            },
            "Berserker_Khorne": {
                "primary_role": "blood_warrior",
                "capabilities": ["berserker_rage", "melee_combat", "intimidation"],
                "narrative_function": "chaos_enforcer",
                "faction": "Chaos",
                "sub_crew": "Chaos"
            },
            "Mag_Tzeentch": {
                "primary_role": "change_sorcerer",
                "capabilities": ["illusion_magic", "manipulation", "scheming"],
                "narrative_function": "chaos_manipulator",
                "faction": "Chaos",
                "sub_crew": "Chaos"
            },

            # Elves Faction (4 agents)
            "Zwiadowca": {
                "primary_role": "intelligence_gathering",
                "capabilities": ["scouting", "tracking", "survival"],
                "narrative_function": "information_broker",
                "faction": "Elves",
                "sub_crew": "Elves"
            },
            "Mag_Wysokich_Elfów": {
                "primary_role": "high_magic_user",
                "capabilities": ["high_magic", "ancient_knowledge", "artifact_lore"],
                "narrative_function": "lore_master",
                "faction": "Elves",
                "sub_crew": "Elves"
            },
            "Strażnik_Lasu": {
                "primary_role": "nature_guardian",
                "capabilities": ["nature_magic", "archery", "forest_knowledge"],
                "narrative_function": "nature_ally",
                "faction": "Elves",
                "sub_crew": "Elves"
            },
            "Tancerz_Cieni": {
                "primary_role": "shadow_operative",
                "capabilities": ["stealth", "assassination", "shadow_magic"],
                "narrative_function": "dark_elf_agent",
                "faction": "Elves",
                "sub_crew": "Elves"
            },

            # Dwarfs Faction (3 agents)
            "Kowal_Krasnoludzki": {
                "primary_role": "master_craftsman",
                "capabilities": ["smithing", "engineering", "runic_magic"],
                "narrative_function": "equipment_provider",
                "faction": "Dwarfs",
                "sub_crew": "Dwarfs"
            },
            "Górnik_Karak": {
                "primary_role": "underground_expert",
                "capabilities": ["mining", "tunnel_fighting", "geology"],
                "narrative_function": "underground_guide",
                "faction": "Dwarfs",
                "sub_crew": "Dwarfs"
            },
            "Inżynier_Gildii": {
                "primary_role": "siege_specialist",
                "capabilities": ["engineering", "siege_weapons", "explosives"],
                "narrative_function": "technical_expert",
                "faction": "Dwarfs",
                "sub_crew": "Dwarfs"
            },

            # Neutral Faction (3 agents)
            "Wiedźma": {
                "primary_role": "mystical_advisor",
                "capabilities": ["divination", "magic", "ancient_knowledge"],
                "narrative_function": "lore_keeper",
                "faction": "Neutrals",
                "sub_crew": "Neutrals"
            },
            "Łowca_Nagród": {
                "primary_role": "bounty_hunter",
                "capabilities": ["tracking", "combat", "investigation"],
                "narrative_function": "mercenary",
                "faction": "Neutrals",
                "sub_crew": "Neutrals"
            },
            "Handlarz_Halfling": {
                "primary_role": "merchant_trader",
                "capabilities": ["trading", "cooking", "social_networking"],
                "narrative_function": "supply_coordinator",
                "faction": "Neutrals",
                "sub_crew": "Neutrals"
            }
        }
    
    def generate_dynamic_event(self, trigger_context: Dict[str, Any] = None, fast_mode: bool = False) -> Dict[str, Any]:
        """Generate a dynamic narrative event based on current context"""

        # Analyze current narrative state
        context = self._analyze_narrative_context(trigger_context)

        # Select appropriate event type
        event_type = self._select_event_type(context)

        # Fast mode: skip LLM calls for performance testing
        if fast_mode:
            event = self._generate_fallback_event(event_type, context)
        else:
            # Generate event using Groq for complex narrative planning
            event_request = LLMRequest(
                prompt=self._build_event_prompt(event_type, context),
                system_message=self._get_narrative_system_prompt(),
                agent_name="NarrativeEngine",
                provider=LLMProvider.GROQ,
                max_tokens=800,
                temperature=0.8,
                context=context
            )

            response = self.llm_service.call_llm(event_request)

            if response.success:
                event = self._parse_event_response(response.content, event_type, context)
            else:
                event = self._generate_fallback_event(event_type, context)

        # Store event in memory and update narrative state
        self._process_event(event)

        return event
    
    def generate_quest(self, quest_type: QuestType = None, difficulty: int = None) -> Quest:
        """Generate a new quest based on current narrative state"""
        
        if quest_type is None:
            quest_type = self._select_quest_type()
        
        if difficulty is None:
            difficulty = self._calculate_quest_difficulty()
        
        # Generate quest using Groq for detailed planning
        quest_prompt = self._build_quest_prompt(quest_type, difficulty)
        
        quest_request = LLMRequest(
            prompt=quest_prompt,
            system_message=self._get_quest_system_prompt(),
            agent_name="QuestMaster",
            provider=LLMProvider.GROQ,
            max_tokens=1000,
            temperature=0.7,
            context={"narrative_state": asdict(self.narrative_state)}
        )
        
        response = self.llm_service.call_llm(quest_request)
        
        if response.success:
            quest = self._parse_quest_response(response.content, quest_type, difficulty)
        else:
            quest = self._generate_fallback_quest(quest_type, difficulty)
        
        # Add quest to active quests
        self.active_quests[quest.id] = quest
        self.narrative_state.active_quests.append(quest.id)
        
        return quest
    
    def orchestrate_agent_interaction(self, agents: List[str], scenario: str) -> List[Dict[str, Any]]:
        """Orchestrate interaction between multiple agents"""
        
        interactions = []
        
        for i, agent in enumerate(agents):
            # Get agent context from memory
            agent_context = self.memory_system.get_agent_context(agent)
            
            # Determine agent's response using appropriate LLM
            agent_role = self.agent_roles.get(agent, {})
            
            if agent_role.get("narrative_function") in ["quest_giver", "lore_keeper"]:
                # Use Groq for complex narrative responses
                response = self._get_agent_narrative_response(agent, scenario, agent_context, LLMProvider.GROQ)
            else:
                # Use Cerebras for quick reactions
                response = self._get_agent_quick_response(agent, scenario, agent_context)
            
            interaction = {
                "agent": agent,
                "response": response,
                "timestamp": time.time(),
                "context": agent_context,
                "scenario": scenario
            }
            
            interactions.append(interaction)
            
            # Store interaction in agent memory
            self.memory_system.store_memory(
                agent_id=agent,
                memory_type=MemoryType.INTERACTION,
                content=f"Responded to scenario: {scenario}. Response: {response}",
                importance=MemoryImportance.MEDIUM,
                context={"scenario": scenario, "other_agents": [a for a in agents if a != agent]},
                related_agents=[a for a in agents if a != agent]
            )
        
        return interactions
    
    def advance_narrative(self, player_actions: List[str] = None) -> Dict[str, Any]:
        """Advance the narrative based on player actions and current state"""
        
        narrative_update = {
            "timestamp": time.time(),
            "events": [],
            "quest_updates": [],
            "agent_reactions": [],
            "state_changes": {}
        }
        
        # Process player actions if any
        if player_actions:
            for action in player_actions:
                self._process_player_action(action, narrative_update)
        
        # Check for automatic events
        if self._should_trigger_automatic_event():
            event = self.generate_dynamic_event()
            narrative_update["events"].append(event)
        
        # Update active quests
        for quest_id in self.narrative_state.active_quests[:]:
            quest = self.active_quests.get(quest_id)
            if quest:
                quest_update = self._update_quest_progress(quest)
                if quest_update:
                    narrative_update["quest_updates"].append(quest_update)
        
        # Generate agent reactions to current state
        agent_reactions = self._generate_agent_reactions()
        narrative_update["agent_reactions"] = agent_reactions
        
        # Update narrative state
        state_changes = self._update_narrative_state()
        narrative_update["state_changes"] = state_changes
        
        return narrative_update
    
    def get_narrative_summary(self) -> Dict[str, Any]:
        """Get comprehensive narrative summary"""
        
        return {
            "current_state": asdict(self.narrative_state),
            "active_quests": [asdict(quest) for quest in self.active_quests.values()],
            "recent_events": self.event_history[-10:],  # Last 10 events
            "agent_status": {
                agent: self.memory_system.get_agent_context(agent, context_size=5)
                for agent in self.agent_roles.keys()
            },
            "narrative_metrics": {
                "total_events": len(self.event_history),
                "active_quest_count": len(self.active_quests),
                "average_tension": self.narrative_state.tension_level,
                "story_complexity": self._calculate_story_complexity()
            }
        }
    
    def _analyze_narrative_context(self, trigger_context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Analyze current narrative context for event generation"""
        
        context = {
            "tension_level": self.narrative_state.tension_level,
            "active_events": len(self.narrative_state.active_events),
            "active_quests": len(self.narrative_state.active_quests),
            "tavern_atmosphere": self.narrative_state.tavern_atmosphere,
            "time_of_day": self.narrative_state.time_of_day,
            "recent_events": self.event_history[-3:] if self.event_history else []
        }
        
        if trigger_context:
            context.update(trigger_context)
        
        return context
    
    def _select_event_type(self, context: Dict[str, Any]) -> NarrativeEvent:
        """Select appropriate event type based on context"""
        
        tension = context.get("tension_level", 0)
        active_events = context.get("active_events", 0)
        
        # Weight events based on current state
        if tension < 30 and active_events < 2:
            # Low tension, introduce new elements
            return random.choice([
                NarrativeEvent.TAVERN_ENTRANCE,
                NarrativeEvent.MYSTERIOUS_STRANGER,
                NarrativeEvent.QUEST_OPPORTUNITY
            ])
        elif tension < 60:
            # Medium tension, build drama
            return random.choice([
                NarrativeEvent.RUMOR_SPREADING,
                NarrativeEvent.ALLIANCE_FORMING,
                NarrativeEvent.THREAT_DETECTED
            ])
        else:
            # High tension, climactic events
            return random.choice([
                NarrativeEvent.BRAWL_BREWING,
                NarrativeEvent.BETRAYAL_REVEALED,
                NarrativeEvent.THREAT_DETECTED
            ])
    
    def _build_event_prompt(self, event_type: NarrativeEvent, context: Dict[str, Any]) -> str:
        """Build prompt for event generation"""
        
        return f"""Generate a {event_type.value} event for a Warhammer Fantasy tavern.

Current Context:
- Tension Level: {context.get('tension_level', 0)}/100
- Atmosphere: {context.get('tavern_atmosphere', 'calm')}
- Time: {context.get('time_of_day', 'evening')}
- Active Events: {context.get('active_events', 0)}

Create an engaging event that:
1. Fits the Warhammer Fantasy setting
2. Involves tavern patrons and agents
3. Has clear consequences and opportunities
4. Advances the narrative meaningfully

Format as JSON with: title, description, participants, consequences, tension_change"""
    
    def _get_narrative_system_prompt(self) -> str:
        """Get system prompt for narrative generation"""
        
        return """You are a master storyteller for Warhammer Fantasy RPG sessions. 
        Create immersive, dark fantasy narratives that capture the gritty atmosphere of the Old World.
        Focus on political intrigue, supernatural threats, and moral ambiguity.
        Keep events grounded in tavern setting while hinting at larger conflicts."""
    
    def _load_event_templates(self) -> Dict[str, Any]:
        """Load event templates for fallback generation"""
        
        return {
            NarrativeEvent.TAVERN_ENTRANCE: {
                "title": "Mysterious Arrival",
                "description": "A hooded figure enters the tavern, drawing suspicious glances",
                "tension_change": 10
            },
            NarrativeEvent.BRAWL_BREWING: {
                "title": "Rising Tensions",
                "description": "Arguments escalate between patrons, violence seems imminent",
                "tension_change": 25
            },
            NarrativeEvent.QUEST_OPPORTUNITY: {
                "title": "Call for Heroes",
                "description": "A desperate messenger seeks brave souls for a dangerous mission",
                "tension_change": 5
            }
        }
    
    def _load_quest_templates(self) -> Dict[QuestType, Dict[str, Any]]:
        """Load quest templates"""
        
        return {
            QuestType.INVESTIGATION: {
                "title_template": "Investigate the {mystery}",
                "objectives": ["Gather clues", "Interview witnesses", "Uncover the truth"],
                "rewards": ["Information", "Gold", "Reputation"]
            },
            QuestType.RESCUE_MISSION: {
                "title_template": "Rescue {target} from {location}",
                "objectives": ["Locate target", "Plan rescue", "Execute extraction"],
                "rewards": ["Gratitude", "Reward money", "Allies"]
            }
        }

    def _parse_event_response(self, response: str, event_type: NarrativeEvent, context: Dict[str, Any]) -> Dict[str, Any]:
        """Parse LLM response into event structure"""
        try:
            import json
            event_data = json.loads(response)

            event = {
                "id": str(uuid.uuid4()),
                "type": event_type.value,
                "title": event_data.get("title", f"Unknown {event_type.value}"),
                "description": event_data.get("description", "Something happens in the tavern"),
                "participants": event_data.get("participants", []),
                "consequences": event_data.get("consequences", []),
                "tension_change": event_data.get("tension_change", 0),
                "timestamp": time.time(),
                "context": context
            }

            return event

        except (json.JSONDecodeError, KeyError):
            return self._generate_fallback_event(event_type, context)

    def _generate_fallback_event(self, event_type: NarrativeEvent, context: Dict[str, Any]) -> Dict[str, Any]:
        """Generate fallback event when LLM fails"""
        template = self.event_templates.get(event_type, {})

        return {
            "id": str(uuid.uuid4()),
            "type": event_type.value,
            "title": template.get("title", "Tavern Event"),
            "description": template.get("description", "Something interesting happens"),
            "participants": ["Karczmarz"],
            "consequences": ["Tension changes"],
            "tension_change": template.get("tension_change", 5),
            "timestamp": time.time(),
            "context": context
        }

    def _process_event(self, event: Dict[str, Any]):
        """Process event and update narrative state"""
        # Add to event history
        self.event_history.append(event)

        # Update tension
        self.narrative_state.tension_level += event.get("tension_change", 0)
        self.narrative_state.tension_level = max(0, min(100, self.narrative_state.tension_level))

        # Add to active events
        self.narrative_state.active_events.append(event["id"])

        # Update economy based on event (reputation changes)
        if hasattr(self, 'economy_system') and self.economy_system:
            try:
                reputation_changes = self.economy_system.update_reputation_on_event(event)
                event["reputation_changes"] = reputation_changes
            except Exception as e:
                print(f"Warning: Failed to update economy from event: {e}")

        # Store in agent memories
        for participant in event.get("participants", []):
            if participant in self.agent_roles:
                self.memory_system.store_memory(
                    agent_id=participant,
                    memory_type=MemoryType.EVENT,
                    content=f"Witnessed event: {event['title']}. {event['description']}",
                    importance=MemoryImportance.HIGH if event.get("tension_change", 0) > 15 else MemoryImportance.MEDIUM,
                    context=event,
                    tags=[event["type"], "event"]
                )

    def _get_agent_narrative_response(self, agent: str, scenario: str, context: Dict[str, Any], provider: LLMProvider) -> str:
        """Get narrative response from agent using specified LLM provider"""
        agent_role = self.agent_roles.get(agent, {})

        request = LLMRequest(
            prompt=f"Scenario: {scenario}\n\nHow do you respond as {agent}?",
            system_message=f"You are {agent}, a {agent_role.get('primary_role', 'tavern character')} in a Warhammer Fantasy tavern. Your capabilities include: {', '.join(agent_role.get('capabilities', []))}. Respond in character.",
            agent_name=agent,
            provider=provider,
            max_tokens=300,
            temperature=0.8,
            context=context
        )

        response = self.llm_service.call_llm(request)
        return response.content if response.success else f"{agent} observes the situation carefully."

    def _get_agent_quick_response(self, agent: str, scenario: str, context: Dict[str, Any]) -> str:
        """Get quick response from agent using Cerebras"""
        cerebras_request = CerebrasRequest(
            response_type=ResponseType.REAL_TIME_REACTION,
            context=scenario,
            character_name=agent,
            max_words=25,
            urgency_level=8
        )

        return self.cerebras_service.generate_real_time_reaction(cerebras_request)

    def _should_trigger_automatic_event(self) -> bool:
        """Determine if an automatic event should be triggered"""
        # Base probability of 20%, modified by current state
        base_probability = 0.2

        # Increase probability if tension is low (story needs drama)
        if self.narrative_state.tension_level < 30:
            base_probability += 0.1

        # Decrease probability if too many active events
        if len(self.narrative_state.active_events) > 3:
            base_probability -= 0.15

        # Check economy system for reputation-based events
        if hasattr(self, 'economy_system') and self.economy_system:
            tavern_reputation = self.economy_system.economic_state.reputation_score

            # Force event if reputation is very low
            if tavern_reputation < 25:
                base_probability += 0.4  # High chance of crisis events
            elif tavern_reputation < 50:
                base_probability += 0.2  # Moderate chance of problems
            elif tavern_reputation > 80:
                base_probability += 0.1  # Good reputation attracts events

        return random.random() < base_probability

    def get_faction_agents(self, faction: str) -> List[str]:
        """Get all agents belonging to a specific faction"""
        return self.faction_crews.get(faction, [])

    def coordinate_faction_response(self, faction: str, event: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Coordinate response from all agents in a faction"""
        faction_agents = self.get_faction_agents(faction)
        responses = []

        for agent in faction_agents:
            if agent in self.agent_roles:
                agent_context = self.memory_system.get_agent_context(agent)
                response = self._get_agent_quick_response(
                    agent,
                    f"Faction {faction} responds to: {event.get('title', 'Unknown Event')}",
                    agent_context
                )
                responses.append({
                    "agent": agent,
                    "faction": faction,
                    "response": response,
                    "timestamp": time.time()
                })

        return responses

    def get_agent_count_by_faction(self) -> Dict[str, int]:
        """Get count of agents per faction"""
        return {faction: len(agents) for faction, agents in self.faction_crews.items()}

    def get_total_agent_count(self) -> int:
        """Get total number of agents"""
        return len(self.agent_roles)

    def _generate_agent_reactions(self) -> List[Dict[str, Any]]:
        """Generate reactions from agents to current narrative state"""
        reactions = []

        for agent in self.agent_roles.keys():
            # Get recent memories to inform reaction
            recent_memories = self.memory_system.retrieve_memories(
                agent,
                importance_threshold=MemoryImportance.MEDIUM,
                limit=3
            )

            if recent_memories:
                # Generate reaction based on recent events
                memory_context = "; ".join([m.content for m in recent_memories[-2:]])
                reaction = self._get_agent_quick_response(
                    agent,
                    f"Recent events: {memory_context}",
                    {"recent_memories": [m.content for m in recent_memories]}
                )

                reactions.append({
                    "agent": agent,
                    "reaction": reaction,
                    "timestamp": time.time(),
                    "trigger": "narrative_state_update"
                })

        return reactions

    def _update_narrative_state(self) -> Dict[str, Any]:
        """Update narrative state and return changes"""
        changes = {}

        # Update atmosphere based on tension
        old_atmosphere = self.narrative_state.tavern_atmosphere

        if self.narrative_state.tension_level < 25:
            self.narrative_state.tavern_atmosphere = "calm"
        elif self.narrative_state.tension_level < 50:
            self.narrative_state.tavern_atmosphere = "tense"
        elif self.narrative_state.tension_level < 75:
            self.narrative_state.tavern_atmosphere = "hostile"
        else:
            self.narrative_state.tavern_atmosphere = "explosive"

        if old_atmosphere != self.narrative_state.tavern_atmosphere:
            changes["atmosphere"] = {
                "from": old_atmosphere,
                "to": self.narrative_state.tavern_atmosphere
            }

        # Clean up old events (keep last 10)
        if len(self.narrative_state.active_events) > 10:
            removed_events = self.narrative_state.active_events[:-10]
            self.narrative_state.active_events = self.narrative_state.active_events[-10:]
            changes["events_cleaned"] = len(removed_events)

        return changes

    def _calculate_story_complexity(self) -> float:
        """Calculate current story complexity score"""
        complexity = 0.0

        # Base complexity from active elements
        complexity += len(self.narrative_state.active_events) * 0.1
        complexity += len(self.narrative_state.active_quests) * 0.2
        complexity += self.narrative_state.tension_level * 0.01

        # Relationship complexity
        total_relationships = sum(
            len(relationships)
            for relationships in self.narrative_state.character_relationships.values()
        )
        complexity += total_relationships * 0.05

        return min(complexity, 10.0)  # Cap at 10.0

    def _select_quest_type(self) -> QuestType:
        """Select appropriate quest type based on narrative state"""
        # Weight quest types based on current tension and atmosphere
        if self.narrative_state.tension_level < 30:
            return random.choice([QuestType.INVESTIGATION, QuestType.DIPLOMATIC_MISSION])
        elif self.narrative_state.tension_level < 60:
            return random.choice([QuestType.RESCUE_MISSION, QuestType.TREASURE_HUNT])
        else:
            return random.choice([QuestType.COMBAT_CHALLENGE, QuestType.MYSTICAL_RITUAL])

    def _calculate_quest_difficulty(self) -> int:
        """Calculate appropriate quest difficulty"""
        base_difficulty = 3

        # Increase difficulty with tension
        tension_modifier = self.narrative_state.tension_level // 20

        # Increase difficulty with active quests (players are experienced)
        quest_modifier = len(self.active_quests) // 2

        difficulty = base_difficulty + tension_modifier + quest_modifier
        return max(1, min(10, difficulty))

    def _build_quest_prompt(self, quest_type: QuestType, difficulty: int) -> str:
        """Build prompt for quest generation"""
        return f"""Generate a {quest_type.value} quest for a Warhammer Fantasy tavern setting.

Quest Requirements:
- Type: {quest_type.value}
- Difficulty: {difficulty}/10
- Setting: Tavern and surrounding area
- Atmosphere: {self.narrative_state.tavern_atmosphere}
- Current Tension: {self.narrative_state.tension_level}/100

Create a quest that:
1. Fits the dark fantasy Warhammer setting
2. Has clear objectives and rewards
3. Involves tavern agents appropriately
4. Scales to the specified difficulty

Format as JSON with: title, description, objectives (array), rewards (array), required_agents (array), time_limit (minutes)"""

    def _get_quest_system_prompt(self) -> str:
        """Get system prompt for quest generation"""
        return """You are a Warhammer Fantasy RPG quest master. Create engaging quests that capture the dark, gritty atmosphere of the Old World. Focus on moral ambiguity, political intrigue, and supernatural threats. Quests should be challenging but achievable."""

    def _parse_quest_response(self, response: str, quest_type: QuestType, difficulty: int) -> Quest:
        """Parse LLM response into quest structure"""
        try:
            import json
            quest_data = json.loads(response)

            quest = Quest(
                id=str(uuid.uuid4()),
                quest_type=quest_type,
                title=quest_data.get("title", f"Unknown {quest_type.value}"),
                description=quest_data.get("description", "A mysterious quest awaits"),
                objectives=quest_data.get("objectives", ["Complete the task"]),
                rewards=quest_data.get("rewards", ["Experience"]),
                difficulty=difficulty,
                time_limit=quest_data.get("time_limit"),
                required_agents=quest_data.get("required_agents", [])
            )

            return quest

        except (json.JSONDecodeError, KeyError):
            return self._generate_fallback_quest(quest_type, difficulty)

    def _generate_fallback_quest(self, quest_type: QuestType, difficulty: int) -> Quest:
        """Generate fallback quest when LLM fails"""
        template = self.quest_templates.get(quest_type, {})

        return Quest(
            id=str(uuid.uuid4()),
            quest_type=quest_type,
            title=template.get("title_template", f"Unknown {quest_type.value}").format(
                mystery="strange disappearance",
                target="missing merchant",
                location="nearby ruins"
            ),
            description=f"A {quest_type.value} quest of difficulty {difficulty}",
            objectives=template.get("objectives", ["Complete the objective"]),
            rewards=template.get("rewards", ["Gold", "Experience"]),
            difficulty=difficulty,
            required_agents=["Karczmarz"]
        )

    def _process_player_action(self, action: str, narrative_update: Dict[str, Any]):
        """Process a player action and update narrative"""
        # Store player action in memory
        self.memory_system.store_memory(
            agent_id="Player",
            memory_type=MemoryType.INTERACTION,
            content=f"Player action: {action}",
            importance=MemoryImportance.HIGH,
            context={"action_type": "player_action"},
            tags=["player", "action"]
        )

        # Modify tension based on action type
        tension_changes = {
            "investigate": 5,
            "challenge": 15,
            "negotiate": -5,
            "attack": 25,
            "retreat": -10
        }

        for keyword, change in tension_changes.items():
            if keyword in action.lower():
                self.narrative_state.tension_level += change
                break

    def _update_quest_progress(self, quest: Quest) -> Optional[Dict[str, Any]]:
        """Update quest progress and return changes if any"""
        if quest.status != "active":
            return None

        # Simple progress simulation - in real implementation, this would be more complex
        if random.random() < 0.3:  # 30% chance of progress
            progress_update = {
                "quest_id": quest.id,
                "title": quest.title,
                "progress_type": "objective_completed",
                "description": f"Progress made on {quest.title}",
                "timestamp": time.time()
            }

            # Update quest progress
            completed_objectives = quest.progress.get("completed_objectives", 0)
            quest.progress["completed_objectives"] = completed_objectives + 1

            # Check if quest is complete
            if quest.progress["completed_objectives"] >= len(quest.objectives):
                quest.status = "completed"
                progress_update["progress_type"] = "quest_completed"

                # Remove from active quests
                if quest.id in self.narrative_state.active_quests:
                    self.narrative_state.active_quests.remove(quest.id)

            return progress_update

        return None

# Global narrative engine instance
narrative_engine = NarrativeEngine()
