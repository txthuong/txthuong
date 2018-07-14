#!/bin/env python
# _*_ coding: utf-8 _*_


#----------------------------------------------------------------------------
# Name:                 ComModuleAPI.py
#
# Goal:                 Contains all API functions, in order to create scenarii
#               The most used are SagOpen, SagSend and SagWaitAndTestLine
#
# Author:               refer below
#
# Version:              refer below
#
# Date:                 refer below
#
# Property:             Sagemcomm
#----------------------------------------------------------------------------


#date              who                 version                 modification
#04->09-2007       Bingxun HOU         1.0                     creation
#09-09-2011        JF Weiss            1.8.1                   add comments and light modifications
#27-06-2012        Manuel Renouf       1.8.7                   modifications for Linux
#08-12-2013        Manuel Renouf       1.9.6.2                 modifications for new serial port library like CETI
#16-06-2014        Kelvin Wong         1.9.6.8                 modifications for Tracker 4678
#10-09-2014        Kelvin Wong         1.9.6.9                 Update for string2cmd() CEREG

import wx
import sys
import time
import serial
import XmlTree
import VarGlobal
import cStringIO
import traceback
import threading
from   Output                    import *
from   ExcelDoc                  import *
from   datetime                  import datetime
from   threadStop                import Thread,PauseAllThread,ContinueAllThread,GetPauseStatus,StopAllThread
from   PersonalException import *
from xmodem import XMODEM
import logging
logging.basicConfig()
import ConfigParser
import fnmatch
import itertools
import __builtin__
from Wesh27 import AVMS
from AVMSINI import AVMSCFG
from PowerSuppy import POWERSUPPLY
import serial.tools.list_ports
from CMW import CMW
from VarGlobal import VERSION
from WESH_LWM2M import AVMS2,activateSystem,createSystem,creatReport,deleteReport,findAllReport
from EULER_LWM2M import AVMS3,activateSystem,createSystem,creatReport,deleteReport,findAllReport
from SMS_API import *
from Yocto import TARGET
from ADB import ADB
from TemperatureChamber import TEMPERATURE_CHAMBER
import re
from IPy import IP
from TelnetUtil import TelnetUtil

# Event to say MainFrame is closing
#EventClosingMainFrame = SagCreateEvent("ClosingMainFrame")

#list of opened COM ports
list_hCom = []

def ExitSagWaitLineWhenRecvError(value):
        staticVariables.ExitWhenErrorValue = value

# La classe repr?sente une commande AT
#class ATcommand():
#       def __init__(self, hCom=0, command="", delay=0):
#               self.hCom = hCom
#               self.command = command
#               self.delay = delay

# La classe repr?sente une r?ponse
class Response():
        def __init__(self):
                self.isOK=False
                self.find=False
                self.res = ''
                self.tabData = ''
                self.tabLines = []
                self.tabParse = []
                self.echo = ''
                self.totalTime = 0

# La classe repr?sente une cha?ne de donn?e en binaire 
class BinData():
        def __init__(self):
                self.tabData = ''
                self.length = 0

# La classe repr?sente event implant? par le logiciel
class SagEvent():
        """
        Subclass of threading.Thread, with a method stop() et pause()
        An event manages a flag that can be set to true with the set() method and reset to false with the clear() method. 
        The wait() method blocks until the flag is true.
        """
        
        def __init__(self, name=''):
                if VarGlobal.DEBUG_LEVEL == "DEBUG":
                        print "SagEvent.__init__()\r\n"
                self.name = name
                #returns an event instance
                self.event = threading.Event()
                        
        def set(self):
                self.event.set()
        
        def clear(self):
                self.event.clear()
        
        def wait(self,timeout=None):
                self.event.wait(timeout)
        
        def isSet(self):
                return self.event.isSet()
        
        def getName(self):
                return self.name

class Static_Variables(object):
        def __init__(self):
                self.ExitWhenErrorValue = False
                self.List_Thread = []
                #FC : First Character
                self.FcSave=['',None]

staticVariables = Static_Variables()

result = "OK"
list_hCom = []
uartbuffer = {}


def TimeDisplay(dt = None):
        "Display the time ; if dt is empty retrun actual date time under format, otherless return dt under format"
        "INPUT  : (optionnal) dt : date Time"
        "OUTPUT : date Time under format hh:mm:ss:???"
        if dt == None:
                dt = datetime.now() 
        return "(%0.2d:%0.2d:%0.2d:%0.3d)"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)

# instanciate a Lock object ; the Lock MUTEX object is needed for displaying information on screen
# because several thread may display information at the same time
print_mutex = threading.Lock()

def SafePrint(time, hCom, info, color = 8):
        "goal of the method : This method displays information, using a mutex"
        "INPUT : "
        "OUTPUT : "
        if color < len(VarGlobal.colorLsit):# or type(color)==str:
                if VarGlobal.MODE != VarGlobal.DEMO_MODE:
                        if type(time)==datetime or time == None:
                                timeDisplay = TimeDisplay(time) + " "
                        elif type(time)==str and time=="":
                                timeDisplay = ""
                        else:
                                timeDisplay = str(time) + " "
                else:
                        timeDisplay = ""
                if hCom != None and info.find("%s"%(hCom.port)) == -1 and VarGlobal.MODE != VarGlobal.DEMO_MODE:
                        info = "(%s) "%(hCom.port)+info
                # acquire the MUTEX lock
                print_mutex.acquire()  
                VarGlobal.myColor = VarGlobal.colorLsit[color]
                print timeDisplay + str(info)
                VarGlobal.myColor = VarGlobal.colorLsit[8]
                # release the MUTEX lock
                print_mutex.release()  
        else:
                # acquire the MUTEX lock
                print_mutex.acquire()  
                VarGlobal.myColor = VarGlobal.colorLsit[9]
                print "Color not in table"
                VarGlobal.myColor = VarGlobal.colorLsit[8]
                # release the MUTEX lock
                print_mutex.release()  

def SafePrintError(time, hCom, info):
        "goal of the method : This method displays errors (in red color), using a mutex"
        "INPUT : timeDisplay , hCom, info as string"
        "OUTPUT : none"
        if hCom != None and info.find("%s"%(hCom.port)) == -1 and VarGlobal.MODE != VarGlobal.DEMO_MODE:
                info = "(%s) "%(hCom.port)+info
                timeDisplay = ""
        else:
                timeDisplay = TimeDisplay(time) + ","
        # acquire the MUTEX lock
        print_mutex.acquire()
        VarGlobal.myColor = VarGlobal.colorLsit[9]
        print timeDisplay, info
        print '---------------------------------------------------------------------' 
        print '                        --- Error Detail ---                                              ' 
        print '---------------------------------------------------------------------' 
        f = cStringIO.StringIO()
        traceback.print_exc(file = f)
        print f.getvalue()
        print '---------------------------------------------------------------------'
        VarGlobal.myColor = VarGlobal.colorLsit[8]
        # release the MUTEX lock
        print_mutex.release() 


def SagOpen( port=None, baudrate=115200, bytesize=8, parity="N", stopbits=1, rtscts=1, timeout=1, RTS=True,DTR=True,xonxoff=0,interCharTimeout=None,OpenPortTimeout=2000):
        "goal of the method : This function opens the serial port"
        "INPUT : port : string including the COM port (e.g. COM9 or 9)"
        "        baudrate : communication speed"
        "        timeout : timeout value, or None if infinite wait"
        "        RTS : value of RTS state"
        "        DTR : value of DTR state"
        "        rtscts : enable RTS/CTS flow control"
        "        xonxoff : enable software flow control"
        "        interCharTimeout : Inter-character timeout, None to disable"
        "OUTPUT : COM port object"

    # validate parameter - rtscts
        flowcontrol = "Hardware"
        if type(rtscts) == type("string"):
                if rtscts not in ["Hardware", "None"]:
                        print "Invalid parameter for SagOpen() - rtscts"
                        print "Option:"
                        print "\"Hardware\"", "\"None\""
                        print ""
                        rtscts = 1
                        flowcontrol = "Hardware"
                if rtscts == "Hardware":
                        rtscts = 1
                        flowcontrol = "Hardware"
                if rtscts == "None":
                        rtscts = 0
                        flowcontrol = "None"

        SagDetectCom(port,OpenPortTimeout, "nologmsg")
        try:
                import os
                hCom=None
                #chose an implementation, depending on os
                        
                if os.name == 'nt': #sys.platform == 'win32':
                        pass
                        # if type(port)==str:
                        #         port=int(port.split("COM")[1])
                        

                elif os.name == 'posix':
                        if type(port)==int:
                                port="/dev/ttyS%d"%port
                else:
                        raise Exception("Sorry: no implementation for your platform ('%s') available" % os.name)
                #instanciate Serial object which is derivated from SerialBase class. refer to serialutil.py for arguments
        # for old version pySerial
                #hCom = serial.Serial(port, baudrate, timeout=timeout,interCharTimeout=interCharTimeout,rtscts=rtscts,xonxoff=xonxoff,rtsState=RTS,dtrState=DTR)
        # for pySerial 2.6
                hCom = serial.Serial(port, baudrate, bytesize, parity, stopbits, timeout, xonxoff, rtscts, interCharTimeout, 0)

                #rtn            
                # time.sleep(1)
                # hCom.write('AT\r')
                # print "send test AT command: "
                # print "AT"
                # time.sleep(2)
                # if hCom.inWaiting() < 6:
                #     print "Requested baudrate %s not working." % str(baudrate)
                #     print "Now try self-adaption:"
                #     for rate in [115200,9600,57600,38400,19200,4800,2400,1200,600,300]:
                #                 print "try : %s" % str(rate)
                #                 try:
                #                         hCom.baudrate = rate
                #                         hCom.write('AT\r')
                #                         time.sleep(2)
                #                         if hCom.inWaiting() >= 6:
                #                             print "%s is working" % str(rate)
                #                             print hCom.read(hCom.inWaiting()).replace('\r\n','<CR><LF>')
                #                             print "***Serial Port is working at %s baudrate VS requested %s***\n" % (str(rate),baudrate)
                #                             break
                #                         else:
                #                             hCom.flushInput()
                #                 except:
                #                     "problem when try %s " % str(rate)                        
                # else:
                #     print hCom.read(hCom.inWaiting())
                '''if DTR!=None:
                        hCom.setDTR(DTR)
                if RTS!=None:
                        hCom.setRTS(RTS)
                '''
                #add the new opened COM port to the list including all opened COM port
                list_hCom.append(hCom)
                SafePrint(None, hCom, "OPEN: Open the COM"+str(hCom.port)+" @"+str(baudrate)+" "+str(bytesize)+str(parity)+str(stopbits)+" "+str(flowcontrol),color = 4)
                time.sleep(1)

                global uartbuffer
                uartbuffer[hCom.port] = ""

                return hCom
        
        except serial.SerialException, val:
                print val
                if ("%s"%val).startswith("could not open port "):
                        SafePrint(None, None, "ERROR Could not open COM%d !"%(port),color = 9)
                        print "hCom" + str(hCom)
                else:
                        SafePrint(None, None, "ERROR : %s"%val,color = 9)
                #v1.8.1 CR2816 remove exception for Femto team : they wish to continue even if a COM port can't be opened
                #default : the exception is raised
                if VarGlobal.IsSystemStopsWhenhComFails == True:
                        raise COM_exception
                
        except AttributeError:
                SafePrint(None, None, "OPEN: Busy for %s!"%(hCom.port),color = 9)

def DisplayPortOpened():
        "goal of the method : This method displays all opened ports"
        "INPUT : none"
        "OUTPUT : none"
        global list_hCom
        for hCom in list_hCom:                                          
                SafePrint(None, hCom, hCom,color = 4)

def SagClose(hCom):
        "goal of the method : This method closes a COM port"
        "INPUT : hCom : COM port object"
        "OUTPUT : none"
        try:
        #print "close com port ", hCom.port
                # hCom.setDTR(0)
                # hCom.stop()
                # hCom.setDTR(1)
                hCom.close()    
                list_hCom.remove(hCom)
                SafePrint(None, hCom, "CLOSE: Close the %s"%(hCom.port),color = 4)
        except:                 
                SafePrint(None, hCom, "CLOSE: Error for %s"%(hCom.port),color = 9)

def SagStopAllPort():
        "goal of the method : This method closes all COM ports"
        "INPUT : none"
        "OUTPUT : none"
        # serial.stopAllPort()
        for hCom in list_hCom:
                # hCom.stop()
                hCom.close()

def SagReleaseAllComPort(release = True):
        "goal of the method : close or open all the COM ports"
        "INPUT : releaase : flag to indicate if COM ports are to stop (1) or to open (0)"
        "OUTPUT : none"
        if release:
                SafePrint(None, None, 'Release all COM ports',color = 4)
                for hCom in list_hCom:
                        hCom.stop()
                        hCom.close()
        else:
                SafePrint(None, None, 'ReOpen all COM ports',color = 4)
                for hCom in list_hCom:
                        hCom.open()

def SagCloseAll(silent = False):
        "goal of the method : this method closes all COM ports"
        "INPUT : silent : flag to display or not information on screen"
        "OUTPUT : none"
        if list_hCom != []:
                if not silent:
                        SafePrint(None, None, 'CLOSE: Close all COM ports',color = 4)
                for hCom in list_hCom:
                        #print "close com port ", hCom.port
                        try:
                                # if hCom.isOpen():
                                #         hCom.setDTR(0)
                                # hCom.stop()
                                # if hCom.isOpen():
                                #         hCom.setDTR(1)
                                hCom.close()
                        except:
                                SafePrint(None, hCom, "CLOSE: Error for %s"%(hCom.port),color = 9)
                SagSleep(150,silent=True)

def SagSend(hCom, cmd, silent=False):
        "                                                           "
        "   Not suggest to use anymore, replacement: SagSendAT()    "
        "                                                           "
        "goal of the method : this method sends an AT command on a COM port"
        "INPUT : hCom : COM port object"
        "        cmd : AT command to send"
        "        silent : flag to display or not information on screen"
        "OUTPUT : none"
        try:
                # if the COM port is close due to error in previous command reopen it
                if hCom.isOpen() == False:
                        hCom.open()
                
                #Clear input buffer, discarding all that is in the buffer
                hCom.flushInput()
                staticVariables.FcSave[0]=""
                staticVariables.FcSave[1]=None
                time.sleep(0.1)
                #Output the given string over the serial port
                hCom.write(str(cmd))
                
                timeDisplay = TimeDisplay()
                if not silent:
                        SafePrint(None, hCom, 'SEND: %s'%(cmd.replace('\r', '\\r').replace('\n', '\\n')),color = 6)
                
                # for test report
                VarGlobal.numOfCommand += 1.0
                # For Excel doc
                mystr = timeDisplay + ',' + '(' + str(hCom.port) + ')' + 'SEND: ' + str(cmd.replace('\r', '\\r').replace('\n', '\\n'))             
                VarGlobal.excelComment = VarGlobal.excelComment + mystr + '\r\n'
                # For xml tree
                '''XmlTree.xmlTree.AddNode('at_tx')
                XmlTree.xmlTree.SetContent(cmd.replace('\r', '\\r').replace('\n', '\\n'))
                XmlTree.xmlTree.GoToFather()
                '''
        except SystemExit:
                raise SystemExit
        
        except:
                #v1.8.1 CR2816
                if hCom == None:
                        SafePrintError(None,None, "SagSend : the COM port is not created and GlobalIsSystemStopWhenhComFails False")
                else:
                        hCom.close()                            
                        SafePrintError(None,hCom, "SEND: Error!")

                
        
def SagSendBin(hCom, tab, length=0, offset=0):
        "goal of the method : this method an hexa string on COM port"
        "INPUT : hCom : COM port object"
        "        tab : includes the hexa string to send"
        "               length : length of the hexa string to send"
        "       offset : offset from the beginning of the string to send"
        "OUTPUT : none"
        try:
                # if the COM port is close due to error in previous command reopen it
                if hCom.isOpen() == False:
                        hCom.open()
                hCom.flushInput()
                staticVariables.FcSave[0]=""
                staticVariables.FcSave[1]=None
                if length == 0:
                        length = len(tab)
                hCom.write(tab[offset:(offset+length)])
                SafePrint(None, hCom, 'SEND: Binary data',color = 4)
        except:
                hCom.close()
                SafePrintError(None,hCom, "SEND: Error!")

