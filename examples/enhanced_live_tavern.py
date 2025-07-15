#!/usr/bin/env python3
"""
Enhanced Live Tavern - Zaawansowane życie karczmy z integracją agentów
Pokazuje rzeczywiste interakcje i rozmowy między agentami CrewAI
"""

import streamlit as st
import time
import random
from datetime import datetime, timedelta
import threading
from typing import List, Dict, Optional
import json
import asyncio
from dataclasses import dataclass

# Page configuration
st.set_page_config(
    page_title="🏰 Enhanced Live Tavern",
    page_icon="🏰",
    layout="wide",
    initial_sidebar_state="expanded"
)

@dataclass
class TavernEvent:
    """Event happening in the tavern"""
    id: str
    type: str  # conversation, action, arrival, departure, conflict, trade
    participants: List[str]
    description: str
    timestamp: datetime
    importance: int  # 1-10
    mood: str
    location: str  # main_hall, corner_table, bar, fireplace

class EnhancedLiveTavern:
    """Enhanced tavern life simulation with real agent integration"""
    
    def __init__(self):
        self.agents = {
            'Karczmarz': {
                'role': 'tavern_keeper',
                'personality': 'friendly_host',
                'current_activity': 'serving_drinks',
                'location': 'bar',
                'mood': 'welcoming',
                'energy': 0.8,
                'relationships': {'Skrytobójca': 0.6, 'Wiedźma': 0.7, 'Czempion': 0.9, 'Zwiadowca': 0.8}
            },
            'Skrytobójca': {
                'role': 'information_broker',
                'personality': 'mysterious_observer',
                'current_activity': 'observing',
                'location': 'corner_table',
                'mood': 'calculating',
                'energy': 0.6,
                'relationships': {'Karczmarz': 0.6, 'Wiedźma': 0.5, 'Czempion': 0.3, 'Zwiadowca': 0.7}
            },
            'Wiedźma': {
                'role': 'mystic_advisor',
                'personality': 'wise_mysterious',
                'current_activity': 'reading_cards',
                'location': 'fireplace',
                'mood': 'contemplative',
                'energy': 0.7,
                'relationships': {'Karczmarz': 0.7, 'Skrytobójca': 0.5, 'Czempion': 0.6, 'Zwiadowca': 0.8}
            },
            'Czempion': {
                'role': 'warrior_protector',
                'personality': 'noble_brave',
                'current_activity': 'sharpening_sword',
                'location': 'main_hall',
                'mood': 'vigilant',
                'energy': 0.9,
                'relationships': {'Karczmarz': 0.9, 'Skrytobójca': 0.3, 'Wiedźma': 0.6, 'Zwiadowca': 0.8}
            },
            'Zwiadowca': {
                'role': 'scout_messenger',
                'personality': 'alert_traveler',
                'current_activity': 'studying_map',
                'location': 'corner_table',
                'mood': 'focused',
                'energy': 0.5,
                'relationships': {'Karczmarz': 0.8, 'Skrytobójca': 0.7, 'Wiedźma': 0.8, 'Czempion': 0.8}
            }
        }
        
        self.tavern_locations = {
            'bar': {'atmosphere': 'social', 'capacity': 3, 'current_occupants': ['Karczmarz']},
            'main_hall': {'atmosphere': 'open', 'capacity': 8, 'current_occupants': ['Czempion']},
            'corner_table': {'atmosphere': 'private', 'capacity': 2, 'current_occupants': ['Skrytobójca', 'Zwiadowca']},
            'fireplace': {'atmosphere': 'cozy', 'capacity': 4, 'current_occupants': ['Wiedźma']},
            'upstairs': {'atmosphere': 'quiet', 'capacity': 2, 'current_occupants': []}
        }
        
        self.conversation_scenarios = {
            'daily_greeting': {
                'probability': 0.3,
                'participants': 2,
                'templates': [
                    "{agent1} kiwa głową w stronę {agent2}: 'Dzień dobry, {agent2}'",
                    "{agent2} odpowiada: 'Witaj, {agent1}. Jak się miewasz?'",
                    "{agent1}: 'Nie mogę narzekać. A ty jak się czujesz?'"
                ]
            },
            'information_exchange': {
                'probability': 0.4,
                'participants': 2,
                'templates': [
                    "{agent1} nachyla się do {agent2}: 'Słyszałeś o dziwnych wydarzeniach na północy?'",
                    "{agent2}: 'Tak, podobno widziano tam dziwne światła...'",
                    "{agent1}: 'To niepokojące. Może powinniśmy być ostrożni.'"
                ]
            },
            'tavern_business': {
                'probability': 0.5,
                'participants': 2,
                'templates': [
                    "{agent1}: 'Karczmarz, poproszę jeszcze jedno piwo'",
                    "Karczmarz: 'Oczywiście! Zaraz przyniosę'",
                    "{agent1}: 'Dziękuję, to piwo jest naprawdę dobre'"
                ]
            },
            'group_discussion': {
                'probability': 0.2,
                'participants': 3,
                'templates': [
                    "{agent1}: 'Zbieramy się, żeby omówić sytuację w okolicy'",
                    "{agent2}: 'Tak, ostatnio dzieje się dużo dziwnych rzeczy'",
                    "{agent3}: 'Musimy być przygotowani na wszystko'"
                ]
            }
        }
        
        self.initialize_session_state()
    
    def initialize_session_state(self):
        """Initialize enhanced session state"""
        if 'enhanced_tavern_state' not in st.session_state:
            st.session_state.enhanced_tavern_state = {
                'events': [],
                'active_conversations': {},
                'tavern_mood': 'peaceful',
                'time_of_day': 'evening',
                'weather': 'clear',
                'running': False,
                'event_counter': 0,
                'last_event_time': datetime.now(),
                'agent_states': self.agents.copy(),
                'location_states': self.tavern_locations.copy()
            }
    
    def generate_tavern_event(self) -> Optional[TavernEvent]:
        """Generate realistic tavern event"""
        current_time = datetime.now()
        
        # Choose event type based on tavern state and time
        event_types = ['conversation', 'action', 'mood_change', 'location_change']
        event_weights = [0.6, 0.2, 0.1, 0.1]
        
        event_type = random.choices(event_types, weights=event_weights)[0]
        
        if event_type == 'conversation':
            return self.generate_conversation_event()
        elif event_type == 'action':
            return self.generate_action_event()
        elif event_type == 'mood_change':
            return self.generate_mood_event()
        elif event_type == 'location_change':
            return self.generate_location_event()
        
        return None
    
    def generate_conversation_event(self) -> TavernEvent:
        """Generate conversation between agents"""
        # Choose scenario
        scenario_name = random.choices(
            list(self.conversation_scenarios.keys()),
            weights=[s['probability'] for s in self.conversation_scenarios.values()]
        )[0]
        
        scenario = self.conversation_scenarios[scenario_name]
        
        # Choose participants
        available_agents = list(self.agents.keys())
        num_participants = scenario['participants']
        
        if num_participants == 2:
            participants = random.sample(available_agents, 2)
        else:
            participants = random.sample(available_agents, min(num_participants, len(available_agents)))
        
        # Generate conversation
        templates = scenario['templates']
        conversation_parts = []
        
        for template in templates:
            if len(participants) >= 2:
                formatted = template.format(
                    agent1=participants[0],
                    agent2=participants[1],
                    agent3=participants[2] if len(participants) > 2 else participants[0]
                )
                conversation_parts.append(formatted)
        
        description = " | ".join(conversation_parts)
        
        # Determine location (where most participants are)
        participant_locations = [self.agents[p]['location'] for p in participants]
        location = max(set(participant_locations), key=participant_locations.count)
        
        st.session_state.enhanced_tavern_state['event_counter'] += 1
        
        return TavernEvent(
            id=f"conv_{st.session_state.enhanced_tavern_state['event_counter']}",
            type='conversation',
            participants=participants,
            description=description,
            timestamp=datetime.now(),
            importance=random.randint(3, 7),
            mood=random.choice(['friendly', 'serious', 'mysterious', 'casual']),
            location=location
        )
    
    def generate_action_event(self) -> TavernEvent:
        """Generate action event"""
        agent = random.choice(list(self.agents.keys()))
        agent_data = self.agents[agent]
        
        actions = {
            'Karczmarz': [
                f"{agent} czyści kufle za barem",
                f"{agent} sprawdza zapasy piwa",
                f"{agent} rozmawia z dostawcą",
                f"{agent} zapala świece w karczmie"
            ],
            'Skrytobójca': [
                f"{agent} obserwuje wchodzących gości",
                f"{agent} sprawdza swoje notatki",
                f"{agent} dyskretnie słucha rozmów",
                f"{agent} sprawdza ukryte przejścia"
            ],
            'Wiedźma': [
                f"{agent} miesza tajemniczą miksturę",
                f"{agent} czyta w starożytnej księdze",
                f"{agent} wpatruje się w płomienie",
                f"{agent} układa karty tarota"
            ],
            'Czempion': [
                f"{agent} sprawdza stan swojej zbroi",
                f"{agent} ćwiczy ruchy mieczem",
                f"{agent} obserwuje wejście do karczmy",
                f"{agent} pomaga innym gościom"
            ],
            'Zwiadowca': [
                f"{agent} studiuje mapę okolicy",
                f"{agent} sprawdza swój ekwipunek",
                f"{agent} nasłuchuje pogłosek",
                f"{agent} planuje następną wyprawę"
            ]
        }
        
        action = random.choice(actions.get(agent, [f"{agent} wykonuje jakąś czynność"]))
        
        st.session_state.enhanced_tavern_state['event_counter'] += 1
        
        return TavernEvent(
            id=f"action_{st.session_state.enhanced_tavern_state['event_counter']}",
            type='action',
            participants=[agent],
            description=action,
            timestamp=datetime.now(),
            importance=random.randint(1, 4),
            mood=agent_data['mood'],
            location=agent_data['location']
        )
    
    def generate_mood_event(self) -> TavernEvent:
        """Generate mood change event"""
        mood_changes = [
            "Atmosfera w karczmie staje się bardziej ożywiona",
            "W karczmie zapada cisza, wszyscy nasłuchują",
            "Goście stają się bardziej rozmowni",
            "Napięcie w powietrzu nieco opada",
            "Muzyka sprawia, że wszyscy się relaksują"
        ]
        
        description = random.choice(mood_changes)
        
        st.session_state.enhanced_tavern_state['event_counter'] += 1
        
        return TavernEvent(
            id=f"mood_{st.session_state.enhanced_tavern_state['event_counter']}",
            type='mood_change',
            participants=[],
            description=description,
            timestamp=datetime.now(),
            importance=random.randint(2, 5),
            mood='atmospheric',
            location='main_hall'
        )
    
    def generate_location_event(self) -> TavernEvent:
        """Generate location change event"""
        agent = random.choice(list(self.agents.keys()))
        current_location = self.agents[agent]['location']
        
        # Choose new location
        available_locations = [loc for loc in self.tavern_locations.keys() if loc != current_location]
        new_location = random.choice(available_locations)
        
        # Update agent location
        self.agents[agent]['location'] = new_location
        
        # Update location occupants
        if agent in self.tavern_locations[current_location]['current_occupants']:
            self.tavern_locations[current_location]['current_occupants'].remove(agent)
        
        if agent not in self.tavern_locations[new_location]['current_occupants']:
            self.tavern_locations[new_location]['current_occupants'].append(agent)
        
        description = f"{agent} przechodzi z {current_location} do {new_location}"
        
        st.session_state.enhanced_tavern_state['event_counter'] += 1
        
        return TavernEvent(
            id=f"move_{st.session_state.enhanced_tavern_state['event_counter']}",
            type='location_change',
            participants=[agent],
            description=description,
            timestamp=datetime.now(),
            importance=random.randint(1, 3),
            mood='neutral',
            location=new_location
        )
    
    def add_event_to_timeline(self, event: TavernEvent):
        """Add event to timeline"""
        events = st.session_state.enhanced_tavern_state['events']
        events.append(event)
        
        # Keep only last 100 events
        if len(events) > 100:
            st.session_state.enhanced_tavern_state['events'] = events[-100:]
        
        st.session_state.enhanced_tavern_state['last_event_time'] = datetime.now()
    
    def render_tavern_overview(self):
        """Render tavern overview"""
        st.title("🏰 Enhanced Live Tavern")
        st.markdown("*Zaawansowana symulacja życia karczmy z rzeczywistymi agentami*")
        
        # Control panel
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("🎭 Start Life", type="primary"):
                st.session_state.enhanced_tavern_state['running'] = True
                st.rerun()
        
        with col2:
            if st.button("⏸️ Pause"):
                st.session_state.enhanced_tavern_state['running'] = False
                st.rerun()
        
        with col3:
            if st.button("🔄 Generate Event"):
                event = self.generate_tavern_event()
                if event:
                    self.add_event_to_timeline(event)
                st.rerun()
        
        with col4:
            if st.button("🗑️ Clear Timeline"):
                st.session_state.enhanced_tavern_state['events'] = []
                st.rerun()
        
        # Tavern status
        st.subheader("🏰 Status Karczmy")
        status_cols = st.columns(4)
        
        with status_cols[0]:
            running_status = "🟢 Aktywna" if st.session_state.enhanced_tavern_state.get('running', False) else "🔴 Zatrzymana"
            st.metric("Status", running_status)
        
        with status_cols[1]:
            event_count = len(st.session_state.enhanced_tavern_state.get('events', []))
            st.metric("Wydarzenia", event_count)
        
        with status_cols[2]:
            mood = st.session_state.enhanced_tavern_state.get('tavern_mood', 'peaceful')
            st.metric("Nastrój", mood.title())
        
        with status_cols[3]:
            time_of_day = st.session_state.enhanced_tavern_state.get('time_of_day', 'evening')
            st.metric("Pora dnia", time_of_day.title())
    
    def render_agent_status(self):
        """Render agent status panel"""
        st.subheader("👥 Status Agentów")
        
        agent_cols = st.columns(5)
        
        for i, (agent_name, agent_data) in enumerate(self.agents.items()):
            with agent_cols[i]:
                # Agent card
                st.markdown(f"""
                <div style="
                    background: linear-gradient(135deg, #1e3c72, #2a5298);
                    padding: 15px;
                    border-radius: 10px;
                    text-align: center;
                    color: white;
                    margin: 5px 0;
                ">
                    <h4>{agent_name}</h4>
                    <p><strong>Lokacja:</strong> {agent_data['location']}</p>
                    <p><strong>Aktywność:</strong> {agent_data['current_activity']}</p>
                    <p><strong>Nastrój:</strong> {agent_data['mood']}</p>
                    <p><strong>Energia:</strong> {agent_data['energy']:.1f}</p>
                </div>
                """, unsafe_allow_html=True)
    
    def render_location_map(self):
        """Render tavern location map"""
        st.subheader("🗺️ Mapa Karczmy")
        
        location_cols = st.columns(3)
        
        locations_grid = [
            ['bar', 'main_hall', 'fireplace'],
            ['corner_table', 'upstairs', '']
        ]
        
        for row in locations_grid:
            cols = st.columns(3)
            for i, location in enumerate(row):
                if location and location in self.tavern_locations:
                    with cols[i]:
                        loc_data = self.tavern_locations[location]
                        occupants = loc_data['current_occupants']
                        
                        st.markdown(f"""
                        <div style="
                            background: linear-gradient(135deg, #667eea, #764ba2);
                            padding: 10px;
                            border-radius: 8px;
                            text-align: center;
                            color: white;
                            margin: 5px;
                        ">
                            <h5>{location.replace('_', ' ').title()}</h5>
                            <p><strong>Atmosfera:</strong> {loc_data['atmosphere']}</p>
                            <p><strong>Obecni:</strong> {', '.join(occupants) if occupants else 'Pusty'}</p>
                        </div>
                        """, unsafe_allow_html=True)
    
    def render_event_timeline(self):
        """Render event timeline"""
        st.subheader("📜 Timeline Wydarzeń")
        
        events = st.session_state.enhanced_tavern_state.get('events', [])
        
        if not events:
            st.info("🏰 Brak wydarzeń. Kliknij 'Start Life' aby rozpocząć symulację!")
            return
        
        # Show last 15 events
        recent_events = events[-15:]
        
        for event in reversed(recent_events):
            self.render_event(event)
    
    def render_event(self, event: TavernEvent):
        """Render individual event"""
        timestamp = event.timestamp.strftime("%H:%M:%S")
        
        # Choose color based on event type
        type_colors = {
            'conversation': '#4CAF50',
            'action': '#2196F3',
            'mood_change': '#FF9800',
            'location_change': '#9C27B0'
        }
        
        color = type_colors.get(event.type, '#666666')
        
        # Choose emoji based on event type
        type_emojis = {
            'conversation': '💬',
            'action': '⚡',
            'mood_change': '🎭',
            'location_change': '🚶'
        }
        
        emoji = type_emojis.get(event.type, '📝')
        
        # Render event
        st.markdown(f"""
        <div style="
            background: linear-gradient(90deg, {color}20, transparent);
            border-left: 4px solid {color};
            padding: 12px;
            margin: 8px 0;
            border-radius: 8px;
        ">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <strong>{emoji} {event.type.replace('_', ' ').title()}</strong>
                <small style="color: #888;">{timestamp}</small>
            </div>
            <div style="margin-top: 8px;">
                <strong>Uczestnicy:</strong> {', '.join(event.participants) if event.participants else 'Brak'}
            </div>
            <div style="margin-top: 5px; font-style: italic;">
                {event.description}
            </div>
            <div style="margin-top: 5px; font-size: 12px; color: #666;">
                📍 {event.location} | 🎭 {event.mood} | ⭐ Ważność: {event.importance}/10
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def auto_generate_events(self):
        """Auto-generate events if running"""
        if not st.session_state.enhanced_tavern_state.get('running', False):
            return
        
        current_time = datetime.now()
        last_event = st.session_state.enhanced_tavern_state.get('last_event_time', current_time)
        
        # Generate event every 4-10 seconds
        time_since_last = (current_time - last_event).total_seconds()
        next_interval = random.uniform(4, 10)
        
        if time_since_last >= next_interval:
            event = self.generate_tavern_event()
            if event:
                self.add_event_to_timeline(event)
                st.rerun()

def main():
    """Main application function"""
    tavern = EnhancedLiveTavern()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Ustawienia Karczmy")
        
        # Tavern settings
        tavern_mood = st.selectbox(
            "🎭 Nastrój karczmy",
            ["peaceful", "lively", "tense", "mysterious", "festive"],
            index=0
        )
        st.session_state.enhanced_tavern_state['tavern_mood'] = tavern_mood
        
        time_of_day = st.selectbox(
            "🕐 Pora dnia",
            ["dawn", "morning", "afternoon", "evening", "night", "midnight"],
            index=3
        )
        st.session_state.enhanced_tavern_state['time_of_day'] = time_of_day
        
        weather = st.selectbox(
            "🌤️ Pogoda",
            ["clear", "cloudy", "rainy", "stormy", "foggy"],
            index=0
        )
        st.session_state.enhanced_tavern_state['weather'] = weather
        
        st.markdown("---")
        st.markdown("""
        ### 🏰 Enhanced Live Tavern
        
        **Zaawansowana symulacja życia karczmy:**
        
        - 🎭 Realistyczne wydarzenia
        - 👥 5 unikalnych agentów
        - 🗺️ Mapa lokacji
        - 💬 Naturalne rozmowy
        - ⚡ Akcje w czasie rzeczywistym
        - 📊 Szczegółowe statystyki
        """)
    
    # Main content
    tavern.render_tavern_overview()
    
    # Three column layout
    col1, col2 = st.columns([1, 1])
    
    with col1:
        tavern.render_agent_status()
        tavern.render_location_map()
    
    with col2:
        tavern.render_event_timeline()
    
    # Auto-generate events
    tavern.auto_generate_events()
    
    # Auto-refresh if running
    if st.session_state.enhanced_tavern_state.get('running', False):
        time.sleep(3)
        st.rerun()

if __name__ == "__main__":
    main()
