"""
Test suite for Ultra-Native GSAP Environment
Validates comprehensive JavaScript integration and advanced GSAP features
"""

import re
from components.gsap_ultra_native import UltraNativeGSAPRenderer

class TestUltraNativeGSAP:
    """Test suite for ultra-native GSAP renderer"""
    
    def setup_method(self):
        """Setup test environment"""
        self.renderer = UltraNativeGSAPRenderer()
    
    def test_renderer_initialization(self):
        """Test renderer initialization"""
        assert self.renderer is not None
        assert hasattr(self.renderer, 'animation_queue')
        assert hasattr(self.renderer, 'particle_systems')
        assert hasattr(self.renderer, 'physics_engine')
        assert hasattr(self.renderer, 'data_visualizations')
    
    def test_cdn_links_generation(self):
        """Test CDN links include all required libraries"""
        cdn_links = self.renderer.get_ultra_native_cdn_links()
        
        # Check for core GSAP plugins
        required_gsap = [
            'gsap.min.js',
            'ScrollTrigger.min.js',
            'MorphSVGPlugin.min.js',
            'DrawSVGPlugin.min.js',
            'PixiPlugin.min.js',
            'Physics2DPlugin.min.js',
            'Draggable.min.js'
        ]
        
        for plugin in required_gsap:
            assert plugin in cdn_links, f"Missing GSAP plugin: {plugin}"
        
        # Check for additional JavaScript libraries
        required_libs = [
            'howler.min.js',
            'tone',
            'three.min.js',
            'pixi.min.js',
            'matter.min.js',
            'd3.min.js',
            'lodash.min.js',
            'stats.min.js'
        ]
        
        for lib in required_libs:
            assert lib in cdn_links, f"Missing JavaScript library: {lib}"
    
    def test_html_structure_generation(self):
        """Test HTML structure contains all required elements"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for essential HTML elements
        required_elements = [
            'ultra-tavern-container',
            'pixi-canvas',
            'three-canvas',
            'morph-svg',
            'performance-monitor',
            'audio-controls',
            'animation-controls',
            'interactive-zone',
            'data-viz-container'
        ]
        
        for element in required_elements:
            assert element in html, f"Missing HTML element: {element}"
    
    def test_css_styling(self):
        """Test CSS includes advanced styling features"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for advanced CSS features
        css_features = [
            'transform-style: preserve-3d',
            'will-change: transform',
            'perspective: 1000px',
            'backdrop-filter',
            'radial-gradient',
            'linear-gradient',
            'box-shadow',
            'transition: all'
        ]
        
        for feature in css_features:
            assert feature in html, f"Missing CSS feature: {feature}"
    
    def test_javascript_classes(self):
        """Test JavaScript contains all required classes"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for JavaScript classes
        js_classes = [
            'UltraParticleSystem',
            'UltraMorphSystem',
            'UltraAudioSystem',
            'UltraPhysicsSystem',
            'UltraDataViz',
            'UltraInteractionSystem'
        ]
        
        for js_class in js_classes:
            assert js_class in html, f"Missing JavaScript class: {js_class}"
    
    def test_gsap_configuration(self):
        """Test GSAP configuration and plugins"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for GSAP configuration
        gsap_config = [
            'gsap.registerPlugin',
            'force3D: true',
            'gsap.ticker.fps(60)',
            'CustomEase.create',
            'ultraBounce',
            'ultraElastic',
            'ultraMagic',
            'ultraPhysics'
        ]
        
        for config in gsap_config:
            assert config in html, f"Missing GSAP configuration: {config}"
    
    def test_particle_system_features(self):
        """Test particle system functionality"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for particle system features
        particle_features = [
            'createParticle',
            'animateParticle',
            'getParticleStyles',
            'burst',
            'spark-particle',
            'magic-particle',
            'fire-particle',
            'ice-particle'
        ]
        
        for feature in particle_features:
            assert feature in html, f"Missing particle feature: {feature}"
    
    def test_morph_system_features(self):
        """Test MorphSVG system functionality"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for morph system features
        morph_features = [
            'createMorphTarget',
            'morphBetween',
            'morphSVG:',
            'createDynamicShape',
            'pointsToPath',
            'onMorphUpdate'
        ]
        
        for feature in morph_features:
            assert feature in html, f"Missing morph feature: {feature}"
    
    def test_audio_system_features(self):
        """Test audio system functionality"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for audio system features
        audio_features = [
            'Tone.start()',
            'Tone.Synth',
            'playTone',
            'playSound',
            'playSequence',
            'setMasterVolume',
            'triggerAttackRelease'
        ]
        
        for feature in audio_features:
            assert feature in html, f"Missing audio feature: {feature}"
    
    def test_physics_system_features(self):
        """Test physics system functionality"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for physics system features
        physics_features = [
            'Matter.Engine.create',
            'Matter.Bodies.rectangle',
            'Matter.Bodies.circle',
            'createBody',
            'createCircle',
            'applyForce',
            'syncWithGSAP'
        ]
        
        for feature in physics_features:
            assert feature in html, f"Missing physics feature: {feature}"
    
    def test_interaction_system_features(self):
        """Test interaction system functionality"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for interaction system features
        interaction_features = [
            'makeDraggable',
            'createDropZone',
            'checkDropZoneCollisions',
            'handleDrop',
            'isColliding',
            'logInteraction',
            'Draggable.create'
        ]
        
        for feature in interaction_features:
            assert feature in html, f"Missing interaction feature: {feature}"
    
    def test_data_visualization_features(self):
        """Test data visualization functionality"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for data visualization features
        dataviz_features = [
            'd3.select',
            'createFPSChart',
            'updateFPSChart',
            'createInteractionGraph',
            'd3.scaleLinear',
            'd3.line',
            'curveMonotoneX'
        ]
        
        for feature in dataviz_features:
            assert feature in html, f"Missing data viz feature: {feature}"
    
    def test_scroll_trigger_features(self):
        """Test ScrollTrigger functionality"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for ScrollTrigger features
        scroll_features = [
            'scrollTrigger:',
            'initScrollTriggerAnimations',
            'toggleActions:',
            'scrub: true',
            'onEnter:',
            'start: "top'
        ]
        
        for feature in scroll_features:
            assert feature in html, f"Missing ScrollTrigger feature: {feature}"
    
    def test_performance_optimization(self):
        """Test performance optimization features"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for performance optimizations
        perf_features = [
            'force3D: true',
            'transformPerspective: 1000',
            'backfaceVisibility: "hidden"',
            'gsap.ticker.fps(60)',
            'lagSmoothing',
            'autoSleep: 60',
            'requestAnimationFrame'
        ]
        
        for feature in perf_features:
            assert feature in html, f"Missing performance feature: {feature}"
    
    def test_initialization_system(self):
        """Test initialization system"""
        html = self.renderer.get_ultra_native_html("Test Tavern")
        
        # Check for initialization features
        init_features = [
            'initializeUltraNativeEnvironment',
            'createInitialContent',
            'setupControls',
            'startAnimationLoop',
            'DOMContentLoaded'
        ]
        
        for feature in init_features:
            assert feature in html, f"Missing initialization feature: {feature}"

