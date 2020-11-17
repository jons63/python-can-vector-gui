# Python 3 wrapper for flashing an ECU with vFlash
# THIS CODE IS PROVIDED AS EXAMPLE ONLY!
# VECTOR IS NOT LIABLE FOR ANY DAMAGE CAUSED BY USING IT.

import tkinter as tk
import tkinter_gui

if __name__== "__main__":
    root = tk.Tk()
    app = tkinter_gui.Application(master=root)
    #print = app.logger.info <- NOTE FIX THIS. Should point to app.tabControl.first_page.logger.info Find way to access first_page
    app.mainloop()