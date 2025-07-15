"""
Base Agent class for Warhammer Fantasy Tavern Simulator
Provides foundation for all AI agents with LLM integration
"""

import json
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from datetime import datetime

from config import agent_config, api_config

@dataclass
class AgentMemory:
    """Memory structure for agents"""
    short_term: List[str] = field(default_factory=list)  # Last 10 interactions
    long_term: Dict[str, Any] = field(default_factory=dict)  # Persistent knowledge
    reasoning_trace: List[str] = field(default_factory=list)  # Decision process
    emotions: Dict[str, float] = field(default_factory=dict)  # Current emotional state
    relationships: Dict[str, float] = field(default_factory=dict)  # Agent relationships

@dataclass
class AgentAction:
    """Represents an action taken by an agent"""
    action_type: str
    target: Optional[str] = None
    parameters: Dict[str, Any] = field(default_factory=dict)
    reasoning: str = ""
    confidence: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

class BaseAgent(ABC):
    """Base class for all tavern agents"""
    
    def __init__(self, name: str, role: str, personality: str):
        self.name = name
        self.role = role
        self.personality = personality
        self.memory = AgentMemory()
        self.active = True
        self.last_action_time = datetime.now()
        
        # Get configuration
        self.config = agent_config.agent_personalities.get(name, {})
        self.preferred_llm = self.config.get("preferred_llm", "grok")
        self.goals = self.config.get("goals", [])
        self.response_style = self.config.get("response_style", "neutral")
        
        # Initialize emotions
        self.memory.emotions = {
            "alertness": 0.5,
            "suspicion": 0.3,
            "satisfaction": 0.6,
            "aggression": 0.2,
            "curiosity": 0.7
        }
    
    @abstractmethod
    def perceive(self, tavern_state: Dict[str, Any]) -> List[str]:
        """Perceive current tavern state and extract relevant information"""
        pass
    
    @abstractmethod
    def decide(self, perceptions: List[str]) -> Optional[AgentAction]:
        """Decide on action based on perceptions and goals"""
        pass
    
    @abstractmethod
    def act(self, action: AgentAction, tavern_state: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the decided action and return results"""
        pass
    
    def update_memory(self, event: str, event_type: str = "observation"):
        """Update agent memory with new information"""
        # Add to short-term memory
        self.memory.short_term.append(f"[{datetime.now().strftime('%H:%M')}] {event}")
        
        # Keep only recent memories
        if len(self.memory.short_term) > agent_config.memory_retention_turns:
            self.memory.short_term.pop(0)
        
        # Update long-term memory for important events
        if event_type in ["important", "relationship", "threat"]:
            timestamp = datetime.now().isoformat()
            if event_type not in self.memory.long_term:
                self.memory.long_term[event_type] = []
            self.memory.long_term[event_type].append({
                "event": event,
                "timestamp": timestamp
            })
    
    def add_reasoning_step(self, step: str):
        """Add a step to the reasoning trace"""
        self.memory.reasoning_trace.append(f"[{datetime.now().strftime('%H:%M:%S')}] {step}")
        
        # Keep trace manageable
        if len(self.memory.reasoning_trace) > agent_config.reasoning_trace_length:
            self.memory.reasoning_trace.pop(0)
    
    def update_emotion(self, emotion: str, change: float):
        """Update emotional state"""
        if emotion in self.memory.emotions:
            self.memory.emotions[emotion] = max(0.0, min(1.0, 
                self.memory.emotions[emotion] + change))
    
    def get_emotional_state(self) -> str:
        """Get current dominant emotion"""
        if not self.memory.emotions:
            return "neutral"
        
        dominant_emotion = max(self.memory.emotions.items(), key=lambda x: x[1])
        return dominant_emotion[0]
    
    def get_emotion_emoji(self) -> str:
        """Get emoji representing current emotional state"""
        emotion_emojis = {
            "alertness": "👁️",
            "suspicion": "🤔", 
            "satisfaction": "😊",
            "aggression": "😠",
            "curiosity": "🧐",
            "fear": "😨",
            "anger": "😡",
            "joy": "😄",
            "sadness": "😢"
        }
        
        dominant_emotion = self.get_emotional_state()
        return emotion_emojis.get(dominant_emotion, "😐")
    
    def can_act(self) -> bool:
        """Check if agent can take action (cooldown, etc.)"""
        time_since_last = datetime.now() - self.last_action_time
        return self.active and time_since_last.total_seconds() > 1.0  # 1 second cooldown
    
    def get_context_for_llm(self) -> str:
        """Prepare context for LLM calls"""
        context = f"""
Agent: {self.name} ({self.role})
Personality: {self.personality}
Goals: {', '.join(self.goals)}
Current Emotion: {self.get_emotional_state()}

Recent Memories:
{chr(10).join(self.memory.short_term[-5:])}

Current Reasoning:
{chr(10).join(self.memory.reasoning_trace[-3:])}
"""
        return context
    
    def call_llm(self, prompt: str, system_message: str = "", task_type: str = "general") -> str:
        """Call appropriate LLM with intelligent auto-selection"""
        try:
            # Auto-select LLM based on task complexity and agent preferences
            selected_provider = self._select_optimal_llm(prompt, task_type)

            # Use LLM service for actual API calls
            from services.llm_service import llm_service, LLMRequest, LLMProvider

            # Map provider names to enum values
            provider_map = {
                "grok": LLMProvider.GROK,
                "cerebras": LLMProvider.CEREBRAS,
                "openai": LLMProvider.OPENAI,
                "mock": LLMProvider.MOCK
            }

            provider = provider_map.get(selected_provider, LLMProvider.MOCK)

            # Create LLM request
            request = LLMRequest(
                prompt=prompt,
                system_message=system_message or self._get_system_message(),
                provider=provider,
                max_tokens=self._get_max_tokens_for_task(task_type),
                temperature=self._get_temperature_for_task(task_type)
            )

            # Call LLM service
            response = llm_service.call_llm(request)

            if response.success:
                return response.content
            else:
                return self._mock_llm_response(prompt, task_type)

        except Exception as e:
            print(f"LLM call failed for {self.name}: {e}")
            return self._mock_llm_response(prompt, task_type)

    def _select_optimal_llm(self, prompt: str, task_type: str) -> str:
        """Intelligently select LLM based on task complexity and requirements"""
        # Analyze prompt complexity
        complexity_score = self._analyze_prompt_complexity(prompt)

        # Task-specific LLM selection rules
        if task_type in ["complex_reasoning", "strategic_planning", "narrative_generation"]:
            # Complex tasks prefer Grok
            if api_config.grok_api_key:
                return "grok"
        elif task_type in ["quick_response", "simple_action", "status_update"]:
            # Fast tasks prefer Cerebras
            if api_config.cerebras_api_key:
                return "cerebras"

        # Fallback to agent preference
        if self.preferred_llm == "grok" and api_config.grok_api_key:
            return "grok"
        elif self.preferred_llm == "cerebras" and api_config.cerebras_api_key:
            return "cerebras"
        elif api_config.openai_api_key:
            return "openai"
        else:
            return "mock"

    def _analyze_prompt_complexity(self, prompt: str) -> float:
        """Analyze prompt complexity to help with LLM selection"""
        complexity_indicators = [
            "strategy", "plan", "analyze", "complex", "reasoning", "decision",
            "evaluate", "consider", "weigh", "implications", "consequences"
        ]

        simple_indicators = [
            "quick", "fast", "simple", "immediate", "now", "status", "update"
        ]

        prompt_lower = prompt.lower()
        complexity_score = 0.5  # Base score

        for indicator in complexity_indicators:
            if indicator in prompt_lower:
                complexity_score += 0.1

        for indicator in simple_indicators:
            if indicator in prompt_lower:
                complexity_score -= 0.1

        # Length also indicates complexity
        if len(prompt) > 200:
            complexity_score += 0.2
        elif len(prompt) < 50:
            complexity_score -= 0.1

        return max(0.0, min(1.0, complexity_score))

    def _get_max_tokens_for_task(self, task_type: str) -> int:
        """Get appropriate token limit for task type"""
        token_limits = {
            "complex_reasoning": 500,
            "strategic_planning": 400,
            "narrative_generation": 300,
            "quick_response": 150,
            "simple_action": 100,
            "status_update": 50,
            "general": 200
        }
        return token_limits.get(task_type, 200)

    def _get_temperature_for_task(self, task_type: str) -> float:
        """Get appropriate temperature for task type"""
        temperatures = {
            "complex_reasoning": 0.7,
            "strategic_planning": 0.6,
            "narrative_generation": 0.8,
            "quick_response": 0.3,
            "simple_action": 0.2,
            "status_update": 0.1,
            "general": 0.5
        }
        return temperatures.get(task_type, 0.5)

    def _get_system_message(self) -> str:
        """Get agent-specific system message"""
        return f"You are {self.name}, a {self.role} in a Warhammer Fantasy tavern. {self.personality}"
    
    def _call_grok(self, prompt: str, system_message: str = "") -> str:
        """Call Grok API for complex reasoning"""
        # TODO: Implement actual Grok API call
        # For now, return mock response
        return f"[GROK] {self.name} analyzes: {prompt[:50]}..."
    
    def _call_cerebras(self, prompt: str, system_message: str = "") -> str:
        """Call Cerebras API for fast responses"""
        # TODO: Implement actual Cerebras API call
        # For now, return mock response
        return f"[CEREBRAS] {self.name} responds: {prompt[:30]}..."
    
    def _mock_llm_response(self, prompt: str, task_type: str = "general") -> str:
        """Enhanced mock LLM response for testing with task-aware responses"""
        # Task-specific response templates
        task_responses = {
            "complex_reasoning": {
                "Karczmarz": "After careful analysis, I believe the best approach is to maintain order while gathering more information about the underlying tensions.",
                "Skrytobójca": "My calculations suggest multiple variables at play. The shadows reveal patterns others cannot see.",
                "Wiedźma": "The ethereal currents speak of deeper mysteries. This situation requires mystical insight beyond mortal understanding.",
                "Zwiadowca": "Based on my extensive travels and observations, I recommend a strategic approach considering all regional factors.",
                "Czempion": "The dark gods whisper of opportunities for corruption. This complexity serves chaos well."
            },
            "quick_response": {
                "Karczmarz": "Immediate action required.",
                "Skrytobójca": "Moving to position.",
                "Wiedźma": "The signs are clear.",
                "Zwiadowca": "Threat detected.",
                "Czempion": "Chaos calls."
            },
            "general": {
                "Karczmarz": "I observe the tavern carefully and consider the best course of action.",
                "Skrytobójca": "I remain in the shadows, gathering information silently.",
                "Wiedźma": "The mystical energies reveal hidden truths about this situation.",
                "Zwiadowca": "I report what I've seen and heard from my travels.",
                "Czempion": "Chaos stirs within me, seeking opportunities for discord."
            }
        }

        # Select appropriate response set
        response_set = task_responses.get(task_type, task_responses["general"])
        return response_set.get(self.name, "I contemplate the situation before me.")
    
    def to_dict(self) -> Dict[str, Any]:
        """Serialize agent state"""
        return {
            "name": self.name,
            "role": self.role,
            "personality": self.personality,
            "active": self.active,
            "emotions": self.memory.emotions,
            "recent_memories": self.memory.short_term[-5:],
            "reasoning_trace": self.memory.reasoning_trace[-3:],
            "last_action": self.last_action_time.isoformat()
        }
    
    def get_status_summary(self) -> str:
        """Get brief status for UI display"""
        emotion = self.get_emotional_state()
        recent_action = self.memory.reasoning_trace[-1] if self.memory.reasoning_trace else "Observing..."
        return f"{emotion.title()} | {recent_action[:50]}..."