def SagSendFile(hCom, FileName, EOF = None, silent=True):
        "goal of the method : this method sends a file on COM port"
        "INPUT : hCom : COM port object"
        "        FileName : file to send"
        "        EOF : Enf Of File to send aftre the file, or None if nothng to send after the file"
        "        silent : flag to display or not information on screen"
        "OUTPUT : none"
        try:
                if hCom.isOpen() == False:
                        hCom.open()
                hCom.flushInput()
                staticVariables.FcSave[0]=""
                staticVariables.FcSave[1]=None
                time.sleep(0.1)
                
                file = open(FileName, 'rb')
                tab = file.read()
                file.close()
                
                SafePrint(None, hCom, 'SEND: Start Send File : %s'%(FileName),color = 4)
                dt = datetime.now()
                hCom.write(tab)
                if not(silent):
                        for elem in tab.splitlines(1):
                                SafePrint(dt, hCom, elem.replace("\r","\\r").replace("\n","\\n"),color = 4)
                if EOF != None:
                        hCom.write(EOF)
                        if not(silent):
                                SafePrint(dt, hCom, EOF.replace("\r","\\r").replace("\n","\\n"),color = 4)
                
                SafePrint(None, hCom, 'SEND: Send File : %s complet'%(FileName),color = 4)
        except:
                hCom.close()
                SafePrintError(None,hCom, "SEND: Error!")

def SagWaitTextFile(hCom, FileName="", file_size = 0, timeout=60000, EOF = chr(3), SOF='', silent=True): 
        "goal of the method : this method waits a text file from the COM port"
        "default timeout is 1 minute between each received packet"
        "INPUT : hCom : COM port object"
        "        FileName : file name to receive ; if elmpty, the default name is recv text.txt"
        "        file_size : file name size"
        "        timeout : timeout between each received packet"
        "        EOF : end of file to put at the ed of received file"
        "        SOF : ???"
        "        silent : flag to display or not information on screen"
        "OUTPUT : none"
        try:
                # if the COM port is close due to error in previous command reopen it
                if hCom.isOpen() == False:
                        hCom.open()
                
                taille = 50             # nb de barre de la barre de progression
                step = 10               # taille(ko) de chaque barre dans le cas ou la taille du fichier n'est pas connu
                
                # def des flag
                flagTimeout = False
                flagFind = False
                flagEOFFind = False
                flagError = False
                flagOldTime = False
                flagSOFFind = SOF == ''
                SAV_size = max(len(SOF),len(EOF))
                print (SAV_size)
                sav_buffer = ""
                file_buffer = ""
                
                percent_old = -1
                size = 0
                
                # First Caracter fc est '' par d?faut
                fc = ''
                line = []
                
                if FileName == "":
                        FileName = "recv text.txt"
                        FileName = FileName.split(".")[0] + " " + ("%s"%datetime.now()).split(".")[0].replace(":",".") + "." + FileName.split(".")[1]
                
                if os.path.isfile(FileName):
                        print "Replace data in file : %s"%FileName
                else:
                        print "Create file : %s"%FileName
                fic = open(FileName,'wb')
                
                SagActivatePrintOnGUI(2)
                
                start_time = datetime.now()
                while not(flagEOFFind) and not(flagTimeout):
                        # Attendre la reponse
                        flagTimeout = not(hCom.waitRXData(timeout))
                        
                        if not(flagTimeout) and hCom.inWaiting()>0:
                                #print "data detected"
                                # tempo pour avoir plus de donnee dans le buffer
                                time.sleep(0.01)
                                
                                # Recupere le buffer In du port com
                                serialBuffer = hCom.read(hCom.inWaiting())
                                dt = datetime.now()
                                
                                if not(flagEOFFind):
                                        if flagSOFFind:
                                                file_buffer += serialBuffer
                                                size = len(file_buffer.split(EOF)[0])
                                        
                                        if not(silent):
                                                VarGlobal.myColor = VarGlobal.colorLsit[7]
                                                sys.stdout.write(serialBuffer.split(EOF)[0])
                                                if serialBuffer.find(EOF)!=-1:
                                                        sys.stdout.write(EOF)
                                        else:
                                                if file_size !=0:
                                                        percent = size*100/file_size
                                                        if percent_old == -1:
                                                                VarGlobal.myColor = VarGlobal.colorLsit[7]
                                                                sys.stdout.write("\rDownload : %0.3d%% ["%(percent))
                                                                percent_old = percent
                                                                tx = ''
                                                                for j in range(taille):
                                                                        VarGlobal.myColor = "white" 
                                                                        tx += "|"
                                                                sys.stdout.write(tx)
                                                                VarGlobal.myColor = VarGlobal.colorLsit[7]
                                                                
                                                        if percent != percent_old:
                                                                VarGlobal.myColor = VarGlobal.colorLsit[7]
                                                                sys.stdout.write("\rDownload : %0.3d%% ["%(percent))
                                                                percent_old = percent
                                                                pas = 100/taille
                                                                if percent%(pas) == 0:
                                                                        tx = ''
                                                                        for j in range(percent/pas):
                                                                                VarGlobal.myColor = VarGlobal.colorLsit[2] 
                                                                                tx += "|"
                                                                        sys.stdout.write(tx)
                                                else:
                                                        nb = size/(1024*step)
                                                        if percent_old != nb:
                                                                percent_old = nb
                                                                sys.stdout.write("\rdownload in progress ( | = %sKo) : "%step)
                                                                VarGlobal.myColor = VarGlobal.colorLsit[6]
                                                                sys.stdout.write("|"*nb)
                                
                                if not(flagSOFFind) and (sav_buffer+serialBuffer).find(SOF) != -1:
                                        flagSOFFind = True
                                        fic.write((sav_buffer+serialBuffer).split(SOF,1)[-1])
                                        size += len((sav_buffer+serialBuffer).split(SOF,1)[-1])
                                        sav_buffer = ""
                                        serialBuffer = ""
                                
                                if (sav_buffer+serialBuffer).find(EOF) != -1:
                                        flagEOFFind = True
                                        VarGlobal.myColor = VarGlobal.colorLsit[7] 
                                        sys.stdout.write("\r\n")
                                        if len((sav_buffer+serialBuffer).split(EOF,1))==2:
                                                staticVariables.FcSave[0] = (sav_buffer+serialBuffer).split(EOF,1)[-1]
                                                staticVariables.FcSave[1] = dt
                                
                                if len(serialBuffer) < SAV_size:
                                        sav_buffer = sav_buffer[-(SAV_size-len(serialBuffer)):] + serialBuffer[-SAV_size:]
                                else:
                                        sav_buffer = serialBuffer[-SAV_size:]
                                
                                VarGlobal.myColor = VarGlobal.colorLsit[8]
                SagActivatePrintOnGUI(1)
                if flagTimeout:
                        VarGlobal.myColor = VarGlobal.colorLsit[9] 
                        print "\nERROR time out"
                        VarGlobal.myColor = VarGlobal.colorLsit[8]
                        VarGlobal.numOfFailedResponse += 1.0
                        VarGlobal.statOfItem = 'NOK'                    
                        VarGlobal.process_stat = 'NOK'
                        return [0, 0, False, 0]
                else:
                        duration = dt - start_time
                        print "Download size: %s octets"%(size)
                        if duration.seconds != 0 and VarGlobal.MODE != VarGlobal.DEMO_MODE:
                                print "Download time : %s"%(("%s"%(duration)).split(".")[0])
                                speed = float(size)/(1024*(duration).seconds)
                                print "Download speed average : %0.2dKo/s"%(speed)
                        else:
                                speed = 0
                        if file_size !=0:
                                print "Download successful :",size == file_size
                        
                        return [duration, size, size == file_size, speed]
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()    
                SafePrintError(None,hCom, "RECV: Error!")
        finally:
                fic.write(file_buffer.split(EOF)[0])
                fic.close()

def SagWaitCSDTextFile(hCom, file_name, file_size, timeout=60000): 
        "goal of the method : this method waits for a text file in CSD mode"
        "default timeout is 1 minute between each received packet"
        "INPUT : hCom : COM port object"
        "        FileName : file name to receive ; if elmpty, the default name is recv text.txt"
        "        file_size : file name size"
        "        timeout : timeout between each received packet"
        "OUTPUT : none"
        try:
                # if the COM port is close due to error in previous command reopen it
                if hCom.isOpen() == False:
                        hCom.open()
                
                # string attendue apres le telechargement
                taille = 50      # nb de barre de la barre de progression
                
                flag = False
                percent_old = -1
                size = 0
                
                # First Caracter fc est '' par d?faut
                fc = ''
                line = []
                start_time = datetime.now()
                start_time2 = -1
                
                if file_name == "":
                        file_name = "recv text.txt"
                        file_name = file_name.split(".")[0] + " " + ("%s"%datetime.now()).split(".")[0].replace(":",".") + "." + file_name.split(".")[1]
                
                if os.path.isfile(file_name):
                        fic = open(file_name,'wb')
                        #print "Replace data in file : %s"%file_name
                else:
                        fic = open(file_name,'wb')
                        #print "Create file : %s"%file_name
                
                SagActivatePrintOnGUI(2)
                while flag == False:
                        # Timeout operation 
                        end_time = datetime.now()
                        diff_time = (end_time - start_time).seconds * 1000.0 + (end_time - start_time).microseconds / 1000.0
                        if diff_time > timeout:
                                break                                    
                        
                        # Attendre donnee dans le buffer
                        if hCom.inWaiting() != 0:
                                if start_time2 == -1:
                                        start_time2 = datetime.now()
                                
                                start_time = datetime.now()
                                dt = start_time
                                currentTime = "%0.2d:%0.2d:%0.2d:%0.3d"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)
                                timeDisplay = '['+currentTime+']'
                                
                                # Traitement readline sp?cifique pour les lignes de commande AT
                                c = hCom.read(hCom.inWaiting())
                                print c
                                fic.write(c)
                                #sys.stdout.write("c :" + str(c)+"|\r\n")
                                size += len(c)
                                #sys.stdout.write(str(size)+"\r\n")
                                percent = size*100/file_size
                                if percent_old == -1:
                                        VarGlobal.myColor = VarGlobal.colorLsit[7]
                                        sys.stdout.write("\rDownload (%s): %0.3d%% ["%(hCom.port,percent))
                                        percent_old = percent
                                        tx="|"*taille
                                        VarGlobal.myColor = "white" 
                                        sys.stdout.write(tx)
                                        VarGlobal.myColor = VarGlobal.colorLsit[7] 
                                        sys.stdout.write("]")
                                        
                                if percent != percent_old:
                                        VarGlobal.myColor = VarGlobal.colorLsit[7]
                                        #sys.stdout.write("\rDownload (COM%d): %0.3d%% ["%(hCom.port,percent))
                                        sys.stdout.write("\rDownload (%s): %0.5d%% ["%(hCom.port,size))
                                        percent_old = percent
                                        pas = 100/taille
                                        if percent%(pas) == 0:
                                                tx="|"*(percent/pas)
                                                sys.stdout.write(tx)
                        
                        if size >= file_size:
                                VarGlobal.myColor = VarGlobal.colorLsit[7] 
                                sys.stdout.write("\r\n")
                                flag = True
                                
                        VarGlobal.myColor = VarGlobal.colorLsit[8]
                                
                SagActivatePrintOnGUI(1)
                if diff_time > timeout:
                        VarGlobal.myColor = VarGlobal.colorLsit[9] 
                        print "\nERROR time out"
                        VarGlobal.myColor = VarGlobal.colorLsit[8]
                        VarGlobal.numOfFailedResponse += 1.0
                        VarGlobal.statOfItem = 'NOK'                    
                        VarGlobal.process_stat = 'NOK'
                        return [0, 0, False, 0]
                else:
                        duration = dt - start_time2
                        print "Download time : %s"%(("%s"%(duration)).split(".")[0])
                        print "Download size: %s octets"%(size)
                        if duration.seconds != 0:
                                speed = float(size)/(duration).seconds
                                print "Download speed average : %do/s"%(speed)
                        else:
                                speed = 0
                                print "Download speed average : error"
                        if file_size !=0:
                                print "Download successful :",size == file_size
                        
                        return [duration, size, size == file_size, speed]
        except SystemExit:
                raise SystemExit
        
        except:
                hCom.close()
                VarGlobal.myColor = VarGlobal.colorLsit[9]                                                              
                SafePrintError(None,hCom, "RECV: Error!")
                VarGlobal.myColor = VarGlobal.colorLsit[8]

def SagWaitLine(hCom, waitline, timeout=60000, critical = False, errorKeyWords = []): 
        "                                                           "
        "   Not suggest to use anymore, replacement: SagWaitResp()  "
        "                                                           "
        "goal of the method : this method waits for the data received from Com port"
        "It check also if one received line starts with one of the keywords cincluded either in waitline or inerrorKeyWords"
        "INPUT : hCom : COM port object"
        "        waitline : list of keywords ; the check is successul if one of them is found at the beginning of 1 line in received data"
        "        timeout (ms) : timeout between each received packet"
        "        critical : flag ; if True and if no keyword is found, an exception is raised"
        "        errorKeyWords : list of error keywords ; the check is successul if one of them is found at the beginning of 1 line in received data"
        "OUTPUT : response object"
        
        try:
                if type(waitline)==str:
                        waitline = [waitline]
                # if the COM port is close due to error in previous command reopen it
                if hCom.isOpen() == False:
                        hCom.open()
                
                # Response object
                res = Response()
                
                flagTimeout = False
                flagFind = False
                flagError = False
                flagOldTime = False
                flagFcOnStart = False

                # number of received lines
                cpt_line = 0
                
                # fc : First Caracters
                #we need complete lines with CR LF at the end
                #if more data is received, it is saved in FcSave and will inserted at the beginning of received data next time
                fc = staticVariables.FcSave[0]
                #if there is data previously saved
                if fc !="":
                        #set the flag which mean previously saved data shall be inserted at the beginning
                        flagFcOnStart = True
                        #time of reception of previously saved data
                        dt_fc_tmp = staticVariables.FcSave[1]
                        staticVariables.FcSave[0]=""
                        staticVariables.FcSave[1]=None
                # array of received data
                line = []
                
                # memorize current time to compute timeout
                start_time = datetime.now()
                
                Timeout = timeout
                #wait for data until to have some stuff, or timer expiration
                while not(flagTimeout or flagFind or flagError):
                        #if not flagFcOnStart:
                        #       flagTimeout = not(SagWaitRXData(hCom,Timeout,silent=True))
                        #print "SagWaitRXData()", flagTimeout
                        #if either data in input buffer, or previously saved data
                        if not(flagTimeout) and hCom.inWaiting()>0 or flagFcOnStart:
                                # just to have a little bit more data un input buffer
                                time.sleep(0.001)

                                #if no data previously saved
                                if not flagFcOnStart:
                                        # inWaiting returns the nb of characters currently in the input buffer
                                        #so we read all data included in input bufferS
                                        serialBuffer = hCom.read(hCom.inWaiting())
                                        dt = datetime.now()  # memorize the current time of data reception
                                        # the reception time of fc data has been memorised and is going to be used
                                        if fc != "" and str(serialBuffer)[0] != '\n':
                                                #NJF : normally impossible : we are in not flagFcOnStart, so fc shall be null
                                                dt_fc = dt_fc_tmp
                                                flagOldTime = True
                                        else:
                                                flagOldTime = False
                                #if data previously saved
                                else:
                                        serialBuffer = ""
                                        flagFcOnStart = False
                                        dt = dt_fc_tmp
                                
                                #add fc at the begin of line (NJF : even if fc is empty)
                                #splitlines return a list of the lines in the string, breaking at line boundaries (keep boundary because of 1)
                                line  = (fc + serialBuffer).splitlines(1)
                                fc=""
                                
                                # remove last item of array and save it in fc (only if last item doesn't finish by '\r\n' or is different from '> ' or the first item doesn't finish by '\r')
                                #L[-1] is used to access the last item in the list
                                #L.pop() removes the last item
                                #find returns the lowest index of the found substring ; returns -1 if not found
                                #if the list doesn't finish with \r\n and not by > and don't find \r
                                if not( line[-1].endswith("\r\n") or \
                                                line[-1]=="> " or \
                                                (line[-1].find("\r")!=-1 and cpt_line == len(line)-1 and len(line[-1])>3 ) ):
                                        #it exists a pb if the echo finishes by \r\n and if \n is after, then \n will be confused with data instead of the end of echo
                                        fc = line.pop()
                                        dt_fc_tmp=dt    # save time of arrival
                                
                                # put all items of list into a string
                                for elem in line:
                                        res.tabData += elem
                                
                                cpt_line += len(line)
                                
                                # Traitement de echo et tabLine
                                if len(line)>0:
                                        timeDisplay = TimeDisplay(dt)
                                        # echo
                                        #2 last conditions : to avoid to confuse "notif" or "connect" with echo
                                        if (line[0] != "\r\n") and (cpt_line == len(line)) and line[0] != "\r" and not(line[0].startswith("+")) and not(line[0].startswith("CONNECT")): 
                                                # remove the first item of list : l echo
                                                res.echo = line.pop(0).replace('\n', '\\n').replace('\r', '\\r') 
                                                SafePrint(dt,   hCom, "ECHO: %s"%(res.echo), color = 5)
                                                # add for Excel
                                                mystr = timeDisplay +',' + '(COM' + str(hCom.port) + ')' + 'ECHO: ' + str (res.echo)          
                                                VarGlobal.excelComment = VarGlobal.excelComment + mystr + '\r\n'
                                        
                                        #data
                                        for elem in line:
                                                if flagOldTime:
                                                        timeDisplay2 = TimeDisplay(dt_fc)
                                                        flagOldTime = False
                                                        dt = dt_fc
                                                else:
                                                        timeDisplay2 = timeDisplay
                                                res.tabLines.append((elem, timeDisplay2))
                                                tmp = elem.replace('\r', '\\r').replace('\n', '\\n')
                                                SafePrint(dt, hCom, "RECV: %s"%(tmp), color = 7)
                                                # add for Excel         
                                                mystr = timeDisplay2 + ',' + '(COM' + str(hCom.port) + ') ' + 'RECV: ' + str(tmp)             
                                                VarGlobal.excelComment = VarGlobal.excelComment + mystr + '\r\n'
                                
                                # check if one keyword is found in the list
                                for elem in waitline + errorKeyWords:
                                        for ligne in line:
                                                if ligne.startswith(elem):
                                                        if elem in waitline:
                                                                flagFind = True
                                                                res.res = elem
                                                                res.find = True
                                                        elif elem in errorKeyWords:
                                                                flagError = True
                                                                res.res = elem
                                                        break
                                                
                                                # exit if ERROR ou +CME ERROR
                                                if (ligne.startswith("ERROR") or ligne.startswith("+CME ERROR")) and staticVariables.ExitWhenErrorValue:
                                                        flagError = True
                                                        res.res = elem
                                                        break
                                        
                                        if flagFind or flagError:
                                                break
                        
                        #check if timeout has expired
                        diff = datetime.now() - start_time
                        Timeout = timeout - (diff.seconds * 1000 + diff.microseconds / 1000)
                        
                        #if timeout expired, the read is stopped
                        if Timeout <= 0 or flagTimeout:
                                SafePrint(None, hCom,"RECV: ERROR time out",color = 7)
                                # display the non complete line
                                if fc != "":
                                        SafePrint(dt_fc_tmp, hCom,"RECV non complete line :%s"%(fc),color = 7)
                                flagTimeout = True
                
                #save fc and its time of arrival
                staticVariables.FcSave[0] = fc
                if fc != "":
                        staticVariables.FcSave[1] = dt_fc_tmp
                else:
                        staticVariables.FcSave[1] = None
                
                res.totalTime = diff
                
                if flagFind:
                        VarGlobal.numOfResponse += 1
                elif len(waitline) > 0:
                        VarGlobal.numOfResponse += 1
                
                # For xml tree
                XmlTree.xmlTree.AddNode('at_rx')
                cpt_line = 0
                for elem in res.tabLines:
                        cpt_line += 1
                        XmlTree.xmlTree.AddNode('line%d'%cpt_line)
                        XmlTree.xmlTree.AddNode('notif')
                        tmp = elem[0].replace('\r', '\\r')
                        tmp = tmp.replace('\n', '\\n')
                        XmlTree.xmlTree.SetContent(tmp)
                        XmlTree.xmlTree.GoToFather()
                        XmlTree.xmlTree.AddNode('time')
                        XmlTree.xmlTree.SetContent(elem[1])
                        XmlTree.xmlTree.GoToFather()
                        XmlTree.xmlTree.GoToFather()
                XmlTree.xmlTree.GoToFather()
                
                if flagFind == False and critical:
                        raise no_receive_exception
                
                return res
        
        except SystemExit:
                #v1.8.1 CR2816
                if hCom == None:
                        SafePrintError(None,None, "SagWaitLine : the COM port is not created and GlobalIsSystemStopWhenhComFails False")
                else:
                        hCom.stop()
                raise SystemExit
        except no_receive_exception:
                #v1.8.1 CR2816
                if hCom == None:
                        SafePrintError(None,None, "SagWaitLine : the COM port is not created and GlobalIsSystemStopWhenhComFails False")
                else:
                        hCom.stop()
                raise no_receive_exception
        except:
                #v1.8.1 CR2816
                if hCom == None:
                        SafePrintError(None,None, "SagWaitLine : the COM port is not created and GlobalIsSystemStopWhenhComFails False")
                else:
                        hCom.stop()
                        hCom.close()
                        SafePrintError(None,hCom, "RECV: Error!")
                return None

