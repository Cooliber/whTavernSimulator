#!/usr/bin/env python3
"""
Test Cerebras specialized service for fast dialogues, rumors, and real-time responses
"""

import os
import sys
import time
from dotenv import load_dotenv

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from services.cerebras_service import CerebrasService, CerebrasRequest, ResponseType

# Load environment variables
load_dotenv()

def test_quick_dialogue():
    """Test quick dialogue generation"""
    print("💬 Testing Quick Dialogue Generation")
    print("=" * 45)
    
    service = CerebrasService()
    
    # Test different dialogue scenarios
    scenarios = [
        {
            "character": "Karczmarz",
            "context": "A suspicious patron asks about room availability",
            "personality": "Cautious but professional tavern keeper",
            "urgency": 7
        },
        {
            "character": "Skrytobójca", 
            "context": "Someone asks about the hooded figures in the corner",
            "personality": "Silent observer who reveals little",
            "urgency": 9
        },
        {
            "character": "Wiedźma",
            "context": "A patron seeks advice about strange dreams",
            "personality": "Mystical oracle with cryptic wisdom",
            "urgency": 5
        }
    ]
    
    for i, scenario in enumerate(scenarios, 1):
        print(f"📋 Scenario {i}: {scenario['character']}")
        
        request = CerebrasRequest(
            response_type=ResponseType.QUICK_DIALOGUE,
            context=scenario["context"],
            character_name=scenario["character"],
            character_personality=scenario["personality"],
            urgency_level=scenario["urgency"],
            max_words=30
        )
        
        start_time = time.time()
        response = service.generate_quick_dialogue(request)
        response_time = time.time() - start_time
        
        print(f"  Context: {scenario['context']}")
        print(f"  Response: {response}")
        print(f"  ⚡ Speed: {response_time:.3f}s")
        print()
    
    return service

def test_rumor_generation():
    """Test rumor generation"""
    print("🗣️ Testing Rumor Generation")
    print("=" * 35)
    
    service = CerebrasService()
    
    rumor_contexts = [
        "Strange lights seen in the forest last night",
        "A merchant caravan is three days overdue",
        "The local lord hasn't been seen in weeks",
        "Wolves have been acting strangely aggressive"
    ]
    
    characters = ["Zwiadowca", "Karczmarz", "Wiedźma"]
    
    for context in rumor_contexts:
        character = characters[rumor_contexts.index(context) % len(characters)]
        
        request = CerebrasRequest(
            response_type=ResponseType.RUMOR_GENERATION,
            context=context,
            character_name=character,
            max_words=25,
            urgency_level=6
        )
        
        start_time = time.time()
        rumor = service.generate_rumor(request)
        response_time = time.time() - start_time
        
        print(f"📰 {character}: {rumor}")
        print(f"   ⚡ Generated in: {response_time:.3f}s")
        print()
    
    return service

def test_real_time_reactions():
    """Test real-time reaction generation"""
    print("⚡ Testing Real-Time Reactions")
    print("=" * 35)
    
    service = CerebrasService()
    
    urgent_events = [
        "A fight breaks out between two patrons",
        "Someone screams 'FIRE!' in the tavern",
        "Armed guards burst through the door",
        "A mysterious figure collapses at the bar"
    ]
    
    characters = ["Karczmarz", "Skrytobójca", "Czempion", "Zwiadowca"]
    
    for event in urgent_events:
        character = characters[urgent_events.index(event)]
        
        request = CerebrasRequest(
            response_type=ResponseType.REAL_TIME_REACTION,
            context=event,
            character_name=character,
            max_words=15,
            urgency_level=10,
            emotional_state="alarmed"
        )
        
        start_time = time.time()
        reaction = service.generate_real_time_reaction(request)
        response_time = time.time() - start_time
        
        print(f"🚨 Event: {event}")
        print(f"   {character}: {reaction}")
        print(f"   ⚡ Reaction time: {response_time:.3f}s")
        print()
    
    return service

