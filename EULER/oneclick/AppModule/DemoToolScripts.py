#!/usr/bin/env python
# _*_ coding: utf-8 _*_

#----------------------------------------------------------------------------
# Nom:		DemoToolScripts.py
# Objet:	Fenetres Dialog pour entrer les valeurs des variables
#
# Auteur:	Jean-Michel RUFFLE
# Date:		Mars 2009
#
# Auteur modification: Jean-Marc SEILLON
# Modification: ajout des fonctions GNSS_Start,GNSS_Stop, GNSS_Map.
# Modification de la liste 'fonction'
# Date:		Avril 2012
#
# Version:	AutoTest 1.8.3 DemoTool
# copyright Sagemcom
#----------------------------------------------------------------------------


#date              who                 version                 modification
#2008..2011        JM Ruffle           1.x                     creation and modifications
#28-02-2012        JM Seillon          1.8.2                   add functions GNSS_Start,GNSS_Stop, GNSS_Map.
#                                                              Modification of list 'fonction'
#23-03-2012        JM Seillon          1.8.3                   changes for GNSS feature
#xx-04-2012        JM Seillon          1.8.4                   changes for GNSS feature
#24-05-2012        (SII)MR             1.8.5                   Mdofify voice call sequence to avoid writing parameters Bug 3987
#xx-05-2012        JM Seillon          1.8.6                   before GNSS fix, messages are displayed (were not before)
#                                                              optionally don't send AT+KGNSS* anymore (for 3G, to be done by external tool)

#18-06-2012        JM Seillon          1.8.7                   Deletion of the message box "Waiting for fix", bug 4118
#                                                              Modify the fields where is displayed "FIX in progress", field "FieldTTFF", bug 4122
#25-06-2012        JM Seillon          1.8.7                   Initialization of the variable "data", bug 4151
#
#18-06-2012        JM Seillon          1.8.7                   Deletion of the message box "Waiting for fix", bug 4118
#                                                              Modify the fields where is displayed "FIX in progress", field "FieldTTFF", bug 4122
#25-06-2012        JM Seillon          1.8.7                   Initialization of the variable "data", bug 4151
#10-07-2012        SII (MR)            1.8.8                   Add possible response to AT+CREG? command (Factory need)
#26-07-2012        JM Seillon          1.9.0                   Clear the histo graph and array of data for each startGNSS
#26-07-2012        JM Seillon          1.9.1                   Clear the information fields for each startGNSS
#13-09-2012		   SII (MR)			   1.9.2				   Modify def Init(...) and def Voice_Call_Call(...) for a particular module : SIMONXT
#11-03-2013		   Eric BARRE		   1.9.3				   HiloStarter: did modifications to support 3G module and fix the GNSS feature to support the display of the ID/SNR before fix

from ComModuleAPI import SagWaitLine, SagTestCmd,SagSend, SagClose, SagOpen, SagStartThread
from Mux0710 import *
from PersonalException import *
from threadStop		   import Thread
from VarGlobal		   import VERSION
import VarDemoTool
import MessagesGNSS
import Histo
import thread
from MSDeCall import *

MRM = None
flagIE = True


# Timer on RECV command (ms) ------------------------------------
C_TIMER_LOW 	   = 5000    # Short local command (ms) :  5s
C_TIMER_MEDIUM 	   = 20000   # Long local commands (ms) : 20s
C_TIMER_HIGH 	   = 61000   # Network use (ms)		 : 1min 1s
C_TIMER_REALY_HIGH = 300000  #						 : 5min
C_TIMER_EXTRA_HIGH = 3600000 #						 : 1h


# Raise run event (to desable NoteBook)
def RaiseRunEvent(object):
	evt = VarDemoTool.RunEvent(VarDemoTool.myEVT_RUN, object.GetId())						# Set Event Run
	evt.SetRunStatus(True)
	object.GetEventHandler().ProcessEvent(evt)

# Clear run event (to enable NoteBook)
def ClearRunEvent(object):
	evt = VarDemoTool.RunEvent(VarDemoTool.myEVT_RUN, object.GetId())						# Set Event Run
	evt.SetRunStatus(False)
	object.GetEventHandler().ProcessEvent(evt)

# Function to start script
def StartScript(test,noteBook):
	print test
	functions.get(test,Error)(noteBook)		# excecute test or if test is not a function excecute Error()

#########
# Scripts #
#########
def Init(MRM, GSM=True, GPRS=True):
	print "Init AT	commands"

	print "\r\nAT starter version : %s\r\n"%VarGlobal.VERSION
#Bug 3987	SagSend(MRM, 'ATE0+CMEE=1\r')
#Bug 3987	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
#Bug 3987	SagTestCmd(resultat.tabLines, ["OK"])
	