def SagWaitAndTestLine(hCom, waitline, errorKeyWords = [], timeout=60000, critical = False): 
        "                                                                 "
        "   Not suggest to use anymore, replacement: SagWaitnMatchResp()  "
        "                                                                 "
        "goal of the method : this method waits for the data received from Com port"
        "It check also if one received line starts with one of the keywords cincluded either in waitline or inerrorKeyWords"
        "it replaces the 2 following methods : SagWaitLine() & SagTestCmd()"
        "INPUT : hCom : COM port object"
        "        waitline : list of keywords ; the check is successul if one of them is found at the beginning of 1 line in received data"
        "        errorKeyWords : list of error keywords ; the check is successul if one of them is found at the beginning of 1 line in received data"
        "        timeout (ms) : timeout between each received packet"
        "        critical : flag ; if True and if no keyword is found, an exception is raised"
        "OUTPUT : Response instance"
        
        result = SagWaitLine(hCom, waitline[-1], timeout = timeout, errorKeyWords=errorKeyWords, critical=critical)
        
        #if one of the keywords has been found
        if result.find:
                result.isOK = SagTestCmd(result, waitline, critical)
        else:
                VarGlobal.myColor = VarGlobal.colorLsit[9]
                VarGlobal.excelComment = VarGlobal.excelComment + "!!! Failed, expected response was : " + str(waitline) + '\r\n'
                VarGlobal.excelCommentGlobal += VarGlobal.excelComment          
                print "!!! Failed, expected response was : " + str(waitline)
                VarGlobal.myColor = VarGlobal.colorLsit[8]
                VarGlobal.numOfFailedResponse += 1.0
                if critical:
                        raise receive_exception
                
                VarGlobal.statOfItem = 'NOK'                    
                VarGlobal.process_stat = 'NOK'
        
        return result

def SagReadBin(hCom, length=-1, timeout=60000):
        "goal of the method : this method reads the data from the hCom COM port"
        "INPUT : hCom, COM port instance"
        "                legnth, length of data to receive. By default -1 to detect automaticcaly the data length"
        "                timeout (ms), guard timer for data reception"
        "OUTPUT : BinData instance"
        try:
                # if the COM port is close due to error in previous command reopen it
                if hCom.isOpen() == False:
                        hCom.open()
                
                if length == -1:
                        length = hCom.inWaiting()
                
                res = BinData()
                tmp = ''
                start_time = datetime.now()
                for i in range(length):
                        # loop while there is nothing in hCom, until timeout expires
                        while tmp == '':
                                # Timeout operation 
                                end_time = datetime.now()
                                diff_time = (end_time - start_time).seconds * 1000.0 + (end_time - start_time).microseconds / 1000.0
                                if diff_time > timeout:
                                        res.length = len(res.tabData)
                                        return res                                       
                                # read hCom buffer
                                tmp = hCom.read()
                        res.tabData += tmp
                        tmp = ''
                
                res.length = len(res.tabData)
                return res 
        
        except SystemExit:
                raise SystemExit
        
        except:
                hCom.close()                            
                SafePrintError(None,hCom, "RECV: Error!")
                return res 


def SagPrintResp(res, flag=True):
        "goal of the method : this method displays the content of Response instance"
        "INPUT : res, Response instance to display"
        "                flag, boolean flag to know if the instance shall be displayed"
        "OUTPUT : none"
        try:
                # Un flag pour dire si on affiche la r?ponse en d?tail
                if flag == False:
                        return
                
                # acquire the MUTEX lock ; the Safeprint is not used because the following is not an atomic operation
                print_mutex.acquire()  
                
                print "-------------------------- Response Detail --------------------------"
                if res == None:
                        print " ATTENTION: Response is None."
                        print "---------------------------------------------------------------------"
                        return
                
                print "Response: %s"%res.res
                print "Command Echo: %s"%res.echo.replace('\r', '\\r')
                
                # Afficher tabData qui est une tableau de tous les caract?res re?us en binaire
                print "Response In Hexa:"
                chain_hexa = ''
                for carac in res.tabData:
                        chain_hexa += "\\x%.2x"%ord(carac)
                
                div = len(chain_hexa) / 68 
                mod = len(chain_hexa) % 68
                for i in range(div):
                        print chain_hexa[i*68:i*68+68]+'\\'
                
                print chain_hexa[div*68:div*68+68]
                
                # Afficher tabLines qui est un tableau des lignes 
                print " Response Lines:"
                for line in res.tabLines:
                        print " - (%s, %s)"%(line[0].replace('\r\n', '\\r\\n'), line[1])

                # Afficher tabParse qui est une tableau contenant les ligne pars?
                print " Response Lines Parse:"
                print "  List:"
                print res.tabParse
                print "  Detail:"
                for line in res.tabParse:
                        if line[0] == 'RES_CODE':
                                print " - %s: %s"%(line[0], line[1])
                        elif line[0] == 'INFO_RESP':
                                print " - %s:" %line[0]
                                for elem in line[1]:
                                        if len(elem) == 0: 
                                                print "  - "
                                        elif elem[0] != 'LIST':
                                                print "  - %s: %s"%(elem[0], elem[1])
                                        else:
                                                print "  - %s:"%elem[0]
                                                for param in elem[1]:
                                                        if len(param) == 0:
                                                                print "         - "
                                                        else:
                                                                print "         - %s: %s"%(param[0], param[1])

                # Afficher le temps total utilis? 
                
                print "Total Time: %d milliseconds"%res.totalTime
                print "---------------------------------------------------------------------"

                # release the MUTEX lock
                print_mutex.release()
        
        except SystemExit:
                raise SystemExit
        
        except:
                SafePrintError(None,None, "PRINT_RESP: Error!")

def SagReadFile(filename,silent=False):
        "goal of the method : this method reads a file in bnary mode and put the data into an array"
        "INPUT : filename, name of the file from which to read the data"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : data readen"
        try:
                file = open(filename, 'rb')
                tab = file.read()
                file.close()
                if not(silent):
                        SafePrint(None, None, 'READ_FILE: Read file %s' % filename,color = 6)
                return tab
        
        except SystemExit:
                raise SystemExit
        
        except:                                 
                SafePrintError(None,None, 'READ_FILE: Read file %s Error!' % filename)
                return '' 

def SagWriteFile(filename, tab):
        "goal of the method : this method is to write the content of an array into a binary file"
        "INPUT : filename, name of the file to write the data"
        "                tab, content of the array to write into the file"
        "OUTPUT : none"
        try:
                file = open(filename, 'wb')
                file.write(tab)
                file.close()
                SafePrint(None, None, 'WRITE_FILE: Write file %s' % filename,color = 6)
        
        except SystemExit:
                raise SystemExit
        
        except:
                SafePrintError(None,None, 'WRITE_FILE: Write file %s Error!' % filename)

def SagSleep(millisecond, silent=False):
        "goal of the method : this method sleep during x milliseconds"
        "INPUT : milliseconds (ms), sleep duration"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : none"
        try:
                if not(silent):
                        SafePrint(None, None, "SLEEP: Start sleep for %d milliseconds" % millisecond,color = 6)
                threading.Event().wait(millisecond/1000.0)
                if not(silent):
                        SafePrint(None, None, "SLEEP: End sleep",color = 6)
        
        except SystemExit:
                raise SystemExit
        
        except:
                SafePrintError(None,None, "SLEEP: Error!")

def SwiSleep(millisecond, silent=False):
        "goal of the method : this method sleep during x milliseconds"
        "Created by Rtang to remove problem when run on win8"
        "INPUT : milliseconds (ms), sleep duration"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : none"
        try:
                if not(silent):
                        SafePrint(None, None, "SLEEP: Start sleep for %d milliseconds" % millisecond,color = 6)
                time.sleep(millisecond/1000.0)
                if not(silent):
                        SafePrint(None, None, "SLEEP: End sleep",color = 6)
        
        except SystemExit:
                raise SystemExit
        
        except:
                SafePrintError(None,None, "SLEEP: Error!")
        
def SagStartThread(fonc, *args):
        "goal of the method : this method starts a thread which will execute fonc method (e.g. SagSendBin)"
        "INPUT : fonc method name to execute in the thread"
        "        *args arguments needed to call the method"
        "OUTPUT : the thread instance"
        try:
                if len(args)==1 and type(args[0])==list:
                        args = args[0]
                thread = Thread(target=fonc, args=args)
                if VarGlobal.MODE != VarGlobal.DEMO_MODE:
                        SafePrint(None, None, 'THREAD: Thread %s> start'%str(fonc).split(" at 0x")[0],color = 8)
                thread.setName(str(fonc).split(" at 0x")[0].split(" ",1)[1])
                if VarGlobal.DEBUG_LEVEL == "DEBUG":
                        print "SagStartThread() thread Thread is starting\r\n"
                        print "@@@thread launched@@@\r\n"
                thread.start()
                return thread
        
        except SystemExit:
                raise SystemExit
        
        except:
                SafePrintError(None,None, "THREAD: Start Thread Error!")

def SagStopAllThread(silent=False):
        "goal of the method : this method stops all threads"
        "INPUT : silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : none"
        try:
                StopAllThread()
                if not(silent):
                        SafePrint(None, None, "Stop all thread",color = 8)
        except SystemExit:
                pass

def SagStopAllThreadWithout(threads):
        "goal of the method : this method stops all threads which are not in list"
        "INPUT : threads, list of threads to keep"
        "OUTPUT : none"
        if type(threads) != list:
                threads = [threads]
        
        for thread in threading.enumerate():
                if thread.getName() not in ["MainThread", "Test"] and thread not in threads:
                        SafePrint(None, None, "Stop thread %s"%str(thread.getName()),color = 8)
                        # thread.stop()
                        thread.join(0.1)

def SagStopThread(thread):
        "goal of the method : this method stops the thead in argument"
        "INPUT : thread, thread to stop"
        "OUTPUT : none"
        if thread in threading.enumerate():
                if thread.isAlive():
                        if VarGlobal.MODE != VarGlobal.DEMO_MODE:
                                SafePrint(None, None, "Stop thread %s"%str(thread.getName()),color = 8)
                        #thread.stop()
                        thread.join(0.1)
        else:
                SafePrintError(None,None,"Thread not found")

def SagPauseAllThread(silent=False):
        "goal of the method : this method pauses all threads"
        "INPUT : silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : none"
        PauseAllThread()
        if not(silent):
                SafePrint(None, None, "Pause all thread",color = 8)

def SagPauseThread(thread,silent=False):
        "goal of the method : this method pauses the thread given in argument"
        "INPUT : thread, thread to pause "
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : "
        if thread in threading.enumerate():
                if not(silent):
                        SafePrint(None, None, "Pause thread %s"%str(thread.getName()),color = 8)
                thread.Pause()
        elif not(silent):
                SafePrintError(None,None,"Thread not found")

def SagContinueAllThread(silent=False):
        "goal of the method : this method unpauses all threads"
        "INPUT : silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : none"
        ContinueAllThread()
        if not(silent):
                SafePrint(None, None, "Continue all thread",color = 8)

def SagContinueThread(thread,silent=False):
        "goal of the method : this method "
        "INPUT : thread, thread to unpause"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : "
        if thread in threading.enumerate():
                if not(silent):
                        SafePrint(None, None, "Pause thread %s"%str(thread.getName()),color = 8)
                thread.Continue()
        elif not(silent):
                SafePrintError(None,None,"Thread not found")

def SagWaitEndOfThread(thread,timeout=30000):
        "goal of the method : this method waits for the end of a thread"
        "INPUT : thread, thread to pause "
        "                timeout (ms), timer to wait the end of thread"
        "OUTPUT : TBC"
        try:
                #if staticVariables.List_Thread.count(thread)>0:
                if threading.enumerate().index(thread):
                        if VarGlobal.MODE != VarGlobal.DEMO_MODE:
                                if timeout == None:
                                        SafePrint(None,None,"Wait End of Thread %s"%(thread.getName()),8)
                                else:
                                        SafePrint(None,None,"Wait End of Thread %s durring %s sec"%(thread.getName(),timeout/1000.0),8)
                        
                        result = thread.WaitEndOfThread(timeout)
                        
                        if VarGlobal.MODE != VarGlobal.DEMO_MODE:
                                if result:
                                        SafePrint(None,None,"End of Thread %s detect"%(thread.getName()),8)
                                else:
                                        SafePrint(None,None,"Timeout thread %s still in running"%(thread.getName()),8)
                        
                        return result
                else:
                        SafePrint(None,None,"Thread not found",8)
        except SystemExit:
                raise SystemExit
        except:
                SafePrintError(None,None,"Thread not found")