def test_ultra_native_integration():
    """Integration test for ultra-native GSAP environment"""
    print("🚀 Testing Ultra-Native GSAP Integration...")
    
    renderer = UltraNativeGSAPRenderer()
    html = renderer.get_ultra_native_html("Integration Test Tavern")
    
    # Validate HTML structure
    assert '<!DOCTYPE html>' in html
    assert '<html lang="en">' in html
    assert '</html>' in html
    
    # Validate comprehensive JavaScript environment
    js_libraries = [
        'gsap', 'ScrollTrigger', 'MorphSVGPlugin', 'DrawSVGPlugin',
        'PixiPlugin', 'Physics2DPlugin', 'Draggable', 'howler',
        'tone', 'three', 'pixi', 'matter', 'd3', 'lodash', 'stats'
    ]
    
    for lib in js_libraries:
        assert lib.lower() in html.lower(), f"Missing library: {lib}"
    
    # Validate advanced features
    advanced_features = [
        'particlesystem', 'morph', 'audio', 'physics',
        'interaction', 'dataviz', 'scrolltrigger'
    ]

    for feature in advanced_features:
        assert feature.lower() in html.lower(), f"Missing feature: {feature}"
    
    print("✅ Ultra-Native GSAP Integration Test Passed!")
    print(f"📊 HTML Size: {len(html)} characters")
    print(f"🎯 JavaScript Libraries: {len(js_libraries)} integrated")
    print(f"⚡ Advanced Features: {len(advanced_features)} implemented")

if __name__ == "__main__":
    # Run integration test
    test_ultra_native_integration()
    
    # Run pytest if available
    try:
        import pytest
        pytest.main([__file__, "-v"])
    except ImportError:
        print("pytest not available, running basic tests...")
        
        # Run basic tests manually
        test_suite = TestUltraNativeGSAP()
        test_suite.setup_method()
        
        test_methods = [method for method in dir(test_suite) if method.startswith('test_')]
        
        for test_method in test_methods:
            try:
                getattr(test_suite, test_method)()
                print(f"✅ {test_method}")
            except Exception as e:
                print(f"❌ {test_method}: {e}")
        
        print(f"\n🎯 Completed {len(test_methods)} tests")
