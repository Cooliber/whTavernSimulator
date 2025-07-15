"""
Configuration file for Warhammer Fantasy Tavern Simulator
Contains API keys, settings, and global constants
"""

import os
from dataclasses import dataclass
from typing import Dict, List
from dotenv import load_dotenv

# Load environment variables at module import
load_dotenv()

@dataclass
class APIConfig:
    """API configuration for LLM providers"""
    groq_api_key: str = os.getenv("groq_api_key", "")  # Using the correct env var name
    groq_base_url: str = "https://api.groq.com/openai/v1"

    cerebras_api_key: str = os.getenv("Cerebras_api", "")  # Using the correct env var name
    cerebras_base_url: str = "https://api.cerebras.ai/v1"

    # Fallback to OpenAI if others unavailable
    openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
    openai_base_url: str = "https://api.openai.com/v1"

@dataclass
class TavernConfig:
    """Tavern simulation configuration"""
    max_characters: int = 20
    max_tension: int = 100
    brawl_threshold: int = 80
    rumor_spread_chance: float = 0.3
    auto_event_chance: float = 0.25
    
    # Animation settings
    animation_fps: int = 60
    particle_count: int = 30
    max_particles: int = 100

@dataclass
class AgentConfig:
    """Multi-agent system configuration"""
    max_agents: int = 5
    memory_retention_turns: int = 50
    reasoning_trace_length: int = 10
    
    # Agent personalities
    agent_personalities: Dict[str, Dict] = None
    
    def __post_init__(self):
        if self.agent_personalities is None:
            self.agent_personalities = {
                "Karczmarz": {
                    "role": "Tavern Keeper",
                    "personality": "Wise, observant, protective of patrons",
                    "goals": ["Maintain order", "Protect reputation", "Gather information"],
                    "preferred_llm": "grok",  # Complex reasoning for management
                    "response_style": "thoughtful"
                },
                "Skrytobójca": {
                    "role": "Shadow Agent",
                    "personality": "Mysterious, calculating, information broker",
                    "goals": ["Gather secrets", "Monitor threats", "Execute contracts"],
                    "preferred_llm": "cerebras",  # Fast responses for stealth
                    "response_style": "cryptic"
                },
                "Wiedźma": {
                    "role": "Mystic Oracle",
                    "personality": "Mystical, prophetic, sees hidden connections",
                    "goals": ["Divine future", "Interpret omens", "Guide fate"],
                    "preferred_llm": "grok",  # Complex narrative generation
                    "response_style": "mystical"
                },
                "Zwiadowca": {
                    "role": "Information Gatherer",
                    "personality": "Alert, curious, well-traveled",
                    "goals": ["Report news", "Track movements", "Warn of dangers"],
                    "preferred_llm": "cerebras",  # Quick information processing
                    "response_style": "direct"
                },
                "Czempion": {
                    "role": "Chaos Champion",
                    "personality": "Aggressive, unpredictable, seeks conflict",
                    "goals": ["Spread chaos", "Challenge order", "Corrupt others"],
                    "preferred_llm": "grok",  # Complex corruption strategies
                    "response_style": "menacing"
                }
            }

@dataclass
class UIConfig:
    """UI and GSAP animation configuration"""
    # GSAP settings
    gsap_cdn_version: str = "3.12.5"
    animation_duration_base: float = 1.0
    stagger_amount: float = 0.1
    
    # Color schemes
    faction_colors: Dict[str, str] = None
    
    # Layout settings
    sidebar_width: int = 300
    main_content_height: int = 800
    agent_box_height: int = 150
    
    def __post_init__(self):
        if self.faction_colors is None:
            self.faction_colors = {
                "empire": "#ffd700",
                "dwarf": "#8b4513", 
                "highelf": "#87ceeb",
                "woodelf": "#228b22",
                "bretonnian": "#4169e1",
                "halfling": "#daa520",
                "tilean": "#800080",
                "kislev": "#e0ffff",
                "norse": "#696969",
                "arabyan": "#ffd700",
                "cathayan": "#dc143c",
                "nipponese": "#ff69b4",
                "witchhunter": "#f5f5f5",
                "cultist": "#8b0000"
            }

@dataclass
class GameConfig:
    """Game mechanics configuration"""
    # Economy
    base_ale_price: int = 2
    base_wine_price: int = 5
    base_food_price: int = 3
    base_room_price: int = 10
    
    # Reputation effects
    reputation_brawl_penalty: int = -10
    reputation_good_service_bonus: int = 5
    reputation_rumor_spread_modifier: float = 0.1
    
    # Quest system
    max_active_quests: int = 3
    quest_completion_reputation: int = 20
    quest_failure_penalty: int = -15

# Global configuration instances
api_config = APIConfig()
tavern_config = TavernConfig()
agent_config = AgentConfig()
ui_config = UIConfig()
game_config = GameConfig()

# Validation
def validate_config():
    """Validate configuration settings"""
    errors = []
    
    if not api_config.groq_api_key and not api_config.openai_api_key:
        errors.append("No LLM API key configured")
    
    if tavern_config.max_characters <= 0:
        errors.append("Max characters must be positive")
    
    if agent_config.max_agents <= 0:
        errors.append("Max agents must be positive")
    
    return errors

# Export commonly used values
GSAP_CDN_BASE = f"https://cdnjs.cloudflare.com/ajax/libs/gsap/{ui_config.gsap_cdn_version}"
REQUIRED_GSAP_PLUGINS = [
    "gsap.min.js",
    "ScrollTrigger.min.js",
    "TextPlugin.min.js", 
    "MorphSVGPlugin.min.js",
    "DrawSVGPlugin.min.js",
    "PixiPlugin.min.js",
    "Flip.min.js",
    "CustomEase.min.js"
]