def SagCreateEvent(name,silent=False):
        "goal of the method : this method creates an event for threads"
        "An event manages a flag that can be set to true with the set() method and reset to false with the clear() method. "
        "The wait() method blocks until the flag is true."
        "INPUT : name, event name"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : SagEvent instance"
        try:
                event = SagEvent(name)
                if not silent:
                        SafePrint(None, None, 'THREAD: Create Event %s'%event.name,color = 6)
                return event
        
        except SystemExit:
                raise SystemExit
        
        except:
                SafePrintError(None,None, 'THREAD: Create Event %s Error!'%event.name)
                return None


def WaitEvent(event,timeout=None):
        "goal of the method : this method waits for the event : event"
        "INPUT : event, SagEvent instance"
        "                timeout (ms), timer to wait the end of thread"
        "OUTPUT : boolean, True if the event has been reached"
        if timeout != None:
                timeout = timeout/1000.0
                start = datetime.now()
                event.wait(timeout)
                diff = datetime.now() - start
                event.clear()
                diff_time = diff.seconds + diff.microseconds / 1000000.0
                return diff_time < timeout
        else:
                event.wait()
                event.clear()
                return True

def SagWaitEvent(hCom, event, timeout=60000,silent=False):
        "goal of the method : this method waits for the event"
        "INPUT : hCom, COM port instance"
        "                event, SagEvent instance"
        "                timeout (ms), timer to wait the end of thread"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : boolean, True if the event has been reached"
        try:
                if not silent:
                        SafePrint(None, hCom, 'THREAD: Wait Event %s'%(event.name), color = 6)
                EvtOK = WaitEvent(event, timeout)
                if not silent:
                        SafePrint(None, hCom, 'THREAD: Wait Event %s is recieve :%s'%(event.name, EvtOK), color = 6)
                return EvtOK
        
        except SystemExit:
                raise SystemExit
        
        except:
                SafePrintError(None,hCom, 'THREAD: Wait Event %s Error!'%(event.name))# Cette fonction fait r?veiller tous les threads qui attendent un event

def SagSetEvent(hCom, event):
        "goal of the method : this method sets an event"
        "INPUT : hCom, COM port instance"
        "                event, SagEvent instance"
        "OUTPUT : none"
        try:
                event.event.set()
                event.event.clear()
                SafePrint(None, hCom, 'THREAD: Set Event %s'%(event.name),color = 6)
        
        except SystemExit:
                raise SystemExit
        
        except:
                SafePrintError(None,hCom, 'THREAD: Set Event %s Error!'%(event.name))

def SagCleanBuffer(hCom):
        "goal of the method : this method clears the input buffer of hCom COM port instance"
        "INPUT : hCom, COM port instance"
        "OUTPUT : none"
        try:
                hCom.flushInput()
        
        except SystemExit:
                raise SystemExit
        
        except:
                hCom.close()
                SafePrintError(None,hCom, "CLEAR_BUFFER: Error!")

def SagIsOpen(hCom):
        "goal of the method : this method checks if a COM port is opened"
        "INPUT : hCom, COM port instance"
        "OUTPUT : boolean, True if COM port is opened"
        if hCom.isOpen():
                SafePrint(None, hCom, "MESSAGE: The COM%d is opened.",color = 6)
                return True
        else:
                SafePrintError(None,hCom, "MESSAGE: The COM%d is not opened.")
                return False

def SagSetBaudrate(hCom, baudrate):
        "goal of the method : this method set the baudrate of hCom COM port"
        "INPUT : hCom, COM port instance"
        "                baudrate, ben it is the baudrate"
        "OUTPUT : none"
        try:
                hCom.baudrate = baudrate
                SafePrint(None, hCom, 'SET_BAUDRATE: %d'%(baudrate),color = 6)
        
        except SystemExit:
                raise SystemExit
        
        except:
                hCom.close()
                SafePrintError(None,hCom, "SET_BAUDRATE: Error! Valid Value: (2400,4800,9600,...)")

def SagSetBytesize(hCom, bytesize):
        "goal of the method : this method set the bytesize of hCom COM port"
        "INPUT : hCom, COM port instance"
        "                bytesize, ben it is the baudrate"
        "OUTPUT : none"
        try:
                hCom.bytesize = bytesize
                SafePrint(None, hCom, 'SET_BYTESIZE: %d'%(bytesize),color = 6)
        
        except SystemExit:
                raise SystemExit
        
        except:
                hCom.close()
                SafePrintError(None,hCom, "SET_BYTESIZE: Error! Valid Value: (5,6,7,8)")

def SagSetParity(hCom, parity):
        "goal of the method : this method set the bit parity of hCom COM port"
        "INPUT : hCom, COM port instance"
        "                parity, ben it is the bit parity"
        "OUTPUT : none"
        try:
                hCom.parity = parity
                if hCom.parity == 'N':
                        SafePrint(None, hCom, 'SET_PARITY: %s'%('None'),color = 6)
                elif hCom.parity == 'E':
                        SafePrint(None, hCom, 'SET_PARITY: %s'%('Parity Even'),color = 6)
                elif hCom.parity == 'O':
                        SafePrint(None, hCom, 'SET_PARITY: %s'%('Parity Odd'),color = 6)
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "SET_PARITY: Error! Valid Value: ('N','E','O')")

def SagSetStopbits(hCom, stopbits):
        "goal of the method : this method set the stop bit of hCom COM port"
        "INPUT : hCom, COM port instance"
        "                stopbits, ben it is the stop bit"
        "OUTPUT : none"
        try:
                hCom.stopbits = stopbits
                SafePrint(None, hCom, 'SET_STOPBITS: %d'%(stopbits),color = 6)
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "SET_STOPBITS: Error! Valid Value: (1,2)")

def SagSetParamDefault(hCom):
        "goal of the method : this method set default parameters of hCom COM port"
        "the default parameters are speed=9600bauds, bytesize=eight bits, no parity, 1 stop bit, timeout enabled, no soft flow control"
        "RTS/CTS flow control disabled"
        "INPUT : hCom, COM port instance"
        "OUTPUT : none"
        try:
                hCom.baudrate = 9600
                hCom.bytesize = serial.EIGHTBITS
                hCom.parity   = serial.PARITY_NONE
                hCom.stopbits = serial.STOPBITS_ONE
                hCom.timeout  = 1
                hCom.xonxoff  = 0
                hCom.rtscts   = 0
                SafePrint(None, hCom, 'SET_PARAM: Set Default Parameter',color = 6)
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "SET_PARAM: Set Default Paramter Error!")

def SagSetFlowControl(hCom, Enable=True):
        "goal of the method : this method enables or disables the hardware flow control"
        "INPUT : hCom, COM port instance"
        "                Enable, boolean flag to enable or disable flow control"
        "OUTPUT : none"
        try:
                hCom.setRtsCts(Enable)
                SafePrint(None, hCom, "SET Flow Control: %s"%(Enable),color = 6)
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "SET Flow Control: Error!")

def SagGetFlowControl(hCom):
        "goal of the method : this method get the hardware flow control status"
        "INPUT : hCom, COM port instance"
        "OUTPUT : none"
        try:
                Enable = hCom.getRtsCts()==1
                SafePrint(None, hCom, "GET Flow Control: %s"%(Enable),color = 6)
                return Enable
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "SET Flow Control: Error!")

def SagSetRTS(hCom, level, silent=False):
        "goal of the method : this method set the RTS at given level"
        "INPUT : hCom, COM port instance"
        "                level, level to set the RTS"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : none"
        try:
                hCom.setRTS(level)
                if not silent:
                        SafePrint(None, hCom, "SET_RTS: %d"%(level),color = 6)
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "SET_RTS: Error!")

def SagSetDTR(hCom, level, silent=False):
        "goal of the method : this method set the DTR at given level"
        "INPUT : hCom, COM port instance"
        "                level, level to set the DTR"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : none"
        try:
                hCom.setDTR(level)
                if not silent:
                        SafePrint(None, hCom, "SET_DTR: %d"%(level),color = 6)
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "SET_DTR: Error!")

def SagGetCTS(hCom, silent=False):
        "goal of the method : this method get the CTS level"
        "INPUT : hCom, COM port instance"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : none"
        try:
                CTS = hCom.getCTS()
                if not silent:
                        SafePrint(None, hCom, "GET_CTS: CTS = %d"%(CTS),color = 6)
                return CTS
        except SystemExit:
                raise SystemExit
        except serial.SerialException:
                raise
        except:
                hCom.close()
                SafePrintError(None,hCom, "GET_CTS: Error!")
                return None

def SagGetDSR(hCom, silent=False):
        "goal of the method : this method get the DSR level"
        "INPUT : hCom, COM port instance"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : none"
        try:
                DSR = hCom.getDSR()
                if not silent:
                        SafePrint(None, hCom, "GET_DSR: DSR = %d"%(DSR),color = 6)
                return DSR
        except SystemExit:
                raise SystemExit
        except serial.SerialException:
                raise
        except:
                hCom.close()
                SafePrintError(None,hCom, "GET_DSR: Error!")
                return None

def SagGetRI(hCom, silent=False):
        "goal of the method : this method get the RING level"
        "INPUT : hCom, COM port instance"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : none"
        try:
                RI = hCom.getRI()
                if not silent:
                        SafePrint(None, hCom, "GET_RI: RI = %d"%(RI),color = 6)
                return RI
        except SystemExit:
                raise SystemExit
        except serial.SerialException:
                raise
        except:
                hCom.close()
                SafePrintError(None,hCom, "GET_RI: Error!")
                return None

def SagGetCD(hCom, silent=False):
        "goal of the method : this method get the CD level"
        "INPUT : hCom, COM port instance"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : none"
        try:
                CD = hCom.getCD()
                if not silent:
                        SafePrint(None, hCom, "GET_CD: CD = %d"%(CD),color = 6)
                return CD
        except SystemExit:
                raise SystemExit
        except serial.SerialException:
                raise
        except:
                hCom.close()
                SafePrintError(None,hCom, "GET_CD: Error!")
                return None

def SagWaitRXData(hCom, timeout=30000, silent=False):
        "goal of the method : this method waits for data in hCom input buffer"
        "INPUT : hCom, COM port instance"
        "                timeout (ms), guard timer while waiting for signal"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : Boolean, True if signal received"
        try:
                if not(silent):
                        if timeout!=0:
                                SafePrint(None, hCom, "Wait DATA during :%ss"%(timeout/1000.0),color = 4)
                        else:
                                SafePrint(None, hCom, "Wait DATA",color = 4)
                        start = datetime.now()
                recv = hCom.waitRXData(timeout)
                if not(silent):
                        if recv:
                                diff = datetime.now() -start
                                SafePrint(None, hCom, "DATA detect after %ss"%((diff.seconds + diff.microseconds/1000000.0)),color = 6)
                        else:
                                SafePrint(None, hCom, "Can't detect DATA",color = 4)
                return recv
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "Wait DATA: Error!")
                return None

def SagWaitCTS(hCom, timeout=30000, silent=False):
        "goal of the method : this method waits for CST signal"
        "INPUT : hCom, COM port instance"
        "                timeout (ms), guard timer while waiting for signal"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : Boolean, True if signal received"
        try:
                if not(silent):
                        if timeout!=0:
                                SafePrint(None, hCom, "Wait CTS during :%ss"%(timeout/1000.0),color = 4)
                        else:
                                SafePrint(None, hCom, "Wait CTS",color = 4)
                        start = datetime.now()
                
                recv = hCom.waitCTS(timeout)
                if not(silent):
                        if recv:
                                diff = datetime.now() -start
                                SafePrint(None, hCom, "CTS detect after %ss"%((diff.seconds + diff.microseconds/1000000.0)),color = 4)
                        else:
                                SafePrint(None, hCom, "Can't detect CTS",color = 4)
                return recv
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "Wait CTS: Error!")
                return None

def SagWaitDSR(hCom, timeout=30000, silent=False):
        "goal of the method : this method waits for DSR signal"
        "INPUT : hCom, COM port instance"
        "                timeout (ms), guard timer while waiting for signal"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : Boolean, True if signal received"
        try:
                if not(silent):
                        if timeout!=0:
                                SafePrint(None, hCom, "Wait DSR during :%ss"%(timeout/1000.0),color = 4)
                        else:
                                SafePrint(None, hCom, "Wait DSR",color = 4)
                        start = datetime.now()
                
                recv = hCom.waitDSR(timeout)
                if not(silent):
                        if recv:
                                diff = datetime.now() -start
                                SafePrint(None, hCom, "DSR detect after %ss"%((diff.seconds + diff.microseconds/1000000.0)),color = 4)
                        else:
                                SafePrint(None, hCom, "Can't detect DSR",color = 4)
                return recv
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "Wait DSR: Error!")
                return None

def SagWaitRI(hCom, timeout=30000, silent=False):
        "goal of the method : this method waits for RING signal"
        "INPUT : hCom, COM port instance"
        "                timeout (ms), guard timer while waiting for signal"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : Boolean, True if signal received"
        try:
                if not(silent):
                        if timeout!=0:
                                SafePrint(None, hCom, "Wait RI during :%ss"%(timeout/1000.0),color = 4)
                        else:
                                SafePrint(None, hCom, "Wait RI",color = 4)
                        start = datetime.now()
                
                recv = hCom.waitRI(timeout)
                
                if not(silent):
                        if recv:
                                diff = datetime.now() -start
                                SafePrint(None, hCom, "RI detect after %ss"%((diff.seconds + diff.microseconds/1000000.0)),color = 4)
                        else:
                                SafePrint(None, hCom, "Can't detect RI",color = 4)
                return recv
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "Wait RI: Error!")
                return None

def SagWaitDCD(hCom, timeout=30000, silent=False):
        "goal of the method : this method waits for DCD signal"
        "INPUT : hCom, COM port instance"
        "                timeout (ms), guard timer while waiting for signal"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : Boolean, True if signal received"
        try:
                if not(silent):
                        if timeout!=0:
                                SafePrint(None, hCom, "Wait DCD during :%ss"%(timeout/1000.0),color = 4)
                        else:
                                SafePrint(None, hCom, "Wait DCD",color = 4)
                        start = datetime.now()
                
                recv = hCom.waitDCD(timeout)
                
                if not(silent):
                        if recv:
                                diff = datetime.now() -start
                                SafePrint(None, hCom, "DCD detect after %ss"%((diff.seconds + diff.microseconds/1000000.0)),color = 4)
                        else:
                                SafePrint(None, hCom, "Can't detect DCD",color = 4)
                return recv
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "Wait DCD: Error!")
                return None

def SagWaitBREAK(hCom, timeout=30000, silent=False):
        "goal of the method : this method waits for BREAK signal"
        "INPUT : hCom, COM port instance"
        "                timeout (ms), guard timer while waiting for signal"
        "                silent, flag to know if a comment shall be displayed or not"
        "OUTPUT : Boolean, True if signal received"
        try:
                if not(silent):
                        if timeout!=0:
                                SafePrint(None, hCom, "Wait Break during :%ss"%(timeout/1000.0),color = 4)
                        else:
                                SafePrint(None, hCom, "Wait Break",color = 4)
                        start = datetime.now()
                
                recv = hCom.waitBreak(timeout)
                
                if not(silent):
                        if recv:
                                diff = datetime.now() -start
                                SafePrint(None, hCom, "Break detect after %ss"%((diff.seconds + diff.microseconds/1000000.0)),color = 4)
                        else:
                                SafePrint(None, hCom, "Can't detect Break",color = 4)
                return recv
        except SystemExit:
                raise SystemExit
        except:
                hCom.close()
                SafePrintError(None,hCom, "Wait Break: Error!")
                return None

#not in help# =============================================================================================
# =============================================================================================

def PRINT_START_FUNC(_string):
        "goal of the method : this method displays information"
        "INPUT : _string, information to display"
        "OUTPUT : none"
        #VarGlobal.statOfItem = 'OK'
        VarGlobal.myColor = VarGlobal.colorLsit[3]
        print "----------------------------------------------------------------------"
        print _string
        print "----------------------------------------------------------------------"
        VarGlobal.myColor = VarGlobal.colorLsit[8]

