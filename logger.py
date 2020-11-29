import sys
import logging
import tkinter as tk
import can

class Gui_Streamer(logging.Handler):
    """ Streams data from logger to be visualized in gui """
    def __init__(self, stream, tkText):
        """ Gui_Streamer init function
            Parameters
            ----------
            stream :
                Data stream to listen to
            tkText :
                Tkinter text widget to output data to
            Returns
            -------
            Gui_Streamer
                Gui_Streamer object
        """
        super().__init__(level=logging.DEBUG)
        self.tkText = tkText
        self.setLevel(logging.DEBUG)
        self.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    def emit(self, record):
        """ Callback function when new data is available on stream
            Parameters
            ----------
            record :
                Stream data
            Returns
            -------
            void
        """ 
        msg = self.format(record)
        self.tkText.config(state=tk.NORMAL)
        self.tkText.insert(tk.END, msg + '\n')
        self.tkText.config(state=tk.DISABLED)

class Logger(logging.Logger):
    """ logging.logger with initialization """
    def __init__(self, master='Logger'):
        """ Logger init function 
            Parameters
            ----------
            master :
                Name of logger
            Returns
            -------
            Logger
                Logger object
        """
        super().__init__(master)
        self.master = master
        self.setLevel(logging.DEBUG)
        handler = logging.StreamHandler(sys.stdout)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.addHandler(handler)

        handler = logging.FileHandler(filename='output.log')
        handler.setFormatter(formatter)
        self.addHandler(handler)

class guiLogger(can.Listener):
    def __init__(self, window: tk.Text):
        self.window = window
    
    def on_message_received(self, msg):
        self.window.config(state=tk.NORMAL)
        self.window.insert(tk.END, str(msg) + '\n')
        self.window.config(state=tk.DISABLED)