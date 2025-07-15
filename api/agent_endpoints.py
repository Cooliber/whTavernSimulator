"""
Extended API endpoints for 17-agent system management
Provides detailed control over individual agents and their interactions
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel, Field
from typing import Dict, List, Any, Optional
from datetime import datetime
import logging

from agents.base_agent import AgentAction
from services.agent_manager import AgentManager

logger = logging.getLogger(__name__)

# Create router for agent endpoints
router = APIRouter(prefix="/api/agents", tags=["agents"])

# Pydantic models
class AgentActionRequest(BaseModel):
    action_type: str
    target: Optional[str] = None
    parameters: Dict[str, Any] = Field(default_factory=dict)
    reasoning: str = ""

class AgentInteractionRequest(BaseModel):
    initiator: str
    target: str
    interaction_type: str  # conversation, trade, conflict, etc.
    context: Dict[str, Any] = Field(default_factory=dict)

class FactionStatusResponse(BaseModel):
    faction_name: str
    agents: List[str]
    total_influence: float
    relationships: Dict[str, float]
    active_quests: List[str]

# Global agent manager reference (will be set by main app)
agent_manager: Optional[AgentManager] = None

def set_agent_manager(manager: AgentManager):
    """Set the global agent manager reference"""
    global agent_manager
    agent_manager = manager

@router.get("/factions")
async def get_faction_overview():
    """Get overview of all factions and their agents"""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    
    try:
        factions = {
            "Empire": ["Karczmarz", "Kapitan_Straży", "Kupiec_Imperialny", "Czarodziej_Jasności"],
            "Chaos": ["Czempion", "Kultista_Nurgle", "Berserker_Khorne", "Mag_Tzeentch"],
            "Elves": ["Zwiadowca", "Mag_Wysokich_Elfów", "Strażnik_Lasu", "Tancerz_Cieni"],
            "Dwarfs": ["Kowal_Krasnoludzki", "Górnik_Karak", "Inżynier_Gildii"],
            "Neutrals": ["Wiedźma", "Łowca_Nagród", "Handlarz_Halfling"]
        }
        
        faction_status = {}
        for faction_name, agent_names in factions.items():
            active_agents = []
            total_influence = 0.0
            
            for agent_name in agent_names:
                if agent_name in agent_manager.agents:
                    agent = agent_manager.agents[agent_name]
                    if agent.active:
                        active_agents.append(agent_name)
                        total_influence += getattr(agent, 'influence', 1.0)
            
            faction_status[faction_name] = {
                "total_agents": len(agent_names),
                "active_agents": len(active_agents),
                "agent_names": active_agents,
                "total_influence": total_influence,
                "average_influence": total_influence / max(len(active_agents), 1)
            }
        
        return {"factions": faction_status}
        
    except Exception as e:
        logger.error(f"Error getting faction overview: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/faction/{faction_name}")
async def get_faction_details(faction_name: str):
    """Get detailed information about a specific faction"""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    
    faction_agents = {
        "Empire": ["Karczmarz", "Kapitan_Straży", "Kupiec_Imperialny", "Czarodziej_Jasności"],
        "Chaos": ["Czempion", "Kultista_Nurgle", "Berserker_Khorne", "Mag_Tzeentch"],
        "Elves": ["Zwiadowca", "Mag_Wysokich_Elfów", "Strażnik_Lasu", "Tancerz_Cieni"],
        "Dwarfs": ["Kowal_Krasnoludzki", "Górnik_Karak", "Inżynier_Gildii"],
        "Neutrals": ["Wiedźma", "Łowca_Nagród", "Handlarz_Halfling"]
    }
    
    if faction_name not in faction_agents:
        raise HTTPException(status_code=404, detail="Faction not found")
    
    try:
        agent_names = faction_agents[faction_name]
        faction_data = {
            "name": faction_name,
            "agents": [],
            "relationships": {},
            "recent_actions": []
        }
        
        for agent_name in agent_names:
            if agent_name in agent_manager.agents:
                agent = agent_manager.agents[agent_name]
                faction_data["agents"].append({
                    "name": agent.name,
                    "role": agent.role,
                    "active": agent.active,
                    "emotions": agent.memory.emotions,
                    "last_action": agent.last_action_time.isoformat()
                })
        
        # Get faction relationships
        faction_data["relationships"] = agent_manager.get_faction_relationships(faction_name)
        
        # Get recent actions
        faction_data["recent_actions"] = agent_manager.get_faction_recent_actions(faction_name, limit=10)
        
        return faction_data
        
    except Exception as e:
        logger.error(f"Error getting faction details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{agent_name}/action")
async def execute_agent_action(agent_name: str, action_request: AgentActionRequest, background_tasks: BackgroundTasks):
    """Execute a specific action for an agent"""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    
    if agent_name not in agent_manager.agents:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        agent = agent_manager.agents[agent_name]
        
        # Create agent action
        action = AgentAction(
            action_type=action_request.action_type,
            target=action_request.target,
            parameters=action_request.parameters,
            reasoning=action_request.reasoning
        )
        
        # Execute action in background
        background_tasks.add_task(execute_action_background, agent_name, action)
        
        return {
            "success": True,
            "message": f"Action '{action_request.action_type}' queued for {agent_name}",
            "action_id": f"{agent_name}_{datetime.now().timestamp()}"
        }
        
    except Exception as e:
        logger.error(f"Error executing agent action: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def execute_action_background(agent_name: str, action: AgentAction):
    """Execute agent action in background"""
    try:
        if agent_manager and agent_name in agent_manager.agents:
            agent = agent_manager.agents[agent_name]
            result = agent.act(action, {})  # Empty tavern state for now
            
            # Log action result
            logger.info(f"Agent {agent_name} executed action {action.action_type}: {result}")
            
    except Exception as e:
        logger.error(f"Error in background action execution: {e}")

@router.post("/interaction")
async def create_agent_interaction(interaction_request: AgentInteractionRequest, background_tasks: BackgroundTasks):
    """Create an interaction between two agents"""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    
    initiator = interaction_request.initiator
    target = interaction_request.target
    
    if initiator not in agent_manager.agents:
        raise HTTPException(status_code=404, detail=f"Initiator agent '{initiator}' not found")
    
    if target not in agent_manager.agents:
        raise HTTPException(status_code=404, detail=f"Target agent '{target}' not found")
    
    try:
        # Queue interaction in background
        background_tasks.add_task(process_agent_interaction, interaction_request)
        
        return {
            "success": True,
            "message": f"Interaction between {initiator} and {target} initiated",
            "interaction_type": interaction_request.interaction_type
        }
        
    except Exception as e:
        logger.error(f"Error creating agent interaction: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def process_agent_interaction(interaction_request: AgentInteractionRequest):
    """Process agent interaction in background"""
    try:
        if not agent_manager:
            return
        
        initiator_agent = agent_manager.agents[interaction_request.initiator]
        target_agent = agent_manager.agents[interaction_request.target]
        
        # Create interaction based on type
        if interaction_request.interaction_type == "conversation":
            result = agent_manager.facilitate_conversation(
                interaction_request.initiator,
                interaction_request.target,
                interaction_request.context.get("topic", "general")
            )
        elif interaction_request.interaction_type == "trade":
            result = agent_manager.facilitate_trade(
                interaction_request.initiator,
                interaction_request.target,
                interaction_request.context
            )
        elif interaction_request.interaction_type == "conflict":
            result = agent_manager.facilitate_conflict(
                interaction_request.initiator,
                interaction_request.target,
                interaction_request.context
            )
        else:
            result = {"success": False, "message": "Unknown interaction type"}
        
        logger.info(f"Interaction result: {result}")
        
    except Exception as e:
        logger.error(f"Error processing agent interaction: {e}")

@router.get("/relationships")
async def get_agent_relationships():
    """Get relationship matrix between all agents"""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    
    try:
        relationships = {}
        
        for agent_name, agent in agent_manager.agents.items():
            relationships[agent_name] = agent.memory.relationships.copy()
        
        return {"relationships": relationships}
        
    except Exception as e:
        logger.error(f"Error getting agent relationships: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/communication/history")
async def get_communication_history(limit: int = 20):
    """Get recent communication history between agents"""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    
    try:
        history = agent_manager.get_communication_history(limit=limit)
        return {"communication_history": history}
        
    except Exception as e:
        logger.error(f"Error getting communication history: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
async def reset_all_agents():
    """Reset all agents to initial state"""
    if not agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    
    try:
        agent_manager.reset_all_agents()
        return {"success": True, "message": "All agents reset to initial state"}
        
    except Exception as e:
        logger.error(f"Error resetting agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))
