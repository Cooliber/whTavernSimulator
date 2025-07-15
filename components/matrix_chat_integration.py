#!/usr/bin/env python3
"""
Matrix Chat Integration with Existing Agent System
Seamlessly converts agent communications to Matrix Chat messages
"""

import streamlit as st
from typing import Dict, List, Optional, Any
from datetime import datetime
import time
import random

from .matrix_chat_interface import MatrixChatInterface, ChatMessage
from services.agent_manager import AgentManager, AgentCommunication
from core.tavern_simulator import TavernSimulator

class MatrixChatIntegration:
    """
    Integrates Matrix Chat Interface with existing agent system
    Provides seamless conversion and real-time updates
    """
    
    def __init__(self, chat_interface: MatrixChatInterface):
        self.chat_interface = chat_interface
        self.agent_manager = None
        self.tavern_simulator = None
        self.last_processed_communication = 0
        self.last_processed_event = 0
        
        # Agent personality mapping for better message conversion
        self.agent_personalities = {
            'Karczmarz': {
                'default_emotion': 'happy',
                'message_style': 'friendly',
                'color_theme': 'gold',
                'preferred_effects': ['glow', 'typewriter']
            },
            'Skrytobójca': {
                'default_emotion': 'mysterious',
                'message_style': 'secretive',
                'color_theme': 'purple',
                'preferred_effects': ['matrix', 'fade']
            },
            'Wiedźma': {
                'default_emotion': 'mysterious',
                'message_style': 'mystical',
                'color_theme': 'purple',
                'preferred_effects': ['matrix', 'glow', 'typewriter']
            },
            'Czempion': {
                'default_emotion': 'happy',
                'message_style': 'heroic',
                'color_theme': 'gold',
                'preferred_effects': ['glow']
            },
            'Zwiadowca': {
                'default_emotion': 'calm',
                'message_style': 'observant',
                'color_theme': 'green',
                'preferred_effects': ['fade']
            }
        }
    
    def set_agent_manager(self, agent_manager: AgentManager):
        """Set the agent manager for integration"""
        self.agent_manager = agent_manager
    
    def set_tavern_simulator(self, tavern_simulator: TavernSimulator):
        """Set the tavern simulator for integration"""
        self.tavern_simulator = tavern_simulator
    
    def convert_agent_communication_to_chat_message(self, comm: AgentCommunication) -> ChatMessage:
        """Convert agent communication to Matrix Chat message"""
        
        # Get sender personality
        sender_personality = self.agent_personalities.get(comm.sender, {
            'default_emotion': 'calm',
            'message_style': 'neutral',
            'color_theme': 'blue',
            'preferred_effects': ['fade']
        })
        
        # Determine message type based on communication type and priority
        message_type = self._determine_message_type(comm)
        
        # Determine emotion based on priority and content
        emotion = self._determine_emotion(comm, sender_personality)
        
        # Select appropriate effects
        effects = self._select_effects(comm, sender_personality, message_type)
        
        # Generate unique message ID
        message_id = f"agent_comm_{comm.sender}_{comm.receiver}_{int(time.time() * 1000)}"
        
        return ChatMessage(
            id=message_id,
            sender=comm.sender,
            receiver=comm.receiver,
            content=comm.message,
            message_type=message_type,
            emotion=emotion,
            priority=comm.priority,
            timestamp=comm.timestamp,
            effects=effects,
            color_theme=sender_personality['color_theme'],
            duration=3.0 + comm.priority * 0.5
        )
    
    def _determine_message_type(self, comm: AgentCommunication) -> str:
        """Determine message type based on communication"""
        if comm.message_type == "warning" and comm.priority >= 8:
            return "shout"
        elif comm.message_type == "warning":
            return "whisper"
        elif comm.priority >= 9:
            return "shout"
        elif "magic" in comm.message.lower() or "spell" in comm.message.lower():
            return "magic"
        elif any(word in comm.message.lower() for word in ["think", "consider", "wonder"]):
            return "thought"
        elif any(word in comm.message.lower() for word in ["move", "attack", "defend", "act"]):
            return "action"
        else:
            return "whisper"
    
    def _determine_emotion(self, comm: AgentCommunication, personality: Dict) -> str:
        """Determine emotion based on communication and personality"""
        # High priority messages are urgent
        if comm.priority >= 9:
            return "urgent"
        elif comm.priority >= 7:
            return "angry" if "threat" in comm.message.lower() else "urgent"
        
        # Check message content for emotional keywords
        message_lower = comm.message.lower()
        if any(word in message_lower for word in ["danger", "threat", "attack", "enemy"]):
            return "angry"
        elif any(word in message_lower for word in ["magic", "spell", "mystery", "secret"]):
            return "mysterious"
        elif any(word in message_lower for word in ["good", "great", "excellent", "success"]):
            return "happy"
        else:
            return personality['default_emotion']
    
    def _select_effects(self, comm: AgentCommunication, personality: Dict, message_type: str) -> List[str]:
        """Select appropriate effects for the message"""
        effects = []
        
        # Add personality-based effects
        if comm.priority <= 5:
            effects.extend(personality['preferred_effects'][:1])  # Use first effect for low priority
        else:
            effects.extend(personality['preferred_effects'])  # Use all effects for high priority
        
        # Add message type specific effects
        if message_type == "shout":
            effects.extend(["shake", "glow"])
        elif message_type == "magic":
            effects.extend(["matrix", "glow"])
        elif message_type == "thought":
            effects.append("typewriter")
        elif message_type == "action":
            effects.append("glow")
        
        # Remove duplicates and limit to 3 effects for performance
        effects = list(set(effects))[:3]
        
        return effects
    
    def process_agent_communications(self):
        """Process new agent communications and convert to chat messages"""
        if not self.agent_manager:
            return
        
        try:
            # Get recent communications
            recent_comms = self.agent_manager.get_communication_history(limit=20)
            
            # Process only new communications
            new_comms = [
                comm for comm in recent_comms 
                if self._is_new_communication(comm)
            ]
            
            for comm_data in new_comms:
                # Convert dict back to AgentCommunication object
                comm = AgentCommunication(
                    sender=comm_data['sender'],
                    receiver=comm_data['receiver'],
                    message=comm_data['message'],
                    message_type=comm_data['type'],
                    timestamp=datetime.fromisoformat(comm_data['timestamp']),
                    priority=comm_data['priority']
                )
                
                # Convert to chat message
                chat_message = self.convert_agent_communication_to_chat_message(comm)
                
                # Add to chat interface
                self.chat_interface.add_message(chat_message)
                
                # Update last processed
                self.last_processed_communication = time.time()
                
        except Exception as e:
            st.error(f"Error processing agent communications: {e}")
    
    def _is_new_communication(self, comm_data: Dict) -> bool:
        """Check if communication is new (not yet processed)"""
        try:
            comm_time = datetime.fromisoformat(comm_data['timestamp']).timestamp()
            return comm_time > self.last_processed_communication
        except:
            return True  # Process if we can't determine timestamp
    
    def process_tavern_events(self):
        """Process tavern events and convert to chat messages"""
        if not self.tavern_simulator:
            return
        
        try:
            # Get recent events from tavern
            if hasattr(self.tavern_simulator, 'get_recent_events'):
                events = self.tavern_simulator.get_recent_events()
                
                for event in events:
                    if self._is_new_event(event):
                        chat_message = self._convert_event_to_chat_message(event)
                        if chat_message:
                            self.chat_interface.add_message(chat_message)
                
                self.last_processed_event = time.time()
                
        except Exception as e:
            st.error(f"Error processing tavern events: {e}")
    
    def _is_new_event(self, event) -> bool:
        """Check if event is new"""
        try:
            if hasattr(event, 'timestamp'):
                event_time = event.timestamp.timestamp() if hasattr(event.timestamp, 'timestamp') else event.timestamp
                return event_time > self.last_processed_event
            return True
        except:
            return True
    
    def _convert_event_to_chat_message(self, event) -> Optional[ChatMessage]:
        """Convert tavern event to chat message"""
        try:
            # Extract event information
            event_type = getattr(event, 'type', 'unknown')
            description = getattr(event, 'description', str(event))
            
            # Determine participants
            if hasattr(event, 'character1') and hasattr(event, 'character2'):
                sender = event.character1.name
                receiver = event.character2.name
            elif hasattr(event, 'character'):
                sender = event.character.name
                receiver = "Wszyscy"
            else:
                sender = "Karczma"
                receiver = "Wszyscy"
            
            # Determine message properties based on event type
            if event_type == "character_interaction":
                message_type = "action"
                emotion = "happy"
                priority = 5
            elif event_type == "conflict":
                message_type = "shout"
                emotion = "angry"
                priority = 8
            elif event_type == "rumor":
                message_type = "whisper"
                emotion = "mysterious"
                priority = 6
            else:
                message_type = "action"
                emotion = "calm"
                priority = 4
            
            message_id = f"event_{event_type}_{int(time.time() * 1000)}"
            
            return ChatMessage(
                id=message_id,
                sender=sender,
                receiver=receiver,
                content=description,
                message_type=message_type,
                emotion=emotion,
                priority=priority,
                timestamp=datetime.now(),
                effects=["glow", "fade"],
                color_theme="blue",
                duration=4.0
            )
            
        except Exception as e:
            st.error(f"Error converting event to chat message: {e}")
            return None
    
    def start_real_time_integration(self):
        """Start real-time integration with agent system"""
        # This would be called periodically to check for new communications
        self.process_agent_communications()
        self.process_tavern_events()
    
    def add_system_message(self, content: str, message_type: str = "action", priority: int = 5):
        """Add a system message to the chat"""
        message = ChatMessage(
            id=f"system_{int(time.time() * 1000)}",
            sender="System",
            receiver="Wszyscy",
            content=content,
            message_type=message_type,
            emotion="calm",
            priority=priority,
            timestamp=datetime.now(),
            effects=["typewriter"],
            color_theme="blue",
            duration=3.0
        )
        
        self.chat_interface.add_message(message)
    
    def simulate_agent_conversation(self, num_messages: int = 5):
        """Simulate a conversation between agents for demo purposes"""
        agents = list(self.agent_personalities.keys())
        
        conversation_templates = [
            ("Karczmarz", "Wszyscy", "Witajcie w mojej karczmie! Dzisiaj mamy specjalne piwo z dalekich krain.", "shout", "happy", 6),
            ("Skrytobójca", "Wiedźma", "Słyszałem dziwne plotki o magicznych artefaktach w okolicy...", "whisper", "mysterious", 7),
            ("Wiedźma", "Skrytobójca", "Gwiazdy mówią o nadchodzących zmianach. Coś się dzieje.", "thought", "mysterious", 8),
            ("Czempion", "Wszyscy", "Jestem gotów bronić tej karczmy przed każdym zagrożeniem!", "shout", "happy", 7),
            ("Zwiadowca", "Karczmarz", "Widziałem dziwne ślady w lesie. Może to nic, ale...", "whisper", "calm", 6),
            ("Karczmarz", "Zwiadowca", "Dziękuję za ostrzeżenie. Będę czujny.", "action", "calm", 5),
            ("Wiedźma", "Wszyscy", "Czuję magię w powietrzu... Coś potężnego się zbliża.", "magic", "mysterious", 9),
            ("Skrytobójca", "Czempion", "Twój miecz może być potrzebny wcześniej niż myślisz.", "whisper", "urgent", 8)
        ]
        
        for i in range(min(num_messages, len(conversation_templates))):
            sender, receiver, content, msg_type, emotion, priority = conversation_templates[i]
            
            message = ChatMessage(
                id=f"demo_conv_{i}_{int(time.time() * 1000)}",
                sender=sender,
                receiver=receiver,
                content=content,
                message_type=msg_type,
                emotion=emotion,
                priority=priority,
                timestamp=datetime.now(),
                effects=self.agent_personalities[sender]['preferred_effects'],
                color_theme=self.agent_personalities[sender]['color_theme'],
                duration=3.0 + priority * 0.3
            )
            
            self.chat_interface.add_message(message)
            
            # Add small delay between messages for realistic flow
            time.sleep(0.5)
