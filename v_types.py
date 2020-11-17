import ctypes
import platform
from enum import IntEnum


XLportHandle = ctypes.c_long
XLaccess     = ctypes.c_uint64
XLstatus     = ctypes.c_short
XLstringType = ctypes.c_char_p
XLhandle     = ctypes.c_void_p
XLuint64     = ctypes.c_int64

RX_QUEUE_SIZE = ctypes.c_uint(4096)
XL_INTERFACE_VERSION = ctypes.c_uint(3)
XL_BUS_TYPE_CAN = ctypes.c_uint(1)
    # Is there a way to create a enum type that hold ctypes values?

XL_HWTYPE_CANCASEXL = ctypes.c_uint(21)
XL_HWTYPE_VN1630    = ctypes.c_uint(57)


XL_SUCCESS                      = 0
XL_PENDING                      = 1
XL_ERR_QUEUE_IS_EMPTY           = 10 
XL_ERR_QUEUE_IS_FULL            = 11 
XL_ERR_TX_NOT_POSSIBLE          = 12 
XL_ERR_NO_LICENSE               = 14 
XL_ERR_WRONG_PARAMETER          = 101
XL_ERR_TWICE_REGISTER           = 110
XL_ERR_INVALID_CHAN_INDEX       = 111
XL_ERR_INVALID_ACCESS           = 112
XL_ERR_PORT_IS_OFFLINE          = 113
XL_ERR_CHAN_IS_ONLINE           = 116
XL_ERR_NOT_IMPLEMENTED          = 117
XL_ERR_INVALID_PORT             = 118
XL_ERR_HW_NOT_READY             = 120
XL_ERR_CMD_TIMEOUT              = 121
XL_ERR_CMD_HANDLING             = 122
XL_ERR_HW_NOT_PRESENT           = 129
XL_ERR_NOTIFY_ALREADY_ACTIVE    = 131
XL_ERR_INVALID_TAG              = 132
XL_ERR_INVALID_RESERVED_FLD     = 133
XL_ERR_INVALID_SIZE             = 134
XL_ERR_INSUFFICIENT_BUFFER      = 135
XL_ERR_ERROR_CRC                = 136
XL_ERR_BAD_EXE_FORMAT           = 137
XL_ERR_NO_SYSTEM_RESOURCES      = 138
XL_ERR_NOT_FOUND                = 139
XL_ERR_INVALID_ADDRESS          = 140
XL_ERR_REQ_NOT_ACCEP            = 141
XL_ERR_INVALID_LEVEL            = 142
XL_ERR_NO_DATA_DETECTED         = 143
XL_ERR_INTERNAL_ERROR           = 144
XL_ERR_UNEXP_NET_ERR            = 145
XL_ERR_INVALID_USER_BUFFER      = 146
XL_ERR_INVALID_PORT_ACCESS_TYPE = 147
XL_ERR_NO_RESOURCES             = 152
XL_ERR_WRONG_CHIP_TYPE          = 153
XL_ERR_WRONG_COMMAND            = 154
XL_ERR_INVALID_HANDLE           = 155
XL_ERR_RESERVED_NOT_ZERO        = 157
XL_ERR_INIT_ACCESS_MISSING      = 158
XL_ERR_WRONG_VERSION            = 160
XL_ERR_CANNOT_OPEN_DRIVER       = 201
XL_ERR_WRONG_BUS_TYPE           = 202
XL_ERR_DLL_NOT_FOUND            = 203
XL_ERR_INVALID_CHANNEL_MASK     = 204
XL_ERR_NOT_SUPPORTED            = 205
# special stream defines
XL_ERR_CONNECTION_BROKEN        = 210 
XL_ERR_CONNECTION_CLOSED        = 211 
XL_ERR_INVALID_STREAM_NAME      = 212 
XL_ERR_CONNECTION_FAILED        = 213 
XL_ERR_STREAM_NOT_FOUND         = 214 
XL_ERR_STREAM_NOT_CONNECTED     = 215 
XL_ERR_QUEUE_OVERRUN            = 216 
XL_ERROR                        = 255 

