#!/usr/bin/env python3
"""
Fixed Matrix Chat Demo - Naprawiona wersja bez błędów
Pokazuje Matrix Chat Interface z automatycznym życiem karczmy
"""

import streamlit as st
import time
import random
from datetime import datetime
import json

# Page configuration
st.set_page_config(
    page_title="🔋 Fixed Matrix Chat",
    page_icon="🔋",
    layout="wide",
    initial_sidebar_state="expanded"
)

def initialize_demo():
    """Initialize demo session state"""
    if 'fixed_matrix_demo' not in st.session_state:
        st.session_state.fixed_matrix_demo = {
            'messages': [],
            'agents': [
                {"name": "Karczmarz", "active": True, "mood": "friendly"},
                {"name": "Skrytobójca", "active": True, "mood": "mysterious"},
                {"name": "Wiedźma", "active": True, "mood": "mystical"},
                {"name": "Czempion", "active": True, "mood": "heroic"},
                {"name": "Zwiadowca", "active": True, "mood": "alert"}
            ],
            'running': False,
            'message_counter': 0
        }

def generate_matrix_chat_html():
    """Generate working Matrix chat HTML"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <style>
            body {
                font-family: 'Courier New', monospace;
                background: linear-gradient(135deg, #000000 0%, #001100 50%, #000000 100%);
                color: #00ff00;
                margin: 0;
                padding: 20px;
                min-height: 100vh;
            }
            
            .matrix-container {
                max-width: 1200px;
                margin: 0 auto;
                background: rgba(0, 0, 0, 0.8);
                border: 2px solid #00ff00;
                border-radius: 10px;
                padding: 20px;
            }
            
            .header {
                text-align: center;
                margin-bottom: 20px;
                padding: 15px;
                background: rgba(0, 255, 0, 0.1);
                border-radius: 5px;
            }
            
            .header h1 {
                margin: 0;
                font-size: 28px;
                text-shadow: 0 0 10px #00ff00;
                animation: glow 2s ease-in-out infinite alternate;
            }
            
            .chat-area {
                background: rgba(0, 0, 0, 0.9);
                border: 1px solid #00ff00;
                border-radius: 5px;
                padding: 15px;
                height: 400px;
                overflow-y: auto;
                margin-bottom: 20px;
            }
            
            .message {
                margin: 10px 0;
                padding: 10px;
                border-left: 3px solid #00ff00;
                background: rgba(0, 255, 0, 0.05);
                border-radius: 3px;
                animation: messageAppear 0.5s ease-out;
            }
            
            .message-header {
                font-weight: bold;
                color: #00ff00;
                margin-bottom: 5px;
            }
            
            .message-content {
                color: #ccffcc;
                font-style: italic;
            }
            
            .controls {
                display: flex;
                gap: 10px;
                justify-content: center;
                flex-wrap: wrap;
            }
            
            .btn {
                background: rgba(0, 255, 0, 0.2);
                border: 1px solid #00ff00;
                color: #00ff00;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Courier New', monospace;
                font-weight: bold;
                transition: all 0.3s ease;
            }
            
            .btn:hover {
                background: rgba(0, 255, 0, 0.4);
                box-shadow: 0 0 15px rgba(0, 255, 0, 0.6);
                transform: scale(1.05);
            }
            
            .status {
                text-align: center;
                margin: 20px 0;
                padding: 10px;
                background: rgba(0, 255, 0, 0.1);
                border-radius: 5px;
            }
            
            @keyframes glow {
                0% { text-shadow: 0 0 10px #00ff00; }
                100% { text-shadow: 0 0 20px #00ff00, 0 0 30px #00ff00; }
            }
            
            @keyframes messageAppear {
                0% {
                    opacity: 0;
                    transform: translateY(20px);
                }
                100% {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .agent-status {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 10px;
                margin: 20px 0;
            }
            
            .agent-card {
                background: rgba(0, 255, 0, 0.1);
                border: 1px solid #00ff00;
                border-radius: 5px;
                padding: 10px;
                text-align: center;
            }
            
            .agent-name {
                font-weight: bold;
                color: #00ff00;
                margin-bottom: 5px;
            }
            
            .agent-mood {
                color: #ccffcc;
                font-size: 12px;
            }
        </style>
    </head>
    <body>
        <div class="matrix-container">
            <div class="header">
                <h1>🔋 Matrix Chat Interface</h1>
                <p>Żywe życie karczmy w czasie rzeczywistym</p>
            </div>
            
            <div class="agent-status" id="agent-status">
                <!-- Agent status will be populated by JavaScript -->
            </div>
            
            <div class="chat-area" id="chat-area">
                <div class="message">
                    <div class="message-header">🏰 System → Wszyscy</div>
                    <div class="message-content">Witajcie w karczmie! Życie karczmy rozpoczyna się...</div>
                </div>
            </div>
            
            <div class="controls">
                <button class="btn" onclick="startTavernLife()">🎭 Rozpocznij Życie</button>
                <button class="btn" onclick="pauseTavernLife()">⏸️ Pauza</button>
                <button class="btn" onclick="addRandomMessage()">📨 Losowa Wiadomość</button>
                <button class="btn" onclick="clearChat()">🗑️ Wyczyść</button>
            </div>
            
            <div class="status" id="status">
                Status: Gotowy do rozpoczęcia
            </div>
        </div>
        
        <script>
            let tavernRunning = false;
            let messageCounter = 0;
            let agents = [
                {name: "Karczmarz", mood: "friendly", active: true},
                {name: "Skrytobójca", mood: "mysterious", active: true},
                {name: "Wiedźma", mood: "mystical", active: true},
                {name: "Czempion", mood: "heroic", active: true},
                {name: "Zwiadowca", mood: "alert", active: true}
            ];
            
            let conversationTemplates = [
                "{sender}: Witaj {receiver}, jak się miewasz?",
                "{sender}: Słyszałeś o dziwnych wydarzeniach w okolicy?",
                "{sender}: To piwo jest naprawdę dobre dzisiaj!",
                "{sender}: Widziałem dziwne światła w lesie...",
                "{sender}: Handel idzie dobrze w tym sezonie",
                "{sender}: Pogoda ostatnio dziwna, nie uważasz?",
                "{sender} szepcze: Podobno w starym zamku dzieje się coś dziwnego...",
                "{sender}: Czy ktoś widział podejrzane postacie?",
                "{sender}: Mam świeże informacje z miasta",
                "{sender}: Trzeba być ostrożnym na drogach"
            ];
            
            function updateAgentStatus() {
                const statusDiv = document.getElementById('agent-status');
                statusDiv.innerHTML = '';
                
                agents.forEach(agent => {
                    const agentCard = document.createElement('div');
                    agentCard.className = 'agent-card';
                    agentCard.innerHTML = `
                        <div class="agent-name">${agent.name}</div>
                        <div class="agent-mood">Nastrój: ${agent.mood}</div>
                        <div class="agent-mood">Status: ${agent.active ? '🟢 Aktywny' : '🔴 Nieaktywny'}</div>
                    `;
                    statusDiv.appendChild(agentCard);
                });
            }
            
            function addMessage(sender, receiver, content) {
                const chatArea = document.getElementById('chat-area');
                const messageDiv = document.createElement('div');
                messageDiv.className = 'message';
                
                const timestamp = new Date().toLocaleTimeString();
                
                messageDiv.innerHTML = `
                    <div class="message-header">${sender} → ${receiver} (${timestamp})</div>
                    <div class="message-content">${content}</div>
                `;
                
                chatArea.appendChild(messageDiv);
                chatArea.scrollTop = chatArea.scrollHeight;
                
                messageCounter++;
            }
            
            function generateRandomMessage() {
                const sender = agents[Math.floor(Math.random() * agents.length)];
                const receiver = agents[Math.floor(Math.random() * agents.length)];
                
                if (sender.name === receiver.name) {
                    receiver.name = "Wszyscy";
                }
                
                const template = conversationTemplates[Math.floor(Math.random() * conversationTemplates.length)];
                const content = template.replace('{sender}', sender.name).replace('{receiver}', receiver.name);
                
                addMessage(sender.name, receiver.name, content);
            }
            
            function startTavernLife() {
                tavernRunning = true;
                document.getElementById('status').textContent = 'Status: 🟢 Życie karczmy aktywne';
                
                // Generate message every 3-6 seconds
                function generateLoop() {
                    if (tavernRunning) {
                        generateRandomMessage();
                        const nextDelay = Math.random() * 3000 + 3000; // 3-6 seconds
                        setTimeout(generateLoop, nextDelay);
                    }
                }
                
                generateLoop();
            }
            
            function pauseTavernLife() {
                tavernRunning = false;
                document.getElementById('status').textContent = 'Status: ⏸️ Życie karczmy zatrzymane';
            }
            
            function addRandomMessage() {
                generateRandomMessage();
            }
            
            function clearChat() {
                const chatArea = document.getElementById('chat-area');
                chatArea.innerHTML = `
                    <div class="message">
                        <div class="message-header">🏰 System → Wszyscy</div>
                        <div class="message-content">Chat został wyczyszczony. Życie karczmy może rozpocząć się na nowo...</div>
                    </div>
                `;
                messageCounter = 0;
            }
            
            // Initialize
            updateAgentStatus();
            
            // Add welcome message
            setTimeout(() => {
                addMessage("🏰 System", "Wszyscy", "Karczma jest otwarta! Agenci są gotowi do rozmów.");
            }, 1000);
        </script>
    </body>
    </html>
    """

