"""
Character information panel for the Warhammer Fantasy Tavern Simulator
"""

import tkinter as tk
from tkinter import ttk
from typing import Optional
from ..core.tavern_simulator import TavernSimulator
from ..core.character import Character

class CharacterPanel:
    """Panel displaying character information and details"""
    
    def __init__(self, parent: tk.Widget, simulator: TavernSimulator):
        self.parent = parent
        self.simulator = simulator
        self.selected_character: Optional[Character] = None
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets for the character panel"""
        # Main frame
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.frame, text="Characters", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Character list
        list_frame = ttk.LabelFrame(self.frame, text="Characters in Tavern")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Character listbox with scrollbar
        list_container = ttk.Frame(list_frame)
        list_container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        self.char_listbox = tk.Listbox(list_container, height=8)
        char_scrollbar = ttk.Scrollbar(list_container, orient=tk.VERTICAL, 
                                      command=self.char_listbox.yview)
        self.char_listbox.config(yscrollcommand=char_scrollbar.set)
        
        self.char_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        char_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind selection event
        self.char_listbox.bind('<<ListboxSelect>>', self.on_character_select)
        
        # Character details
        details_frame = ttk.LabelFrame(self.frame, text="Character Details")
        details_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Create scrollable frame for character details
        details_canvas = tk.Canvas(details_frame, height=300)
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, 
                                         command=details_canvas.yview)
        self.details_frame = ttk.Frame(details_canvas)
        
        self.details_frame.bind(
            "<Configure>",
            lambda e: details_canvas.configure(scrollregion=details_canvas.bbox("all"))
        )
        
        details_canvas.create_window((0, 0), window=self.details_frame, anchor="nw")
        details_canvas.configure(yscrollcommand=details_scrollbar.set)
        
        details_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Initialize character details widgets
        self.create_character_details()
        
        # Character actions
        actions_frame = ttk.LabelFrame(self.frame, text="Actions")
        actions_frame.pack(fill=tk.X, pady=5)
        
        action_buttons = ttk.Frame(actions_frame)
        action_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(action_buttons, text="Remove from Tavern", 
                  command=self.remove_character).pack(fill=tk.X, pady=1)
        ttk.Button(action_buttons, text="View Relationships", 
                  command=self.view_relationships).pack(fill=tk.X, pady=1)
    
    def create_character_details(self):
        """Create widgets for displaying character details"""
        # Character name
        self.name_var = tk.StringVar()
        name_label = ttk.Label(self.details_frame, textvariable=self.name_var, 
                              font=("Arial", 10, "bold"))
        name_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Basic info
        self.faction_var = tk.StringVar()
        self.class_var = tk.StringVar()
        self.age_var = tk.StringVar()
        
        basic_frame = ttk.Frame(self.details_frame)
        basic_frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(basic_frame, text="Faction:", font=("Arial", 8, "bold")).grid(row=0, column=0, sticky=tk.W)
        ttk.Label(basic_frame, textvariable=self.faction_var, font=("Arial", 8)).grid(row=0, column=1, sticky=tk.W)
        
        ttk.Label(basic_frame, text="Class:", font=("Arial", 8, "bold")).grid(row=1, column=0, sticky=tk.W)
        ttk.Label(basic_frame, textvariable=self.class_var, font=("Arial", 8)).grid(row=1, column=1, sticky=tk.W)
        
        ttk.Label(basic_frame, text="Age:", font=("Arial", 8, "bold")).grid(row=2, column=0, sticky=tk.W)
        ttk.Label(basic_frame, textvariable=self.age_var, font=("Arial", 8)).grid(row=2, column=1, sticky=tk.W)
        
        # Appearance
        ttk.Label(self.details_frame, text="Appearance:", font=("Arial", 8, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.appearance_var = tk.StringVar()
        appearance_label = ttk.Label(self.details_frame, textvariable=self.appearance_var, 
                                   wraplength=250, justify=tk.LEFT, font=("Arial", 8))
        appearance_label.pack(anchor=tk.W, fill=tk.X)
        
        # Backstory
        ttk.Label(self.details_frame, text="Backstory:", font=("Arial", 8, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.backstory_var = tk.StringVar()
        backstory_label = ttk.Label(self.details_frame, textvariable=self.backstory_var, 
                                   wraplength=250, justify=tk.LEFT, font=("Arial", 8))
        backstory_label.pack(anchor=tk.W, fill=tk.X)
        
        # Personality traits
        ttk.Label(self.details_frame, text="Personality:", font=("Arial", 8, "bold")).pack(anchor=tk.W, pady=(10, 0))
        self.personality_var = tk.StringVar()
        personality_label = ttk.Label(self.details_frame, textvariable=self.personality_var, 
                                     wraplength=250, justify=tk.LEFT, font=("Arial", 8))
        personality_label.pack(anchor=tk.W, fill=tk.X)
        
        # Status
        status_frame = ttk.LabelFrame(self.details_frame, text="Current Status")
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.mood_var = tk.StringVar()
        self.health_var = tk.StringVar()
        self.wealth_var = tk.StringVar()
        self.drunk_var = tk.StringVar()
        
        ttk.Label(status_frame, text="Mood:", font=("Arial", 8, "bold")).grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(status_frame, textvariable=self.mood_var, font=("Arial", 8)).grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(status_frame, text="Health:", font=("Arial", 8, "bold")).grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(status_frame, textvariable=self.health_var, font=("Arial", 8)).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(status_frame, text="Wealth:", font=("Arial", 8, "bold")).grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(status_frame, textvariable=self.wealth_var, font=("Arial", 8)).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        ttk.Label(status_frame, text="Drunk Level:", font=("Arial", 8, "bold")).grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        ttk.Label(status_frame, textvariable=self.drunk_var, font=("Arial", 8)).grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Top skills
        skills_frame = ttk.LabelFrame(self.details_frame, text="Top Skills")
        skills_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.skills_text = tk.Text(skills_frame, height=4, wrap=tk.WORD, font=("Arial", 8))
        self.skills_text.pack(fill=tk.X, padx=5, pady=5)
        
        # Clear initial display
        self.clear_character_details()
    
    def on_character_select(self, event):
        """Handle character selection from listbox"""
        selection = self.char_listbox.curselection()
        if selection and self.simulator.current_tavern:
            index = selection[0]
            if index < len(self.simulator.current_tavern.characters):
                self.selected_character = self.simulator.current_tavern.characters[index]
                self.update_character_details()
    
    def clear_character_details(self):
        """Clear all character detail fields"""
        self.name_var.set("Select a character")
        self.faction_var.set("")
        self.class_var.set("")
        self.age_var.set("")
        self.appearance_var.set("")
        self.backstory_var.set("")
        self.personality_var.set("")
        self.mood_var.set("")
        self.health_var.set("")
        self.wealth_var.set("")
        self.drunk_var.set("")
        self.skills_text.delete(1.0, tk.END)
    
    def update_character_details(self):
        """Update character details display"""
        if not self.selected_character:
            self.clear_character_details()
            return
        
        char = self.selected_character
        
        # Basic info
        self.name_var.set(char.name)
        self.faction_var.set(char.faction.value)
        self.class_var.set(char.character_class.value)
        self.age_var.set(f"{char.age} years old")
        
        # Appearance and background
        self.appearance_var.set(char.appearance)
        self.backstory_var.set(char.backstory)
        self.personality_var.set(", ".join(char.personality_traits))
        
        # Status
        self.mood_var.set(char.current_mood.title())
        self.health_var.set(f"{char.health}/100")
        self.wealth_var.set(f"{char.wealth} coins")
        
        drunk_status = "Drunk" if char.is_drunk() else f"{char.drunk_level}/10"
        self.drunk_var.set(drunk_status)
        
        # Top skills
        self.skills_text.delete(1.0, tk.END)
        sorted_skills = sorted(char.skills.items(), key=lambda x: x[1], reverse=True)
        top_skills = sorted_skills[:6]  # Show top 6 skills
        
        for skill, value in top_skills:
            self.skills_text.insert(tk.END, f"{skill.value}: {value}\n")
    
    def remove_character(self):
        """Remove selected character from tavern"""
        if self.selected_character:
            success = self.simulator.remove_character_from_tavern(self.selected_character.name)
            if success:
                self.selected_character = None
                self.update_display()
    
    def view_relationships(self):
        """View relationships for selected character"""
        if self.selected_character:
            # This would open a relationships window
            # For now, just show a simple message
            relationships = []
            for other_char in self.simulator.current_tavern.characters:
                if other_char != self.selected_character:
                    rel = self.selected_character.get_relationship(other_char.name)
                    relationships.append(f"{other_char.name}: {rel.name}")
            
            if relationships:
                rel_text = "\n".join(relationships)
                tk.messagebox.showinfo(f"{self.selected_character.name}'s Relationships", rel_text)
            else:
                tk.messagebox.showinfo("Relationships", "No relationships to display")
    
    def update_display(self):
        """Update the character list and details"""
        # Clear listbox
        self.char_listbox.delete(0, tk.END)
        
        if not self.simulator.current_tavern:
            self.clear_character_details()
            return
        
        # Populate character list
        for char in self.simulator.current_tavern.characters:
            display_text = f"{char.name} ({char.faction.value})"
            if char.is_drunk():
                display_text += " [DRUNK]"
            if char.health < 50:
                display_text += " [INJURED]"
            
            self.char_listbox.insert(tk.END, display_text)
        
        # Update character details if one is selected
        if self.selected_character:
            # Check if selected character is still in tavern
            if self.selected_character in self.simulator.current_tavern.characters:
                self.update_character_details()
            else:
                self.selected_character = None
                self.clear_character_details()