class Can(ctypes.Structure):
    _fields_=[
    ("bitRate", ctypes.c_uint),
    ("tseg1", ctypes.c_ubyte),
    ("tseg2", ctypes.c_ubyte),
    ("sam", ctypes.c_ubyte),
    ("outputMode", ctypes.c_ubyte),
    ("reserved1", ctypes.c_ubyte*7),
    ("canOpMode", ctypes.c_ubyte)
]

class CanFD(ctypes.Structure):
    _fields_=[
    ("arbitrationBitRate", ctypes.c_uint),
    ("sjwAbr", ctypes.c_ubyte),
    ("tseg1Abr", ctypes.c_ubyte),
    ("tseg2Abr", ctypes.c_ubyte),
    ("samAbr", ctypes.c_ubyte),
    ("outputMode", ctypes.c_ubyte),
    ("sjwDbr", ctypes.c_ubyte),
    ("tseg1Dbr", ctypes.c_ubyte),
    ("tseg2Dbr", ctypes.c_ubyte),
    ("dataBitRate", ctypes.c_uint),
    ("canOpMode", ctypes.c_ubyte)
]

class Most(ctypes.Structure):
    _fields_=[
    ("activeSpeedGrade", ctypes.c_uint),
    ("compatibleSpeedGrade", ctypes.c_uint),
    ("inicFwVersion", ctypes.c_uint),
]

class Flexray(ctypes.Structure):
    _fields_=[
    ("status", ctypes.c_uint),
    ("cfgMode", ctypes.c_uint),
    ("baudrate", ctypes.c_uint)]

class Ethernet(ctypes.Structure):
    _fields_=[
    ("macAddr", ctypes.c_ubyte*6),
    ("connector", ctypes.c_ubyte),
    ("phy", ctypes.c_ubyte),
    ("link", ctypes.c_ubyte),
    ("speed", ctypes.c_ubyte),
    ("clockMode", ctypes.c_ubyte),
    ("bypass", ctypes.c_ubyte)
]

class Can_Tx(ctypes.Structure):
    _fields_=[
        ("bitrate", ctypes.c_uint),
        ("parity", ctypes.c_uint),
        ("minGap", ctypes.c_uint)
    ]

class Can_Rx(ctypes.Structure):
    _fields_=[
        ("bitrate", ctypes.c_uint),
        ("minBitrate", ctypes.c_uint),
        ("maxBitrate", ctypes.c_uint),
        ("parity", ctypes.c_uint),
        ("minGap", ctypes.c_uint),
        ("autoBaudrate", ctypes.c_uint),
    ]

class Can_Direction(ctypes.Union):
    _fields_=[
        ("tx", Can_Tx),
        ("rx", Can_Rx),
        ("raw", ctypes.c_ubyte*24)
    ]

class A429(ctypes.Structure):
    _fields_=[
    ("channelDirection", ctypes.c_ushort),
    ("res1", ctypes.c_ushort),
    ("dir", Can_Direction)
]

class Can_Data(ctypes.Union):
    _fields_=[
        ("can", Can),
        ("canFD", CanFD),
        ("most", Most),
        ("flexray", Flexray),
        ("ethernet", Ethernet),
        ("a429", A429),
        ("raw", ctypes.c_ubyte*28)
    ]

class XLbusParams(ctypes.Structure):
    _fields_=[
    ("busType", ctypes.c_uint),
    ("data", Can_Data)
    ]