#Variable added for particular module behaviour (SimonNXT) which does not respond "\r\n" after some specific requests
	nIndice=1
	VarDemoTool.Flag_SimoNXT=False
	
	SagSend(MRM, 'AT+CGMR\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	SagTestCmd(resultat.tabLines, ["OK"])
	
#set the module type
	VarDemoTool.moduleType.setType(resultat.tabLines[1][0])

#If the software is a SIMONXT, the indice to read information is not the same comparing to a standard module.
	if resultat.tabLines[1][0].find(VarDemoTool.SOFT_SIMONXT)!= -1:
			nIndice=0
			VarDemoTool.Flag_SimoNXT=True	

#set the sleep mode to 2: the module never enters in sleep
	SagSend(MRM, 'AT+KSLEEP=2\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	SagTestCmd(resultat.tabLines, ["OK"])
	
#remove the echo mode
	SagSend(MRM, 'ATE0\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	SagTestCmd(resultat.tabLines, ["OK"])
	
#SEND *PSPRAS command
	if VarDemoTool.moduleType.type!=VarDemoTool.ModuleType_HILO3G and VarDemoTool.moduleType.type!=VarDemoTool.ModuleType_HILO3GPS:
		SagSend(MRM, 'AT*PSPRAS?\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		result = SagTestCmd(resultat.tabLines, ["*PSPRAS:","OK"])
		if result == 0 and resultat.tabLines[1][0].startswith("*PSPRAS: 1"):
			SafePrint(None,None,"Stop : PIN CODE Last try!! Security procedure : Enter manualy your pin code",9)
			raise stop_exception
	
	#SEND +CPIN command
	SagSend(MRM, 'AT+CPIN?\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW, errorKeyWords=["ERROR","+CME ERROR: 10","+CME ERROR: SIM not inserted"])
	try:
		rcv = resultat.tabLines[nIndice][0]
	except:
		raise receive_exception
	
	if rcv.startswith("ERROR") or rcv.startswith("+CME ERROR: 10") or rcv.startswith("+CME ERROR: SIM not inserted"):
		SafePrint(None,None,"No SIM card detected !!",9)
		raise stop_exception
	
	PinNotOK = not(rcv.startswith("+CPIN: READY"))
	
	if PinNotOK and VarDemoTool.SIM_PIN!="":
		SagSend(MRM, 'AT+CPIN="'+VarDemoTool.SIM_PIN+'"\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW, errorKeyWords=["ERROR","+CME ERROR: 16","+CME ERROR: incorrect password","+CME ERROR: 12","+CME ERROR: SIM PUK required"])
		result = SagTestCmd(resultat.tabLines, ["OK"])
		try:
			rcv = resultat.tabLines[nIndice][0]
		except:
			raise receive_exception
		if rcv.startswith("ERROR") or rcv.startswith("+CME ERROR: 16") or rcv.startswith("+CME ERROR: incorrect password"):
			SafePrint(None,None,"Stop : BAD PIN CODE !!",9)
			raise stop_exception
		if rcv.startswith("ERROR") or rcv.startswith("+CME ERROR: 12") or rcv.startswith("+CME ERROR: SIM PUK required"):
			SafePrint(None,None,"Stop : SIM PUK required !!",9)
			raise stop_exception
		
		SagSend(MRM, 'AT+CPIN?\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		result = SagTestCmd(resultat.tabLines, ["+CPIN: READY","OK"])
	else:
		result = SagTestCmd(resultat.tabLines, ["+CPIN: READY","OK"])
	
#Bug 3987	SagSend(MRM, "AT+CREG=0\r")
#Bug 3987	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
#Bug 3987	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	if GSM:
		bLoop = True
		while bLoop:
			SagSend(MRM, "AT+CREG?\r")
			resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
			try:
				next_creg_01 = not(resultat.tabLines[nIndice][0].startswith("+CREG: 0,1"))
				next_creg_11 = not(resultat.tabLines[nIndice][0].startswith("+CREG: 1,1"))
				next_creg_05 = not(resultat.tabLines[nIndice][0].startswith("+CREG: 0,5"))
			except:
				bLoop = True
			if next_creg_01 and next_creg_11 and next_creg_05:
				SagSleep(2000,silent=True)
			else:
				bLoop = False
		
		if not next_creg_01:
			result = SagTestCmd(resultat.tabLines, ["+CREG: 0,1", "OK"])
		elif not next_creg_11:
			result = SagTestCmd(resultat.tabLines, ["+CREG: 1,1", "OK"])
		elif not next_creg_05:
			result = SagTestCmd(resultat.tabLines, ["+CREG: 0,5", "OK"])
	
#Bug 3987	SagSend(MRM, "AT+CGREG=0\r")
#Bug 3987	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
#Bug 3987	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	if GPRS:
		bLoop = True
		while bLoop:
			SagSend(MRM, "AT+CGREG?\r")
			resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
			try:
				next_cgreg_01 = not(resultat.tabLines[nIndice][0].startswith("+CGREG: 0,1"))
				next_cgreg_11 = not(resultat.tabLines[nIndice][0].startswith("+CGREG: 1,1"))
				next_cgreg_05 = not(resultat.tabLines[nIndice][0].startswith("+CGREG: 0,5"))
			except:
				bLoop = True
			if next_cgreg_01 and next_cgreg_11 and next_cgreg_05:
				SagSleep(2000,silent=True)
			else:
				bLoop = False
		
		if not next_cgreg_01:
			result = SagTestCmd(resultat.tabLines, ["+CGREG: 0,1", "OK"])
		elif not next_cgreg_11:
			result = SagTestCmd(resultat.tabLines, ["+CGREG: 1,1", "OK"])
		elif not next_cgreg_05:
			result = SagTestCmd(resultat.tabLines, ["+CGREG: 0,5", "OK"])
		
#Bug 3987		SagSend(MRM, "AT+CGATT=1\r")
#Bug 3987		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
#Bug 3987		result = SagTestCmd(resultat.tabLines, ["OK"])
	
	if GSM:
		SagSend(MRM, "AT+CSQ\r")
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		result = SagTestCmd(resultat.tabLines, ["+CSQ: ","OK"])
		
		SagSend(MRM, "AT+COPS?\r")
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		result = SagTestCmd(resultat.tabLines, ["+COPS: ","OK"])
		
#Bug 3987		SagSend(MRM, "AT+KCELL=0\r")
#Bug 3987		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
#Bug 3987		result = SagTestCmd(resultat.tabLines, ["+KCELL:","OK"])


def eCall_Start(noteBook):
	indice=0
	for i in range(noteBook.GetPageCount()):
		if noteBook.GetPage(i).GetName() == "eCall":
			noteBook.ChangeSelection(i)
			indice=i
	
	#disable stop button
	noteBook.GetPage(indice).GetParent().GetParent().toolBar.EnableTool(noteBook.GetPage(indice).GetParent().GetParent().ID_stop, 0)
	
	#clear the user information area		
	noteBook.GetPage(indice).ZoneProc.SetValue("")

	# Open Com port
	try:
		MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
		VarGlobal.MRM = MRM
		Init(MRM,GPRS=False)
	except COM_exception:
		SafePrint(None,None,"\nError on com port opening ! Configure your port com, it is maybe busy.\n", color=9)
		return

	#Ecall not supported by Hilo3G or HiloV2
	if VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3G or VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO2G:
		SafePrint(None,	None, "SORRY HILO3G DOES NOT SUPPORT GNSS FEATURE",color = 4)
		SagClose(MRM)
	else:
		
		#if the user wants to use the internal GNNS : active the GNSS and wait for a fix
		if noteBook.GetPage(indice).GNSS_External==0:
			noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      Use internal GNSS\r\n"))
			#disable fix URCs
			SagSend(MRM, "AT+KGNSSFIX=0\r")
			resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
			
			#Check if GNSS is running
			SagSend(MRM, "AT+KGNSSRUN?\r")
			resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
			
			if resultat.tabLines[1][0]=="+KGNSSRUN: 0\r\n" or resultat.tabLines[1][0]=="+KGNSSRUN: 0, 0\r\n" or resultat.tabLines[1][0]=="+KGNSSRUN: 0, 1\r\n" or resultat.tabLines[1][0]=="+KGNSSRUN: 0, 2\r\n":
				#AT Start GNSS
				SagSend(MRM, "AT+KGNSSRUN=1\r")
				resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
			
			noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      GNSS activated (wait for fix)\r\n"))
			
			#Wait for the GNSS to fix
			#enable stop button
			noteBook.GetPage(indice).GetParent().GetParent().toolBar.EnableTool(noteBook.GetPage(indice).GetParent().GetParent().ID_stop, 1)

			bLoop = True
			while bLoop:
				try:
					SagSend(MRM, "AT+KGNSSFIX?\r")
					resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
					if resultat.tabLines[1][0]=="+KGNSSFIX: 0, 1\r\n" or resultat.tabLines[1][0]=="+KGNSSFIX: 1, 1\r\n" or resultat.tabLines[1][0]=="+KGNSSFIX: 2, 1\r\n":
						bLoop = False
					else:
						SafePrint(None,None,"\nWait for GNSS fix...\n", color=9)
						SagSleep(10000,silent=True)
				except IndexError:
					return
					
			noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      Internal GNNS is ready to start an ecall\r\n"))		

			#disable stop button
			noteBook.GetPage(indice).GetParent().GetParent().toolBar.EnableTool(noteBook.GetPage(indice).GetParent().GetParent().ID_stop, 0)

	
		noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      Start the ecall configuration\r\n"))
		SagSend(MRM, 'AT+KECALLCFG=1,'+str(noteBook.GetPage(indice).MyMSD.getVehiculeType())+',"'+noteBook.GetPage(indice).MyMSD.getVIN()+'",'+str(noteBook.GetPage(indice).MyMSD.getVehPropStrType())+'\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagSend(MRM, 'AT+KECALLCFG=2,'+str(noteBook.GetPage(indice).MyMSD.getNomberOfPassengers_o())+'\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		#if the user wants to use the external GNNS : use the command KECALLCFG=3 and fill it with the IHM values
		if noteBook.GetPage(indice).GNSS_External==1:
			SagSend(MRM, 'AT+KECALLCFG=3,"'+noteBook.GetPage(indice).MyMSD.getVehicleLocationLatitude()+'","'+noteBook.GetPage(indice).MyMSD.getVehicleLocationLongitude()+'",'+str(noteBook.GetPage(indice).MyMSD.getVehicleDirection())+','+str(noteBook.GetPage(indice).MyMSD.getConfidence())+'\r')
			resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		
		SagSend(MRM, "AT+KECALLCFG?\r")
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	
		noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      Start the ecall\r\n"))
		SagSend(MRM, 'AT+KECALL=0,"'+str(noteBook.GetPage(indice).MyMSD.getCallNumber())+'",'+str(noteBook.GetPage(indice).MyMSD.getActivationMode())+'\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)	

		EndOfEcall=False
		while EndOfEcall==False:
		
				#if VarDemoTool.flagStop:
				#	_Stop(noteBook)
				#	break
			
				resultat = SagWaitLine(MRM, ["+KECALL"], 30000)
				result = resultat.tabData.splitlines()
				for res in range(len(result)):
		
					if result[res][0:11:1] == "+KECALL: 11":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      There is no network coverage : End of eCall\r\n"))
						EndOfEcall=True
					elif result[res][0:11:1] == "+KECALL: 12":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      Call drop. Internal Network error : End of eCall\r\n"))
						EndOfEcall=True
					elif result[res][0:11:1] == "+KECALL: 13":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      The PSAP has ended the call : End of eCall\r\n"))
						EndOfEcall=True
					elif result[res][0:11:1] == "+KECALL: 14":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      An eCall is already in progress : End of eCall\r\n"))
						EndOfEcall=True
					elif result[res][0:11:1] == "+KECALL: 21":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      The PSAP line is busy : End of eCall\r\n"))
						EndOfEcall=True
					elif result[res][0:11:1] == "+KECALL: 41":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      Send MSD message reception timed out: switch to audio call\r\n"))
					elif result[res][0:11:1] == "+KECALL: 42":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      PSAP has required to send the MSD message but no new position has been received from the external GNSS so the previous GNSS position is used.\r\n"))
					elif result[res][0:11:1] == "+KECALL: 51":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      LL-ACK message reception timed out: switch to audio call\r\n"))
					elif result[res][0:11:1] == "+KECALL: 61":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      AL-ACK message reception timed out: switch to audio call\r\n"))
					elif result[res][0:11:1] == "+KECALL: 71":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      Call Clear down timed out: End of eCall\r\n"))
						EndOfEcall=True


					elif result[res][0:10:1] == "+KECALL: 1":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      Call to the PSAP in progress\r\n"))
					elif result[res][0:10:1] == "+KECALL: 2":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      eCall established\r\n"))						
					elif result[res][0:10:1] == "+KECALL: 3":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      Send the PUSH message\r\n"))		
					elif result[res][0:10:1] == "+KECALL: 4":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      Send MSD order has been received\r\n"))
					elif result[res][0:10:1] == "+KECALL: 5":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      LL-ACK message has been received\r\n"))			
					elif result[res][0:10:1] == "+KECALL: 6":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      AL-ACK message has been received\r\n"))
					elif result[res][0:10:1] == "+KECALL: 7":	
						noteBook.GetPage(indice).ZoneProc.AppendText((str(datetime.now())[0:19]+"      Clear down request received: End of eCall\r\n"))
						EndOfEcall=True



def eCall_Stop(noteBook):
	#TODO: a terminer
	SagStopAllThread(silent=True)


def FTP_Upload(noteBook):
	print "start FTP Upload script"
	
	FTP_UDP_EOF_PATTERN = "--EOF--Pattern--"
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM)
	
	# GPRS CONFIG
	SagSend(MRM, 'AT&k3\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	SagSetFlowControl(MRM,True)
	
	SagSend(MRM, 'AT+KPATTERN="'+FTP_UDP_EOF_PATTERN+'"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, 'AT+KCNXCFG=0,"GPRS","' + VarDemoTool.GPRS_APN + '","' + VarDemoTool.GPRS_Login + '","' + VarDemoTool.GPRS_Password + '"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW,True)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, 'AT+KCNXTIMER=0,60\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	# FTP CONFIG
	SagSend(MRM, 'AT+KFTPCFG=0,"' + VarDemoTool.FTP_URL + '","' + VarDemoTool.FTP_Login + '","' + VarDemoTool.FTP_Password + '",' + VarDemoTool.FTP_Port + ',1\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW,True)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		FtpCfg = resultat.tabLines[1][0].split(": ")[1][:-2]
		
		# SEND a file
		SagSend(MRM, 'AT+KFTPSND=' + FtpCfg + ',,"' + VarDemoTool.FTP_UplaodPath + '","' + VarDemoTool.FTP_UplaodFile.split('\\')[-1]  + '"\r')
		resultat = SagWaitLine(MRM, ["CONNECT"], C_TIMER_MEDIUM,True)
		result = SagTestCmd(resultat.tabLines, ["CONNECT"])
		
		if result == 0:
			SagSendFile(MRM, VarDemoTool.FTP_UplaodFile, FTP_UDP_EOF_PATTERN, silent=True)
		
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_MEDIUM)
		result = SagTestCmd(resultat.tabLines, ["OK"])
		
		# Close connection
		SagSend(MRM, 'AT+KFTPCLOSE='+FtpCfg+'\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, "AT+CSQ\r")
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["+CSQ: ","OK"])
	
	SagSend(MRM, "AT+KCELL=0\r")
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["+KCELL:","OK"])
	
	SagClose(MRM)

def FTP_Download(noteBook):
	print "start FTP Download script"
	
	FTP_UDP_EOF_PATTERN = "--EOF--Pattern--"
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM)
	
	# GPRS CONFIG
	SagSend(MRM, 'AT&k3\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	SagSetFlowControl(MRM,True)
	
	SagSend(MRM, 'AT+KPATTERN="'+FTP_UDP_EOF_PATTERN+'"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, 'AT+KCNXCFG=0,"GPRS","' + VarDemoTool.GPRS_APN + '","' + VarDemoTool.GPRS_Login + '","' + VarDemoTool.GPRS_Password + '"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW,True)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, 'AT+KCNXTIMER=0,60\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	# FTP CONFIG
	SagSend(MRM, 'AT+KFTPCFG=0,"' + VarDemoTool.FTP_URL + '","' + VarDemoTool.FTP_Login + '","' + VarDemoTool.FTP_Password + '",' + VarDemoTool.FTP_Port + ',1\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW,True)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		FtpCfg = resultat.tabLines[1][0].split(": ")[1][:-2]
		
		# Receive a file
		SagSend(MRM, 'AT+KFTPRCV=' + FtpCfg + ',,"' + VarDemoTool.FTP_DownlaodPath + '","' + VarDemoTool.FTP_DownlaodFile + '",0\r')
		#resultat = SagWaitLine(MRM, ["CONNECT"], C_TIMER_MEDIUM,True)
		#result = SagTestCmd(resultat.tabLines, ["CONNECT"])
		
		if result == 0:
			if not(os.path.isdir("DATA")):
				os.mkdir("DATA")
			if not(os.path.isdir("DATA\\FTP")):
				os.mkdir("DATA\\FTP")
			SagWaitTextFile(MRM,"DATA\\FTP\\"+str(datetime.now()).split(".")[0].replace(":","h",1).replace(":","m").replace(" ","_") + "_" + VarDemoTool.FTP_DownlaodFile, EOF = FTP_UDP_EOF_PATTERN, SOF="CONNECT\r\n", silent = True)
			resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
			result = SagTestCmd(resultat.tabLines, ['OK'])
		#SagSleep(1000,silent=True)
		
		# Close connection
		SagSend(MRM, 'AT+KFTPCLOSE='+FtpCfg+'\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, "AT+CSQ\r")
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["+CSQ: ","OK"])
	
	SagSend(MRM, "AT+KCELL=0\r")
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["+KCELL:","OK"])
	
	SagClose(MRM)

def TCP_REQUEST(noteBook):
	print "start TCP Request script"
	
	FTP_UDP_EOF_PATTERN = "--EOF--Pattern--"
	TCPFile  = "GET / HTTP/1.0\r\n\r\n"
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM)
	
	# GPRS CONFIG
	SagSend(MRM, 'AT&k3\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	SagTestCmd(resultat.tabLines, ["OK"])
	SagSetFlowControl(MRM,True)
	
	SagSend(MRM, 'AT+KPATTERN="'+FTP_UDP_EOF_PATTERN+'"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, 'AT+KCNXCFG=0,"GPRS","' + VarDemoTool.GPRS_APN + '","' + VarDemoTool.GPRS_Login + '","' + VarDemoTool.GPRS_Password + '"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW,True)
	SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, 'AT+KCNXTIMER=0,60\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	SagTestCmd(resultat.tabLines, ["OK"])

	# +KCNSPROFILE not supported on Hilo3G and Hilo3GPS
	if VarDemoTool.moduleType.type!=VarDemoTool.ModuleType_HILO3G and VarDemoTool.moduleType.type!=VarDemoTool.ModuleType_HILO3GPS:
		SagSend(MRM, 'AT+KCNXPROFILE=0\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])
	
	# TCP CONFIG
	SagSend(MRM, 'AT+KTCPCFG=0,0,"'+VarDemoTool.TCP_URL+'",'+VarDemoTool.TCP_Port+'\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		TcpCfg = str(resultat.tabLines[1][0].split(": ")[1][:-2])
		
		SagSend(MRM, 'AT+KTCPCNX='+TcpCfg+'\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_HIGH)
		result = SagTestCmd(resultat.tabLines, ["OK"])
		
		if result == 0:
			SagSend(MRM, 'AT+KTCPSND='+TcpCfg+','+str(len(TCPFile))+'\r')
			resultat = SagWaitLine(MRM, ["CONNECT"], C_TIMER_HIGH)
			result = SagTestCmd(resultat.tabLines, ["CONNECT"])
			
			if result == 0:
				SagSend(MRM, TCPFile+FTP_UDP_EOF_PATTERN)
				resultat = SagWaitLine(MRM, ["OK"], C_TIMER_MEDIUM)
				result = SagTestCmd(resultat.tabLines, ["OK"])
				
				resultat = SagWaitLine(MRM, ["+KTCP_DATA: "+TcpCfg+","], C_TIMER_HIGH)
				result = SagTestCmd(resultat.tabLines, ["+KTCP_DATA: "+TcpCfg+","])
				
				#resultat2 = SagWaitLine(MRM, ["+KTCP_NOTIF: "+TcpCfg+",4"], C_TIMER_HIGH)
				#result2 = SagTestCmd(resultat2.tabLines, ["+KTCP_NOTIF: "+TcpCfg+",4"])
				
				SagSleep(1000,silent=True)
				
				if result == 0 and resultat.tabLines[-1][0].find("+KTCP_DATA: ") != -1:
					datalen = str(resultat.tabLines[-1][0].split("+KTCP_DATA: "+TcpCfg+",")[-1]).replace("\r","").replace("\n","")
					
					SagSend(MRM, 'AT+KTCPRCV='+TcpCfg+','+datalen+'\r')
					if not(os.path.isdir("DATA")):
						os.mkdir("DATA")
					if not(os.path.isdir("DATA\\TCP")):
						os.mkdir("DATA\\TCP")
					SagWaitTextFile(MRM,"DATA\\TCP\\"+str(datetime.now()).split(".")[0].replace(":","h",1).replace(":","m").replace(" ","_") + "_" + VarDemoTool.TCP_URL + "_index.html", EOF = FTP_UDP_EOF_PATTERN, SOF = "CONNECT\r\n", silent = True,timeout=30000)
					resultat = SagWaitLine(MRM, ["+KTCP"], C_TIMER_LOW)
					result = SagTestCmd(resultat.tabLines, ['+KTCP'])
		
		SagSend(MRM, 'AT+KTCPCLOSE='+TcpCfg+',1\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		result = SagTestCmd(resultat.tabLines, ["OK"])
		
		SagSend(MRM, 'AT+KTCPDEL='+TcpCfg+'\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagClose(MRM)

def SMS_SEND(noteBook):
	print "start SMS send script"
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM,GPRS=False)
	
	if VarDemoTool.SMS_IRA:
		# SEND SMS in IRA mode
		
		SagSend(MRM, 'AT+CSCS="IRA"\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		result = SagTestCmd(resultat.tabLines, ["OK"])
	else:
		# send SMS in UCS2 mode
		VarDemoTool.SMS_Number = ''.join(["%04x" % ord(x) for x in VarDemoTool.SMS_Number])
		VarDemoTool.SMS_Text = ''.join(["%04x" % ord(x) for x in VarDemoTool.SMS_Text])
		
		SagSend(MRM, 'AT+CSCS="UCS2"\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, "AT+CMGF=1\r")
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, 'AT+CMGS="' + VarDemoTool.SMS_Number + '"\r')
	resultat = SagWaitLine(MRM, ["> "], C_TIMER_LOW)
	if resultat.tabLines[1][0]!="> ":
		VarGlobal.statOfItem = 'NOK'		
		VarGlobal.numOfFailedResponse += 1.0
		result=1
		print '!!! Failed, expected response was : "> "'
	else:
		SagSend(MRM, VarDemoTool.SMS_Text + chr(26))
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_MEDIUM)
		result = SagTestCmd(resultat.tabLines, ["+CMGS", "OK"])
		
		if result != 0:
			SagSend(MRM, chr(27))
	
	SagClose(MRM)

def SMS_Wait_Incomming_SMS(noteBook):
	print "start SMS receive script"
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM,GPRS=False)
	
	SagSend(MRM, "AT+CNMI=2,1,0,1,0\r")
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, "AT+KRIC=2\r")
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, 'AT+CPMS="ME","ME","ME"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	# wait incomming SMS
	RIsignal = SagWaitRI(MRM,C_TIMER_MEDIUM)
	
	if RIsignal:
		resultat = SagWaitLine(MRM, ['+CMTI: "ME",'], C_TIMER_MEDIUM)
		result = SagTestCmd(resultat.tabLines, ['+CMTI: "ME",'])
		if result == 0:
			SMSnumber = resultat.tabLines[1][0].split('+CMTI: "ME",')[1]
			
			SagSend(MRM, "AT+CMGR="+SMSnumber)
			resultat = SagWaitLine(MRM, ["OK"], C_TIMER_HIGH)
			result = SagTestCmd(resultat.tabLines, ["OK"])
			
			SagSend(MRM, "AT+CMGD="+SMSnumber)
			resultat = SagWaitLine(MRM, ["OK"], C_TIMER_HIGH)
			result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, "AT+CNMI=2,0,0,1,0\r")
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagClose(MRM)
	
def Voice_Call_Call(noteBook):
	print "start Voice call"
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM,GPRS=False)
	
	if VarDemoTool.Flag_SimoNXT==False:
		
		#remove the + for hilo3G modules
		if VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3G or VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3GPS:
			VarDemoTool.VoiceCall_Number = VarDemoTool.VoiceCall_Number.replace("+","00") #3G modules does not support +

		SagSend(MRM, "ATD"+VarDemoTool.VoiceCall_Number+";\r")
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		result = SagTestCmd(resultat.tabLines, ["OK"])
	
		if result == 0:
			dlg = wx.MessageDialog(None, "Press OK to Hang up","Hang up ?" ,wx.ICON_QUESTION)
			if dlg.ShowModal() == wx.ID_OK:
				SagSend(MRM, "ATH\r")
				resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
				result = SagTestCmd(resultat.tabLines, ["OK"])
	else:		
		SagSend(MRM, "ATD"+VarDemoTool.VoiceCall_Number+";\r")
		SagSleep(3000, True)
		dlg = wx.MessageDialog(None, "Press OK to Hang up","Hang up ?" ,wx.ICON_QUESTION)
		if dlg.ShowModal() == wx.ID_OK:
			SagSend(MRM, "ATH\r")
							
	SagClose(MRM)
	
def GNSS_Start(noteBook):
	""" start satellite detection """
	print "start satellite detection"
	global flagIE
	global MRM

	flagIE = False
	''' Search the GNSS index tab'''
	indice=0
	for i in range(noteBook.GetPageCount()):
		if noteBook.GetPage(i).GetName() == "GNSS":
			noteBook.ChangeSelection(i)
			indice=i

	noteBook.GetPage(indice).Enable(False)
	VarDemoTool.indice = indice
	noteBook.GetPage(indice).GetParent().GetParent().toolBar.EnableTool(noteBook.GetPage(indice).GetParent().GetParent().ID_startGNSS, 0)
	noteBook.GetPage(indice).GetParent().GetParent().toolBar.EnableTool(noteBook.GetPage(indice).GetParent().GetParent().ID_stopGNSS, 0)

	''' Reset the infos fields '''
	noteBook.GetPage(indice).GNSS_Infos.FieldLongitude.SetValue(" ")
	noteBook.GetPage(indice).GNSS_Infos.FieldLatitude.SetValue(" ")
	noteBook.GetPage(indice).GNSS_Infos.FieldTimeUTC.SetValue(" ")
	noteBook.GetPage(indice).GNSS_Alt.FieldSOG.SetValue("")
	noteBook.GetPage(indice).GNSS_Alt.FieldHDOP.SetValue(" ")
	noteBook.GetPage(indice).GNSS_Alt.FieldAltitude.SetValue(" ")
	noteBook.GetPage(indice).GNSS_Infos.FieldSatUsed.SetValue(" ")
	noteBook.GetPage(indice).GNSS_Infos.FieldSatInView.SetValue(" ")


	# Open Com port
	try:
		MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
		VarGlobal.MRM = MRM
		Init(MRM,GPRS=False)
	except COM_exception:
		SafePrint(None,None,"\nError on com port opening ! Configure your port com, it is maybe busy.\n", color=9)
		noteBook.GetPage(indice).GetParent().GetParent().toolBar.EnableTool(noteBook.GetPage(indice).GetParent().GetParent().ID_startGNSS, 1)
		return

	#GNSS not supported by Hilo3G	
	if VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3G:
		SafePrint(None,	None, "SORRY HILO3G DOES NOT SUPPORT GNSS FEATURE",color = 4)
		SagClose(MRM)
	else:
		if not VarDemoTool.CheckNMEA: # Modif Mai 2012
			"""AT Stop GNSS"""
			SagSend(MRM, "AT+KGNSSRUN?\r")
			resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
			
			if resultat.tabLines[1]=="+KGNSSRUN: 1\r\n":
				SagSend(MRM, "AT+KGNSSRUN=0\r")
				resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)

				if resultat != 0:
					SafePrint(None,None,"\nWARNING BAD COM PORT >>>>>>>>>  VERIFY THE COM PORT CONFIGURATION !\n", color=9)
					noteBook.GetPage(indice).GetParent().GetParent().toolBar.EnableTool(noteBook.GetPage(indice).GetParent().GetParent().ID_startGNSS, 1)
					return
	
			
	
		
			"""AT Start GNSS """
			SagSend(MRM, "AT+KGNSSRUN=1\r")
			SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		
		
			""" Config UART """
			if VarDemoTool.moduleType.type!=VarDemoTool.ModuleType_HILO3GPS: #HILONC3GPS does not support this command on the UART
				SagSend(MRM, "AT+KUARTCFG=1\r")
				SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		
			noteBook.GetPage(indice).GNSS_Infos.FieldTTFF.SetValue("FIX in progress")
			
		
			""" Config a FIX (2,0):
			Mode=2 -> Require GNSS position information
			Pos=0 -> last position
			"""
			noteBook.GetPage(indice).GNSS_Infos.FieldTTFF.SetValue("")
		
			"""
			Command recieve (1,0)
			1=activate sending standard NMEA frames
			0=UART0 or UART1 depending on KUARTCFG 
			"""
			SagSend(MRM, "AT+KNMEARCV=1,0\r")
			resultat = SagWaitLine(MRM, ["CONNECT"], C_TIMER_LOW)
		noteBook.GetPage(indice).Enable(True) #Modif Mai 2012
	
		GNSS_TraitMess(noteBook,indice)

def GNSS_TraitMess(noteBook,indice):
	global flagIE
	start = True
	TimeToFIX = ""
	flagFIX = False
	flagPast = False
	flagIE = True
	MessDictGP = {}
	MessDictGL = {}
	List_SAT_USED = [] #list of ID of satellites used
	List_GPS_VIEW = [] #list of color, ID of GPS satellites, SNR VIEW
	List_GLN_VIEW = [] #list of color, ID of GLONASS satellites, SNR VIEW
	DISPLAY_DATA_SAT = [] #used to display the bar graph

	SOG=""
	SatView = 0
	idGNGSA = 1 # GNGSA counter frames
	nbGPSSatView=0 #number of GPS satellites in view
	nbGLNSatView=0 #number of GLONASS satellites in view
	displayHisto=False #if true display the information in the bar graph, it is set to True when a complete sequence of GPGSV frame have been receive
	histo = VarDemoTool.Histo
	if histo:
		histo.ClearListData()
	starttimestamp = datetime.now()
	try:
		histo.Show(True)
		histo.UpdateWindowUI()
	except :
		print "Crash sur creation frame histo"
	TotalK = 1	
	while TotalK < 25:
	#	print"TotalK: ", TotalK
		noteBook.GetPage(indice).GNSS_SNR.FindWindowByName("FieldIDSat"+str(TotalK)).SetOwnBackgroundColour("WHITE")
		noteBook.GetPage(indice).GNSS_SNR.FindWindowByName("FieldIDSat"+str(TotalK)).SetValue(" ")
		noteBook.GetPage(indice).GNSS_SNR.FindWindowByName("FieldSnrSat"+str(TotalK)).SetOwnBackgroundColour("WHITE")
		noteBook.GetPage(indice).GNSS_SNR.FindWindowByName("FieldSnrSat"+str(TotalK)).SetValue(" ")
		TotalK += 1

#==================================================================
	while True:
		''' Main loop endless'''
		if VarDemoTool.flagStop:
#			print"=== StopGNSS === ",str(VarDemoTool.flagStop)
			GNSS_Stop(noteBook)
			break
		
	
#====================================================================================
# begin the GP processing
#====================================================================================
#		print"\r=== processing GPRMC message ===\r"
		resultat = SagWaitLine(MRM, ["$GPRMC","$GPGGA","$GNGSA","$GPGSV","$GLGSV"], C_TIMER_LOW)
		result = resultat.tabData.splitlines()
# result = pile de messages
#		print"GPRMC result: "+ str(result)



		# recherche de l'entête "$GPRMC" dans la pile de messages
		for res in range(len(result)):
# processing $GPRMC message
#			print "pile messages : " + str(result[res][0:6:1])
			messGPRMC = None
			gprmcMess = None
			flagErreur = False
			if result[res][0:6:1] == "$GPRMC":
				try:
					gprmcMess = str.replace(result[res],'*',',*',1)
				except IndexError:
					print"\rGPRMC message IndexError !\r"
					flagErreur = True
		#		print"gprmcMess: " + str(gprmcMess)
		#		print"long mess: " + str(len(gprmcMess.split(',')))
		
				try:
					lengprmcMess = len(gprmcMess.split(','))
				except AttributeError:
					MessDictGP.clear()
					MessDictGL.clear()
					flagErreur = True
				
		
				if lengprmcMess >= 12 and flagErreur == False and gprmcMess.split(',')[0] == "$GPRMC" :
					noteBook.GetPage(indice).GetParent().GetParent().toolBar.EnableTool(noteBook.GetPage(indice).GetParent().GetParent().ID_stopGNSS, 1)
					#print "mess GPRMC: " + str(gprmcMess.split(','))
					messGPRMC = MessagesGNSS.GPRMC_Class(gprmcMess)
					noteBook.GetPage(indice).GNSS_Infos.FieldTimeUTC.SetValue(str(messGPRMC.get_UTCTIME()))
					if gprmcMess.split(',')[2] == 'V': #data not valide
						noteBook.GetPage(indice).GNSS_Infos.FieldLongitude.SetValue(" ")
						noteBook.GetPage(indice).GNSS_Infos.FieldLatitude.SetValue(" ")
					elif gprmcMess.split(',')[2] == 'A' and len(gprmcMess.split(',')) > 11: #data valide
						try:
							latit_deg = float(gprmcMess.split(',')[3][0:2:1])
							latit_min = float(gprmcMess.split(',')[3][2:4:1] + '.' + gprmcMess.split(',')[3][5::1])
							try:
								NS = gprmcMess.split(',')[4][0]
							except IndexError:
								print"\rGPRMC message: IndexError wrong field NS !"
							longit_deg = float(gprmcMess.split(',')[5][0:3:1])
							longit_min = float(gprmcMess.split(',')[5][3:5:1] + '.' + gprmcMess.split(',')[5][6::1])
							try:
								EW = gprmcMess.split(',')[6][0]
							except IndexError:
								print"\rGPRMC message: IndexError wrong field EW !"
		
							VarDemoTool.Longitude = longit_deg + longit_min/60 
							VarDemoTool.Latitude = latit_deg + latit_min/60 
							#Longitude
							FieldLongitude = str(VarDemoTool.Longitude) + " " + str(EW)
							#Latitude
							FieldLatitude = str(VarDemoTool.Latitude) + " " + str(NS)
						except ValueError:
							print"GPRMC message ValueError !"
							
						try:
							SOG = float(gprmcMess.split(',')[7][0::1])
		#					print"SOG: ", str(SOG) 
						except IndexError:
							print"IndexError: On Speed Over Ground field !"
							SOG=""
						except ValueError:
							SOG=""
		
						#display in the IHM 
						try:
							noteBook.GetPage(indice).GNSS_Infos.FieldLongitude.SetValue(str(int(gprmcMess.split(',')[5][0:3:1]))+" : "+str(gprmcMess.split(',')[5][3:5:1]) + ' : ' + str(float("0"+str(float(gprmcMess.split(',')[5][5::1])*60)))+ " " + str(EW))
							noteBook.GetPage(indice).GNSS_Infos.FieldLatitude.SetValue(str(int(gprmcMess.split(',')[3][0:2:1]))+" : "+str(gprmcMess.split(',')[3][2:4:1]) + ' : ' + str(float("0"+str(float(gprmcMess.split(',')[3][4::1])*60)))+ " " + str(NS))
						except ValueError: 
							noteBook.GetPage(indice).GNSS_Infos.FieldLongitude.SetValue(" ")
							noteBook.GetPage(indice).GNSS_Infos.FieldLatitude.SetValue(" ")
		
						'''Start IExplorer on google maps'''
						if flagIE:
							try:
								os.startfile('http://maps.google.fr/maps?q='+FieldLatitude+'+'+FieldLongitude+'&t=m&z=13&output=embed')
								flagIE = False
							except OSError:
								print "Crash du lancement d'internet explorer"

#		print"=== End processing GPRMC message ==="

#====================================================================================
# processing GPGGA message
#		print "=== processing GPGGA message ==="

			MessageGPGGA = None
			flagFoundGPGGA = False

			if result[res][0:6:1] == "$GPGGA":
				MessageGPGGA = str.replace(result[res],'*',',*',1)
				longMess = len(MessageGPGGA.split(','))
				#print "DEBUG: $GPGGA: " + str(MessageGPGGA.split(','))
				#print "long mess $GPGGA: " + str(len(MessageGPGGA.split(',')))
				flagFoundGPGGA = True

				if flagFoundGPGGA and longMess > 14 :
					#instanciation
					messGPGGA = MessagesGNSS.GPGGA_Class(MessageGPGGA)
					noteBook.GetPage(indice).GNSS_Infos.FieldTimeUTC.SetValue(messGPGGA.get_UTCTIME())
					#try:
					NS = MessageGPGGA.split(',')[3]
					EW = MessageGPGGA.split(',')[5]
		
					try:
						noteBook.GetPage(indice).GNSS_Infos.FieldLongitude.SetValue(str(int(MessageGPGGA.split(',')[4][0:3:1]))+" : "+str(MessageGPGGA.split(',')[4][3:5:1]) + ' : ' + str(float("0"+str(float(MessageGPGGA.split(',')[4][5::1])*60)))+ " " + str(EW))
						noteBook.GetPage(indice).GNSS_Infos.FieldLatitude.SetValue(str(int(MessageGPGGA.split(',')[2][0:2:1]))+" : "+str(MessageGPGGA.split(',')[2][2:4:1]) + ' : ' + str(float("0"+str(float(MessageGPGGA.split(',')[2][4::1])*60)))+ " " + str(NS))
					except ValueError:
						noteBook.GetPage(indice).GNSS_Infos.FieldLongitude.SetValue(" ")
						noteBook.GetPage(indice).GNSS_Infos.FieldLatitude.SetValue(" ")
						#print"Wrong message GPGGA, ValueError Longitude/Latitude field."
					except IndexError:
						noteBook.GetPage(indice).GNSS_Infos.FieldLongitude.SetValue(" ")
						noteBook.GetPage(indice).GNSS_Infos.FieldLatitude.SetValue(" ")
						#print"Wrong message GPGGA, IndexError Longitude/Latitude field."
		
					noteBook.GetPage(indice).GNSS_Alt.FieldAltitude.SetValue(messGPGGA.get_MSLAltitude())
					noteBook.GetPage(indice).GNSS_Alt.FieldHDOP.SetValue(messGPGGA.get_HDOP())
					try:
						noteBook.GetPage(indice).GNSS_Alt.FieldSOG.SetValue(str(float(SOG)*1.852))
					except ValueError:
						noteBook.GetPage(indice).GNSS_Alt.FieldSOG.SetValue("")
						#print"Defective message GPRMC, ValueError S.O.G. field."
					except TypeError:
						noteBook.GetPage(indice).GNSS_Alt.FieldSOG.SetValue("")
					#libération
					messGPGGA = None
		#		print "=== End processing GPGGA message ==="

#======================================================================================
# processing GNGSA message
#
# Two of these messages are output each second, one listing
# the GPS satellites, the other listing the GLONASS satellites.
# use the variable idGNGSA to count these 2 messages: idGNGSA=1 then idGNGSA=2

			if result[res][0:6:1] == "$GNGSA":
					
				messGNGSA = MessagesGNSS.GNGSA_Class(result[res])
				
				if messGNGSA.isValidMsg()==False:
					print"Warning, malformed GNGSA message !"
				elif messGNGSA.isFix()==False:
					nbSatUsed = 0
					List_SAT_USED=[]
					flagFIX = False
				else:
					flagFIX = True
					
					
					if idGNGSA==1: #first message
						List_SAT_USED = messGNGSA.get_SatellitesUsed()
					else: #add message 1 and message 2
						List_SAT_USED = List_SAT_USED + messGNGSA.get_SatellitesUsed()
					
					nbSatUsed = int(len(List_SAT_USED))
					noteBook.GetPage(indice).GNSS_Infos.FieldSatUsed.SetValue(str(nbSatUsed))
					
					if flagFIX == True and flagPast == False:
						TimeToFIX = str(datetime.now() - starttimestamp)[0:10]
						noteBook.GetPage(indice).Enable(True)
						noteBook.GetPage(indice).GNSS_Infos.FieldTTFF.SetValue(TimeToFIX)
						flagPast = True
			
				if idGNGSA>=2:
					idGNGSA=1
				else:
					idGNGSA=2

		#		print "=== End processing GPGSA message ==="

#======================================================================================
# processing GPGSV message AND GLGSV
#		print "=== processing GPGSV message ==="
# GPGSV messages are sent by sequence (several GPGSV) , the item #1 of the message tells how many messages GPGSV will be sent.
# the number of message can be 1,2 or 3
# the item #2 gives the id of the message. item #2 is 1 it means it is the first message of the sequence


			flagGPGSV = False
			flagGLGSV = False
			TotalK = 0

			if result[res][0:6:1] == "$GPGSV":
				flagGPGSV=True
			elif result[res][0:6:1] == "$GLGSV":
				flagGLGSV = True
				
			if flagGPGSV==True or flagGLGSV == True:
				
				try:
					#create an instance of the class messageGNSS
					msgGPGSV = MessagesGNSS.GPGSV_Class(result[res])
					
					#get the id of the message
					mesgID=msgGPGSV.get_MessNb()
					
					#get the total number of satellites in view
					if flagGPGSV==True:
						SatView=SatView-nbGPSSatView #remove the old satellites then add the new ones
						nbGPSSatView=int(msgGPGSV.get_SatellitesInView())
						SatView=SatView+nbGPSSatView 
					else:
						SatView=SatView-nbGLNSatView #remove the old satellites then add the new ones
						nbGLNSatView=int(msgGPGSV.get_SatellitesInView())
						SatView=SatView+nbGLNSatView 
						
					noteBook.GetPage(indice).GNSS_Infos.FieldSatInView.SetValue(str(SatView)) #update the IHM
					
					#get the satellites information in a table: ID,Elevation,Azimuth,SNR
					tabSatData=msgGPGSV.get_SatellitesChanel()
		
					#init the used satellites list
					if mesgID=="1": #this is the 1st message of the GPGSV sequence
						if flagGPGSV==True:
							List_GPS_VIEW=[]
						else:
							List_GLN_VIEW=[]
		
					#if this is the last message of the GPGSV sequence so information can be displayed
					if mesgID==msgGPGSV.get_NbMess(): 
						displayHisto=True
					else:
						displayHisto=False
									
					#add the satellites info to the IHM
					for i in range(len(tabSatData)):
						
						#fielID is used to know where (in which cell) to display the satellite information
						if mesgID=="1": #this is the 1st message of the GPGSV sequence
							fielID = i+1
							if flagGPGSV==True and i==0:
								cleanSNRview(noteBook,indice,0) #this is the 1st sequence so we can clean the cells
							elif i==0:
								cleanSNRview(noteBook,indice,12) #this is the 1st sequence so we can clean the cells
							
						elif mesgID=="2": #this is the 2nd message of the GPGSV sequence, so it means there are already 4 satellites displayed
							fielID = i+1+ 4
						elif mesgID=="3": #this is the 3rd message of the GPGSV sequence, so it means there are already 8 satellites displayed
							fielID = i+1 + 8
						
						#Glonass cells are on the left	
						if flagGLGSV == True:
							fielID = fielID + 12 
						
						
						#Define the displayed color
						if flagGPGSV==True: #GPS sat not used
							FlagColor=wx.Colour(253,192,218) # light pink for sat in view 
						else: #GLONASS sat not used
							FlagColor=wx.Colour(208,222,251)    #"LIGHT BLUE"
								
						for satID in range(len(List_SAT_USED)):
							if List_SAT_USED[satID]==tabSatData[i][0]:
								if flagGPGSV==True:#GPS sat used
									FlagColor = wx.Colour(255,100,80) #dark PINK use a darker color for satellites used
								else:#GLONASS sat used
									FlagColor=wx.Colour(61,146,216) # dark BLUE #use a darker color for satellites used

								
									
						if flagGPGSV==True:
							List_GPS_VIEW.append([]) #add 1 satellite
							List_GPS_VIEW[len(List_GPS_VIEW)-1].append([FlagColor,tabSatData[i][0],tabSatData[i][3]])
						else:
							List_GLN_VIEW.append([]) #add 1 satellite
							List_GLN_VIEW[len(List_GLN_VIEW)-1].append([FlagColor,tabSatData[i][0],tabSatData[i][3]])									
				
						noteBook.GetPage(indice).GNSS_SNR.FindWindowByName("FieldIDSat"+str(fielID)).SetOwnBackgroundColour(FlagColor)
						noteBook.GetPage(indice).GNSS_SNR.FindWindowByName("FieldIDSat"+str(fielID)).SetValue(tabSatData[i][0])
						noteBook.GetPage(indice).GNSS_SNR.FindWindowByName("FieldSnrSat"+str(fielID)).SetOwnBackgroundColour(FlagColor)
						noteBook.GetPage(indice).GNSS_SNR.FindWindowByName("FieldSnrSat"+str(fielID)).SetValue(tabSatData[i][3])
		

				except IndexError:
					print"Index Error MessageGPGSV !"		
					msgGPGSV=None #delete the class
				except ValueError:
					print"Value Error MessageGPGSV !"
					msgGPGSV=None #delete the class
		
		
		#		print "=== End processing GPGSV message ==="

				if displayHisto==True and (len(List_GLN_VIEW)>0 or len(List_GPS_VIEW)>0):
					try:
						DISPLAY_DATA_SAT=[]
						DISPLAY_DATA_SAT=List_GPS_VIEW+List_GLN_VIEW
						#Send the datas to the histo window
						setDataThread = SagStartThread(histo.SetListData,["ld",DISPLAY_DATA_SAT])
					except:
						print"Crash on send datas to graphic window !"
		
					displayHisto = False
					
				noteBook.GetPage(indice).GetParent().GetParent().toolBar.EnableTool(noteBook.GetPage(indice).GetParent().GetParent().ID_stopGNSS, 1)


def GNSS_Stop(noteBook):
	""" stop satellites detection """
	print "Stop satellite detection"
	global flagIE

	if  VarDemoTool.Histo != None:
		VarDemoTool.Histo.OnCloseWindow(0)

#	SagSend(MRM, 'AT&D1\r')
#	SagWaitLine(MRM, ["OK"], C_TIMER_LOW) #20s
#	SagSetDTR(MRM, 0)
#	SagSleep(200)
#	SagSetDTR(MRM, 1)
	if not VarDemoTool.CheckNMEA:
		SagSend(MRM, "+++")
		SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagSend(MRM, "AT+KNMEARCV=0,0\r")
		SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagSend(MRM, "AT+KGNSSRUN=0\r")
		SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagClose(MRM)
	flagIE = True
	print "Stop all thread."

	VarDemoTool.flagStop = False
	noteBook.GetPage(VarDemoTool.indice).GetParent().GetParent().toolBar.EnableTool(noteBook.GetPage(VarDemoTool.indice).GetParent().GetParent().ID_startGNSS, 1)
	noteBook.GetPage(VarDemoTool.indice).GetParent().GetParent().toolBar.EnableTool(noteBook.GetPage(VarDemoTool.indice).GetParent().GetParent().ID_stopGNSS, 0)
	SagStopAllThread(silent=True)


#	print"Fin GNSS_Stop"


def cleanSNRview(noteBook,indice,offset):
	FlagColorWhite=wx.Colour(255,255,255) # light pink for sat in view but don't used
	for i in range(12):
		noteBook.GetPage(indice).GNSS_SNR.FindWindowByName("FieldIDSat"+str(i+1+offset)).SetOwnBackgroundColour(FlagColorWhite)
		noteBook.GetPage(indice).GNSS_SNR.FindWindowByName("FieldIDSat"+str(i+1+offset)).SetValue("")
		noteBook.GetPage(indice).GNSS_SNR.FindWindowByName("FieldSnrSat"+str(i+1+offset)).SetOwnBackgroundColour(FlagColorWhite)
		noteBook.GetPage(indice).GNSS_SNR.FindWindowByName("FieldSnrSat"+str(i+1+offset)).SetValue("")


def MUX_Upload(noteBook):
	print "start FTP Upload in MUX script"
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM)
	
	#AT+CMUX : Open mux 07.10
	SagSend(MRM, "AT+CMUX=0,0,5,64\r\n")
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	# start autotest to listen Mux Frames
	SagMuxStartThreadWait(MRM)
	
	#################
	## Open Channel 0, 1 & 2  ##
	#################
	FTPdlci  = 2
	DATAdlci = 1
	
	SagMuxOpenDLCI(MRM,dlci=0)
	SagMuxOpenDLCI(MRM,dlci=DATAdlci)
	SagMuxOpenDLCI(MRM,dlci=FTPdlci)
	
	##################
	## Start Send AT Commands ##
	##################
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='ATE\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n")
# corriger les instructions avec: DecodedFrames = SagMuxWaitAndDecodeData(MRM, data="OK\r\n", dlci=FTPdlci)
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT&K3\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n")
	SagSetFlowControl(MRM,False)
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+KCNXTIMER=0,60,2,70\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n")
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+KCNXPROFILE=0\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n")
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+CGATT=1\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n")
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+KCNXCFG=0,"GPRS","' + str(VarDemoTool.GPRS_APN) + '","' + str(VarDemoTool.GPRS_Login) + '","' + str(VarDemoTool.GPRS_Password) + '"\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n")
	
	SagSleep(1000,silent=True)
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+KFTPCFG=0,"' + str(VarDemoTool.FTP_URL) + '","' + str(VarDemoTool.FTP_Login) + '","' + str(VarDemoTool.FTP_Password) + '",' + str(VarDemoTool.FTP_Port) + ',0\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n")
	
	SagSleep(1000,silent=True)
	file = str(VarDemoTool.FTP_UplaodFile)
	fileName= file.rsplit('\\',1)[1]
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+KFTPSND=0,,"'+str(VarDemoTool.FTP_UplaodPath)+'","'+fileName+'"\r')
	DecodedFrames = SagMuxWaitAndDecodeData("CONNECT\r\n",timeout = 30000)
	SagSleep(3000,silent=True)
	SagSendFileInMuxMode(MRM, dlci=FTPdlci, FileName=file, EOF="--EOF--Pattern--")
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n",timeout = 10000)
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+KFTPCLOSE=0\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n")

	###########
	## Close MUX  ##
	###########
	VarGlobal.myColor = VarGlobal.colorLsit[2] 
	print "\r\nClose Mux Control Channel\r\nUIH"
	VarGlobal.myColor = VarGlobal.colorLsit[8]
	SagMuxSend(MRM, UIH, dlci=0, data=[0xC3,0x01])
	DecodedFrames = SagMuxWaitAndDecodeData([0xC1,0x01], C_TIMER_LOW)

	VarGlobal.myColor = VarGlobal.colorLsit[2]
	print "\r\nClose Mux Control Channel\r\nDISC"
	VarGlobal.myColor = VarGlobal.colorLsit[8]
	SagMuxSend(MRM, DISC, dlci=0)

	SagMuxStopThreadWait()

	SagClose(MRM)

def MUX_Download(noteBook):
	print "start FTP Download in MUX script"
	# Open Com port
	
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	#Init(MRM)
	
	# ouverture du mux 07.10
	#AT+CMUX
	SagSend(MRM, "AT+CMUX=0,0,5,64\r\n")
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	# start autotest to listen Mux Frames
	SagMuxStartThreadWait(MRM)
	
	#################
	## Open Channel 0, 1 & 2  ##
	#################
	FTPdlci  = 63
	DATAdlci = 1
	
	SagMuxOpenDLCI(MRM,dlci=0)
	SagMuxOpenDLCI(MRM,dlci=DATAdlci)
	SagMuxOpenDLCI(MRM,dlci=FTPdlci)
	##################
	## Start Send AT Command ##
	##################
	
	FTP_Thread = SagStartThread(MUXDownloadFTP,[MRM,FTPdlci])
	KCELL_Thread = SagStartThread(MUXKCELL,[MRM,DATAdlci])
	
	SagWaitEndOfThread(FTP_Thread,None)
	print "ok"
	SagStopThread(KCELL_Thread)
	print "ok2"
	
	###########
	## Close MUX ##
	###########
	VarGlobal.myColor = VarGlobal.colorLsit[2] 
	print "\r\nMux Control Channel\r\nUIH"
	VarGlobal.myColor = VarGlobal.colorLsit[8]
	SagMuxSend(MRM, UIH, dlci=0, data=[0xC3,0x01])
	DecodedFrames = SagMuxWaitAndDecodeData(data2string([0xC1,0x01]), dlci=0,timeout = C_TIMER_LOW)

	VarGlobal.myColor = VarGlobal.colorLsit[2]
	print "\r\nMux Control Channel\r\nDISC"
	VarGlobal.myColor = VarGlobal.colorLsit[8]
	SagMuxSend(MRM, DISC, dlci=0)

	SagMuxStopThreadWait()

	SagClose(MRM)

def MUXDownloadFTP(MRM,FTPdlci):
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='ATE1\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n",dlci=FTPdlci)
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT&K3\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n",dlci=FTPdlci)
	SagSetFlowControl(MRM,True)
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+KCNXTIMER=0,60,2,70\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n",dlci=FTPdlci)
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+KCNXPROFILE=0\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n",dlci=FTPdlci)
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+CGATT=1\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n",dlci=FTPdlci)
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+KCNXCFG=0,"GPRS","' + str(VarDemoTool.GPRS_APN) + '","' + str(VarDemoTool.GPRS_Login) + '","' + str(VarDemoTool.GPRS_Password) + '"\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n",dlci=FTPdlci)
	
	SagSleep(500,silent=True)
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+KFTPCFG=0,"' + str(VarDemoTool.FTP_URL) + '","' + str(VarDemoTool.FTP_Login) + '","' + str(VarDemoTool.FTP_Password) + '",' + str(VarDemoTool.FTP_Port) + ',0\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n",dlci=FTPdlci)
	SagSleep(500,silent=True)
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+KFTPRCV=' + '0' + ',,"' + str(VarDemoTool.FTP_DownlaodPath) + '","' + str(VarDemoTool.FTP_DownlaodFile) + '",0\r')
	DecodedFrames = SagMuxWaitAndDecodeData("CONNECT\r\n",timeout = 10000,dlci=FTPdlci)
	resultat = SagMuxWaitData(dlci=FTPdlci,EOF="--EOF--Pattern--\r\n\r\nOK\r\n",timeout = 10000)
	
	SagMuxSend(MRM, UIH, dlci=FTPdlci, data='AT+KFTPCLOSE=0\r')
	DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n",dlci=FTPdlci)

def MUXKCELL(MRM,dlci):
	while True:
		SagMuxSend(MRM, UIH, dlci=dlci, data='AT+COPS?\r')
		DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n",dlci=dlci,timeout=C_TIMER_LOW)
		SagSleep(2000,silent=True)
		SagMuxSend(MRM, UIH, dlci=dlci, data='AT+CSQ\r')
		DecodedFrames = SagMuxWaitAndDecodeData("OK\r\n",dlci=dlci,timeout=C_TIMER_LOW)
		SagSleep(2000,silent=True)

def GPIO_Input(noteBook):
	print "start GPIO input script"
	
	for i in range(noteBook.GetPageCount()):
		if noteBook.GetPage(i).GetName() == "GPIO":
			noteBook.GetPage(i).GPIO.GPIO1.SetValue(False)
			noteBook.GetPage(i).GPIO.GPIO2.SetValue(False)
			noteBook.GetPage(i).GPIO.GPIO3.SetValue(False)
			if VarDemoTool.moduleType.type!=VarDemoTool.ModuleType_HILO3G: #there are only 3 GPIO on Hilo3G
				noteBook.GetPage(i).GPIO.GPIO4.SetValue(False)
				noteBook.GetPage(i).GPIO.GPIO5.SetValue(False)
			break
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM,GSM=False,GPRS=False)
	
	for i in range(5):
		if i>2 and VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3G: #there are only 3 GPIO on Hilo3G
			break
		
		SagSend(MRM, "AT+KGPIOCFG="+str(i+1)+",1,0\r")
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])
	
	SagClose(MRM)

def GPIO_Output(noteBook):
	print "start GPIO output script"
	
	for i in range(noteBook.GetPageCount()):
		if noteBook.GetPage(i).GetName() == "GPIO":
			noteBook.GetPage(i).GPIO.GPIO1.SetValue(False)
			noteBook.GetPage(i).GPIO.GPIO2.SetValue(False)
			noteBook.GetPage(i).GPIO.GPIO3.SetValue(False)
			if VarDemoTool.moduleType.type!=VarDemoTool.ModuleType_HILO3G: #there are only 3 GPIO on Hilo3G
				noteBook.GetPage(i).GPIO.GPIO4.SetValue(False)
				noteBook.GetPage(i).GPIO.GPIO5.SetValue(False)
			break
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM,GSM=False,GPRS=False)
	
	for i in range(5):
		if i>2 and VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3G: #there are only 3 GPIO on Hilo3G
			break
		SagSend(MRM, "AT+KGPIOCFG="+str(i+1)+",0,2\r")
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])
		
		SagSend(MRM, "AT+KGPIO="+str(i+1)+",0\r")
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])

	SagClose(MRM)

