"""
Thomas Robert
2024-05-31
trobert@hydromat.com

FocasInterface.py
    More human readable functions to interact with CNC
"""

from fwlib import *

class FocasInterface:

    def __init__(self):
        self.ETHERNET()
    
    def ETHERNET(self, ip="192.168.1.10", port=8193, timeout=10) -> None:
        self.handle = c_ushort()
        self.ip = ip
        self.port = port
        self.timeout = timeout
        self.node = None

    def HSSB(self, node=0) -> None:
        self.handle = c_ushort()
        self.ip = None
        self.port = None
        self.timeout = None
        self.node = node


    def Disconnect(self) -> Focas1.focas_ret:
        return Focas1.cnc_freelibhndl(self.handle)
    
    def Connect(self) -> Focas1.focas_ret:
        if(self.node != None):
            return Focas1.cnc_allclibhndl2(self.node, self.handle)
        elif (self.ip != None):
            return Focas1.cnc_allclibhndl3(self.ip, self.port, self.timeout, self.handle)

    def WriteByteParameter(self, paramNum: int, byteValue: int, axisNumber: int=0) -> Focas1.focas_ret:
        param = IODBPSD_2()
        rdata = REALPRM()
        rdata.prm_val = byteValue
        param.datano = paramNum
        param.type = axisNumber
        param.rdata = rdata
        return Focas1.cnc_wrparam(self.handle, 5, param)
    
    """
    def WriteWordParameter(self, paramNum: int, wordValue: int, axisNumber: int=0):
        param = IODBPSD_2()
        rdata = REALPRM()
        rdata.prm_val = wordValue
        param.datano = paramNum
        param.type = axisNumber
        param.rdata = rdata
        return Focas1.cnc_wrparam(self.handle, 6, param)
    """
        
    def WriteShortParameter(self, paramNum: int, shortValue: int, axisNumber: int=0) -> Focas1.focas_ret:
        param = IODBPSD_2()
        rdata = REALPRM()
        rdata.prm_val = shortValue
        param.datano = paramNum
        param.type = axisNumber
        param.rdata = rdata
        return Focas1.cnc_wrparam(self.handle, 8, param)
    
    def ReadParameter(self, paramNum: int, axisNumber: int = 0) -> c_short:
        param = IODBPSD_1()
        ret = Focas1.cnc_rdparam3(self.handle, paramNum, axisNumber, 8, axisNumber!= 0, param)
        #print(ret)
        return param.cdata
        
    def ReadPMCBool(self, addressType: Focas1.focas_pmc_address_type, startByte: int, startBit: int) -> bool:
        pmcByte = self.ReadPMCByte(addressType, startByte)
        return bool(int(format(pmcByte, '08b')[7-startBit]))

    def ReadPMCByte(self, addressType: Focas1.focas_pmc_address_type, startByte: int) -> int:
        iodbpmc = IODBPMC0()
        Focas1.pmc_rdpmcrng(self.handle, addressType, Focas1.focas_pmc_data_type.BYTE, startByte, startByte+1, 16, iodbpmc)
        return iodbpmc.u.cdata[0]
    
    def ReadPMCAddress(self, address: str):
        if( "." in address):
            return self.ReadPMCBool(Focas1.focas_pmc_address_type[address[0]], int(address[1:-2]), int(address[-1]))
        else:
            return self.ReadPMCByte(Focas1.focas_pmc_address_type[address[0]], int(address[1:]))