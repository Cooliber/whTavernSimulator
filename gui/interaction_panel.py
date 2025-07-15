"""
Interaction panel for the Warhammer Fantasy Tavern Simulator
"""

import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
from ..core.tavern_simulator import TavernSimulator
from ..core.enums import InteractionType

class InteractionPanel:
    """Panel for managing character interactions"""
    
    def __init__(self, parent: tk.Widget, simulator: TavernSimulator, update_callback: Callable):
        self.parent = parent
        self.simulator = simulator
        self.update_callback = update_callback
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets for the interaction panel"""
        # Main frame
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(self.frame, text="Character Interactions", font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Interaction setup frame
        setup_frame = ttk.LabelFrame(self.frame, text="Setup Interaction")
        setup_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Character selection
        char_frame = ttk.Frame(setup_frame)
        char_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Initiator selection
        ttk.Label(char_frame, text="Initiator:").grid(row=0, column=0, sticky=tk.W, pady=2)
        self.initiator_var = tk.StringVar()
        self.initiator_combo = ttk.Combobox(char_frame, textvariable=self.initiator_var,
                                           state="readonly", width=20)
        self.initiator_combo.grid(row=0, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Target selection
        ttk.Label(char_frame, text="Target:").grid(row=1, column=0, sticky=tk.W, pady=2)
        self.target_var = tk.StringVar()
        self.target_combo = ttk.Combobox(char_frame, textvariable=self.target_var,
                                        state="readonly", width=20)
        self.target_combo.grid(row=1, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Interaction type selection
        ttk.Label(char_frame, text="Interaction:").grid(row=2, column=0, sticky=tk.W, pady=2)
        self.interaction_var = tk.StringVar()
        self.interaction_combo = ttk.Combobox(char_frame, textvariable=self.interaction_var,
                                             state="readonly", width=20)
        self.interaction_combo.grid(row=2, column=1, sticky=tk.W, padx=(5, 0), pady=2)
        
        # Populate interaction types
        interaction_types = [interaction.value for interaction in InteractionType]
        self.interaction_combo['values'] = interaction_types
        
        # Perform interaction button
        ttk.Button(char_frame, text="Perform Interaction", 
                  command=self.perform_interaction).grid(row=3, column=0, columnspan=2, 
                                                        pady=10, sticky=tk.EW)
        
        # Quick actions frame
        quick_frame = ttk.LabelFrame(self.frame, text="Quick Actions")
        quick_frame.pack(fill=tk.X, padx=5, pady=5)
        
        quick_buttons = ttk.Frame(quick_frame)
        quick_buttons.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Button(quick_buttons, text="Random Conversation", 
                  command=self.random_conversation).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_buttons, text="Drinking Round", 
                  command=self.drinking_round).pack(side=tk.LEFT, padx=2)
        ttk.Button(quick_buttons, text="Gambling Game", 
                  command=self.gambling_game).pack(side=tk.LEFT, padx=2)
        
        # Recent interactions frame
        recent_frame = ttk.LabelFrame(self.frame, text="Recent Interactions")
        recent_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create treeview for interaction history
        columns = ("Time", "Initiator", "Target", "Type", "Result")
        self.interactions_tree = ttk.Treeview(recent_frame, columns=columns, show="headings", height=10)
        
        # Configure columns
        self.interactions_tree.heading("Time", text="Time")
        self.interactions_tree.heading("Initiator", text="Initiator")
        self.interactions_tree.heading("Target", text="Target")
        self.interactions_tree.heading("Type", text="Type")
        self.interactions_tree.heading("Result", text="Result")
        
        self.interactions_tree.column("Time", width=80)
        self.interactions_tree.column("Initiator", width=120)
        self.interactions_tree.column("Target", width=120)
        self.interactions_tree.column("Type", width=100)
        self.interactions_tree.column("Result", width=80)
        
        # Add scrollbar
        tree_scrollbar = ttk.Scrollbar(recent_frame, orient=tk.VERTICAL, 
                                      command=self.interactions_tree.yview)
        self.interactions_tree.configure(yscrollcommand=tree_scrollbar.set)
        
        self.interactions_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        tree_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Bind double-click to show details
        self.interactions_tree.bind("<Double-1>", self.show_interaction_details)
        
        # Interaction details frame
        details_frame = ttk.LabelFrame(self.frame, text="Interaction Details")
        details_frame.pack(fill=tk.X, padx=5, pady=5)
        
        self.details_text = tk.Text(details_frame, height=4, wrap=tk.WORD, font=("Arial", 9))
        details_scrollbar = ttk.Scrollbar(details_frame, orient=tk.VERTICAL, 
                                         command=self.details_text.yview)
        self.details_text.configure(yscrollcommand=details_scrollbar.set)
        
        self.details_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5, pady=5)
        details_scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
    
    def perform_interaction(self):
        """Perform the selected interaction"""
        initiator = self.initiator_var.get()
        target = self.target_var.get()
        interaction_type_str = self.interaction_var.get()
        
        if not all([initiator, target, interaction_type_str]):
            messagebox.showwarning("Incomplete Selection", 
                                 "Please select initiator, target, and interaction type.")
            return
        
        if initiator == target:
            messagebox.showwarning("Invalid Selection", 
                                 "Initiator and target cannot be the same character.")
            return
        
        # Convert string to enum
        try:
            interaction_type = InteractionType(interaction_type_str)
        except ValueError:
            messagebox.showerror("Error", "Invalid interaction type selected.")
            return
        
        # Perform the interaction
        interaction = self.simulator.perform_interaction(initiator, target, interaction_type)
        
        if interaction:
            self.update_display()
            self.update_callback()
            
            # Show result in details
            self.show_interaction_result(interaction)
        else:
            messagebox.showwarning("Interaction Failed", 
                                 "The interaction could not be performed.")
    
    def random_conversation(self):
        """Start a random conversation between two characters"""
        if not self.simulator.current_tavern or len(self.simulator.current_tavern.characters) < 2:
            messagebox.showwarning("Not Enough Characters", 
                                 "Need at least 2 characters for a conversation.")
            return
        
        import random
        chars = random.sample(self.simulator.current_tavern.characters, 2)
        
        interaction = self.simulator.perform_interaction(
            chars[0].name, chars[1].name, InteractionType.CONVERSATION
        )
        
        if interaction:
            self.update_display()
            self.update_callback()
            self.show_interaction_result(interaction)
    
    def drinking_round(self):
        """Start a drinking round among characters"""
        if not self.simulator.current_tavern:
            return
        
        # Make multiple characters drink
        for char in self.simulator.current_tavern.characters:
            if self.simulator.current_tavern.serve_drink(char):
                self.simulator.log_event(f"{char.name} drinks ale")
        
        self.update_callback()
        self.details_text.delete(1.0, tk.END)
        self.details_text.insert(tk.END, "A round of drinks is served to all patrons!")
    
    def gambling_game(self):
        """Start a gambling game between random characters"""
        if not self.simulator.current_tavern or len(self.simulator.current_tavern.characters) < 2:
            messagebox.showwarning("Not Enough Characters", 
                                 "Need at least 2 characters for gambling.")
            return
        
        import random
        chars = random.sample(self.simulator.current_tavern.characters, 2)
        
        interaction = self.simulator.perform_interaction(
            chars[0].name, chars[1].name, InteractionType.GAMBLING
        )
        
        if interaction:
            self.update_display()
            self.update_callback()
            self.show_interaction_result(interaction)
    
    def show_interaction_result(self, interaction):
        """Show the result of an interaction in the details area"""
        self.details_text.delete(1.0, tk.END)
        
        result_text = f"Interaction: {interaction.interaction_type.value}\n"
        result_text += f"Initiator: {interaction.initiator}\n"
        result_text += f"Target: {interaction.target}\n"
        result_text += f"Dice Roll: {interaction.dice_roll} + {interaction.modifier} = {interaction.dice_roll + interaction.modifier}\n"
        result_text += f"Result: {'SUCCESS' if interaction.success else 'FAILURE'}\n"
        result_text += f"Outcome: {interaction.outcome_description}\n"
        
        if interaction.relationship_change != 0:
            change_text = "improved" if interaction.relationship_change > 0 else "worsened"
            result_text += f"Relationship {change_text} by {abs(interaction.relationship_change)}\n"
        
        self.details_text.insert(tk.END, result_text)
    
    def show_interaction_details(self, event):
        """Show details of selected interaction"""
        selection = self.interactions_tree.selection()
        if not selection:
            return
        
        item = self.interactions_tree.item(selection[0])
        values = item['values']
        
        if len(values) >= 5:
            # Find the interaction in history
            time_str = values[0]
            initiator = values[1]
            target = values[2]
            
            # Find matching interaction (simplified)
            for interaction in reversed(self.simulator.interaction_history):
                if (interaction.initiator == initiator and 
                    interaction.target == target):
                    self.show_interaction_result(interaction)
                    break
    
    def update_display(self):
        """Update the interaction panel display"""
        if not self.simulator.current_tavern:
            # Clear everything if no tavern
            self.initiator_combo['values'] = []
            self.target_combo['values'] = []
            self.interactions_tree.delete(*self.interactions_tree.get_children())
            self.details_text.delete(1.0, tk.END)
            return
        
        # Update character lists
        char_names = [char.name for char in self.simulator.current_tavern.characters]
        self.initiator_combo['values'] = char_names
        self.target_combo['values'] = char_names
        
        # Set default selections if empty
        if char_names:
            if not self.initiator_var.get() or self.initiator_var.get() not in char_names:
                self.initiator_var.set(char_names[0])
            if not self.target_var.get() or self.target_var.get() not in char_names:
                if len(char_names) > 1:
                    self.target_var.set(char_names[1])
        
        # Update interaction history
        self.interactions_tree.delete(*self.interactions_tree.get_children())
        
        # Show last 20 interactions
        recent_interactions = self.simulator.interaction_history[-20:]
        for interaction in reversed(recent_interactions):
            time_str = interaction.timestamp.strftime("%H:%M:%S")
            result = "SUCCESS" if interaction.success else "FAILURE"
            
            self.interactions_tree.insert("", 0, values=(
                time_str,
                interaction.initiator,
                interaction.target,
                interaction.interaction_type.value,
                result
            ))
