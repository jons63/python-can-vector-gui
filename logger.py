import sys
import logging
import tkinter as tk
import can

class GuiLogger(tk.Frame, can.Listener):
    """ Combines a can.Listener with a tk.Text widget to create a log object
        ----------
        parent :
            parent container to pace object in
        Returns 
        -------
        List with command name and data bytes 
    """
    def __init__(self, parent: tk.Frame):
        super().__init__(parent)
        self.text_widget = tk.Text(self)
        self.text_widget.grid(sticky="NSEW")
        tk.Grid.columnconfigure(self, self.text_widget, weight=1)
        tk.Grid.rowconfigure(self, self.text_widget, weight=1)
        self.text_widget.config(state=tk.DISABLED)
    
    def on_message_received(self, msg):
        self.text_widget.config(state=tk.NORMAL)
        self.text_widget.insert(tk.END, str(msg) + '\n')
        self.text_widget.config(state=tk.DISABLED)