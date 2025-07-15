"""
Relationship graph visualization for the Warhammer Fantasy Tavern Simulator
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import networkx as nx
import numpy as np
from typing import Dict, List, Tuple
from ..core.tavern_simulator import TavernSimulator
from ..core.enums import RelationshipType

class RelationshipGraph:
    """Interactive relationship graph visualization"""
    
    def __init__(self, parent: tk.Widget, simulator: TavernSimulator):
        self.parent = parent
        self.simulator = simulator
        
        # Graph settings
        self.node_size = 1000
        self.font_size = 8
        self.edge_width_multiplier = 2
        
        self.create_widgets()
        self.setup_graph()
    
    def create_widgets(self):
        """Create the graph visualization widgets"""
        # Main frame
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Control frame
        control_frame = ttk.Frame(self.frame)
        control_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Refresh button
        ttk.Button(control_frame, text="Refresh Graph", 
                  command=self.update_display).pack(side=tk.LEFT, padx=5)
        
        # Layout selection
        ttk.Label(control_frame, text="Layout:").pack(side=tk.LEFT, padx=(20, 5))
        self.layout_var = tk.StringVar(value="spring")
        layout_combo = ttk.Combobox(control_frame, textvariable=self.layout_var,
                                   values=["spring", "circular", "random", "shell"],
                                   state="readonly", width=10)
        layout_combo.pack(side=tk.LEFT, padx=5)
        layout_combo.bind('<<ComboboxSelected>>', lambda e: self.update_display())
        
        # Show labels checkbox
        self.show_labels_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(control_frame, text="Show Labels", 
                       variable=self.show_labels_var,
                       command=self.update_display).pack(side=tk.LEFT, padx=20)
        
        # Legend frame
        legend_frame = ttk.LabelFrame(self.frame, text="Relationship Legend")
        legend_frame.pack(fill=tk.X, padx=5, pady=5)
        
        legend_content = ttk.Frame(legend_frame)
        legend_content.pack(fill=tk.X, padx=5, pady=5)
        
        # Create legend items
        legend_items = [
            ("Loyalty", "darkgreen", "━━━"),
            ("Friendship", "green", "━━━"),
            ("Acquaintance", "lightgreen", "━━━"),
            ("Neutral", "gray", "━━━"),
            ("Distrust", "orange", "━━━"),
            ("Dislike", "red", "━━━"),
            ("Hatred", "darkred", "━━━")
        ]
        
        for i, (label, color, line) in enumerate(legend_items):
            col = i % 4
            row = i // 4
            
            item_frame = ttk.Frame(legend_content)
            item_frame.grid(row=row, column=col, sticky=tk.W, padx=10, pady=2)
            
            # Color indicator (using a label with colored text)
            color_label = tk.Label(item_frame, text=line, fg=color, font=("Arial", 10, "bold"))
            color_label.pack(side=tk.LEFT)
            
            tk.Label(item_frame, text=label, font=("Arial", 8)).pack(side=tk.LEFT, padx=(5, 0))
    
    def setup_graph(self):
        """Set up the matplotlib figure and canvas"""
        # Create matplotlib figure
        self.fig, self.ax = plt.subplots(figsize=(10, 8))
        self.fig.patch.set_facecolor('white')
        
        # Create canvas
        self.canvas = FigureCanvasTkAgg(self.fig, self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Initialize empty graph
        self.graph = nx.Graph()
        
        # Initial empty plot
        self.ax.set_title("Character Relationships", fontsize=14, fontweight='bold')
        self.ax.text(0.5, 0.5, "No tavern loaded", ha='center', va='center', 
                    transform=self.ax.transAxes, fontsize=12)
        self.ax.set_xlim(0, 1)
        self.ax.set_ylim(0, 1)
        self.ax.axis('off')
        
        self.canvas.draw()
    
    def get_relationship_color(self, relationship_value: int) -> str:
        """Get color for relationship based on value"""
        color_map = {
            3: "darkgreen",    # Loyalty
            2: "green",        # Friendship
            1: "lightgreen",   # Acquaintance
            0: "gray",         # Neutral
            -1: "orange",      # Distrust
            -2: "red",         # Dislike
            -3: "darkred"      # Hatred
        }
        return color_map.get(relationship_value, "gray")
    
    def get_relationship_width(self, relationship_value: int) -> float:
        """Get edge width based on relationship strength"""
        abs_value = abs(relationship_value)
        return max(0.5, abs_value * self.edge_width_multiplier)
    
    def get_node_color(self, character_name: str) -> str:
        """Get node color based on character faction"""
        if not self.simulator.current_tavern:
            return "lightblue"
        
        character = self.simulator.current_tavern.get_character_by_name(character_name)
        if not character:
            return "lightblue"
        
        faction_colors = {
            "Empire": "gold",
            "Dwarf": "brown",
            "High Elf": "lightblue",
            "Wood Elf": "forestgreen",
            "Bretonnian": "blue",
            "Halfling": "orange",
            "Tilean": "purple",
            "Estalia": "red",
            "Kislev": "lightcyan",
            "Norse": "darkgray",
            "Arabyan": "yellow",
            "Cathayan": "crimson",
            "Nipponese": "pink",
            "Mercenary": "silver",
            "Outlaw": "black",
            "Cultist": "darkred",
            "Witch Hunter": "white"
        }
        
        return faction_colors.get(character.faction.value, "lightblue")
    
    def create_graph_from_relationships(self) -> nx.Graph:
        """Create NetworkX graph from character relationships"""
        graph = nx.Graph()
        
        if not self.simulator.current_tavern:
            return graph
        
        characters = self.simulator.current_tavern.characters
        
        # Add nodes
        for char in characters:
            graph.add_node(char.name)
        
        # Add edges for relationships
        for char in characters:
            for other_char in characters:
                if char != other_char:
                    relationship = char.get_relationship(other_char.name)
                    rel_value = int(relationship)
                    
                    # Only add edge if relationship is not neutral or if we want to show all
                    if rel_value != 0 or len(characters) <= 5:  # Show all edges for small groups
                        if not graph.has_edge(char.name, other_char.name):
                            graph.add_edge(char.name, other_char.name, weight=rel_value)
        
        return graph
    
    def get_layout_positions(self, graph: nx.Graph) -> Dict:
        """Get node positions based on selected layout"""
        if len(graph.nodes()) == 0:
            return {}
        
        layout = self.layout_var.get()
        
        try:
            if layout == "spring":
                return nx.spring_layout(graph, k=2, iterations=50)
            elif layout == "circular":
                return nx.circular_layout(graph)
            elif layout == "random":
                return nx.random_layout(graph)
            elif layout == "shell":
                return nx.shell_layout(graph)
            else:
                return nx.spring_layout(graph)
        except:
            # Fallback to spring layout if there's an error
            return nx.spring_layout(graph)
    
    def update_display(self):
        """Update the relationship graph display"""
        # Clear the current plot
        self.ax.clear()
        
        if not self.simulator.current_tavern or not self.simulator.current_tavern.characters:
            self.ax.set_title("Character Relationships", fontsize=14, fontweight='bold')
            self.ax.text(0.5, 0.5, "No characters in tavern", ha='center', va='center', 
                        transform=self.ax.transAxes, fontsize=12)
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.ax.axis('off')
            self.canvas.draw()
            return
        
        # Create graph from relationships
        self.graph = self.create_graph_from_relationships()
        
        if len(self.graph.nodes()) == 0:
            self.ax.set_title("Character Relationships", fontsize=14, fontweight='bold')
            self.ax.text(0.5, 0.5, "No relationships to display", ha='center', va='center', 
                        transform=self.ax.transAxes, fontsize=12)
            self.ax.set_xlim(0, 1)
            self.ax.set_ylim(0, 1)
            self.ax.axis('off')
            self.canvas.draw()
            return
        
        # Get layout positions
        pos = self.get_layout_positions(self.graph)
        
        # Prepare node colors
        node_colors = [self.get_node_color(node) for node in self.graph.nodes()]
        
        # Draw nodes
        nx.draw_networkx_nodes(self.graph, pos, 
                              node_color=node_colors,
                              node_size=self.node_size,
                              alpha=0.8,
                              ax=self.ax)
        
        # Draw edges with different colors and widths based on relationships
        for edge in self.graph.edges(data=True):
            node1, node2, data = edge
            weight = data.get('weight', 0)
            
            color = self.get_relationship_color(weight)
            width = self.get_relationship_width(weight)
            
            # Draw edge
            nx.draw_networkx_edges(self.graph, pos,
                                  edgelist=[(node1, node2)],
                                  edge_color=color,
                                  width=width,
                                  alpha=0.7,
                                  ax=self.ax)
        
        # Draw labels if enabled
        if self.show_labels_var.get():
            # Create shortened labels for better readability
            labels = {}
            for node in self.graph.nodes():
                # Use first name only or abbreviate long names
                parts = node.split()
                if len(parts) > 1:
                    labels[node] = parts[0]  # First name only
                elif len(node) > 10:
                    labels[node] = node[:8] + "..."  # Truncate long names
                else:
                    labels[node] = node
            
            nx.draw_networkx_labels(self.graph, pos,
                                   labels=labels,
                                   font_size=self.font_size,
                                   font_weight='bold',
                                   ax=self.ax)
        
        # Set title
        num_chars = len(self.simulator.current_tavern.characters)
        self.ax.set_title(f"Character Relationships ({num_chars} characters)", 
                         fontsize=14, fontweight='bold')
        
        # Remove axes
        self.ax.axis('off')
        
        # Adjust layout to prevent clipping
        self.fig.tight_layout()
        
        # Redraw canvas
        self.canvas.draw()
    
    def on_node_click(self, event):
        """Handle node click events (for future implementation)"""
        # This could be used to show detailed character information
        # when clicking on nodes in the graph
        pass
