#!/usr/bin/env python3
"""
Three.js Integration Component for Warhammer Tavern Simulator
Advanced 3D visualization and animation system
"""

import streamlit as st
import streamlit.components.v1 as components
from typing import Dict, List, Optional, Any
import json
import time
from dataclasses import dataclass, asdict
from enum import Enum

class RenderQuality(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    ULTRA = "ultra"

@dataclass
class Character3D:
    id: str
    name: str
    faction: str
    position: Dict[str, float]
    rotation: Dict[str, float]
    scale: Dict[str, float]
    animation_state: str
    emotion: str
    health: float

@dataclass
class TavernEnvironment:
    lighting: Dict[str, Any]
    weather: str
    time_of_day: str
    atmosphere: Dict[str, Any]
    interactive_objects: List[Dict[str, Any]]

@dataclass
class PerformanceMetrics:
    fps: float
    frame_time: float
    memory_usage: float
    draw_calls: int
    triangle_count: int
    texture_memory: float

class ThreeJSIntegration:
    """
    Advanced Three.js integration for Streamlit with performance optimization
    """

    def __init__(self):
        self.component_id = "threejs_warhammer_tavern"
        self.performance_monitor = PerformanceMonitor()
        self.quality_settings = RenderQuality.HIGH
        self.adaptive_quality = True

        # Initialize session state
        if 'threejs_state' not in st.session_state:
            st.session_state.threejs_state = {
                'initialized': False,
                'characters': {},
                'environment': None,
                'performance_metrics': None
            }

    def render_3d_tavern(self,
                        characters: List[Character3D],
                        environment: TavernEnvironment,
                        relationships: List[Dict],
                        height: int = 800,
                        enable_vr: bool = False) -> Optional[Dict]:
        """
        Render the 3D tavern environment with characters and interactions
        """

        # Update session state
        st.session_state.threejs_state['characters'] = {
            char.id: asdict(char) for char in characters
        }
        st.session_state.threejs_state['environment'] = asdict(environment)

        # Generate Three.js HTML
        html_content = self._generate_threejs_html(
            characters, environment, relationships, enable_vr
        )

        # Render component
        component_value = components.html(
            html_content,
            height=height,
            scrolling=False
        )

        # Process return data
        if component_value and isinstance(component_value, dict):
            self._process_component_data(component_value)

        return component_value

    def _generate_threejs_html(self,
                              characters: List[Character3D],
                              environment: TavernEnvironment,
                              relationships: List[Dict],
                              enable_vr: bool) -> str:
        """
        Generate complete Three.js HTML with embedded data and scripts
        """

        characters_data = [asdict(char) for char in characters]
        environment_data = asdict(environment)

        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>Warhammer Tavern 3D</title>

            <!-- Three.js Core -->
            <script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r150/three.min.js"></script>

            <!-- Three.js Loaders -->
            <script src="https://cdn.jsdelivr.net/npm/three@0.150.0/examples/js/loaders/GLTFLoader.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/three@0.150.0/examples/js/loaders/DRACOLoader.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/three@0.150.0/examples/js/loaders/TextureLoader.js"></script>

            <!-- Three.js Controls -->
            <script src="https://cdn.jsdelivr.net/npm/three@0.150.0/examples/js/controls/OrbitControls.js"></script>

            <!-- Three.js Post-processing -->
            <script src="https://cdn.jsdelivr.net/npm/three@0.150.0/examples/js/postprocessing/EffectComposer.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/three@0.150.0/examples/js/postprocessing/RenderPass.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/three@0.150.0/examples/js/postprocessing/UnrealBloomPass.js"></script>

            <!-- WebXR Support -->
            {self._get_webxr_scripts() if enable_vr else ''}

            <!-- Performance Monitoring -->
            <script src="https://cdnjs.cloudflare.com/ajax/libs/stats.js/r17/Stats.min.js"></script>

            <!-- Animation Library -->
            <script src="https://cdnjs.cloudflare.com/ajax/libs/animejs/3.2.1/anime.min.js"></script>

            <style>
                {self._get_css_styles()}
            </style>
        </head>
        <body>
            <div id="threejs-container"></div>
            <div id="ui-overlay">
                <div id="performance-panel">
                    <h3>Performance</h3>
                    <div>FPS: <span id="fps">0</span></div>
                    <div>Frame Time: <span id="frame-time">0</span>ms</div>
                    <div>Memory: <span id="memory">0</span>MB</div>
                    <div>Draw Calls: <span id="draw-calls">0</span></div>
                </div>

                <div id="controls-panel">
                    <h3>Controls</h3>
                    <button id="toggle-quality">Quality: <span id="quality-level">High</span></button>
                    <button id="toggle-lighting">Toggle Lighting</button>
                    <button id="reset-camera">Reset Camera</button>
                    {f'<button id="enter-vr">Enter VR</button>' if enable_vr else ''}
                </div>

                <div id="character-panel">
                    <h3>Characters</h3>
                    <div id="character-list"></div>
                </div>
            </div>

            <script>
                // Embedded data
                const CHARACTERS_DATA = {json.dumps(characters_data)};
                const ENVIRONMENT_DATA = {json.dumps(environment_data)};
                const RELATIONSHIPS_DATA = {json.dumps(relationships)};
                const ENABLE_VR = {json.dumps(enable_vr)};
                const QUALITY_SETTING = "{self.quality_settings.value}";

                // Initialize application
                {self._get_threejs_application_code()}
            </script>
        </body>
        </html>
        """

    def _get_css_styles(self) -> str:
        """Get CSS styles for the Three.js component"""
        return """
            body {
                margin: 0;
                padding: 0;
                overflow: hidden;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: #1a1a1a;
                color: #ffffff;
            }

            #threejs-container {
                width: 100vw;
                height: 100vh;
                position: relative;
            }

            #ui-overlay {
                position: absolute;
                top: 0;
                left: 0;
                z-index: 1000;
                pointer-events: none;
            }

            #ui-overlay > div {
                background: rgba(0, 0, 0, 0.8);
                border: 1px solid #444;
                border-radius: 8px;
                padding: 15px;
                margin: 10px;
                min-width: 200px;
                pointer-events: auto;
                backdrop-filter: blur(10px);
            }

            #performance-panel {
                position: absolute;
                top: 10px;
                left: 10px;
            }

            #controls-panel {
                position: absolute;
                top: 10px;
                right: 10px;
            }

            #character-panel {
                position: absolute;
                bottom: 10px;
                left: 10px;
                max-height: 300px;
                overflow-y: auto;
            }

            button {
                background: #8b0000;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                cursor: pointer;
                margin: 2px;
                transition: background 0.3s;
            }

            button:hover {
                background: #a00000;
            }

            .character-item {
                display: flex;
                align-items: center;
                padding: 5px;
                margin: 2px 0;
                background: rgba(139, 0, 0, 0.2);
                border-radius: 4px;
                cursor: pointer;
            }

            .character-item:hover {
                background: rgba(139, 0, 0, 0.4);
            }

            .character-status {
                width: 10px;
                height: 10px;
                border-radius: 50%;
                margin-right: 8px;
            }

            .status-healthy { background: #00ff00; }
            .status-injured { background: #ffff00; }
            .status-critical { background: #ff0000; }
        """

    def _get_webxr_scripts(self) -> str:
        """Get WebXR support scripts"""
        return """
            <script src="https://cdn.jsdelivr.net/npm/three@0.150.0/examples/js/webxr/VRButton.js"></script>
            <script src="https://cdn.jsdelivr.net/npm/three@0.150.0/examples/js/webxr/XRControllerModelFactory.js"></script>
        """

    def _process_component_data(self, data: Dict):
        """Process data returned from the Three.js component"""
        try:
            if isinstance(data, dict) and 'performance' in data:
                metrics = PerformanceMetrics(**data['performance'])
                self.performance_monitor.update_metrics(metrics)
                st.session_state.threejs_state['performance_metrics'] = metrics

            if isinstance(data, dict) and 'interactions' in data:
                # Handle user interactions (character clicks, object interactions, etc.)
                self._handle_interactions(data['interactions'])
        except Exception as e:
            st.error(f"Error processing component data: {e}")
            # Log the error but don't crash the app

    def _handle_interactions(self, interactions: List[Dict]):
        """Handle user interactions from the 3D scene"""
        for interaction in interactions:
            if interaction['type'] == 'character_click':
                st.session_state.selected_character = interaction['character_id']
            elif interaction['type'] == 'object_interaction':
                st.session_state.last_interaction = interaction

    def get_performance_metrics(self) -> Optional[PerformanceMetrics]:
        """Get current performance metrics"""
        return st.session_state.threejs_state.get('performance_metrics')

    def update_character(self, character_id: str, updates: Dict):
        """Update a specific character's properties"""
        if character_id in st.session_state.threejs_state['characters']:
            st.session_state.threejs_state['characters'][character_id].update(updates)
            # Trigger component update
            st.rerun()

    def _get_threejs_application_code(self) -> str:
        """Get the main Three.js application code"""
        return """
            // Global variables
            let scene, camera, renderer, controls;
            let characters = new Map();
            let environment = null;
            let performanceStats = null;
            let animationMixer = null;
            let clock = new THREE.Clock();

            // Performance monitoring
            let frameCount = 0;
            let lastTime = performance.now();
            let performanceData = {
                fps: 0,
                frameTime: 0,
                memoryUsage: 0,
                drawCalls: 0,
                triangleCount: 0
            };

            // Initialize the application
            function init() {
                setupScene();
                setupRenderer();
                setupCamera();
                setupControls();
                setupLighting();
                setupPerformanceMonitoring();
                loadEnvironment();
                loadCharacters();
                setupEventListeners();
                animate();
            }

            function setupScene() {
                scene = new THREE.Scene();
                scene.background = new THREE.Color(0x1a1a1a);
                scene.fog = new THREE.Fog(0x1a1a1a, 10, 50);
            }

            function setupRenderer() {
                const container = document.getElementById('threejs-container');
                renderer = new THREE.WebGLRenderer({
                    antialias: true,
                    powerPreference: "high-performance"
                });

                renderer.setSize(container.clientWidth, container.clientHeight);
                renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
                renderer.shadowMap.enabled = true;
                renderer.shadowMap.type = THREE.PCFSoftShadowMap;
                renderer.outputEncoding = THREE.sRGBEncoding;
                renderer.toneMapping = THREE.ACESFilmicToneMapping;
                renderer.toneMappingExposure = 1.2;

                container.appendChild(renderer.domElement);

                // WebXR setup if enabled
                if (ENABLE_VR && 'xr' in navigator) {
                    renderer.xr.enabled = true;
                    setupVR();
                }
            }

            function setupCamera() {
                const container = document.getElementById('threejs-container');
                camera = new THREE.PerspectiveCamera(
                    75,
                    container.clientWidth / container.clientHeight,
                    0.1,
                    1000
                );
                camera.position.set(0, 5, 10);
                camera.lookAt(0, 0, 0);
            }

            function setupControls() {
                controls = new THREE.OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.05;
                controls.maxPolarAngle = Math.PI / 2;
                controls.minDistance = 2;
                controls.maxDistance = 50;
            }

            function setupLighting() {
                // Ambient light
                const ambientLight = new THREE.AmbientLight(0x404040, 0.3);
                scene.add(ambientLight);

                // Main directional light (sun)
                const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
                directionalLight.position.set(10, 10, 5);
                directionalLight.castShadow = true;
                directionalLight.shadow.mapSize.width = 2048;
                directionalLight.shadow.mapSize.height = 2048;
                directionalLight.shadow.camera.near = 0.5;
                directionalLight.shadow.camera.far = 50;
                scene.add(directionalLight);

                // Fireplace light
                const fireplaceLight = new THREE.PointLight(0xff4500, 2, 10);
                fireplaceLight.position.set(-8, 2, 0);
                fireplaceLight.castShadow = true;
                scene.add(fireplaceLight);

                // Animate fireplace flickering
                animateFireplaceLight(fireplaceLight);
            }

            function animateFireplaceLight(light) {
                if (typeof anime !== 'undefined') {
                    anime({
                        targets: light,
                        intensity: [1.5, 2.5],
                        duration: anime.random(100, 300),
                        easing: 'easeInOutSine',
                        complete: () => animateFireplaceLight(light)
                    });
                }
            }

            function setupPerformanceMonitoring() {
                if (typeof Stats !== 'undefined') {
                    performanceStats = new Stats();
                    performanceStats.showPanel(0);
                    const perfPanel = document.getElementById('performance-panel');
                    if (perfPanel) {
                        perfPanel.appendChild(performanceStats.dom);
                    }
                }

                // Custom performance tracking
                setInterval(updatePerformanceMetrics, 1000);
            }

            function updatePerformanceMetrics() {
                const now = performance.now();
                const deltaTime = now - lastTime;
                performanceData.fps = Math.round(1000 / (deltaTime / frameCount));
                performanceData.frameTime = deltaTime / frameCount;

                if (performance.memory) {
                    performanceData.memoryUsage = Math.round(performance.memory.usedJSHeapSize / 1048576);
                }

                // Update UI
                const fpsEl = document.getElementById('fps');
                const frameTimeEl = document.getElementById('frame-time');
                const memoryEl = document.getElementById('memory');

                if (fpsEl) fpsEl.textContent = performanceData.fps;
                if (frameTimeEl) frameTimeEl.textContent = performanceData.frameTime.toFixed(1);
                if (memoryEl) memoryEl.textContent = performanceData.memoryUsage;

                // Send data back to Streamlit
                sendDataToStreamlit({
                    type: 'performance',
                    data: performanceData
                });

                frameCount = 0;
                lastTime = now;
            }

            async function loadEnvironment() {
                // Create tavern base
                const tavernGeometry = new THREE.BoxGeometry(20, 8, 20);
                const tavernMaterial = new THREE.MeshStandardMaterial({
                    color: 0x8B4513,
                    roughness: 0.8,
                    metalness: 0.1
                });

                const tavern = new THREE.Mesh(tavernGeometry, tavernMaterial);
                tavern.position.y = 4;
                tavern.castShadow = true;
                tavern.receiveShadow = true;
                scene.add(tavern);

                // Add floor
                const floorGeometry = new THREE.PlaneGeometry(30, 30);
                const floorMaterial = new THREE.MeshStandardMaterial({
                    color: 0x654321,
                    roughness: 0.9
                });

                const floor = new THREE.Mesh(floorGeometry, floorMaterial);
                floor.rotation.x = -Math.PI / 2;
                floor.receiveShadow = true;
                scene.add(floor);

                // Load interactive objects based on environment data
                loadInteractiveObjects();
            }

            function loadInteractiveObjects() {
                const objects = ENVIRONMENT_DATA.interactive_objects || [];

                objects.forEach(objData => {
                    createInteractiveObject(objData);
                });
            }

            function createInteractiveObject(objData) {
                let geometry, material;

                switch(objData.type) {
                    case 'bar':
                        geometry = new THREE.BoxGeometry(4, 2, 1);
                        material = new THREE.MeshStandardMaterial({ color: 0x8B4513 });
                        break;
                    case 'table':
                        geometry = new THREE.CylinderGeometry(1, 1, 0.1, 8);
                        material = new THREE.MeshStandardMaterial({ color: 0x654321 });
                        break;
                    case 'fireplace':
                        geometry = new THREE.BoxGeometry(2, 3, 1);
                        material = new THREE.MeshStandardMaterial({ color: 0x333333 });
                        break;
                    default:
                        geometry = new THREE.BoxGeometry(1, 1, 1);
                        material = new THREE.MeshStandardMaterial({ color: 0x888888 });
                }

                const mesh = new THREE.Mesh(geometry, material);
                mesh.position.set(objData.position.x, objData.position.y, objData.position.z);
                mesh.castShadow = true;
                mesh.receiveShadow = true;
                mesh.userData = { type: objData.type, interactive: true };

                scene.add(mesh);
            }

            async function loadCharacters() {
                for (const charData of CHARACTERS_DATA) {
                    await createCharacter(charData);
                }

                updateCharacterList();
            }

            async function createCharacter(charData) {
                // Create simple character representation (can be replaced with GLTF models)
                const characterGroup = new THREE.Group();

                // Body
                const bodyGeometry = new THREE.CapsuleGeometry(0.3, 1.5, 4, 8);
                const bodyMaterial = new THREE.MeshStandardMaterial({
                    color: getFactionColor(charData.faction)
                });
                const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
                body.position.y = 1;
                body.castShadow = true;
                characterGroup.add(body);

                // Head
                const headGeometry = new THREE.SphereGeometry(0.2, 16, 16);
                const headMaterial = new THREE.MeshStandardMaterial({ color: 0xffdbac });
                const head = new THREE.Mesh(headGeometry, headMaterial);
                head.position.y = 2;
                head.castShadow = true;
                characterGroup.add(head);

                // Position character
                characterGroup.position.set(
                    charData.position.x,
                    charData.position.y,
                    charData.position.z
                );

                characterGroup.userData = {
                    id: charData.id,
                    name: charData.name,
                    faction: charData.faction,
                    interactive: true
                };

                characters.set(charData.id, characterGroup);
                scene.add(characterGroup);

                // Add character animation
                animateCharacterEntrance(characterGroup);
            }

            function getFactionColor(faction) {
                const colors = {
                    'empire': 0x0066cc,
                    'chaos': 0x8b0000,
                    'dwarf': 0x8b4513,
                    'elf': 0x228b22,
                    'orc': 0x556b2f,
                    'undead': 0x2f2f2f
                };
                return colors[faction.toLowerCase()] || 0x888888;
            }

            function animateCharacterEntrance(character) {
                // Initial state
                character.scale.set(0, 0, 0);
                character.rotation.y = Math.PI * 2;

                // Entrance animation using basic JavaScript animation
                const startTime = performance.now();
                const duration = 1000;

                function animate() {
                    const elapsed = performance.now() - startTime;
                    const progress = Math.min(elapsed / duration, 1);

                    // Elastic easing approximation
                    const easeProgress = progress === 1 ? 1 : 1 - Math.pow(2, -10 * progress) * Math.cos((progress * 10 - 0.75) * (2 * Math.PI) / 3);

                    character.scale.setScalar(easeProgress);
                    character.rotation.y = (1 - progress) * Math.PI * 2;

                    if (progress < 1) {
                        requestAnimationFrame(animate);
                    }
                }

                animate();
            }

            function updateCharacterList() {
                const characterList = document.getElementById('character-list');
                if (!characterList) return;

                characterList.innerHTML = '';

                characters.forEach((character, id) => {
                    const charData = CHARACTERS_DATA.find(c => c.id === id);
                    if (charData) {
                        const item = document.createElement('div');
                        item.className = 'character-item';
                        item.innerHTML = `
                            <div class="character-status status-${getHealthStatus(charData.health)}"></div>
                            <span>${charData.name}</span>
                        `;
                        item.onclick = () => focusOnCharacter(id);
                        characterList.appendChild(item);
                    }
                });
            }

            function getHealthStatus(health) {
                if (health > 0.7) return 'healthy';
                if (health > 0.3) return 'injured';
                return 'critical';
            }

            function focusOnCharacter(characterId) {
                const character = characters.get(characterId);
                if (character) {
                    // Smooth camera transition to character
                    const targetPos = {
                        x: character.position.x + 3,
                        y: character.position.y + 2,
                        z: character.position.z + 3
                    };

                    // Simple camera animation
                    const startPos = { x: camera.position.x, y: camera.position.y, z: camera.position.z };
                    const startTime = performance.now();
                    const duration = 1000;

                    function animateCamera() {
                        const elapsed = performance.now() - startTime;
                        const progress = Math.min(elapsed / duration, 1);
                        const easeProgress = 1 - Math.pow(1 - progress, 3); // Cubic ease out

                        camera.position.x = startPos.x + (targetPos.x - startPos.x) * easeProgress;
                        camera.position.y = startPos.y + (targetPos.y - startPos.y) * easeProgress;
                        camera.position.z = startPos.z + (targetPos.z - startPos.z) * easeProgress;

                        camera.lookAt(character.position);

                        if (progress < 1) {
                            requestAnimationFrame(animateCamera);
                        }
                    }

                    animateCamera();

                    // Send interaction data to Streamlit
                    sendDataToStreamlit({
                        type: 'interaction',
                        data: {
                            type: 'character_focus',
                            character_id: characterId
                        }
                    });
                }
            }

            function setupEventListeners() {
                // Window resize
                window.addEventListener('resize', onWindowResize);

                // Mouse interactions
                const raycaster = new THREE.Raycaster();
                const mouse = new THREE.Vector2();

                renderer.domElement.addEventListener('click', (event) => {
                    const rect = renderer.domElement.getBoundingClientRect();
                    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
                    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;

                    raycaster.setFromCamera(mouse, camera);
                    const intersects = raycaster.intersectObjects(scene.children, true);

                    if (intersects.length > 0) {
                        const object = intersects[0].object;
                        handleObjectClick(object);
                    }
                });

                // UI Controls
                const toggleQualityBtn = document.getElementById('toggle-quality');
                const resetCameraBtn = document.getElementById('reset-camera');

                if (toggleQualityBtn) toggleQualityBtn.onclick = toggleQuality;
                if (resetCameraBtn) resetCameraBtn.onclick = resetCamera;

                if (ENABLE_VR) {
                    const enterVRBtn = document.getElementById('enter-vr');
                    if (enterVRBtn) enterVRBtn.onclick = enterVR;
                }
            }

            function handleObjectClick(object) {
                // Find the top-level object with userData
                let targetObject = object;
                while (targetObject.parent && !targetObject.userData.interactive) {
                    targetObject = targetObject.parent;
                }

                if (targetObject.userData.interactive) {
                    if (targetObject.userData.id) {
                        // Character clicked
                        focusOnCharacter(targetObject.userData.id);
                    } else {
                        // Interactive object clicked
                        sendDataToStreamlit({
                            type: 'interaction',
                            data: {
                                type: 'object_interaction',
                                object_type: targetObject.userData.type
                            }
                        });
                    }
                }
            }

            function onWindowResize() {
                const container = document.getElementById('threejs-container');
                camera.aspect = container.clientWidth / container.clientHeight;
                camera.updateProjectionMatrix();
                renderer.setSize(container.clientWidth, container.clientHeight);
            }

            function toggleQuality() {
                const qualityLevels = ['low', 'medium', 'high', 'ultra'];
                const currentIndex = qualityLevels.indexOf(QUALITY_SETTING);
                const nextIndex = (currentIndex + 1) % qualityLevels.length;
                const newQuality = qualityLevels[nextIndex];

                applyQualitySettings(newQuality);
                const qualityLevelEl = document.getElementById('quality-level');
                if (qualityLevelEl) {
                    qualityLevelEl.textContent = newQuality.charAt(0).toUpperCase() + newQuality.slice(1);
                }
            }

            function applyQualitySettings(quality) {
                switch(quality) {
                    case 'low':
                        renderer.setPixelRatio(0.5);
                        renderer.shadowMap.enabled = false;
                        break;
                    case 'medium':
                        renderer.setPixelRatio(1);
                        renderer.shadowMap.enabled = true;
                        break;
                    case 'high':
                        renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
                        renderer.shadowMap.enabled = true;
                        break;
                    case 'ultra':
                        renderer.setPixelRatio(window.devicePixelRatio);
                        renderer.shadowMap.enabled = true;
                        break;
                }
            }

            function resetCamera() {
                const startPos = { x: camera.position.x, y: camera.position.y, z: camera.position.z };
                const targetPos = { x: 0, y: 5, z: 10 };
                const startTime = performance.now();
                const duration = 1000;

                function animateReset() {
                    const elapsed = performance.now() - startTime;
                    const progress = Math.min(elapsed / duration, 1);
                    const easeProgress = 1 - Math.pow(1 - progress, 3);

                    camera.position.x = startPos.x + (targetPos.x - startPos.x) * easeProgress;
                    camera.position.y = startPos.y + (targetPos.y - startPos.y) * easeProgress;
                    camera.position.z = startPos.z + (targetPos.z - startPos.z) * easeProgress;

                    camera.lookAt(0, 0, 0);

                    if (progress < 1) {
                        requestAnimationFrame(animateReset);
                    } else {
                        controls.reset();
                    }
                }

                animateReset();
            }

            function sendDataToStreamlit(data) {
                // Send data back to Streamlit parent window
                if (window.parent) {
                    window.parent.postMessage(data, '*');
                }
            }

            function animate() {
                if (performanceStats) performanceStats.begin();

                frameCount++;

                // Update controls
                controls.update();

                // Update animations
                const delta = clock.getDelta();
                if (animationMixer) {
                    animationMixer.update(delta);
                }

                // Render scene
                renderer.render(scene, camera);

                if (performanceStats) performanceStats.end();

                if (renderer.xr && renderer.xr.isPresenting) {
                    // VR mode - use XR animation loop
                } else {
                    requestAnimationFrame(animate);
                }
            }

            // Initialize when DOM is loaded
            if (document.readyState === 'loading') {
                document.addEventListener('DOMContentLoaded', init);
            } else {
                init();
            }
        """

class PerformanceMonitor:
    """Monitor and optimize Three.js performance"""

    def __init__(self):
        self.metrics_history = []
        self.alert_thresholds = {
            "fps": 50,
            "frame_time": 20,
            "memory_usage": 100,
            "draw_calls": 1000
        }

    def update_metrics(self, metrics: PerformanceMetrics):
        """Update performance metrics and check for alerts"""
        self.metrics_history.append({
            "timestamp": time.time(),
            **asdict(metrics)
        })

        # Keep only last 100 measurements
        if len(self.metrics_history) > 100:
            self.metrics_history.pop(0)

        self._check_performance_alerts(metrics)

    def _check_performance_alerts(self, metrics: PerformanceMetrics):
        """Check for performance issues and display alerts"""
        alerts = []

        if metrics.fps < self.alert_thresholds["fps"]:
            alerts.append(f"⚠️ Low FPS: {metrics.fps:.1f}")

        if metrics.frame_time > self.alert_thresholds["frame_time"]:
            alerts.append(f"⚠️ High frame time: {metrics.frame_time:.1f}ms")

        if metrics.memory_usage > self.alert_thresholds["memory_usage"]:
            alerts.append(f"⚠️ High memory usage: {metrics.memory_usage:.1f}MB")

        if metrics.draw_calls > self.alert_thresholds["draw_calls"]:
            alerts.append(f"⚠️ High draw calls: {metrics.draw_calls}")

        if alerts:
            st.warning(" | ".join(alerts))

    def render_performance_dashboard(self):
        """Render performance metrics dashboard"""
        if not self.metrics_history:
            st.info("No performance data available yet")
            return

        latest = self.metrics_history[-1]

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            fps = latest.get("fps", 0)
            delta_fps = fps - 60
            st.metric("FPS", f"{fps:.1f}", delta=f"{delta_fps:+.1f}")

        with col2:
            frame_time = latest.get("frame_time", 0)
            st.metric("Frame Time", f"{frame_time:.1f}ms")

        with col3:
            memory = latest.get("memory_usage", 0)
            st.metric("Memory", f"{memory:.1f}MB")

        with col4:
            draw_calls = latest.get("draw_calls", 0)
            st.metric("Draw Calls", f"{draw_calls}")

        # Performance chart
        if len(self.metrics_history) > 1:
            import pandas as pd
            import plotly.graph_objects as go

            df = pd.DataFrame(self.metrics_history)
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='s')

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=df['timestamp'],
                y=df['fps'],
                mode='lines',
                name='FPS',
                line=dict(color='#00ff00')
            ))

            fig.update_layout(
                title="Performance Over Time",
                xaxis_title="Time",
                yaxis_title="FPS",
                height=300,
                showlegend=True
            )

            st.plotly_chart(fig, use_container_width=True)
