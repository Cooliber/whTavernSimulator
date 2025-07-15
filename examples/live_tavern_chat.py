#!/usr/bin/env python3
"""
Live Tavern Chat - Żywe życie karczmy w czasie rzeczywistym
Pokazuje ciągłe rozmowy i interakcje między agentami
"""

import streamlit as st
import time
import random
from datetime import datetime, timedelta
import threading
from typing import List, Dict
import json

# Page configuration
st.set_page_config(
    page_title="🏰 Żywe Życie Karczmy",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

class LiveTavernChat:
    """System żywego życia karczmy z ciągłymi rozmowami"""
    
    def __init__(self):
        self.agents = {
            'Karczmarz': {
                'personality': 'friendly',
                'topics': ['piwo', 'jedzenie', 'plotki', 'goście', 'handel'],
                'mood': 'happy',
                'activity_level': 0.8
            },
            'Skrytobójca': {
                'personality': 'mysterious',
                'topics': ['informacje', 'sekrety', 'niebezpieczeństwo', 'zlecenia'],
                'mood': 'mysterious',
                'activity_level': 0.6
            },
            'Wiedźma': {
                'personality': 'mystical',
                'topics': ['magia', 'przepowiednie', 'mikstury', 'zaklęcia'],
                'mood': 'mysterious',
                'activity_level': 0.7
            },
            'Czempion': {
                'personality': 'heroic',
                'topics': ['honor', 'walka', 'sprawiedliwość', 'przygody'],
                'mood': 'confident',
                'activity_level': 0.9
            },
            'Zwiadowca': {
                'personality': 'observant',
                'topics': ['drogi', 'niebezpieczeństwa', 'podróże', 'obserwacje'],
                'mood': 'alert',
                'activity_level': 0.5
            }
        }
        
        self.conversation_templates = {
            'greeting': [
                "{sender} kiwa głową w stronę {receiver}",
                "{sender} wita się z {receiver}",
                "{sender} uśmiecha się do {receiver}"
            ],
            'tavern_talk': [
                "{sender}: Słyszałeś o dziwnych wydarzeniach w okolicy?",
                "{sender}: To piwo jest naprawdę dobre dzisiaj!",
                "{sender}: Widziałem dziwne światła w lesie...",
                "{sender}: Handel idzie dobrze w tym sezonie",
                "{sender}: Pogoda ostatnio dziwna, nie uważasz?"
            ],
            'rumors': [
                "{sender} szepcze: Podobno w starym zamku dzieje się coś dziwnego...",
                "{sender} mówi cicho: Słyszałem, że bandyci grasują na północnej drodze",
                "{sender} szeptem: Ktoś widział dziwne stworzenia w bagnie"
            ],
            'reactions': [
                "{receiver}: Naprawdę? Opowiedz więcej!",
                "{receiver}: To interesujące...",
                "{receiver}: Hmm, trzeba być ostrożnym",
                "{receiver}: Dzięki za ostrzeżenie",
                "{receiver} kiwa głową ze zrozumieniem"
            ]
        }
        
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize session state for live chat"""
        if 'live_tavern_state' not in st.session_state:
            st.session_state.live_tavern_state = {
                'messages': [],
                'last_activity': {},
                'conversation_pairs': [],
                'tavern_mood': 'peaceful',
                'time_of_day': 'evening',
                'running': False,
                'message_counter': 0
            }
            
            # Initialize last activity for each agent
            for agent in self.agents.keys():
                st.session_state.live_tavern_state['last_activity'][agent] = datetime.now()
    
    def generate_natural_conversation(self) -> Dict:
        """Generate natural conversation between agents"""
        # Select active agents based on activity level
        active_agents = [
            agent for agent, data in self.agents.items()
            if random.random() < data['activity_level']
        ]
        
        if len(active_agents) < 2:
            active_agents = list(self.agents.keys())[:2]
        
        sender = random.choice(active_agents)
        receiver = random.choice([a for a in active_agents if a != sender])
        
        # Choose conversation type based on time and mood
        conversation_types = ['greeting', 'tavern_talk', 'rumors']
        weights = [0.2, 0.6, 0.2]  # Most conversations are tavern talk
        
        conv_type = random.choices(conversation_types, weights=weights)[0]
        
        # Generate message
        template = random.choice(self.conversation_templates[conv_type])
        message = template.format(sender=sender, receiver=receiver)
        
        # Generate reaction if it's not a greeting
        reaction = None
        if conv_type != 'greeting' and random.random() > 0.3:
            reaction_template = random.choice(self.conversation_templates['reactions'])
            reaction = reaction_template.format(sender=sender, receiver=receiver)
        
        st.session_state.live_tavern_state['message_counter'] += 1
        
        conversation = {
            'id': f"live_{st.session_state.live_tavern_state['message_counter']}",
            'sender': sender,
            'receiver': receiver,
            'message': message,
            'reaction': reaction,
            'type': conv_type,
            'timestamp': datetime.now(),
            'mood': self.agents[sender]['mood']
        }
        
        return conversation
    
    def add_conversation_to_chat(self, conversation: Dict):
        """Add conversation to chat display"""
        messages = st.session_state.live_tavern_state['messages']
        
        # Add main message
        messages.append({
            'sender': conversation['sender'],
            'receiver': conversation['receiver'],
            'content': conversation['message'],
            'timestamp': conversation['timestamp'],
            'type': conversation['type'],
            'mood': conversation['mood']
        })
        
        # Add reaction if exists
        if conversation['reaction']:
            time.sleep(0.5)  # Small delay for natural flow
            messages.append({
                'sender': conversation['receiver'],
                'receiver': conversation['sender'],
                'content': conversation['reaction'],
                'timestamp': datetime.now(),
                'type': 'reaction',
                'mood': self.agents[conversation['receiver']]['mood']
            })
        
        # Keep only last 50 messages for performance
        if len(messages) > 50:
            st.session_state.live_tavern_state['messages'] = messages[-50:]
        
        # Update last activity
        st.session_state.live_tavern_state['last_activity'][conversation['sender']] = datetime.now()
        st.session_state.live_tavern_state['last_activity'][conversation['receiver']] = datetime.now()
    
    def get_agent_status(self, agent: str) -> str:
        """Get current status of agent"""
        last_activity = st.session_state.live_tavern_state['last_activity'].get(agent, datetime.now())
        time_since = (datetime.now() - last_activity).total_seconds()
        
        if time_since < 30:
            return "🟢 Aktywny"
        elif time_since < 120:
            return "🟡 Spokojny"
        else:
            return "🔴 Cichy"
    
    def render_live_chat(self):
        """Render live chat interface"""
        st.title("🏰 Żywe Życie Karczmy")
        st.markdown("*Obserwuj naturalne rozmowy i interakcje między mieszkańcami karczmy*")
        
        # Control panel
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if st.button("🎭 Rozpocznij Życie Karczmy", type="primary"):
                st.session_state.live_tavern_state['running'] = True
                st.rerun()
        
        with col2:
            if st.button("⏸️ Pauza"):
                st.session_state.live_tavern_state['running'] = False
                st.rerun()
        
        with col3:
            if st.button("🗑️ Wyczyść"):
                st.session_state.live_tavern_state['messages'] = []
                st.rerun()
        
        # Agent status panel
        st.subheader("👥 Status Agentów")
        agent_cols = st.columns(5)
        
        for i, (agent, data) in enumerate(self.agents.items()):
            with agent_cols[i]:
                status = self.get_agent_status(agent)
                st.metric(
                    agent,
                    status,
                    f"Nastrój: {data['mood']}"
                )
        
        # Chat display
        st.subheader("💬 Rozmowy w Karczmie")
        
        # Create chat container
        chat_container = st.container()
        
        with chat_container:
            messages = st.session_state.live_tavern_state.get('messages', [])
            
            if not messages:
                st.info("🏰 Karczma jest cicha... Kliknij 'Rozpocznij Życie Karczmy' aby zobaczyć rozmowy!")
            else:
                # Display messages
                for msg in messages[-20:]:  # Show last 20 messages
                    self.render_message(msg)
        
        # Auto-generate conversations if running
        if st.session_state.live_tavern_state.get('running', False):
            self.auto_generate_conversations()
    
    def render_message(self, message: Dict):
        """Render individual message"""
        timestamp = message['timestamp'].strftime("%H:%M:%S")
        
        # Choose emoji based on message type
        type_emojis = {
            'greeting': '👋',
            'tavern_talk': '🍺',
            'rumors': '🤫',
            'reaction': '💭'
        }
        
        emoji = type_emojis.get(message['type'], '💬')
        
        # Choose color based on mood
        mood_colors = {
            'happy': '#4CAF50',
            'mysterious': '#9C27B0',
            'confident': '#FF9800',
            'alert': '#2196F3'
        }
        
        color = mood_colors.get(message['mood'], '#666666')
        
        # Render message
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, {color}20, transparent);
            border-left: 3px solid {color};
            padding: 10px;
            margin: 5px 0;
            border-radius: 5px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong>{emoji} {message['sender']} → {message['receiver']}</strong>
                <small style="color: #888;">{timestamp}</small>
            </div>
            <div style="margin-top: 5px; font-style: italic;">
                {message['content']}
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def auto_generate_conversations(self):
        """Auto-generate conversations in background"""
        # Generate conversation every 3-8 seconds
        if 'last_generation' not in st.session_state:
            st.session_state.last_generation = time.time()
        
        current_time = time.time()
        time_since_last = current_time - st.session_state.last_generation
        
        # Random interval between 3-8 seconds
        next_interval = random.uniform(3, 8)
        
        if time_since_last >= next_interval:
            conversation = self.generate_natural_conversation()
            self.add_conversation_to_chat(conversation)
            st.session_state.last_generation = current_time
            st.rerun()

def main():
    """Main application function"""
    live_chat = LiveTavernChat()
    
    # Sidebar with settings
    with st.sidebar:
        st.header("⚙️ Ustawienia Karczmy")
        
        # Time of day
        time_of_day = st.selectbox(
            "🕐 Pora dnia",
            ["morning", "afternoon", "evening", "night"],
            index=2
        )
        st.session_state.live_tavern_state['time_of_day'] = time_of_day
        
        # Tavern mood
        tavern_mood = st.selectbox(
            "🎭 Nastrój karczmy",
            ["peaceful", "lively", "tense", "mysterious"],
            index=0
        )
        st.session_state.live_tavern_state['tavern_mood'] = tavern_mood
        
        # Statistics
        st.header("📊 Statystyki")
        message_count = len(st.session_state.live_tavern_state.get('messages', []))
        st.metric("Wiadomości", message_count)
        
        running_status = "🟢 Aktywne" if st.session_state.live_tavern_state.get('running', False) else "🔴 Zatrzymane"
        st.metric("Status", running_status)
        
        # Info
        st.markdown("---")
        st.markdown("""
        ### 🏰 O Systemie
        
        Ten interfejs pokazuje **żywe życie karczmy** z naturalnymi rozmowami między agentami.
        
        **Funkcje:**
        - 🎭 Automatyczne rozmowy
        - 👥 5 unikalnych agentów
        - 💬 Naturalne dialogi
        - 📊 Status w czasie rzeczywistym
        - 🎨 Kolorowe interfejsy
        """)
    
    # Render main chat
    live_chat.render_live_chat()
    
    # Auto-refresh every 2 seconds if running
    if st.session_state.live_tavern_state.get('running', False):
        time.sleep(2)
        st.rerun()

if __name__ == "__main__":
    main()
