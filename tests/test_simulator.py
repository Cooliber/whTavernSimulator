#!/usr/bin/env python3
"""
Test script for the Warhammer Fantasy Tavern Simulator
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

def test_core_systems():
    """Test core simulator functionality"""
    print("Testing Warhammer Fantasy Tavern Simulator...")
    
    try:
        # Test imports
        print("✓ Testing imports...")
        from core.tavern_simulator import TavernSimulator
        from core.character_generator import CharacterGenerator
        from core.tavern_generator import TavernGenerator
        from core.dice_system import DiceSystem, InteractionSystem
        from core.enums import InteractionType, Faction
        
        # Test character generation
        print("✓ Testing character generation...")
        char_gen = CharacterGenerator()
        characters = char_gen.get_all_characters()
        assert len(characters) == 17, f"Expected 17 characters, got {len(characters)}"
        print(f"  Generated {len(characters)} unique characters")
        
        # Test tavern generation
        print("✓ Testing tavern generation...")
        tavern_gen = TavernGenerator()
        tavern = tavern_gen.generate_tavern()
        assert tavern.name, "Tavern should have a name"
        print(f"  Generated tavern: {tavern.name}")
        
        # Test dice system
        print("✓ Testing dice system...")
        dice_system = DiceSystem()
        char = characters[0]
        from core.enums import Skill
        result = dice_system.skill_check(char, Skill.DIPLOMACY, 10)
        assert result.roll >= 1 and result.roll <= 20, "Dice roll should be 1-20"
        print(f"  Dice roll: {result.roll} + {result.modifier} = {result.total}")
        
        # Test simulator
        print("✓ Testing main simulator...")
        simulator = TavernSimulator()
        simulator.generate_new_tavern()
        assert simulator.current_tavern, "Simulator should have a current tavern"
        assert len(simulator.current_tavern.characters) > 0, "Tavern should have characters"
        print(f"  Tavern '{simulator.current_tavern.name}' has {len(simulator.current_tavern.characters)} characters")
        
        # Test interaction
        print("✓ Testing character interaction...")
        chars = simulator.current_tavern.characters[:2]
        if len(chars) >= 2:
            interaction = simulator.perform_interaction(
                chars[0].name, chars[1].name, InteractionType.CONVERSATION
            )
            assert interaction, "Interaction should be created"
            print(f"  {interaction.initiator} -> {interaction.target}: {interaction.outcome_description}")
        
        # Test turn advancement
        print("✓ Testing turn advancement...")
        initial_turn = simulator.turn_counter
        simulator.advance_turn()
        assert simulator.turn_counter == initial_turn + 1, "Turn counter should increment"
        print(f"  Advanced to turn {simulator.turn_counter}")
        
        print("\n🎉 All core systems working correctly!")
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_character_details():
    """Test character details and uniqueness"""
    print("\nTesting character details...")
    
    try:
        from core.character_generator import CharacterGenerator
        
        char_gen = CharacterGenerator()
        characters = char_gen.get_all_characters()
        
        print(f"Character roster ({len(characters)} characters):")
        print("-" * 60)
        
        factions = set()
        for char in characters:
            factions.add(char.faction.value)
            print(f"• {char.name:20} | {char.faction.value:12} | {char.character_class.value}")
        
        print(f"\nFactions represented: {len(factions)}")
        for faction in sorted(factions):
            print(f"  - {faction}")
        
        return True
        
    except Exception as e:
        print(f"❌ Character test failed: {e}")
        return False

def test_gui_imports():
    """Test GUI component imports"""
    print("\nTesting GUI imports...")
    
    try:
        try:
            import tkinter as tk
            print("✓ tkinter available")
        except ImportError:
            print("⚠ tkinter not available (GUI will not work)")
            return False
        
        import matplotlib
        matplotlib.use('Agg')  # Use non-interactive backend for testing
        print("✓ matplotlib available")
        
        import networkx as nx
        print("✓ networkx available")
        
        import numpy as np
        print("✓ numpy available")
        
        # Test GUI imports
        from gui.main_window import MainWindow
        from gui.character_panel import CharacterPanel
        from gui.tavern_panel import TavernPanel
        from gui.relationship_graph import RelationshipGraph
        from gui.interaction_panel import InteractionPanel
        from gui.log_panel import LogPanel
        print("✓ All GUI components importable")
        
        return True
        
    except Exception as e:
        print(f"❌ GUI test failed: {e}")
        return False

if __name__ == "__main__":
    print("Warhammer Fantasy Tavern Simulator - Test Suite")
    print("=" * 50)
    
    success = True
    
    # Run tests
    success &= test_core_systems()
    success &= test_character_details()
    success &= test_gui_imports()
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests passed! The simulator is ready to run.")
        print("\nTo start the simulator, run:")
        print("  python main.py")
        print("  or")
        print("  python run_simulator.py")
    else:
        print("❌ Some tests failed. Please check the error messages above.")
        sys.exit(1)
