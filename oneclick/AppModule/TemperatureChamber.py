#
#
# 2016-11-30, Chamber Temperature need cofig data map mode 2, baudrate = 19600
#

import sys
import telnetlib
import time,re
import serial,threading
import VarGlobal
from VarGlobal import *

print_mutex = threading.Lock()

com_addr1 = ''

def my_print(s):
    localtime   = time.localtime()
    timeString  = time.strftime("%Y/%m/%d %H:%M:%S", localtime)
    print_mutex.acquire()
    print "(%s) %s" % (timeString, s)
    print_mutex.release()

def my_print_send(s):

    hex_list = ["{:02x}".format(ord(c)) for c in s]
    for i in range(0,len(hex_list)):
        hex_list[i] = '0x'+hex_list[i]
    str = '><'.join(hex_list)

    s = 'Snd Chamber '+com_addr1+': <' + str +'>'
    localtime   = time.localtime()
    timeString  = time.strftime("%Y/%m/%d %H:%M:%S", localtime)
    print_mutex.acquire()
    VarGlobal.myColor = VarGlobal.colorLsit[7]
    print "(%s) %s" % (timeString, s)
    VarGlobal.myColor = VarGlobal.colorLsit[8]
    print_mutex.release()

def my_print_rcv(s):
    hex_list = ["{:02x}".format(ord(c)) for c in s]
    for i in range(0,len(hex_list)):
        hex_list[i] = '0x'+hex_list[i]
    str = '><'.join(hex_list)

    s = 'Rcv Chamber '+com_addr1+': <' + str +'>'

    localtime   = time.localtime()
    timeString  = time.strftime("%Y/%m/%d %H:%M:%S", localtime)
    print_mutex.acquire()
    VarGlobal.myColor = VarGlobal.colorLsit[6]
    print "(%s) %s" % (timeString, s)
    VarGlobal.myColor = VarGlobal.colorLsit[8]
    print_mutex.release()
 
def _calculateCrcString(inputstring):
    _CRC16TABLE = (
            0, 49345, 49537,   320, 49921,   960,   640, 49729, 50689,  1728,  1920, 
        51009,  1280, 50625, 50305,  1088, 52225,  3264,  3456, 52545,  3840, 53185, 
        52865,  3648,  2560, 51905, 52097,  2880, 51457,  2496,  2176, 51265, 55297, 
         6336,  6528, 55617,  6912, 56257, 55937,  6720,  7680, 57025, 57217,  8000, 
        56577,  7616,  7296, 56385,  5120, 54465, 54657,  5440, 55041,  6080,  5760, 
        54849, 53761,  4800,  4992, 54081,  4352, 53697, 53377,  4160, 61441, 12480, 
        12672, 61761, 13056, 62401, 62081, 12864, 13824, 63169, 63361, 14144, 62721, 
        13760, 13440, 62529, 15360, 64705, 64897, 15680, 65281, 16320, 16000, 65089, 
        64001, 15040, 15232, 64321, 14592, 63937, 63617, 14400, 10240, 59585, 59777, 
        10560, 60161, 11200, 10880, 59969, 60929, 11968, 12160, 61249, 11520, 60865, 
        60545, 11328, 58369,  9408,  9600, 58689,  9984, 59329, 59009,  9792,  8704, 
        58049, 58241,  9024, 57601,  8640,  8320, 57409, 40961, 24768, 24960, 41281, 
        25344, 41921, 41601, 25152, 26112, 42689, 42881, 26432, 42241, 26048, 25728, 
        42049, 27648, 44225, 44417, 27968, 44801, 28608, 28288, 44609, 43521, 27328, 
        27520, 43841, 26880, 43457, 43137, 26688, 30720, 47297, 47489, 31040, 47873, 
        31680, 31360, 47681, 48641, 32448, 32640, 48961, 32000, 48577, 48257, 31808, 
        46081, 29888, 30080, 46401, 30464, 47041, 46721, 30272, 29184, 45761, 45953, 
        29504, 45313, 29120, 28800, 45121, 20480, 37057, 37249, 20800, 37633, 21440, 
        21120, 37441, 38401, 22208, 22400, 38721, 21760, 38337, 38017, 21568, 39937, 
        23744, 23936, 40257, 24320, 40897, 40577, 24128, 23040, 39617, 39809, 23360, 
        39169, 22976, 22656, 38977, 34817, 18624, 18816, 35137, 19200, 35777, 35457, 
        19008, 19968, 36545, 36737, 20288, 36097, 19904, 19584, 35905, 17408, 33985, 
        34177, 17728, 34561, 18368, 18048, 34369, 33281, 17088, 17280, 33601, 16640, 
        33217, 32897, 16448)
    # Preload a 16-bit register with ones
    register = 0xFFFF

    for char in inputstring:
        register = (register >> 8) ^ _CRC16TABLE[(register ^ ord(char)) & 0xFF]
 
    return register
    
        