class XLchannelConfig(ctypes.Structure):
    _fields_=[
    ("name", ctypes.c_char*32),
    ("hwType", ctypes.c_ubyte),
    ("hwIndex", ctypes.c_ubyte),
    ("hwChannel", ctypes.c_ubyte),
    ("transceiverType", ctypes.c_ushort),
    ("transceiverState", ctypes.c_ushort),
    ("configError", ctypes.c_ushort),
    ("channelIndex", ctypes.c_ubyte),
    ("channelMask", XLuint64),
    ("channelCapabilities", ctypes.c_uint),
    ("channelBusCapabilities", ctypes.c_uint),

    ("isOnBus", ctypes.c_ubyte),
    ("connectedBusType", ctypes.c_uint),
    ("busParams", XLbusParams),
    ("_doNotUse", ctypes.c_uint),

    ("driverVersion", ctypes.c_uint),
    ("interfaceVersion", ctypes.c_uint),
    ("raw_data", ctypes.c_uint*10),

    ("serialNumber", ctypes.c_uint),
    ("articleNumber", ctypes.c_uint),

    ("transceiverName", ctypes.c_char*32),

    ("specialCabFlags", ctypes.c_int),
    ("dominantTimeout", ctypes.c_int),
    ("dominantRecessiveDelay", ctypes.c_ubyte),
    ("recessiveDominantDelay", ctypes.c_ubyte),
    ("connectionInfo", ctypes.c_ubyte),
    ("currentlyAvailableTimestamps", ctypes.c_ubyte),
    ("minimalSupplyVoltage", ctypes.c_ushort),
    ("maximalSupplyVoltage", ctypes.c_ushort),
    ("maximalBaudrate", ctypes.c_uint),
    ("fpgaCoreCapabilities", ctypes.c_ubyte),
    ("specialDeviceStatus", ctypes.c_ubyte),
    ("channelBusActiveCapabilities", ctypes.c_ushort),
    ("breakOffset", ctypes.c_ushort),
    ("delimiterOffset", ctypes.c_ushort),
    ("reserved", ctypes.c_uint*3)
    ]

class XLdriverConfig(ctypes.Structure):
    _fields_=[
        ("dllVersion", ctypes.c_uint),
        ("channelCount", ctypes.c_uint),
        ("reserved", ctypes.c_uint*10),
        ("channel", XLchannelConfig*64)
        ]

class s_xl_can_msg(ctypes.Structure):
    _fields_=[
        ("id", ctypes.c_uint),
        ("flags", ctypes.c_ushort),
        ("dlc", ctypes.c_ushort),
        ("res1", ctypes.c_ulonglong),
        ("data", ctypes.c_ubyte*8),
        ("res2", ctypes.c_ulonglong)
    ]

class s_xl_chip_state(ctypes.Structure):
    _fields_=[
        ("busStatus", ctypes.c_ubyte),
        ("txErrorCounter", ctypes.c_ubyte),
        ("rxErrorCounter", ctypes.c_ubyte),
    ]

# Unfinished data struct, will probably work with CAN
class s_xl_tag_data(ctypes.Union):
    _fields_=[
        ("msg", s_xl_can_msg),
        ("chipState", s_xl_chip_state)
    ]

class XLevent(ctypes.Structure):
    _fields_=[
        ("tag", ctypes.c_ubyte),
        ("chanIndex", ctypes.c_ubyte),
        ("transId", ctypes.c_ushort),
        ("portHandle", ctypes.c_ushort),
        ("flags", ctypes.c_ubyte),
        ("reserved", ctypes.c_ubyte),
        ("timeStamp", ctypes.c_ulonglong),
        ("tagData", s_xl_tag_data)
    ]

