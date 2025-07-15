"""
CrewAI Integration Layer for FastAPI Backend
Bridges the existing CrewAI implementation with the new web interface
"""

import asyncio
import logging
from typing import Dict, List, Any, Optional
from datetime import datetime
from dataclasses import dataclass
import json

from crewai_app import WarhamerTavernCrew, CrewAIConfig
from services.agent_manager import AgentManager
from services.narrative_engine import NarrativeEngine
from services.tavern_economy import TavernEconomySystem
from api.websocket_manager import websocket_manager, WebSocketMessage, MessageType

logger = logging.getLogger(__name__)

@dataclass
class CrewExecutionResult:
    """Result of crew execution"""
    success: bool
    result: str
    execution_time: float
    agents_involved: List[str]
    tasks_completed: List[str]
    errors: List[str]
    timestamp: datetime

class CrewAIWebIntegration:
    """Integration layer between CrewAI and web interface"""
    
    def __init__(self, crew: WarhamerTavernCrew, agent_manager: AgentManager, 
                 narrative_engine: NarrativeEngine, economy: TavernEconomySystem):
        self.crew = crew
        self.agent_manager = agent_manager
        self.narrative_engine = narrative_engine
        self.economy = economy
        self.execution_history: List[CrewExecutionResult] = []
        self.is_executing = False
        
    async def execute_crew_with_broadcast(self, context: Dict[str, Any] = None) -> CrewExecutionResult:
        """Execute crew and broadcast results to connected clients"""
        if self.is_executing:
            logger.warning("Crew execution already in progress")
            return CrewExecutionResult(
                success=False,
                result="Crew execution already in progress",
                execution_time=0.0,
                agents_involved=[],
                tasks_completed=[],
                errors=["Execution already in progress"],
                timestamp=datetime.now()
            )
        
        self.is_executing = True
        start_time = datetime.now()
        
        try:
            # Broadcast execution start
            start_message = WebSocketMessage(
                type=MessageType.CONVERSATION_START.value,
                data={
                    "event": "crew_execution_start",
                    "context": context or {},
                    "timestamp": start_time.isoformat()
                }
            )
            await websocket_manager.broadcast_to_subscription("conversations", start_message)
            
            # Execute crew
            logger.info("Starting CrewAI execution...")
            result = self.crew.execute_crew()
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            # Create execution result
            execution_result = CrewExecutionResult(
                success=True,
                result=str(result),
                execution_time=execution_time,
                agents_involved=[agent.role for agent in self.crew.agents],
                tasks_completed=[task.description[:50] + "..." for task in self.crew.tasks],
                errors=[],
                timestamp=datetime.now()
            )
            
            # Store in history
            self.execution_history.append(execution_result)
            
            # Broadcast completion
            completion_message = WebSocketMessage(
                type=MessageType.CONVERSATION_END.value,
                data={
                    "event": "crew_execution_complete",
                    "result": str(result),
                    "execution_time": execution_time,
                    "agents_involved": execution_result.agents_involved,
                    "timestamp": datetime.now().isoformat()
                }
            )
            await websocket_manager.broadcast_to_subscription("conversations", completion_message)
            
            logger.info(f"CrewAI execution completed in {execution_time:.2f}s")
            return execution_result
            
        except Exception as e:
            execution_time = (datetime.now() - start_time).total_seconds()
            error_msg = str(e)
            
            execution_result = CrewExecutionResult(
                success=False,
                result="",
                execution_time=execution_time,
                agents_involved=[],
                tasks_completed=[],
                errors=[error_msg],
                timestamp=datetime.now()
            )
            
            # Store error in history
            self.execution_history.append(execution_result)
            
            # Broadcast error
            error_message = WebSocketMessage(
                type=MessageType.ERROR.value,
                data={
                    "event": "crew_execution_error",
                    "error": error_msg,
                    "execution_time": execution_time,
                    "timestamp": datetime.now().isoformat()
                }
            )
            await websocket_manager.broadcast_to_subscription("conversations", error_message)
            
            logger.error(f"CrewAI execution failed: {e}")
            return execution_result
            
        finally:
            self.is_executing = False
    
    async def execute_agent_conversation(self, participants: List[str], topic: str = "general") -> Dict[str, Any]:
        """Execute conversation between specific agents"""
        try:
            # Validate participants
            valid_participants = []
            for participant in participants:
                if participant in self.agent_manager.agents:
                    valid_participants.append(participant)
                else:
                    logger.warning(f"Agent {participant} not found")
            
            if len(valid_participants) < 2:
                return {
                    "success": False,
                    "error": "Need at least 2 valid participants for conversation"
                }
            
            # Broadcast conversation start
            start_message = WebSocketMessage(
                type=MessageType.CONVERSATION_START.value,
                data={
                    "participants": valid_participants,
                    "topic": topic,
                    "timestamp": datetime.now().isoformat()
                }
            )
            await websocket_manager.broadcast_to_subscription("conversations", start_message)
            
            # Facilitate conversation through agent manager
            conversation_result = self.agent_manager.facilitate_conversation(
                valid_participants[0],
                valid_participants[1],
                topic
            )
            
            # Broadcast conversation messages
            for i, participant in enumerate(valid_participants):
                message = WebSocketMessage(
                    type=MessageType.CONVERSATION_MESSAGE.value,
                    data={
                        "speaker": participant,
                        "message": f"[{participant}] discusses {topic}",
                        "emotion": "engaged",
                        "timestamp": datetime.now().isoformat()
                    }
                )
                await websocket_manager.broadcast_to_subscription("conversations", message)
                
                # Small delay between messages for realism
                await asyncio.sleep(1)
            
            # Broadcast conversation end
            end_message = WebSocketMessage(
                type=MessageType.CONVERSATION_END.value,
                data={
                    "participants": valid_participants,
                    "topic": topic,
                    "result": conversation_result,
                    "timestamp": datetime.now().isoformat()
                }
            )
            await websocket_manager.broadcast_to_subscription("conversations", end_message)
            
            return {
                "success": True,
                "participants": valid_participants,
                "topic": topic,
                "result": conversation_result
            }
            
        except Exception as e:
            logger.error(f"Error executing agent conversation: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def generate_narrative_event(self) -> Dict[str, Any]:
        """Generate and broadcast narrative event"""
        try:
            # Generate event using narrative engine
            event = self.narrative_engine.generate_random_event()
            
            # Broadcast event
            event_message = WebSocketMessage(
                type=MessageType.TAVERN_EVENT.value,
                data={
                    "event_type": event.get("type", "general"),
                    "description": event.get("description", "Something happens in the tavern"),
                    "participants": event.get("participants", []),
                    "effects": event.get("effects", {}),
                    "timestamp": datetime.now().isoformat()
                }
            )
            await websocket_manager.broadcast_to_subscription("events", event_message)
            
            return {
                "success": True,
                "event": event
            }
            
        except Exception as e:
            logger.error(f"Error generating narrative event: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    async def update_economy_and_broadcast(self) -> Dict[str, Any]:
        """Update economy and broadcast changes"""
        try:
            # Run economic cycle
            cycle_result = self.economy.run_economic_cycle()
            
            # Get updated status
            economy_status = {
                "resources": self.economy.get_resource_summary(),
                "recent_transactions": self.economy.get_recent_transactions(limit=5),
                "market_trends": self.economy.get_market_trends(),
                "cycle_result": cycle_result
            }
            
            # Broadcast economy update
            economy_message = WebSocketMessage(
                type=MessageType.ECONOMY_UPDATE.value,
                data=economy_status
            )
            await websocket_manager.broadcast_to_subscription("economy", economy_message)
            
            return {
                "success": True,
                "economy_status": economy_status
            }
            
        except Exception as e:
            logger.error(f"Error updating economy: {e}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_crew_status(self) -> Dict[str, Any]:
        """Get current crew status"""
        return {
            "is_executing": self.is_executing,
            "crew_ready": self.crew.crew is not None,
            "agents": [
                {
                    "role": agent.role,
                    "goal": agent.goal,
                    "llm_configured": agent.llm is not None
                }
                for agent in self.crew.agents
            ],
            "tasks": [
                {
                    "description": task.description[:100] + "...",
                    "agent_role": task.agent.role if task.agent else "Unassigned"
                }
                for task in self.crew.tasks
            ],
            "execution_history": [
                {
                    "success": result.success,
                    "execution_time": result.execution_time,
                    "agents_involved": result.agents_involved,
                    "timestamp": result.timestamp.isoformat(),
                    "errors": result.errors
                }
                for result in self.execution_history[-10:]  # Last 10 executions
            ]
        }
    
    async def broadcast_agent_action(self, agent_name: str, action_type: str, result: Dict[str, Any]):
        """Broadcast agent action to connected clients"""
        action_message = WebSocketMessage(
            type=MessageType.AGENT_ACTION.value,
            data={
                "agent_name": agent_name,
                "action_type": action_type,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
        )
        await websocket_manager.broadcast_to_subscription("agent_actions", action_message)

# Global integration instance (will be set by main app)
crewai_integration: Optional[CrewAIWebIntegration] = None

def set_crewai_integration(integration: CrewAIWebIntegration):
    """Set the global CrewAI integration instance"""
    global crewai_integration
    crewai_integration = integration

def get_crewai_integration() -> Optional[CrewAIWebIntegration]:
    """Get the global CrewAI integration instance"""
    return crewai_integration