def PRINT_TEST_RESULT(_test_id, _result=VarGlobal.statOfItem):
        "goal of the method : this method displays information"
        "INPUT : _test_id, information to display (test case number)"
        "                _result, result of the test acse execution"
        "OUTPUT : none"
        VarGlobal.myColor = VarGlobal.colorLsit[8]
        # if _result == 'OK':
                # print "===> " + str(_test_id) + "was successful"
        # else:
                # print "===> " + str(_test_id) + "was failed"
        print ""
        if _result == 'OK':
                print "Status " + str(_test_id) + ": PASSED"
        elif _result == 'NA':
                print "Status " + str(_test_id) + ": NOT APPLICABLE"
        else:
                print "Status " + str(_test_id) + ": FAILED"

# ------------------------------------------------------------------------------------
# @description : compare the received command to the expected command and Display the test command result
# ------------------------------------------------------------------------------------
def isBoolean(cmd):
        "goal of the method : this method returns True if input is boolean, False else"
        "INPUT : cmd, data to check"
        "OUTPUT : true if input is boolean, false else"
        return type(cmd) == bool

def SagTestCmd(_cmd_recv, _res, _result=0):
        "                                                           "
        "   Not suggest to use anymore, replacement: SagMatchResp() "
        "                                                           "
        "goal of the method : this method compares the received command to the expected command and Display the test command result"
        "each keyword shall be found in given order (very important)"
        "INPUT :  _cmd_recv : response object"
        "         _res (list), expected keywords"
        "         _result : is the check critical or not ; if critical and if the result is failed, an exception is raised"
        "OUTPUT : Boolean"
        _result=0
        k=0                                     #ReachedLineIndexByPreviousKeyword
        IsPartialCorrFound = 0  #1 means at least 1 partial correspondance has been found
        IsNoCorrFound = 0               #1 means 1 keyword not found => error
        IsExactCorrFound = 0    #1 means at least 1 exact correspondance has been found
        my_liste = ""
        
        #to be consistent with old scripts
        if isBoolean(_result):  
                critical = _result
        else:
                critical = False

        if type(_cmd_recv)==type(Response()):
                if VarGlobal.DEBUG_LEVEL == "DEBUG":
                        print "_cmd_recv is a Response object"
                #the check has already been done
                if _cmd_recv.find:
                        if VarGlobal.DEBUG_LEVEL == "DEBUG":
                                print "_cmd_recv is a Response object and find is True"
                                print "before change _cmd_recv=" + str(_cmd_recv)
                        _cmd_recv = _cmd_recv.tabLines
                        if VarGlobal.DEBUG_LEVEL == "DEBUG":
                                print "after change _cmd_recv=" + str(_cmd_recv)
                else:
                        if VarGlobal.DEBUG_LEVEL == "DEBUG":
                                print "_cmd_recv is a Response object but find is True"
                        #the keyword has not been found : print error and raise an exception if critical
                        _result=1
                        VarGlobal.myColor = VarGlobal.colorLsit[9]
                        print "!!! Failed, expected response was : " + str(_res)
                        VarGlobal.myColor = VarGlobal.colorLsit[8]
                        VarGlobal.numOfFailedResponse += 1.0

                        #for Excel document
                        VarGlobal.excelComment = VarGlobal.excelComment + "!!! Failed, expected response was : " + str(_res) + '\r\n'
                        VarGlobal.excelCommentGlobal += VarGlobal.excelComment          

                        if critical:
                                raise receive_exception
                        my_liste = str(_res)
                        _res = []
        
        if VarGlobal.DEBUG_LEVEL == "DEBUG":
                print "loop on every keyword which presence in reception from module is to be checked"

                #loop on every keyword which presence in reception from module is to be checked
        for KeywordLoopIndex in range(len(_res)):
                IsNoCorrFound = 0
                my_liste = my_liste + " <" + _res[KeywordLoopIndex] + "> "
                if VarGlobal.DEBUG_LEVEL == "DEBUG":
                        print "keyword to check=" + str(_res[KeywordLoopIndex])
                        print "received lines=" + str(_cmd_recv)

                #if the end of received lines has been reached with previous keyword, the current can't be found
                #i.e. the keyword list is sorted and each received lines is analyzed only 1 time
                #happen also if received line is empty
                if k > len(_cmd_recv)-1:
                        IsNoCorrFound = 1
                else:
                        #for the current keyword, loop on each received lines
                        for AnalyzedLinesIndex in range(k, len(_cmd_recv)):
                                #_cmd_recv[j][0] is the data received
                                #_cmd_recv[j][1] is the date of reception
                                #often there is "\r\n" for j=0 and "OK" for j=1 (if succesfull)
                                #example : _cmd_recv=[('\r\n', '[08:42:17:677]'), ('OK\r\n', '[08:42:17:677]')]
                                if _cmd_recv[AnalyzedLinesIndex][0] == "\r\n":
                                        continue
                                else:
                                        #for the check, we remove the CR and LF of the received data
                                        _cmd_recv1 = _cmd_recv[AnalyzedLinesIndex][0].replace("\r","")
                                        _cmd_recv1 = _cmd_recv1.replace("\n","")
                                        #ok, now, we can do the check
                                        if _res[KeywordLoopIndex] == _cmd_recv1:
                                                #the keyword is exactly the received data
                                                k=AnalyzedLinesIndex+1                  #memorize the index of current line ; previous lines won't be parsed anymore
                                                IsNoCorrFound = 0
                                                IsExactCorrFound = 1
                                                break #exit the loop
                                        elif _res[KeywordLoopIndex] in _cmd_recv1:
                                                #the keyword is included in the received data
                                                k=AnalyzedLinesIndex+1                  #memorize the index of current line ; previous lines won't be parsed anymore
                                                IsNoCorrFound = 0
                                                IsPartialCorrFound = 1
                                                break #exit the loop
                                        else:
                                                #current keyword not found in any received lines
                                                IsNoCorrFound = 1
                        #the current keyword has not been found in any element of received list => exit
                        if IsNoCorrFound == 1:          
                                break
                                        
        if IsNoCorrFound == 1:
                #at least 1 keyword not found in received lines
                if VarGlobal.DEBUG_LEVEL == "DEBUG":
                        print "at least 1 keyword not found in received lines"
                _result=1
                VarGlobal.myColor = VarGlobal.colorLsit[9]
                print "!!! Failed, expected response was : " + my_liste
                VarGlobal.myColor = VarGlobal.colorLsit[8]
                VarGlobal.numOfFailedResponse += 1.0

                #for Excel document
                VarGlobal.excelComment = VarGlobal.excelComment + "!!! Failed, expected response was : " + my_liste + '\r\n'
                VarGlobal.excelCommentGlobal += VarGlobal.excelComment          

                if critical:
                        raise receive_exception
        elif IsPartialCorrFound == 1 :
                #all keyword found, at least 1 partial correspondance
                if VarGlobal.DEBUG_LEVEL == "DEBUG":
                        print "all keyword found, at least 1 partial correspondance"
                if VarGlobal.MODE == VarGlobal.DEMO_MODE:
                        print ""
                else:
                        print "--> Success <OK>*"
                #for Excel document
                VarGlobal.excelComment = ''
        elif IsExactCorrFound==1:
                #all keyword found, all exact correspondance found (no partial)
                if VarGlobal.DEBUG_LEVEL == "DEBUG":
                        print "all keyword found, all exact correspondance found (no partial)"
                if VarGlobal.MODE == VarGlobal.DEMO_MODE:
                        print ""
                else:
                        print "--> Success <OK>"
                #for Excel document
                VarGlobal.excelComment = ''
        elif _res != []:
                #should never happen
                if VarGlobal.DEBUG_LEVEL == "DEBUG":
                        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                        print "IMPOSSIBLE CASE HAS BEEN REACHED"
                        print "IsPartialCorrFound=" + str(IsPartialCorrFound)
                        print "IsNoCorrFound=" + str(IsNoCorrFound)
                        print "IsExactCorrFound=" + str(IsExactCorrFound)
                        print "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
                _result=1
                VarGlobal.myColor = VarGlobal.colorLsit[9]
                print "!!! Failed, expected response was : " + my_liste
                VarGlobal.myColor = VarGlobal.colorLsit[8]
                VarGlobal.numOfFailedResponse += 1.0

                #for Excel document
                VarGlobal.excelComment += "!!! Failed, expected response was : " + my_liste
                VarGlobal.excelCommentGlobal += VarGlobal.excelComment
                
                if critical:
                        raise receive_exception
        
        if _result != 0 :
                VarGlobal.statOfItem = 'NOK'                    
                VarGlobal.process_stat = 'NOK'
        else:
                VarGlobal.numOfSuccessfulResponse += 1.0
        #print "VarGlobal.excelComment = ", VarGlobal.excelComment
        return _result

def SagSystemStopsIfComError(MustSystemStop = True):
        "goal of the method : this method as been added for Femto team ; "
        "they don't wish the system stop is hCom fails to be opened"
        "if such behaviour is request, this method shall be executed first, before any other method"
        "added : v1.8.1"
        "INPUT : MustSystemStop boolean, True means the system shall stop if a COM port can't be opened"
        "OUTPUT : none"
        
        VarGlobal.IsSystemStopsWhenhComFails = MustSystemStop

def SagSendAT(hCom, cmd, printmode="symbol"): 
    "goal of the method : this method sends an AT command on a COM port"
    "INPUT : hCom : COM port object"
    "        cmd : AT command to send"
    "OUTPUT : none"
    time.sleep(0.1)
    hCom.write(cmd)
    time.sleep(0.1)
    if str(cmd).upper().startswith("AT"):
        # for test report
        VarGlobal.numOfCommand += 1.0

    if VarGlobal.SndRcvTimestamp:
        timestamp = TimeDisplay()+" "
    else:
        timestamp = ""
    # print_mutex.acquire() 
    # VarGlobal.myColor = VarGlobal.colorLsit[6]  # blue
    # print timestamp+"Snd COM"+ str(hCom.port)+" ["+ascii2print(cmd,printmode)+"]"
    # VarGlobal.myColor = VarGlobal.colorLsit[8]  # black
    # print_mutex.release() 
    LogMsg = timestamp+"Snd "+ str(hCom.port)+" ["+ascii2print(cmd,printmode)+"]"
    SafePrintLog(LogMsg, 6)

def SagWaitResp(hCom, waitpattern, timeout=60000, log_msg="logmsg", printmode="symbol"): 
    "goal of the method : this method waits for the data received from Com port"
    "INPUT : hCom : COM port object"
    "        waitpattern : the matching pattern for the received data"
    "        timeout (ms) : timeout between each received packet"
    "        log_msg : option for log message"
    "OUTPUT : Received data (String)"

    start_time = datetime.now()
    com_port_name = str(hCom.port)
    if log_msg == "debug":
        #print start_time
        SafePrintLog(start_time)
    global uartbuffer
    flag_matchrsp = False
    flag_matchstring = False
    flag_timeout = False
    flag_wait_until_timeout = False
    flag_printline = False
    LogMsg = ""
    timestamp = ""

    # wait until timeout mode
    if waitpattern == None or waitpattern[0] == "":
        flag_wait_until_timeout = True
        waitpattern = [""]
        SafePrintLog("")
        SafePrintLog("Wait responses in %s ms" % str(timeout))
        SafePrintLog("")

    displaybuffer = ""
    displaypointer = 0
    while 1:
        # Read data from UART Buffer
        if hCom.inWaiting()>0:
            uartbuffer[hCom.port] += hCom.read(hCom.inWaiting())
            if log_msg == "debug":
                #VarGlobal.myColor = VarGlobal.colorLsit[7]
                #print "Read data from UART buffer:", uartbuffer[hCom.port].replace("\r","<CR>").replace("\n","<LF>")
                #print "Read data from UART buffer:", ascii2print(uartbuffer[hCom.port],printmode)
                LogMsg = "Read data from UART buffer: "+ascii2print(uartbuffer[hCom.port],printmode)
                SafePrintLog(LogMsg,7)
        # Match response
        # Loop for each character
        for (i,each_char) in enumerate(uartbuffer[hCom.port]) :
            if log_msg == "debug":
                #VarGlobal.myColor = VarGlobal.colorLsit[7]
                #print i, uartbuffer[hCom.port][:i+1].replace("\r","<CR>").replace("\n","<LF>").replace("\n","<LF>")
                #print i, ascii2print(uartbuffer[hCom.port][:i+1],printmode)
                LogMsg = str(i)+" "+ascii2print(uartbuffer[hCom.port][:i+1],printmode)
                SafePrintLog(LogMsg,7)
            # display if matched with a line syntax
            displaybuffer = uartbuffer[hCom.port][displaypointer:i+1]
            line_syntax1 = "*\r\n*\r\n"
            line_syntax2 = "+*\r\n"
            line_syntax3 = "\r\n> "
            if fnmatch.fnmatchcase(displaybuffer, line_syntax1) or \
                fnmatch.fnmatchcase(displaybuffer, line_syntax2) or \
                fnmatch.fnmatchcase(displaybuffer, line_syntax3) :
                # display timestamp
                if VarGlobal.SndRcvTimestamp:
                    timestamp = TimeDisplay() + " "
                # display data
                #VarGlobal.myColor = VarGlobal.colorLsit[7]
                #received_data = displaybuffer.replace("\r","<CR>").replace("\n","<LF>").replace("\x15","<NAK>").replace("\x06","<ACK>").replace("\x00","<NULL>")
                received_data = ascii2print(displaybuffer,printmode)
                #print timestamp+"Rcv COM", com_port_name, "["+received_data+"]",
                LogMsg = timestamp+"Rcv "+com_port_name+" ["+received_data+"] "
                displaypointer = i+1
                flag_printline = True

            # match received response with waitpattern
            for (each_elem) in waitpattern:
                receivedResp = uartbuffer[hCom.port][:i+1]
                expectedResp = each_elem
                if fnmatch.fnmatchcase(receivedResp, expectedResp):
                    flag_matchstring = True
                    break
            if flag_matchstring:
                # display the remaining matched response when waitpettern is found
                displaybuffer = uartbuffer[hCom.port][displaypointer:i+1]
                if len(displaybuffer)>0:
                    # display timestamp
                    if VarGlobal.SndRcvTimestamp:
                        timestamp = TimeDisplay() + " "
                    # display data
                    #VarGlobal.myColor = VarGlobal.colorLsit[7]
                    #received_data = displaybuffer.replace("\r","<CR>").replace("\n","<LF>").replace("\x15","<NAK>").replace("\x06","<ACK>").replace("\x00","<NULL>")
                    received_data = ascii2print(displaybuffer,printmode)
                    #print "Rcv COM", com_port_name, "["+received_data+"]",
                    LogMsg = timestamp+"Rcv "+str(com_port_name)+" ["+received_data+"] "
                    pass

                # display time spent in receive
                if VarGlobal.RcvTimespent:
                    diff_time = datetime.now() - start_time
                    diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
                    #print " <"+str(timeout), " @"+str(diff_time_ms), "ms",
                    LogMsg += " <"+str(timeout)+" @"+str(diff_time_ms)+" ms "

                flag_printline = True

                # clear matched resposne in UART Buffer
                uartbuffer[hCom.port] = uartbuffer[hCom.port][i+1:]
                flag_matchrsp = True
                
                # break for Match response
                flag_matchrsp = True

            # print linebreak for EOL
            if flag_printline:
                flag_printline = False
                #print ""
                SafePrintLog(LogMsg,7)

            # break for Match response
            if flag_matchrsp:                
                break


        # Count timeout
        diff_time = datetime.now() - start_time
        diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
        if diff_time_ms > timeout:
            if log_msg == "debug":
                #print "Timeout: ", diff_time, "diff_time_ms:", diff_time_ms
                LogMsg = "Timeout: "+str(diff_time)+" diff_time_ms: "+str(diff_time_ms)
                SafePrintLog(LogMsg,7)
            # display the remaining response when timeout
            displaybuffer = uartbuffer[hCom.port][displaypointer:]
            if len(displaybuffer)>0:
                # display timestamp
                if VarGlobal.SndRcvTimestamp:
                    #VarGlobal.myColor = VarGlobal.colorLsit[7]
                    #print TimeDisplay(),
                    timestamp = TimeDisplay() + " "
                # display data
                #VarGlobal.myColor = VarGlobal.colorLsit[7]
                #received_data = receivedResp.replace("\r","<CR>").replace("\n","<LF>").replace("\x15","<NAK>").replace("\x06","<ACK>").replace("\x00","<NULL>")
                received_data = ascii2print(receivedResp,printmode)
                #print "Rcv COM", com_port_name, " ["+received_data+"]"
                LogMsg = "Rcv "+str(com_port_name)+" ["+received_data+"]"
                SafePrintLog(LogMsg,7)
                pass

            # clear all resposne in UART Buffer
            VarGlobal.myColor = VarGlobal.colorLsit[8]
            receivedResp = uartbuffer[hCom.port]

            if flag_wait_until_timeout != True:
                if log_msg == "logmsg" or log_msg == "debug":
                    if len(receivedResp) > 0:
                        VarGlobal.numOfResponse += 1.0
                        #print "\nNo Match! "+"@COM"+com_port_name+ " <"+str(timeout)+" ms\n"
                        LogMsg = "\nNo Match! "+"@COM"+com_port_name+" <"+str(timeout)+" ms\n"
                        SafePrintLog(LogMsg,7)
                    if len(receivedResp) == 0:
                        #print "\nNo Response! "+"@COM"+com_port_name+ " <"+str(timeout)+" ms\n"
                        LogMsg = "\nNo Response! "+"@COM"+com_port_name+ " <"+str(timeout)+" ms\n"
                        SafePrintLog(LogMsg,7)
            uartbuffer[hCom.port] = ""
            flag_timeout = True
        

        if flag_matchrsp:
            VarGlobal.numOfResponse += 1.0
            break
        if flag_timeout:
            break


    if log_msg == "debug":
        #print ""
        #print len(uartbuffer[hCom.port])
        #print "The remaining data in uartbuffer " + str((hCom.port + 1))  + " : [", uartbuffer[hCom.port].replace("\r","<CR>").replace("\n","<LF>"), "]"
        #print "The remaining data in uartbuffer " + str((hCom.port + 1))  + " : [", ascii2print(uartbuffer[hCom.port],printmode), "]"
        SafePrintLog("")
        SafePrintLog(str(len(uartbuffer[hCom.port])),7)
        LogMsg = "The remaining data in uartbuffer " + str((hCom.port + 1))  + " : [", ascii2print(uartbuffer[hCom.port],printmode), "]"
        SafePrintLog(LogMsg,7)
    return receivedResp


