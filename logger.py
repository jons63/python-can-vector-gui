import sys
import logging
import tkinter as tk
import can

class guiLogger(can.Listener):
    """ Create a can.Listener which outputs to a tkinter text widget
        ----------
        name :
            Name of command to get
        Returns 
        -------
        List with command name and data bytes 
    """
    def __init__(self, window: tk.Text):
        self.window = window
    
    def on_message_received(self, msg):
        self.window.config(state=tk.NORMAL)
        self.window.insert(tk.END, str(msg) + '\n')
        self.window.config(state=tk.DISABLED)