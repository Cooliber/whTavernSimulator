"""
Responsive Design & UX Enhancement System
Implements responsive design, loading screens, tutorial flow, keyboard shortcuts, and save/load functionality
"""

import streamlit as st
import json
import time
from datetime import datetime
from typing import Dict, Any, Optional

class ResponsiveDesignSystem:
    """Handles responsive design and UX enhancements"""
    
    def __init__(self):
        self.breakpoints = {
            'mobile': 768,
            'tablet': 1024,
            'desktop': 1200,
            'large': 1440
        }
        
        # Initialize tutorial state
        if 'tutorial_state' not in st.session_state:
            st.session_state.tutorial_state = {
                'current_step': 0,
                'completed': False,
                'show_tutorial': False
            }
    
    def render_responsive_css(self):
        """Render responsive CSS for different screen sizes"""
        st.markdown("""
        <style>
        /* Responsive Design System */
        
        /* Mobile First Approach */
        .responsive-container {
            width: 100%;
            max-width: 100%;
            padding: 10px;
            box-sizing: border-box;
        }
        
        .responsive-grid {
            display: grid;
            grid-template-columns: 1fr;
            gap: 15px;
            width: 100%;
        }
        
        .responsive-card {
            background: linear-gradient(135deg, rgba(40,20,10,0.9), rgba(60,30,15,0.9));
            border: 2px solid var(--primary-gold, #ffd700);
            border-radius: 12px;
            padding: 15px;
            margin: 10px 0;
            box-shadow: 0 4px 15px rgba(0,0,0,0.6);
            transition: all 0.3s ease;
        }
        
        .responsive-card:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0,0,0,0.8);
        }
        
        /* Tablet Styles */
        @media (min-width: 768px) {
            .responsive-container {
                padding: 20px;
            }
            
            .responsive-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
            }
            
            .responsive-card {
                padding: 20px;
            }
        }
        
        /* Desktop Styles */
        @media (min-width: 1024px) {
            .responsive-container {
                padding: 30px;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .responsive-grid {
                grid-template-columns: repeat(3, 1fr);
                gap: 25px;
            }
            
            .responsive-card {
                padding: 25px;
            }
        }
        
        /* Large Desktop Styles */
        @media (min-width: 1440px) {
            .responsive-container {
                max-width: 1400px;
                padding: 40px;
            }
            
            .responsive-grid {
                grid-template-columns: repeat(4, 1fr);
                gap: 30px;
            }
        }
        
        /* Loading Screen Styles */
        .loading-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #1a0f0a 0%, #2c1810 50%, #1a0f0a 100%);
            display: flex;
            flex-direction: column;
            justify-content: center;
            align-items: center;
            z-index: 9999;
            opacity: 1;
            transition: opacity 0.5s ease;
        }
        
        .loading-overlay.fade-out {
            opacity: 0;
            pointer-events: none;
        }
        
        .loading-spinner {
            width: 80px;
            height: 80px;
            border: 4px solid rgba(255,215,0,0.3);
            border-top: 4px solid var(--primary-gold, #ffd700);
            border-radius: 50%;
            animation: spin 1s linear infinite;
            margin-bottom: 30px;
        }
        
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        .loading-text {
            color: var(--primary-gold, #ffd700);
            font-family: 'Cinzel', serif;
            font-size: 1.5rem;
            text-align: center;
            margin-bottom: 20px;
        }
        
        .loading-progress {
            width: 300px;
            height: 6px;
            background: rgba(255,215,0,0.2);
            border-radius: 3px;
            overflow: hidden;
        }
        
        .loading-progress-bar {
            height: 100%;
            background: linear-gradient(90deg, var(--primary-gold, #ffd700), #fff);
            border-radius: 3px;
            transition: width 0.3s ease;
        }
        
        /* Tutorial Overlay Styles */
        .tutorial-overlay {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 8888;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .tutorial-card {
            background: linear-gradient(135deg, rgba(40,20,10,0.95), rgba(60,30,15,0.95));
            border: 3px solid var(--primary-gold, #ffd700);
            border-radius: 15px;
            padding: 30px;
            max-width: 500px;
            width: 90%;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
            text-align: center;
        }
        
        .tutorial-title {
            color: var(--primary-gold, #ffd700);
            font-family: 'Cinzel', serif;
            font-size: 1.8rem;
            margin-bottom: 20px;
        }
        
        .tutorial-content {
            color: #ccc;
            font-size: 1.1rem;
            line-height: 1.6;
            margin-bottom: 25px;
        }
        
        .tutorial-buttons {
            display: flex;
            gap: 15px;
            justify-content: center;
        }
        
        .tutorial-btn {
            background: linear-gradient(135deg, var(--primary-gold, #ffd700), #b8860b);
            color: var(--dark-brown, #2c1810);
            border: none;
            border-radius: 8px;
            padding: 12px 24px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Cinzel', serif;
        }
        
        .tutorial-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(255,215,0,0.5);
        }
        
        .tutorial-btn.secondary {
            background: rgba(255,255,255,0.1);
            color: #ccc;
        }
        
        /* Keyboard Shortcuts Overlay */
        .shortcuts-overlay {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(40,20,10,0.95);
            border: 2px solid var(--primary-gold, #ffd700);
            border-radius: 10px;
            padding: 15px;
            max-width: 300px;
            z-index: 7777;
            opacity: 0;
            transform: translateX(100%);
            transition: all 0.3s ease;
        }
        
        .shortcuts-overlay.show {
            opacity: 1;
            transform: translateX(0);
        }
        
        .shortcuts-title {
            color: var(--primary-gold, #ffd700);
            font-weight: bold;
            margin-bottom: 10px;
            text-align: center;
        }
        
        .shortcut-item {
            display: flex;
            justify-content: space-between;
            margin: 5px 0;
            color: #ccc;
            font-size: 0.9rem;
        }
        
        .shortcut-key {
            background: rgba(255,255,255,0.1);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: monospace;
            color: var(--primary-gold, #ffd700);
        }
        
        /* Save/Load Dialog Styles */
        .save-load-dialog {
            background: linear-gradient(135deg, rgba(40,20,10,0.95), rgba(60,30,15,0.95));
            border: 3px solid var(--primary-gold, #ffd700);
            border-radius: 15px;
            padding: 25px;
            max-width: 400px;
            width: 90%;
            box-shadow: 0 10px 40px rgba(0,0,0,0.8);
        }
        
        .save-slot {
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,215,0,0.3);
            border-radius: 8px;
            padding: 15px;
            margin: 10px 0;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .save-slot:hover {
            border-color: var(--primary-gold, #ffd700);
            background: rgba(255,215,0,0.1);
        }
        
        .save-slot.occupied {
            border-color: var(--primary-gold, #ffd700);
        }
        
        .save-slot-name {
            color: var(--primary-gold, #ffd700);
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .save-slot-date {
            color: #aaa;
            font-size: 0.9rem;
        }
        </style>
        """, unsafe_allow_html=True)
    
    def show_loading_screen(self, message: str = "Loading Tavern Systems...", duration: float = 2.0):
        """Display animated loading screen"""
        loading_placeholder = st.empty()
        
        with loading_placeholder.container():
            st.markdown(f"""
            <div class="loading-overlay" id="loading-overlay">
                <div class="loading-spinner"></div>
                <div class="loading-text">{message}</div>
                <div class="loading-progress">
                    <div class="loading-progress-bar" id="loading-progress-bar" style="width: 0%;"></div>
                </div>
            </div>
            
            <script>
            // Animate loading progress
            let progress = 0;
            const progressBar = document.getElementById('loading-progress-bar');
            const overlay = document.getElementById('loading-overlay');
            
            const interval = setInterval(() => {{
                progress += Math.random() * 15 + 5;
                if (progress > 100) progress = 100;
                
                if (progressBar) {{
                    progressBar.style.width = progress + '%';
                }}
                
                if (progress >= 100) {{
                    clearInterval(interval);
                    setTimeout(() => {{
                        if (overlay) {{
                            overlay.classList.add('fade-out');
                            setTimeout(() => overlay.remove(), 500);
                        }}
                    }}, 500);
                }}
            }}, {duration * 1000 / 20});
            </script>
            """, unsafe_allow_html=True)
        
        # Wait for loading to complete
        time.sleep(duration)
        loading_placeholder.empty()
    
    def render_tutorial_system(self):
        """Render interactive tutorial system"""
        if not st.session_state.tutorial_state['completed'] and st.session_state.tutorial_state['show_tutorial']:
            self._render_tutorial_step()
    
    def _render_tutorial_step(self):
        """Render current tutorial step"""
        tutorial_steps = [
            {
                "title": "🏰 Welcome to the Tavern!",
                "content": "Welcome to the most advanced Warhammer Fantasy Tavern Simulator! This tutorial will guide you through the enhanced features and controls.",
                "action": "Let's begin your journey!"
            },
            {
                "title": "🎨 Enhanced Visualization",
                "content": "The Live Visualization tab shows your tavern with advanced GSAP animations, particle effects, and interactive characters. Click on characters to see their details!",
                "action": "Explore the visualization"
            },
            {
                "title": "🎮 Control Panel",
                "content": "Use the Control Panel to manage your tavern's economy, trigger events, and control narrative elements. Each action has visual feedback!",
                "action": "Try the controls"
            },
            {
                "title": "📊 Metrics Dashboard",
                "content": "Monitor your tavern's performance with real-time metrics, economic trends, and agent status. Watch the gauges update in real-time!",
                "action": "Check the metrics"
            },
            {
                "title": "⌨️ Keyboard Shortcuts",
                "content": "Use keyboard shortcuts for quick actions: Ctrl+E (Economic Cycle), Ctrl+G (Generate Event), Ctrl+S (Save), Space (Pause). Press 'H' to toggle help.",
                "action": "Try a shortcut"
            },
            {
                "title": "🎉 You're Ready!",
                "content": "You've completed the tutorial! Your tavern awaits your management. Create epic stories, manage resources, and watch your reputation grow!",
                "action": "Start managing!"
            }
        ]
        
        current_step = st.session_state.tutorial_state['current_step']
        if current_step < len(tutorial_steps):
            step = tutorial_steps[current_step]
            
            st.markdown(f"""
            <div class="tutorial-overlay" id="tutorial-overlay">
                <div class="tutorial-card">
                    <div class="tutorial-title">{step['title']}</div>
                    <div class="tutorial-content">{step['content']}</div>
                    <div style="color: #aaa; margin-bottom: 20px;">Step {current_step + 1} of {len(tutorial_steps)}</div>
                    <div class="tutorial-buttons">
                        <button class="tutorial-btn secondary" onclick="skipTutorial()">Skip Tutorial</button>
                        <button class="tutorial-btn" onclick="nextTutorialStep()">{step['action']}</button>
                    </div>
                </div>
            </div>
            
            <script>
            function nextTutorialStep() {{
                // This would normally communicate with Streamlit
                console.log('Next tutorial step');
                document.getElementById('tutorial-overlay').style.display = 'none';
            }}
            
            function skipTutorial() {{
                console.log('Skip tutorial');
                document.getElementById('tutorial-overlay').style.display = 'none';
            }}
            </script>
            """, unsafe_allow_html=True)
    
    def start_tutorial(self):
        """Start the tutorial flow"""
        st.session_state.tutorial_state['show_tutorial'] = True
        st.session_state.tutorial_state['current_step'] = 0
        st.rerun()
    
    def next_tutorial_step(self):
        """Advance to next tutorial step"""
        st.session_state.tutorial_state['current_step'] += 1
        tutorial_steps_count = 6  # Total number of steps
        
        if st.session_state.tutorial_state['current_step'] >= tutorial_steps_count:
            st.session_state.tutorial_state['completed'] = True
            st.session_state.tutorial_state['show_tutorial'] = False
        
        st.rerun()
    
    def skip_tutorial(self):
        """Skip the tutorial"""
        st.session_state.tutorial_state['completed'] = True
        st.session_state.tutorial_state['show_tutorial'] = False
        st.rerun()

    def render_keyboard_shortcuts(self):
        """Render keyboard shortcuts overlay"""
        st.markdown("""
        <div class="shortcuts-overlay" id="shortcuts-overlay">
            <div class="shortcuts-title">⌨️ Keyboard Shortcuts</div>
            <div class="shortcut-item">
                <span>Economic Cycle</span>
                <span class="shortcut-key">Ctrl+E</span>
            </div>
            <div class="shortcut-item">
                <span>Generate Event</span>
                <span class="shortcut-key">Ctrl+G</span>
            </div>
            <div class="shortcut-item">
                <span>Save State</span>
                <span class="shortcut-key">Ctrl+S</span>
            </div>
            <div class="shortcut-item">
                <span>Load State</span>
                <span class="shortcut-key">Ctrl+L</span>
            </div>
            <div class="shortcut-item">
                <span>Pause/Resume</span>
                <span class="shortcut-key">Space</span>
            </div>
            <div class="shortcut-item">
                <span>Toggle Help</span>
                <span class="shortcut-key">H</span>
            </div>
            <div class="shortcut-item">
                <span>Reset View</span>
                <span class="shortcut-key">R</span>
            </div>
            <div class="shortcut-item">
                <span>Fullscreen</span>
                <span class="shortcut-key">F11</span>
            </div>
        </div>

        <script>
        // Keyboard shortcuts handler
        document.addEventListener('keydown', function(e) {
            // Toggle shortcuts overlay with 'H'
            if (e.key === 'h' || e.key === 'H') {
                const overlay = document.getElementById('shortcuts-overlay');
                if (overlay) {
                    overlay.classList.toggle('show');
                }
                e.preventDefault();
            }

            // Handle Ctrl combinations
            if (e.ctrlKey) {
                switch(e.key.toLowerCase()) {
                    case 'e':
                        console.log('Economic cycle shortcut triggered');
                        // Trigger economic cycle
                        e.preventDefault();
                        break;
                    case 'g':
                        console.log('Generate event shortcut triggered');
                        // Trigger event generation
                        e.preventDefault();
                        break;
                    case 's':
                        console.log('Save state shortcut triggered');
                        // Trigger save
                        e.preventDefault();
                        break;
                    case 'l':
                        console.log('Load state shortcut triggered');
                        // Trigger load
                        e.preventDefault();
                        break;
                }
            }

            // Handle other shortcuts
            switch(e.key) {
                case ' ':
                    console.log('Pause/Resume shortcut triggered');
                    e.preventDefault();
                    break;
                case 'r':
                case 'R':
                    if (!e.ctrlKey) {
                        console.log('Reset view shortcut triggered');
                        e.preventDefault();
                    }
                    break;
            }
        });

        // Hide shortcuts overlay when clicking outside
        document.addEventListener('click', function(e) {
            const overlay = document.getElementById('shortcuts-overlay');
            if (overlay && !overlay.contains(e.target)) {
                overlay.classList.remove('show');
            }
        });
        </script>
        """, unsafe_allow_html=True)

    def render_save_load_system(self):
        """Render save/load system interface"""
        if 'save_slots' not in st.session_state:
            st.session_state.save_slots = {}

        # Save/Load buttons in sidebar or main area
        col1, col2 = st.columns(2)

        with col1:
            if st.button("💾 Save Game", key="save_game_btn"):
                self.show_save_dialog()

        with col2:
            if st.button("📂 Load Game", key="load_game_btn"):
                self.show_load_dialog()

    def show_save_dialog(self):
        """Show save game dialog"""
        st.markdown("""
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0,0,0,0.8); z-index: 8888;
                    display: flex; justify-content: center; align-items: center;">
            <div class="save-load-dialog">
                <h3 style="color: var(--primary-gold, #ffd700); text-align: center; margin-bottom: 20px;">
                    💾 Save Game
                </h3>
                <div id="save-slots">
                    <!-- Save slots will be populated here -->
                </div>
                <div style="text-align: center; margin-top: 20px;">
                    <button class="tutorial-btn secondary" onclick="closeSaveDialog()">Cancel</button>
                    <button class="tutorial-btn" onclick="saveToSlot()">Save</button>
                </div>
            </div>
        </div>

        <script>
        function closeSaveDialog() {
            // Close dialog logic
            console.log('Close save dialog');
        }

        function saveToSlot() {
            // Save to selected slot logic
            console.log('Save to slot');
        }
        </script>
        """, unsafe_allow_html=True)

    def show_load_dialog(self):
        """Show load game dialog"""
        st.markdown("""
        <div style="position: fixed; top: 0; left: 0; width: 100%; height: 100%;
                    background: rgba(0,0,0,0.8); z-index: 8888;
                    display: flex; justify-content: center; align-items: center;">
            <div class="save-load-dialog">
                <h3 style="color: var(--primary-gold, #ffd700); text-align: center; margin-bottom: 20px;">
                    📂 Load Game
                </h3>
                <div id="load-slots">
                    <!-- Load slots will be populated here -->
                </div>
                <div style="text-align: center; margin-top: 20px;">
                    <button class="tutorial-btn secondary" onclick="closeLoadDialog()">Cancel</button>
                    <button class="tutorial-btn" onclick="loadFromSlot()">Load</button>
                </div>
            </div>
        </div>

        <script>
        function closeLoadDialog() {
            // Close dialog logic
            console.log('Close load dialog');
        }

        function loadFromSlot() {
            // Load from selected slot logic
            console.log('Load from slot');
        }
        </script>
        """, unsafe_allow_html=True)

    def save_tavern_state(self, slot_name: str = None) -> bool:
        """Save current tavern state to specified slot"""
        try:
            if slot_name is None:
                slot_name = f"autosave_{datetime.now().strftime('%Y%m%d_%H%M%S')}"

            # Gather current state
            tavern_state = {
                'timestamp': datetime.now().isoformat(),
                'ui_state': st.session_state.ui_state,
                'tutorial_state': st.session_state.tutorial_state,
                'interaction_log': getattr(st.session_state, 'interaction_log', []),
                'version': '1.0.0'
            }

            # Save to session state (in production, this would be saved to file/database)
            st.session_state.save_slots[slot_name] = tavern_state

            st.success(f"✅ Game saved to slot: {slot_name}")
            return True

        except Exception as e:
            st.error(f"❌ Save failed: {e}")
            return False

    def load_tavern_state(self, slot_name: str) -> bool:
        """Load tavern state from specified slot"""
        try:
            if slot_name not in st.session_state.save_slots:
                st.error(f"❌ Save slot '{slot_name}' not found")
                return False

            # Load state
            tavern_state = st.session_state.save_slots[slot_name]

            # Restore state
            st.session_state.ui_state = tavern_state.get('ui_state', {})
            st.session_state.tutorial_state = tavern_state.get('tutorial_state', {})
            st.session_state.interaction_log = tavern_state.get('interaction_log', [])

            st.success(f"✅ Game loaded from slot: {slot_name}")
            st.rerun()
            return True

        except Exception as e:
            st.error(f"❌ Load failed: {e}")
            return False

    def auto_save(self):
        """Perform automatic save"""
        if st.session_state.ui_state.get('auto_save', True):
            self.save_tavern_state("autosave")

    def get_responsive_layout(self, content_type: str = "default") -> Dict[str, Any]:
        """Get responsive layout configuration based on content type"""
        layouts = {
            "default": {
                "mobile": {"columns": 1, "spacing": "compact"},
                "tablet": {"columns": 2, "spacing": "normal"},
                "desktop": {"columns": 3, "spacing": "comfortable"},
                "large": {"columns": 4, "spacing": "spacious"}
            },
            "dashboard": {
                "mobile": {"columns": 1, "spacing": "compact"},
                "tablet": {"columns": 1, "spacing": "normal"},
                "desktop": {"columns": 2, "spacing": "comfortable"},
                "large": {"columns": 3, "spacing": "spacious"}
            },
            "visualization": {
                "mobile": {"columns": 1, "spacing": "minimal"},
                "tablet": {"columns": 1, "spacing": "minimal"},
                "desktop": {"columns": 1, "spacing": "minimal"},
                "large": {"columns": 1, "spacing": "minimal"}
            }
        }

        return layouts.get(content_type, layouts["default"])

    def render_responsive_grid(self, items: list, content_type: str = "default"):
        """Render items in a responsive grid layout"""
        layout = self.get_responsive_layout(content_type)

        # For Streamlit, we'll use columns based on desktop layout
        desktop_cols = layout["desktop"]["columns"]

        # Create columns
        cols = st.columns(desktop_cols)

        # Distribute items across columns
        for i, item in enumerate(items):
            col_index = i % desktop_cols
            with cols[col_index]:
                item()  # Render the item (should be a callable)
