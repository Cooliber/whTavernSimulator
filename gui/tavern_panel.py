"""
Tavern information panel for the Warhammer Fantasy Tavern Simulator
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
from ..core.tavern_simulator import TavernSimulator

class TavernPanel:
    """Panel displaying tavern information and controls"""
    
    def __init__(self, parent: tk.Widget, simulator: TavernSimulator):
        self.parent = parent
        self.simulator = simulator
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets for the tavern panel"""
        # Main frame
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.frame, text="Tavern Information", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Tavern name
        self.name_var = tk.StringVar()
        name_frame = ttk.Frame(self.frame)
        name_frame.pack(fill=tk.X, pady=2)
        ttk.Label(name_frame, text="Name:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        name_label = ttk.Label(name_frame, textvariable=self.name_var, wraplength=280)
        name_label.pack(anchor=tk.W, fill=tk.X)
        
        # Tavern description
        self.desc_var = tk.StringVar()
        desc_frame = ttk.Frame(self.frame)
        desc_frame.pack(fill=tk.X, pady=2)
        ttk.Label(desc_frame, text="Description:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        desc_label = ttk.Label(desc_frame, textvariable=self.desc_var, wraplength=280, justify=tk.LEFT)
        desc_label.pack(anchor=tk.W, fill=tk.X)
        
        # Location
        self.location_var = tk.StringVar()
        location_frame = ttk.Frame(self.frame)
        location_frame.pack(fill=tk.X, pady=2)
        ttk.Label(location_frame, text="Location:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        location_label = ttk.Label(location_frame, textvariable=self.location_var, wraplength=280)
        location_label.pack(anchor=tk.W, fill=tk.X)
        
        # Separator
        ttk.Separator(self.frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        
        # Status information
        status_frame = ttk.LabelFrame(self.frame, text="Current Status")
        status_frame.pack(fill=tk.X, pady=5)
        
        # Atmosphere
        self.atmosphere_var = tk.StringVar()
        atm_frame = ttk.Frame(status_frame)
        atm_frame.pack(fill=tk.X, pady=2)
        ttk.Label(atm_frame, text="Atmosphere:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        ttk.Label(atm_frame, textvariable=self.atmosphere_var).pack(anchor=tk.W)
        
        # Atmosphere description
        self.atm_desc_var = tk.StringVar()
        atm_desc_label = ttk.Label(status_frame, textvariable=self.atm_desc_var, 
                                  wraplength=260, justify=tk.LEFT, font=("Arial", 8))
        atm_desc_label.pack(anchor=tk.W, fill=tk.X, pady=(0, 5))
        
        # Occupancy
        self.occupancy_var = tk.StringVar()
        occ_frame = ttk.Frame(status_frame)
        occ_frame.pack(fill=tk.X, pady=2)
        ttk.Label(occ_frame, text="Occupancy:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        ttk.Label(occ_frame, textvariable=self.occupancy_var).pack(anchor=tk.W)
        
        # Tension meter
        tension_frame = ttk.Frame(status_frame)
        tension_frame.pack(fill=tk.X, pady=2)
        ttk.Label(tension_frame, text="Tension:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        
        self.tension_var = tk.IntVar()
        self.tension_progress = ttk.Progressbar(tension_frame, variable=self.tension_var, 
                                              maximum=100, length=200)
        self.tension_progress.pack(fill=tk.X, pady=2)
        
        self.tension_label = ttk.Label(tension_frame, text="0/100")
        self.tension_label.pack(anchor=tk.W)
        
        # Reputation
        self.reputation_var = tk.StringVar()
        rep_frame = ttk.Frame(status_frame)
        rep_frame.pack(fill=tk.X, pady=2)
        ttk.Label(rep_frame, text="Reputation:", font=("Arial", 9, "bold")).pack(anchor=tk.W)
        ttk.Label(rep_frame, textvariable=self.reputation_var).pack(anchor=tk.W)
        
        # Current events
        events_frame = ttk.LabelFrame(self.frame, text="Current Events")
        events_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Events listbox with scrollbar
        events_list_frame = ttk.Frame(events_frame)
        events_list_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.events_listbox = tk.Listbox(events_list_frame, height=4)
        events_scrollbar = ttk.Scrollbar(events_list_frame, orient=tk.VERTICAL, 
                                        command=self.events_listbox.yview)
        self.events_listbox.config(yscrollcommand=events_scrollbar.set)
        
        self.events_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        events_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Control buttons
        controls_frame = ttk.LabelFrame(self.frame, text="Controls")
        controls_frame.pack(fill=tk.X, pady=5)
        
        # Button frame
        button_frame = ttk.Frame(controls_frame)
        button_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(button_frame, text="New Tavern", 
                  command=self.new_tavern).pack(fill=tk.X, pady=1)
        ttk.Button(button_frame, text="Advance Turn", 
                  command=self.advance_turn).pack(fill=tk.X, pady=1)
        ttk.Button(button_frame, text="Trigger Event", 
                  command=self.trigger_event).pack(fill=tk.X, pady=1)
        ttk.Button(button_frame, text="Generate Rumor", 
                  command=self.generate_rumor).pack(fill=tk.X, pady=1)
        
        # Character management
        char_mgmt_frame = ttk.LabelFrame(self.frame, text="Character Management")
        char_mgmt_frame.pack(fill=tk.X, pady=5)
        
        # Available characters dropdown
        char_frame = ttk.Frame(char_mgmt_frame)
        char_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(char_frame, text="Add Character:").pack(anchor=tk.W)
        
        self.available_chars_var = tk.StringVar()
        self.available_chars_combo = ttk.Combobox(char_frame, textvariable=self.available_chars_var,
                                                 state="readonly")
        self.available_chars_combo.pack(fill=tk.X, pady=2)
        
        ttk.Button(char_frame, text="Add to Tavern", 
                  command=self.add_character).pack(fill=tk.X, pady=2)
    
    def new_tavern(self):
        """Generate a new tavern"""
        self.simulator.generate_new_tavern()
        self.update_display()
    
    def advance_turn(self):
        """Advance the simulation by one turn"""
        self.simulator.advance_turn()
        self.update_display()
    
    def trigger_event(self):
        """Trigger a random event"""
        self.simulator.trigger_random_event()
        self.update_display()
    
    def generate_rumor(self):
        """Generate a new rumor"""
        self.simulator.generate_rumor()
        self.update_display()
    
    def add_character(self):
        """Add selected character to tavern"""
        char_name = self.available_chars_var.get()
        if char_name:
            success = self.simulator.add_character_to_tavern(char_name)
            if success:
                self.update_display()
    
    def update_display(self):
        """Update the display with current tavern information"""
        tavern = self.simulator.current_tavern
        if not tavern:
            # Clear display if no tavern
            self.name_var.set("No tavern loaded")
            self.desc_var.set("")
            self.location_var.set("")
            self.atmosphere_var.set("")
            self.atm_desc_var.set("")
            self.occupancy_var.set("")
            self.tension_var.set(0)
            self.tension_label.config(text="0/100")
            self.reputation_var.set("")
            self.events_listbox.delete(0, tk.END)
            self.available_chars_combo['values'] = []
            return
        
        # Update basic information
        self.name_var.set(tavern.name)
        self.desc_var.set(tavern.description)
        self.location_var.set(tavern.location)
        
        # Update status
        self.atmosphere_var.set(tavern.atmosphere.value)
        self.atm_desc_var.set(tavern.atmosphere_description)
        self.occupancy_var.set(f"{tavern.current_occupancy}/{tavern.capacity}")
        
        # Update tension meter
        self.tension_var.set(tavern.tension_level)
        self.tension_label.config(text=f"{tavern.tension_level}/100")
        
        # Color code tension meter
        if tavern.tension_level < 30:
            self.tension_progress.config(style="green.Horizontal.TProgressbar")
        elif tavern.tension_level < 70:
            self.tension_progress.config(style="yellow.Horizontal.TProgressbar")
        else:
            self.tension_progress.config(style="red.Horizontal.TProgressbar")
        
        # Update reputation
        rep_text = f"{tavern.reputation}/100"
        if tavern.reputation < 30:
            rep_text += " (Poor)"
        elif tavern.reputation < 70:
            rep_text += " (Average)"
        else:
            rep_text += " (Excellent)"
        self.reputation_var.set(rep_text)
        
        # Update events list
        self.events_listbox.delete(0, tk.END)
        for event in tavern.current_events:
            self.events_listbox.insert(tk.END, event)
        
        # Update available characters dropdown
        current_char_names = {char.name for char in tavern.characters}
        available_chars = [name for name in self.simulator.available_characters.keys() 
                          if name not in current_char_names]
        self.available_chars_combo['values'] = available_chars
        
        if available_chars and not self.available_chars_var.get():
            self.available_chars_var.set(available_chars[0])
