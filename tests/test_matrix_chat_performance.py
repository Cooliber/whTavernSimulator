#!/usr/bin/env python3
"""
Matrix Chat Performance Test Suite
Comprehensive performance testing for Matrix Chat Interface
"""

import time
import threading
import random
from datetime import datetime
from components.matrix_chat_interface import MatrixChatInterface, ChatMessage
from components.matrix_chat_integration import MatrixChatIntegration

class MatrixChatPerformanceTest:
    """
    Performance test suite for Matrix Chat Interface
    Tests various scenarios and measures performance metrics
    """
    
    def __init__(self):
        self.chat_interface = MatrixChatInterface()
        self.chat_integration = MatrixChatIntegration(self.chat_interface)
        self.test_results = {}
        
    def test_message_throughput(self, num_messages: int = 100) -> dict:
        """Test message processing throughput"""
        print(f"🚀 Testing message throughput with {num_messages} messages...")
        
        start_time = time.time()
        
        for i in range(num_messages):
            message = ChatMessage(
                id=f"perf_test_{i}",
                sender=f"Agent{i % 5}",
                receiver=f"Agent{(i + 1) % 5}",
                content=f"Performance test message {i}",
                message_type=random.choice(["whisper", "shout", "thought", "action", "magic"]),
                emotion=random.choice(["happy", "angry", "mysterious", "urgent", "calm"]),
                priority=random.randint(1, 10),
                timestamp=datetime.now(),
                effects=random.sample(["matrix", "glow", "shake", "typewriter", "fade"], 2),
                color_theme=random.choice(["gold", "red", "green", "blue", "purple"]),
                duration=random.uniform(2.0, 6.0)
            )
            
            self.chat_interface.add_message(message)
        
        end_time = time.time()
        duration = end_time - start_time
        throughput = num_messages / duration
        
        result = {
            "test": "message_throughput",
            "num_messages": num_messages,
            "duration": duration,
            "throughput": throughput,
            "messages_per_second": throughput,
            "status": "PASS" if throughput > 50 else "FAIL"
        }
        
        print(f"✅ Throughput test completed: {throughput:.2f} messages/second")
        return result
    
    def test_concurrent_messages(self, num_threads: int = 5, messages_per_thread: int = 20) -> dict:
        """Test concurrent message processing"""
        print(f"🔄 Testing concurrent messages with {num_threads} threads, {messages_per_thread} messages each...")
        
        def add_messages_thread(thread_id: int):
            for i in range(messages_per_thread):
                message = ChatMessage(
                    id=f"concurrent_{thread_id}_{i}",
                    sender=f"Thread{thread_id}",
                    receiver="All",
                    content=f"Concurrent message {i} from thread {thread_id}",
                    message_type="action",
                    emotion="calm",
                    priority=5,
                    timestamp=datetime.now(),
                    effects=["fade"],
                    color_theme="blue",
                    duration=3.0
                )
                self.chat_interface.add_message(message)
                time.sleep(0.01)  # Small delay to simulate real usage
        
        start_time = time.time()
        
        threads = []
        for thread_id in range(num_threads):
            thread = threading.Thread(target=add_messages_thread, args=(thread_id,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        end_time = time.time()
        duration = end_time - start_time
        total_messages = num_threads * messages_per_thread
        throughput = total_messages / duration
        
        result = {
            "test": "concurrent_messages",
            "num_threads": num_threads,
            "messages_per_thread": messages_per_thread,
            "total_messages": total_messages,
            "duration": duration,
            "throughput": throughput,
            "status": "PASS" if throughput > 30 else "FAIL"
        }
        
        print(f"✅ Concurrent test completed: {throughput:.2f} messages/second")
        return result
    
    def test_memory_usage(self, num_messages: int = 500) -> dict:
        """Test memory usage with large number of messages"""
        print(f"💾 Testing memory usage with {num_messages} messages...")
        
        import psutil
        import os
        
        process = psutil.Process(os.getpid())
        initial_memory = process.memory_info().rss / 1024 / 1024  # MB
        
        # Add messages
        for i in range(num_messages):
            message = ChatMessage(
                id=f"memory_test_{i}",
                sender=f"Agent{i % 10}",
                receiver="All",
                content=f"Memory test message {i} with some longer content to test memory usage patterns",
                message_type=random.choice(["whisper", "shout", "thought", "action", "magic"]),
                emotion=random.choice(["happy", "angry", "mysterious", "urgent", "calm"]),
                priority=random.randint(1, 10),
                timestamp=datetime.now(),
                effects=random.sample(["matrix", "glow", "shake", "typewriter", "fade"], 3),
                color_theme=random.choice(["gold", "red", "green", "blue", "purple"]),
                duration=random.uniform(2.0, 8.0)
            )
            self.chat_interface.add_message(message)
        
        final_memory = process.memory_info().rss / 1024 / 1024  # MB
        memory_increase = final_memory - initial_memory
        memory_per_message = memory_increase / num_messages
        
        result = {
            "test": "memory_usage",
            "num_messages": num_messages,
            "initial_memory_mb": initial_memory,
            "final_memory_mb": final_memory,
            "memory_increase_mb": memory_increase,
            "memory_per_message_kb": memory_per_message * 1024,
            "status": "PASS" if memory_per_message < 0.1 else "FAIL"  # Less than 100KB per message
        }
        
        print(f"✅ Memory test completed: {memory_per_message * 1024:.2f} KB per message")
        return result
    
    def test_conversation_flow_performance(self, num_conversations: int = 50) -> dict:
        """Test conversation flow tracking performance"""
        print(f"💬 Testing conversation flow with {num_conversations} conversations...")
        
        start_time = time.time()
        
        agents = ["Karczmarz", "Skrytobójca", "Wiedźma", "Czempion", "Zwiadowca"]
        
        for i in range(num_conversations):
            sender = random.choice(agents)
            receiver = random.choice([a for a in agents if a != sender])
            
            # Create conversation with multiple messages
            for j in range(random.randint(2, 8)):
                message = ChatMessage(
                    id=f"conv_{i}_{j}",
                    sender=sender if j % 2 == 0 else receiver,
                    receiver=receiver if j % 2 == 0 else sender,
                    content=f"Conversation {i}, message {j}",
                    message_type="whisper",
                    emotion="calm",
                    priority=random.randint(3, 7),
                    timestamp=datetime.now(),
                    effects=["fade"],
                    color_theme="blue",
                    duration=3.0
                )
                self.chat_interface.add_message(message)
        
        # Get active conversations
        active_conversations = self.chat_interface.get_active_conversations()
        
        end_time = time.time()
        duration = end_time - start_time
        
        result = {
            "test": "conversation_flow_performance",
            "num_conversations": num_conversations,
            "active_conversations": len(active_conversations),
            "duration": duration,
            "conversations_per_second": num_conversations / duration,
            "status": "PASS" if len(active_conversations) > 0 else "FAIL"
        }
        
        print(f"✅ Conversation flow test completed: {len(active_conversations)} active conversations")
        return result
    
    def test_integration_performance(self, num_simulations: int = 10) -> dict:
        """Test integration with agent system performance"""
        print(f"🤖 Testing integration performance with {num_simulations} simulations...")
        
        start_time = time.time()
        
        for i in range(num_simulations):
            self.chat_integration.simulate_agent_conversation(8)
            time.sleep(0.1)  # Small delay between simulations
        
        end_time = time.time()
        duration = end_time - start_time
        
        result = {
            "test": "integration_performance",
            "num_simulations": num_simulations,
            "duration": duration,
            "simulations_per_second": num_simulations / duration,
            "status": "PASS" if duration < num_simulations * 2 else "FAIL"  # Should be faster than 2s per simulation
        }
        
        print(f"✅ Integration test completed: {num_simulations / duration:.2f} simulations/second")
        return result
    
    def run_all_tests(self) -> dict:
        """Run all performance tests"""
        print("🔋 Starting Matrix Chat Performance Test Suite...")
        print("=" * 60)
        
        all_results = {}
        
        # Run individual tests
        all_results["throughput"] = self.test_message_throughput(100)
        all_results["concurrent"] = self.test_concurrent_messages(5, 20)
        all_results["memory"] = self.test_memory_usage(500)
        all_results["conversation_flow"] = self.test_conversation_flow_performance(50)
        all_results["integration"] = self.test_integration_performance(10)
        
        # Calculate overall score
        passed_tests = sum(1 for result in all_results.values() if result["status"] == "PASS")
        total_tests = len(all_results)
        overall_score = (passed_tests / total_tests) * 100
        
        # Performance rating on 2137 scale
        performance_rating = int((overall_score / 100) * 2137)
        
        summary = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": total_tests - passed_tests,
            "overall_score": overall_score,
            "performance_rating_2137": performance_rating,
            "status": "EXCELLENT" if overall_score >= 90 else "GOOD" if overall_score >= 70 else "NEEDS_IMPROVEMENT"
        }
        
        all_results["summary"] = summary
        
        print("=" * 60)
        print("📊 PERFORMANCE TEST RESULTS")
        print("=" * 60)
        
        for test_name, result in all_results.items():
            if test_name != "summary":
                status_emoji = "✅" if result["status"] == "PASS" else "❌"
                print(f"{status_emoji} {test_name.upper()}: {result['status']}")
        
        print("=" * 60)
        print(f"📈 OVERALL SCORE: {overall_score:.1f}%")
        print(f"🎯 PERFORMANCE RATING: {performance_rating}/2137")
        print(f"🏆 STATUS: {summary['status']}")
        print("=" * 60)
        
        return all_results

def run_performance_tests():
    """Run Matrix Chat performance tests"""
    try:
        # Mock streamlit session state for testing
        import streamlit as st
        if not hasattr(st, 'session_state'):
            class MockSessionState:
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
            st.session_state = MockSessionState()
        
        # Run tests
        test_suite = MatrixChatPerformanceTest()
        results = test_suite.run_all_tests()
        
        return results
        
    except Exception as e:
        print(f"❌ Error running performance tests: {e}")
        return None

if __name__ == "__main__":
    run_performance_tests()