def GPIO_GPIO(noteBook):

	if int(VarDemoTool.GPIO_Number)>3 and VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3G: #there are only 3 GPIO on Hilo3G
		print "There are only 3 GPIO on HILO3G"
	else:
		print "start set GPIO script"
		# Open Com port
		MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
		SagSend(MRM, "AT+KGPIO="+str(VarDemoTool.GPIO_Number)+","+VarDemoTool.GPIO_Value+"\r")
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])
		
		SagClose(MRM)

def GPIO_Read(noteBook):
	print "start set GPIO script"
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	GPIO_Value = [0,0,0,0,0]
	
	for i in range(5):
		if i>2 and VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3G: #there are only 3 GPIO on Hilo3G
			SagSend(MRM, "AT+KGPIO="+str(i+1)+",2\r")
			resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
			result = SagTestCmd(resultat.tabLines, ["OK"])
		
			if result == 0:
				GPIO_Value[i] = (int(resultat.tabLines[1][0].split("+KGPIO: "+str(i+1)+",")[1][:-2]))
	
	for i in range(noteBook.GetPageCount()):
		if noteBook.GetPage(i).GetName() == "GPIO":
			noteBook.GetPage(i).GPIO.GPIO1.SetValue(GPIO_Value[0])
			noteBook.GetPage(i).GPIO.GPIO2.SetValue(GPIO_Value[1])
			noteBook.GetPage(i).GPIO.GPIO3.SetValue(GPIO_Value[2])
			if VarDemoTool.moduleType.type!=VarDemoTool.ModuleType_HILO3G: #there are only 3 GPIO on Hilo3G
				noteBook.GetPage(i).GPIO.GPIO4.SetValue(GPIO_Value[3])
				noteBook.GetPage(i).GPIO.GPIO5.SetValue(GPIO_Value[4])
			break
	
	SagClose(MRM)

