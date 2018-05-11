#!/bin/env python
# _*_ coding: utf-8 _*_


#----------------------------------------------------------------------------
# Name:                 GPS_API.py
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
from VarGlobal import *
from ComModuleAPI import *

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
        