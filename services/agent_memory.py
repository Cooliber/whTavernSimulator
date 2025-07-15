"""
Agent Memory System for persistent context and cross-agent communication
Implements memory storage, retrieval, and sharing between tavern agents
"""

import json
import time
import uuid
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, asdict
from enum import Enum
from pathlib import Path
import threading
from collections import defaultdict, deque
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

def convert_enums_to_values(obj):
    """Recursively convert enums to their values in nested data structures"""
    if isinstance(obj, Enum):
        return obj.value
    elif isinstance(obj, dict):
        return {
            (k.value if isinstance(k, Enum) else k): convert_enums_to_values(v)
            for k, v in obj.items()
        }
    elif isinstance(obj, (list, tuple)):
        return [convert_enums_to_values(item) for item in obj]
    else:
        return obj

class EnumJSONEncoder(json.JSONEncoder):
    """Custom JSON encoder that handles Enum serialization"""
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)

    def encode(self, obj):
        """Override encode to handle enum keys in dictionaries"""
        converted_obj = convert_enums_to_values(obj)
        return super().encode(converted_obj)

class MemoryType(Enum):
    OBSERVATION = "observation"
    INTERACTION = "interaction"
    DECISION = "decision"
    EMOTION = "emotion"
    RELATIONSHIP = "relationship"
    EVENT = "event"
    RUMOR = "rumor"
    THREAT = "threat"

