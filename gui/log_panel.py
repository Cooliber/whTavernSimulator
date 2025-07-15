"""
Log panel for the Warhammer Fantasy Tavern Simulator
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ..core.tavern_simulator import TavernSimulator

class LogPanel:
    """Panel for displaying and managing session logs"""
    
    def __init__(self, parent: tk.Widget, simulator: TavernSimulator):
        self.parent = parent
        self.simulator = simulator
        
        self.create_widgets()
    
    def create_widgets(self):
        """Create all widgets for the log panel"""
        # Main frame
        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        # Title and controls
        header_frame = ttk.Frame(self.frame)
        header_frame.pack(fill=tk.X, padx=5, pady=5)
        
        ttk.Label(header_frame, text="Session Log", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        
        # Control buttons
        button_frame = ttk.Frame(header_frame)
        button_frame.pack(side=tk.RIGHT)
        
        ttk.Button(button_frame, text="Clear Log", 
                  command=self.clear_log).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Export Log", 
                  command=self.export_log).pack(side=tk.LEFT, padx=2)
        ttk.Button(button_frame, text="Refresh", 
                  command=self.update_display).pack(side=tk.LEFT, padx=2)
        
        # Filter frame
        filter_frame = ttk.Frame(self.frame)
        filter_frame.pack(fill=tk.X, padx=5, pady=2)
        
        ttk.Label(filter_frame, text="Filter:").pack(side=tk.LEFT)
        
        self.filter_var = tk.StringVar()
        filter_entry = ttk.Entry(filter_frame, textvariable=self.filter_var, width=30)
        filter_entry.pack(side=tk.LEFT, padx=(5, 0))
        filter_entry.bind('<KeyRelease>', self.on_filter_change)
        
        ttk.Button(filter_frame, text="Clear Filter", 
                  command=self.clear_filter).pack(side=tk.LEFT, padx=5)
        
        # Auto-scroll checkbox
        self.auto_scroll_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(filter_frame, text="Auto-scroll", 
                       variable=self.auto_scroll_var).pack(side=tk.RIGHT)
        
        # Log display
        log_frame = ttk.Frame(self.frame)
        log_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Create text widget with scrollbar
        self.log_text = tk.Text(log_frame, wrap=tk.WORD, font=("Consolas", 9))
        log_scrollbar = ttk.Scrollbar(log_frame, orient=tk.VERTICAL, 
                                     command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Configure text tags for different log levels
        self.log_text.tag_configure("event", foreground="blue")
        self.log_text.tag_configure("interaction", foreground="green")
        self.log_text.tag_configure("error", foreground="red")
        self.log_text.tag_configure("warning", foreground="orange")
        self.log_text.tag_configure("rumor", foreground="purple")
        self.log_text.tag_configure("turn", foreground="darkblue", font=("Consolas", 9, "bold"))
        
        # Statistics frame
        stats_frame = ttk.LabelFrame(self.frame, text="Session Statistics")
        stats_frame.pack(fill=tk.X, padx=5, pady=5)
        
        stats_content = ttk.Frame(stats_frame)
        stats_content.pack(fill=tk.X, padx=5, pady=5)
        
        # Statistics labels
        self.total_events_var = tk.StringVar(value="Events: 0")
        self.total_interactions_var = tk.StringVar(value="Interactions: 0")
        self.total_turns_var = tk.StringVar(value="Turns: 0")
        self.session_time_var = tk.StringVar(value="Session Time: 0:00")
        
        ttk.Label(stats_content, textvariable=self.total_events_var).grid(row=0, column=0, sticky=tk.W, padx=5)
        ttk.Label(stats_content, textvariable=self.total_interactions_var).grid(row=0, column=1, sticky=tk.W, padx=5)
        ttk.Label(stats_content, textvariable=self.total_turns_var).grid(row=1, column=0, sticky=tk.W, padx=5)
        ttk.Label(stats_content, textvariable=self.session_time_var).grid(row=1, column=1, sticky=tk.W, padx=5)
    
    def clear_log(self):
        """Clear the session log"""
        result = messagebox.askyesno("Clear Log", 
                                   "Are you sure you want to clear the session log? This cannot be undone.")
        if result:
            self.simulator.session_log.clear()
            self.update_display()
    
    def export_log(self):
        """Export the session log to a file"""
        try:
            filename = filedialog.asksaveasfilename(
                defaultextension=".txt",
                filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                title="Export Session Log"
            )
            if filename:
                exported_file = self.simulator.export_session_log(filename)
                messagebox.showinfo("Export Complete", f"Log exported to {exported_file}")
        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export log: {str(e)}")
    
    def clear_filter(self):
        """Clear the log filter"""
        self.filter_var.set("")
        self.update_display()
    
    def on_filter_change(self, event):
        """Handle filter text change"""
        self.update_display()
    
    def get_log_tag(self, log_entry: str) -> str:
        """Determine the appropriate tag for a log entry"""
        entry_lower = log_entry.lower()
        
        if "turn" in entry_lower and "completed" in entry_lower:
            return "turn"
        elif "interaction:" in entry_lower:
            return "interaction"
        elif "event:" in entry_lower:
            return "event"
        elif "rumor" in entry_lower:
            return "rumor"
        elif "error" in entry_lower:
            return "error"
        elif "warning" in entry_lower or "failed" in entry_lower:
            return "warning"
        else:
            return ""
    
    def update_display(self):
        """Update the log display"""
        # Clear current display
        self.log_text.delete(1.0, tk.END)
        
        # Get filter text
        filter_text = self.filter_var.get().lower()
        
        # Display filtered log entries
        for entry in self.simulator.session_log:
            if not filter_text or filter_text in entry.lower():
                tag = self.get_log_tag(entry)
                self.log_text.insert(tk.END, entry + "\n", tag)
        
        # Auto-scroll to bottom if enabled
        if self.auto_scroll_var.get():
            self.log_text.see(tk.END)
        
        # Update statistics
        self.update_statistics()
    
    def update_statistics(self):
        """Update session statistics"""
        # Count different types of events
        event_count = sum(1 for entry in self.simulator.session_log if "event:" in entry.lower())
        interaction_count = len(self.simulator.interaction_history)
        turn_count = self.simulator.turn_counter
        
        # Calculate session time
        from datetime import datetime
        session_duration = datetime.now() - self.simulator.session_start_time
        hours, remainder = divmod(int(session_duration.total_seconds()), 3600)
        minutes, _ = divmod(remainder, 60)
        
        # Update labels
        self.total_events_var.set(f"Events: {event_count}")
        self.total_interactions_var.set(f"Interactions: {interaction_count}")
        self.total_turns_var.set(f"Turns: {turn_count}")
        self.session_time_var.set(f"Session Time: {hours}:{minutes:02d}")
    
    def add_log_entry(self, entry: str, tag: str = ""):
        """Add a new log entry (for real-time updates)"""
        filter_text = self.filter_var.get().lower()
        
        if not filter_text or filter_text in entry.lower():
            if not tag:
                tag = self.get_log_tag(entry)
            
            self.log_text.insert(tk.END, entry + "\n", tag)
            
            # Auto-scroll if enabled
            if self.auto_scroll_var.get():
                self.log_text.see(tk.END)
        
        # Update statistics
        self.update_statistics()
