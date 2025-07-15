"""
FastAPI Backend Server for Warhammer Fantasy Tavern Simulator
Bridges JavaScript frontend with existing CrewAI Python implementation
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import Dict, List, Any, Optional
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
import uvicorn

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import existing components
from crewai_app import WarhamerTavernCrew, CrewAIConfig
from services.agent_manager import AgentManager
from services.llm_service import LLMService
from services.tavern_economy import TavernEconomySystem
from services.narrative_engine import NarrativeEngine
from core.tavern_simulator import TavernSimulator
from core.character_generator import CharacterGenerator
from components.gsap_renderer import GSAPRenderer

# Import agent endpoints and WebSocket manager
from api.agent_endpoints import router as agent_router, set_agent_manager
from api.websocket_manager import websocket_manager, WebSocketMessage, MessageType
from api.crewai_integration import CrewAIWebIntegration, set_crewai_integration, get_crewai_integration

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global state management
class AppState:
    def __init__(self):
        self.crew: Optional[WarhamerTavernCrew] = None
        self.agent_manager: Optional[AgentManager] = None
        self.economy: Optional[TavernEconomySystem] = None
        self.narrative: Optional[NarrativeEngine] = None
        self.simulator: Optional[TavernSimulator] = None
        self.gsap_renderer: Optional[GSAPRenderer] = None
        self.websocket_connections: List[WebSocket] = []
        self.is_initialized = False

app_state = AppState()

# Pydantic models for API
class AgentResponse(BaseModel):
    agent_name: str
    role: str
    message: str
    emotion: str = "neutral"
    faction: str
    timestamp: datetime = Field(default_factory=datetime.now)

class ConversationRequest(BaseModel):
    participants: List[str] = Field(default_factory=list)
    topic: Optional[str] = None
    duration: int = 30  # seconds

class TavernEvent(BaseModel):
    event_type: str
    description: str
    participants: List[str] = Field(default_factory=list)
    effects: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.now)

class TavernState(BaseModel):
    name: str
    reputation: int
    tension: int
    wealth: int
    active_characters: List[Dict[str, Any]]
    current_events: List[TavernEvent]
    conversation_history: List[AgentResponse]

# Use the enhanced WebSocket manager
manager = websocket_manager

# Application lifecycle
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("🏰 Starting Warhammer Fantasy Tavern Simulator API...")
    await initialize_systems()
    yield
    # Shutdown
    logger.info("🏰 Shutting down Tavern Simulator API...")

# Initialize FastAPI app
app = FastAPI(
    title="Warhammer Fantasy Tavern Simulator API",
    description="Advanced API for CrewAI-powered Warhammer Fantasy tavern simulation",
    version="2.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(agent_router)

async def initialize_systems():
    """Initialize all backend systems"""
    try:
        logger.info("Initializing backend systems...")
        
        # Initialize CrewAI system
        app_state.crew = WarhamerTavernCrew()
        success = app_state.crew.initialize_mvp_crew()
        if not success:
            logger.error("Failed to initialize CrewAI crew")
            return False
        
        # Initialize other systems
        app_state.agent_manager = AgentManager()
        app_state.economy = TavernEconomySystem()
        app_state.narrative = NarrativeEngine(economy_system=app_state.economy)
        app_state.simulator = TavernSimulator()
        app_state.gsap_renderer = GSAPRenderer()

        # Set agent manager for agent endpoints
        set_agent_manager(app_state.agent_manager)

        # Initialize CrewAI integration
        integration = CrewAIWebIntegration(
            crew=app_state.crew,
            agent_manager=app_state.agent_manager,
            narrative_engine=app_state.narrative,
            economy=app_state.economy
        )
        set_crewai_integration(integration)

        # Generate initial tavern
        app_state.simulator.generate_new_tavern()

        app_state.is_initialized = True
        logger.info("✅ All systems initialized successfully")
        return True
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize systems: {e}")
        return False

# Health check endpoint
@app.get("/health")
async def health_check():
    return {
        "status": "healthy" if app_state.is_initialized else "initializing",
        "timestamp": datetime.now().isoformat(),
        "systems": {
            "crew": app_state.crew is not None,
            "agent_manager": app_state.agent_manager is not None,
            "economy": app_state.economy is not None,
            "narrative": app_state.narrative is not None,
            "simulator": app_state.simulator is not None
        }
    }

# Tavern state endpoints
@app.get("/api/tavern/state", response_model=TavernState)
async def get_tavern_state():
    """Get current tavern state"""
    if not app_state.is_initialized:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        tavern = app_state.simulator.current_tavern
        if not tavern:
            raise HTTPException(status_code=404, detail="No active tavern")
        
        # Get active characters
        active_characters = []
        for char in tavern.characters:
            active_characters.append({
                "name": char.name,
                "faction": char.faction.value if hasattr(char.faction, 'value') else str(char.faction),
                "role": char.role,
                "mood": getattr(char, 'mood', 'neutral'),
                "location": getattr(char, 'location', 'tavern_main')
            })
        
        return TavernState(
            name=tavern.name,
            reputation=getattr(tavern, 'reputation', 75),
            tension=getattr(tavern, 'tension', 25),
            wealth=getattr(tavern, 'wealth', 1250),
            active_characters=active_characters,
            current_events=[],
            conversation_history=[]
        )
        
    except Exception as e:
        logger.error(f"Error getting tavern state: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tavern/generate")
async def generate_new_tavern():
    """Generate a new tavern"""
    if not app_state.is_initialized:
        raise HTTPException(status_code=503, detail="System not initialized")
    
    try:
        app_state.simulator.generate_new_tavern()
        
        # Broadcast update to connected clients
        message = WebSocketMessage(
            type=MessageType.TAVERN_UPDATE.value,
            data={
                "event": "tavern_generated",
                "name": app_state.simulator.current_tavern.name,
                "timestamp": datetime.now().isoformat()
            }
        )
        await manager.broadcast_to_subscription("tavern_updates", message)
        
        return {"success": True, "message": "New tavern generated"}
        
    except Exception as e:
        logger.error(f"Error generating tavern: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Agent endpoints
@app.get("/api/agents")
async def get_agents():
    """Get all available agents"""
    if not app_state.agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    
    try:
        agents_info = []
        for name, agent in app_state.agent_manager.agents.items():
            agents_info.append({
                "name": name,
                "role": agent.role,
                "active": agent.active,
                "personality": agent.personality,
                "faction": getattr(agent, 'faction', 'unknown'),
                "last_action": agent.last_action_time.isoformat()
            })
        
        return {"agents": agents_info}
        
    except Exception as e:
        logger.error(f"Error getting agents: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/agents/{agent_name}")
async def get_agent_details(agent_name: str):
    """Get detailed information about a specific agent"""
    if not app_state.agent_manager:
        raise HTTPException(status_code=503, detail="Agent manager not initialized")
    
    agent = app_state.agent_manager.agents.get(agent_name)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    try:
        return {
            "name": agent.name,
            "role": agent.role,
            "personality": agent.personality,
            "active": agent.active,
            "memory": {
                "short_term": agent.memory.short_term[-5:],  # Last 5 memories
                "emotions": agent.memory.emotions,
                "relationships": agent.memory.relationships
            },
            "last_action": agent.last_action_time.isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error getting agent details: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Conversation endpoints
@app.post("/api/conversation/start")
async def start_conversation(request: ConversationRequest, background_tasks: BackgroundTasks):
    """Start a conversation between agents"""
    if not app_state.is_initialized:
        raise HTTPException(status_code=503, detail="System not initialized")

    try:
        # Start conversation in background
        background_tasks.add_task(run_conversation, request)

        return {
            "success": True,
            "message": "Conversation started",
            "participants": request.participants,
            "topic": request.topic
        }

    except Exception as e:
        logger.error(f"Error starting conversation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

async def run_conversation(request: ConversationRequest):
    """Run conversation between agents"""
    try:
        integration = get_crewai_integration()
        if integration:
            if request.participants:
                # Run specific agent conversation
                result = await integration.execute_agent_conversation(
                    request.participants,
                    request.topic or "general"
                )
            else:
                # Run full crew execution
                result = await integration.execute_crew_with_broadcast()

            logger.info(f"Conversation result: {result}")
        else:
            logger.error("CrewAI integration not available")

    except Exception as e:
        logger.error(f"Error running conversation: {e}")

@app.post("/api/events/generate")
async def generate_event(background_tasks: BackgroundTasks):
    """Generate a random tavern event"""
    if not app_state.is_initialized:
        raise HTTPException(status_code=503, detail="System not initialized")

    try:
        # Generate event using narrative engine
        if app_state.narrative:
            event = app_state.narrative.generate_random_event()

            # Broadcast event to all clients
            await manager.broadcast(json.dumps({
                "type": "tavern_event",
                "data": {
                    "event_type": event.get("type", "general"),
                    "description": event.get("description", "Something happens in the tavern"),
                    "timestamp": datetime.now().isoformat()
                }
            }))

            return {"success": True, "event": event}
        else:
            raise HTTPException(status_code=503, detail="Narrative engine not available")

    except Exception as e:
        logger.error(f"Error generating event: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/economy/status")
async def get_economy_status():
    """Get current economy status"""
    if not app_state.economy:
        raise HTTPException(status_code=503, detail="Economy system not initialized")

    try:
        return {
            "resources": app_state.economy.get_resource_summary(),
            "transactions": app_state.economy.get_recent_transactions(limit=10),
            "market_trends": app_state.economy.get_market_trends()
        }

    except Exception as e:
        logger.error(f"Error getting economy status: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/economy/trade")
async def execute_trade(trade_data: Dict[str, Any]):
    """Execute a trade transaction"""
    if not app_state.economy:
        raise HTTPException(status_code=503, detail="Economy system not initialized")

    try:
        result = app_state.economy.execute_trade(
            trade_data.get("buyer"),
            trade_data.get("seller"),
            trade_data.get("resource"),
            trade_data.get("quantity", 1),
            trade_data.get("price")
        )

        # Broadcast trade update
        await manager.broadcast(json.dumps({
            "type": "trade_executed",
            "data": {
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        }))

        return {"success": True, "result": result}

    except Exception as e:
        logger.error(f"Error executing trade: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# GSAP rendering endpoints
@app.get("/api/render/tavern")
async def render_tavern_scene():
    """Get GSAP-rendered tavern scene"""
    if not app_state.gsap_renderer or not app_state.simulator:
        raise HTTPException(status_code=503, detail="Renderer not initialized")

    try:
        tavern = app_state.simulator.current_tavern
        if not tavern:
            raise HTTPException(status_code=404, detail="No active tavern")

        # Generate GSAP scene
        scene_html = app_state.gsap_renderer.render_tavern_scene(
            tavern.name,
            tavern.characters,
            theme="dark-fantasy"
        )

        return {"html": scene_html, "tavern_name": tavern.name}

    except Exception as e:
        logger.error(f"Error rendering tavern scene: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/render/characters")
async def render_character_animations():
    """Get character animation data for frontend"""
    if not app_state.simulator:
        raise HTTPException(status_code=503, detail="Simulator not initialized")

    try:
        tavern = app_state.simulator.current_tavern
        if not tavern:
            raise HTTPException(status_code=404, detail="No active tavern")

        character_data = []
        for char in tavern.characters:
            character_data.append({
                "name": char.name,
                "faction": char.faction.value if hasattr(char.faction, 'value') else str(char.faction),
                "position": getattr(char, 'position', {"x": 0, "y": 0, "z": 0}),
                "animation_state": getattr(char, 'animation_state', 'idle'),
                "mood": getattr(char, 'mood', 'neutral'),
                "dialogue": getattr(char, 'current_dialogue', '')
            })

        return {"characters": character_data}

    except Exception as e:
        logger.error(f"Error rendering character animations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# WebSocket endpoint for real-time communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket, client_id: str = None):
    client_id = await manager.connect(websocket, client_id)
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            await manager.handle_client_message(client_id, message_data)

    except WebSocketDisconnect:
        manager.disconnect(client_id)
    except Exception as e:
        logger.error(f"WebSocket error for client {client_id}: {e}")
        manager.disconnect(client_id)

# CrewAI specific endpoints
@app.get("/api/crew/status")
async def get_crew_status():
    """Get current CrewAI crew status"""
    integration = get_crewai_integration()
    if not integration:
        raise HTTPException(status_code=503, detail="CrewAI integration not available")

    return integration.get_crew_status()

@app.post("/api/crew/execute")
async def execute_crew(background_tasks: BackgroundTasks, context: Dict[str, Any] = None):
    """Execute the full CrewAI crew"""
    integration = get_crewai_integration()
    if not integration:
        raise HTTPException(status_code=503, detail="CrewAI integration not available")

    if integration.is_executing:
        raise HTTPException(status_code=409, detail="Crew execution already in progress")

    # Execute in background
    background_tasks.add_task(integration.execute_crew_with_broadcast, context or {})

    return {
        "success": True,
        "message": "Crew execution started",
        "timestamp": datetime.now().isoformat()
    }

@app.post("/api/crew/conversation")
async def start_crew_conversation(request: ConversationRequest, background_tasks: BackgroundTasks):
    """Start a conversation using CrewAI agents"""
    integration = get_crewai_integration()
    if not integration:
        raise HTTPException(status_code=503, detail="CrewAI integration not available")

    # Execute conversation in background
    background_tasks.add_task(
        integration.execute_agent_conversation,
        request.participants,
        request.topic or "general"
    )

    return {
        "success": True,
        "message": "Conversation started",
        "participants": request.participants,
        "topic": request.topic
    }

@app.get("/api/websocket/stats")
async def get_websocket_stats():
    """Get WebSocket connection statistics"""
    return manager.get_connection_stats()

if __name__ == "__main__":
    uvicorn.run(
        "fastapi_server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