class VXlApi:
    def __init__(self):
        
        VECTOR_DLL = 'vxlapi64.dll' if platform.machine().endswith('64') else 'vxlapi.dll'
        try:
            self.vxlapi = ctypes.cdll.LoadLibrary(VECTOR_DLL)
        except:
            print('No dll found in default folder C:/Users/Public/Documents/Vector/XL Driver Library 11.6.12/bin/')

        # Configure input parameters to vxlapi functions
        self.vxlapi.xlGetApplConfig.argtypes = [ctypes.c_char_p, ctypes.c_uint, ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.POINTER(ctypes.c_uint), ctypes.c_uint]

        self.vxlapi.xlGetDriverConfig.argtypes = [ctypes.POINTER(XLdriverConfig)]

        self.vxlapi.xlGetErrorString.argtypes = [XLstatus]
        self.vxlapi.xlGetErrorString.restype = ctypes.c_char_p

        self.vxlapi.xlGetChannelMask.argtypes = [ctypes.c_uint, ctypes.c_uint, ctypes.c_uint]
        self.vxlapi.xlGetChannelMask.restype = ctypes.c_ulonglong

        self.vxlapi.xlOpenPort.argtypes = [ctypes.POINTER(XLportHandle), ctypes.c_char_p, XLaccess, ctypes.POINTER(XLaccess), ctypes.c_uint,  ctypes.c_uint,  ctypes.c_uint]
        
        self.vxlapi.xlActivateChannel.argtypes = [XLportHandle, XLaccess, ctypes.c_uint,  ctypes.c_uint]

        self.vxlapi.xlSetNotification.argtypes = [XLportHandle, ctypes.POINTER(XLhandle), ctypes.c_int]
        
        self.vxlapi.xlCanTransmit.argtypes = [XLportHandle, XLaccess, ctypes.POINTER(ctypes.c_uint), ctypes.c_void_p]
        
        
    def xlGetApplConfig(
        self, 
        appName: ctypes.c_char_p,
        appChannel: ctypes.c_uint, 
        pHwType: ctypes.POINTER(ctypes.c_uint), 
        pHwIndex: ctypes.POINTER(ctypes.c_uint), 
        pHwChannel: ctypes.POINTER(ctypes.c_uint), 
        busType: ctypes.c_uint
        ) -> XLstatus:
        """ Get application config

        Parameters
        ----------
        appName :
            The name of the application
        appChannel :
            ?
        pHwType :
            The specific vector hardware interface (e.g. CanCaseXL, VN1630)
        pHwIndex :
            If multiple hardware interfaces are connected, which one to use. If only one connected, use index 0
        pHwChannel :
            Which physical channel the applicaion is tied to
        busType :
            Can, CanFD, Lin...
        Returns
        -------
        XLstatus
            Status of the function call
        """
        return self.vxlapi.xlGetApplConfig(appName, appChannel, pHwType, pHwIndex, pHwChannel, busType)

    def xlGetErrorString(
        self,
        err: XLstatus
    ) -> XLstringType:
        return self.vxlapi.xlGetErrorString(err)
        
    def xlOpenDriver(
        self) -> XLstatus:
        return self.vxlapi.xlOpenDriver()

    def xlGetDriverConfig(
        self,
        pDriverConfig: ctypes.POINTER(XLdriverConfig)
    ) -> XLstatus:
        return self.vxlapi.xlGetDriverConfig(pDriverConfig)

    def xlGetChannelMask(
        self,
        hwType: ctypes.c_uint,
        hwIndex: ctypes.c_uint,
        hwChannel: ctypes.c_uint
    ) -> XLstatus:
        return self.vxlapi.xlGetChannelMask(hwType, hwIndex, hwChannel)

    def xlOpenPort(
        self,
        pPortHandle: XLportHandle,
        userName: ctypes.c_char_p,
        accessMask: XLaccess,
        pPermissionMask: XLaccess,
        rxQueueSize: ctypes.c_uint,
        xlInterfaceVersion: ctypes.c_uint,
        busType: ctypes.c_uint
    ) -> XLstatus:
        return self.vxlapi.xlOpenPort(pPortHandle, userName, accessMask, pPermissionMask, rxQueueSize, xlInterfaceVersion, busType)

    def xlActivateChannel(
        self,
        portHandle: XLportHandle,
        accessMask: XLaccess,
        busType: ctypes.c_uint,
        flags: ctypes.c_uint
    ) -> XLstatus:
        return self.vxlapi.xlActivateChannel(portHandle, accessMask, busType, flags)

    def xlSetNotification(
        self,
        portHandle: XLportHandle,
        pHandle: ctypes.POINTER(XLhandle),
        queueLevel: ctypes.c_int
    ) -> XLstatus:
        return self.vxlapi.xlSetNotification(portHandle, pHandle, queueLevel)

    def xlReceive(
        self,
        portHandle: XLportHandle,
        pEventCount: ctypes.POINTER(ctypes.c_uint),
        pEventList: ctypes.POINTER(XLevent)
    ) -> XLstatus:
        return self.vxlapi.xlReceive(portHandle, pEventCount, pEventList)

    def xlCanTransmit(
        self,
        portHandle: XLportHandle,
        accessMask: XLaccess,
        messageCount: ctypes.POINTER(ctypes.c_uint),
        pMessages: ctypes.c_void_p
    ) -> XLstatus:
        return self.vxlapi.xlCanTransmit(portHandle, accessMask, messageCount, pMessages)