def test_tavern_banter():
    """Test tavern banter generation"""
    print("🍺 Testing Tavern Banter")
    print("=" * 30)
    
    service = CerebrasService()
    
    banter_topics = [
        "the weather has been unusually cold",
        "rumors of bandits on the trade roads",
        "the quality of this year's ale harvest"
    ]
    
    participants = ["Karczmarz", "Zwiadowca", "Wiedźma"]
    
    for topic in banter_topics:
        print(f"💭 Topic: {topic}")
        
        start_time = time.time()
        banter = service.generate_tavern_banter(participants, topic)
        response_time = time.time() - start_time
        
        for line in banter:
            print(f"   {line}")
        
        print(f"   ⚡ Generated in: {response_time:.3f}s")
        print()
    
    return service

def test_threat_assessment():
    """Test quick threat assessment"""
    print("🛡️ Testing Threat Assessment")
    print("=" * 35)
    
    service = CerebrasService()
    
    threats = [
        "Hooded figures whispering in a corner, one keeps checking the exits",
        "Drunk patron becoming increasingly aggressive and violent",
        "Stranger asking too many questions about local defenses",
        "Unusual number of armed travelers arriving simultaneously"
    ]
    
    assessors = ["Skrytobójca", "Zwiadowca", "Karczmarz", "Czempion"]
    
    for threat in threats:
        assessor = assessors[threats.index(threat)]
        
        print(f"⚠️ Threat: {threat}")
        
        start_time = time.time()
        assessment = service.assess_threat_quickly(threat, assessor)
        response_time = time.time() - start_time
        
        print(f"   Assessor: {assessment['assessor']}")
        print(f"   Assessment: {assessment['assessment']}")
        print(f"   Threat Level: {assessment['threat_level']}/10")
        print(f"   ⚡ Assessment time: {response_time:.3f}s")
        print()
    
    return service

def test_performance_benchmarks():
    """Test performance benchmarks"""
    print("📊 Performance Benchmarks")
    print("=" * 30)
    
    service = CerebrasService()
    
    # Rapid-fire test
    print("🔥 Rapid-fire dialogue test (10 requests):")
    
    request = CerebrasRequest(
        response_type=ResponseType.QUICK_DIALOGUE,
        context="A patron orders ale",
        character_name="Karczmarz",
        max_words=10,
        urgency_level=8
    )
    
    times = []
    for i in range(10):
        start_time = time.time()
        response = service.generate_quick_dialogue(request)
        response_time = time.time() - start_time
        times.append(response_time)
        print(f"   Request {i+1}: {response_time:.3f}s")
    
    avg_time = sum(times) / len(times)
    min_time = min(times)
    max_time = max(times)
    
    print(f"\n📈 Performance Summary:")
    print(f"   Average: {avg_time:.3f}s")
    print(f"   Fastest: {min_time:.3f}s")
    print(f"   Slowest: {max_time:.3f}s")
    
    # Show service stats
    stats = service.get_performance_stats()
    print(f"\n📊 Service Statistics:")
    print(f"   Cache size: {stats['cache_size']} entries")
    print(f"   LLM stats: {stats['llm_stats']}")
    
    return service

def main():
    """Main test function"""
    print("🧠 Cerebras Specialized Service Test Suite")
    print("=" * 50)
    
    # Test all features
    service = test_quick_dialogue()
    service = test_rumor_generation()
    service = test_real_time_reactions()
    service = test_tavern_banter()
    service = test_threat_assessment()
    service = test_performance_benchmarks()
    
    print("🎉 Cerebras service testing complete!")
    print("\n🚀 Key Features Demonstrated:")
    print("   ✅ Quick dialogue generation")
    print("   ✅ Rumor creation")
    print("   ✅ Real-time reactions")
    print("   ✅ Tavern banter")
    print("   ✅ Threat assessment")
    print("   ✅ Performance optimization")

if __name__ == "__main__":
    main()
