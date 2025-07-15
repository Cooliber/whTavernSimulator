#!/usr/bin/env python3
"""
Warhammer Fantasy Tavern Simulator
A comprehensive tavern simulation set in the Warhammer Fantasy universe
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import sys
import os

# Add the current directory to the path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from core.tavern_simulator import TavernSimulator
    from gui.main_window import MainWindow
except ImportError:
    # Try relative imports if absolute imports fail
    from .core.tavern_simulator import TavernSimulator
    from .gui.main_window import MainWindow

def main():
    """Main entry point for the Warhammer Fantasy Tavern Simulator"""
    try:
        # Create the main tkinter root
        root = tk.Tk()
        root.title("Warhammer Fantasy Tavern Simulator")
        root.geometry("1200x800")
        root.minsize(800, 600)
        
        # Set the application icon (if available)
        try:
            root.iconbitmap("assets/tavern_icon.ico")
        except:
            pass  # Icon file not found, continue without it
        
        # Initialize the simulator
        simulator = TavernSimulator()
        
        # Create and start the main window
        app = MainWindow(root, simulator)
        
        # Start the main event loop
        root.mainloop()
        
    except Exception as e:
        messagebox.showerror("Error", f"Failed to start the application: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