def SagMatchResp(resp, keywords, condition="wildcard", update_result="critical", log_msg="logmsg", printmode="symbol"):
    "goal of the method : this method compares the received command to the expected command and Display the comparison result"
    "INPUT :  resp : Response object or a string"
    "         keywords (list) : expected response"
    "         condition : matching condition, 1.wildcard"
    "                                        2.match_all_order"
    "                                        3.match_all_disorder"
    "                                        4.contain_all_order"
    "                                        5.contain_all_disorder"
    "                                        6.contain_anyone"
    "                                        7.not_contain_anyone"
    "         update_result : 1. critical, update result to global variable VarGlobal.statOfItem"
    "                         2. not_critical, do nothing for the result"
    "         log_msg : 1. logmsg, print with log message"
    "                   2. debug, print with log and debug message"
    "                   3. nologmsg, print without any message"
    "OUTPUT : Boolean >> True:response matched, False:repsonse mis-matched"

    VarGlobal.myColor = VarGlobal.colorLsit[8]

    # If resp is Response() >> assign .tabData to resp
    if type(resp) != type("string"):
        #print "This is not a string"
        resp = resp.tabData

    # If keywords is None >> assign empty string
    if keywords == None:
        keywords = [""]

    # validate parameter - condition
    if condition not in ["wildcard", "match_all_order", "match_all_disorder", "contain_all_order", "contain_all_disorder", "contain_anyone", "not_contain_anyone"]:
        SafePrintLog( "Invalid parameter for SagMatchResp() - condition", 8 )
        SafePrintLog( "Option:", 8 )
        SafePrintLog( "\"wildcard\"", "\"match_all_order\"", "\"match_all_disorder\"", "\"contain_all_order\"", "\"contain_all_disorder\"", "\"contain_anyone\"", "\"not_contain_anyone\"", 8 )
        SafePrintLog( "" )
        condition = "wildcard"

    # validate parameter - update_result
    if update_result not in ["critical", "not_critical"]:
        SafePrintLog("Invalid parameter for SagMatchResp() - update_result", 8)
        SafePrintLog("Option:", 8)
        SafePrintLog("\"critical\"", "\"not_critical\"",8)
        SafePrintLog("")
        update_result = "critical"

    # validate parameter - log_msg
    if log_msg not in ["logmsg", "nologmsg", "debug"]:
        SafePrintLog("Invalid parameter for SagMatchResp() - log_msg",8)
        SafePrintLog("Option:",8)
        SafePrintLog("\"logmsg\"", "\"nologmsg\"", "\"debug\"",8)
        SafePrintLog("")
        log_msg = "logmsg"

    # 1
    # Default - matching with wildcard character
    if condition=="wildcard":
        flag_matchstring = False
        matched = False
        for (each_elem) in keywords:
            receivedResp = resp
            expectedResp = each_elem
            if fnmatch.fnmatchcase(receivedResp, expectedResp):
                flag_matchstring = True
                matched = True
                break

        if matched == 0 :
            if log_msg == "logmsg" or log_msg == "debug":
                if len(keywords)==1:
                    SafePrintLog("")
                    SafePrintLog("Expected Response: %s" % ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                    SafePrintLog("Received Response: %s" % ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                    SafePrintLog("")
                if len(keywords)>1:
                    SafePrintLog("")
                    SafePrintLog("Expected Response: %s" % ascii2print(keywords[0],printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                    for (i,each_elem) in enumerate(keywords):
                        if i == 0:
                            pass
                        if i >0:
                            SafePrintLog("Expected Response: %s" % ascii2print(each_elem,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                    SafePrintLog("Received Response: %s" % ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                    SafePrintLog("")
    # 2
    if condition=="match_all_order":
        if log_msg == "debug":
            SafePrintLog("Check if response match all keywords in order: ( match without extra char. )", 8)
        receivedResp = resp
        expectedResp = ""
        for (i,each_keyword) in enumerate(keywords) :
            expectedResp += keywords[i]
        matched = fnmatch.fnmatchcase(receivedResp, expectedResp)
        if matched == 0 :
            if log_msg == "logmsg" or log_msg == "debug":
                SafePrintLog("")
                SafePrintLog("No Match!! (match_all_order)", 8)
                SafePrintLog("")
                SafePrintLog("Expected Response: %s" % ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                SafePrintLog("Received Response: %s" % ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                SafePrintLog("")

    # 3
    if condition=="match_all_disorder":
        debug_msg = ""
        debug_msg += "Check if response contains all keywords ( without extra character, dis-order ): \n"
        # differcuit to code , code later

        itemlist = keywords
        #itemlist = ["A","B","C"]
        permutation_list = list(itertools.permutations(itemlist, len(itemlist)))
        permutation_concat_list = []
        for each_elem in permutation_list:
            tempstring = ""
            for eachchar in each_elem:
                tempstring += eachchar
            permutation_concat_list.append(tempstring)

        debug_msg += "\nConbination of keywords: \n"

        for (i,each_conbination) in enumerate(permutation_concat_list) :
            # print i+1, ascii2print(each_conbination,printmode).replace("<CR>","\\r").replace("<LF>","\\n")

            receivedResp = resp
            expectedResp = each_conbination
            matched = fnmatch.fnmatchcase(receivedResp, expectedResp)

            # debug message
            if matched == 0 : 
                debug_msg += str(i+1) + " " + ascii2print(each_conbination,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- no match\n"
            else:
                debug_msg += str(i+1) + " " + ascii2print(each_conbination,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- matched\n"

            # break in normal mode when result matched
            # normal mode >> matched result and break, debug mode >> list all conbination and result
            if matched == 1 :
                if log_msg != "debug":
                    break

        # display "No Match" when matching failed
        if matched == 1 :
            if log_msg == "debug":
                SafePrintLog( debug_msg, 8 )
        else:
            if log_msg == "logmsg" or log_msg == "debug":
                SafePrintLog("")
                SafePrintLog("No Match!! (match_all_disorder)", 8)
                SafePrintLog("")
                SafePrintLog( debug_msg, 8 )

    # 4
    if condition=="contain_all_order":
        debug_msg = ""
        debug_msg += "Check if response contains all keywords in order:"
        receivedResp = resp
        expectedResp = "*"
        for (i,each_keyword) in enumerate(keywords) :
            if i == 0 :
                expectedResp += keywords[i]
            else:
                expectedResp += "*" + keywords[i]
        expectedResp += "*"
        matched = fnmatch.fnmatchcase(receivedResp, expectedResp)
        if matched == 1 :
            if log_msg == "debug":
                SafePrintLog("")
                SafePrintLog( debug_msg, 8 )
                SafePrintLog( "Expected Response: %s" % ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8 )
                SafePrintLog("")
        else:
            if log_msg == "logmsg" or log_msg == "debug":
                SafePrintLog("")
                SafePrintLog("No Match!! (contain_all_order)", 8)
                SafePrintLog("")
                SafePrintLog("Expected Response: %s" % ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8 )
                SafePrintLog("Received Response: %s" % ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8 )
                SafePrintLog("")

    # 5
    if condition=="contain_all_disorder":
        debug_msg = ""
        debug_msg += "\nCheck if response contains all keywords without order:\n\n"
        #for (i,each_keyword) in enumerate(keywords) :
        #    print ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n")
        receivedResp = resp
        expectedResp = ""

        debug_msg += "Response: " + ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "\n"
        debug_msg += "Keywords:\n"
        flag_notfound = 0
        matched = 1

        for (i,each_keyword) in enumerate(keywords) :
            if resp.find(keywords[i]) >= 0:
                debug_msg += ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- found\n"
            else:
                debug_msg += ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- not found\n"
                flag_notfound = 1


        if flag_notfound == 0:
            matched = 1
            if log_msg == "debug":
                SafePrintLog( debug_msg, 8 )

        if flag_notfound == 1:
            matched = 0
            if log_msg == "logmsg" or log_msg == "debug":
                SafePrintLog("")
                SafePrintLog( "No Match!! (contain_all_disorder)", 8 )
                SafePrintLog("")
                SafePrintLog(debug_msg, 8 )

    # 6
    if condition=="contain_anyone":
        debug_msg = ""
        debug_msg += "\nCheck if response contains anyone of keywords: \n\n"
        #for (i,each_keyword) in enumerate(keywords) :
        #    print ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n")
        receivedResp = resp
        expectedResp = ""

        debug_msg += "Response: " + ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "\n"
        debug_msg += "Keywords:\n"
        flag_found = 0
        matched = 0
        for (i,each_keyword) in enumerate(keywords) :
            if resp.find(keywords[i]) >= 0:
                debug_msg += ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- found\n"
                flag_found = 1
            else:
                debug_msg += ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- not found\n"

        if flag_found == 1:
            matched = 1
            if log_msg == "debug":
                SafePrintLog(debug_msg, 8 )

        if flag_found == 0:
            matched = 0
            if log_msg == "logmsg" or log_msg == "debug":
                SafePrintLog("")
                SafePrintLog("No Match!! (contain_anyone)", 8)
                SafePrintLog("")
                SafePrintLog( debug_msg, 8 )

    # 7
    if condition=="not_contain_anyone":
        debug_msg = ""
        debug_msg += "\nCheck that response do not contains anyone of keywords: \n\n"
        #for (i,each_keyword) in enumerate(keywords) :
        #    print ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n")
        receivedResp = resp
        expectedResp = ""

        debug_msg += "Response: " + ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "\n"
        debug_msg += "Keywords:\n"
        flag_found = 0
        matched = 1

        for (i,each_keyword) in enumerate(keywords) :
            if resp.find(keywords[i]) >= 0:
                debug_msg += ascii2print(keywords[i],printmode).replace("<CR>","\\r").replace("<LF>","\\n") + "      <-- found\n"
                flag_found = 1
            else:
                debug_msg += ascii2print(keywords[i],printmode) + "      <-- not found\n"


        if flag_found == 0:
            matched = 1
            if log_msg == "debug":
                SafePrintLog( debug_msg, 8 )

        if flag_found == 1:
            matched = 0
            if log_msg == "logmsg" or log_msg == "debug":
                SafePrintLog("")
                SafePrintLog("No Match!! (not_contain_anyone)", 8)
                SafePrintLog("")
                SafePrintLog( debug_msg, 8 )

    # udpate result to VarGlobal.statOfItem
    if update_result == "critical":
        if matched == 0:
            # for Autotest GUI and CLI
            if 'VarGlobal' in globals():
                VarGlobal.statOfItem = 'NOK'
                VarGlobal.numOfFailedResponse  += 1.0
                #VarGlobal.process_stat = 'NOK'
        else:
            if 'VarGlobal' in globals():
                VarGlobal.numOfSuccessfulResponse += 1.0
                pass
            pass
    else:
        if log_msg == "logmsg":
            SafePrintLog("\nNot Critical command\n", 8)

    return matched


def SagWaitnMatchResp(hCom, waitpattern, timeout, condition="wildcard", update_result="critical", log_msg="logmsg", printmode="symbol"):
    "goal of the method : combine SagWaitResp() and SagMatchResp()"
    "INPUT : hCom : COM port object"
    "        waitpattern : the matching pattern for the received data"
    "        timeout : timeout value in second"
    "OUTPUT : None"

    #VarGlobal.myColor = VarGlobal.colorLsit[8]

    # validate parameter - condition
    if condition not in ["wildcard"]:
        SafePrintLog("Invalid parameter for SagWaitnMatchResp() - condition",8)
        SafePrintLog("Option:",8)
        SafePrintLog("\"wildcard\"",8)
        SafePrintLog("")
        SafePrintLog("SagWaitnMatchResp() only support \"wildcard\" in \"condition\"",8)
        SafePrintLog("")
        condition = "wildcard"

    SagWaitResp_response = SagWaitResp(hCom, waitpattern, timeout, log_msg, printmode)
    match_result = SagMatchResp(SagWaitResp_response, waitpattern, condition, update_result, log_msg, printmode)
    return match_result

def get_ini_value ( file_path, sections, name ):    
    if os.path.isfile(file_path):
        print "Read %s:%s from %s" % ( sections, name, file_path )        
        Parser = ConfigParser.RawConfigParser()
        found = Parser.read(file_path)        
        if not Parser.has_section(sections):
            print "\nNo Section %s in %s  !!!" % ( str(sections), file_path )
        if not Parser.has_option(sections, name):
            print "\nNo Name %s udner %s in %s  !!!" % ( name, str(sections), file_path )

        Parser = ConfigParser.ConfigParser()
        found = Parser.read(file_path)
        value = Parser.get(sections, name)
        return value.strip("\"'")
    else:
        print "\%s NOT exits !!!\n" % file_path
        return ''

def string2cmd( hCom, module_type, item ):
    item_list = item.split(" ")
    #print item_list
    default_loop_count = 1
    default_timeout = 1000
    default_flag_break = 0
    default_flag_update_result = "critical"

    for (i,each_item) in enumerate(item_list) :

        # not critical
        flag_update_result = default_flag_update_result
        # *!*
        if fnmatch.fnmatchcase(each_item, "*nc"):
            flag_update_result = "not_critical"
            # #* will be removed
            each_item = each_item[:-2]

        # flag_break 
        flag_break = default_flag_break
        # *!*
        if fnmatch.fnmatchcase(each_item, "*#"):
            flag_break = 1
            # #* will be removed
            each_item = each_item.split("#")[0]

        # loop value 
        loop_count = default_loop_count
        # *!*
        if fnmatch.fnmatchcase(each_item, "*!*"):
            loop_count = int(each_item.split("!")[1])
            # !* will be removed
            each_item = each_item.split("!")[0]

        # timeout value
        timeout_value = default_timeout
        # *<*
        if fnmatch.fnmatchcase(each_item, "*<*"):
            timeout_value = int(each_item.split("<")[1]) * 1000
            # <* will be removed
            each_item = each_item.split("<")[0]

        # Remove AT+
        if fnmatch.fnmatchcase(each_item, "AT+*"):
            each_item = each_item[3:]

        # Loop start
        match_result = 0
        for i in range(loop_count):
            if loop_count > 1:
                print "Loop: ", str(i+1)


            # Command for checking module information
            
            # 1.
            # response with \r\nOK\r\n
            # AT
            if each_item in ["AT"]:
                SagSendAT(hCom, each_item+"\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\nOK\r\n", "AT\r\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # AT*OK
            if each_item in ["AT*OK"]:
                SagSendAT(hCom, "AT\r")
                match_result = SagWaitnMatchResp(hCom, ["*\r\nOK\r\n", "*\r\nOK\r\n"], timeout_value, update_result=flag_update_result)


            # 2.
            # response with  \r\n*\r\n\r\nOK\r\n
            # ATI3 ATI9
            if each_item in ["ATI3","ATI9"]:
                SagSendAT(hCom, each_item+"\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\n*\r\n\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # AT+
            # CGMI
            if each_item in ["CGMI","CGMM","WHWV","WDOP","WMSN","CGSN","CGMR","GCAP","WSSW","CPINC","CCID"]:
                SagSendAT(hCom, "AT+"+each_item+"\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\n*\r\n\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # Smart convertion
            # IPR WIMEI CMEE WIND
            if each_item in ["IPR","WIMEI","CMEE","WIND"]:
                SagSendAT(hCom, "AT+"+each_item+"?\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\n*\r\n\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # IPR? WIMEI? CMEE? WIND?
            if each_item in ["IPR?","WIMEI?","CMEE?","WIND?"]:
                SagSendAT(hCom, "AT+"+each_item+"\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\n*\r\n\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # WOPEN
            if fnmatch.fnmatch(each_item, "*WOPEN"):
                SagSendAT(hCom, "AT+WOPEN=2\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\n*\r\n\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # WOPEN=2 
            if fnmatch.fnmatch(each_item, "*WOPEN=2"):
                SagSendAT(hCom, "AT+WOPEN=2\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\n*\r\n\r\nOK\r\n"], timeout_value, update_result=flag_update_result)

            # 3.
            # response with \r\n*\r\n
            # CPIN
            if fnmatch.fnmatch(each_item, "*CPIN"):
                if fnmatch.fnmatch(module_type, "*Intel*"):
                    SagSendAT(hCom, "AT+CPIN?\r")
                    match_result = SagWaitnMatchResp(hCom, ["\r\n*\r\n\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
                if fnmatch.fnmatch(module_type, "*Qualcomm*"):
                    SagSendAT(hCom, "AT+CPIN?\r")
                    match_result = SagWaitnMatchResp(hCom, ["\r\n*\r\n"], timeout_value, update_result=flag_update_result)
                if fnmatch.fnmatch(module_type, "*Legacy*"):
                    SagSendAT(hCom, "AT+CPIN?\r")
                    match_result = SagWaitnMatchResp(hCom, ["\r\n*\r\n"], timeout_value, update_result=flag_update_result)
            # CPIN?
            if fnmatch.fnmatch(each_item, "*CPIN?"):
                if fnmatch.fnmatch(module_type, "*Intel*"):
                    SagSendAT(hCom, "AT+CPIN?\r")
                    match_result = SagWaitnMatchResp(hCom, ["\r\n*\r\n\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
                if fnmatch.fnmatch(module_type, "*Qualcomm*"):
                    SagSendAT(hCom, "AT+CPIN?\r")
                    match_result = SagWaitnMatchResp(hCom, ["\r\n*\r\n"], timeout_value, update_result=flag_update_result)
                if fnmatch.fnmatch(module_type, "*Legacy*"):
                    SagSendAT(hCom, "AT+CPIN?\r")
                    match_result = SagWaitnMatchResp(hCom, ["\r\n*\r\n"], timeout_value, update_result=flag_update_result)
            # Command for module initialization
            # 1.
            # response with *\r\nOK\r\n

            # ATE0 ATE1
            if each_item in ["ATE0","ATE1"]:
                SagSendAT(hCom, each_item+"\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\nOK\r\n","ATE0\r\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # AT&F AT&W
            if each_item in ["AT&F","AT&W"]:
                SagSendAT(hCom, each_item+"\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], timeout_value, update_result=flag_update_result)

            # Smart convertion
            # *CFUN
            if fnmatch.fnmatch(each_item, "*CFUN"):
                SagSendAT(hCom, "AT+CFUN=1\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # CFUN1
            if each_item == "CFUN1":
                SagSendAT(hCom, "AT+CFUN=1\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # CFUN11
            if each_item == "CFUN11":
                SagSendAT(hCom, "AT+CFUN=1,1\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # *CFUN=1 
            if fnmatch.fnmatch(each_item, "*CFUN=1"):
                SagSendAT(hCom, "AT+CFUN=1\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # *CFUN=1,1
            if fnmatch.fnmatch(each_item, "*CFUN=1,1"):
                SagSendAT(hCom, "AT+CFUN=1,1\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], timeout_value, update_result=flag_update_result)


            # *CMEE=1
            if fnmatch.fnmatch(each_item, "*CMEE=1"):
                SagSendAT(hCom, "AT+CMEE=1\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # CMEE1
            if each_item == "CMEE1":
                SagSendAT(hCom, "AT+CMEE=1\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], timeout_value, update_result=flag_update_result)

            # *CPIN=????
            if fnmatch.fnmatch(each_item, "*CPIN=????"):
                pin_code = each_item.split("=")[1]
                SagSendAT(hCom, "AT+CPIN=\""+str(pin_code)+"\"\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\nOK\r\n","\r\n+CME ERROR: 3\r\n","\r\n+CME ERROR: 10\r\n"], timeout_value, update_result=flag_update_result)

            # *WIND=????
            if fnmatch.fnmatch(each_item, "*WIND=*"):
                wind_code = each_item.split("=")[1]
                SagSendAT(hCom, "AT+WIND="+str(wind_code)+"\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], timeout_value, update_result=flag_update_result)


            # Command for Waiting module get ready
            # +WIND:*
            if fnmatch.fnmatch(each_item, "*WIND:*"):
                wind_event = each_item.split(":")[1]
                match_result = SagWaitnMatchResp(hCom, ["\r\n+WIND: "+ wind_event +"\r\n"], timeout_value, update_result=flag_update_result)
            # +CREG:*
            if fnmatch.fnmatch(each_item, "*CREG:*"):
                creg_stat = each_item.split(":")[1]
                SagSendAT(hCom, "AT+CREG?\r")
                #match_result = SagWaitnMatchResp(hCom, ["\r\n+CREG: ?,"+ str(creg_stat) +"\r\n\r\nOK\r\n"], timeout_value, "wildcard", "not_critical", "nologmsg")
                match_result = SagWaitnMatchResp(hCom, ["\r\n+CREG: ?,"+ str(creg_stat) +"\r\n\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # +CGREG:*
            if fnmatch.fnmatch(each_item, "+CGREG:*"):
                creg_stat = each_item.split(":")[1]
                SagSendAT(hCom, "AT+CGREG?\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\n+CGREG: ?,"+ str(creg_stat) +"\r\n\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # +CEREG:*
            if fnmatch.fnmatch(each_item, "+CEREG:*"):
                creg_stat = each_item.split(":")[1]
                SagSendAT(hCom, "AT+CEREG?\r")
                match_result = SagWaitnMatchResp(hCom, ["\r\n+CEREG: ?,"+ str(creg_stat) +"\r\n\r\nOK\r\n"], timeout_value, update_result=flag_update_result)
            # DELAY:*
            if fnmatch.fnmatch(each_item, "*DELAY:*"):
                timeout_value = int(each_item.split(":")[1].replace("S","").replace("s",""))*1000
                print "Wait " + str(timeout_value) + " ms"
                time.sleep(timeout_value/1000)
                #match_result = SagWaitnMatchResp(hCom, None, timeout_value, "wildcard", "not_critical", "nologmsg")
            # +KSUP:*
            if fnmatch.fnmatch(each_item, "*KSUP:*"):
                wind_event = each_item.split(":")[1]
                match_result = SagWaitnMatchResp(hCom, ["\r\n+KSUP: "+ wind_event +"\r\n"], timeout_value, update_result=flag_update_result)
            # +SIM:*
            if fnmatch.fnmatch(each_item, "*SIM:*"):
                wind_event = each_item.split(":")[1]
                match_result = SagWaitnMatchResp(hCom, ["\r\n+SIM: "+ wind_event +"\r\n"], timeout_value, update_result=flag_update_result)
            # +PBREADY
            if fnmatch.fnmatch(each_item, "*PBREADY"):
                match_result = SagWaitnMatchResp(hCom, ["\r\n+PBREADY\r\n"], timeout_value, update_result=flag_update_result)


            # break loop if matched 
            if flag_break:
                if match_result == 1:
                    if (loop_count-i) > 1:
                        break
    return None

def check_module( hCom, module_type, item ):
    item = item[0]
    string2cmd( hCom, module_type, item )
def init_module( hCom, module_type, item ):
    item = item[0]
    string2cmd( hCom, module_type, item )
def wait_module( hCom, module_type, item ):
    item = item[0]
    string2cmd( hCom, module_type, item )
def restore_module( hCom, module_type, item ):
    item = item[0]
    string2cmd( hCom, module_type, item )
def SagDetectCom(port, timeout=60000, logmsg="logmsg"):
    start_time = datetime.now()
    flag_linebreak = 0
    VarGlobal.myColor = VarGlobal.colorLsit[8]
    #print "Detect COM port"
    while 1:
        try:
            s = serial.Serial(port, baudrate=115200, bytesize=8, parity='N', stopbits=1, timeout=1, xonxoff=0, rtscts=1, writeTimeout=None, dsrdtr=0)
            if logmsg=="logmsg":
                if flag_linebreak:
                    print ""
                print "COM "+str(port)+" - port found", 
            # display time spent in receive
            diff_time = datetime.now() - start_time
            diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
            if logmsg=="logmsg":
                print " <"+str(timeout), " @"+str(diff_time_ms), "ms"
            s.close()
            break
        except serial.SerialException:
            pass
        time.sleep(1)
        sys.stdout.write("*")
        flag_linebreak = 1
        
        # Count timeout
        diff_time = datetime.now() - start_time
        diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
        if diff_time_ms > timeout:
            if logmsg=="logmsg":
                if flag_linebreak:
                    print ""
                print "COM "+str(port)+" - port not found"+" <"+str(timeout)+" ms"
            break
def SagTryAT(hCom):
    match_result = 0
    SagSendAT(hCom, "AT\r")
    match_result = SagWaitnMatchResp(hCom, ["*\r\nOK\r\n"], 4000, "wildcard", "not_critical", "logmsg")
    return match_result

def wait_com_ready(port, timeout=60000):
    test_result = 0
    SagDetectCom(port, timeout)
    
    s = SagOpen(port, 115200) 
    test_result = SagTryAT(s)
    SagClose(s)

    return test_result

xmodem_displaybuffer = ""

def xmodem_send(hCom, dwlfile, logmsg="silent", modem_mode="xmodem1k"):
    start_time = datetime.now()
    VarGlobal.myColor = VarGlobal.colorLsit[8]
    print "xmodem send - start: ", "("+logmsg+")", dwlfile
    def getc(size, timeout=1):
        global xmodem_displaybuffer
        answer =  hCom.read(size)
        # logmsg - raw
        if logmsg=="raw":
            sys.stdout.write(answer)
        # logmsg - buffer
        if logmsg=="buffer":
            xmodem_displaybuffer += answer
            if len(xmodem_displaybuffer)>500:
                #for each_char in xmodem_displaybuffer:
                sys.stdout.write(xmodem_displaybuffer.replace("\x06","<ACK>").replace("\x15","<NAK>"))
                xmodem_displaybuffer = ""
        return answer
    def putc(data, timeout=1):
        hCom.write(data)
        return None
    modem = XMODEM(getc, putc, modem_mode)

    stream = open(dwlfile, 'rb')
    status = modem.send(stream, retry=8)
    stream.close()
    #status = 0

    # display time spent in receive
    diff_time = datetime.now() - start_time
    diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
    print "xmodem send - completed", "@"+str(diff_time_ms), "ms"

    return status

def SagWDWLDownload(hCom, moduletype, baudrate, dwl_filefullpath, onoff_com=1 , cfun_delay_time = 10000, cfun_timeout = 60000):
    print "WDWL Download - Start:"
    ComOjb = hCom
    ComPort = hCom.port + 1

    if os.path.isfile(dwl_filefullpath):
        #print dwl_filefullpath + " is found."
        pass
    else:
        #print dwl_filefullpath + " is not found."
        raise Exception("Error: %s is not found." % dwl_filefullpath)

    SagSendAT(hCom, "AT\r")
    SagWaitnMatchResp(hCom, ["*\r\nOK\r\n"], 4000)

    SagSendAT(hCom, "AT+WDWL\r")
    SagWaitnMatchResp(hCom, ["*\r\n+WDWL: 0\r\n"], 4000)

    # Close and Re-open COM for USB port
    if onoff_com:
        SagClose(hCom)
        SagSleep(cfun_delay_time)
        SagDetectCom(ComPort,cfun_timeout)
        hCom = SagOpen(ComPort,baudrate) 
    else:
        SagSleep(cfun_delay_time)

    # wait for NAK
    NAK_counter = 0
    while 1:
        answer = SagWaitResp(hCom, ["?"], 4000)
        #match_result = SagMatchResp(answer, ["*?"])
        NAK_counter = NAK_counter + 1;
        if NAK_counter == 5:
            break

    status = xmodem_send(hCom, dwl_filefullpath)

    # wait for NAK after download
    answer = SagWaitResp(hCom, ["?"], 90000)
    NAK_counter = 0
    while 1:
        answer = SagWaitResp(hCom, ["?"], 4000)
        #match_result = SagMatchResp(answer, ["*?"])
        NAK_counter = NAK_counter + 1;
        if NAK_counter == 5:
            break

    # Close and Re-open COM after CFUN
    SagSendAT(hCom, "AT+CFUN=1\r")

    if onoff_com:
        SagClose(hCom)
        SagSleep(cfun_delay_time)
        SagDetectCom(ComPort,cfun_timeout)
        hCom = SagOpen(ComPort,baudrate) 
        SagWaitnMatchResp(hCom, ["*\r\nOK\r\n"], 4000, "wildcard", "not_critical", "nologmsg")
    else:
        SagWaitnMatchResp(hCom, ["*\r\nOK\r\n"], cfun_timeout, "wildcard", "not_critical", "nologmsg")


    SagSendAT(hCom, "AT\r")
    SagWaitnMatchResp(hCom, ["*\r\nOK\r\n"], 4000)

    print ""
    return hCom

def SagReOpenCom(hCom, cfun_delay_time=2000, cfun_timeout=60000, baudrate=115200):
    ComPort = hCom.port + 1

    SagClose(hCom)
    SagSleep(cfun_delay_time)
    SagDetectCom(ComPort,cfun_timeout)
    hCom = SagOpen(ComPort,baudrate) 
    return hCom

def ascii2print(inputstring, mode="symbol"):

    if mode=="symbol":
        # calculate value to hexstring >> too slow , don't use these code
        if 0:
            outputstring = ""
            for eachchar in inputstring:
                if ord(eachchar)<32:
                    outputstring += VarGlobal.ascii_symbol[eachchar]
                elif ord(eachchar)==127:
                    outputstring += VarGlobal.ascii_symbol[eachchar]
                elif ord(eachchar)>127:
                    outputstring += "<"+"0x{:02X}".format(ord(eachchar))+">"
                else:
                    outputstring += eachchar

        # direct convert value to string by Dictionary >> very fast
        if 1:
            string_raw = inputstring
            # convert raw data to <symbol> for \x00 - \x1F
            #                     <0x??>   for \x80 - \xFF
            for key, value in VarGlobal.ascii_symbol.iteritems():
                string_raw = string_raw.replace(key,value)
            outputstring = string_raw


    if mode=="hexstring":
        # calculate value to hexstring >> too slow , don't use these code
        if 0:
            outputstring = ""
            for eachchar in inputstring:
                outputstring += "<"+"0x{:02X}".format(ord(eachchar))+">"
                
        # direct convert value to string by Dictionary >> very fast
        if 1:
            string_raw = inputstring
            for key, value in VarGlobal.ascii2hexstring_printable_tempsymbol.iteritems():
                string_raw = string_raw.replace(key,value)
            for key, value in VarGlobal.ascii2hexstring_printable_revert.iteritems():
                string_raw = string_raw.replace(key,value)
            for key, value in VarGlobal.ascii2hexstring_symbol.iteritems():
                string_raw = string_raw.replace(key,value)
            for key, value in VarGlobal.ascii2hexstring_extended.iteritems():
                string_raw = string_raw.replace(key,value)
            outputstring = string_raw


    if mode=="raw":
        string_raw = inputstring
        # convert <symbol> to raw data
        for key, value in VarGlobal.ascii_symbol.iteritems():
            string_raw = string_raw.replace(value,key)
        # convert <0x??> to raw data
        for key, value in VarGlobal.ascii2hexstring_printable.iteritems():
            string_raw = string_raw.replace(value,key)
        for key, value in VarGlobal.ascii2hexstring_symbol.iteritems():
            string_raw = string_raw.replace(value,key)
        for key, value in VarGlobal.ascii2hexstring_extended.iteritems():
            string_raw = string_raw.replace(value,key)
        outputstring = string_raw
                
    return outputstring

def SagDetectIPR(hCom):
    at_response_time_ms = {'115200':100,'57600':100,'38400':200,'19200':200,'9600':200,'4800':500,'2400':500,'1200':500,'600':2000,'300':3000}
    for baudrate in [115200,9600,57600,38400,19200,4800,2400,1200,600,300]:
        #for i in range(2):
            #print "Loop: ", str(i+1)
        com_port = hCom.port
        SagClose(hCom)
        hCom = SagOpen(com_port,baudrate,8,"N",1,"Hardware")
        SagSendAT(hCom, "AT\r")
        match_result = SagWaitnMatchResp(hCom, ["*\r\nOK\r\n"], at_response_time_ms[str(baudrate)], "wildcard", "not_critical", "nologmsg")
        SagSendAT(hCom, "AT\r")
        match_result = SagWaitnMatchResp(hCom, ["*\r\nOK\r\n"], at_response_time_ms[str(baudrate)], "wildcard", "not_critical", "nologmsg")
        if match_result == 1:
            SagSendAT(hCom, "AT+IPR=115200;&w\r")
            SagWaitnMatchResp(hCom, ["*\r\nOK\r\n"], at_response_time_ms[str(baudrate)])
            time.sleep(2)

            SagClose(hCom)
            hCom = SagOpen(com_port,115200,8,"N",1,"Hardware")
            break
    return hCom



def SafePrintLog( Msg, color = 8):
    "goal of the method : This method displays information, using a mutex"
    "INPUT : "
    "OUTPUT : "

    print_mutex.acquire()  
    VarGlobal.myColor = VarGlobal.colorLsit[color]
    print str(Msg)
    VarGlobal.myColor = VarGlobal.colorLsit[8]
    print_mutex.release()

def initiateAvmsConnection(hCom, recv = ["\r\n+WDSI: 4\r\n","\r\n+WDSI: 6\r\n","\r\n+WDSI: 8\r\n"], count=1):
    if count != 5:
        resp = 1
        print "this is " + str(count) + "th try"
        SagSendAT(hCom, "AT+WDSS=1,1\r\n")
        SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], 10000, update_result="not_critical")
        for i in range(0,len(recv)):
            resp = resp * SagWaitnMatchResp(hCom, [recv[i]], 180000, update_result="not_critical")        
        
        if resp != 1:
            count += 1
            initiateAvmsConnection(hCom, recv,count)
    else:
        VarGlobal.statOfItem="NOK"
        print "Connection to AVMS fails in 5 try\n"
            
def WaitComPortBack(hCom):
    count = 1
    COM = 'COM' + str(hCom)
    Not_Back = True
    while Not_Back:
        print "This is %sth trial to get %s back" % (str(count),COM)
        time.sleep(10)
        print "Sleep 10 second"
        for com_port in serial.tools.list_ports.comports():
            print com_port
            if COM in com_port:
                print "%s has come back" % COM
                Not_Back = False
                break
        count += 1
        if count == 10:
            print "Wait Com Port Back : Fail. %s is lost" % COM
            Not_Back = False
            break

# Do not use below GNSS API any more
def GetGpsStatus(hCom, expected_resp, fix_timeout = 255, time_sleep = 10, printmode="symbol"):
    "goal of the method : this method is used to get gps status"
    "INPUT :  hCom : the COM port use to interact"
    "         expected_resp (list) : expected response"
    "         fix_timeout (sec) : the given time out use to check gps status"
    "         time_sleep (sec)  : time sleep"
    "OUTPUT : Boolean >> True:response matched, False: response mismatched"
    
    strTemp = VarGlobal.statOfItem
    start_time = int(round(time.time()*1000))
    matched = False
    while (1):
        SagSendAT(hCom, "AT!GPSSTATUS?\r")
        answer = SagWaitResp(hCom, ["*OK\r\n"], 3000)
        for (each_item) in expected_resp:
            receivedResp = answer
            expectedResp = each_item
            
            if fnmatch.fnmatchcase(receivedResp, expectedResp):
                matched = True
                return matched
                
        if matched == 0:
            if (int(round(time.time()*1000)) - start_time) > (fix_timeout * 1000):
                if len(expected_resp) == 1:
                    SafePrintLog("")
                    SafePrintLog("Expected Response: %s" % ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                    SafePrintLog("Received Response: %s" % ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                    SafePrintLog("")
                if len(expected_resp) > 1:
                    SafePrintLog("")
                    SafePrintLog("Expected Response: %s" % ascii2print(expected_resp[0],printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                    for (i,each_elem) in enumerate(expected_resp):
                        if i == 0:
                            pass
                        if i >0:
                            SafePrintLog("Expected Response: %s" % ascii2print(each_elem,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                    SafePrintLog("Received Response: %s" % ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                    SafePrintLog("")
                strTemp = "NOK"
                VarGlobal.statOfItem = strTemp
                return matched
            else:
                time.sleep(time_sleep)

def ColdStartGPS(hCom, timeout = 65):
    strTemp = VarGlobal.statOfItem
    start_time = int(round(time.time()*1000))
    while(1):
        print '----------------------'
        SagSendAT(hCom,"AT!GPSCOLDSTART\r")
        response = SagWaitResp(hCom, ["*ERROR\r\n","*OK\r\n"], 3000)
        if (int(round(time.time()*1000)) - start_time) < (timeout * 1000):
            if "ERROR" in response or "ErrCode" in response:
                time.sleep(10)
            else:
                break
        else:
            break
def CheckAttachNW(hCom,pin_code,timeout=150):
    "goal of the method : this method is used to get Network status"
    "INPUT :  hCom : the COM port use to interact"
    "         pin_code : the pin code of SIM   "
    "         timeout (sec) : the given time out use to check Network status"
    "OUTPUT : Boolean >> True:response matched, False: response mismatched"
    SagSendAT(hCom, "AT+CFUN=1\r")
    SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], 3000)
    SagSendAT(hCom,"AT+CPIN?\r")
    anwser=SagWaitResp(hCom,["\r\n+CPIN: SIM PIN\r\n\r\nOK\r\n"],10000)
    if "SIM PIN" in anwser:
        SagSendAT(hCom, "AT+CPIN="+pin_code+"\r")
        SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], 3000) 
    start_time=time.time()
    while(1):
        SagSendAT(hCom, "AT!GSTATUS?\r")
        status=SagWaitResp(hCom,["*Attached*OK\r\n"],10000)
        if  "Attached" in status:
            return True
        elif (time.time()-start_time) > timeout:
            print "Module can't attach NetWork\r\n"
            return False
        else:
            time.sleep(10)
            continue      

def wait_and_check_ip_address(hCom, waitpattern, numberipaddress, timeout=60000, log_msg="logmsg", printmode="symbol"): 
    "goal of the method : this method waits for the data received from Com port"
    "INPUT : hCom : COM port object"
    "        waitpattern : the matching pattern for the received data"
    "        timeout (ms) : timeout between each received packet"
    "        log_msg : option for log message"
    "OUTPUT : Received data (String)"

    start_time = datetime.now()
    com_port_name = str(hCom.port)
    if log_msg == "debug":
        #print start_time
        SafePrintLog(start_time)
    global uartbuffer
    flag_matchrsp = False
    flag_matchstring = False
    flag_timeout = False
    flag_wait_until_timeout = False
    flag_printline = False
    LogMsg = ""
    timestamp = ""

    # wait until timeout mode
    if waitpattern == None or waitpattern[0] == "":
        flag_wait_until_timeout = True
        waitpattern = [""]
        SafePrintLog("")
        SafePrintLog("Wait responses in %s ms" % str(timeout))
        SafePrintLog("")

    displaybuffer = ""
    displaypointer = 0
    while 1:
        # Read data from UART Buffer
        if hCom.inWaiting()>0:
            uartbuffer[hCom.port] += hCom.read(hCom.inWaiting())
            if log_msg == "debug":
                #VarGlobal.myColor = VarGlobal.colorLsit[7]
                #print "Read data from UART buffer:", uartbuffer[hCom.port].replace("\r","<CR>").replace("\n","<LF>")
                #print "Read data from UART buffer:", ascii2print(uartbuffer[hCom.port],printmode)
                LogMsg = "Read data from UART buffer: "+ascii2print(uartbuffer[hCom.port],printmode)
                SafePrintLog(LogMsg,7)
        # Match response
        # Loop for each character
        for (i,each_char) in enumerate(uartbuffer[hCom.port]) :
            if log_msg == "debug":
                #VarGlobal.myColor = VarGlobal.colorLsit[7]
                #print i, uartbuffer[hCom.port][:i+1].replace("\r","<CR>").replace("\n","<LF>").replace("\n","<LF>")
                #print i, ascii2print(uartbuffer[hCom.port][:i+1],printmode)
                LogMsg = str(i)+" "+ascii2print(uartbuffer[hCom.port][:i+1],printmode)
                SafePrintLog(LogMsg,7)
            # display if matched with a line syntax
            displaybuffer = uartbuffer[hCom.port][displaypointer:i+1]
            line_syntax1 = "*\r\n*\r\n"
            line_syntax2 = "+*\r\n"
            line_syntax3 = "\r\n> "
            if fnmatch.fnmatchcase(displaybuffer, line_syntax1) or \
                fnmatch.fnmatchcase(displaybuffer, line_syntax2) or \
                fnmatch.fnmatchcase(displaybuffer, line_syntax3) :
                # display timestamp
                if VarGlobal.SndRcvTimestamp:
                    timestamp = TimeDisplay() + " "
                # display data
                #VarGlobal.myColor = VarGlobal.colorLsit[7]
                #received_data = displaybuffer.replace("\r","<CR>").replace("\n","<LF>").replace("\x15","<NAK>").replace("\x06","<ACK>").replace("\x00","<NULL>")
                received_data = ascii2print(displaybuffer,printmode)
                #print timestamp+"Rcv COM", com_port_name, "["+received_data+"]",
                LogMsg = timestamp+"Rcv "+com_port_name+" ["+received_data+"] "
                displaypointer = i+1
                flag_printline = True

            # match received response with waitpattern
            for (each_elem) in waitpattern:
                receivedResp = uartbuffer[hCom.port][:i+1]
                expectedResp = each_elem
                if fnmatch.fnmatchcase(receivedResp, expectedResp):
                    flag_matchstring = True
                    break
            if flag_matchstring:
                # display the remaining matched response when waitpettern is found
                displaybuffer = uartbuffer[hCom.port][displaypointer:i+1]
                if len(displaybuffer)>0:
                    # display timestamp
                    if VarGlobal.SndRcvTimestamp:
                        timestamp = TimeDisplay() + " "
                    # display data
                    #VarGlobal.myColor = VarGlobal.colorLsit[7]
                    #received_data = displaybuffer.replace("\r","<CR>").replace("\n","<LF>").replace("\x15","<NAK>").replace("\x06","<ACK>").replace("\x00","<NULL>")
                    received_data = ascii2print(displaybuffer,printmode)
                    #print "Rcv COM", com_port_name, "["+received_data+"]",
                    LogMsg = timestamp+"Rcv "+str(com_port_name)+" ["+received_data+"] "
                    pass

                # display time spent in receive
                if VarGlobal.RcvTimespent:
                    diff_time = datetime.now() - start_time
                    diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
                    #print " <"+str(timeout), " @"+str(diff_time_ms), "ms",
                    LogMsg += " <"+str(timeout)+" @"+str(diff_time_ms)+" ms "

                flag_printline = True

                # clear matched resposne in UART Buffer
                uartbuffer[hCom.port] = uartbuffer[hCom.port][i+1:]
                flag_matchrsp = True
                
                # break for Match response
                flag_matchrsp = True

            # print linebreak for EOL
            if flag_printline:
                flag_printline = False
                #print ""
                SafePrintLog(LogMsg,7)

            # break for Match response
            if flag_matchrsp:                
                break


        # Count timeout
        diff_time = datetime.now() - start_time
        diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
        if diff_time_ms > timeout:
            if log_msg == "debug":
                #print "Timeout: ", diff_time, "diff_time_ms:", diff_time_ms
                LogMsg = "Timeout: "+str(diff_time)+" diff_time_ms: "+str(diff_time_ms)
                SafePrintLog(LogMsg,7)
            # display the remaining response when timeout
            displaybuffer = uartbuffer[hCom.port][displaypointer:]
            if len(displaybuffer)>0:
                # display timestamp
                if VarGlobal.SndRcvTimestamp:
                    #VarGlobal.myColor = VarGlobal.colorLsit[7]
                    #print TimeDisplay(),
                    timestamp = TimeDisplay() + " "
                # display data
                #VarGlobal.myColor = VarGlobal.colorLsit[7]
                #received_data = receivedResp.replace("\r","<CR>").replace("\n","<LF>").replace("\x15","<NAK>").replace("\x06","<ACK>").replace("\x00","<NULL>")
                received_data = ascii2print(receivedResp,printmode)
                #print "Rcv COM", com_port_name, " ["+received_data+"]"
                LogMsg = "Rcv "+str(com_port_name)+" ["+received_data+"]"
                SafePrintLog(LogMsg,7)
                pass

            # clear all resposne in UART Buffer
            VarGlobal.myColor = VarGlobal.colorLsit[8]
            receivedResp = uartbuffer[hCom.port]

            if flag_wait_until_timeout != True:
                if log_msg == "logmsg" or log_msg == "debug":
                    if len(receivedResp) > 0:
                        VarGlobal.numOfResponse += 1.0
                        #print "\nNo Match! "+"@COM"+com_port_name+ " <"+str(timeout)+" ms\n"
                        LogMsg = "\nNo Match! "+"@COM"+com_port_name+" <"+str(timeout)+" ms\n"
                        SafePrintLog(LogMsg,7)
                    if len(receivedResp) == 0:
                        #print "\nNo Response! "+"@COM"+com_port_name+ " <"+str(timeout)+" ms\n"
                        LogMsg = "\nNo Response! "+"@COM"+com_port_name+ " <"+str(timeout)+" ms\n"
                        SafePrintLog(LogMsg,7)
            uartbuffer[hCom.port] = ""
            flag_timeout = True
        

        if flag_matchrsp:
            VarGlobal.numOfResponse += 1.0
            break
        if flag_timeout:
            break

    if log_msg == "debug":
        SafePrintLog("")
        SafePrintLog(str(len(uartbuffer[hCom.port])),7)
        LogMsg = "The remaining data in uartbuffer " + str((hCom.port + 1))  + " : [", ascii2print(uartbuffer[hCom.port],printmode), "]"
        SafePrintLog(LogMsg,7)
    receivedResp_ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', receivedResp)
    if len(receivedResp_ip) != numberipaddress:
        raise Exception("Sorry! The total number of ip addresses is not correct! We expect %s, but it's %s\n" %(str(numberipaddress),str(len(receivedResp))))
    for ipaddress in receivedResp_ip:
        try:
            IP(ipaddress)
        except Exception, err_msg :
            VarGlobal.statOfItem = "NOK"
            print Exception, err_msg

    match_result = SagMatchResp(receivedResp, waitpattern)
#    return match_result

def return_subnet(gateway_address):
    tmp_array = gateway_address.split('.')
    tmp_array.pop()
    subnet_return = '.'.join(tmp_array)
    return subnet_return

def SagSendRemoteAT(hCom, session, cmd, mtu):
    remote_cmd = []
    i = 0
    while len(cmd) >= (mtu-3)*i:
        if len(cmd) < (mtu-3)*(i+1):
            temp = cmd[(mtu-3)*i:len(cmd)]
            temp = 'AT+SRBCSMARTCMD=%s,"' % session + temp.replace('"', '\\22') + '\\0d"'
            remote_cmd.append(temp)
        else:
            temp = cmd[(mtu-3)*i:(mtu-3)*(i+1)]
            temp = 'AT+SRBCSMARTCMD=%s,"' % session + temp.replace('"', '\\22') + '"'
            remote_cmd.append(temp)
        i = i+1
    for c in remote_cmd:
        SagSendAT(hCom, '%s\r' % c)
        SagWaitnMatchResp(hCom, ['OK\r\n'], 2000)

def SagWaitRemoteResp(hCom, session, timeout):
    response = ''
    while True:
        temp = SagWaitResp(hCom, ['+SRBCSMARTRSP: %s,"*"\r\n' % session], 1000)
        if temp != '':
            SagMatchResp(temp, ['+SRBCSMARTRSP: %s,"*"\r\n' % session])
            res = temp.split('"')[1]
            response = response + res
        else:
            break
    return response

def SagWaitnMatchRemoteResp(hCom, session, waitpattern, timeout):
    receivedResp = SagWaitRemoteResp(hCom, session, timeout)
    temp_pattern = []
    for i in range(0, len(waitpattern)):
        temp = waitpattern[i].replace('\r\n', '\\0d\\0a').replace('"', '\\22')
        temp_pattern.append(temp)
    match_result = SagMatchResp(receivedResp, temp_pattern)
    return match_result


if __name__ == u'__main__':
        print get_ini_value ( r'C:\SVN\Configuration\SIM\CSL_3631.ini', "test", "test" )
    
    
