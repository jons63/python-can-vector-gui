# Python 3 wrapper for flashing an ECU with vFlash
# THIS CODE IS PROVIDED AS EXAMPLE ONLY!
# VECTOR IS NOT LIABLE FOR ANY DAMAGE CAUSED BY USING IT.

import ctypes
import sys
import os
import time
import platform

from ctypes import POINTER
from ctypes.wintypes import HANDLE

# Define types used for the callbacks
PROGRESSFUNC = ctypes.WINFUNCTYPE(None, ctypes.c_int, ctypes.c_int)
STATUSFUNC = ctypes.WINFUNCTYPE(None, ctypes.c_uint)

class vFlash:
    def __init__(self):
        self.CurrentProgress = 0
        self.Remaining = 99999
        self.FlashResult = -1

        self.Dll = None
        arch='' # no postfix for 32bit
        if platform.architecture()[0] == '64bit':
            arch='64'
        for path in os.environ['PATH'].split(';'):
            dllPath = path + 'vFlashAutomation' + arch + '.dll'
            if os.path.isfile(dllPath):
                self.Dll = ctypes.cdll.LoadLibrary(dllPath)
                if self.Dll != None:
                    break

        if self.Dll is None:
            raise FileNotFoundError("vFlashAutomation DLL not found!")

        initres = self.Dll.vFlashInitialize()
        if initres != 0:
            raise AssertionError("vFlashInitialize failed!")

        # the callback objects must exist while the flashing goes on!
        self.ProgressCB = PROGRESSFUNC(self.Progress)
        self.StatusCB = STATUSFUNC(self.Status)

    def __del__(self):
        if self.Dll != None:
            self.Dll.vFlashDeinitialize()

    # This callback function will be called during flashing
    def Progress(self, progressInPercent, remainingInS):
        self.CurrentProgress = progressInPercent
        self.Remaining = remainingInS

    # When the flashing is done, this callback is called with the final status
    # the main application can check for the value to stop waiting when the status is set
    def Status(self, flashStatus):
        self.FlashResult = flashStatus

    # Try to load a .vflashpack, returns project handle or <0 for error
    def Load(self, pathToPack):
        if self.Dll is None:
            return -1

        if not os.path.isfile(pathToPack):
            return -2

        LoadProject = self.Dll.vFlashLoadProject
        LoadProject.argtypes = [ctypes.c_char_p, POINTER(ctypes.c_int)]
        prjHandle = ctypes.c_int()
        # the C API does not accept wide char string, so convert path first
        prores = LoadProject(pathToPack.encode('utf-8'), ctypes.byref(prjHandle))
        return prores

    def Unload(self, projectHandle):
        UnloadProject = self.Dll.vFlashUnloadProject
        UnloadProject.argtypes = [ctypes.c_int]
        return UnloadProject(projectHandle)

    # Start flashing one of the loaded projects
    def Start(self, projectHandle):
        if self.Flashing():
            return -2 # already flashing!

        StartFlashing = self.Dll.vFlashStart
        StartFlashing.argtypes = [ctypes.c_int, PROGRESSFUNC, STATUSFUNC]
        prores = StartFlashing(projectHandle, self.ProgressCB, self.StatusCB)
        if prores != 0:
            return -1
        self.FlashResult = -2
        self.CurrentProgress = 0
        self.Remaining = 99999
        return prores

    def GetProgress(self):
        return self.CurrentProgress

    def GetRemaining(self):
        return self.Remaining

    # returns -1 for not set, -2 for flashing, >= 0 for the resulting status
    def GetResult(self):
        return self.FlashResult

    def Flashing(self):
        return self.FlashResult == -2
    
    # Simple flash function that prints the progress as text
    def DoFlashWithProgress(self, handle, pollInterval=0.5):
        self.Start(handle)

        # Poll the status - the callback will set the variable
        while self.Flashing():
            progress = self.GetProgress()
            full= '#' * int(progress * 40 / 100)
            empty='.' * (40 - len(full))
            print('\r[' + full + empty + '] ' + str(progress) + '% ' \
                  + str(self.GetRemaining()) + 's left     ', end='', flush=True)
            time.sleep(pollInterval)
        print('')
        print('Flash result = ' + str(self.GetResult()))

        
# Executed when called as argument to the python interpreter directly
if __name__== "__main__":
    if len(sys.argv) < 2:
        print('Usage: ' + sys.argv[0] + ' path/to/project.vflashpack')
        sys.exit()

    # load and init the DLL
    flasher = vFlash() # throws exception if init fails
    handle = flasher.Load(sys.argv[1])
    if 0 > handle:
        print('Error ' + str(handle) + ' loading project file ' + sys.argv[1])
        sys.exit()

    print('Project handle = ' + str(handle))

    flasher.DoFlashWithProgress(handle)

    # Clean up
    flasher.Unload(handle)
 