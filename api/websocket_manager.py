"""
Enhanced WebSocket Manager for Real-time Communication
Handles live conversations, events, and state updates
"""

import asyncio
import json
import logging
from typing import Dict, List, Set, Optional, Any
from datetime import datetime
from dataclasses import dataclass, asdict
from enum import Enum

from fastapi import WebSocket, WebSocketDisconnect

logger = logging.getLogger(__name__)

class MessageType(Enum):
    """WebSocket message types"""
    PING = "ping"
    PONG = "pong"
    CONNECT = "connect"
    DISCONNECT = "disconnect"
    TAVERN_UPDATE = "tavern_update"
    CONVERSATION_START = "conversation_start"
    CONVERSATION_MESSAGE = "conversation_message"
    CONVERSATION_END = "conversation_end"
    AGENT_ACTION = "agent_action"
    TAVERN_EVENT = "tavern_event"
    ECONOMY_UPDATE = "economy_update"
    CHARACTER_ANIMATION = "character_animation"
    SYSTEM_STATUS = "system_status"
    ERROR = "error"

@dataclass
class WebSocketMessage:
    """Structured WebSocket message"""
    type: str
    data: Dict[str, Any]
    timestamp: str = None
    client_id: str = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now().isoformat()

@dataclass
class ConnectedClient:
    """Information about connected client"""
    websocket: WebSocket
    client_id: str
    connected_at: datetime
    subscriptions: Set[str]
    last_ping: datetime

