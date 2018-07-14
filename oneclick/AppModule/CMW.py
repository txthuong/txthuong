import imp
##try:
##    imp.find_module("pyvisa")
##    import visa #read the help here: http://pyvisa.readthedocs.org/en/latest/api/highlevel.html
##except Exception,e:
##    print type(e)
##    print e
import pyvisa
    
from time import *

class CMW():
    def __init__(self, USB_Port):        
        self.__rm = visa.ResourceManager()
        self.__inst = self.__rm.open_resource(USB_Port)
        sleep(8)
        self.__inst.timeout = 8000

    def write(self, command):
        try:
            self.__inst.write(command)
            print "-->CMW : %s" % command
            sleep(0.2)
        except Exception,e:
            print type(e)
            print e
            print "\n---->Problem: fail to send command to CMW !!!\n"

    def read(self):
        resp = 'Unkown'
        try:
            resp = self.__inst.read_raw()
            print "<--CMW : %s" % resp
        except Exception,e:
            print type(e)
            print e
            print "\n---->Problem: fail to read response from CMW !!!\n"

    def query(self, command):
        resp = 'Unkown'
        try:
            resp = self.__inst.query(command)
        except Exception,e:
            print type(e)
            print e
            print "\n---->Problem: fail to query CMW !!!\n"
        return resp

    def setCmwReady(self):
        self.query("*IDN?")
        self.write("SYSTem:PRESet:ALL")
        self.write("*RST;*OPC?")
        self.write("*CLS;*OPC?")
        self.write("TRACe:REMote:MODE:DISPlay:ENABle LIVE")
        self.query("*DEV?")

    def setCmwLTE(self,band="LTE-BAND4",connection_type = "data applicatoin", IP_Type = "Auto"):
        cmmand = "NA"
        if "LTE-BAND" in band:
            cmmand = "CONFigure:LTE:SIGN:BAND OB%s" % str(band.split("LTE-BAND")[1])
            self.write(cmmand)
            self.write("CONFigure:LTE:SIGN:DMODe FDD")
            self.write("CONFigure:LTE:SIGN:SCC:AMODe AUTO")
            self.write("CONFigure:LTE:SIGN:ETOE ON")
            self.write("CONFigure:DATA:CONTrol:FTP:STYPe SERV")
            self.write("CONFigure:DATA:CONTrol:FTP:IPVSix ON")
            self.write("CONFigure:DATA:CONTrol:HTTP:IPVSix ON")
            self.write("SOURce:DATA:CONTrol:FTP:STATe ON")
            self.write("SOURce:DATA:CONTrol:DNS:STATe ON")
            self.write("SOURce:DATA:CONTrol:HTTP:STATe ON")
            self.write("ROUTe:LTE:SIGN:SCENario:SCELl RF1C,RX1,RF1C,TX1")
            self.write("CONFigure:LTE:SIGN:CONNection:PCC:TSCHeme SISO")
            self.write("CONFigure:LTE:SIGN:CONNection:UECategory:REPorted ON")
            if connection_type == "data applicatoin":
                self.write("CONFigure:LTE:SIGN:CONNection:CTYPe DAPPlication")
            if IP_Type == "Static":
                self.write("CONFigure:DATA:CONTrol:IPVSix:ADDRess:TYPE STATic")
                self.write("CONFigure:DATA:CONTrol:IPVFour:ADDRess:TYPE STATic")
            if IP_Type == "Auto":
                self.write("CONFigure:DATA:CONTrol:IPVSix:ADDRess:TYPE AUTO")
                self.write("CONFigure:DATA:CONTrol:IPVFour:ADDRess:TYPE AUTO")
##            self.write("SOURce:LTE:SIGN:CELL:STATe ON")
            self.query("*OPC?")
        else:
            print "\n---->Problem: Invalid Band parameter !!!\n"

    def setCmwCell(self, act = 'LTE', state = 'on'):
        if act == 'LTE':
            self.write("SOURce:LTE:SIGN:CELL:STATe %s" % state.upper())
        if act == 'UMTS':
            self.write("SOURce:WCDMa:SIGN:CELL:STATe %s" % state.upper())
        
             
    def setCmwWCDMA(self,band="WCDMA-BAND4", IP_Type = "Auto"):
        cmmand = "NA"
        if "WCDMA-BAND" in band:
            cmmand = "CONFigure:WCDMa:SIGN:CARRier:BAND OB%s" % str(band.split("WCDMA-BAND")[1])
            self.write(cmmand)
            self.write("CONFigure:WCDMa:SIGN:ETOE ON")            
            self.write("CONFigure:DATA:CONTrol:FTP:STYPe SERV")
            self.write("CONFigure:DATA:CONTrol:FTP:IPVSix ON")
            self.write("CONFigure:DATA:CONTrol:HTTP:IPVSix ON")
            self.write("SOURce:DATA:CONTrol:FTP:STATe ON")
            self.write("SOURce:DATA:CONTrol:DNS:STATe ON")
            self.write("SOURce:DATA:CONTrol:HTTP:STATe ON")
            self.write("ROUTe:WCDMa:SIGN:SCENario:SCELl RF1C,RX1,RF1C,TX1")
            self.write("CONFigure:WCDMa:SIGN:CONNection:PACKet:DRATe HSDPa, HSUPa")
            self.write("CONFigure:WCDMa:SIGN:CELL:HSDPa:UECategory:REPorted ON")            
            if IP_Type == "Static":
                self.write("CONFigure:DATA:CONTrol:IPVSix:ADDRess:TYPE STATic")
                self.write("CONFigure:DATA:CONTrol:IPVFour:ADDRess:TYPE STATic")
            if IP_Type == "Auto":
                self.write("CONFigure:DATA:CONTrol:IPVSix:ADDRess:TYPE AUTO")
                self.write("CONFigure:DATA:CONTrol:IPVFour:ADDRess:TYPE AUTO")
##            self.write("SOURce:WCDMa:SIGN:CELL:STATe ON")
            self.query("*OPC?")
        else:
            print "\n---->Problem: Invalid Band parameter !!!\n"

    def checkUeRegistration(self, ue_type = "UMTS"):
        result = False
        if ue_type == "UMTS":
            self.write("FETCh:WCDMa:SIGN:CSWitched:STATe?")
            if "REG" in self.read():
                result = True

        return result
            
        

if __name__ == u'__main__':
    my_cmw = CMW(u'USB0::0x0AAD::0x0057::0150005::INSTR')
    print my_cmw.setCmwReady()
    my_cmw.setCmwBand("LTE-BAND10")
    my_cmw.setCmw
    my_cmw.write('CONFigure:GPRF:MEAS:RFSettings:FREQuency %E' % frequency) 
