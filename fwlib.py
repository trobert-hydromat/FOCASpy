"""
Thomas Robert
2024-05-31
trobert@hydromat.com

fwlib.py
    Function def for fwlib64.dll
"""

import ctypes
from ctypes import *
from enum import Enum

class REALPRM(Structure):
    _fields_ = [
        ('prm_val', c_int),     #/* data of real parameter */
        ('dec_val', c_int)     #/* decimal point of real parameter */
    ]
class IODBPSD_1(Structure):
    _fields_ = [
        ('datano', c_short),  
        ('type', c_short),      
        ('cdata', c_ubyte),
        ('idata', c_short),
        ('ldata', c_int)
    ]
class IODBPSD_2(Structure):
    _fields_ = [
        ('datano', c_short),   #/* data number */
        ('type', c_short),      #/* axis number */
        ('rdata', REALPRM)
    ]
class IODBPMCu(ctypes.Union):
    _fields_ = [
        ('cdata', c_ubyte*5),
        ('idata', c_short*5),
        ('ldata', c_long*5),
        ('fdata', c_float*5),
        ('dfdata', c_double*5)
    ]
class IODBPMC0(Structure):
    _fields_ = [
        ('type_a', c_short),
        ('type_d', c_short),
        ('datano_s', c_short),
        ('datano_e', c_short),
        ('u', IODBPMCu)        
    ]


fwlib = ctypes.CDLL(".\\Fwlib64.dll")
fwlib30i = ctypes.CDLL(".\\Fwlib30i64.dll")

fwlib.cnc_allclibhndl2.restype = c_short
fwlib.cnc_allclibhndl2.argtypes = [c_int, POINTER(c_ushort)]

fwlib.cnc_allclibhndl3.restype = c_short
fwlib.cnc_allclibhndl3.argtypes = [c_char_p, c_ushort, c_int, POINTER(c_ushort)]

fwlib.cnc_freelibhndl.restype = c_short
fwlib.cnc_freelibhndl.argtypes = [POINTER(c_ushort)]

fwlib.cnc_wrparam.restype = c_short
fwlib.cnc_wrparam.argtypes = [c_ushort, c_short, POINTER(IODBPSD_2)]

fwlib.cnc_rdparam3.restype = c_short
fwlib.cnc_rdparam3.argtypes = [c_ushort, c_short, c_short,c_short,c_short, POINTER(IODBPSD_1)]

fwlib30i.pmc_rdpmcrng.restype = c_short
fwlib30i.pmc_rdpmcrng.argtypes = [c_ushort, c_short, c_short,c_ushort,c_ushort,c_ushort, POINTER(IODBPMC0)]


class Focas1:

    class focas_ret(Enum): 
        EW_PROTOCOL =     (-17)           # protocol error */
        EW_SOCKET   =     (-16)           # Windows socket error */
        EW_NODLL    =     (-15)           # DLL not exist error */
        EW_BUS      =     (-11)           # bus error */
        EW_SYSTEM2  =     (-10)           # system error */
        EW_HSSB     =     (-9)            # hssb communication error */
        EW_HANDLE   =     (-8)            # Windows library handle error */
        EW_VERSION  =     (-7)            # CNC/PMC version missmatch */
        EW_UNEXP    =     (-6)            # abnormal error */
        EW_SYSTEM   =     (-5)            # system error */
        EW_PARITY   =     (-4)            # shared RAM parity error */
        EW_MMCSYS   =     (-3)            # emm386 or mmcsys install error */
        EW_RESET    =     (-2)            # reset or stop occured error */
        EW_BUSY     =     (-1)            # busy error */
        EW_OK       =     0               # no problem */
        EW_FUNC     =     1               # command prepare error */
        EW_NOPMC    =     1               # pmc not exist */
        EW_LENGTH   =     2               # data block length error */
        EW_NUMBER   =     3               # data number error */
        EW_RANGE    =     3               # address range error */
        EW_ATTRIB   =     4               # data attribute error */
        EW_TYPE     =     4               # data type error */
        EW_DATA     =     5               # data error */
        EW_NOOPT    =     6               # no option error */
        EW_PROT     =     7               # write protect error */
        EW_OVRFLOW  =     8               # memory overflow error */
        EW_PARAM    =     9               # cnc parameter not correct error */
        EW_BUFFER   =     10              # buffer error */
        EW_PATH     =     11              # path error */
        EW_MODE     =     12              # cnc mode error */
        EW_REJECT   =     13              # execution rejected error */
        EW_DTSRVR   =     14              # data server error */
        EW_ALARM    =     15              # alarm has been occurred */
        EW_STOP     =     16              # CNC is not running */
        EW_PASSWD   =     17              # protection data error */
        DNC_NORMAL  =  (-1)               # normal completed */
        DNC_CANCEL  =  (-32768)           # DNC operation was canceled by CNC */
        DNC_OPENERR =  (-514)             # file open error */
        DNC_NOFILE  =  (-516)             # file not found */
        DNC_READERR =  (-517)              # read error */
    class focas_pmc_address_type(Enum):
        G = 0
        F = 1
        Y = 2
        X = 3
        A = 4
        R = 5
        T = 6
        K = 7
        C = 8
        D = 9
        M = 10
        N = 11
        E = 12
        Z = 13
    class focas_pmc_data_type(Enum):
        BYTE = 0
        WORD = 1
        LONG = 2
        FLOAT32 = 4
        FLOAT64 = 5


    def cnc_allclibhndl2(node, handle):
        return Focas1.focas_ret(fwlib.cnc_allclibhndl2(node, byref(handle)))

    def cnc_allclibhndl3(ip, port, timeout, handle):
        p1 = create_string_buffer(ip.encode(),15)
        return Focas1.focas_ret(fwlib.cnc_allclibhndl3(p1, port, timeout, byref(handle)))
    
    def cnc_freelibhndl(handle):
        return Focas1.focas_ret(fwlib.cnc_freelibhndl(byref(handle)))
    
    def cnc_wrparam(handle, size, iodbpsd:IODBPSD_2):
        return Focas1.focas_ret(fwlib.cnc_wrparam(handle, size, byref(iodbpsd)))
    
    def cnc_rdparam3(handle: int, paramNumber: int, axisNumber: int, size: int, absolute: bool, iodbpsd:IODBPSD_1):
        return Focas1.focas_ret(fwlib.cnc_rdparam3(handle, paramNumber, axisNumber, size, int(absolute), byref(iodbpsd)))
    
    def pmc_rdpmcrng(handle: int, addressType: focas_pmc_address_type, dataType: focas_pmc_data_type, addressStart: int, addressEnd: int, size: int, iodbpmc:IODBPMC0):
        return Focas1.focas_ret(fwlib30i.pmc_rdpmcrng(handle, addressType.value, dataType.value, addressStart, addressEnd, size, byref(iodbpmc)))
    
    

    

    