class EnhancedWebSocketManager:
    """Enhanced WebSocket manager with subscription system"""
    
    def __init__(self):
        self.active_connections: Dict[str, ConnectedClient] = {}
        self.subscriptions: Dict[str, Set[str]] = {}  # topic -> client_ids
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.is_running = False
        
    async def connect(self, websocket: WebSocket, client_id: str = None) -> str:
        """Connect a new client"""
        await websocket.accept()
        
        if client_id is None:
            client_id = f"client_{datetime.now().timestamp()}"
        
        client = ConnectedClient(
            websocket=websocket,
            client_id=client_id,
            connected_at=datetime.now(),
            subscriptions=set(),
            last_ping=datetime.now()
        )
        
        self.active_connections[client_id] = client
        
        # Send welcome message
        welcome_msg = WebSocketMessage(
            type=MessageType.CONNECT.value,
            data={
                "client_id": client_id,
                "server_time": datetime.now().isoformat(),
                "available_subscriptions": [
                    "tavern_updates",
                    "conversations",
                    "agent_actions",
                    "economy",
                    "events"
                ]
            },
            client_id=client_id
        )
        
        await self.send_to_client(client_id, welcome_msg)
        
        logger.info(f"WebSocket client {client_id} connected. Total: {len(self.active_connections)}")
        return client_id
    
    def disconnect(self, client_id: str):
        """Disconnect a client"""
        if client_id in self.active_connections:
            client = self.active_connections[client_id]
            
            # Remove from all subscriptions
            for subscription in client.subscriptions:
                if subscription in self.subscriptions:
                    self.subscriptions[subscription].discard(client_id)
            
            del self.active_connections[client_id]
            logger.info(f"WebSocket client {client_id} disconnected. Total: {len(self.active_connections)}")
    
    async def send_to_client(self, client_id: str, message: WebSocketMessage):
        """Send message to specific client"""
        if client_id not in self.active_connections:
            return False
        
        client = self.active_connections[client_id]
        try:
            message_dict = asdict(message)
            await client.websocket.send_text(json.dumps(message_dict))
            return True
        except Exception as e:
            logger.error(f"Error sending to client {client_id}: {e}")
            self.disconnect(client_id)
            return False
    
    async def broadcast_to_subscription(self, topic: str, message: WebSocketMessage):
        """Broadcast message to all clients subscribed to a topic"""
        if topic not in self.subscriptions:
            return
        
        client_ids = self.subscriptions[topic].copy()
        disconnected = []
        
        for client_id in client_ids:
            success = await self.send_to_client(client_id, message)
            if not success:
                disconnected.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected:
            self.subscriptions[topic].discard(client_id)
    
    async def broadcast_to_all(self, message: WebSocketMessage):
        """Broadcast message to all connected clients"""
        client_ids = list(self.active_connections.keys())
        for client_id in client_ids:
            await self.send_to_client(client_id, message)
    
    def subscribe_client(self, client_id: str, topic: str):
        """Subscribe client to a topic"""
        if client_id not in self.active_connections:
            return False
        
        if topic not in self.subscriptions:
            self.subscriptions[topic] = set()
        
        self.subscriptions[topic].add(client_id)
        self.active_connections[client_id].subscriptions.add(topic)
        
        logger.info(f"Client {client_id} subscribed to {topic}")
        return True
    
    def unsubscribe_client(self, client_id: str, topic: str):
        """Unsubscribe client from a topic"""
        if client_id not in self.active_connections:
            return False
        
        if topic in self.subscriptions:
            self.subscriptions[topic].discard(client_id)
        
        if client_id in self.active_connections:
            self.active_connections[client_id].subscriptions.discard(topic)
        
        logger.info(f"Client {client_id} unsubscribed from {topic}")
        return True
    
    async def handle_client_message(self, client_id: str, message_data: Dict[str, Any]):
        """Handle incoming message from client"""
        try:
            message_type = message_data.get("type")
            data = message_data.get("data", {})
            
            if message_type == MessageType.PING.value:
                # Update last ping time
                if client_id in self.active_connections:
                    self.active_connections[client_id].last_ping = datetime.now()
                
                # Send pong response
                pong_msg = WebSocketMessage(
                    type=MessageType.PONG.value,
                    data={"timestamp": datetime.now().isoformat()},
                    client_id=client_id
                )
                await self.send_to_client(client_id, pong_msg)
            
            elif message_type == "subscribe":
                topic = data.get("topic")
                if topic:
                    success = self.subscribe_client(client_id, topic)
                    response = WebSocketMessage(
                        type="subscription_response",
                        data={
                            "topic": topic,
                            "subscribed": success,
                            "message": f"{'Subscribed to' if success else 'Failed to subscribe to'} {topic}"
                        },
                        client_id=client_id
                    )
                    await self.send_to_client(client_id, response)
            
            elif message_type == "unsubscribe":
                topic = data.get("topic")
                if topic:
                    success = self.unsubscribe_client(client_id, topic)
                    response = WebSocketMessage(
                        type="subscription_response",
                        data={
                            "topic": topic,
                            "subscribed": False,
                            "message": f"{'Unsubscribed from' if success else 'Failed to unsubscribe from'} {topic}"
                        },
                        client_id=client_id
                    )
                    await self.send_to_client(client_id, response)
            
            elif message_type == "start_conversation":
                # Handle conversation start request
                await self.handle_conversation_request(client_id, data)
            
            elif message_type == "agent_action":
                # Handle agent action request
                await self.handle_agent_action_request(client_id, data)
            
            else:
                logger.warning(f"Unknown message type from client {client_id}: {message_type}")
        
        except Exception as e:
            logger.error(f"Error handling message from client {client_id}: {e}")
            error_msg = WebSocketMessage(
                type=MessageType.ERROR.value,
                data={"error": str(e), "original_message": message_data},
                client_id=client_id
            )
            await self.send_to_client(client_id, error_msg)
    
    async def handle_conversation_request(self, client_id: str, data: Dict[str, Any]):
        """Handle conversation start request from client"""
        # This would integrate with the conversation system
        participants = data.get("participants", [])
        topic = data.get("topic", "general")
        
        # Broadcast conversation start to subscribers
        conversation_msg = WebSocketMessage(
            type=MessageType.CONVERSATION_START.value,
            data={
                "participants": participants,
                "topic": topic,
                "initiated_by": client_id
            }
        )
        
        await self.broadcast_to_subscription("conversations", conversation_msg)
    
    async def handle_agent_action_request(self, client_id: str, data: Dict[str, Any]):
        """Handle agent action request from client"""
        agent_name = data.get("agent_name")
        action_type = data.get("action_type")
        
        if not agent_name or not action_type:
            error_msg = WebSocketMessage(
                type=MessageType.ERROR.value,
                data={"error": "Missing agent_name or action_type"},
                client_id=client_id
            )
            await self.send_to_client(client_id, error_msg)
            return
        
        # Broadcast agent action to subscribers
        action_msg = WebSocketMessage(
            type=MessageType.AGENT_ACTION.value,
            data={
                "agent_name": agent_name,
                "action_type": action_type,
                "parameters": data.get("parameters", {}),
                "initiated_by": client_id
            }
        )
        
        await self.broadcast_to_subscription("agent_actions", action_msg)
    
    def get_connection_stats(self) -> Dict[str, Any]:
        """Get connection statistics"""
        return {
            "total_connections": len(self.active_connections),
            "subscriptions": {
                topic: len(clients) for topic, clients in self.subscriptions.items()
            },
            "clients": [
                {
                    "client_id": client.client_id,
                    "connected_at": client.connected_at.isoformat(),
                    "subscriptions": list(client.subscriptions),
                    "last_ping": client.last_ping.isoformat()
                }
                for client in self.active_connections.values()
            ]
        }

# Global WebSocket manager instance
websocket_manager = EnhancedWebSocketManager()