class MemoryImportance(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    CRITICAL = 4

@dataclass
class Memory:
    """Individual memory entry"""
    id: str
    agent_id: str
    memory_type: MemoryType
    content: str
    importance: MemoryImportance
    timestamp: float
    context: Dict[str, Any]
    related_agents: List[str]
    tags: List[str]
    decay_rate: float = 0.1  # How quickly memory fades
    access_count: int = 0
    last_accessed: float = 0.0

@dataclass
class SharedMemory:
    """Memory shared between agents"""
    id: str
    content: str
    shared_by: str
    shared_with: List[str]
    memory_type: MemoryType
    timestamp: float
    importance: MemoryImportance
    context: Dict[str, Any]

class AgentMemorySystem:
    """Comprehensive memory system for tavern agents"""
    
    def __init__(self, memory_dir: str = "data/agent_memory"):
        self.memory_dir = Path(memory_dir)
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # In-memory storage for fast access
        self.agent_memories: Dict[str, List[Memory]] = defaultdict(list)
        self.shared_memories: List[SharedMemory] = []
        self.memory_index: Dict[str, Memory] = {}
        
        # Communication channels between agents
        self.communication_channels: Dict[str, deque] = defaultdict(lambda: deque(maxlen=100))
        
        # Relationship tracking
        self.agent_relationships: Dict[str, Dict[str, float]] = defaultdict(lambda: defaultdict(float))
        
        # Memory statistics
        self.memory_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {
            "total_memories": 0,
            "memories_by_type": defaultdict(int),
            "avg_importance": 0.0,
            "last_activity": 0.0
        })
        
        # Thread lock for concurrent access
        self.lock = threading.Lock()
        
        # Load existing memories
        self.load_memories()
    
    def store_memory(self, agent_id: str, memory_type: MemoryType, content: str, 
                    importance: MemoryImportance, context: Dict[str, Any] = None,
                    related_agents: List[str] = None, tags: List[str] = None) -> str:
        """Store a new memory for an agent"""
        with self.lock:
            memory_id = str(uuid.uuid4())
            
            memory = Memory(
                id=memory_id,
                agent_id=agent_id,
                memory_type=memory_type,
                content=content,
                importance=importance,
                timestamp=time.time(),
                context=context or {},
                related_agents=related_agents or [],
                tags=tags or [],
                last_accessed=time.time()
            )
            
            # Store in agent's memory
            self.agent_memories[agent_id].append(memory)
            self.memory_index[memory_id] = memory
            
            # Update statistics
            self._update_memory_stats(agent_id, memory)
            
            # Auto-share critical memories
            if importance == MemoryImportance.CRITICAL and related_agents:
                self.share_memory(agent_id, memory_id, related_agents)
            
            # Trigger memory consolidation if needed
            self._consolidate_memories(agent_id)
            
            return memory_id
    
    def retrieve_memories(self, agent_id: str, memory_type: MemoryType = None,
                         importance_threshold: MemoryImportance = MemoryImportance.LOW,
                         limit: int = 50, include_shared: bool = True) -> List[Memory]:
        """Retrieve memories for an agent with filtering"""
        with self.lock:
            memories = []
            
            # Get agent's own memories
            agent_memories = self.agent_memories.get(agent_id, [])
            
            for memory in agent_memories:
                if memory_type and memory.memory_type != memory_type:
                    continue
                if memory.importance.value < importance_threshold.value:
                    continue
                
                # Update access statistics
                memory.access_count += 1
                memory.last_accessed = time.time()
                
                memories.append(memory)
            
            # Include shared memories if requested
            if include_shared:
                for shared_memory in self.shared_memories:
                    if agent_id in shared_memory.shared_with:
                        if memory_type and shared_memory.memory_type != memory_type:
                            continue
                        if shared_memory.importance.value < importance_threshold.value:
                            continue
                        
                        # Convert shared memory to regular memory format
                        memory = Memory(
                            id=shared_memory.id,
                            agent_id=shared_memory.shared_by,
                            memory_type=shared_memory.memory_type,
                            content=f"[SHARED] {shared_memory.content}",
                            importance=shared_memory.importance,
                            timestamp=shared_memory.timestamp,
                            context=shared_memory.context,
                            related_agents=[shared_memory.shared_by],
                            tags=["shared"]
                        )
                        memories.append(memory)
            
            # Sort by importance and recency
            memories.sort(key=lambda m: (m.importance.value, m.timestamp), reverse=True)
            
            return memories[:limit]
    
    def share_memory(self, sharing_agent: str, memory_id: str, target_agents: List[str]) -> bool:
        """Share a memory with other agents"""
        with self.lock:
            memory = self.memory_index.get(memory_id)
            if not memory or memory.agent_id != sharing_agent:
                return False
            
            shared_memory = SharedMemory(
                id=str(uuid.uuid4()),
                content=memory.content,
                shared_by=sharing_agent,
                shared_with=target_agents,
                memory_type=memory.memory_type,
                timestamp=time.time(),
                importance=memory.importance,
                context=memory.context
            )
            
            self.shared_memories.append(shared_memory)
            
            # Update relationships
            for target_agent in target_agents:
                self.agent_relationships[sharing_agent][target_agent] += 0.1
                self.agent_relationships[target_agent][sharing_agent] += 0.05
            
            return True
    
    def send_message(self, from_agent: str, to_agent: str, message: str, 
                    message_type: str = "communication") -> bool:
        """Send a message between agents"""
        with self.lock:
            message_data = {
                "id": str(uuid.uuid4()),
                "from": from_agent,
                "to": to_agent,
                "message": message,
                "type": message_type,
                "timestamp": time.time()
            }
            
            self.communication_channels[to_agent].append(message_data)
            
            # Store as memory for both agents
            self.store_memory(
                from_agent, MemoryType.INTERACTION, 
                f"Sent message to {to_agent}: {message}",
                MemoryImportance.MEDIUM,
                {"message_type": message_type, "recipient": to_agent}
            )
            
            self.store_memory(
                to_agent, MemoryType.INTERACTION,
                f"Received message from {from_agent}: {message}",
                MemoryImportance.MEDIUM,
                {"message_type": message_type, "sender": from_agent}
            )
            
            return True
    
    def get_messages(self, agent_id: str, unread_only: bool = True) -> List[Dict[str, Any]]:
        """Get messages for an agent"""
        with self.lock:
            messages = list(self.communication_channels[agent_id])
            
            if unread_only:
                # Clear the channel after reading
                self.communication_channels[agent_id].clear()
            
            return messages
    
    def get_agent_context(self, agent_id: str, context_size: int = 20) -> Dict[str, Any]:
        """Get comprehensive context for an agent"""
        recent_memories = self.retrieve_memories(
            agent_id, 
            importance_threshold=MemoryImportance.LOW,
            limit=context_size
        )
        
        recent_messages = self.get_messages(agent_id, unread_only=False)
        
        relationships = dict(self.agent_relationships[agent_id])
        
        return {
            "agent_id": agent_id,
            "recent_memories": [asdict(memory) for memory in recent_memories],
            "recent_messages": recent_messages[-5:],  # Last 5 messages
            "relationships": relationships,
            "memory_stats": self.memory_stats[agent_id],
            "timestamp": time.time()
        }
    
    def update_relationship(self, agent1: str, agent2: str, change: float):
        """Update relationship between two agents"""
        with self.lock:
            self.agent_relationships[agent1][agent2] += change
            self.agent_relationships[agent2][agent1] += change
            
            # Clamp relationships between -1.0 and 1.0
            self.agent_relationships[agent1][agent2] = max(-1.0, min(1.0, self.agent_relationships[agent1][agent2]))
            self.agent_relationships[agent2][agent1] = max(-1.0, min(1.0, self.agent_relationships[agent2][agent1]))
    
    def search_memories(self, query: str, agent_id: str = None, 
                       memory_types: List[MemoryType] = None) -> List[Memory]:
        """Search memories by content"""
        with self.lock:
            results = []
            query_lower = query.lower()
            
            # Search in specific agent's memories or all memories
            if agent_id:
                memories_to_search = self.agent_memories.get(agent_id, [])
            else:
                memories_to_search = []
                for agent_memories in self.agent_memories.values():
                    memories_to_search.extend(agent_memories)
            
            for memory in memories_to_search:
                if memory_types and memory.memory_type not in memory_types:
                    continue
                
                # Search in content, tags, and context
                if (query_lower in memory.content.lower() or
                    any(query_lower in tag.lower() for tag in memory.tags) or
                    any(query_lower in str(v).lower() for v in memory.context.values())):
                    results.append(memory)
            
            # Sort by relevance (importance and recency)
            results.sort(key=lambda m: (m.importance.value, m.timestamp), reverse=True)
            
            return results
    
    def _update_memory_stats(self, agent_id: str, memory: Memory):
        """Update memory statistics for an agent"""
        stats = self.memory_stats[agent_id]
        stats["total_memories"] += 1
        stats["memories_by_type"][memory.memory_type.value] += 1
        stats["last_activity"] = time.time()
        
        # Update average importance
        total_importance = stats["avg_importance"] * (stats["total_memories"] - 1) + memory.importance.value
        stats["avg_importance"] = total_importance / stats["total_memories"]
    
    def _consolidate_memories(self, agent_id: str, max_memories: int = 1000):
        """Consolidate memories when they exceed limit"""
        memories = self.agent_memories[agent_id]
        
        if len(memories) <= max_memories:
            return
        
        # Sort by importance and recency, keep the most important
        memories.sort(key=lambda m: (m.importance.value, m.timestamp), reverse=True)
        
        # Keep top memories, remove the rest
        kept_memories = memories[:max_memories]
        removed_memories = memories[max_memories:]
        
        # Remove from index
        for memory in removed_memories:
            if memory.id in self.memory_index:
                del self.memory_index[memory.id]
        
        self.agent_memories[agent_id] = kept_memories
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=1, max=5),
        retry=retry_if_exception_type((IOError, OSError, json.JSONDecodeError))
    )
    def save_memories(self):
        """Save memories to disk with retry mechanism"""
        with self.lock:
            # Save agent memories
            for agent_id, memories in self.agent_memories.items():
                agent_file = self.memory_dir / f"{agent_id}_memories.json"
                memory_data = []

                for memory in memories:
                    data = asdict(memory)
                    # Convert enums to strings for JSON serialization
                    data['memory_type'] = memory.memory_type.value
                    data['importance'] = memory.importance.value
                    memory_data.append(data)

                with open(agent_file, 'w') as f:
                    json.dump(memory_data, f, indent=2, cls=EnumJSONEncoder)
            
            # Save shared memories
            shared_file = self.memory_dir / "shared_memories.json"
            shared_data = []

            for memory in self.shared_memories:
                data = asdict(memory)
                # Convert enums to strings for JSON serialization
                data['memory_type'] = memory.memory_type.value
                data['importance'] = memory.importance.value
                shared_data.append(data)

            with open(shared_file, 'w') as f:
                json.dump(shared_data, f, indent=2, cls=EnumJSONEncoder)
            
            # Save relationships
            relationships_file = self.memory_dir / "relationships.json"
            relationships_data = {
                agent1: dict(relationships) 
                for agent1, relationships in self.agent_relationships.items()
            }
            
            with open(relationships_file, 'w') as f:
                json.dump(relationships_data, f, indent=2, cls=EnumJSONEncoder)
    
    def load_memories(self):
        """Load memories from disk"""
        try:
            # Load agent memories
            for memory_file in self.memory_dir.glob("*_memories.json"):
                agent_id = memory_file.stem.replace("_memories", "")
                
                with open(memory_file, 'r') as f:
                    memory_data = json.load(f)
                
                memories = []
                for data in memory_data:
                    # Convert enum strings back to enums
                    data['memory_type'] = MemoryType(data['memory_type'])
                    data['importance'] = MemoryImportance(data['importance'])
                    
                    memory = Memory(**data)
                    memories.append(memory)
                    self.memory_index[memory.id] = memory
                
                self.agent_memories[agent_id] = memories
            
            # Load shared memories
            shared_file = self.memory_dir / "shared_memories.json"
            if shared_file.exists():
                with open(shared_file, 'r') as f:
                    shared_data = json.load(f)
                
                for data in shared_data:
                    data['memory_type'] = MemoryType(data['memory_type'])
                    data['importance'] = MemoryImportance(data['importance'])
                    self.shared_memories.append(SharedMemory(**data))
            
            # Load relationships
            relationships_file = self.memory_dir / "relationships.json"
            if relationships_file.exists():
                with open(relationships_file, 'r') as f:
                    relationships_data = json.load(f)
                
                for agent1, relationships in relationships_data.items():
                    for agent2, value in relationships.items():
                        self.agent_relationships[agent1][agent2] = value
        
        except Exception as e:
            print(f"Warning: Could not load memories: {e}")
    
    def get_system_stats(self) -> Dict[str, Any]:
        """Get overall system statistics"""
        with self.lock:
            total_memories = sum(len(memories) for memories in self.agent_memories.values())
            total_shared = len(self.shared_memories)
            total_agents = len(self.agent_memories)
            
            return {
                "total_memories": total_memories,
                "total_shared_memories": total_shared,
                "total_agents": total_agents,
                "agent_stats": dict(self.memory_stats),
                "memory_index_size": len(self.memory_index),
                "active_communication_channels": len(self.communication_channels)
            }

# Global memory system instance
agent_memory_system = AgentMemorySystem()

# Cleanup function for graceful shutdown
def cleanup_memory_system():
    """Save memories before shutdown"""
    agent_memory_system.save_memories()
    print("💾 Agent memories saved successfully")
