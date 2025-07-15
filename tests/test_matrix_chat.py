#!/usr/bin/env python3
"""
Test Matrix Chat Interface
Comprehensive testing of the new Matrix-style chat interface
"""

import unittest
import time
from datetime import datetime
from components.matrix_chat_interface import MatrixChatInterface, ChatMessage, ConversationFlow

class TestMatrixChatInterface(unittest.TestCase):
    """Test cases for Matrix Chat Interface"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.chat_interface = MatrixChatInterface()
        
        # Sample test message
        self.test_message = ChatMessage(
            id="test_msg_1",
            sender="Karczmarz",
            receiver="Skrytobójca",
            content="Witaj w mojej karczmie, przyjacielu!",
            message_type="whisper",
            emotion="happy",
            priority=5,
            timestamp=datetime.now(),
            effects=["glow", "typewriter"],
            color_theme="gold",
            duration=4.0
        )
    
    def test_chat_interface_initialization(self):
        """Test chat interface initialization"""
        self.assertIsNotNone(self.chat_interface)
        self.assertEqual(self.chat_interface.component_id, "matrix_chat_interface")
        
        # Check if session state is initialized
        import streamlit as st
        self.assertIn('matrix_chat_state', st.session_state)
        
        chat_state = st.session_state.matrix_chat_state
        self.assertIn('messages', chat_state)
        self.assertIn('conversations', chat_state)
        self.assertIn('chat_settings', chat_state)
        self.assertIn('performance', chat_state)
    
    def test_message_creation(self):
        """Test ChatMessage creation"""
        message = self.test_message
        
        self.assertEqual(message.id, "test_msg_1")
        self.assertEqual(message.sender, "Karczmarz")
        self.assertEqual(message.receiver, "Skrytobójca")
        self.assertEqual(message.message_type, "whisper")
        self.assertEqual(message.emotion, "happy")
        self.assertEqual(message.priority, 5)
        self.assertIn("glow", message.effects)
        self.assertIn("typewriter", message.effects)
    
    def test_add_message(self):
        """Test adding messages to chat"""
        initial_count = len(st.session_state.matrix_chat_state.get('messages', []))
        
        # Add message
        self.chat_interface.add_message(self.test_message)
        
        # Check if message was added
        messages = st.session_state.matrix_chat_state.get('messages', [])
        self.assertEqual(len(messages), initial_count + 1)
        
        # Check message content
        added_message = messages[-1]
        self.assertEqual(added_message['sender'], "Karczmarz")
        self.assertEqual(added_message['receiver'], "Skrytobójca")
        self.assertEqual(added_message['content'], "Witaj w mojej karczmie, przyjacielu!")
    
    def test_conversation_flow_tracking(self):
        """Test conversation flow tracking"""
        # Add multiple messages between same characters
        message1 = ChatMessage(
            id="conv_msg_1",
            sender="Karczmarz",
            receiver="Skrytobójca",
            content="Pierwsza wiadomość",
            message_type="whisper",
            emotion="calm",
            priority=3,
            timestamp=datetime.now(),
            effects=["fade"],
            color_theme="blue",
            duration=3.0
        )
        
        message2 = ChatMessage(
            id="conv_msg_2",
            sender="Skrytobójca",
            receiver="Karczmarz",
            content="Odpowiedź",
            message_type="whisper",
            emotion="mysterious",
            priority=4,
            timestamp=datetime.now(),
            effects=["matrix"],
            color_theme="purple",
            duration=3.5
        )
        
        self.chat_interface.add_message(message1)
        self.chat_interface.add_message(message2)
        
        # Check active conversations
        active_convs = self.chat_interface.get_active_conversations()
        self.assertGreater(len(active_convs), 0)
        
        # Find conversation between Karczmarz and Skrytobójca
        conv_found = False
        for conv in active_convs:
            if "Karczmarz" in conv['participants'] and "Skrytobójca" in conv['participants']:
                conv_found = True
                self.assertGreaterEqual(conv['message_count'], 2)
                break
        
        self.assertTrue(conv_found, "Conversation between Karczmarz and Skrytobójca not found")
    
    def test_chat_settings(self):
        """Test chat settings functionality"""
        # Test setting configuration
        self.chat_interface.set_chat_settings(
            matrix_mode=False,
            auto_scroll=False,
            sound_enabled=False,
            effect_intensity=0.5
        )
        
        settings = st.session_state.matrix_chat_state.get('chat_settings', {})
        self.assertEqual(settings.get('matrix_mode'), False)
        self.assertEqual(settings.get('auto_scroll'), False)
        self.assertEqual(settings.get('sound_enabled'), False)
        self.assertEqual(settings.get('effect_intensity'), 0.5)
    
    def test_clear_chat(self):
        """Test clearing chat functionality"""
        # Add some messages first
        self.chat_interface.add_message(self.test_message)
        
        # Verify messages exist
        messages_before = st.session_state.matrix_chat_state.get('messages', [])
        self.assertGreater(len(messages_before), 0)
        
        # Clear chat
        self.chat_interface.clear_chat()
        
        # Verify messages are cleared
        messages_after = st.session_state.matrix_chat_state.get('messages', [])
        conversations_after = st.session_state.matrix_chat_state.get('conversations', {})
        
        self.assertEqual(len(messages_after), 0)
        self.assertEqual(len(conversations_after), 0)
    
    def test_message_types_and_effects(self):
        """Test different message types and effects"""
        message_types = [
            ("whisper", ["matrix", "fade"], "mysterious"),
            ("shout", ["glow", "shake"], "urgent"),
            ("thought", ["typewriter"], "calm"),
            ("action", ["glow"], "happy"),
            ("magic", ["matrix", "glow"], "mysterious")
        ]
        
        for i, (msg_type, effects, emotion) in enumerate(message_types):
            message = ChatMessage(
                id=f"type_test_{i}",
                sender="TestSender",
                receiver="TestReceiver",
                content=f"Test message type: {msg_type}",
                message_type=msg_type,
                emotion=emotion,
                priority=5,
                timestamp=datetime.now(),
                effects=effects,
                color_theme="gold",
                duration=3.0
            )
            
            self.chat_interface.add_message(message)
            
            # Verify message was added with correct properties
            messages = st.session_state.matrix_chat_state.get('messages', [])
            added_message = messages[-1]
            
            self.assertEqual(added_message['message_type'], msg_type)
            self.assertEqual(added_message['emotion'], emotion)
            self.assertEqual(added_message['effects'], effects)
    
    def test_html_generation(self):
        """Test HTML generation for Matrix chat"""
        # Add some test messages
        self.chat_interface.add_message(self.test_message)
        
        messages = st.session_state.matrix_chat_state.get('messages', [])
        settings = st.session_state.matrix_chat_state.get('chat_settings', {})
        
        # Generate HTML
        html_content = self.chat_interface._generate_matrix_chat_html(messages, settings)
        
        # Check if HTML contains required elements
        self.assertIn('matrix-chat-container', html_content)
        self.assertIn('matrix-rain', html_content)
        self.assertIn('chat-interface', html_content)
        self.assertIn('message-container', html_content)
        self.assertIn('floating-conversations', html_content)
        self.assertIn('performance-monitor', html_content)
        
        # Check if GSAP and other libraries are included
        self.assertIn('gsap.min.js', html_content)
        self.assertIn('particles.min.js', html_content)
        self.assertIn('howler.min.js', html_content)
        
        # Check if embedded data is present
        self.assertIn('MESSAGES_DATA', html_content)
        self.assertIn('CHAT_SETTINGS', html_content)
    
    def test_css_generation(self):
        """Test CSS generation for Matrix chat"""
        css_content = self.chat_interface._get_matrix_chat_css()
        
        # Check if CSS contains required classes
        required_classes = [
            'matrix-chat-container',
            'chat-message',
            'message-sender',
            'message-receiver',
            'message-broadcast',
            'floating-bubble',
            'emotion-angry',
            'emotion-happy',
            'emotion-mysterious',
            'message-whisper',
            'message-shout',
            'message-magic'
        ]
        
        for css_class in required_classes:
            self.assertIn(css_class, css_content)
        
        # Check if animations are defined
        animations = [
            'matrix-glow',
            'message-appear',
            'shout-pulse',
            'magic-shimmer',
            'bubble-float'
        ]
        
        for animation in animations:
            self.assertIn(f'@keyframes {animation}', css_content)
    
    def test_performance_metrics(self):
        """Test performance metrics tracking"""
        # Add multiple messages to test performance
        for i in range(10):
            message = ChatMessage(
                id=f"perf_test_{i}",
                sender=f"Agent{i % 3}",
                receiver=f"Agent{(i + 1) % 3}",
                content=f"Performance test message {i}",
                message_type="whisper",
                emotion="calm",
                priority=i % 10 + 1,
                timestamp=datetime.now(),
                effects=["fade"],
                color_theme="blue",
                duration=2.0
            )
            self.chat_interface.add_message(message)
        
        # Check if performance metrics are tracked
        performance = st.session_state.matrix_chat_state.get('performance', {})
        self.assertIn('fps', performance)
        self.assertIn('particles', performance)
        self.assertIn('effects_quality', performance)
        
        # Check message count
        messages = st.session_state.matrix_chat_state.get('messages', [])
        self.assertGreaterEqual(len(messages), 10)

class MockSessionState:
    """Mock Streamlit session state for testing"""
    def __init__(self):
        self.matrix_chat_state = {
            'messages': [],
            'conversations': {},
            'active_effects': [],
            'chat_settings': {
                'matrix_mode': True,
                'auto_scroll': True,
                'sound_enabled': True,
                'effect_intensity': 0.8,
                'max_messages': 100
            },
            'performance': {
                'fps': 60,
                'particles': 500,
                'effects_quality': 'high'
            }
        }

    def get(self, key, default=None):
        return getattr(self, key, default)

def run_matrix_chat_tests():
    """Run all Matrix Chat tests"""
    print("🔋 Running Matrix Chat Interface Tests...")

    # Mock streamlit session state
    import streamlit as st
    if not hasattr(st, 'session_state'):
        st.session_state = MockSessionState()
    elif 'matrix_chat_state' not in st.session_state:
        st.session_state.matrix_chat_state = {
            'messages': [],
            'conversations': {},
            'active_effects': [],
            'chat_settings': {
                'matrix_mode': True,
                'auto_scroll': True,
                'sound_enabled': True,
                'effect_intensity': 0.8,
                'max_messages': 100
            },
            'performance': {
                'fps': 60,
                'particles': 500,
                'effects_quality': 'high'
            }
        }

    # Run tests
    unittest.main(argv=[''], exit=False, verbosity=2)

if __name__ == "__main__":
    run_matrix_chat_tests()