def File_System_Write_File(noteBook):
	print "start File System write script"
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM,GSM=False,GPRS=False)
	
	SagSend(MRM, 'AT&K3\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_HIGH)
	SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSetFlowControl(MRM,True)
	
	FileLen = str(len(SagReadFile(VarDemoTool.FS_WriteFile,silent=True)))
	
	SagSend(MRM, 'AT+KFSFILE=0,"/data/'+VarDemoTool.FS_WriteName+'",'+FileLen+'\r')
	resultat = SagWaitLine(MRM, ["CONNECT"], C_TIMER_HIGH)
	SagTestCmd(resultat.tabLines, ["CONNECT"])
	
	SagSendFile(MRM, VarDemoTool.FS_WriteFile, silent=True)
	
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	SagTestCmd(resultat.tabLines, ["OK"])
	
	SagClose(MRM)

def File_System_Read_File(noteBook):
	print "start File System read script"
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM,GSM=False,GPRS=False)
	
	SagSend(MRM, 'AT&K3\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_HIGH)
	SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSetFlowControl(MRM,True)
	print "\r"
	
	# List all the files in data directory
	SagSend(MRM, 'AT+KFSFILE=4,"/data/"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_HIGH)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	#look for the index containing the file name to retrieve the size
	fileSize=""
	if result==0:
		for i in range(len(resultat.tabLines)):
			strPosition=resultat.tabLines[i][0].find(VarDemoTool.FS_ReadName)
			if strPosition!=-1:
				#the answer uses this pattern: "filenanme size\r" we just need the size
				fileSize=resultat.tabLines[i][0][strPosition+len(VarDemoTool.FS_ReadName)+1:len(resultat.tabLines[i][0])]
				fileSize=fileSize.replace('\r','').replace('\n','') #remove the end of line chars
				break
	
	if fileSize!="":
		SagSend(MRM, 'AT+KFSFILE=1,"/data/'+VarDemoTool.FS_ReadName+'",'+fileSize+'\r')
		if not(os.path.isdir("DATA")):
			os.mkdir("DATA")
		if not(os.path.isdir("DATA\\File System")):
			os.mkdir("DATA\\File System")
		SagWaitTextFile(MRM,"DATA\\File System\\"+str(datetime.now()).split(".")[0].replace(":","h",1).replace(":","m").replace(" ","_") + "_" + VarDemoTool.FS_ReadName, EOF = "OK", SOF = "CONNECT\r\n", silent = True)
	else:
		SafePrint(None,	None, "The file " +VarDemoTool.FS_ReadName+" does not exist",color = 4)
	
	SagClose(MRM)

def File_System_Clear_all_files(noteBook):
	print "start File System delete all file script"
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM,GSM=False,GPRS=False)
	
	SagSend(MRM, 'AT+KFSFILE=4,"/data/"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	if result == 0:
		files = []
		for elem in resultat.tabLines:
			if elem[0].startswith("+KFSFILE: <F> "):
				files.append(elem[0].split("+KFSFILE: <F> ")[1].split()[0])
		
		for elem in files:
			SagSend(MRM, 'AT+KFSFILE=2,"/data/'+str(elem)+'"\r')
			resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
			result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagClose(MRM)

def SMTP_Send(noteBook):
	
	print "start SMTP script"
	
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM)

	#SMTP not supported on Hilo3G and Hilo3GPS	
	if VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3G or VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3GPS:
		print "Sorry HILO3G and HILO3GPS do not support SMTP"
	else:
		SagSend(MRM, "AT&K3\r\n")
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_MEDIUM)
		SagTestCmd(resultat.tabLines, ["OK"])
		SagSetFlowControl(MRM,True)
		
		SagSend(MRM, 'AT+KCNXCFG=0,"GPRS","' + VarDemoTool.GPRS_APN + '","' + VarDemoTool.GPRS_Login + '","' + VarDemoTool.GPRS_Password + '"\r')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])
		
		SagSend(MRM, 'AT+KCNXTIMER=0,60,4,70\r\n')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])
		
		SagSend(MRM, "AT+KCNXPROFILE=0\r\n")
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])
		
		SagSend(MRM, 'AT+KSMTPPARAM="'+VarDemoTool.SMTP_Server+'", 25, "'+VarDemoTool.SMTP_Email+'"\r\n')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])
		
		SagSend(MRM, 'AT+KSMTPPWD="'+VarDemoTool.SMTP_Login+'","'+VarDemoTool.SMTP_PassWord+'"\r\n')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])
		
		SagSend(MRM, 'AT+KSMTPTO="'+VarDemoTool.SMTP_To+'","","",""\r\n')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])
		
		SagSend(MRM, 'AT+KSMTPSUBJECT="'+VarDemoTool.SMTP_Subject+'"\r\n')
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])
		
		SagSend(MRM, 'AT+KSMTPUL=1,'+str(len(VarDemoTool.SMTP_Text))+'\r\n')
		resultat = SagWaitLine(MRM, ["CONNECT"], C_TIMER_MEDIUM)
		SagTestCmd(resultat.tabLines, ["CONNECT"])
		
		SagSend(MRM, VarDemoTool.SMTP_Text)
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		SagTestCmd(resultat.tabLines, ["OK"])
		
	SagClose(MRM)