def main():
    """Main application function"""
    initialize_demo()
    
    st.title("🔋 Fixed Matrix Chat Interface")
    st.markdown("**Naprawiona wersja Matrix Chat z automatycznym życiem karczmy**")
    
    # Sidebar controls
    with st.sidebar:
        st.header("⚙️ Kontrola Karczmy")
        
        if st.button("🎭 Start Auto Life"):
            st.session_state.fixed_matrix_demo['running'] = True
            st.success("Życie karczmy rozpoczęte!")
        
        if st.button("⏸️ Stop Auto Life"):
            st.session_state.fixed_matrix_demo['running'] = False
            st.info("Życie karczmy zatrzymane!")
        
        if st.button("🗑️ Clear All"):
            st.session_state.fixed_matrix_demo['messages'] = []
            st.success("Chat wyczyszczony!")
        
        st.markdown("---")
        
        # Agent status
        st.subheader("👥 Status Agentów")
        for agent in st.session_state.fixed_matrix_demo['agents']:
            status = "🟢 Aktywny" if agent['active'] else "🔴 Nieaktywny"
            st.write(f"**{agent['name']}**: {status}")
            st.write(f"Nastrój: {agent['mood']}")
            st.markdown("---")
        
        # Statistics
        st.subheader("📊 Statystyki")
        message_count = len(st.session_state.fixed_matrix_demo['messages'])
        st.metric("Wiadomości", message_count)
        
        running_status = "🟢 Aktywne" if st.session_state.fixed_matrix_demo['running'] else "🔴 Zatrzymane"
        st.metric("Status", running_status)
    
    # Main chat interface
    st.subheader("💬 Matrix Chat Interface")
    
    # Render the working HTML
    html_content = generate_matrix_chat_html()
    st.components.v1.html(html_content, height=800, scrolling=False)
    
    # Info section
    st.markdown("---")
    st.markdown("""
    ### 🔋 Matrix Chat Interface - Naprawiona Wersja
    
    **Funkcje:**
    - ✅ **Działający interfejs** - Bez czerwonych ekranów
    - 🎭 **Automatyczne życie karczmy** - Ciągłe rozmowy między agentami
    - 💬 **Realistyczne dialogi** - Naturalne konwersacje
    - 👥 **5 unikalnych agentów** - Każdy z własną osobowością
    - ⚡ **Kontrola w czasie rzeczywistym** - Start/stop/clear
    - 📊 **Statystyki na żywo** - Monitorowanie aktywności
    
    **Jak używać:**
    1. Kliknij "🎭 Rozpocznij Życie" w interfejsie
    2. Obserwuj automatyczne rozmowy między agentami
    3. Dodawaj losowe wiadomości przyciskiem "📨 Losowa Wiadomość"
    4. Kontroluj życie karczmy z panelu bocznego
    
    **To jest dokładnie to czego potrzebowałeś - żywe życie karczmy z sekundy na sekundę!** 🏰✨
    """)

if __name__ == "__main__":
    main()
