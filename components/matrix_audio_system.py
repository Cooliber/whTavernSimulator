#!/usr/bin/env python3
"""
Matrix Audio System for Enhanced Chat Experience
Provides immersive audio effects for Matrix Chat Interface
"""

import streamlit as st
from typing import Dict, List, Optional
from dataclasses import dataclass
import json

@dataclass
class AudioEffect:
    """Audio effect configuration"""
    name: str
    url: str
    volume: float = 0.5
    loop: bool = False
    fade_in: float = 0.0
    fade_out: float = 0.0
    delay: float = 0.0

class MatrixAudioSystem:
    """
    Advanced audio system for Matrix Chat Interface
    Provides immersive sound effects and ambient audio
    """
    
    def __init__(self):
        self.component_id = "matrix_audio_system"
        self.initialize_audio_library()
    
    def initialize_audio_library(self):
        """Initialize audio effects library"""
        self.audio_effects = {
            # Matrix effects
            'matrix_rain': AudioEffect(
                name="Matrix Rain",
                url="https://www.soundjay.com/misc/sounds/digital-rain.wav",
                volume=0.3,
                loop=True,
                fade_in=2.0
            ),
            'matrix_glitch': AudioEffect(
                name="Matrix Glitch",
                url="https://www.soundjay.com/misc/sounds/glitch-1.wav",
                volume=0.6,
                fade_in=0.1,
                fade_out=0.5
            ),
            
            # Message type sounds
            'whisper': AudioEffect(
                name="Whisper",
                url="https://www.soundjay.com/misc/sounds/whisper.wav",
                volume=0.4,
                fade_in=0.2
            ),
            'shout': AudioEffect(
                name="Shout Alert",
                url="https://www.soundjay.com/misc/sounds/alert-1.wav",
                volume=0.8,
                fade_in=0.1
            ),
            'thought': AudioEffect(
                name="Thought Bubble",
                url="https://www.soundjay.com/misc/sounds/bubble-1.wav",
                volume=0.3,
                fade_in=0.3
            ),
            'action': AudioEffect(
                name="Action Sound",
                url="https://www.soundjay.com/misc/sounds/swoosh-1.wav",
                volume=0.6,
                fade_in=0.1
            ),
            'magic': AudioEffect(
                name="Magic Spell",
                url="https://www.soundjay.com/misc/sounds/magic-1.wav",
                volume=0.7,
                fade_in=0.2,
                fade_out=1.0
            ),
            
            # Emotion sounds
            'angry': AudioEffect(
                name="Angry Growl",
                url="https://www.soundjay.com/misc/sounds/growl.wav",
                volume=0.5
            ),
            'happy': AudioEffect(
                name="Happy Chime",
                url="https://www.soundjay.com/misc/sounds/chime-1.wav",
                volume=0.4
            ),
            'mysterious': AudioEffect(
                name="Mysterious Tone",
                url="https://www.soundjay.com/misc/sounds/mystery.wav",
                volume=0.5
            ),
            'urgent': AudioEffect(
                name="Urgent Beep",
                url="https://www.soundjay.com/misc/sounds/beep-1.wav",
                volume=0.7
            ),
            'calm': AudioEffect(
                name="Calm Ambient",
                url="https://www.soundjay.com/misc/sounds/ambient-1.wav",
                volume=0.3,
                loop=True
            ),
            
            # Special effects
            'typewriter': AudioEffect(
                name="Typewriter",
                url="https://www.soundjay.com/misc/sounds/typewriter.wav",
                volume=0.4
            ),
            'notification': AudioEffect(
                name="Notification",
                url="https://www.soundjay.com/misc/sounds/notification.wav",
                volume=0.6
            ),
            'error': AudioEffect(
                name="Error Sound",
                url="https://www.soundjay.com/misc/sounds/error.wav",
                volume=0.5
            ),
            'success': AudioEffect(
                name="Success Sound",
                url="https://www.soundjay.com/misc/sounds/success.wav",
                volume=0.5
            )
        }
    
    def get_audio_javascript(self) -> str:
        """Generate JavaScript for audio system"""
        audio_config = {
            name: {
                'url': effect.url,
                'volume': effect.volume,
                'loop': effect.loop,
                'fadeIn': effect.fade_in,
                'fadeOut': effect.fade_out,
                'delay': effect.delay
            }
            for name, effect in self.audio_effects.items()
        }
        
        return f"""
        // Matrix Audio System
        let matrixAudioSystem = {{
            sounds: new Map(),
            isInitialized: false,
            masterVolume: 0.7,
            enabled: true,
            config: {json.dumps(audio_config)}
        }};

        // Initialize Howler.js audio system
        function initializeMatrixAudio() {{
            console.log('🔊 Initializing Matrix Audio System...');
            
            // Check if Howler is available
            if (typeof Howl === 'undefined') {{
                console.warn('Howler.js not loaded, audio disabled');
                matrixAudioSystem.enabled = false;
                return;
            }}

            // Initialize all sounds
            Object.entries(matrixAudioSystem.config).forEach(([name, config]) => {{
                try {{
                    const sound = new Howl({{
                        src: [config.url],
                        volume: config.volume * matrixAudioSystem.masterVolume,
                        loop: config.loop,
                        preload: true,
                        onload: () => console.log(`✅ Loaded audio: ${{name}}`),
                        onloaderror: (id, error) => console.warn(`❌ Failed to load audio: ${{name}}`, error)
                    }});
                    
                    matrixAudioSystem.sounds.set(name, sound);
                }} catch (error) {{
                    console.warn(`Error creating sound ${{name}}:`, error);
                }}
            }});

            matrixAudioSystem.isInitialized = true;
            console.log('✅ Matrix Audio System initialized');
        }}

        // Play audio effect
        function playMatrixAudio(effectName, options = {{}}) {{
            if (!matrixAudioSystem.enabled || !matrixAudioSystem.isInitialized) {{
                return;
            }}

            const sound = matrixAudioSystem.sounds.get(effectName);
            if (!sound) {{
                console.warn(`Audio effect not found: ${{effectName}}`);
                return;
            }}

            try {{
                // Apply options
                if (options.volume !== undefined) {{
                    sound.volume(options.volume * matrixAudioSystem.masterVolume);
                }}
                
                if (options.delay) {{
                    setTimeout(() => {{
                        sound.play();
                    }}, options.delay * 1000);
                }} else {{
                    sound.play();
                }}

                // Fade effects
                if (options.fadeIn) {{
                    sound.fade(0, sound.volume(), options.fadeIn * 1000);
                }}
                
                if (options.fadeOut) {{
                    setTimeout(() => {{
                        sound.fade(sound.volume(), 0, options.fadeOut * 1000);
                    }}, (options.duration || 3) * 1000 - options.fadeOut * 1000);
                }}

                console.log(`🔊 Playing audio: ${{effectName}}`);
            }} catch (error) {{
                console.warn(`Error playing audio ${{effectName}}:`, error);
            }}
        }}

        // Stop audio effect
        function stopMatrixAudio(effectName) {{
            if (!matrixAudioSystem.enabled || !matrixAudioSystem.isInitialized) {{
                return;
            }}

            const sound = matrixAudioSystem.sounds.get(effectName);
            if (sound) {{
                sound.stop();
                console.log(`🔇 Stopped audio: ${{effectName}}`);
            }}
        }}

        // Set master volume
        function setMatrixAudioVolume(volume) {{
            matrixAudioSystem.masterVolume = Math.max(0, Math.min(1, volume));
            
            // Update all sound volumes
            matrixAudioSystem.sounds.forEach((sound, name) => {{
                const config = matrixAudioSystem.config[name];
                if (config) {{
                    sound.volume(config.volume * matrixAudioSystem.masterVolume);
                }}
            }});
            
            console.log(`🔊 Master volume set to: ${{matrixAudioSystem.masterVolume}}`);
        }}

        // Toggle audio system
        function toggleMatrixAudio() {{
            matrixAudioSystem.enabled = !matrixAudioSystem.enabled;
            
            if (!matrixAudioSystem.enabled) {{
                // Stop all sounds
                matrixAudioSystem.sounds.forEach(sound => sound.stop());
                console.log('🔇 Matrix Audio disabled');
            }} else {{
                console.log('🔊 Matrix Audio enabled');
            }}
            
            return matrixAudioSystem.enabled;
        }}

        // Play audio for message type
        function playMessageAudio(messageType, emotion, priority) {{
            if (!matrixAudioSystem.enabled) return;

            // Play message type sound
            if (matrixAudioSystem.sounds.has(messageType)) {{
                playMatrixAudio(messageType);
            }}

            // Play emotion sound for high priority messages
            if (priority > 7 && matrixAudioSystem.sounds.has(emotion)) {{
                setTimeout(() => {{
                    playMatrixAudio(emotion, {{ volume: 0.3 }});
                }}, 200);
            }}

            // Play special effects
            if (priority >= 9) {{
                setTimeout(() => {{
                    playMatrixAudio('matrix_glitch', {{ volume: 0.4 }});
                }}, 400);
            }}
        }}

        // Start ambient Matrix rain sound
        function startMatrixAmbient() {{
            if (matrixAudioSystem.enabled && matrixAudioSystem.sounds.has('matrix_rain')) {{
                playMatrixAudio('matrix_rain', {{ volume: 0.2 }});
            }}
        }}

        // Stop ambient sounds
        function stopMatrixAmbient() {{
            stopMatrixAudio('matrix_rain');
            stopMatrixAudio('calm');
        }}

        // Audio visualization
        function createAudioVisualization(elementId) {{
            const element = document.getElementById(elementId);
            if (!element) return;

            // Create simple audio visualization bars
            const visualizer = document.createElement('div');
            visualizer.className = 'audio-visualizer';
            visualizer.innerHTML = `
                <div class="audio-bar"></div>
                <div class="audio-bar"></div>
                <div class="audio-bar"></div>
                <div class="audio-bar"></div>
                <div class="audio-bar"></div>
            `;
            
            element.appendChild(visualizer);

            // Animate bars when audio is playing
            const bars = visualizer.querySelectorAll('.audio-bar');
            setInterval(() => {{
                if (matrixAudioSystem.enabled) {{
                    bars.forEach(bar => {{
                        const height = Math.random() * 20 + 5;
                        bar.style.height = height + 'px';
                    }});
                }}
            }}, 100);
        }}

        // Initialize audio when DOM is ready
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', initializeMatrixAudio);
        }} else {{
            initializeMatrixAudio();
        }}
        """
    
    def get_audio_css(self) -> str:
        """Generate CSS for audio visualization"""
        return """
        .audio-controls {
            position: fixed;
            top: 60px;
            left: 10px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #00ff00;
            padding: 10px;
            border-radius: 5px;
            z-index: 25;
        }
        
        .audio-controls h4 {
            color: #00ff00;
            margin: 0 0 10px 0;
            font-size: 14px;
        }
        
        .volume-slider {
            width: 100px;
            margin: 5px 0;
        }
        
        .audio-visualizer {
            display: flex;
            align-items: flex-end;
            height: 30px;
            gap: 2px;
            margin: 10px 0;
        }
        
        .audio-bar {
            width: 4px;
            background: linear-gradient(to top, #00ff00, #008800);
            border-radius: 2px;
            transition: height 0.1s ease;
            min-height: 2px;
        }
        
        .audio-status {
            font-size: 10px;
            color: #00ff00;
            margin-top: 5px;
        }
        
        .audio-toggle {
            background: rgba(0, 255, 0, 0.2);
            border: 1px solid #00ff00;
            color: #00ff00;
            padding: 5px 10px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
            margin: 2px;
        }
        
        .audio-toggle:hover {
            background: rgba(0, 255, 0, 0.4);
        }
        
        .audio-toggle.disabled {
            opacity: 0.5;
            background: rgba(255, 0, 0, 0.2);
            border-color: #ff0000;
            color: #ff0000;
        }
        """
    
    def render_audio_controls(self) -> str:
        """Render audio control panel HTML"""
        return f"""
        <div class="audio-controls">
            <h4>🔊 Audio Controls</h4>
            <button class="audio-toggle" onclick="toggleMatrixAudio()" id="audio-toggle">
                Audio: ON
            </button><br>
            <button class="audio-toggle" onclick="startMatrixAmbient()">
                🌧️ Matrix Rain
            </button><br>
            <button class="audio-toggle" onclick="stopMatrixAmbient()">
                🔇 Stop Ambient
            </button><br>
            <label for="volume-slider">Volume:</label><br>
            <input type="range" id="volume-slider" class="volume-slider" 
                   min="0" max="1" step="0.1" value="0.7" 
                   onchange="setMatrixAudioVolume(this.value)"><br>
            <div id="audio-visualizer-container"></div>
            <div class="audio-status" id="audio-status">Ready</div>
        </div>
        
        <script>
            // Update audio toggle button
            function updateAudioToggle() {{
                const toggle = document.getElementById('audio-toggle');
                const status = document.getElementById('audio-status');
                
                if (matrixAudioSystem.enabled) {{
                    toggle.textContent = 'Audio: ON';
                    toggle.classList.remove('disabled');
                    status.textContent = 'Audio enabled';
                }} else {{
                    toggle.textContent = 'Audio: OFF';
                    toggle.classList.add('disabled');
                    status.textContent = 'Audio disabled';
                }}
            }}
            
            // Initialize audio visualization
            setTimeout(() => {{
                createAudioVisualization('audio-visualizer-container');
                updateAudioToggle();
            }}, 1000);
        </script>
        """
