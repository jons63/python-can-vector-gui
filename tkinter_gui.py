import sys
import os
#import time
#import platform
import csv
import re
import argparse

import tkinter as tk
from tkinter import ttk
from logger import GuiLogger
from help_functions import getCommand
import can
import serial

CAN_MESSAGE_DATABASE    = 'data.csv'
SERIAL_MESSAGE_DATABASE = 'serial.csv'

class LogPage(ttk.Frame):
    """ Displays a log of can messages """
    def __hide_window_log(self, tab_widget: ttk.Notebook):
        """ Close log window and show log tab instead
        Parameters
        ----------
        tab_widget :
            tk.Notebook widget
        Returns
        -------
        void
        """
        self.__window_log.withdraw()
        tab_widget.add(self)

    def __show_window_log(self, tab_widget: ttk.Notebook):
        """ Open log window and hide log tab
        Parameters
        ----------
        tab_widget :
            tk.Notebook widget
        Returns
        -------
        void
        """
        self.__window_log.deiconify()
        tab_widget.hide(self)

    def __init__(self, parent: ttk.Notebook, bus: can.Bus):
        """ Creates a frame containing a text widget that displays incoming can messages
        Parameters
        ----------
        parent :
            Parent widget
        bus :
            Can bus to listen for messages on
        """
        super().__init__(parent.root)
        self.name = "Log Page"
        self.__tab_log = GuiLogger(self)
        self.__window_log = tk.Toplevel(parent.root)
        self.__window_log.withdraw()
        self.__window_log.protocol("WM_DELETE_WINDOW", lambda: self.__hide_window_log(parent.root))
        window_log = GuiLogger(self.__window_log)
        can.Notifier(bus, [self.__tab_log, window_log])


        style = ttk.Style()
        style.configure("Send.TButton", foreground="green", background="white")
        style.configure("Delete.TButton", foreground="red", background="white")
        popout_button = ttk.Button(self, text="Popout log", style="Send.TButton", command= lambda: self.__show_window_log(parent.root))

        # Place all elements
        self.__tab_log.grid(sticky="NSEW")
        tk.Grid.columnconfigure(self, self.__tab_log, weight=1)
        tk.Grid.rowconfigure(self, self.__tab_log, weight=1)

        window_log.grid(sticky="NSEW")
        tk.Grid.columnconfigure(self.__window_log, window_log, weight=1)
        tk.Grid.rowconfigure(self.__window_log, window_log, weight=1)

        popout_button.grid(row="1", padx=30,pady=30)

class Input_Field(tk.Entry):
    """ Field for user to input data """
    def character_limit(self, length: int):
        """ Remove last written character from filed if max number of character are already written
            Parameters
            ----------
            length :
                Max length of input string for filed
            Returns
            -------
            void
        """
        if len(self.text.get()) > length:
            self.text.set(self.text.get()[:length])

    def __init__(self, parent, width: int = 20):
        """ Input_Filed class init function
            Parameters
            ----------
            parent :
                Frame to put element in
            width :
                Width of input field
            Returns
            -------
            Input_Field object
        """
        self.text = tk.StringVar()
        self.text.trace("w", lambda *args: self.character_limit(width-1))
        super().__init__(parent, width=str(width), textvariable=self.text, relief="raised", bg="#e6e6e6")

