#!/usr/bin/env python3
"""
Matrix Chat Interface Demo for Warhammer Tavern Simulator
Demonstrates advanced conversation visualization with Matrix effects
"""

import streamlit as st
import time
import random
from datetime import datetime, timedelta
from components.matrix_chat_interface import MatrixChatInterface, ChatMessage
from components.matrix_chat_integration import MatrixChatIntegration

# Page configuration
st.set_page_config(
    page_title="🔋 Matrix Chat Interface Demo",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_demo():
    """Initialize demo session state"""
    if 'matrix_chat_demo' not in st.session_state:
        chat_interface = MatrixChatInterface()
        chat_integration = MatrixChatIntegration(chat_interface)

        st.session_state.matrix_chat_demo = {
            'chat_interface': chat_interface,
            'chat_integration': chat_integration,
            'demo_agents': [
                {"name": "Karczmarz", "id": "karczmarz", "active": True},
                {"name": "Skrytobójca", "id": "skrytobojca", "active": True},
                {"name": "Wiedźma", "id": "wiedzma", "active": True},
                {"name": "Czempion", "id": "czempion", "active": True},
                {"name": "Zwiadowca", "id": "zwiadowca", "active": True}
            ],
            'message_counter': 0,
            'auto_demo_running': False
        }

def generate_sample_message() -> ChatMessage:
    """Generate a sample chat message for demo"""
    agents = st.session_state.matrix_chat_demo['demo_agents']
    sender = random.choice(agents)
    receiver = random.choice([a for a in agents if a['id'] != sender['id']])
    
    # Sample message content based on agent types
    message_templates = {
        'karczmarz': [
            "Witajcie w mojej karczmie, szanowni goście!",
            "Czy ktoś widział podejrzane postacie w okolicy?",
            "Mam świeże piwo i gorący posiłek dla wszystkich!",
            "Słyszałem dziwne plotki z miasta..."
        ],
        'skrytobojca': [
            "Obserwuję cię z cienia...",
            "Informacje mają swoją cenę.",
            "Coś się dzieje w ciemnych zaułkach.",
            "Nie wszyscy są tym, za kogo się podają."
        ],
        'wiedzma': [
            "Czuję magię w powietrzu...",
            "Gwiazdy przepowiadają nadchodzące zmiany.",
            "Moje mikstury mogą pomóc w trudnych czasach.",
            "Chaos szepcze o starożytnych sekretach."
        ],
        'czempion': [
            "Honor i chwała dla Imperium!",
            "Jestem gotów stawić czoła każdemu wyzwaniu!",
            "Mój miecz służy sprawiedliwości!",
            "Razem pokonamy siły ciemności!"
        ],
        'zwiadowca': [
            "Widziałem dziwne ślady w lesie.",
            "Drogi są niebezpieczne ostatnio.",
            "Mam wiadomości z dalekich krain.",
            "Coś podąża naszym tropem..."
        ]
    }
    
    # Message types and their properties
    message_types = [
        {"type": "whisper", "effects": ["matrix", "fade"], "emotion": "mysterious"},
        {"type": "shout", "effects": ["glow", "shake"], "emotion": "urgent"},
        {"type": "thought", "effects": ["typewriter"], "emotion": "calm"},
        {"type": "action", "effects": ["glow"], "emotion": "happy"},
        {"type": "magic", "effects": ["matrix", "glow"], "emotion": "mysterious"}
    ]
    
    msg_type = random.choice(message_types)
    content = random.choice(message_templates.get(sender['id'], ["Mówię coś ważnego..."]))
    
    # Generate unique message ID
    st.session_state.matrix_chat_demo['message_counter'] += 1
    message_id = f"msg_{st.session_state.matrix_chat_demo['message_counter']}"
    
    return ChatMessage(
        id=message_id,
        sender=sender['name'],
        receiver=receiver['name'],
        content=content,
        message_type=msg_type['type'],
        emotion=msg_type['emotion'],
        priority=random.randint(1, 10),
        timestamp=datetime.now(),
        effects=msg_type['effects'],
        color_theme=random.choice(['gold', 'green', 'red', 'blue', 'purple']),
        duration=random.uniform(3.0, 8.0)
    )

def render_sidebar():
    """Render sidebar controls"""
    st.sidebar.title("🔋 Matrix Chat Controls")
    
    # Chat settings
    st.sidebar.subheader("⚙️ Settings")
    
    matrix_mode = st.sidebar.checkbox("Matrix Rain Effect", value=True)
    auto_scroll = st.sidebar.checkbox("Auto Scroll", value=True)
    sound_enabled = st.sidebar.checkbox("Sound Effects", value=True)
    effect_intensity = st.sidebar.slider("Effect Intensity", 0.1, 1.0, 0.8, 0.1)
    
    # Update chat settings
    chat_interface = st.session_state.matrix_chat_demo['chat_interface']
    chat_interface.set_chat_settings(
        matrix_mode=matrix_mode,
        auto_scroll=auto_scroll,
        sound_enabled=sound_enabled,
        effect_intensity=effect_intensity
    )
    
    st.sidebar.markdown("---")
    
    # Demo controls
    st.sidebar.subheader("🎮 Demo Controls")
    
    if st.sidebar.button("📨 Add Random Message"):
        message = generate_sample_message()
        chat_interface.add_message(message)
        st.success(f"Added message from {message.sender}")
    
    if st.sidebar.button("💥 Add Urgent Alert"):
        agents = st.session_state.matrix_chat_demo['demo_agents']
        sender = random.choice(agents)
        
        alert_message = ChatMessage(
            id=f"alert_{int(time.time())}",
            sender=sender['name'],
            receiver="WSZYSCY",
            content="🚨 ALARM! Wykryto zagrożenie w karczmie!",
            message_type="shout",
            emotion="urgent",
            priority=10,
            timestamp=datetime.now(),
            effects=["shake", "glow"],
            color_theme="red",
            duration=5.0
        )
        chat_interface.add_message(alert_message)
        st.error("🚨 Urgent alert added!")
    
    if st.sidebar.button("🔮 Add Magic Message"):
        magic_message = ChatMessage(
            id=f"magic_{int(time.time())}",
            sender="Wiedźma",
            receiver="Wszyscy",
            content="✨ Zaklęcie zostało rzucone... Magia przepływa przez karczmę...",
            message_type="magic",
            emotion="mysterious",
            priority=8,
            timestamp=datetime.now(),
            effects=["matrix", "glow", "typewriter"],
            color_theme="purple",
            duration=7.0
        )
        chat_interface.add_message(magic_message)
        st.success("🔮 Magic message added!")

    if st.sidebar.button("🎭 Simulate Agent Conversation"):
        chat_integration = st.session_state.matrix_chat_demo['chat_integration']
        chat_integration.simulate_agent_conversation(5)
        st.success("🎭 Agent conversation simulated!")

    if st.sidebar.button("📢 Add System Message"):
        chat_integration = st.session_state.matrix_chat_demo['chat_integration']
        chat_integration.add_system_message(
            "🏰 Karczma jest teraz pod ochroną zaawansowanego systemu Matrix Chat!",
            message_type="action",
            priority=7
        )
        st.success("📢 System message added!")
    
    st.sidebar.markdown("---")
    
    # Auto demo
    st.sidebar.subheader("🤖 Auto Demo")
    
    auto_demo = st.sidebar.checkbox("Auto Generate Messages", value=False)
    if auto_demo != st.session_state.matrix_chat_demo['auto_demo_running']:
        st.session_state.matrix_chat_demo['auto_demo_running'] = auto_demo
        if auto_demo:
            st.sidebar.success("Auto demo started!")
        else:
            st.sidebar.info("Auto demo stopped.")
    
    if auto_demo:
        demo_speed = st.sidebar.slider("Demo Speed (seconds)", 1, 10, 3)
        
        # Auto-generate messages
        if 'last_auto_message' not in st.session_state:
            st.session_state.last_auto_message = time.time()
        
        if time.time() - st.session_state.last_auto_message > demo_speed:
            message = generate_sample_message()
            chat_interface.add_message(message)
            st.session_state.last_auto_message = time.time()
            st.rerun()
    
    st.sidebar.markdown("---")
    
    # Clear chat
    if st.sidebar.button("🗑️ Clear All Messages"):
        chat_interface.clear_chat()
        st.sidebar.success("Chat cleared!")
    
    # Performance info
    st.sidebar.subheader("📊 Performance")
    active_conversations = chat_interface.get_active_conversations()
    st.sidebar.metric("Active Conversations", len(active_conversations))
    
    message_count = len(st.session_state.matrix_chat_state.get('messages', []))
    st.sidebar.metric("Total Messages", message_count)

def render_main_content():
    """Render main chat interface"""
    st.title("🔋 Matrix Chat Interface Demo")
    st.markdown("**Zaawansowany interfejs czatu z efektami Matrix dla Warhammer Tavern Simulator**")
    
    # Chat interface
    chat_interface = st.session_state.matrix_chat_demo['chat_interface']
    
    # Render Matrix chat
    chat_result = chat_interface.render_matrix_chat(height=600)
    
    # Display active conversations
    st.subheader("💬 Active Conversations")
    active_convs = chat_interface.get_active_conversations()
    
    if active_convs:
        cols = st.columns(min(len(active_convs), 3))
        for i, conv in enumerate(active_convs[:3]):
            with cols[i]:
                st.metric(
                    f"🗣️ {' ↔ '.join(conv['participants'])}",
                    f"{conv['message_count']} messages",
                    f"Intensity: {conv['intensity']:.1f}"
                )
    else:
        st.info("No active conversations. Add some messages to see them here!")

def main():
    """Main application function"""
    initialize_demo()
    
    # Render components
    render_sidebar()
    render_main_content()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 20px;">
        <h4>🔋 Matrix Chat Interface</h4>
        <p>Advanced conversation visualization with Matrix-style effects</p>
        <p><strong>Features:</strong> Matrix rain, typewriter effects, floating bubbles, multi-dimensional conversations</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
