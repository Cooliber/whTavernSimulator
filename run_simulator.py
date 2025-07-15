#!/usr/bin/env python3
"""
Simple launcher script for the Warhammer Fantasy Tavern Simulator
"""

import sys
import os

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

try:
    from main import main
    main()
except ImportError as e:
    print(f"Import error: {e}")
    print("Please make sure all required packages are installed:")
    print("pip install matplotlib networkx numpy")
    sys.exit(1)
except Exception as e:
    print(f"Error starting simulator: {e}")
    sys.exit(1)
