"""
Specialized Cerebras API service for fast dialogues, rumors, and real-time responses
Optimized for speed and quick interactions in the tavern simulator
"""

import time
import random
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from enum import Enum

from .llm_service import LLMService, LLMRequest, LLMProvider

class ResponseType(Enum):
    QUICK_DIALOGUE = "quick_dialogue"
    RUMOR_GENERATION = "rumor_generation"
    REAL_TIME_REACTION = "real_time_reaction"
    TAVERN_BANTER = "tavern_banter"
    THREAT_ASSESSMENT = "threat_assessment"

@dataclass
class CerebrasRequest:
    """Specialized request structure for Cerebras API"""
    response_type: ResponseType
    context: str
    character_name: str
    character_personality: str = ""
    urgency_level: int = 5  # 1-10, higher = more urgent/faster response needed
    max_words: int = 50  # Keep responses short for speed
    emotional_state: str = "neutral"
    target_audience: str = "tavern_patrons"

class CerebrasService:
    """Specialized service for Cerebras API optimized for tavern interactions"""
    
    def __init__(self):
        self.llm_service = LLMService()
        self.response_cache = {}  # Cache for common responses
        self.personality_templates = self._load_personality_templates()
        self.rumor_templates = self._load_rumor_templates()
    
    def generate_quick_dialogue(self, request: CerebrasRequest) -> str:
        """Generate quick dialogue response optimized for speed"""
        # Check cache first for common responses
        cache_key = f"{request.character_name}_{request.response_type.value}_{hash(request.context[:50])}"
        if cache_key in self.response_cache:
            return self.response_cache[cache_key]
        
        # Prepare optimized prompt for Cerebras
        system_prompt = self._build_dialogue_system_prompt(request)
        user_prompt = self._build_dialogue_user_prompt(request)
        
        llm_request = LLMRequest(
            prompt=user_prompt,
            system_message=system_prompt,
            agent_name=request.character_name,
            provider=LLMProvider.CEREBRAS,
            max_tokens=min(request.max_words * 2, 150),  # Rough token estimation
            temperature=0.8 + (request.urgency_level * 0.02)  # Higher urgency = more creative
        )
        
        response = self.llm_service.call_llm(llm_request)
        
        if response.success:
            # Cache successful responses
            self.response_cache[cache_key] = response.content
            return response.content
        else:
            # Fallback to template-based response
            return self._generate_fallback_dialogue(request)
    
    def generate_rumor(self, request: CerebrasRequest) -> str:
        """Generate tavern rumors quickly"""
        request.response_type = ResponseType.RUMOR_GENERATION
        
        system_prompt = f"""You are {request.character_name} in a Warhammer Fantasy tavern. 
        Generate a short, intriguing rumor (max {request.max_words} words). 
        Make it mysterious and fitting for the dark fantasy setting."""
        
        user_prompt = f"Context: {request.context}\nGenerate a rumor about this situation:"
        
        llm_request = LLMRequest(
            prompt=user_prompt,
            system_message=system_prompt,
            agent_name=request.character_name,
            provider=LLMProvider.CEREBRAS,
            max_tokens=100,
            temperature=0.9  # High creativity for rumors
        )
        
        response = self.llm_service.call_llm(llm_request)
        
        if response.success:
            return response.content
        else:
            return self._generate_fallback_rumor(request)
    
    def generate_real_time_reaction(self, request: CerebrasRequest) -> str:
        """Generate immediate reactions to events"""
        request.response_type = ResponseType.REAL_TIME_REACTION
        
        # Ultra-fast prompt for immediate reactions
        system_prompt = f"{request.character_name}: React immediately in {request.max_words} words or less. {request.character_personality}"
        user_prompt = f"URGENT: {request.context} - Your instant reaction:"
        
        llm_request = LLMRequest(
            prompt=user_prompt,
            system_message=system_prompt,
            agent_name=request.character_name,
            provider=LLMProvider.CEREBRAS,
            max_tokens=75,  # Very short for speed
            temperature=0.7
        )
        
        response = self.llm_service.call_llm(llm_request)
        
        if response.success:
            return response.content
        else:
            return self._generate_fallback_reaction(request)
    
    def generate_tavern_banter(self, participants: List[str], topic: str) -> List[str]:
        """Generate quick back-and-forth banter between characters"""
        banter_responses = []
        
        for i, character in enumerate(participants):
            request = CerebrasRequest(
                response_type=ResponseType.TAVERN_BANTER,
                context=f"Topic: {topic}. Previous responses: {' '.join(banter_responses[-2:])}",
                character_name=character,
                max_words=20,  # Very short for banter
                urgency_level=8  # High urgency for natural flow
            )
            
            response = self.generate_quick_dialogue(request)
            banter_responses.append(f"{character}: {response}")
        
        return banter_responses
    
    def assess_threat_quickly(self, threat_description: str, assessor: str) -> Dict[str, Any]:
        """Quick threat assessment for security purposes"""
        request = CerebrasRequest(
            response_type=ResponseType.THREAT_ASSESSMENT,
            context=threat_description,
            character_name=assessor,
            max_words=30,
            urgency_level=10  # Maximum urgency
        )
        
        system_prompt = f"You are {assessor}. Assess this threat in {request.max_words} words: threat level (1-10), immediate action needed."
        
        llm_request = LLMRequest(
            prompt=f"THREAT: {threat_description}\nQuick assessment:",
            system_message=system_prompt,
            agent_name=assessor,
            provider=LLMProvider.CEREBRAS,
            max_tokens=60,
            temperature=0.3  # Low temperature for consistent threat assessment
        )
        
        response = self.llm_service.call_llm(llm_request)
        
        if response.success:
            # Try to extract threat level from response
            threat_level = self._extract_threat_level(response.content)
            return {
                "assessment": response.content,
                "threat_level": threat_level,
                "assessor": assessor,
                "response_time": response.response_time
            }
        else:
            return {
                "assessment": "Unable to assess threat quickly. Recommend caution.",
                "threat_level": 5,  # Default medium threat
                "assessor": assessor,
                "response_time": 0.0
            }
    
    def _build_dialogue_system_prompt(self, request: CerebrasRequest) -> str:
        """Build optimized system prompt for dialogue"""
        personality = self.personality_templates.get(request.character_name, request.character_personality)
        
        return f"""You are {request.character_name} in a Warhammer Fantasy tavern.
        Personality: {personality}
        Emotional state: {request.emotional_state}
        Respond in {request.max_words} words or less. Be authentic and quick."""
    
    def _build_dialogue_user_prompt(self, request: CerebrasRequest) -> str:
        """Build optimized user prompt for dialogue"""
        return f"Situation: {request.context}\nYour quick response to {request.target_audience}:"
    
    def _generate_fallback_dialogue(self, request: CerebrasRequest) -> str:
        """Generate fallback dialogue when API fails"""
        fallbacks = {
            "Karczmarz": ["*wipes bar nervously*", "*glances around cautiously*", "*mutters under breath*"],
            "Skrytobójca": ["*stays in shadows*", "*watches silently*", "*hand moves to weapon*"],
            "Wiedźma": ["*eyes glow mysteriously*", "*whispers incantation*", "*senses disturbance*"],
            "Zwiadowca": ["*scans the room*", "*reports quietly*", "*stays alert*"],
            "Czempion": ["*grins menacingly*", "*chaos stirs within*", "*seeks opportunity*"]
        }
        
        character_fallbacks = fallbacks.get(request.character_name, ["*reacts cautiously*"])
        return random.choice(character_fallbacks)
    
    def _generate_fallback_rumor(self, request: CerebrasRequest) -> str:
        """Generate fallback rumor when API fails"""
        rumor_starters = [
            "I heard whispers that...",
            "Word from the road is...",
            "The merchants speak of...",
            "Strange tales tell of...",
            "Dark rumors suggest..."
        ]
        
        rumor_topics = [
            "shadowy figures in the night",
            "ancient evils stirring",
            "treasure hidden nearby",
            "political intrigue brewing",
            "mysterious disappearances"
        ]
        
        return f"{random.choice(rumor_starters)} {random.choice(rumor_topics)}."
    
    def _generate_fallback_reaction(self, request: CerebrasRequest) -> str:
        """Generate fallback reaction when API fails"""
        reactions = [
            "What in Sigmar's name?!",
            "*draws weapon instinctively*",
            "By the gods...",
            "*steps back cautiously*",
            "This bodes ill..."
        ]
        
        return random.choice(reactions)
    
    def _extract_threat_level(self, assessment_text: str) -> int:
        """Extract numerical threat level from assessment text"""
        import re
        
        # Look for patterns like "threat level 7", "level: 8", "8/10", etc.
        patterns = [
            r'threat level[:\s]*(\d+)',
            r'level[:\s]*(\d+)',
            r'(\d+)/10',
            r'danger[:\s]*(\d+)',
            r'risk[:\s]*(\d+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, assessment_text.lower())
            if match:
                level = int(match.group(1))
                return min(max(level, 1), 10)  # Clamp between 1-10
        
        # Default to medium threat if no level found
        return 5
    
    def _load_personality_templates(self) -> Dict[str, str]:
        """Load personality templates for characters"""
        return {
            "Karczmarz": "Cautious tavern keeper, protective of establishment and patrons",
            "Skrytobójca": "Silent shadow agent, observant and deadly when needed",
            "Wiedźma": "Mystical oracle with otherworldly knowledge and cryptic speech",
            "Zwiadowca": "Alert scout, always watching for threats and opportunities",
            "Czempion": "Chaos champion seeking to spread discord and corruption"
        }
    
    def _load_rumor_templates(self) -> List[str]:
        """Load rumor templates for quick generation"""
        return [
            "Strange lights seen in the forest",
            "Merchant caravan went missing",
            "Chaos cultists gathering nearby",
            "Ancient tomb discovered",
            "Noble family in political trouble",
            "Bandits planning major heist",
            "Witch hunter investigating locals",
            "Mysterious plague spreading",
            "Dragon sighted in mountains",
            "Undead rising from graveyards"
        ]
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Get performance statistics for Cerebras service"""
        return {
            "cache_size": len(self.response_cache),
            "llm_stats": self.llm_service.get_provider_stats().get("cerebras", {}),
            "avg_response_time": self.llm_service.provider_stats[LLMProvider.CEREBRAS]["avg_response_time"]
        }

# Global Cerebras service instance
cerebras_service = CerebrasService()
