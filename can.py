import ctypes
import v_types
from help_functions import getCommand 
from threading  import Thread
from subprocess import PIPE, Popen
from queue import Queue, Empty
import sys
BASE_16 = 16

class Can_Interface:        
    """ Can bus interface for Vector hardware """
    def __init__(self):
        """ Initializes Can bus for connected Vector hardware """
        self.vxlapi = v_types.VXlApi()
        self.g_xlPortHandle = v_types.XLportHandle(100)
        self.g_xlChannelMask = ctypes.c_ulonglong(0)

        g_xlPermissionMask = v_types.XLaccess(0)
        g_AppName = ctypes.c_char_p(b'xlCANcontrol')
        status = self.vxlapi.xlOpenDriver()
        status = self.vxlapi.xlGetErrorString(status)
        print('{:20s} {}'.format("Open Driver:",''.join(chr(i) for i in status)))
        
        appChannel       = ctypes.c_uint(0)
        XL_HWINDEX       = ctypes.c_uint(0)
        XL_HWCHANNEL     = ctypes.c_uint(0)
        # for input ctypes.c_uint, can send either ctypes.c_uint or ctypes.c_uint.value
        status = self.vxlapi.xlGetApplConfig(g_AppName, appChannel, v_types.XL_HWTYPE_VN1630, XL_HWINDEX, XL_HWCHANNEL, v_types.XL_BUS_TYPE_CAN)
        status = self.vxlapi.xlGetErrorString(status)
        print('{:20s} {}'.format("Get Appl Config:",''.join(chr(i) for i in status)))
        print('Hardware type: {:5d},\nHardware Index: {:3d}, \nHardware Channel: {:1d}'.format(v_types.XL_HWTYPE_VN1630.value, XL_HWINDEX.value, XL_HWCHANNEL.value))

        self.g_xlChannelMask = self.vxlapi.xlGetChannelMask(v_types.XL_HWTYPE_VN1630, XL_HWINDEX, XL_HWCHANNEL)
        print("Hardware Mask: {:X}".format(self.g_xlChannelMask))
        g_xlPermissionMask.value = self.g_xlChannelMask
        status = self.vxlapi.xlOpenPort(self.g_xlPortHandle, g_AppName, self.g_xlChannelMask, g_xlPermissionMask, v_types.RX_QUEUE_SIZE, v_types.XL_INTERFACE_VERSION, v_types.XL_BUS_TYPE_CAN)
        status = self.vxlapi.xlGetErrorString(status)
        print("- OpenPort  : CM=0x{:16X}, PH=0x{:2X}, PM=0x{:16X}, {:s}".format(self.g_xlChannelMask, self.g_xlPortHandle.value, g_xlPermissionMask.value, ''.join(chr(i) for i in status)))

        status = self.vxlapi.xlActivateChannel(self.g_xlPortHandle, self.g_xlChannelMask, v_types.XL_BUS_TYPE_CAN, ctypes.c_uint(8))
        status = self.vxlapi.xlGetErrorString(status)
        print('{:20s} {}'.format("Activate Channels:",''.join(chr(i) for i in status)))

        pHandle = ctypes.c_void_p()
        status = self.vxlapi.xlSetNotification(self.g_xlPortHandle, pHandle, ctypes.c_int(1))

        command = "python -u std_com_slave.py"
        self.process = Popen(command, stdin=PIPE, stdout=PIPE)
        #q = Queue()
        #_rx_listener = Thread(target=self._rx_thread, args=(self.process.stdout, q,)) 
        #_rx_listener.daemon = True
        #_rx_listener.start()

    def _rx_thread(self, out, queue):
        #xl_event = v_types.XLevent()
        #event_count = ctypes.c_uint(1)
        #while True:
        #    msg = self.vxlapi.xlReceive(self.g_xlPortHandle, event_count, xl_event)
        #   if msg != v_types.XL_ERR_QUEUE_IS_EMPTY:
        None
        #for line in iter(out.readline, b''):
        #    print(line)
        #   queue.put(line)
        #out.close()
              
                
    def send(self, command_name: str):
        """ Send message in Can bus 
            Parameters
            ----------
            command_name :
                Name of command to send
            Returns
            -------
            void
        """
        command = getCommand(command_name)
        xlEvent = v_types.XLevent()
        XL_TRANSMIT_MSG = ctypes.c_ubyte(10)
        txID = ctypes.c_uint(2)
        xlEvent.tag                 = XL_TRANSMIT_MSG
        xlEvent.tagData.msg.id      = txID
        xlEvent.tagData.msg.dlc     = 8
        xlEvent.tagData.msg.flags   = 0
        xlEvent.tagData.msg.data[0] = int(command[1], BASE_16)
        xlEvent.tagData.msg.data[1] = int(command[2], BASE_16)
        xlEvent.tagData.msg.data[2] = int(command[3], BASE_16)
        xlEvent.tagData.msg.data[3] = int(command[4], BASE_16)
        xlEvent.tagData.msg.data[4] = int(command[5], BASE_16)
        xlEvent.tagData.msg.data[5] = int(command[6], BASE_16)
        xlEvent.tagData.msg.data[6] = int(command[7], BASE_16)
        xlEvent.tagData.msg.data[7] = int(command[8], BASE_16)

        messageCount = ctypes.c_uint(1)

        status = self.vxlapi.xlCanTransmit(self.g_xlPortHandle, self.g_xlChannelMask, messageCount, ctypes.byref(xlEvent))
        status = self.vxlapi.xlGetErrorString(status)
        message = command = "{:s} {:s} {:s} {:s} {:s} {:s} {:s} {:s}".format(command[1], command[2], command[3], command[4], command[5], command[6], command[7], command[8])
        print('{:s} {}, Status: {}'.format("Sent message:", message,''.join(chr(i) for i in status)))
        out, err = self.process.communicate(input=b'Message sent', timeout=15)
        print(out, err)