class Message_Page(ttk.Frame):
    """ View to add/remove and send messages """
    def switch_com(self):
        """ Switch message page to show active com messages.
            Parameters
            ----------
            None
            Returns
            -------
            void
        """
        self.listbox.delete(first=0, last=tk.END)
        with open(self.active_com.get(), newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                self.listbox.insert(tk.END, row[0])

    def add_entry(self, event):
        """ Add new message
            Parameters
            ----------
            event :
                tk event
            Returns
            -------
            void
        """
        command = self.command_name.text.get()
        command_bytes = ""

        command_bytes = "{:s},{:s},{:s},{:s},{:s},{:s},{:s},{:s}".format(
            self.hex0.text.get(), self.hex1.text.get(), self.hex2.text.get(), self.hex3.text.get(),
            self.hex4.text.get(), self.hex5.text.get(), self.hex6.text.get(), self.hex7.text.get()).upper()
        match = re.search("^([0-9A-F]{2}.*){8}$", command_bytes)
        print(command_bytes)
        if match != None:
            command += "," + command_bytes
            command = command.split(sep=",")
            with open(self.active_com.get(), 'a+', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(command)
                self.listbox.insert(tk.END, command[0])

    def delete_entry(self, event: tk.Event, text: str):
        """ Remove message
            Parameters
            ----------
            event :
                tk event
            text :
                Name of message to remove
            Returns
            -------
            void
        """
        if self.listbox.curselection():
            file_lines = list()
            with open(self.active_com.get(), newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    name = row[0]
                    if text != name:
                        file_lines.append(row)
            with open(self.active_com.get(), 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerows(file_lines)
                self.listbox.delete(tk.ACTIVE)

    def updateStatus(self, event: tk.Event):
        """ Update message information window
            Parameters
            ----------
            event :
                tk event
            Returns
            -------
            void
        """
        if self.listbox.curselection():
            name = self.listbox.get(self.listbox.curselection()[0])
            command = getCommand(name, self.active_com.get())
            command = "{:s} {:s} {:s} {:s} {:s} {:s} {:s} {:s}".format(command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8])
            self.information_text.insert(tk.END, "Message content\n")
            self.information_text.insert(tk.END, command + "\n")

    def send_can_message(self, command_name: str):
        """ Send message on Can bus
            Parameters
            ----------
            command_name :
                Name of command to send
            Returns
            -------
            void
        """
        command = getCommand(command_name, self.active_com.get())
        message = can.Message(arbitration_id=123, data=[int(x, 16) for x in command[1:]])
        self.bus.send(message, timeout=0.2)

    def send_serial_message(self, command_name: str):
        """ Send message on serial bus
            Parameters
            ----------
            command_name :
                Name of command to send
            Returns
            -------
            void
        """
        command = getCommand(command_name, self.active_com.get())
        bytes_to_send = bytes('$DS0B90\n', 'utf-8')
        print(bytes_to_send)
        bus = serial.Serial('COM10', 100000, timeout=2)
        bus.write(bytes_to_send)
        print(bus.readline())
        bus.close()

    def tp_send_message(self, command_name: str):
        """ Redirect message to currently active com
            Parameters
            ----------
            command_name :
                Name of command to send
            Returns
            -------
            void
        """
        if self.active_com.get() == CAN_MESSAGE_DATABASE:
            self.send_can_message(command_name)
        else:
            self.send_serial_message(command_name)

    def __init__(self, parent, bus):
        """ Message_Page init function
            Parameters
            ----------
            parent :
                Toplevel object
            Returns
            -------
            Message_Page
                Message_Page object
        """
        super().__init__(parent.root)
        self.name = "Messages"
        self.bus = bus
        coms = (CAN_MESSAGE_DATABASE, SERIAL_MESSAGE_DATABASE)
        signal_entry_frame = tk.Frame(self)
        signal_information_frame = tk.Frame(self)
        hex_entry_frame = tk.Frame(signal_entry_frame)

        self.listbox = tk.Listbox(signal_entry_frame)
        self.listbox.bind('<<ListboxSelect>>', self.updateStatus)
        for com in coms:
            if not os.path.isfile(com):
                with open(com, 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Empty message','00','00','00','00','00','00','00','00'])

        with open(CAN_MESSAGE_DATABASE, 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                print(row)
                self.listbox.insert(tk.END, row[0])

        self.command_name = Input_Field(hex_entry_frame, width=20)
        self.command_name.text.set("Enter Name")
        self.hex0 = Input_Field(hex_entry_frame, width=3)
        self.hex1 = Input_Field(hex_entry_frame, width=3)
        self.hex2 = Input_Field(hex_entry_frame, width=3)
        self.hex3 = Input_Field(hex_entry_frame, width=3)
        self.hex4 = Input_Field(hex_entry_frame, width=3)
        self.hex5 = Input_Field(hex_entry_frame, width=3)
        self.hex6 = Input_Field(hex_entry_frame, width=3)
        self.hex7 = Input_Field(hex_entry_frame, width=3)

        add_signal_button = ttk.Button(hex_entry_frame, text='Add', style="Send.TButton")
        add_signal_button['command'] = lambda: self.add_entry(None)

        remove_signal_button = ttk.Button(signal_entry_frame, text='Remove', style="Delete.TButton")
        remove_signal_button['command'] = lambda: self.delete_entry(None, self.listbox.get(tk.ACTIVE))

        self.information_text = tk.Text(signal_information_frame)

        send_button = ttk.Button(signal_information_frame, text="Send", style="Send.TButton")
        send_button['command'] = lambda: self.tp_send_message(self.listbox.get(tk.ACTIVE))
        # Place all elements
        #signal_entry.grid(row="0", column="0")

        self.command_name.grid(columnspan="8", sticky="w e", pady=(0,5))
        self.hex0.grid(row="1", column="0")
        self.hex1.grid(row="1", column="1")
        self.hex2.grid(row="1", column="2")
        self.hex3.grid(row="1", column="3")
        self.hex4.grid(row="1", column="4")
        self.hex5.grid(row="1", column="5")
        self.hex6.grid(row="1", column="6")
        self.hex7.grid(row="1", column="7")
        add_signal_button.grid(row="0", column="8", rowspan="2", sticky="n s", padx=(5,0))
        hex_entry_frame.grid(row="0", column="1")
        signal_entry_frame.grid(sticky="n s w", pady=(5,0), padx=(5,0))

        self.listbox.grid(row="2", column="0", columnspan="4", sticky="e w")
        remove_signal_button.grid(row="3", columnspan="4")

        self.information_text.grid()
        send_button.grid(row="1")
        signal_information_frame.grid(row="0", column="1", padx=(5,0))

        self.active_com = tk.StringVar(value=CAN_MESSAGE_DATABASE)
        com_type = tk.Menu(parent.menu, tearoff=0)
        com_type.add_radiobutton(label='Can', variable=self.active_com, value=CAN_MESSAGE_DATABASE, command=self.switch_com)
        com_type.add_radiobutton(label='Serial', variable=self.active_com, value=SERIAL_MESSAGE_DATABASE, command=self.switch_com)
        parent.menu.add_cascade(label='Com', menu=com_type)

class Download_page(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent.root)
        self.name = "Download"
        ttk.Label(self, text="This is the third page").grid(column=0, row=0,padx=30,pady=30)

def parse_args(args):
    # Parse command line arguments
    parser = argparse.ArgumentParser('python tkinter_gui.py',
                                     description='A simple gui for sending/receiveing can message with vector hardware',
                                      )

    parser.add_argument('-r', '--receive_own_messages',
                            help=   'The bus will receive its own outgoing messages. '
                                    '\n For development purposes.',
                            action='store_true')

    parsed_args = parser.parse_args(args)

    return parsed_args

class App:
    """ Top level class for gui """
    def __init__(self):
        """ App init function
            Parameters
            ----------
            None
            Returns
            -------
            App
                App object
        """
        root = tk.Tk()
        self.root = ttk.Notebook(root)
        self.menu = tk.Menu(root)
        self.tabs = ()
        root.config(menu=self.menu)

    def add_tabs(self, tabs):
        [self.root.add(tab, text=tab.name) for tab in tabs]

def main():
    parsed_args = parse_args(sys.argv[1:])
    bus = can.Bus(interface='vector', app_name="xlCANcontrol", channel=0, receive_own_messages=parsed_args.receive_own_messages)
    app = App()
    tabs = (LogPage(app, bus), Message_Page(app, bus), Download_page(app))
    app.add_tabs(tabs)

    app.root.pack(fill="both", expand="True")

    app.root.mainloop()

if __name__== "__main__":
    main()