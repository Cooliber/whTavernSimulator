"""
Main window for the Warhammer Fantasy Tavern Simulator
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from typing import Optional
from ..core.tavern_simulator import TavernSimulator
from ..core.enums import InteractionType
from .character_panel import CharacterPanel
from .tavern_panel import TavernPanel
from .relationship_graph import RelationshipGraph
from .interaction_panel import InteractionPanel
from .log_panel import LogPanel

class MainWindow:
    """Main application window"""
    
    def __init__(self, root: tk.Tk, simulator: TavernSimulator):
        self.root = root
        self.simulator = simulator
        
        # Configure the main window
        self.setup_window()
        
        # Create the main interface
        self.create_widgets()
        
        # Start with a new tavern
        self.new_tavern()
        
        # Start the update loop
        self.update_display()
    
    def setup_window(self):
        """Configure the main window"""
        self.root.title("Warhammer Fantasy Tavern Simulator")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
        # Configure grid weights
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
    
    def create_widgets(self):
        """Create all GUI widgets"""
        # Create menu bar
        self.create_menu_bar()
        
        # Create main frame
        main_frame = ttk.Frame(self.root)
        main_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
        main_frame.grid_rowconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        
        # Create left panel (tavern info and controls)
        left_frame = ttk.Frame(main_frame, width=300)
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_propagate(False)
        
        # Create center panel (main content)
        center_frame = ttk.Frame(main_frame)
        center_frame.grid(row=0, column=1, sticky="nsew", padx=5)
        center_frame.grid_rowconfigure(0, weight=1)
        center_frame.grid_columnconfigure(0, weight=1)
        
        # Create right panel (character info)
        right_frame = ttk.Frame(main_frame, width=300)
        right_frame.grid(row=0, column=2, sticky="nsew", padx=(5, 0))
        right_frame.grid_rowconfigure(0, weight=1)
        right_frame.grid_propagate(False)
        
        # Initialize panels
        self.tavern_panel = TavernPanel(left_frame, self.simulator)
        self.character_panel = CharacterPanel(right_frame, self.simulator)
        
        # Create notebook for center content
        self.notebook = ttk.Notebook(center_frame)
        self.notebook.grid(row=0, column=0, sticky="nsew")
        
        # Create tabs
        self.create_tabs()
        
        # Create status bar
        self.create_status_bar()
    
    def create_menu_bar(self):
        """Create the menu bar"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="New Tavern", command=self.new_tavern, accelerator="Ctrl+N")
        file_menu.add_separator()
        file_menu.add_command(label="Save Session", command=self.save_session, accelerator="Ctrl+S")
        file_menu.add_command(label="Load Session", command=self.load_session, accelerator="Ctrl+O")
        file_menu.add_separator()
        file_menu.add_command(label="Export Log", command=self.export_log)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.root.quit, accelerator="Ctrl+Q")
        
        # Simulation menu
        sim_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Simulation", menu=sim_menu)
        sim_menu.add_command(label="Advance Turn", command=self.advance_turn, accelerator="Space")
        sim_menu.add_command(label="Trigger Event", command=self.trigger_event)
        sim_menu.add_command(label="Generate Rumor", command=self.generate_rumor)
        sim_menu.add_separator()
        sim_menu.add_checkbutton(label="Auto Events", variable=tk.BooleanVar(value=True), 
                                command=self.toggle_auto_events)
        
        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Refresh Display", command=self.update_display, accelerator="F5")
        view_menu.add_command(label="Character Details", command=self.show_character_details)
        
        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)
        
        # Bind keyboard shortcuts
        self.root.bind('<Control-n>', lambda e: self.new_tavern())
        self.root.bind('<Control-s>', lambda e: self.save_session())
        self.root.bind('<Control-o>', lambda e: self.load_session())
        self.root.bind('<Control-q>', lambda e: self.root.quit())
        self.root.bind('<space>', lambda e: self.advance_turn())
        self.root.bind('<F5>', lambda e: self.update_display())
    
    def create_tabs(self):
        """Create the main content tabs"""
        # Relationship Graph tab
        graph_frame = ttk.Frame(self.notebook)
        self.notebook.add(graph_frame, text="Relationships")
        self.relationship_graph = RelationshipGraph(graph_frame, self.simulator)
        
        # Interactions tab
        interaction_frame = ttk.Frame(self.notebook)
        self.notebook.add(interaction_frame, text="Interactions")
        self.interaction_panel = InteractionPanel(interaction_frame, self.simulator, self.update_display)
        
        # Log tab
        log_frame = ttk.Frame(self.notebook)
        self.notebook.add(log_frame, text="Session Log")
        self.log_panel = LogPanel(log_frame, self.simulator)
    
    def create_status_bar(self):
        """Create the status bar"""
        self.status_bar = ttk.Frame(self.root)
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=5, pady=(0, 5))
        
        self.status_label = ttk.Label(self.status_bar, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        self.turn_label = ttk.Label(self.status_bar, text="Turn: 0")
        self.turn_label.pack(side=tk.RIGHT)
    
    def new_tavern(self):
        """Generate a new tavern"""
        try:
            self.simulator.generate_new_tavern()
            self.update_display()
            self.status_label.config(text="New tavern generated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate tavern: {str(e)}")
    
    def save_session(self):
        """Save the current session"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".pkl",
                filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
            )
            if filename:
                saved_file = self.simulator.save_session(filename)
                self.status_label.config(text=f"Session saved to {saved_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session: {str(e)}")
    
    def load_session(self):
        """Load a saved session"""
        try:
            filename = filedialog.askopenfilename(
                filetypes=[("Pickle files", "*.pkl"), ("All files", "*.*")]
            )
            if filename:
                if self.simulator.load_session(filename):
                    self.update_display()
                    self.status_label.config(text=f"Session loaded from {filename}")
                else:
                    messagebox.showerror("Error", "Failed to load session file")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load session: {str(e)}")
    
    def export_log(self):
        """Export the session log"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
            )
            if filename:
                exported_file = self.simulator.export_session_log(filename)
                self.status_label.config(text=f"Log exported to {exported_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export log: {str(e)}")
    
    def advance_turn(self):
        """Advance the simulation by one turn"""
        try:
            self.simulator.advance_turn()
            self.update_display()
            self.status_label.config(text="Turn advanced")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to advance turn: {str(e)}")
    
    def trigger_event(self):
        """Manually trigger a random event"""
        try:
            event = self.simulator.trigger_random_event()
            if event:
                self.update_display()
                self.status_label.config(text=f"Event triggered: {event.title}")
            else:
                self.status_label.config(text="No event occurred")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to trigger event: {str(e)}")
    
    def generate_rumor(self):
        """Generate a new rumor"""
        try:
            rumor = self.simulator.generate_rumor()
            if rumor:
                self.update_display()
                self.status_label.config(text="New rumor generated")
            else:
                self.status_label.config(text="No rumor generated")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to generate rumor: {str(e)}")
    
    def toggle_auto_events(self):
        """Toggle automatic event generation"""
        self.simulator.auto_events_enabled = not self.simulator.auto_events_enabled
        status = "enabled" if self.simulator.auto_events_enabled else "disabled"
        self.status_label.config(text=f"Auto events {status}")
    
    def show_character_details(self):
        """Show detailed character information"""
        # This would open a detailed character window
        messagebox.showinfo("Character Details", "Character details window not yet implemented")
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Warhammer Fantasy Tavern Simulator
        
A comprehensive tavern simulation set in the Warhammer Fantasy universe.

Features:
• 17 unique NPCs from diverse factions
• Dynamic relationship system
• Dice-based interaction mechanics
• Random events and rumors
• Tension and brawl system
• Interactive relationship visualization

Created with Python and Tkinter"""
        
        messagebox.showinfo("About", about_text)
    
    def update_display(self):
        """Update all display elements"""
        try:
            # Update turn counter
            self.turn_label.config(text=f"Turn: {self.simulator.turn_counter}")
            
            # Update all panels
            if hasattr(self, 'tavern_panel'):
                self.tavern_panel.update_display()
            if hasattr(self, 'character_panel'):
                self.character_panel.update_display()
            if hasattr(self, 'relationship_graph'):
                self.relationship_graph.update_display()
            if hasattr(self, 'interaction_panel'):
                self.interaction_panel.update_display()
            if hasattr(self, 'log_panel'):
                self.log_panel.update_display()
                
        except Exception as e:
            print(f"Error updating display: {e}")
    
    def run(self):
        """Start the main event loop"""
        self.root.mainloop()
