import sys
import telnetlib
import time,re
import serial,threading

import imp
try:
    imp.find_module("pyvisa")
    import visa #read the help here: http://pyvisa.readthedocs.org/en/latest/api/highlevel.html
except:
    pass

print_mutex = threading.Lock()



def my_print(s):
    localtime   = time.localtime()
    timeString  = time.strftime("%Y/%m/%d %H:%M:%S", localtime)
    print_mutex.acquire()
    print "(%s) %s" % (timeString, s)
    print_mutex.release()

class POWERSUPPLY():
    boolValidIpAddr = False
    boolValidComAddr = False
    boolValidGpibAddr = False

    def __init__(self, ip_addr = "APC_127.0.0.1_1", vo="4.0"):
        p = re.compile("APC\d*_\d{1,3}\.\d{1,3}\.\d{1,3}.\d{1,3}_\d")
        
        if p.match(ip_addr) is not None:
            POWERSUPPLY.boolValidIpAddr = True
            self.ip = ip_addr.split("_")[1]
            self.outletPort = ip_addr.split("_")[2]
            my_print("Power Suppy IP Addr = " + self.ip)
            my_print("Outlet of Power Supply = " + self.outletPort)
        elif 'COM' in ip_addr:
            POWERSUPPLY.boolValidComAddr = True
            self.ser = serial.Serial(ip_addr)#( ip_addr,9600,8,"N",1,"None")
            self.ser.baudrate = '9600'
            self.ser.bytesize = 8
            self.ser.parity = 'N'
            self.ser.stopbits = 1
            self.ser.timeout = 2
            self.ser.write('system:remote\r\n')
            time.sleep(1)
            self.ser.write('*IDN?\r\n')
            time.sleep(1)
            self.type=""
            if "E3631A" in self.ser.read(self.ser.inWaiting()):
                self.type = "E3631A"
            
            if  self.type == "E3631A":
                self.ser.write('appl p6v, %s, 5.0\r\n' % vo)
            else:
                self.ser.write('appl %s\r\n' % vo)
        elif 'GPIB' in ip_addr:
            self.rm = visa.ResourceManager()
            self.inst = self.rm.open_resource(ip_addr)
            POWERSUPPLY.boolValidGpibAddr = True
            self.inst.write("SYS:REM")
            self.inst.write('CLR')
            my_print( self.inst.query('*IDN?'))
            self.inst.write('appl p6v, %s, 5.0' % vo)
        else:
            my_print("Incorrect APC power address: " + ip_addr)
            my_print("Please correct it in sample.cfg")

    def reboot(self):
      while(1):
        try:
            if POWERSUPPLY.boolValidIpAddr:
                tn = telnetlib.Telnet(self.ip,"23")
                tn.read_until("User Name :",10)
                tn.write("apc\r\n")
                tn.read_until("Password  :",10)
                tn.write("sf2sogo-c\r\n")
                #time.sleep(1)
                my_print( tn.read_until("APC>"))
                tn.write("off " + self.outletPort + "\r\n")
                my_print( tn.read_until("APC>"))
                my_print("---->Power off")
                time.sleep(20)
                tn.write("on " + self.outletPort + "\r\n")
                my_print( tn.read_until("APC>"))
                my_print( tn.write("quit\r\n"))
                tn.close()
                my_print("---->Power on")
                time.sleep(3)
                return "OK"
            elif POWERSUPPLY.boolValidComAddr:
                my_print("---->Power off")
                self.ser.write('outp off\r\n')
                time.sleep(1)
                my_print("---->Power on")
                self.ser.write('outp on\r\n')
                return "OK"
            elif POWERSUPPLY.boolValidGpibAddr:
                my_print("---->Power off")
                self.inst.write('outp off')
                time.sleep(1)
                my_print("---->Power on")
                self.inst.write('outp on')
            else:
                my_print("APC address is invalid")
                return "NOK"
        except Exception, e:
            print e
            print "----->Problem: Exception comes up when reboot !!!"
            continue

    def on(self):
        try:
            if POWERSUPPLY.boolValidIpAddr:
                tn = telnetlib.Telnet(self.ip,"23")
                tn.read_until("User Name :",10)
                tn.write("apc\r\n")
                tn.read_until("Password  :",10)
                tn.write("sf2sogo-c\r\n")
                #time.sleep(1)
                my_print( tn.read_until("APC>") )          
                tn.write("on " + self.outletPort + "\r\n")
                my_print( tn.read_until("APC>"))
                my_print( tn.write("quit\r\n"))
                tn.close()
                my_print("---->Power on")
                #time.sleep(3)
                return "OK"
            elif POWERSUPPLY.boolValidComAddr:
                my_print("---->Power on")
                self.ser.write('outp on\r\n')
            elif POWERSUPPLY.boolValidGpibAddr:
                my_print("---->Power on")
                self.inst.write('outp on')
                time.sleep(1)
            else:
                my_print("APC address is invalid")
                return "NOK"
        except Exception, e:
            print e            
            print "----->Problem: Exception comes up when power on !!!"
            return "NOK"

    def off(self):
        try:
            if POWERSUPPLY.boolValidIpAddr:
                tn = telnetlib.Telnet(self.ip,"23")
                tn.read_until("User Name :",10)
                tn.write("apc\r\n")
                tn.read_until("Password  :",10)
                tn.write("sf2sogo-c\r\n")
                #time.sleep(1)
                my_print( tn.read_until("APC>") )          
                tn.write("off " + self.outletPort + "\r\n")
                my_print( tn.read_until("APC>"))
                my_print( tn.write("quit\r\n"))
                tn.close()
                my_print("---->Power off")
                #time.sleep(3)
                return "OK"
            elif POWERSUPPLY.boolValidComAddr:
                my_print("---->Power off")
                self.ser.write('outp off\r\n')
            elif POWERSUPPLY.boolValidGpibAddr:
                my_print("---->Power off")
                self.inst.write('outp off')
                time.sleep(1)
            else:
                my_print("APC address is invalid")
                return "NOK"
        except Exception, e:
            print e
            print "----->Problem: Exception comes up when power off !!!"
            return "NOK"

    def __del__(self):
        try:
            if POWERSUPPLY.boolValidComAddr:
                self.ser.close()
        except Exception, e:
            print e
            print "----->Warnning: Exception comes up when close power suplly port !!!"
            

    
        

if __name__ == "__main__":
    
    myPower = POWERSUPPLY(ip_addr = "COM8", vo = "4.0")
    myPower = POWERSUPPLY(ip_addr = "APC_10.23.58.400_1", vo = "4.0")
    myPower = POWERSUPPLY(ip_addr = "GPIB0::6::INSTR", vo = "4.0")
    
    
    myPower.on()
    
    myPower.off()
    
    myPower.reboot()
