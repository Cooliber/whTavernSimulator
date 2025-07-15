#!/usr/bin/env python3
"""
Matrix Performance Optimizer
Advanced performance optimizations for Matrix Chat Interface
"""

import streamlit as st
from typing import Dict, List, Optional, Any
import time
import gc
from dataclasses import dataclass

@dataclass
class PerformanceMetrics:
    """Performance metrics tracking"""
    fps: float = 60.0
    memory_usage: float = 0.0
    message_count: int = 0
    effect_count: int = 0
    render_time: float = 0.0
    last_cleanup: float = 0.0

class MatrixPerformanceOptimizer:
    """
    Advanced performance optimizer for Matrix Chat Interface
    Provides intelligent cleanup, caching, and optimization strategies
    """
    
    def __init__(self):
        self.metrics = PerformanceMetrics()
        self.performance_mode = "balanced"  # smooth, balanced, performance
        self.optimization_settings = self._get_optimization_settings()
    
    def _get_optimization_settings(self) -> Dict[str, Any]:
        """Get optimization settings based on performance mode"""
        settings = {
            "smooth": {
                "max_messages": 100,
                "max_effects": 50,
                "cleanup_interval": 30,
                "animation_quality": "high",
                "particle_count": 500,
                "effect_duration_multiplier": 1.0
            },
            "balanced": {
                "max_messages": 75,
                "max_effects": 30,
                "cleanup_interval": 20,
                "animation_quality": "medium",
                "particle_count": 300,
                "effect_duration_multiplier": 0.8
            },
            "performance": {
                "max_messages": 50,
                "max_effects": 20,
                "cleanup_interval": 10,
                "animation_quality": "low",
                "particle_count": 150,
                "effect_duration_multiplier": 0.6
            }
        }
        return settings.get(self.performance_mode, settings["balanced"])
    
    def set_performance_mode(self, mode: str):
        """Set performance mode and update settings"""
        if mode in ["smooth", "balanced", "performance"]:
            self.performance_mode = mode
            self.optimization_settings = self._get_optimization_settings()
            st.session_state.matrix_chat_state['performance']['mode'] = mode
    
    def get_performance_javascript(self) -> str:
        """Generate JavaScript for performance optimization"""
        return f"""
        // Matrix Performance Optimizer
        let matrixPerformanceOptimizer = {{
            settings: {self.optimization_settings},
            metrics: {{
                fps: 60,
                memoryUsage: 0,
                messageCount: 0,
                effectCount: 0,
                renderTime: 0,
                lastCleanup: Date.now()
            }},
            isOptimizing: false
        }};

        // Performance monitoring
        function startPerformanceOptimization() {{
            console.log('⚡ Starting Matrix Performance Optimization...');
            
            // Monitor FPS
            let frameCount = 0;
            let lastTime = performance.now();
            
            function monitorPerformance() {{
                const currentTime = performance.now();
                frameCount++;
                
                // Calculate FPS every second
                if (currentTime - lastTime >= 1000) {{
                    matrixPerformanceOptimizer.metrics.fps = Math.round(frameCount * 1000 / (currentTime - lastTime));
                    frameCount = 0;
                    lastTime = currentTime;
                    
                    // Check if optimization is needed
                    checkPerformanceThresholds();
                }}
                
                requestAnimationFrame(monitorPerformance);
            }}
            
            requestAnimationFrame(monitorPerformance);
            
            // Start periodic cleanup
            setInterval(performPeriodicCleanup, matrixPerformanceOptimizer.settings.cleanup_interval * 1000);
            
            matrixPerformanceOptimizer.isOptimizing = true;
        }}

        function checkPerformanceThresholds() {{
            const fps = matrixPerformanceOptimizer.metrics.fps;
            const messageCount = document.querySelectorAll('.chat-message').length;
            const effectCount = matrixChatSystem.activeEffects.size;
            
            // Auto-adjust quality based on FPS
            if (fps < 30) {{
                console.warn('⚠️ Low FPS detected, reducing quality...');
                reduceQuality();
            }} else if (fps > 55 && matrixPerformanceOptimizer.settings.animation_quality === 'low') {{
                console.log('✅ Good FPS, increasing quality...');
                increaseQuality();
            }}
            
            // Force cleanup if too many messages
            if (messageCount > matrixPerformanceOptimizer.settings.max_messages) {{
                console.log('🧹 Too many messages, forcing cleanup...');
                forceMessageCleanup();
            }}
            
            // Limit active effects
            if (effectCount > matrixPerformanceOptimizer.settings.max_effects) {{
                console.log('🎭 Too many effects, cleaning up...');
                cleanupOldEffects();
            }}
        }}

        function reduceQuality() {{
            // Reduce particle count
            if (window.pJSDom && window.pJSDom[0]) {{
                const particles = window.pJSDom[0].pJS.particles;
                particles.number.value = Math.max(50, particles.number.value * 0.7);
                window.pJSDom[0].pJS.fn.particlesRefresh();
            }}
            
            // Reduce animation duration
            gsap.globalTimeline.timeScale(1.5);
            
            // Disable some effects
            matrixPerformanceOptimizer.settings.animation_quality = 'low';
        }}

        function increaseQuality() {{
            // Increase particle count gradually
            if (window.pJSDom && window.pJSDom[0]) {{
                const particles = window.pJSDom[0].pJS.particles;
                particles.number.value = Math.min(300, particles.number.value * 1.2);
                window.pJSDom[0].pJS.fn.particlesRefresh();
            }}
            
            // Normal animation speed
            gsap.globalTimeline.timeScale(1.0);
            
            // Enable more effects
            matrixPerformanceOptimizer.settings.animation_quality = 'medium';
        }}

        function performPeriodicCleanup() {{
            const now = Date.now();
            
            // Clean up old messages
            cleanupOldMessages();
            
            // Clean up completed animations
            cleanupCompletedAnimations();
            
            // Force garbage collection if available
            if (window.gc) {{
                window.gc();
            }}
            
            // Update metrics
            matrixPerformanceOptimizer.metrics.lastCleanup = now;
            matrixPerformanceOptimizer.metrics.messageCount = document.querySelectorAll('.chat-message').length;
            matrixPerformanceOptimizer.metrics.effectCount = matrixChatSystem.activeEffects.size;
            
            console.log('🧹 Periodic cleanup completed');
        }}

        function cleanupOldMessages() {{
            const messages = document.querySelectorAll('.chat-message');
            const maxMessages = matrixPerformanceOptimizer.settings.max_messages;
            
            if (messages.length > maxMessages) {{
                const messagesToRemove = messages.length - maxMessages;
                
                for (let i = 0; i < messagesToRemove; i++) {{
                    const messageEl = messages[i];
                    const messageId = messageEl.getAttribute('data-message-id');
                    
                    // Remove from active effects
                    if (messageId) {{
                        matrixChatSystem.activeEffects.delete(messageId);
                    }}
                    
                    // Animate out and remove
                    gsap.to(messageEl, {{
                        opacity: 0,
                        scale: 0.8,
                        duration: 0.3,
                        ease: "power2.in",
                        onComplete: () => messageEl.remove()
                    }});
                }}
            }}
        }}

        function forceMessageCleanup() {{
            const messages = document.querySelectorAll('.chat-message');
            const keepCount = Math.floor(matrixPerformanceOptimizer.settings.max_messages * 0.7);
            
            if (messages.length > keepCount) {{
                const messagesToRemove = messages.length - keepCount;
                
                for (let i = 0; i < messagesToRemove; i++) {{
                    const messageEl = messages[i];
                    const messageId = messageEl.getAttribute('data-message-id');
                    
                    if (messageId) {{
                        matrixChatSystem.activeEffects.delete(messageId);
                    }}
                    
                    messageEl.remove();
                }}
            }}
        }}

        function cleanupCompletedAnimations() {{
            // Remove completed GSAP animations
            gsap.globalTimeline.getChildren().forEach(animation => {{
                if (animation.progress() === 1 && !animation.repeat()) {{
                    animation.kill();
                }}
            }});
        }}

        function optimizeForDevice() {{
            // Detect device capabilities
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            
            let deviceScore = 100;
            
            // Check WebGL support
            if (!gl) {{
                deviceScore -= 30;
            }}
            
            // Check memory
            if (navigator.deviceMemory) {{
                if (navigator.deviceMemory < 4) {{
                    deviceScore -= 20;
                }}
            }}
            
            // Check CPU cores
            if (navigator.hardwareConcurrency) {{
                if (navigator.hardwareConcurrency < 4) {{
                    deviceScore -= 15;
                }}
            }}
            
            // Adjust settings based on device score
            if (deviceScore < 60) {{
                matrixPerformanceOptimizer.settings = {{
                    ...matrixPerformanceOptimizer.settings,
                    max_messages: 30,
                    max_effects: 10,
                    particle_count: 100,
                    animation_quality: 'low'
                }};
                console.log('📱 Low-end device detected, using performance mode');
            }} else if (deviceScore > 85) {{
                matrixPerformanceOptimizer.settings = {{
                    ...matrixPerformanceOptimizer.settings,
                    max_messages: 150,
                    max_effects: 60,
                    particle_count: 600,
                    animation_quality: 'high'
                }};
                console.log('💻 High-end device detected, using smooth mode');
            }}
        }}

        function getPerformanceReport() {{
            return {{
                fps: matrixPerformanceOptimizer.metrics.fps,
                messageCount: matrixPerformanceOptimizer.metrics.messageCount,
                effectCount: matrixPerformanceOptimizer.metrics.effectCount,
                memoryUsage: performance.memory ? Math.round(performance.memory.usedJSHeapSize / 1048576) : 0,
                settings: matrixPerformanceOptimizer.settings,
                recommendations: getPerformanceRecommendations()
            }};
        }}

        function getPerformanceRecommendations() {{
            const recommendations = [];
            
            if (matrixPerformanceOptimizer.metrics.fps < 30) {{
                recommendations.push('Consider reducing particle count or disabling Matrix rain');
            }}
            
            if (matrixPerformanceOptimizer.metrics.messageCount > 100) {{
                recommendations.push('Clear old messages to improve performance');
            }}
            
            if (matrixPerformanceOptimizer.metrics.effectCount > 50) {{
                recommendations.push('Reduce active effects for better performance');
            }}
            
            return recommendations;
        }}

        // Initialize optimization when DOM is ready
        if (document.readyState === 'loading') {{
            document.addEventListener('DOMContentLoaded', () => {{
                optimizeForDevice();
                startPerformanceOptimization();
            }});
        }} else {{
            optimizeForDevice();
            startPerformanceOptimization();
        }}
        """
    
    def get_performance_css(self) -> str:
        """Generate CSS for performance indicators"""
        return """
        .performance-indicator {
            position: fixed;
            bottom: 60px;
            right: 10px;
            background: rgba(0, 0, 0, 0.9);
            border: 1px solid #00ff00;
            padding: 8px;
            border-radius: 5px;
            font-size: 10px;
            z-index: 30;
            min-width: 120px;
        }
        
        .performance-indicator h5 {
            color: #00ff00;
            margin: 0 0 5px 0;
            font-size: 11px;
        }
        
        .perf-metric {
            display: flex;
            justify-content: space-between;
            margin: 2px 0;
            color: #ffffff;
        }
        
        .perf-value {
            color: #00ff00;
            font-weight: bold;
        }
        
        .perf-status {
            padding: 2px 4px;
            border-radius: 2px;
            font-size: 9px;
            margin-top: 5px;
        }
        
        .perf-status.good {
            background: rgba(0, 255, 0, 0.2);
            color: #00ff00;
        }
        
        .perf-status.warning {
            background: rgba(255, 255, 0, 0.2);
            color: #ffff00;
        }
        
        .perf-status.critical {
            background: rgba(255, 0, 0, 0.2);
            color: #ff0000;
        }
        
        .optimization-controls {
            position: fixed;
            bottom: 10px;
            left: 200px;
            background: rgba(0, 0, 0, 0.8);
            border: 1px solid #00ff00;
            padding: 10px;
            border-radius: 5px;
            z-index: 25;
        }
        
        .optimization-controls h4 {
            color: #00ff00;
            margin: 0 0 10px 0;
            font-size: 14px;
        }
        
        .perf-mode-btn {
            background: rgba(0, 255, 0, 0.2);
            border: 1px solid #00ff00;
            color: #00ff00;
            padding: 4px 8px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 11px;
            margin: 2px;
        }
        
        .perf-mode-btn:hover {
            background: rgba(0, 255, 0, 0.4);
        }
        
        .perf-mode-btn.active {
            background: rgba(0, 255, 0, 0.6);
            font-weight: bold;
        }
        """
    
    def render_performance_controls(self) -> str:
        """Render performance control panel HTML"""
        return f"""
        <div class="performance-indicator">
            <h5>⚡ Performance</h5>
            <div class="perf-metric">
                <span>FPS:</span>
                <span class="perf-value" id="perf-fps">60</span>
            </div>
            <div class="perf-metric">
                <span>Messages:</span>
                <span class="perf-value" id="perf-messages">0</span>
            </div>
            <div class="perf-metric">
                <span>Effects:</span>
                <span class="perf-value" id="perf-effects">0</span>
            </div>
            <div class="perf-metric">
                <span>Memory:</span>
                <span class="perf-value" id="perf-memory">0MB</span>
            </div>
            <div class="perf-status good" id="perf-status">Optimal</div>
        </div>
        
        <div class="optimization-controls">
            <h4>⚡ Optimization</h4>
            <button class="perf-mode-btn active" onclick="setPerformanceMode('balanced')" id="mode-balanced">
                Balanced
            </button><br>
            <button class="perf-mode-btn" onclick="setPerformanceMode('smooth')" id="mode-smooth">
                Smooth
            </button><br>
            <button class="perf-mode-btn" onclick="setPerformanceMode('performance')" id="mode-performance">
                Performance
            </button><br>
            <button class="perf-mode-btn" onclick="forceCleanup()">
                🧹 Cleanup
            </button><br>
            <button class="perf-mode-btn" onclick="showPerformanceReport()">
                📊 Report
            </button>
        </div>
        
        <script>
            function setPerformanceMode(mode) {{
                // Update active button
                document.querySelectorAll('.perf-mode-btn').forEach(btn => btn.classList.remove('active'));
                document.getElementById('mode-' + mode).classList.add('active');
                
                // Update optimizer settings
                matrixPerformanceOptimizer.settings = {{
                    'smooth': {{
                        max_messages: 100,
                        max_effects: 50,
                        cleanup_interval: 30,
                        animation_quality: 'high',
                        particle_count: 500
                    }},
                    'balanced': {{
                        max_messages: 75,
                        max_effects: 30,
                        cleanup_interval: 20,
                        animation_quality: 'medium',
                        particle_count: 300
                    }},
                    'performance': {{
                        max_messages: 50,
                        max_effects: 20,
                        cleanup_interval: 10,
                        animation_quality: 'low',
                        particle_count: 150
                    }}
                }}[mode];
                
                console.log(`⚡ Performance mode set to: ${{mode}}`);
            }}
            
            function forceCleanup() {{
                performPeriodicCleanup();
                console.log('🧹 Manual cleanup performed');
            }}
            
            function showPerformanceReport() {{
                const report = getPerformanceReport();
                console.log('📊 Performance Report:', report);
                alert(`Performance Report:
FPS: ${{report.fps}}
Messages: ${{report.messageCount}}
Effects: ${{report.effectCount}}
Memory: ${{report.memoryUsage}}MB

Recommendations:
${{report.recommendations.join('\\n')}}`);
            }}
            
            // Update performance display
            setInterval(() => {{
                if (typeof matrixPerformanceOptimizer !== 'undefined') {{
                    document.getElementById('perf-fps').textContent = matrixPerformanceOptimizer.metrics.fps;
                    document.getElementById('perf-messages').textContent = matrixPerformanceOptimizer.metrics.messageCount;
                    document.getElementById('perf-effects').textContent = matrixPerformanceOptimizer.metrics.effectCount;
                    
                    if (performance.memory) {{
                        document.getElementById('perf-memory').textContent = 
                            Math.round(performance.memory.usedJSHeapSize / 1048576) + 'MB';
                    }}
                    
                    // Update status
                    const statusEl = document.getElementById('perf-status');
                    const fps = matrixPerformanceOptimizer.metrics.fps;
                    
                    if (fps >= 50) {{
                        statusEl.textContent = 'Optimal';
                        statusEl.className = 'perf-status good';
                    }} else if (fps >= 30) {{
                        statusEl.textContent = 'Good';
                        statusEl.className = 'perf-status warning';
                    }} else {{
                        statusEl.textContent = 'Poor';
                        statusEl.className = 'perf-status critical';
                    }}
                }}
            }}, 1000);
        </script>
        """
