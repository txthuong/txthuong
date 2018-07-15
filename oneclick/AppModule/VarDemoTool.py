#!/usr/bin/env python
# _*_ coding: utf-8 _*_

#date              who                 version                 modification
#2008..2011        JM Ruffle           1.x                     creation and modifications
#29-02-2012        JM seillon          1.8.2                   modifications for GNSS feature (AT Starter)
#xx-04-2012        JM Seillon          1.8.4                   global variable flagStop, Latitude, Longitude
#xx-05-2012        JM Seillon          1.8.4                   add CheckNMEA
#13-09-2012        SII (MR)            1.9.2                   add variables Flag_SimoNXT and SOFT_SIMONXT for SIMONXT module behaviour
#11-03-2013		   Eric BARRE		   1.9.3				   HiloStarter: add the class ModuleTypeClass to support 3G module and fix the GNSS feature to support the display of the ID/SNR before fix

import wx

# Variables par defaut pour l'execution des scripts en mode DemoTool

flagStop = False
Histo = None
CheckNMEA = False #ajout Mai 2012
indice = None
# for ecall
GPS_config = False # external gps = False, internal = True 

# For COM & SIM
COM_Port  = "1"
SpeedList = ['1200','2400','4800','9600','19200','38400','57600','115200']
COM_Speed = SpeedList[-1]		# select max speed
SIM_PIN	  = "0000"

# For GPRS
GPRS_APN	  = ""
GPRS_Login	  = ""
GPRS_Password = ""

# For alarm +CALA 
Alarm=[0,0,0] #hours,minutes,seconds

# For FTP
'''
FTP_URL			 = "modules.dyndns.org"
FTP_Port		 = "21"
FTP_Login		 = "MODULES_USER"
FTP_Password	 = "ERIC_BARRE"
FTP_UplaodPath	 = "test ftp"
FTP_UplaodFile	 = ""
FTP_DownlaodPath = "test ftp"
FTP_DownlaodFile = "medium_file.txt"
'''

FTP_URL			 = ""
FTP_Port		 = "21"
FTP_Login		 = ""
FTP_Password	 = ""
FTP_UplaodPath	 = ""
FTP_UplaodFile	 = ""
FTP_DownlaodPath = ""
FTP_DownlaodFile = ""

# For TCP
TCP_URL  = "google.com"
TCP_Port = "80"

# For SMS
SMS_IRA = True
SMS_Number = "+336"
SMS_Text   = "Test send a SMS in text mode"

# For Voice call
VoiceCall_Number = "+336"

# For GPIO
GPIO_Number = ""
GPIO_Value  = ""

# For file System
FS_WriteName = ""
FS_WriteFile = ""
FS_ReadName  = ""

# For SMTP
'''
SMTP_Server	  = "smtp.mail.yahoo.fr"
SMTP_Email	  = "mailmodule@yahoo.fr"
SMTP_Login	  = "mailmodule"
SMTP_PassWor
SMTP_Email	  = "atstarter@yahoo.fr"
SMTP_Login	  = "atstarter"
SMTP_PassWord = "module"
'''

SMTP_Server	  = ""
SMTP_Email	  = ""
SMTP_Login	  = ""
SMTP_PassWord = ""
SMTP_To		  = ""
SMTP_Subject  = ""
SMTP_Text	  = ""

IMEI		 = ""
Soft_Version = ""
OperatorName = ""
Roaming		 = ""
SignalLevel	 = ""
PowerBand	 = ""
KCELL		 = [""]
IMSI		 = ""
HPLMN		 = ""
FPLMN		 = []
PPLMN		 = []

ICCIdentification = ""

PhoneBook	 = [""]
SMSOnSIM	 = [""]

PDU_File = ""

#GPS datas
Latitude = ""
Longitude = ""

# For eCall
eCall_Number = "+336"

#Variables added for particular module behaviour (SimonNXT) which does not respond "\r\n" after some specific requests
Flag_SimoNXT=False
SOFT_SIMONXT="Hi2C,A.900.04"

#Variables to detect the module type
# it is detected by the software name
ModuleType_HILO3G="HILO_3G"
ModuleType_HILO3GPS="HILO_3GPS"
ModuleType_HILO2G="HILO_2G"
ModuleType_HIALL2G="HIALL_2G"

class ModuleTypeClass():
	type=""
	def __init__(self):
		self.type= ModuleType_HILO2G
		
	def setType(self,softwareName):
		if softwareName.find("Hi3GC,")!= -1:
			self.type= ModuleType_HILO3G
		elif softwareName.find("HiN3GPS,")!= -1:
			self.type= ModuleType_HILO3GPS
		elif softwareName.find("SAGEMCOM HiAN")!= -1:
			self.type= ModuleType_HIALL2G
		elif softwareName.find("SAGEMCOM Hi")!= -1:
			self.type= ModuleType_HILO2G

moduleType=ModuleTypeClass() #GLOBAL to use


# Personal Event for run
class RunEvent(wx.PyCommandEvent):
	def __init__(self, evtType, ide):
		wx.PyCommandEvent.__init__(self, evtType, ide)
		self.status = False

	def GetRunStatus(self):
		return self.status

	def SetRunStatus(self, status):
		self.status = status

myEVT_RUN = wx.NewEventType()
EVT_RUN = wx.PyEventBinder(myEVT_RUN, 1)