def Environment_Read(noteBook):
	print "start Environment Read script"
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM,GPRS=False)
	
	SagSend(MRM, 'AT+CGSN\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		VarDemoTool.IMEI = resultat.tabLines[1][0].replace("\r","").replace("\n","")
	
	SagSend(MRM, 'AT+CGMR\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		VarDemoTool.Soft_Version = resultat.tabLines[1][0].replace("\r","").replace("\n","")
	
	SagSend(MRM, 'AT+CIMI\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		VarDemoTool.IMSI = resultat.tabLines[1][0].replace("\r","").replace("\n","")
		VarDemoTool.IMSI = VarDemoTool.IMSI.replace("<IMSI>:","")#remove the first part <IMSI>: 
		VarDemoTool.HPLMN = VarDemoTool.IMSI[1]+VarDemoTool.IMSI[0]+"F"+VarDemoTool.IMSI[2]+VarDemoTool.IMSI[4]+VarDemoTool.IMSI[3]
	
	SagSend(MRM, 'AT+CRSM=176,28539,0,0,12\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		FPLMN = resultat.tabLines[1][0].split('"')[1]
		VarDemoTool.FPLMN = [FPLMN[:6],FPLMN[6:12],FPLMN[12:18],FPLMN[18:24]]
		for i in range(len(VarDemoTool.FPLMN)):
			if VarDemoTool.FPLMN[i] == "FFFFFF":
				VarDemoTool.FPLMN[i]=""
	
	SagSend(MRM, 'AT+CRSM=176,28464,0,0,24\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		PPLMN = resultat.tabLines[1][0].split('"')[1]
		VarDemoTool.PPLMN = [PPLMN[:6],PPLMN[6:12],PPLMN[12:18],PPLMN[18:24],PPLMN[24:30],PPLMN[30:36],PPLMN[36:42],PPLMN[42:48]]
		for i in range(len(VarDemoTool.PPLMN)):
			if VarDemoTool.PPLMN[i] == "FFFFFF":
				VarDemoTool.PPLMN[i]=""
	
	SagSend(MRM, 'AT+CRSM=176,12258,0,0,10\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		VarDemoTool.ICCIdentification = resultat.tabLines[1][0].split('"')[1]
	
	SagSend(MRM, 'AT+COPS?\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		VarDemoTool.OperatorName = resultat.tabLines[1][0].split('"')[1]
	
	SagSend(MRM, 'AT+CREG?\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		VarDemoTool.Roaming = resultat.tabLines[1][0].split(',')[1].replace("\r","").replace("\n","") == "5"
	
	SagSend(MRM, 'AT+CSQ\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		VarDemoTool.SignalLevel = str(-110 + int(resultat.tabLines[1][0].split(': ')[1].split(",")[0])*2)+'dbm'
	
	SagSend(MRM, 'AT+KBND?\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		# for Hilo3G and Hilo3GPS the answer is : +KBND: <bnd>,<channel>
		# for Hilo2G the answer is +KBND: <bnd>
		value=resultat.tabLines[1][0].replace("+KBND: ","") #remove "+KBND: "
		value = int(value.split(",")[0]) #use the first paremeter
		
		if VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3G or VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3GPS:
			if value==200:
				VarDemoTool.PowerBand = "GSM 850 MHz"
			elif value==400:
				VarDemoTool.PowerBand = "GSM 900 MHz"
			elif value==800:
				VarDemoTool.PowerBand = "GSM 1800 MHz"
			elif value==1000:
				VarDemoTool.PowerBand = "GSM 1900 MHz"
			elif value==1:
				VarDemoTool.PowerBand = "PCS (1900MHz band2)"
			elif value==2:
				VarDemoTool.PowerBand = "CELL (800MHz band 5)"
			elif value==4:
				VarDemoTool.PowerBand = "IMT2K (2100MHz band1)"
			elif value==8:
				VarDemoTool.PowerBand = "WCDMA 800 MHz"
			elif value==10:
				VarDemoTool.PowerBand = "WCDMA 850 MHz"
			elif value==20:
				VarDemoTool.PowerBand = "WCDMA 1800 MHz"
			elif value==40:
				VarDemoTool.PowerBand = "WCDMA 900 MHz"
			else:
				VarDemoTool.PowerBand = "Not available"
		else:
			if value==1:
				VarDemoTool.PowerBand = "850 MHz"
			elif value==2:
				VarDemoTool.PowerBand = "900 MHz"
			elif value==4:
				VarDemoTool.PowerBand = "1800 MHz"
			elif value==8:
				VarDemoTool.PowerBand = "1900 MHz"
			else:
				VarDemoTool.PowerBand = "Not available"
	
	SagSend(MRM, 'AT+KCELL=0\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	VarDemoTool.KCELL=[]
	if result == 0:
		elem = resultat.tabLines[1][0].upper().split(': ')[1].split("\r")[0].split(",")
		VarDemoTool.NbCell = elem[0]
		VarDemoTool.KCELL.append(['1']+elem[1:8])
		for i in range(8,len(elem),6):
			VarDemoTool.KCELL.append([str(((i-8)/6)+2)]+elem[i:i+6])
	
	for i in range(noteBook.GetPageCount()):
		if noteBook.GetPage(i).GetName() == "Environment":
			noteBook.GetPage(i).Environment_Module.IMEI.SetValue(VarDemoTool.IMEI)
			noteBook.GetPage(i).Environment_Module.SoftVersion.SetValue(VarDemoTool.Soft_Version)
			noteBook.GetPage(i).Environment_RF.OPName.SetValue(VarDemoTool.OperatorName)
			noteBook.GetPage(i).Environment_RF.Roaming.SetValue(VarDemoTool.Roaming)
			noteBook.GetPage(i).Environment_RF.FieldLvl.SetValue(VarDemoTool.SignalLevel)
			noteBook.GetPage(i).Environment_RF.PowerBand.SetValue(VarDemoTool.PowerBand)
			noteBook.GetPage(i).Environment_RF.KCELL.AddItem(VarDemoTool.KCELL)
			noteBook.GetPage(i).Environment_SIM.IMSI.SetValue(VarDemoTool.IMSI)
			noteBook.GetPage(i).Environment_SIM.HPLMN.SetValue(VarDemoTool.HPLMN)
			noteBook.GetPage(i).Environment_SIM.FPLMN1.SetValue(VarDemoTool.FPLMN[0])
			noteBook.GetPage(i).Environment_SIM.FPLMN2.SetValue(VarDemoTool.FPLMN[1])
			noteBook.GetPage(i).Environment_SIM.FPLMN3.SetValue(VarDemoTool.FPLMN[2])
			noteBook.GetPage(i).Environment_SIM.FPLMN4.SetValue(VarDemoTool.FPLMN[3])
			noteBook.GetPage(i).Environment_SIM.PPLMN1.SetValue(VarDemoTool.PPLMN[0])
			noteBook.GetPage(i).Environment_SIM.PPLMN2.SetValue(VarDemoTool.PPLMN[1])
			noteBook.GetPage(i).Environment_SIM.PPLMN3.SetValue(VarDemoTool.PPLMN[2])
			noteBook.GetPage(i).Environment_SIM.PPLMN4.SetValue(VarDemoTool.PPLMN[3])
			noteBook.GetPage(i).Environment_SIM.PPLMN5.SetValue(VarDemoTool.PPLMN[4])
			noteBook.GetPage(i).Environment_SIM.PPLMN6.SetValue(VarDemoTool.PPLMN[5])
			noteBook.GetPage(i).Environment_SIM.PPLMN7.SetValue(VarDemoTool.PPLMN[6])
			noteBook.GetPage(i).Environment_SIM.PPLMN8.SetValue(VarDemoTool.PPLMN[7])
			noteBook.GetPage(i).Environment_SIM.Update_PLMN_ToolTip()
			noteBook.GetPage(i).Environment_SIM.ICCIdentification.SetValue(VarDemoTool.ICCIdentification)
			break
	
def Environment_2_Read(noteBook):
	print "start Environment Read script"
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM,GPRS=False)
	
	SagSend(MRM, 'AT+CPBS="SM"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	SagTestCmd(resultat.tabLines, ["OK"])
	
	VarDemoTool.PhoneBook = []
	SagSend(MRM, 'AT+CPBS?\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	if result == 0:
		MaxPhone = resultat.tabLines[1][0].split(',')[2].replace("\r","").replace("\n","")
		NbPhone = resultat.tabLines[1][0].split(',')[1].replace("\r","").replace("\n","")
		
		if int(NbPhone)>0:
			SagSend(MRM, 'AT+CPBR=1,'+MaxPhone+'\r')
			resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
			result = SagTestCmd(resultat.tabLines, ["OK"])
			
			if result == 0:
				for elem in resultat.tabLines[:-1]:
					elem = elem[0].replace("\r","").replace("\n","").replace('"','')
					if elem != "":
						split = elem.split(": ")[1].split(",")
						VarDemoTool.PhoneBook.append([split[0], split[3],split[1]])
	
	SagSend(MRM, 'AT+CPMS="SM","SM","SM"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, 'AT+CMGF=1\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	SagSend(MRM, 'AT+CMGL="ALL"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_HIGH)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	VarDemoTool.SMSOnSIM = []
	textData = ""
	if result == 0 and len(resultat.tabLines)>2:
		text  = False
		data = ""
		for elem in resultat.tabLines[1:-1]:
			elem = elem[0]
			if elem.startswith("+CMGL"):
				if text:
					VarDemoTool.SMSOnSIM.append(data + [textData.rsplit("\r\n",1)[0]])
					textData = ""
					text = False
				
				split = elem.split(": ")[1].replace("\r","").replace("\n","").replace('"','').split(",")

				for i in range(1,7-len(split)):#data has to be 6 of length
					split += [""]
				data = [split[0], split[1],split[2],split[3],split[4],split[5]]
				text = True
			else:
				if text:
					textData += elem
		VarDemoTool.SMSOnSIM.append(data + [textData.rsplit("\r\n",1)[0]])
	
	for i in range(noteBook.GetPageCount()):
		if noteBook.GetPage(i).GetName() == "Environment_2":
			noteBook.GetPage(i).Environment_PhoneBook.PhoneBook.AddItem(VarDemoTool.PhoneBook)
			noteBook.GetPage(i).Environment_SMS.SMS.AddItem(VarDemoTool.SMSOnSIM)
			break
	

def Environment_2_Alarm(noteBook):
	print "start Environment Alarm script"
	# Open Com port
	MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
	
	Init(MRM,GPRS=False)
	
	import datetime
	actualTime = datetime.datetime.now()
	stringTime = str(actualTime)[2:].replace("-","/").replace(" ",",").split(".")[0]
	
	SagSend(MRM, 'AT+CCLK="'+stringTime+'+01"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	
	alarmTime = actualTime + datetime.timedelta(hours=VarDemoTool.Alarm[0],minutes=VarDemoTool.Alarm[1],seconds=VarDemoTool.Alarm[2])
	alarmTimeString = str(alarmTime)[2:].replace("-","/").replace(" ",",").split(".")[0]
	
	SagSend(MRM, 'AT+CALA="' + alarmTimeString + '"\r')
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"], result)
	
	if VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3G or VarDemoTool.moduleType.type==VarDemoTool.ModuleType_HILO3GPS:
		SagSend(MRM, 'AT+CPOF\r')
	else:
		SagSend(MRM, 'AT*PSCPOF\r')
		
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"], result)
	
	SagSleep((VarDemoTool.Alarm[0]*60*60+VarDemoTool.Alarm[1]*60+VarDemoTool.Alarm[2])*1000-30000, silent=True)
	resultat = SagWaitLine(MRM, ["+CALV: "], C_TIMER_HIGH)
	result = SagTestCmd(resultat.tabLines, ["+CALV: "], result)
	if result !=0:
		print "--> !! Alarm notification was not received!"
	else:
		for i in range(len(resultat.tabLines)): #look for the index containing +CALV 
			if resultat.tabLines[i][0].startswith("+CALV: "):
				break
					
	alarm = resultat.tabLines[i][0].replace("+CALV: ","").replace("\r","").replace("\n","") #remove the /r/n
	
	SagSleep(2500, silent=True)
	SagSend(MRM, "AT+CALD="+alarm+"\r")
	resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
	result = SagTestCmd(resultat.tabLines, ["OK"], result)

class AT_Terminal(Thread):
	def __init__(self, noteBook, AT_TerminalPage):
		MainFrame = noteBook.GetParent()
		if MainFrame.log_flag:
			sys.stdout = GuiLogOutput(MainFrame.log_tc, MainFrame.log_file)
		else:
			sys.stdout = GuiOutput(MainFrame.log_tc)
		sys.stderr = sys.stdout
		print "start AT Terminal script"
		Thread.__init__(self)
		self.noteBook = noteBook
		self.AT_TerminalPage = AT_TerminalPage
		self.OnRun = False
		self.start()
	
	def run(self):
		OnError = False
		try:
			self.noteBook.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGING, self.__PageChange)
			self.noteBook.Enable(True)
			
			self.OnRun = True
			RTS = self.AT_TerminalPage.FindWindowByName("RTS").GetValue()
			DTR = self.AT_TerminalPage.FindWindowByName("DTR").GetValue()
			FlowControl = self.AT_TerminalPage.AT_Terminal.FlowControlListBox.GetCurrentSelection()
			# Open Com port
			self.MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed), timeout=1, DTR=DTR, RTS=RTS, rtscts=FlowControl==1, xonxoff=FlowControl==2)
			
			self.AT_TerminalPage.Bind(wx.EVT_CHECKBOX, self.__OnSelect)																# When Clic on checkbox
			self.AT_TerminalPage.Bind(wx.EVT_BUTTON, self.__OnSendRaw, 	self.AT_TerminalPage.AT_Terminal.SendRawButton)				# When Clic on send raw file Button
			self.AT_TerminalPage.Bind(wx.EVT_TEXT_ENTER, self.__OnSendLine, self.AT_TerminalPage.AT_Terminal.AT_Command)			# When press enter on combobox
			self.AT_TerminalPage.Bind(wx.EVT_BUTTON, self.__OnSendLine, self.AT_TerminalPage.AT_Terminal.SendLineButton)			# When Clic on send line Button
			self.AT_TerminalPage.Bind(wx.EVT_BUTTON, self.__OnSend, 	self.AT_TerminalPage.AT_Terminal.SendButton)				# When Clic on send	Button
			self.AT_TerminalPage.Bind(wx.EVT_CHOICE, self.__OnListSelect)															# When Clic on a list
			self.ReadStatus()
			
			WatchInSignal_Thread = SagStartThread(self.WatchInSignals)
		except SystemExit:
			OnError = True
		except COM_exception:
			OnError = True
		except stop_exception:
			OnError = True
		except:
			OnError = True
			raise
		finally:
			if OnError:
				self.AT_TerminalPage.AT_Terminal.Enable(False)
				SagStopAllPort()
				SagStopAllThread(silent=True)
				try:
					SagClose(self.MRM)
				except:
					pass
				SagCloseAll(silent=True)
				self.OnRun = False
	
	def stop(self):
		self.AT_TerminalPage.AT_Terminal.Enable(False)
		SagStopAllThread(silent=True)
		SagStopAllPort()
		try:
			SagClose(self.MRM)
		except:
			pass
		SagCloseAll(silent=True)
		self.OnRun = False
		super(AT_Terminal, self).stop()
	
	def WatchInSignals(self):
		try:
			import serial
			recv = False
			recv,mask = self.MRM.waitInSignal(0)
			while True:
				if recv:
					if mask&0x10==0x10:
						# tempo pour avoir plus de donnee dans le buffer
						time.sleep(0.001)
						serialBuffer = self.MRM.read(self.MRM.inWaiting())
						VarGlobal.myColor = VarGlobal.colorLsit[7]
						sys.stdout.write(serialBuffer.replace("\n",""))
						VarGlobal.myColor = VarGlobal.colorLsit[8]
					if mask&0xF>0:
						self.ReadStatus(mask)
				recv,mask = self.MRM.waitInSignal(0,False)
		except:
			raise
	
	def ReadStatus(self, mask=0xF):
		status = self.MRM.getComStatus()
		
		MS_CTS_ON  = 16
		MS_DSR_ON  = 32
		MS_RING_ON = 64
		MS_RLSD_ON = 128
		
		if mask & 1 == 1:
			self.AT_TerminalPage.FindWindowByLabel("CTS").SetValue(status&MS_CTS_ON)
		if mask & 2 == 2:
			self.AT_TerminalPage.FindWindowByLabel("DSR").SetValue(status&MS_DSR_ON)
		if mask & 4 == 4:
			self.AT_TerminalPage.FindWindowByLabel("RING/RI").SetValue(status&MS_RING_ON)
		if mask & 8 == 8:
			self.AT_TerminalPage.FindWindowByLabel("RLSD/DCD").SetValue(status&MS_RLSD_ON)
	
	def __OnSendRaw(self,evt):
		FileName = self.AT_TerminalPage.AT_Terminal.RawFile.GetValue()
		file = open(FileName, 'rb')
		tab = file.read()
		file.close()
		self.MRM.write(tab)
	
	def __OnSendLine(self,evt):
		AT_Command = self.AT_TerminalPage.FindWindowByName("AT_Command").GetValue()
		self.MRM.write(str(AT_Command)+"\r")
	
	def __OnSend(self,evt):
		AT_Command = self.AT_TerminalPage.FindWindowByName("AT_Command").GetValue()
		self.MRM.write(str(AT_Command))
	
	def __OnSelect(self,evt):
		try:
			signal = self.AT_TerminalPage.FindWindowById(evt.GetId())
			if signal.GetName() == "RTS":
				self.MRM.setRTS(signal.GetValue())
			if signal.GetName() == "DTR":
				self.MRM.setDTR(signal.GetValue())
			if signal.GetName() == "BREAK":
				self.MRM.setBreak(signal.GetValue())
		except:
			print "error"
			raise
	
	def __PageChange(self,evt):
		if self.OnRun:
			evt.Veto()
		else:
			evt.Skip()
	
	def __OnListSelect(self, evt):
		listBox = self.AT_TerminalPage.FindWindowById(evt.GetId())
		if self.AT_TerminalPage.AT_Terminal.OpenButton.GetLabel() == "Close":
			if listBox.GetName() == "speed":
				SagSetBaudrate(self.MRM,int(VarDemoTool.SpeedList[listBox.GetCurrentSelection()]))
			elif listBox.GetName() == "flow control":
				flowControl=["None","Hardware","Software"]
				SafePrint(None, self.MRM, "SET Flow Control: %s"%(flowControl[listBox.GetCurrentSelection()]),color = 6)
				select = listBox.GetCurrentSelection()
				self.MRM.setRtsCts(select==1)
				self.MRM.setXonXoff(select==2)
	
def PDU_SEND(noteBook):
	print "start PDU SMS send script"
	
	file = open(VarDemoTool.PDU_File, 'rb')
	tab = file.read()
	file.close()
	PDU = tab.split(";")
	
	PDU_Len=[]
	for elem in PDU:
		size = len(elem)/2-1
		if size>160:
			dlg = wx.MessageDialog(None, "The PDU len is too long (it may be not a PDU)","PDU size" ,wx.ICON_ERROR)
			dlg.ShowModal()
			break
		else:
			PDU_Len.append(size)
	
	
	if len(PDU_Len) == len(PDU):
		
		# Open Com port
		MRM = SagOpen(int(VarDemoTool.COM_Port), int(VarDemoTool.COM_Speed))
		
		Init(MRM,GPRS=False)
		
		SagSend(MRM, "AT+CMGF=0\r")
		resultat = SagWaitLine(MRM, ["OK"], C_TIMER_LOW)
		result = SagTestCmd(resultat.tabLines, ["OK"])
		
		for i in range(len(PDU)):
		
			SagSend(MRM, 'AT+CMGS=' + str(PDU_Len[i]) + '\r')
			resultat = SagWaitLine(MRM, ["> "], C_TIMER_LOW)
			if resultat.tabLines[1][0]!="> ":
				VarGlobal.statOfItem = 'NOK'		
				VarGlobal.numOfFailedResponse += 1.0
				result=1
				print '!!! Failed, expected response was : "> "'
			else:
				SagSend(MRM, str(PDU[i]) + chr(26))
				resultat = SagWaitLine(MRM, ["OK"], C_TIMER_MEDIUM)
				result = SagTestCmd(resultat.tabLines, ["+CMGS", "OK"])
				
				if result != 0:
					SagSend(MRM, chr(27))
		
		SagClose(MRM)
	
def Error(object):
	print "Error script unknown"

# List of script name
functions  = {"FTP_Upload": FTP_Upload,"FTP_Download":FTP_Download,"TCP_REQUEST":TCP_REQUEST,"SMS_Send":SMS_SEND,"SMS_Wait Incomming SMS":SMS_Wait_Incomming_SMS,
			  "Voice Call_Call":Voice_Call_Call,"MUX_Upload":MUX_Upload,"MUX_Download":MUX_Download,"GPIO_Input":GPIO_Input,"GPIO_Output":GPIO_Output,
			  "GPIO_GPIO":GPIO_GPIO,"GPIO_Read":GPIO_Read,"File System_Write File":File_System_Write_File,"File System_Read File":File_System_Read_File,
			  "File System_Clear all files":File_System_Clear_all_files,"SMTP_Send":SMTP_Send,"Environment_Read":Environment_Read,
			  "Environment_2_Read":Environment_2_Read,"Environment_2_Alarm":Environment_2_Alarm,"PDU_Send":PDU_SEND,"GNSS_Start":GNSS_Start,"GNSS_Stop":GNSS_Stop,
			  "eCall_Start":eCall_Start,"eCall_Stop":eCall_Stop}

if __name__ == '__main__':
	'''import traceback
	try:
		pass
		#start("FTP")
	except:
		traceback.print_exc (file=open('error.txt', 'w'))
	'''
	# start autotest
	import os,sys
	sys.path.append(os.getcwd().rsplit("\\",1)[0])
	import autotest
	
	app = autotest.MyApp(False)
	app.MainLoop()