class TEMPERATURE_CHAMBER():
    
    def __init__(self, com_addr = "COM1",baudrate=19200, bytesize=8, parity="N", stopbits=1):
        global com_addr1
        com_addr1 = com_addr
        self.ser = serial.Serial(com_addr)
        self.ser.baudrate = baudrate
        self.ser.bytesize = bytesize
        if parity == "N" or parity == "n":
            self.ser.parity = "N"
        self.ser.stopbits = stopbits
        self.ser.timeout = 2
        time.sleep(1)
        self.type=""

    def get_response(self):
        "goal of the method : This method read data was recieved from Chamber COM"
        "INPUT: "
        "OUTPUT: data was recieved"
        time.sleep(0.5)
        res=''
        while self.ser.inWaiting():
            res += self.ser.read(1)
        time.sleep(0.1)
        while self.ser.inWaiting():
            res += self.ser.read(1)
        return res
        
    def read_actual_temp(self):
        "goal of the method : This method return the actually temperature into the Chamber "
        "INPUT: "
        "OUTPUT: The temperature into the Chamber * 10 (C degree)"
        try:
            str1 = '\x01\x03' + chr(int(100/256)) + chr(int(100%256))
            str1 = str1 + chr(0) + chr(1)
            str1 = str1 + chr(int(_calculateCrcString(str1)%256)) + chr(int(_calculateCrcString(str1)/256))
            
            print
            my_print('Read actual Chamber Temperature:')
            my_print_send(str1)
             
            self.ser.write(str1)
            res = self.get_response()
            my_print_rcv(res)
            
            temp =  int(ord(res[3]))*256 + int(ord(res[4]))
            if (temp >> 15) == 1:
                temp = temp -1
                temp = temp^0xffff  
                temp1 = temp/10 
                temp2 = temp%10
                my_print('The temperature is: -%d.%d*C' %(temp1,temp2))
                return (0-temp)
            else:
                temp1 = temp/10 
                temp2 = temp%10
                my_print('The temperature is: %d.%d*C' %(temp1,temp2))
                return temp
                
        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            my_print("----->Problem: Exception comes up when read actual temperature!!!")
            
    def get_temp_setpoint(self):
        "goal of the method: This method read temperature set point to Chamber"
        "INPUT : "
        "OUTPUT : set point temperature after set * 10 (C degree)"
    
        try:
            str1 = '\x01\x03' + chr(int(300/256)) + chr(int(300%256))
            str1 = str1 + chr(0) + chr(1)
            str1 = str1 + chr(int(_calculateCrcString(str1)%256)) + chr(int(_calculateCrcString(str1)/256))
            
            print
            my_print('Get Temperature Set Point:')
            my_print_send(str1)
            
            self.ser.write(str1)
            res = self.get_response()
            my_print_rcv(res)
            
            temp =  int(ord(res[3]))*256 + int(ord(res[4]))
            if (temp >> 15) == 1:
                temp = temp -1
                temp = temp^0xffff  
                temp1 = temp/10 
                temp2 = temp%10
                my_print('The temperature set point is: -%d.%d*C' %(temp1,temp2))
                return (0-temp)
            else:
                temp1 = temp/10 
                temp2 = temp%10
                my_print('The temperature set point is: %d.%d*C' %(temp1,temp2))    
                return temp
        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            my_print("----->Problem: Exception comes up when read set point temperature !!!")
                
    def set_temp_setpoint(self, temp):
        "goal of the method: This method set temperature set point to Chamber"
        "INPUT : set point temperature (C degree)"
        "OUTPUT : "
        try:
            str1 = '\x01\x06' + chr(int(300/256)) + chr(int(300%256))
            if temp >= 0:
                temp = temp*10
                str1 = str1 +  chr(int(temp/256)) + chr(int(temp%256)) 
            else:
                temp = temp*10
                temp = 0 - temp
                temp = temp^0xffff  
                temp = temp +1
                str1 = str1 +  chr(int(temp/256)) + chr(int(temp%256)) 
            str1 = str1 + chr(int(_calculateCrcString(str1)%256)) + chr(int(_calculateCrcString(str1)/256))
            
            print
            my_print('Set Temperature Set Point:')
            my_print_send(str1)
            
            self.ser.write(str1)
            res = self.get_response()
            my_print_rcv(res)
            
            temp =  int(ord(res[4]))*256 + int(ord(res[5]))
            if (temp >> 15) == 1:
                temp = temp -1
                temp = temp^0xffff  
                temp1 = temp/10 
                temp2 = temp%10
                my_print('The temperature set point is: -%d.%d*C' %(temp1,temp2))
            else:
                temp1 = temp/10 
                temp2 = temp%10
                my_print('The temperature set point is: %d.%d*C' %(temp1,temp2))  
                
        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            my_print("----->Problem: Exception comes up when set set point temperature !!!")
            
    def get_power_status(self):
        "goal of the method: This method read Power status of the Chamber"
        "INPUT : "
        "OUTPUT : 'ON' or 'OFF'"
        
        result = 'Unknown'
        try:
            str1 = '\x01\x03' + chr(int(2000/256)) + chr(int(2000%256))
            str1 = str1 + chr(0) + chr(1)
            str1 = str1 + chr(int(_calculateCrcString(str1)%256)) + chr(int(_calculateCrcString(str1)/256))
            
            print
            my_print('Read Power Status:')
            my_print_send(str1)
            
            self.ser.write(str1)
            res = self.get_response()
            my_print_rcv(res)
            
            status =  int(ord(res[3]))*256 + int(ord(res[4]))
            if status == 1:
                my_print('Power is ON')
                result = 'ON'
            else:
                my_print('Power is OFF')
                result = 'OFF'
                
        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            my_print("----->Problem: Exception comes up when read event 1 status !!!")
            
        return result
        
    def set_power_status(self, status):
        "goal of the method: This method set Power status of the Chamber"
        "INPUT : ON or OFF"
        "OUTPUT : "
        try:
            res=''
            if status == 'ON':
                str1 = '\x01\x06' + chr(int(2000/256)) + chr(int(2000%256))
                str1 = str1 +  chr(int(1/256)) + chr(int(1%256)) 
                str1 = str1 + chr(int(_calculateCrcString(str1)%256)) + chr(int(_calculateCrcString(str1)/256))

                self.ser.write(str1)
                res = self.get_response()
                _status =  int(ord(res[4]))*256 + int(ord(res[5]))
                print
                my_print_send(str1)
                my_print_rcv(res)
                if _status == 1:
                    my_print('Power was Turn ON')
                else:
                    my_print('Command is not success')
            elif status == 'OFF':
                str1 = '\x01\x06' + chr(int(2000/256)) + chr(int(2000%256))
                str1 = str1 +  chr(int(0/256)) + chr(int(0%256)) 
                str1 = str1 + chr(int(_calculateCrcString(str1)%256)) + chr(int(_calculateCrcString(str1)/256))

                self.ser.write(str1)
                
                res = self.get_response()
                _status =  int(ord(res[4]))*256 + int(ord(res[5]))
                print
                my_print_send(str1)
                my_print_rcv(res)
                if _status == 0:
                    my_print('Power was Turn OFF')
                else:
                    my_print('Command is not success')
            else:
                print
                my_print('Command is not found')
                VarGlobal.statOfItem="NOK"
            
        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            my_print("----->Problem: Exception comes up when set event 1 status !!!")
            
    def __del__(self):
        #Close Chamber COM
        self.ser.close()
