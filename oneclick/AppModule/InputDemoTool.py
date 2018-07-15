#!/usr/bin/env python
# _*_ coding: utf-8 _*_

#----------------------------------------------------------------------------
# Nom:		InputDemoTool.py
# Objet:	Fenêtres Dialog pour entrer les valeurs des variables
#
# Auteur:	Jean-Michel RUFFLE
# Date:		Mars 2009
#
# Auteur modification: Jean-Marc SEILLON
# Modification: ajout des classes GNSS,GNSS_Infos, GNSS_Page
# Date:		Fevrier 2012
#
# Modif du texte du Help
# Date:		Avril 2012
#
# Modif, ajout __OnCheckNMEA dans la classe Notebook 
# date: Mai 2012
# Version:	AutoTest 1.8.4 DemoTool
#----------------------------------------------------------------------------

#date              who                 version                 modification
#2008..2011        JM Ruffle           1.x                     creation and modifications
#28-02-2012        Jean-Marc SEILLON   1.8.2                   classes GNSS,GNSS_Infos, GNSS_Page
#23-03-2012        Jean-Marc Seillon   1.8.3                   modifications for GNSS
#xx-05-2012        Jean-Marc Seillon   1.8.4                   modifications for GNSS feature
#xx-05-2012        Jean-Marc Seillon   1.8.6                   optionally don't send AT+KGNSS* anymore (for 3G, to be done by external tool)
#18-06-2012        Jean-Marc Seillon   1.8.7                   Deletion of "3G" in the label (ligne 2158), bug 4120


import wx, os, sys
import VarDemoTool
import Mux0710Dlg
import Test
import Output
import DemoToolScripts
import datetime
import anydbm, dbhash
import shelve

from MSDeCall import MSDeCall
from ComModuleAPI import SafePrintError, SagOpen, SagSend, SagWaitLine, SafePrint, SagClose, SagStopAllThread, SagTestCmd

from ComDetect import WndProcHookMixin
import _winreg
from PersonalException import *
from VarGlobal import VERSION
###############
# Config Dialog #
###############
class ConfigurationDialog(wx.Dialog,WndProcHookMixin):
	def __init__(self, parent=None, NoteBook=None):
		self.NoteBook = NoteBook
		WndProcHookMixin.__init__(self)
		wx.Dialog.__init__(self, parent, -1, "Configuration", size=(350, 235))
		
		# Create objects to display
		self.ComAndSim = ComAndSim(self)
		self.GPRS = GPRS(self)
		ButtonPanel = wx.Panel(self)
		self.SaveButton = wx.Button(ButtonPanel, -1, "Save")
		self.CancelButton = wx.Button(ButtonPanel, -1, "Cancel")
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.GPRS, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		ButtonBox.Add(self.SaveButton, 0,wx.RIGHT,15)
		ButtonBox.Add(self.CancelButton, 0)
		ButtonPanel.SetSizer(ButtonBox)
		Box.Add(ButtonPanel, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		self.SetSizer(Box)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnSave, self.SaveButton)			# When Clic on Save Button
		self.Bind(wx.EVT_BUTTON, self.__OnCancel, self.CancelButton)		# When Clic on Cancel Button
		self.Bind(wx.EVT_TEXT, self.__OnTxtChange)							# When Text Change active or desactive buttons
		self.Bind(wx.EVT_CHOICE, self.__OnTxtChange)						# When List box Change active or desactive buttons
		self.Bind(wx.EVT_CLOSE, self.__OnClose)								# When List box Change active or desactive buttons
		
		self.__OnTxtChange()												# Init activation of buttons
		
		self.ShowModal()													# Display Dialog
	
	def __OnSave(self,evt):
		VarDemoTool.COM_Port  = self.ComAndSim.COM.GetStringSelection().split("COM")[1]
		VarDemoTool.COM_Speed = self.ComAndSim.SpeedListBox.GetStringSelection()
		VarDemoTool.SIM_PIN	  = self.ComAndSim.Pin.GetValue()
		
		VarDemoTool.GPRS_APN	  = self.GPRS.APN.GetValue()
		VarDemoTool.GPRS_Login	  = self.GPRS.Login.GetValue()
		VarDemoTool.GPRS_Password = self.GPRS.Password.GetValue()
		
		if self.NoteBook != None:
			self.NoteBook.Update_COM_And_GPRS_Values()
		
		WriteConfigFile()
		self.Destroy()
	
	def __OnCancel(self,evt):
		self.Destroy()
	
	def __OnTxtChange(self,evt=None):
		self.SaveButton.Enable(self.ComAndSim.AllFielded() and self.GPRS.AllFielded())
	
	def __OnClose(self,evt):
		self.unhookWndProc()
		evt.Skip()

##########
# NoteBook #
##########
class Notebook(wx.Notebook):
	def __init__(self, parent, id=-1):
		wx.Notebook.__init__(self, parent, id, name="NoteBook",style=wx.BK_LEFT|wx.NB_MULTILINE)
		
		ReadConfigFile()
		
		# Add all pages
		self.AddPage(FTP_Page(self))			# "FTP"
		self.AddPage(TCP_Page(self))			# "TCP"
		self.AddPage(SMS_Page(self))			# "SMS"
		self.AddPage(VoiceCall_Page(self))		# "Voice Call"
		self.AddPage(MUX_Page(self))			# "MUX"
		self.GetPage(4).Enable(False)			# Disable MUX
		self.AddPage(GPIO_Page(self))			# "GPIO"
		self.AddPage(FileSystem_Page(self))		# "File System"
		self.AddPage(SMTP_Page(self))			# "SMTP"
		self.AddPage(Environment_Page(self))	# "Environment_Page"
		self.AddPage(Environment_Page2(self))	# "Environment_Page2"
		self.AddPage(AT_Terminal_Page(self))	# "AT_Terminal"
		self.AddPage(GNSS_Page(self))			# "GNSS"
		self.AddPage(eCall_Page(self))			# "eCall"
		'''
		self.AddPage(FOTA_PDU_Page(self))		# "FOTA_PDU_Page"
		'''
		# events
		self.Bind(wx.EVT_CHECKBOX, self.__OnCheckNMEA)#ajout Mai 2012
		self.Bind(VarDemoTool.EVT_RUN, self.__OnRun)						# On run active or desactive notbook
		self.Bind(wx.EVT_BUTTON, self.__OnHelp)								# Display Help

	def __OnCheckNMEA(self, evt):
		VarDemoTool.CheckNMEA = not VarDemoTool.CheckNMEA
		#print str(VarDemoTool.CheckNMEA)

	def __OnRun(self, evt):
		self.Enable(not(evt.GetRunStatus()))		# Active or desactive notebook
		evt.Skip()
	
	def __OnHelp(self, evt):
		button = self.FindWindowById(evt.GetId())	# Get button press
		if button.GetName()=="Help":				# Check if is a Help Button
			dlg = wx.MessageDialog(None, button.GetParent().Help(),"Help on "+button.GetParent().GetName()+":" ,wx.ICON_QUESTION)	# Display Help Dialog
			dlg.ShowModal()
	
	# Set COM, SIM and GPRS Value (call after boot and after modification)
	def Set_COM_And_GPRS_Values(self,COM_Port,COM_Speed,PIN_Code,GPRS_APN,GPRS_Login,GPRS_Password):
		for i in range(self.GetPageCount()):
			try:
				self.GetPage(i).ComAndSim.SetValues(COM_Port,COM_Speed,PIN_Code)
				self.GetPage(i).GPRS.SetValues(GPRS_APN,GPRS_Login,GPRS_Password)
			except:
				pass
	
	# Update with Default params
	def Update_COM_And_GPRS_Values(self):
		self.Set_COM_And_GPRS_Values(VarDemoTool.COM_Port,VarDemoTool.COM_Speed,VarDemoTool.SIM_PIN,VarDemoTool.GPRS_APN,VarDemoTool.GPRS_Login,VarDemoTool.GPRS_Password)
	
	# Redefine AddPage function
	def AddPage(self, panel, text=None, select = False, imageId = -1):
		if text==None:
			super(Notebook, self).AddPage(panel,panel.GetName().replace("_"," "))
		else:
			super(Notebook, self).AddPage(panel,text,select,imageId)

################
# NoteBook Pages  #
################
def StartScript(self, id):
	scriptName = self.GetName() + "_" 
	scriptName += self.FindWindowById(id).GetName()

	WriteConfigFile()
	MainFrame = self.GetParent().GetParent()

	if MainFrame.log_flag:
		MainFrame.test_output = Output.GuiLogOutput(MainFrame.log_tc, MainFrame.log_file)
	else:
		MainFrame.test_output = Output.GuiOutput(MainFrame.log_tc)
	
	MainFrame.toolBar.EnableTool(MainFrame.ID_stop, 1)
	MainFrame.menuBar.Enable(MainFrame.ID_Config,False)
	
	#MainFrame.test = Test.Test(cfg=self.GetParent(), gui=True, list_test=[scriptName], test_output=MainFrame.test_output, toolBar=MainFrame.toolBar, log_tc=MainFrame.log_tc, ID_stop=MainFrame.ID_stop)
	MainFrame.test = Test.Test(cfg='', gui=True, list_test=[scriptName], test_output=MainFrame.test_output, MainFrame=MainFrame,DemoToolId=self.GetParent())#toolBar=MainFrame.toolBar, log_tc=MainFrame.log_tc, ID_stop=MainFrame.ID_stop)
	MainFrame.test.start() #start the thread 'test'

def StartScript2(self, Func_Name, noteBook):
	scriptName = Func_Name
#	print"Name: ",scriptName
	WriteConfigFile()
	MainFrame = self

	if MainFrame.log_flag:
		MainFrame.test_output = Output.GuiLogOutput(MainFrame.log_tc, MainFrame.log_file)
	else:
		MainFrame.test_output = Output.GuiOutput(MainFrame.log_tc)
	
	MainFrame.toolBar.EnableTool(MainFrame.ID_stopGNSS, 0)
	MainFrame.toolBar.EnableTool(MainFrame.ID_startGNSS, 0)
	MainFrame.menuBar.Enable(MainFrame.ID_Config,False)
	
	MainFrame.test = Test.Test(cfg='', gui=True, list_test=[scriptName], test_output=MainFrame.test_output, MainFrame=MainFrame,DemoToolId=noteBook)#toolBar=MainFrame.toolBar, log_tc=MainFrame.log_tc, ID_stop=MainFrame.ID_stop)
	MainFrame.test.start() #start the thread 'test'

# specific for eCall
def StartScript3(self, Func_Name, noteBook):
	scriptName = Func_Name
#	print"Name: ",scriptName
	WriteConfigFile()
	MainFrame = noteBook.GetParent()

	if MainFrame.log_flag:
		MainFrame.test_output = Output.GuiLogOutput(MainFrame.log_tc, MainFrame.log_file)
	else:
		MainFrame.test_output = Output.GuiOutput(MainFrame.log_tc)
	
#	MainFrame.menuBar.Enable(MainFrame.ID_Config,False)
	

def ReadConfigFile():
	if os.path.isfile("Config.ini"):
		file = open("Config.ini", 'r')
		data = file.read()
		file.close()
		data = data.decode("utf8","replace").split(";")
		if len(data) == 32:
			VarDemoTool.COM_Port		= data[0]
			VarDemoTool.COM_Speed		= data[1]
			VarDemoTool.SIM_PIN			= data[2]
			VarDemoTool.GPRS_APN		= data[3]
			VarDemoTool.GPRS_Login		= data[4]
			VarDemoTool.GPRS_Password	= data[5]
			VarDemoTool.FTP_URL			= data[6]
			VarDemoTool.FTP_Port		= data[7]
			VarDemoTool.FTP_Login		= data[8]
			VarDemoTool.FTP_Password	= data[9]
			VarDemoTool.FTP_UplaodPath	= data[10]
			VarDemoTool.FTP_UplaodFile	= data[11]
			VarDemoTool.FTP_DownlaodPath= data[12]
			VarDemoTool.FTP_DownlaodFile= data[13]
			VarDemoTool.TCP_URL			= data[14]
			VarDemoTool.TCP_Port		= data[15]
			VarDemoTool.SMS_Number		= data[16]
			VarDemoTool.SMS_Text		= data[17]
			VarDemoTool.VoiceCall_Number= data[18]
			VarDemoTool.GPIO_Number		= data[19]
			VarDemoTool.GPIO_Value		= data[20]
			VarDemoTool.FS_WriteName	= data[21]
			VarDemoTool.FS_WriteFile	= data[22]
			VarDemoTool.FS_ReadName		= data[23]
			VarDemoTool.SMTP_Server		= data[24]
			VarDemoTool.SMTP_Email		= data[25]
			VarDemoTool.SMTP_Login		= data[26]
			VarDemoTool.SMTP_PassWord	= data[27]
			VarDemoTool.SMTP_To			= data[28]
			VarDemoTool.SMTP_Subject	= data[29]
			VarDemoTool.SMTP_Text		= data[30].replace("\\r","\r").replace("\\n","\n")
			VarDemoTool.PDU_File		= data[31]

def WriteConfigFile():
	config = [VarDemoTool.COM_Port,VarDemoTool.COM_Speed,VarDemoTool.SIM_PIN,VarDemoTool.GPRS_APN,VarDemoTool.GPRS_Login,
			  VarDemoTool.GPRS_Password,VarDemoTool.FTP_URL,VarDemoTool.FTP_Port,VarDemoTool.FTP_Login,VarDemoTool.FTP_Password,
			  VarDemoTool.FTP_UplaodPath,VarDemoTool.FTP_UplaodFile,VarDemoTool.FTP_DownlaodPath,VarDemoTool.FTP_DownlaodFile,
			  VarDemoTool.TCP_URL,VarDemoTool.TCP_Port,VarDemoTool.SMS_Number,VarDemoTool.SMS_Text,VarDemoTool.VoiceCall_Number,
			  VarDemoTool.GPIO_Number,VarDemoTool.GPIO_Value,VarDemoTool.FS_WriteName,VarDemoTool.FS_WriteFile,VarDemoTool.FS_ReadName,
			  VarDemoTool.SMTP_Server,VarDemoTool.SMTP_Email,VarDemoTool.SMTP_Login,VarDemoTool.SMTP_PassWord,VarDemoTool.SMTP_To,
			  VarDemoTool.SMTP_Subject,VarDemoTool.SMTP_Text.replace("\r","\\r").replace("\n","\\n"),VarDemoTool.PDU_File]
	data = ";".join("%s"%elem for elem in config)
	data = data.encode("utf8","replace")
	file = open("Config.ini", 'w')
	file.write(data)
	file.close()

class FTP_Page(wx.Panel):
	def  __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="FTP")
		
		# Create objects to display
		self.ComAndSim = ComAndSim(self,False)
		self.GPRS = GPRS(self,False)
		self.FTP = FTP(self)
		ButtonPanel = wx.Panel(self)
		self.UploadButton = wx.Button(ButtonPanel, -1, "Upload",name="Upload")
		self.DownloadButton = wx.Button(ButtonPanel, -1, "Download",name="Download")
		self.HelpButton = wx.Button(self, -1, "?",size=(25,25),name="Help")
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.GPRS, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.FTP, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		ButtonBox.Add(self.DownloadButton, 0,wx.RIGHT,10)
		ButtonBox.Add(self.UploadButton, 0,wx.LEFT,75)
		ButtonPanel.SetSizer(ButtonBox)
		Box.Add(ButtonPanel, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		Box.Add((10,10),1)
		Box.Add(self.HelpButton,0,wx.LEFT|wx.BOTTOM|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT,5)
		self.SetSizer(Box)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnUpload, self.UploadButton)		# When Clic on Upload Button
		self.Bind(wx.EVT_BUTTON, self.__OnDownload, self.DownloadButton)	# When Clic on Download Button
		self.Bind(wx.EVT_TEXT, self.__OnTxtChange)							# When Text Change active or desactive buttons
		
		self.__OnTxtChange()												# Init activation of buttons
	
	def __OnUpload(self, evt):
		VarDemoTool.FTP_URL			 = self.FTP.URL.GetValue()
		VarDemoTool.FTP_Port		 = self.FTP.FTPPort.GetValue()
		VarDemoTool.FTP_Login		 = self.FTP.Login.GetValue()
		VarDemoTool.FTP_Password	 = self.FTP.Password.GetValue()
		VarDemoTool.FTP_UplaodPath	 = self.FTP.FTPPathTosend.GetValue()
		VarDemoTool.FTP_UplaodFile	 = self.FTP.FileToSend.GetValue()
		VarDemoTool.FTP_DownlaodPath = self.FTP.FTPPathToReceive.GetValue()
		VarDemoTool.FTP_DownlaodFile = self.FTP.FileToReceive.GetValue()
		
		StartScript(self,evt.GetId())
	
	def __OnDownload(self, evt):
		VarDemoTool.FTP_URL			 = self.FTP.URL.GetValue()
		VarDemoTool.FTP_Port		 = self.FTP.FTPPort.GetValue()
		VarDemoTool.FTP_Login		 = self.FTP.Login.GetValue()
		VarDemoTool.FTP_Password	 = self.FTP.Password.GetValue()
		VarDemoTool.FTP_UplaodPath	 = self.FTP.FTPPathTosend.GetValue()
		VarDemoTool.FTP_UplaodFile	 = self.FTP.FileToSend.GetValue()
		VarDemoTool.FTP_DownlaodPath = self.FTP.FTPPathToReceive.GetValue()
		VarDemoTool.FTP_DownlaodFile = self.FTP.FileToReceive.GetValue()
		
		StartScript(self,evt.GetId())
	
	def __OnTxtChange(self,evt=None):
		COM_and_GPRS = self.ComAndSim.AllFielded() and self.GPRS.AllFielded()
		self.UploadButton.Enable(self.FTP.AllUplaodFielded() and COM_and_GPRS)
		self.DownloadButton.Enable(self.FTP.AllDownlaodFielded() and COM_and_GPRS)
	
	# Text to display in Help Dialog
	def Help(self):
		text = ["This page allow you to upload or download a file over FTP\r\n",
				"Download button: download a file from FTP server",
				"Upload button: uplaod your file to FTP server",
				"All data receive are store in :",
				'"%s\DATA\FTP"'%(os.getcwd())]
		
		return  '\r\n'.join(text)

class TCP_Page(wx.Panel):
	def  __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="TCP")
		
		# Create objects to display
		self.ComAndSim = ComAndSim(self,False)
		self.GPRS = GPRS(self,False)
		self.TCP = TCP(self)
		ButtonPanel = wx.Panel(self)
		self.TCPButton = wx.Button(ButtonPanel, -1, "Request", name="REQUEST")
		self.HelpButton = wx.Button(self, -1, "?",size=(25,25),name="Help")
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.GPRS, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.TCP, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		ButtonBox.Add(self.TCPButton, 0)
		ButtonPanel.SetSizer(ButtonBox)
		Box.Add(ButtonPanel, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		Box.Add((10,10),1)
		Box.Add(self.HelpButton,0,wx.LEFT|wx.BOTTOM|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT,5)
		self.SetSizer(Box)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnRequest, self.TCPButton)			# When Clic on Request Button
		self.Bind(wx.EVT_TEXT, self.__OnTxtChange)							# When Text Change active or desactive buttons
		
		self.__OnTxtChange()												# Init activation of buttons
	
	def __OnRequest(self, evt):
		VarDemoTool.TCP_URL  = self.TCP.URL.GetValue()
		VarDemoTool.TCP_Port = self.TCP.TCPPort.GetValue()
		StartScript(self,evt.GetId())
	
	def __OnTxtChange(self,evt=None):
		COM_and_GPRS = self.ComAndSim.AllFielded() and self.GPRS.AllFielded()
		self.TCPButton.Enable(self.TCP.AllFielded() and COM_and_GPRS)
	
	# Text to display in Help Dialog
	def Help(self):
		text = ["This page allow you to get a HTML page\r\n",
				"Request: send a get over TCP and dislpay the web page",
				"All data receive are store in :",
				'"%s\DATA\TCP"'%(os.getcwd())]
		
		return  '\r\n'.join(text)

class SMS_Page(wx.Panel):
	def  __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="SMS")
		
		# Create objects to display
		self.ComAndSim = ComAndSim(self,False)
		self.SMS = SMS(self)
		ButtonPanel = wx.Panel(self)
		self.SendSMSButton = wx.Button(ButtonPanel, -1, "SEND", name="Send")
		self.RcvSMSButton = wx.Button(ButtonPanel, -1, "Wait Incomming SMS", name="Wait Incomming SMS")
		self.HelpButton = wx.Button(self, -1, "?",size=(25,25),name="Help")
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.SMS, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		ButtonBox.Add(self.SendSMSButton, 0, wx.RIGHT,15)
		ButtonBox.Add(self.RcvSMSButton, 0)
		ButtonPanel.SetSizer(ButtonBox)
		Box.Add(ButtonPanel, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		Box.Add((10,10),1)
		Box.Add(self.HelpButton,0,wx.LEFT|wx.BOTTOM|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT,5)
		self.SetSizer(Box)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnSendSMS, self.SendSMSButton)		# When Clic on Send SMS Button
		self.Bind(wx.EVT_BUTTON, self.__OnReceiveSMS, self.RcvSMSButton)	# When Clic on Read SMS Button
		self.Bind(wx.EVT_TEXT, self.__OnTxtChange)							# When Text Change active or desactive buttons
		
		self.__OnTxtChange()												# Init activation of buttons
	
	def __OnSendSMS(self,evt):
		VarDemoTool.SMS_IRA	   = self.SMS.IRA.GetValue()
		VarDemoTool.SMS_Number = self.SMS.Number.GetValue()
		VarDemoTool.SMS_Text   = self.SMS.Text.GetValue()
		StartScript(self,evt.GetId())
	
	def __OnReceiveSMS(self,evt):
		StartScript(self,evt.GetId())
	
	def __OnTxtChange(self,evt=None):
		COM_and_GPRS = self.ComAndSim.AllFielded()
		self.SendSMSButton.Enable(self.SMS.AllFielded() and COM_and_GPRS)
	
	# Text to display in Help Dialog
	def Help(self):
		text = ["This page allow you to send and receives SMS\r\n",
				"Send: Send your SMS to the phone number",
				"Wait incomming SMS: 30 sec a SMS and display it"]
		
		return  '\r\n'.join(text)

class VoiceCall_Page(wx.Panel):
	def  __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="Voice Call")
		
		# Create objects to display
		self.ComAndSim = ComAndSim(self,False)
		self.VoiceCall = VoiceCall(self)
		ButtonPanel = wx.Panel(self)
		self.CallButton = wx.Button(ButtonPanel, -1, "Call", name="Call")
		self.HelpButton = wx.Button(self, -1, "?",size=(25,25),name="Help")
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.VoiceCall, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		ButtonBox.Add(self.CallButton, 0)
		ButtonPanel.SetSizer(ButtonBox)
		Box.Add(ButtonPanel, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		Box.Add((10,10),1)
		Box.Add(self.HelpButton,0,wx.LEFT|wx.BOTTOM|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT,5)
		self.SetSizer(Box)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnCall, self.CallButton)			# When Clic on Call Button
		self.Bind(wx.EVT_TEXT, self.__OnTxtChange)							# When Text Change active or desactive buttons
		
		self.__OnTxtChange()												# Init activation of buttons

	def __OnCall(self,evt):
		VarDemoTool.VoiceCall_Number = self.VoiceCall.Number.GetValue()
		StartScript(self,evt.GetId())
	
	def __OnTxtChange(self,evt=None):
		COM_and_GPRS = self.ComAndSim.AllFielded()
		self.CallButton.Enable(self.VoiceCall.AllFielded() and COM_and_GPRS)
	
	# Text to display in Help Dialog
	def Help(self):
		text = ["This page allow you to make a voice call\r\n",
				"Call: Make a voice call to the phone number"]
		
		return  '\r\n'.join(text)

class MUX_Page(wx.Panel):
	def  __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="MUX")
		
		# Create objects to display
		self.ComAndSim = ComAndSim(self,False)
		self.GPRS = GPRS(self,False)
		self.FTP = MUX(self)
		ButtonPanel = wx.Panel(self)
		#self.UploadButton = wx.Button(ButtonPanel, -1, "Upload", name="Upload")
		self.DownloadButton = wx.Button(ButtonPanel, -1, "Download", name="Download")
		self.HelpButton = wx.Button(self, -1, "?",size=(25,25),name="Help")
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.GPRS, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.FTP, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		#ButtonBox.Add(self.UploadButton, 0,wx.RIGHT,15)
		ButtonBox.Add(self.DownloadButton, 0)
		ButtonPanel.SetSizer(ButtonBox)
		Box.Add(ButtonPanel, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		Box.Add((10,10),1)
		Box.Add(self.HelpButton,0,wx.LEFT|wx.BOTTOM|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT,5)
		self.SetSizer(Box)
		
		# Events
		#self.Bind(wx.EVT_BUTTON, self.__OnUpload, self.UploadButton)		# When Clic on Upload Button
		self.Bind(wx.EVT_BUTTON, self.__OnDownload, self.DownloadButton)	# When Clic on Download Button
		self.Bind(wx.EVT_TEXT, self.__OnTxtChange)							# When Text Change active or desactive buttons
		
		self.__OnTxtChange()												# Init activation of buttons

	def __OnUpload(self, evt):
		VarDemoTool.FTP_URL			 = self.FTP.URL.GetValue()
		VarDemoTool.FTP_Port		 = self.FTP.FTPPort.GetValue()
		VarDemoTool.FTP_Login		 = self.FTP.Login.GetValue()
		VarDemoTool.FTP_Password	 = self.FTP.Password.GetValue()
		VarDemoTool.FTP_UplaodPath	 = self.FTP.FTPPathTosend.GetValue()
		VarDemoTool.FTP_UplaodFile	 = self.FTP.FileToSend.GetValue()
		VarDemoTool.FTP_DownlaodPath = self.FTP.FTPPathToReceive.GetValue()
		VarDemoTool.FTP_DownlaodFile = self.FTP.FileToReceive.GetValue()
		Mux0710Dlg.openDlg07102()
		StartScript(self,evt.GetId())
	
	def __OnDownload(self, evt):
		VarDemoTool.FTP_URL			 = self.FTP.URL.GetValue()
		VarDemoTool.FTP_Port		 = self.FTP.FTPPort.GetValue()
		VarDemoTool.FTP_Login		 = self.FTP.Login.GetValue()
		VarDemoTool.FTP_Password	 = self.FTP.Password.GetValue()
		#VarDemoTool.FTP_UplaodPath	 = self.FTP.FTPPathTosend.GetValue()
		#VarDemoTool.FTP_UplaodFile	 = self.FTP.FileToSend.GetValue()
		VarDemoTool.FTP_DownlaodPath = self.FTP.FTPPathToReceive.GetValue()
		VarDemoTool.FTP_DownlaodFile = self.FTP.FileToReceive.GetValue()
		
		Mux0710Dlg.openDlg07102()
		StartScript(self,evt.GetId())
	
	def __OnTxtChange(self,evt=None):
		COM_and_GPRS = self.ComAndSim.AllFielded() and self.GPRS.AllFielded()
		#self.UploadButton.Enable(self.FTP.AllUplaodFielded() and COM_and_GPRS)
		self.DownloadButton.Enable(self.FTP.AllDownlaodFielded() and COM_and_GPRS)
	
	# Text to display in Help Dialog
	def Help(self):
		text = ["This page allow you to \r\n"]
		
		return  '\r\n'.join(text)

class GPIO_Page(wx.Panel):
	def  __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="GPIO")
		
		# Create objects to display
		self.ComAndSim = ComAndSim(self,False)
		self.GPIO = GPIO(self)
		ButtonPanel = wx.Panel(self)
		self.ReadButton = wx.Button(ButtonPanel, -1, "Read",name="Read")
		self.HelpButton = wx.Button(self, -1, "?",size=(25,25),name="Help")
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.GPIO, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		ButtonBox.Add(self.ReadButton, 0)
		ButtonPanel.SetSizer(ButtonBox)
		Box.Add(ButtonPanel, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		Box.Add((10,10),1)
		Box.Add(self.HelpButton,0,wx.LEFT|wx.BOTTOM|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT,5)
		self.SetSizer(Box)
		
		# Desactive all GPIO checkbox and read button
		self.ReadButton.Enable(False)
		self.GPIO.GPIO1.Enable(False)
		self.GPIO.GPIO2.Enable(False)
		self.GPIO.GPIO3.Enable(False)
		self.GPIO.GPIO4.Enable(False)
		self.GPIO.GPIO5.Enable(False)
		
		# Events
		self.Bind(wx.EVT_RADIOBUTTON, self.__OnRadioButtonSelected)			# When Clic on one of two radio button
		self.Bind(wx.EVT_CHECKBOX, self.__OnCheckBoxSelected)				# When Clic on one of five check box
		self.Bind(wx.EVT_BUTTON, self.__OnRead, self.ReadButton)			# When Clic on Read button

	def __OnRadioButtonSelected(self, evt):
		if self.ComAndSim.AllFielded():
			OutputSelected = self.GPIO.OutputSelected()
			self.ReadButton.Enable(not(OutputSelected))
			self.GPIO.GPIO1.Enable(OutputSelected)
			self.GPIO.GPIO2.Enable(OutputSelected)
			self.GPIO.GPIO3.Enable(OutputSelected)
			self.GPIO.GPIO4.Enable(OutputSelected)
			self.GPIO.GPIO5.Enable(OutputSelected)
			StartScript(self,evt.GetId())
		else:
			self.ReadButton.Enable(False)
			self.GPIO.Input.SetValue(False)
			self.GPIO.Output.SetValue(False)
	
	def __OnCheckBoxSelected(self, evt):
		CheckBox = self.GPIO.FindWindowById(evt.GetId())
		VarDemoTool.GPIO_Number = CheckBox.GetLabel().split()[1]
		if CheckBox.GetValue():
			VarDemoTool.GPIO_Value  = "1"
		else:
			VarDemoTool.GPIO_Value  = "0"
		StartScript(self,evt.GetId())
	
	def __OnRead(self, evt):
		StartScript(self,evt.GetId())
	
	# Text to display in Help Dialog
	def Help(self):
		text = ["This page allow you to set or read GPIO\r\n",
				"Input: set GPIO as input",
				"Output: set GPIO as output",
				"Read: read States of GPIO (only available on input mode)",
				"GPIO (1-5): display state in input mode or could be set in output mode"]
		
		return  '\r\n'.join(text)

class FileSystem_Page(wx.Panel):
	def  __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="File System")
		
		# Create objects to display
		self.ComAndSim = ComAndSim(self,False)
		self.FileSystem = FileSystem(self)
		ButtonPanel = wx.Panel(self)
		self.WriteFileButton = wx.Button(ButtonPanel,-1,"Write File", name="Write File")
		self.ReadFileButton = wx.Button(ButtonPanel,-1,"Read File", name="Read File")
		self.ClearButton = wx.Button(ButtonPanel,-1,"Clear all files", name="Clear all files")
		self.HelpButton = wx.Button(self, -1, "?",size=(25,25),name="Help")
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.FileSystem, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		ButtonBox.Add(self.WriteFileButton, 0,wx.RIGHT,15)
		ButtonBox.Add(self.ReadFileButton, 0,wx.RIGHT,15)
		ButtonBox.Add(self.ClearButton, 0)
		ButtonPanel.SetSizer(ButtonBox)
		Box.Add(ButtonPanel, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		Box.Add((10,10),1)
		Box.Add(self.HelpButton,0,wx.LEFT|wx.BOTTOM|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT,5)
		self.SetSizer(Box)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnWrite, self.WriteFileButton)		# When Clic on write Button
		self.Bind(wx.EVT_BUTTON, self.__OnRead, self.ReadFileButton)		# When Clic on read Button
		self.Bind(wx.EVT_BUTTON, self.__OnClear, self.ClearButton)			# When Clic on clear Button
		self.Bind(wx.EVT_TEXT, self.__OnTxtChange)							# When Text Change active or desactive buttons
		
		self.__OnTxtChange()												# Init activation of buttons

	def __OnWrite(self,evt):
		VarDemoTool.FS_WriteName = self.FileSystem.WriteFileName.GetValue()
		VarDemoTool.FS_WriteFile = self.FileSystem.WriteFile.GetValue()
		StartScript(self,evt.GetId())
	
	def __OnRead(self,evt):
		VarDemoTool.FS_ReadName = self.FileSystem.ReadFile.GetValue()
		StartScript(self,evt.GetId())
	
	def __OnClear(self,evt):
		StartScript(self,evt.GetId())
	
	def __OnTxtChange(self,evt=None):
		COM_and_GPRS = self.ComAndSim.AllFielded()
		self.WriteFileButton.Enable(self.FileSystem.AllWriteFielded() and COM_and_GPRS)
		self.ReadFileButton.Enable(self.FileSystem.AllReadFielded() and COM_and_GPRS)
	
	# Text to display in Help Dialog
	def Help(self):
		text = ["This page allow you to read or write file on HILO file system\r\n",
				"Write File: send a file to HILO file system",
				"Read File: read a file from HILO file system",
				"Clear all files: delete all files on HILO file system",
				"All data receive are store in :",
				'"%s\DATA\File System"'%(os.getcwd())]
		
		return  '\r\n'.join(text)

class SMTP_Page(wx.Panel):
	def  __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="SMTP")
		
		# Create objects to display
		self.ComAndSim = ComAndSim(self,False)
		self.GPRS = GPRS(self,False)
		self.SMTP = SMTP(self)
		ButtonPanel = wx.Panel(self)
		self.SendButton = wx.Button(ButtonPanel, -1, "Send", name="Send")
		self.HelpButton = wx.Button(self, -1, "?",size=(25,25),name="Help")
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.GPRS, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.SMTP, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		ButtonBox.Add(self.SendButton, 0)
		ButtonPanel.SetSizer(ButtonBox)
		Box.Add(ButtonPanel, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		Box.Add((10,10),1)
		Box.Add(self.HelpButton,0,wx.LEFT|wx.BOTTOM|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT,5)
		self.SetSizer(Box)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnSend, self.SendButton)			# When Clic on send Button
		self.Bind(wx.EVT_TEXT, self.__OnTxtChange)							# When Text Change active or desactive buttons
		
		self.__OnTxtChange()												# Init activation of buttons

	def __OnSend(self,evt):
		VarDemoTool.SMTP_Server		 = self.SMTP.Server.GetValue()
		VarDemoTool.SMTP_Email		 = self.SMTP.Email.GetValue()
		VarDemoTool.SMTP_Login		 = self.SMTP.Login.GetValue()
		VarDemoTool.SMTP_PassWord	 = self.SMTP.PassWord.GetValue()
		VarDemoTool.SMTP_To		 	 = self.SMTP.To.GetValue()
		VarDemoTool.SMTP_Subject 	 = self.SMTP.Subject.GetValue()
		VarDemoTool.SMTP_Text	 	 = self.SMTP.Text.GetValue().replace('\n','\r\n')
		StartScript(self,evt.GetId())
	
	def __OnTxtChange(self,evt=None):
		COM_and_GPRS = self.ComAndSim.AllFielded() and self.GPRS.AllFielded()
		self.SendButton.Enable(self.SMTP.AllFielded() and COM_and_GPRS)
	
	# Text to display in Help Dialog
	def Help(self):
		text = ["This page allow you to send a email\r\n",
				"Send: send the email"]
		
		return  '\r\n'.join(text)

class Environment_Page(wx.Panel):
	def  __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="Environment")
		
		# Create objects to display
		self.ComAndSim = ComAndSim(self,False)
		self.Environment_Module = Environment_Module(self)
		self.Environment_SIM = Environment_SIM(self)
		self.Environment_RF = Environment_RF(self)
		ButtonPanel = wx.Panel(self)
		self.ReadButton = wx.Button(ButtonPanel, -1, "Read Environment", name="Read")
		self.HelpButton = wx.Button(self, -1, "?",size=(25,25),name="Help")
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.Environment_Module, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.Environment_SIM, 	 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.Environment_RF, 	 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		ButtonBox.Add(self.ReadButton, 0)
		ButtonPanel.SetSizer(ButtonBox)
		Box.Add(ButtonPanel, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		Box.Add((10,10),1)
		Box.Add(self.HelpButton,0,wx.LEFT|wx.BOTTOM|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT,5)
		self.SetSizer(Box)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnRead, self.ReadButton)			# When Clic on send Button
		self.Bind(wx.EVT_TEXT, self.__OnTxtChange)							# When Text Change active or desactive buttons
		
		self.__OnTxtChange()												# Init activation of buttons

	def __OnRead(self,evt):
		self.Environment_RF.clear()
		StartScript(self,evt.GetId())
	
	def __OnTxtChange(self,evt=None):
		self.ReadButton.Enable(self.ComAndSim.AllFielded())
	
	# Text to display in Help Dialog
	def Help(self):
		text = ["This page allow you to read module environement\r\n",
				]
		
		return  '\r\n'.join(text)

class Environment_Page2(wx.Panel):
	def  __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="Environment_2")
		
		# Create objects to display
		self.ComAndSim = ComAndSim(self,False)
		self.Environment_PhoneBook = Environment_PhoneBook(self)
		self.Environment_SMS = Environment_SMS(self)
		self.Environment_Alarm = Environment_Alarm(self)
		ButtonPanel = wx.Panel(self)
		self.ReadButton = wx.Button(ButtonPanel, -1, "Read Environment", name="Read")
		ButtonPanel2 = wx.Panel(self)
		self.AlarmButton = wx.Button(ButtonPanel2, -1, "Set Alarm", name="Alarm")
		self.HelpButton = wx.Button(self, -1, "?",size=(25,25),name="Help")
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.Environment_PhoneBook, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.Environment_SMS, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		ButtonBox.Add(self.ReadButton, 0)
		ButtonPanel.SetSizer(ButtonBox)
		Box.Add(ButtonPanel, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		Box.Add(self.Environment_Alarm, 0,wx.EXPAND|wx.LEFT|wx.RIGHT,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		ButtonBox.Add(self.AlarmButton, 0)
		ButtonPanel2.SetSizer(ButtonBox)
		Box.Add(ButtonPanel2, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		Box.Add((10,10),1)
		Box.Add(self.HelpButton,0,wx.LEFT|wx.BOTTOM|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT,5)
		self.SetSizer(Box)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnRead, self.ReadButton)			# When Clic on send Button
		self.Bind(wx.EVT_BUTTON, self.__OnAlarm, self.AlarmButton)			# When Clic on Set Alarm Button
		self.Bind(wx.EVT_TEXT, self.__OnTxtChange)							# When Text Change active or desactive buttons
		
		self.__OnTxtChange()												# Init activation of buttons

	def __OnRead(self,evt):
		self.Environment_PhoneBook.clear()
		self.Environment_SMS.clear()
		StartScript(self,evt.GetId())
	
	def __OnAlarm(self,evt):
		dlg = wx.MessageDialog(None, "Please remove PWON jumper(TB301)","Please remove PWON" ,wx.ICON_WARNING)	# Display Help Dialog
		dlg.ShowModal()
		VarDemoTool.Alarm = [self.Environment_Alarm.Hours.GetValue(),self.Environment_Alarm.Minutes.GetValue(),self.Environment_Alarm.Seconds.GetValue()]
		StartScript(self,evt.GetId())
	
	def __OnTxtChange(self,evt=None):
		self.ReadButton.Enable(self.ComAndSim.AllFielded())
	
	# Text to display in Help Dialog
	def Help(self):
		text = ["This page allow you to read module environement\r\n",
				]
		
		return  '\r\n'.join(text)

class AT_Terminal_Page(wx.Panel):
	def  __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="AT_Terminal")
		
		# Create objects to display
		self.AT_Terminal = AT_Terminal(self)
		self.ComAndSim   = self.AT_Terminal
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.AT_Terminal, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		self.SetSizer(Box)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnOpenCOM, 	self.AT_Terminal.OpenButton)				# When Clic on Open Button
		
	def __OnOpenCOM(self,evt):
		if self.AT_Terminal.OpenButton.GetLabel() == "Open":
			self.AT_Terminal.Enable(True)
			VarDemoTool.COM_Port = int(self.AT_Terminal.COM.GetStringSelection().split("COM")[1])
			VarDemoTool.COM_Speed = self.AT_Terminal.SpeedListBox.GetStringSelection()
			VarDemoTool.COM_Flow_Control = self.AT_Terminal.FlowControlListBox.GetStringSelection()
			self.script = DemoToolScripts.AT_Terminal(self.GetParent(),self)
		else:
			self.script.stop()
			self.AT_Terminal.Enable(False)
	
	def __OnTxtChange(self,evt=None):
		self.ReadButton.Enable(self.ComAndSim.AllFielded())
	
	# Text to display in Help Dialog
	def Help(self):
		text = ["This page allow you to read module environement\r\n",
				]
		
		return  '\r\n'.join(text)


class FOTA_PDU_Page(wx.Panel):
	def  __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="PDU")
		
		# Create objects to display
		self.ComAndSim = ComAndSim(self,False)
		self.PDU = FOTA_PDU(self)
		ButtonPanel = wx.Panel(self)
		self.SendPDUButton = wx.Button(ButtonPanel, -1, "SEND", name="Send")
		self.HelpButton = wx.Button(self, -1, "?",size=(25,25),name="Help")
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		Box.Add(self.PDU, 0,wx.EXPAND|wx.LEFT|wx.RIGHT|wx.TOP,5)
		ButtonBox = wx.BoxSizer(wx.HORIZONTAL)
		ButtonBox.Add(self.SendPDUButton, 0, wx.RIGHT,15)
		ButtonPanel.SetSizer(ButtonBox)
		Box.Add(ButtonPanel, 0,wx.LEFT|wx.RIGHT|wx.TOP|wx.ALIGN_CENTER_HORIZONTAL,5)
		Box.Add((10,10),1)
		Box.Add(self.HelpButton,0,wx.LEFT|wx.BOTTOM|wx.ALIGN_BOTTOM|wx.ALIGN_LEFT,5)
		self.SetSizer(Box)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnSendSMS, self.SendPDUButton)		# When Clic on Send SMS Button
		self.Bind(wx.EVT_TEXT, self.__OnTxtChange)							# When Text Change active or desactive buttons
		
		self.__OnTxtChange()												# Init activation of buttons
	
	def __OnSendSMS(self,evt):
		VarDemoTool.PDU_File   = self.PDU.PDU_File.GetValue()
		StartScript(self,evt.GetId())
	
	def __OnReceiveSMS(self,evt):
		StartScript(self,evt.GetId())
	
	def __OnTxtChange(self,evt=None):
		COM_and_GPRS = self.ComAndSim.AllFielded()
		self.SendPDUButton.Enable(self.PDU.AllFielded() and COM_and_GPRS)
	
	# Text to display in Help Dialog
	def Help(self):
		text = ["This page allow you to send a PDU SMS\r\n",
				"Send: Send your PDU SMS to the phone number",
				]
		
		return  '\r\n'.join(text)


class eCall_Page(wx.Panel):
	''' eCall panel '''
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id, name="eCall")
			
		self.MyMSD = MSDeCall(MSDeCall) 	# Instance of MSDecall - see "__OnSend" for completion
		self.GNSS_External=0 #use internal GNSS by default
		self.ComAndSim = ComAndSim(self, False)
		RbList = ["use Internal","use External"]
		sizerrb = wx.BoxSizer(wx.VERTICAL)
		self.NoteBook = None
		# create ihm eCall
		self.eCall_MSD = eCall_MSD(self)
		self.rbox = wx.RadioBox(self, -1, "GNSS", wx.DefaultPosition, wx.DefaultSize,
						RbList, 2, wx.RA_SPECIFY_COLS,name="GPS choice")
		sizerrb.Add(self.rbox, 0, flag=wx.TOP, border=3)
		self.ZoneProc = wx.TextCtrl(self, -1,"",
							size=(250, 80), style=wx.TE_MULTILINE|wx.TE_PROCESS_ENTER)

		self.HelpButton = wx.Button(self, -1, "?", size=(25, 25), name="Help")
		self.Bind(wx.EVT_RADIOBOX, self.EvtRadioBox, self.rbox)
		self.Bind(wx.EVT_BUTTON, self.__OnSend, self.eCall_MSD.SendEcall)
		
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
		Box.Add(self.rbox, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
		Box.Add(self.eCall_MSD, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
		Box.Add(self.ZoneProc, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
		Box.Add(self.HelpButton, 0, wx.LEFT | wx.BOTTOM | wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 5)

		self.displayExtGNSSInfo(None)
		
		self.SetSizer(Box)

	def EvtRadioBox(self,evt):
		'''
		@note: Choice the GPS selection, Internal (on the board) or External (provided by the user).
		Internal: - GPS activation (kgnssrun=1)
				  -	Wait for Fix (+kgnssfix :1)
				  - Ecall configuration (kecallcfg 1, 2)
				  - Start Ecall
		External: - Ecall configuration (kecallcfg 1, 2,3)
				  - Start Ecall
		'''
		selectRB = self.rbox.GetSelection()
		self.GNSS_External = selectRB
		
		self.displayExtGNSSInfo(evt)
		

	def displayExtGNSSInfo(self,evt):
		#disable the GNSS positions and confidence fieds as they are automatically fill by the internal GNSS
		selectRB = self.rbox.GetSelection()
		if selectRB==0:
			dislayInfo=False
			if evt!=None:
				wx.MessageBox("If the external GNSS has been used before you have to reboot your module before using internal GNSS","Warning !")
		else:
			dislayInfo=True
			
		self.eCall_MSD.FieldEW.Enable(dislayInfo)
		self.eCall_MSD.FieldCurLong.Enable(dislayInfo)
		self.eCall_MSD.FieldNS.Enable(dislayInfo)
		self.eCall_MSD.FieldCurLat.Enable(dislayInfo)
		self.eCall_MSD.FieldCurDir.Enable(dislayInfo)
		self.eCall_MSD.FieldConfid.Enable(dislayInfo)
		self.eCall_MSD.Current_Latitude.Enable(dislayInfo)
		self.eCall_MSD.Current_Longitude.Enable(dislayInfo)
		self.eCall_MSD.Current_Direction.Enable(dislayInfo)
		self.eCall_MSD.Confidence.Enable(dislayInfo)
		self.eCall_MSD.text1.Enable(dislayInfo)
		self.eCall_MSD.text2.Enable(dislayInfo)
		self.eCall_MSD.text3.Enable(dislayInfo)

	def __OnSend(self, evt):
		''' Event on start '''
		print "Start eCall event"
#		nBook = self.NoteBook
#	singleton = MSDeCall()
			
		# Véhicule type
		VehiculeType=self.eCall_MSD.FieldVT.GetSelection()+1
		self.MyMSD.setVehiculeType(VehiculeType)		
	
		# Véhicule propulsion storage, values: 1,2,4,8,16,32
		VehiculePropStorage=pow(2,self.eCall_MSD.FieldPS.GetSelection())
		self.MyMSD.setVehPropStrType(VehiculePropStorage)	
		
		# Activation Mode
		actMode=self.eCall_MSD.FieldActivationMode.GetSelection()
		self.MyMSD.setActivationMode(actMode)
		
		# Nb of passengers
		NbPassengers= self.eCall_MSD.FieldNbPass.GetSelection()+1  # index selection starts from 0
		self.MyMSD.setNomberOfPassengers_o(NbPassengers)
		
		# VIN
		VIN = self.eCall_MSD.FieldVIN.GetValue()
		self.MyMSD.setVIN(VIN)

		# Call Number
		callNB = self.eCall_MSD.FieldCallNumb.GetValue()
		callNB = callNB.replace(" ","") #remove spaces
		self.MyMSD.setCallNumber(callNB)
		
		
		# current latitude
		CurLat = self.eCall_MSD.FieldCurLat.GetValue().encode('utf-8')
		if self.eCall_MSD.FieldNS.GetSelection()==0:
			self.MyMSD.setVehicleLocationLatitude(CurLat+",N")
		else:
			self.MyMSD.setVehicleLocationLatitude(CurLat+",S")	
		
		# current longitude
		CurLong = self.eCall_MSD.FieldCurLong.GetValue().encode('utf-8')
		if self.eCall_MSD.FieldEW.GetSelection()==0:
			self.MyMSD.setVehicleLocationLongitude(CurLong+",E")
		else:
			self.MyMSD.setVehicleLocationLongitude(CurLong+",W")
		
		
		# current direction 
		VehicleDirection = self.eCall_MSD.FieldCurDir.GetValue()
		self.MyMSD.setVehicleDirection(int(int(VehicleDirection)/2))
				
		# Write confidence
		Confidence = self.eCall_MSD.FieldConfid.GetSelection()
		self.MyMSD.setConfidence(Confidence)
		
		VarDemoTool.eCall_Number=self.eCall_MSD.FieldCallNumb.GetValue()
		
		self.eCall_MSD.SaveEcallInfo()
						
		# démarrage du thread 
		FuncName = "eCall_Start"
		StartScript(self,evt.GetId())

	def __OnStop(self, evt):
		''' Event on stop '''
		StartScript(self, evt.GetId())

	# Text to display in Help Dialog
	def Help(self):
		''' Help '''
		text = ["Version: "+VERSION+"\r\n"
				"This page allow you to make a emergency call\r\n",
				"To start an emergency call, you have to click the Send ecall button.\r\n",
				"* is an optional field.\r\n"]
		return  '\r\n'.join(text)


class eCall_MSD(wx.Panel):
	def __init__(self, parent, id=-1):
		''' constructor '''
		wx.Panel.__init__(self,parent, id)
		self.NoteBook = self.GetGrandParent()
		# Create objects to display
		panel = wx.Panel(self)
		ListVehicle = ["passenger vehicle (class M1)",
						"buses and coaches (class M2)",
						"buses and coaches (class M3)",
						"light commercial vehicles (class N1)",
						"heavy duty vehicles (class N2)",
						"heavy duty vehicles (class N3)",
						"motorcycles (class L1e)",
						"motorcycles (class L2e)",
						"motorcycles (class L3e)",
						"motorcycles (class L4e)",
						"motorcycles (class L5e)",
						"motorcycles (class L6e)",
						"motorcycles (class L7e)"]
		
		ListPropStorage = ["gasoline tank",
							"diesel tank",
							"compress natural gas (CNG)",
							"liquid propane gas (LPG)",
							"electric energy storage ", #(with more than 42V and 100 Ah)
							"hydrogen storage"]

		ListConfidence = ["No confidence in position","Position can be trusted"]

		ListActivationMode = ["Manual","Automatic"]

		# List of passengers Number in the vehicle
		ListNbPass = ["1","2","3","4","5","6","7","8","9","10","11","12","13"]

		vehicle_type = wx.StaticText(panel, id, " Vehicle type: ")
		self.FieldVT = wx.Choice(panel, -1, wx.DefaultPosition,(200,45),ListVehicle)
		self.FieldVT.SetSelection(0)

		VIN = wx.StaticText(panel, id, " VIN: ")
		self.FieldVIN = wx.TextCtrl(panel, -1, "", size= (115,21),name="FieldVIN")
		self.FieldVIN.SetMaxLength(17)

		propulsion_storage = wx.StaticText(panel, id, " Propulsion storage: ")
		self.FieldPS = wx.Choice(panel, -1, wx.DefaultPosition,(170,45),ListPropStorage)
		self.FieldPS.SetSelection(0)

		Nb_of_passenger = wx.StaticText(panel, id, " Nb of passengers *: ")
		self.FieldNbPass = wx.Choice(panel, -1, wx.DefaultPosition,(45,21),ListNbPass)

		self.Current_Latitude = wx.StaticText(panel, id, " Current Latitude: ")
		self.FieldCurLat = wx.TextCtrl(panel, -1, "",name="FieldCurLat")
		self.FieldNS = wx.Choice(panel, -1, wx.DefaultPosition,(60,21),["North","South"]) # field North/South
		self.text1 = wx.StaticText(panel, id, "degree     ")
		self.Current_Longitude = wx.StaticText(panel, id, " Current Longitude: ")
		self.FieldCurLong = wx.TextCtrl(panel, -1, "",name="FieldCurLong")
		self.FieldEW = wx.Choice(panel, -1, wx.DefaultPosition,(60,21),["East","West"]) # field East/West
		self.text2 = wx.StaticText(panel, id, "degree     ")

		self.Current_Direction = wx.StaticText(panel, id, " Current Direction: ")
		self.FieldCurDir = wx.TextCtrl(panel, -1, "",size= (30,21),name="FieldCurDir")
		self.FieldCurDir.SetMaxLength(3)
		self.text3 = wx.StaticText(panel, id, "degree     ")

		self.Confidence = wx.StaticText(panel, id, " Confidence: ")
		self.FieldConfid = wx.Choice(panel, -1, wx.DefaultPosition,(150,21),ListConfidence)
		self.FieldConfid.SetSelection(0)
		
		ActivationMode = wx.StaticText(panel, id, " Activation mode: ")
		self.FieldActivationMode = wx.Choice(panel, -1, wx.DefaultPosition,(60,21),ListActivationMode)
		self.FieldActivationMode.SetSelection(0)

		Call_Number = wx.StaticText(panel, id, " Call number: ")
		self.FieldCallNumb = wx.TextCtrl(panel, -1, "",name="FieldCallNumb")

		self.SendEcall = wx.Button(panel, -1, "Start eCall", name="Start")
		#ecall cannot be stopped self.StopEcall = wx.Button(panel, -1, "Stop eCall")
		
		#self.Bind(wx.EVT_BUTTON, self.__onSendEcall, self.SendEcall)
		#self.Bind(wx.EVT_BUTTON, self.__onStopEcall, self.StopEcall)

		# Layout data MSD
		staticBox = wx.StaticBox(self, -1, " Minimum Set of Data ")
		MSD_StaticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5, vgap=0)

		sizer.Add(vehicle_type, pos=(0, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldVT, pos=(0, 1),span = (1,3), flag=wx.TOP, border=3)
		sizer.Add(VIN, pos=(1, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldVIN, pos=(1, 1),span = (1,3), flag=wx.TOP, border=3)
		sizer.Add(propulsion_storage, pos=(2, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldPS, pos=(2, 1),span = (1,3), flag=wx.TOP, border=3)
		sizer.Add(Nb_of_passenger, pos=(3, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldNbPass, pos=(3, 1),span = (1,3), flag=wx.TOP, border=3)
		sizer.Add(self.Current_Latitude, pos=(5, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldCurLat, pos=(5, 1), flag=wx.TOP, border=3)
		sizer.Add(self.text1, pos=(5, 2), flag=wx.LEFT|wx.TOP, border=3)
		sizer.Add(self.FieldNS, pos=(5, 3), flag=wx.RIGHT|wx.TOP, border=3)
		sizer.Add(self.Current_Longitude, pos=(6, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldCurLong, pos=(6, 1), flag=wx.TOP, border=3)
		sizer.Add(self.text2, pos=(6, 2), flag=wx.LEFT|wx.TOP, border=3)
		sizer.Add(self.FieldEW, pos=(6, 3), flag=wx.RIGHT|wx.TOP, border=3)
		sizer.Add(self.Current_Direction, pos=(7, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldCurDir, pos=(7, 1), flag=wx.TOP, border=3)
		sizer.Add(self.text3, pos=(7, 2), flag=wx.LEFT|wx.TOP, border=3)
		sizer.Add(self.Confidence, pos=(9, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldConfid, pos=(9, 1), flag=wx.TOP, border=3)
		sizer.Add(ActivationMode, pos=(10, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldActivationMode, pos=(10, 1), flag=wx.TOP, border=3)
		sizer.Add(Call_Number, pos=(11, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldCallNumb, pos=(11, 1), flag=wx.TOP, border=3)
		# Buttons
		sizer.Add(self.SendEcall, pos=(13, 0), flag=wx.BOTTOM, border=3)
		#ecall cannot be stopped sizer.Add(self.StopEcall, pos=(13, 1), flag=wx.BOTTOM, border=3)

		panel.SetSizer(sizer)
		MSD_StaticBoxSizer.Add(panel, 0, wx.ALL, 1)
		self.SetSizer(MSD_StaticBoxSizer)
		
		# IHM initialization with data from saved file
		try:
			saveConf = shelve.open("save\\save.dat")
			self.FieldVIN.SetValue(saveConf["VIN"])
			self.FieldNbPass.SetSelection(int(saveConf["NbPass"]))
			self.FieldCurLat.SetValue(saveConf["CurLat"].decode('utf-8'))
			self.FieldEW.SetSelection(int(saveConf["EW"]))
			self.FieldCurLong.SetValue(saveConf["CurLong"].decode('utf-8'))
			self.FieldNS.SetSelection(int(saveConf["NS"]))
			self.FieldCurDir.SetValue(saveConf["CurDir"])
			self.FieldConfid.SetSelection(int(saveConf["Confid"]))
			self.FieldPS.SetSelection(int(saveConf["PS"]))
			self.FieldVT.SetSelection(int(saveConf["VT"]))
			self.FieldCallNumb.SetValue(saveConf["CallNumb"])
			saveConf.close()
		except IOError:
			print"IOerror !"
		except KeyError:
			print"Key error on save !"

	def SaveEcallInfo(self):
	
		try:
			saveConf = shelve.open("save\\save.dat")
			saveConf["VIN"] = str(self.FieldVIN.GetValue())
			saveConf["CurLat"] = str(self.FieldCurLat.GetValue().encode('utf-8'))
			saveConf["NbPass"] = str(self.FieldNbPass.GetSelection())
			saveConf["EW"] = str(self.FieldEW.GetSelection())
			saveConf["CurLong"] = str(self.FieldCurLong.GetValue().encode('utf-8'))
			saveConf["NS"] = str(self.FieldNS.GetSelection())
			saveConf["CurDir"] = str(self.FieldCurDir.GetValue())
			saveConf["Confid"] = str(self.FieldConfid.GetSelection())
			saveConf["PS"] = str(self.FieldPS.GetSelection())
			saveConf["VT"] = str(self.FieldVT.GetSelection())
			saveConf["CallNumb"] = str(self.FieldCallNumb.GetValue())
			saveConf.close()
		except IOError:
			print"IOError on create/open save.dat file ! "
			raise




################
# Elements Blocs  #
################
class ComAndSim(wx.Panel):
	def __init__(self, parent, enable=True):
		self.enable = enable
		wx.Panel.__init__(self,parent)
		# Create objects to display
		staticBox = wx.StaticBox(self, -1, "COM/SIM:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		panel = wx.Panel(self)
		COM_Label = wx.StaticText(panel, -1, "COM port:")
		if enable:
			list = self.__ReadComList()
			list.sort(self.sort_COM)
			self.COM = wx.Choice(panel,choices=list)
			if str("COM"+str(VarDemoTool.COM_Port)) in self.COM.GetStrings():
				self.COM.SetStringSelection(str("COM"+str(VarDemoTool.COM_Port)))
		else:
			self.COM = wx.TextCtrl(panel,size=(25,-1),value=VarDemoTool.COM_Port)
			self.COM.SetMaxLength(2)
		Speed_Label = wx.StaticText(panel, -1, "COM speed:")
		self.SpeedListBox = wx.Choice(panel,choices=VarDemoTool.SpeedList)
		self.SpeedListBox.SetStringSelection(VarDemoTool.COM_Speed)
		PinLabel = wx.StaticText(panel, label = "Pin CODE:")
		self.Pin = wx.TextCtrl(panel,size=(65,-1),value=VarDemoTool.SIM_PIN)
		self.Pin.SetMaxLength(8)
		
		if enable:
			# Event to catch USB COM Arrival/Remove
			self.GetParent().hookMsgHandler(self.__onDeviceArrival,self.__onDeviceRemove)
		else:
			ToolTip = "To modify those options please see Configuration menu"
			self.SetToolTip(wx.ToolTip(ToolTip))
			panel.SetToolTip(wx.ToolTip(ToolTip))
			COM_Label.SetToolTip(wx.ToolTip(ToolTip))
			Speed_Label.SetToolTip(wx.ToolTip(ToolTip))
			PinLabel.SetToolTip(wx.ToolTip(ToolTip))
		
		# Layout
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(COM_Label,pos=(0,0),flag=wx.TOP,border=3)
		sizer.Add(self.COM,(0,1))
		sizer.Add(Speed_Label,pos=(0,2),flag=wx.TOP,border=3)
		sizer.Add(self.SpeedListBox,(0,3))
		sizer.Add(PinLabel,pos=(1,0),flag=wx.TOP,border=3)
		sizer.Add(self.Pin,pos=(1,1),span=(1,2),flag=wx.EXPAND)
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
		
		# Enable or not
		self.Enable(enable)
	
	def sort_COM(self,COMx,COMy):
		x=int(COMx.split("COM")[1])
		y=int(COMy.split("COM")[1])
		
		if x>y:
			return 1
		if x==y:
			return 0
		if x<y:
			return -1
	
	def __ReadComList(self):
		port = []
		SERIALCOMM_Find = False
		
		key = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\DEVICEMAP',0, _winreg.KEY_READ)
		keyNb = _winreg.QueryInfoKey(key)[0]
		for index in range(keyNb):
			if _winreg.EnumKey(key, index) == "SERIALCOMM":
				SERIALCOMM_Find = True
				break
		_winreg.CloseKey(key)

		if SERIALCOMM_Find:
			key = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\DEVICEMAP\SERIALCOMM',0, _winreg.KEY_READ)
			try:
				ValueNb = _winreg.QueryInfoKey(key)[1]
				for i in range(ValueNb):
					port.append(_winreg.EnumValue(key,i)[1])
				_winreg.CloseKey(key)
			except:
				_winreg.CloseKey(key)
		return port
	
	def __onDeviceArrival(self,Name):
		#print "Arrival",Name
		list = self.COM.GetStrings()+[Name]
		list.sort(self.sort_COM)
		sav = self.COM.GetStringSelection()
		self.COM.Clear()
		for elem in list:
			self.COM.Append(elem)
		self.COM.SetStringSelection(sav)
	
	def __onDeviceRemove(self,Name):
		#print "Remove",Name
		if Name == self.COM.GetStringSelection():
			self.COM.SetStringSelection(self.COM.GetStrings()[0])
		self.COM.Delete(self.COM.FindString(Name))
	
	# Set COM and SIM values
	def SetValues(self,COM_Port,COM_Speed,PIN_Code):
		self.COM.SetValue(COM_Port)
		self.SpeedListBox.SetStringSelection(COM_Speed)
		self.Pin.SetValue(PIN_Code)
	
	# Enable Input field
	def Enable(self,state=True):
		self.COM.Enable(state)
		self.SpeedListBox.Enable(state)
		self.Pin.Enable(state)
	
	# Test if all field are fielded
	def AllFielded(self):
		if self.enable:
			return self.COM.GetStringSelection()!="" and self.SpeedListBox.GetStringSelection()!=""
		else:
			return self.COM.GetValue()!="" and self.SpeedListBox.GetStringSelection()!=""

class GPRS(wx.Panel):
	def __init__(self, parent, enable=True):
		wx.Panel.__init__(self,parent)
		
		# Create objects to display
		staticBox = wx.StaticBox(self, -1, "GPRS:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		panel = wx.Panel(self)
		APN_Label = wx.StaticText(panel, -1, "APN:",size=(47,-1))
		self.APN = wx.TextCtrl(panel,value=VarDemoTool.GPRS_APN)
		Login_Label = wx.StaticText(panel, -1, "Login:")
		self.Login = wx.TextCtrl(panel,value=VarDemoTool.GPRS_Login)
		Password_Label = wx.StaticText(panel, label = "Password:")
		self.Password = wx.TextCtrl(panel,value=VarDemoTool.GPRS_Password)
		
		if not(enable):
			ToolTip = "To modify those options please see Configuration menu"
			self.SetToolTip(wx.ToolTip(ToolTip))
			panel.SetToolTip(wx.ToolTip(ToolTip))
			APN_Label.SetToolTip(wx.ToolTip(ToolTip))
			Login_Label.SetToolTip(wx.ToolTip(ToolTip))
			Password_Label.SetToolTip(wx.ToolTip(ToolTip))
		
		# Layout
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(APN_Label,pos=(0,0),flag=wx.TOP,border=3)
		sizer.Add(self.APN,pos=(0,1),span=(1,3),flag=wx.EXPAND)
		sizer.Add(Login_Label,pos=(1,0),flag=wx.TOP,border=3)
		sizer.Add(self.Login,pos=(1,1))
		sizer.Add(Password_Label,pos=(1,2),flag=wx.TOP,border=3)
		sizer.Add(self.Password,pos=(1,3),flag=wx.ALIGN_CENTER)
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
		
		# Enable or not
		self.Enable(enable)
	
	# Set GPRS values
	def SetValues(self,GPRS_APN,GPRS_Login,GPRS_Password):
		self.APN.SetValue(GPRS_APN)
		self.Login.SetValue(GPRS_Login)
		self.Password.SetValue(GPRS_Password)
	
	# Enable Input field
	def Enable(self,state=True):
		self.APN.Enable(state)
		self.Login.Enable(state)
		self.Password.Enable(state)
	
	# Test if all field are fielded
	def AllFielded(self):
		return self.APN.GetValue()!=""

class FTP(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		staticBox = wx.StaticBox(self, -1, "FTP:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		panel = wx.Panel(self)
		ServeurPanel = wx.Panel(panel)
		Address_Label = wx.StaticText(ServeurPanel, -1, "URL/IP:",size=(42,-1))
		self.URL = wx.TextCtrl(ServeurPanel,size=(186,-1),value=VarDemoTool.FTP_URL)
		self.URL.SetToolTip(wx.ToolTip("Enter your FTP address"))
		Port_Label = wx.StaticText(ServeurPanel, -1, "Port:")
		self.FTPPort = wx.TextCtrl(ServeurPanel,size=(40,-1),value=VarDemoTool.FTP_Port)
		self.FTPPort.SetToolTip(wx.ToolTip("Enter your FTP port number"))
		self.FTPPort.SetMaxLength(4)
		Login_Label = wx.StaticText(panel, -1, "Login:")
		self.Login = wx.TextCtrl(panel,value=VarDemoTool.FTP_Login)
		self.Login.SetToolTip(wx.ToolTip("Enter your FTP Login"))
		Password_Label = wx.StaticText(panel, label = "Password:")
		self.Password = wx.TextCtrl(panel,value=VarDemoTool.FTP_Password)
		self.Password.SetToolTip(wx.ToolTip("Enter your FTP Password"))
		FTPUplaod_Label = wx.StaticText(panel, -1, "Upload (from PC):")
		font = FTPUplaod_Label.GetFont()
		font.SetUnderlined(True)
		FTPUplaod_Label.SetFont(font)
		FTPPathToSend_Label = wx.StaticText(panel, -1, "FTP path:")
		self.FTPPathTosend = wx.TextCtrl(panel,value=VarDemoTool.FTP_UplaodPath)
		self.FTPPathTosend.SetToolTip(wx.ToolTip("Enter your FTP path where uplaod your file"))
		FileToSend_Label = wx.StaticText(panel, -1, "File:")
		self.FileToSend = wx.TextCtrl(panel,value=VarDemoTool.FTP_UplaodFile,style=wx.TE_READONLY)
		self.FileToSend.SetToolTip(wx.ToolTip("Enter the file to upload on FTP"))
		self.FileToSend.SetInsertionPointEnd()
		self.OpenFileButton = wx.Button(panel,-1,"...",size=(22,17))
		FTPDownlaod_Label = wx.StaticText(panel, -1, "Download (from PC):")
		font = FTPDownlaod_Label.GetFont()
		font.SetUnderlined(True)
		FTPDownlaod_Label.SetFont(font)
		FTPPathToRcv_Label = wx.StaticText(panel, -1, "FTP path:")
		self.FTPPathToReceive = wx.TextCtrl(panel,value=VarDemoTool.FTP_DownlaodPath)
		self.FTPPathToReceive.SetToolTip(wx.ToolTip("Enter your FTP path where is your file"))
		FileToRcv_Label = wx.StaticText(panel, -1, "File name:")
		self.FileToReceive = wx.TextCtrl(panel,value=VarDemoTool.FTP_DownlaodFile)
		self.FileToReceive.SetToolTip(wx.ToolTip("Enter the name file you want to download"))
		
		# Layout
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		Box = wx.BoxSizer(wx.HORIZONTAL)
		Box.Add(Address_Label,0,wx.TOP|wx.RIGHT,3)
		Box.Add(self.URL,0,wx.LEFT|wx.RIGHT,7)
		Box.Add(Port_Label,0,wx.RIGHT|wx.TOP,3)
		Box.Add(self.FTPPort,0)
		ServeurPanel.SetSizer(Box)
		sizer.Add(ServeurPanel,pos=(0,0),span=(1,4),flag=wx.EXPAND)
		sizer.Add(Login_Label,pos=(1,0),flag=wx.TOP,border=3)
		sizer.Add(self.Login,pos=(1,1))
		sizer.Add(Password_Label,pos=(1,2),flag=wx.TOP,border=3)
		sizer.Add(self.Password,pos=(1,3),flag=wx.ALIGN_CENTER)
		sizer.Add(wx.StaticLine(panel),pos=(2,0),span=(1,5),flag=wx.EXPAND)
		sizer.Add(FTPUplaod_Label,pos=(3,2),span=(1,3),flag=wx.EXPAND)
		sizer.Add(FTPPathToSend_Label,pos=(4,2),flag=wx.TOP,border=3)
		sizer.Add(self.FTPPathTosend,pos=(4,3))
		sizer.Add(FileToSend_Label,pos=(5,2),flag=wx.TOP,border=3)
		sizer.Add(self.FileToSend,pos=(5,3))
		sizer.Add(self.OpenFileButton,pos=(5,4),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
		sizer.Add(FTPDownlaod_Label,pos=(3,0),span=(1,2),flag=wx.EXPAND)
		sizer.Add(FTPPathToRcv_Label,pos=(4,0),flag=wx.TOP,border=3)
		sizer.Add(self.FTPPathToReceive,pos=(4,1))
		sizer.Add(FileToRcv_Label,pos=(5,0),flag=wx.TOP,border=3)
		sizer.Add(self.FileToReceive,pos=(5,1))
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnOpenFile, self.OpenFileButton)	# When Clic on Open File Button
	
	def __OnOpenFile(self,evt):
		dlg = wx.FileDialog(self, 
							message="Open File",
							defaultDir=os.getcwd(), 
							defaultFile="", 
							wildcard="*.*",
							style=wx.OPEN|wx.FD_FILE_MUST_EXIST)
		
		if dlg.ShowModal() == wx.ID_OK:
			self.FileToSend.SetValue(dlg.GetPath())
			self.FileToSend.SetInsertionPointEnd()
		dlg.Destroy()
	
	# Test if all upload field are fielded
	def AllUplaodFielded(self):
		return self.URL.GetValue()!="" and self.FTPPort.GetValue()!="" and self.Login.GetValue()!="" and self.Password.GetValue()!="" and self.FileToSend.GetValue()!=""	#self.FTPPathTosend.GetValue()!="" and 
	
	# Test if all download field are fielded
	def AllDownlaodFielded(self):
		return self.URL.GetValue()!="" and self.FTPPort.GetValue()!="" and self.Login.GetValue()!="" and self.Password.GetValue()!="" and self.FileToReceive.GetValue()!=""	#self.FTPPathToReceive.GetValue()!="" and 

class TCP(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		ServeurPanel = wx.Panel(self)
		Address_Label = wx.StaticText(ServeurPanel, -1, "URL/IP:")
		self.URL = wx.TextCtrl(ServeurPanel,size=(186,-1),value=VarDemoTool.TCP_URL)
		self.URL.SetToolTip(wx.ToolTip("Enter your TCP address"))
		Port_Label = wx.StaticText(ServeurPanel, -1, "Port:")
		self.TCPPort = wx.TextCtrl(ServeurPanel,size=(40,-1),value=VarDemoTool.TCP_Port)
		self.TCPPort.SetToolTip(wx.ToolTip("Enter your TCP port number"))
		self.TCPPort.SetMaxLength(4)
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "TCP:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		Box = wx.BoxSizer(wx.HORIZONTAL)
		Box.Add(Address_Label,0,wx.TOP|wx.RIGHT,3)
		Box.Add(self.URL,0,wx.LEFT|wx.RIGHT,7)
		Box.Add(Port_Label,0,wx.RIGHT|wx.TOP,3)
		Box.Add(self.TCPPort,0)
		ServeurPanel.SetSizer(Box)
		StaticBoxSizer.Add(ServeurPanel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
	
	# Test if all field are fielded
	def AllFielded(self):
		return self.URL.GetValue()!="" and self.TCPPort.GetValue()!=""

class SMS(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		panel = wx.Panel(self)
		Number_Label = wx.StaticText(panel, -1, "Dial Number:")
		self.Number = wx.TextCtrl(panel,value=VarDemoTool.SMS_Number)
		self.Number.SetToolTip(wx.ToolTip("Enter the phone number to send SMS"))
		self.IRA = wx.RadioButton(panel,-1,'IRA',style=wx.RB_GROUP)
		self.UCS2  = wx.RadioButton(panel,-1,'UCS2')
		Text_Label = wx.StaticText(panel, -1, "Text:")
		self.Text = wx.TextCtrl(panel,size=(270,200),value=VarDemoTool.SMS_Text, style=wx.TE_MULTILINE|wx.TE_WORDWRAP)
		self.Text.SetToolTip(wx.ToolTip("Enter the SMS text"))
		self.Text.SetMaxLength(160)
		
		# temp hide IRA and UCS2 cause HILO UCS2 pb
		self.IRA.Hide()
		self.UCS2.Hide()
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "SMS:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(Number_Label,pos=(0,0),flag=wx.TOP,border=3)
		sizer.Add(self.Number,pos=(0,1))
		sizer.Add(self.IRA,pos=(0,3),flag=wx.TOP,border=3)
		sizer.Add(self.UCS2,pos=(0,4),flag=wx.TOP,border=3)
		sizer.Add(Text_Label,pos=(1,0),flag=wx.TOP,border=3)
		sizer.Add(self.Text,pos=(1,1),span=(1,5))
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
	
	# Test if all field are fielded
	def AllFielded(self):
		return self.Number.GetValue()!="" and self.Text.GetValue()!=""

class VoiceCall(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		panel = wx.Panel(self)
		Number_Label = wx.StaticText(panel, -1, "Dial Number:")
		self.Number = wx.TextCtrl(panel,value=VarDemoTool.VoiceCall_Number)
		self.Number.SetToolTip(wx.ToolTip("Enter the phone number to dial"))
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "Voice Call:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(Number_Label,pos=(0,0),flag=wx.TOP,border=3)
		sizer.Add(self.Number,pos=(0,1))
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
	
	# Test if all field are fielded
	def AllFielded(self):
		return self.Number.GetValue()!=""

class MUX(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		staticBox = wx.StaticBox(self, -1, "MUX:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		panel = wx.Panel(self)
		ServeurPanel = wx.Panel(panel)
		Address_Label = wx.StaticText(ServeurPanel, -1, "URL/IP:",size=(42,-1))
		self.URL = wx.TextCtrl(ServeurPanel,size=(186,-1),value=VarDemoTool.FTP_URL)
		Port_Label = wx.StaticText(ServeurPanel, -1, "Port:")
		self.FTPPort = wx.TextCtrl(ServeurPanel,size=(40,-1),value=VarDemoTool.FTP_Port)
		self.FTPPort.SetMaxLength(4)
		Login_Label = wx.StaticText(panel, -1, "Login:")
		self.Login = wx.TextCtrl(panel,value=VarDemoTool.FTP_Login)
		Password_Label = wx.StaticText(panel, label = "Password:")
		self.Password = wx.TextCtrl(panel,value=VarDemoTool.FTP_Password)
		'''FTPUplaod_Label = wx.StaticText(panel, -1, "Upload (from PC):")
		font = FTPUplaod_Label.GetFont()
		font.SetUnderlined(True)
		FTPUplaod_Label.SetFont(font)
		FTPPathToSend_Label = wx.StaticText(panel, -1, "FTP path:")
		self.FTPPathTosend = wx.TextCtrl(panel,value=VarDemoTool.FTP_UploadPath)
		FileToSend_Label = wx.StaticText(panel, -1, "File:")
		self.FileToSend = wx.TextCtrl(panel,value=VarDemoTool.FTP_UplaodFile,style=wx.TE_READONLY)
		self.FileToSend.SetInsertionPointEnd()
		self.OpenFileButton = wx.Button(panel,-1,"...",size=(22,17))
		'''
		FTPDownlaod_Label = wx.StaticText(panel, -1, "Download (from PC):")
		font = FTPDownlaod_Label.GetFont()
		font.SetUnderlined(True)
		FTPDownlaod_Label.SetFont(font)
		FTPPathToRcv_Label = wx.StaticText(panel, -1, "FTP path:")
		self.FTPPathToReceive = wx.TextCtrl(panel,value=VarDemoTool.FTP_DownlaodPath)
		FileToRcv_Label = wx.StaticText(panel, -1, "File name:")
		self.FileToReceive = wx.TextCtrl(panel,value=VarDemoTool.FTP_DownlaodFile)
		
		# Layout
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		Box = wx.BoxSizer(wx.HORIZONTAL)
		Box.Add(Address_Label,0,wx.TOP|wx.RIGHT,3)
		Box.Add(self.URL,0,wx.LEFT|wx.RIGHT,7)
		Box.Add(Port_Label,0,wx.RIGHT|wx.TOP,3)
		Box.Add(self.FTPPort,0)
		ServeurPanel.SetSizer(Box)
		sizer.Add(ServeurPanel,pos=(0,0),span=(1,4),flag=wx.EXPAND)
		sizer.Add(Login_Label,pos=(1,0),flag=wx.TOP,border=3)
		sizer.Add(self.Login,pos=(1,1))
		sizer.Add(Password_Label,pos=(1,2),flag=wx.TOP,border=3)
		sizer.Add(self.Password,pos=(1,3),flag=wx.ALIGN_CENTER)
		sizer.Add(wx.StaticLine(panel),pos=(2,0),span=(1,5),flag=wx.EXPAND)
		'''sizer.Add(FTPUplaod_Label,pos=(3,0),span=(1,5),flag=wx.EXPAND)
		sizer.Add(FTPPathToSend_Label,pos=(4,0),flag=wx.TOP,border=3)
		sizer.Add(self.FTPPathTosend,pos=(4,1))
		sizer.Add(FileToSend_Label,pos=(4,2),flag=wx.TOP,border=3)
		sizer.Add(self.FileToSend,pos=(4,3))
		sizer.Add(self.OpenFileButton,pos=(4,4),flag=wx.ALIGN_CENTER_VERTICAL|wx.ALIGN_LEFT)
		'''
		sizer.Add(FTPDownlaod_Label,pos=(5,0),span=(1,5),flag=wx.EXPAND)
		sizer.Add(FTPPathToRcv_Label,pos=(6,0),flag=wx.TOP,border=3)
		sizer.Add(self.FTPPathToReceive,pos=(6,1))
		sizer.Add(FileToRcv_Label,pos=(6,2),flag=wx.TOP,border=3)
		sizer.Add(self.FileToReceive,pos=(6,3))
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
		
		# Events
		#self.Bind(wx.EVT_BUTTON, self.__OnOpenFile, self.OpenFileButton)	# When Clic on Open File Button
	
	def __OnOpenFile(self,evt):
		dlg = wx.FileDialog(self, 
							message="Open File",
							defaultDir=os.getcwd(), 
							defaultFile="", 
							wildcard="*.*",
							style=wx.OPEN|wx.FD_FILE_MUST_EXIST)
		
		if dlg.ShowModal() == wx.ID_OK:
			self.FileToSend.SetValue(dlg.GetPath())
			self.FileToSend.SetInsertionPointEnd()
		dlg.Destroy()
	
	# Test if all upload field are fielded
	def AllUplaodFielded(self):
		return self.URL.GetValue()!="" and self.FTPPort.GetValue()!="" and self.Login.GetValue()!="" and self.Password.GetValue()!="" and self.FTPPathTosend.GetValue()!="" and self.FileToSend.GetValue()!=""
	
	# Test if all download field are fielded
	def AllDownlaodFielded(self):
		return self.URL.GetValue()!="" and self.FTPPort.GetValue()!="" and self.Login.GetValue()!="" and self.Password.GetValue()!="" and self.FTPPathToReceive.GetValue()!="" and self.FileToReceive.GetValue()!=""

class GPIO(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		panel = wx.Panel(self)
		self.Input = wx.RadioButton(panel,-1,'Input',style=wx.RB_GROUP,name='Input')
		self.Input.SetToolTip(wx.ToolTip("Set GPIO as input"))
		self.Input.SetValue(False)
		self.Output  = wx.RadioButton(panel,-1,'Output',name='Output')
		self.Output.SetToolTip(wx.ToolTip("Set GPIO as output"))
		ChoicePanel = wx.Panel(panel,style=wx.BORDER_SIMPLE )
		self.GPIO1 = wx.CheckBox(ChoicePanel,wx.NewId(),"GPIO 1",name="GPIO")
		self.GPIO1.SetToolTip(wx.ToolTip("State of GPIO 1"))
		self.GPIO2 = wx.CheckBox(ChoicePanel,wx.NewId(),"GPIO 2",name="GPIO")
		self.GPIO2.SetToolTip(wx.ToolTip("State of GPIO 2"))
		self.GPIO3 = wx.CheckBox(ChoicePanel,wx.NewId(),"GPIO 3",name="GPIO")
		self.GPIO3.SetToolTip(wx.ToolTip("State of GPIO 3"))
		self.GPIO4 = wx.CheckBox(ChoicePanel,wx.NewId(),"GPIO 4",name="GPIO")
		self.GPIO4.SetToolTip(wx.ToolTip("State of GPIO 4"))
		self.GPIO5 = wx.CheckBox(ChoicePanel,wx.NewId(),"GPIO 5",name="GPIO")
		self.GPIO5.SetToolTip(wx.ToolTip("State of GPIO 5"))
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "GPIO:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.GPIO1, 0,wx.TOP|wx.LEFT|wx.RIGHT,5)
		Box.Add(self.GPIO2, 0,wx.TOP|wx.LEFT|wx.RIGHT,5)
		Box.Add(self.GPIO3, 0,wx.TOP|wx.LEFT|wx.RIGHT,5)
		Box.Add(self.GPIO4, 0,wx.TOP|wx.LEFT|wx.RIGHT,5)
		Box.Add(self.GPIO5, 0,wx.ALL,5)
		ChoicePanel.SetSizer(Box)
		sizer.Add(self.Input,pos=(0,0))
		sizer.Add(self.Output,pos=(1,0))
		sizer.Add(ChoicePanel,pos=(2,0),flag=wx.TOP,border=3)
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
	
	def OutputSelected(self):
		return self.Output.GetValue()

class FileSystem(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		panel = wx.Panel(self)
		WriteTitle_Label = wx.StaticText(panel, -1, "Write a File to HILO File System:")
		font = WriteTitle_Label.GetFont()
		font.SetUnderlined(True)
		WriteTitle_Label.SetFont(font)
		WriteFileName_Label = wx.StaticText(panel, -1, "File name (on HILO):")
		self.WriteFileName = wx.TextCtrl(panel,size=(186,-1),value=VarDemoTool.FS_WriteName)
		self.WriteFileName.SetToolTip(wx.ToolTip("Enter the file name store on HILO"))
		WriteFile_Label = wx.StaticText(panel, -1, "File to send:")
		self.WriteFile = wx.TextCtrl(panel,size=(186,-1),value=VarDemoTool.FS_WriteFile,style=wx.TE_READONLY)
		self.WriteFile.SetToolTip(wx.ToolTip("Enter the file to send on HILO"))
		self.WriteFile.SetInsertionPointEnd()
		self.FileToSendButton = wx.Button(panel,-1,"...",size=(22,17))
		ReadTitle_Label = wx.StaticText(panel, -1, "Read a File from HILO File System:")
		font = ReadTitle_Label.GetFont()
		font.SetUnderlined(True)
		ReadTitle_Label.SetFont(font)
		ReadFile_Label = wx.StaticText(panel, -1, "File name (on HILO):")
		self.ReadFile = wx.TextCtrl(panel,size=(186,-1),value=VarDemoTool.FS_ReadName)
		self.ReadFile.SetToolTip(wx.ToolTip("Enter the file name on HILO to read"))
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "File System:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(WriteTitle_Label,pos=(0,0),span=(1,3),flag=wx.EXPAND)
		sizer.Add(WriteFileName_Label,pos=(1,0),flag=wx.TOP,border=3)
		sizer.Add(self.WriteFileName,pos=(1,1))
		sizer.Add(WriteFile_Label,pos=(2,0),flag=wx.TOP,border=3)
		sizer.Add(self.WriteFile,pos=(2,1))
		sizer.Add(self.FileToSendButton,pos=(2,2))
		sizer.Add(wx.StaticLine(panel),pos=(3,0),span=(1,3),flag=wx.EXPAND)
		sizer.Add(ReadTitle_Label,pos=(4,0),span=(1,3),flag=wx.EXPAND)
		sizer.Add(ReadFile_Label,pos=(5,0),flag=wx.TOP,border=3)
		sizer.Add(self.ReadFile,pos=(5,1))
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnOpenFile, self.FileToSendButton)	# When Clic on Open File Button
	
	def __OnOpenFile(self,evt):
		
		dlg = wx.FileDialog(self, 
							message="Open File",
							defaultDir=os.getcwd(), 
							defaultFile="", 
							wildcard="*.*",
							style=wx.OPEN|wx.FD_FILE_MUST_EXIST)
		
		if dlg.ShowModal() == wx.ID_OK:
			if int(str(os.path.getsize(dlg.GetPath())))/1048576.0 > 1:
				dlg = wx.MessageDialog(None, "Maximum file size is 1Mo","File size too big" ,wx.ICON_ERROR)
				dlg.ShowModal()
			else:
				self.WriteFile.SetValue(dlg.GetPath())
				self.WriteFile.SetInsertionPointEnd()
		dlg.Destroy()
	
	# Test if all write field are fielded
	def AllWriteFielded(self):
		return self.WriteFile.GetValue()!="" and self.WriteFileName.GetValue()!=""
	
	# Test if all read field are fielded
	def AllReadFielded(self):
		return self.ReadFile.GetValue()!=""

class SMTP(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		panel = wx.Panel(self)
		Server_Label = wx.StaticText(panel, -1, "SMTP server:")
		self.Server = wx.TextCtrl(panel,size=(186,-1),value=VarDemoTool.SMTP_Server)
		self.Server.SetToolTip(wx.ToolTip("Enter the SMTP server address"))
		Email_Label = wx.StaticText(panel, -1, "SMTP email:")
		self.Email = wx.TextCtrl(panel,size=(186,-1),value=VarDemoTool.SMTP_Email)
		self.Email.SetToolTip(wx.ToolTip("Enter the SMTP email"))
		Login_Label = wx.StaticText(panel, -1, "SMTP login:")
		self.Login =wx.TextCtrl(panel,size=(186,-1),value=VarDemoTool.SMTP_Login)
		self.Login.SetToolTip(wx.ToolTip("Enter the SMTP loging"))
		PassWord_Label = wx.StaticText(panel, -1, "SMTP password:")
		self.PassWord =wx.TextCtrl(panel,size=(186,-1),value=VarDemoTool.SMTP_PassWord)
		self.PassWord.SetToolTip(wx.ToolTip("Enter the SMTP password"))
		To_Label = wx.StaticText(panel, -1, "To:")
		self.To = wx.TextCtrl(panel,size=(186,-1),value=VarDemoTool.SMTP_To)
		self.To.SetToolTip(wx.ToolTip("Enter the email address to send your email"))
		Subject_Label = wx.StaticText(panel, -1, "Subject:")
		self.Subject = wx.TextCtrl(panel,size=(186,-1),value=VarDemoTool.SMTP_Subject)
		self.Subject.SetToolTip(wx.ToolTip("Enter the subject of your email"))
		Text_Label = wx.StaticText(panel, -1, "Text:")
		self.Text = wx.TextCtrl(panel,size=(270,200),value=VarDemoTool.SMTP_Text, style=wx.TE_MULTILINE|wx.TE_WORDWRAP)
		self.Text.SetToolTip(wx.ToolTip("Enter the text of your email"))
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "SMTP:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(Server_Label,pos=(0,0),flag=wx.TOP,border=3)
		sizer.Add(self.Server,pos=(0,1))
		sizer.Add(Email_Label,pos=(1,0),flag=wx.TOP,border=3)
		sizer.Add(self.Email,pos=(1,1))
		sizer.Add(Login_Label,pos=(2,0),flag=wx.TOP,border=3)
		sizer.Add(self.Login,pos=(2,1))
		sizer.Add(PassWord_Label,pos=(3,0),flag=wx.TOP,border=3)
		sizer.Add(self.PassWord,pos=(3,1))
		sizer.Add(wx.StaticLine(panel),pos=(4,0),span=(1,3),flag=wx.EXPAND)
		sizer.Add(To_Label,pos=(5,0),flag=wx.TOP,border=3)
		sizer.Add(self.To,pos=(5,1))
		sizer.Add(Subject_Label,pos=(6,0),flag=wx.TOP,border=3)
		sizer.Add(self.Subject,pos=(6,1))
		sizer.Add(Text_Label,pos=(7,0),flag=wx.TOP,border=3)
		sizer.Add(self.Text,pos=(7,1))
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
	
	# Test if all field are fielded
	def AllFielded(self):
		return self.Server.GetValue()!="" and self.Email.GetValue()!="" and self.To.GetValue()!=""

class Environment_Module(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		panel = wx.Panel(self)
		panel2 = wx.Panel(panel)
		IMEI_Label = wx.StaticText(panel2, -1, "IMEI:")
		self.IMEI = wx.TextCtrl(panel2,style=wx.TE_READONLY,size=(105,-1))
		self.IMEI.SetToolTip(wx.ToolTip("Display the module IMEI"))
		SoftVersion_Label = wx.StaticText(panel2, -1, "Soft Version:")
		self.SoftVersion = wx.TextCtrl(panel2,style=wx.TE_READONLY,size=(115,-1))
		self.SoftVersion.SetToolTip(wx.ToolTip("Display the Soft Version"))
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "Module:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		Box = wx.BoxSizer(wx.HORIZONTAL)
		Box.Add(IMEI_Label,0,wx.LEFT|wx.TOP,3)
		Box.Add(self.IMEI,0,wx.LEFT|wx.RIGHT,2)
		Box.Add(SoftVersion_Label,0,wx.LEFT|wx.RIGHT|wx.TOP,3)
		Box.Add(self.SoftVersion,0,wx.LEFT|wx.RIGHT,2)
		panel2.SetSizer(Box)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(panel2,pos=(0,0),span=(1,2), flag=wx.TOP,border=3)
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)

class Environment_SIM(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		panel = wx.Panel(self)
		IMSI_Label = wx.StaticText(panel, -1, "IMSI:")
		self.IMSI = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(105,-1))
		self.IMSI.SetToolTip(wx.ToolTip("Display the module IMSI"))
		HPLMN_Label = wx.StaticText(panel, -1, "HPLMN:")
		self.HPLMN = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.HPLMN.SetToolTip(wx.ToolTip("Display the Home PLMN"))
		FPLMN_Label = wx.StaticText(panel, -1, "Forbiden PLMN:")
		self.FPLMN1 = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.FPLMN1.SetToolTip(wx.ToolTip("Display the Forbiden PLMN"))
		self.FPLMN2 = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.FPLMN2.SetToolTip(wx.ToolTip("Display the Forbiden PLMN"))
		self.FPLMN3 = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.FPLMN3.SetToolTip(wx.ToolTip("Display the Forbiden PLMN"))
		self.FPLMN4 = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.FPLMN4.SetToolTip(wx.ToolTip("Display the Forbiden PLMN"))
		PPLMN_Label = wx.StaticText(panel, -1, "Prefer PLMN:")
		self.PPLMN1 = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.PPLMN1.SetToolTip(wx.ToolTip("Display the Prefer PLMN"))
		self.PPLMN2 = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.PPLMN2.SetToolTip(wx.ToolTip("Display the Prefer PLMN"))
		self.PPLMN3 = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.PPLMN3.SetToolTip(wx.ToolTip("Display the Prefer PLMN"))
		self.PPLMN4 = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.PPLMN4.SetToolTip(wx.ToolTip("Display the Prefer PLMN"))
		self.PPLMN5 = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.PPLMN5.SetToolTip(wx.ToolTip("Display the Prefer PLMN"))
		self.PPLMN6 = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.PPLMN6.SetToolTip(wx.ToolTip("Display the Prefer PLMN"))
		self.PPLMN7 = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.PPLMN7.SetToolTip(wx.ToolTip("Display the Prefer PLMN"))
		self.PPLMN8 = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(50,-1))
		self.PPLMN8.SetToolTip(wx.ToolTip("Display the Prefer PLMN"))
		ICCIdentification_Label = wx.StaticText(panel, -1, "ICC Identification:")
		self.ICCIdentification = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(133,-1))
		self.ICCIdentification.SetToolTip(wx.ToolTip("Display the ICC Identification"))
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "SIM:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(IMSI_Label,pos=(0,0),flag=wx.TOP,border=3)
		sizer.Add(self.IMSI,pos=(0,1),span=(1,2))
		sizer.Add(HPLMN_Label,pos=(0,3),flag=wx.TOP,border=3)
		sizer.Add(self.HPLMN,pos=(0,4),span=(1,3))
		sizer.Add(wx.StaticLine(panel),pos=(1,0),span=(1,7),flag=wx.EXPAND)
		sizer.Add(FPLMN_Label,pos=(2,0),flag=wx.TOP,border=3)
		sizer.Add(self.FPLMN1,pos=(2,1),flag=wx.EXPAND)
		sizer.Add(self.FPLMN2,pos=(2,2))
		sizer.Add(self.FPLMN3,pos=(2,3))
		sizer.Add(self.FPLMN4,pos=(2,4))
		sizer.Add(wx.StaticLine(panel),pos=(3,0),span=(1,7),flag=wx.EXPAND)
		sizer.Add(PPLMN_Label,pos=(4,0),span=(2,1),flag=wx.TOP|wx.ALIGN_CENTER_VERTICAL,border=3)
		sizer.Add(self.PPLMN1,pos=(4,1))
		sizer.Add(self.PPLMN2,pos=(4,2))
		sizer.Add(self.PPLMN3,pos=(4,3))
		sizer.Add(self.PPLMN4,pos=(4,4))
		sizer.Add(self.PPLMN5,pos=(5,1))
		sizer.Add(self.PPLMN6,pos=(5,2))
		sizer.Add(self.PPLMN7,pos=(5,3))
		sizer.Add(self.PPLMN8,pos=(5,4))
		sizer.Add(wx.StaticLine(panel),pos=(6,0),span=(1,7),flag=wx.EXPAND)
		sizer.Add(ICCIdentification_Label,pos=(7,0),flag=wx.TOP,border=3)
		sizer.Add(self.ICCIdentification,pos=(7,1),span=(1,3))
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
	
	def DecodePLMN(self,PLMN):
		from VarGlobal import PLMN_dict
		if PLMN == "":
			return ""
		else:
			return str(PLMN_dict.get(int("".join(PLMN[i+1]+PLMN[i] for i in range(0,len(PLMN),2)).replace("F","")),"UNKNOWN"))
	
	def Update_PLMN_ToolTip(self):
		self.HPLMN.SetToolTip(wx.ToolTip("Display the Home PLMN : "+self.DecodePLMN(self.HPLMN.GetValue())))
		self.FPLMN1.SetToolTip(wx.ToolTip("Display the Forbiden PLMN : "+self.DecodePLMN(self.FPLMN1.GetValue())))
		self.FPLMN2.SetToolTip(wx.ToolTip("Display the Forbiden PLMN : "+self.DecodePLMN(self.FPLMN2.GetValue())))
		self.FPLMN3.SetToolTip(wx.ToolTip("Display the Forbiden PLMN : "+self.DecodePLMN(self.FPLMN3.GetValue())))
		self.FPLMN4.SetToolTip(wx.ToolTip("Display the Forbiden PLMN : "+self.DecodePLMN(self.FPLMN4.GetValue())))
		self.PPLMN1.SetToolTip(wx.ToolTip("Display the Prefer PLMN : "+self.DecodePLMN(self.PPLMN1.GetValue())))
		self.PPLMN2.SetToolTip(wx.ToolTip("Display the Prefer PLMN : "+self.DecodePLMN(self.PPLMN2.GetValue())))
		self.PPLMN3.SetToolTip(wx.ToolTip("Display the Prefer PLMN : "+self.DecodePLMN(self.PPLMN3.GetValue())))
		self.PPLMN4.SetToolTip(wx.ToolTip("Display the Prefer PLMN : "+self.DecodePLMN(self.PPLMN4.GetValue())))
		self.PPLMN5.SetToolTip(wx.ToolTip("Display the Prefer PLMN : "+self.DecodePLMN(self.PPLMN5.GetValue())))
		self.PPLMN6.SetToolTip(wx.ToolTip("Display the Prefer PLMN : "+self.DecodePLMN(self.PPLMN6.GetValue())))
		self.PPLMN7.SetToolTip(wx.ToolTip("Display the Prefer PLMN : "+self.DecodePLMN(self.PPLMN7.GetValue())))
		self.PPLMN8.SetToolTip(wx.ToolTip("Display the Prefer PLMN : "+self.DecodePLMN(self.PPLMN8.GetValue())))

class Environment_RF(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		panel = wx.Panel(self)
		OPName_Label = wx.StaticText(panel, -1, "Operator Name:")
		self.OPName = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(105,-1),)
		self.OPName.SetToolTip(wx.ToolTip("Display the Operator Name"))
		self.Roaming = wx.CheckBox(panel,label="Roaming:",style=wx.ALIGN_RIGHT|wx.CHK_2STATE)
		self.Roaming.SetToolTip(wx.ToolTip("Display if in Roaming or not"))
		FieldLvl_Label = wx.StaticText(panel, -1, "Field level:")
		self.FieldLvl = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(54,-1))
		self.FieldLvl.SetToolTip(wx.ToolTip("Display the receive field level"))
		PowerBand_Label = wx.StaticText(panel, -1, "Frequency Band:")
		self.PowerBand = wx.TextCtrl(panel,style=wx.TE_READONLY,size=(130,-1))
		self.PowerBand.SetToolTip(wx.ToolTip("Display the PowerBand"))
		KCELL_Label = wx.StaticText(panel, -1, "neighbourhood cells:")
		font = KCELL_Label.GetFont()
		font.SetUnderlined(True)
		KCELL_Label.SetFont(font)
		self.KCELL = TableList(panel,(335,122), ["N","ARFCN","BSIC","PLMN","LAC","Cell ID","RSSI","TA"], [27,49,38,48,50,50,39,30])
		self.KCELL.SetToolTip(wx.ToolTip("Display neighbourhood cells"))
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "RF:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(OPName_Label,pos=(0,0), flag=wx.TOP,border=3)
		sizer.Add(self.OPName,pos=(0,1),span=(1,2))
		sizer.Add(self.Roaming,pos=(0,3), flag=wx.RIGHT|wx.TOP,border=3)
		sizer.Add(FieldLvl_Label,pos=(1,0),flag=wx.TOP,border=3)
		sizer.Add(self.FieldLvl,pos=(1,1))
		sizer.Add(PowerBand_Label,pos=(1,2),flag=wx.TOP,border=3)
		sizer.Add(self.PowerBand,pos=(1,3))
		sizer.Add(KCELL_Label,pos=(2,0),span=(1,5))
		sizer.Add(self.KCELL,pos=(3,0),span=(1,5),flag=wx.EXPAND)
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
		
		self.Bind(wx.EVT_CHECKBOX,self.__OnSelect,self.Roaming)
		
	def __OnSelect(self, evt):
		self.Roaming.SetValue(not evt.IsChecked())
	
	def clear(self):
		self.KCELL.DeleteAllItems()

class Environment_PhoneBook(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		panel = wx.Panel(self)
		self.PhoneBook = TableList(panel, (335,120), ["Id","Name","Number"], [27,157,130])
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "PhoneBook:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		#sizer.Add(PhoneBook_Label,pos=(0,0),span=(1,7))
		sizer.Add(self.PhoneBook,pos=(0,0),span=(1,7),flag=wx.EXPAND)
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
	
	def clear(self):
		self.PhoneBook.DeleteAllItems()

class Environment_SMS(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		panel = wx.Panel(self)
		self.SMS = TableList(panel, (335,120), ["Id","Status","From","Name","Date", "Time"], [27,90,90,130,59,78])
		self.TextSMS = wx.TextCtrl(panel,style=wx.TE_READONLY|wx.TE_MULTILINE,size=(-1, 80))
		self.TextSMS.SetToolTip(wx.ToolTip("Display Text SMS selected in list"))
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "SMS on SIM:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(self.SMS,pos=(0,0),span=(1,7),flag=wx.EXPAND)
		sizer.Add(self.TextSMS,pos=(1,0),span=(1,7),flag=wx.EXPAND)
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
		
		self.Bind(wx.EVT_LIST_ITEM_SELECTED,self.__OnSMSSelected,self.SMS)
		self.Bind(wx.EVT_LIST_ITEM_DESELECTED,self.__OnSMSDeselected,self.SMS)
	
	def clear(self):
		self.SMS.DeleteAllItems()
		self.TextSMS.SetValue("")
	
	def __OnSMSSelected(self,evt):
		self.TextSMS.SetValue(VarDemoTool.SMSOnSIM[evt.GetIndex()][6])
	
	def __OnSMSDeselected(self, evt):
		self.TextSMS.SetValue("")

class Environment_Alarm(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		panel = wx.Panel(self)
		Alarm_Label = wx.StaticText(panel, -1, "Set Alarm in:")
		self.Hours = wx.SpinCtrl(panel,min=0,max=24,size=(42,-1))
		self.Hours.SetToolTip(wx.ToolTip("Set Hour alarm"))
		Hours_Label = wx.StaticText(panel, -1, "h")
		self.Minutes = wx.SpinCtrl(panel,min=1,max=59,size=(42,-1),initial=1)
		self.Minutes.SetToolTip(wx.ToolTip("Set Minutes alarm"))
		Minutes_Label = wx.StaticText(panel, -1, "m")
		self.Seconds = wx.SpinCtrl(panel,min=0,max=59,size=(42,-1))
		self.Seconds.SetToolTip(wx.ToolTip("Set seconds alarm"))
		Seconds_Label = wx.StaticText(panel, -1, "s")
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "Alarm:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(Alarm_Label,pos=(0,0), flag=wx.TOP,border=3)
		sizer.Add(self.Hours,pos=(0,1))
		sizer.Add(Hours_Label,pos=(0,2), flag=wx.TOP,border=3)
		sizer.Add(self.Minutes,pos=(0,3))
		sizer.Add(Minutes_Label,pos=(0,4), flag=wx.TOP,border=3)
		sizer.Add(self.Seconds,pos=(0,5))
		sizer.Add(Seconds_Label,pos=(0,6), flag=wx.TOP,border=3)
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)

class AT_Terminal(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		MainSizer = wx.BoxSizer(wx.VERTICAL)
		InterfacePanel = self.Interface_LayoutPanel(self)
		MainSizer.Add(InterfacePanel)
		StatePanel = self.State_LayoutPanel(self)
		MainSizer.Add(StatePanel,0,wx.CENTER)
		RawPanel = self.Raw_LayoutPanel(self)
		MainSizer.Add(RawPanel)
		SendPanel = self.Send_LayoutPanel(self)
		MainSizer.Add(SendPanel)
		self.SetSizer(MainSizer)
		
		self.Enable(False)
		# Events
		self.GetParent().GetParent().GetParent().hookMsgHandler(self.__onDeviceArrival,self.__onDeviceRemove)	# To detect Insert/remove Serial/USB converter
		self.Bind(wx.EVT_BUTTON, self.__OnOpenFile, self.OpenFileButton)				# When Clic on Open file Button
		self.Bind(wx.EVT_CHECKBOX,self.__OnSelect)										# When Clic on IN CheckBox
	
	def __OnSelect(self, evt):
		checkBox = self.FindWindowById(evt.GetId())
		if checkBox.GetParent().GetName() == 'IN Signal':	# only in case of IN checkBox
			checkBox.SetValue(not evt.IsChecked())
		else:
			evt.Skip()
	
	def __OnOpenFile(self,evt):
		dlg = wx.FileDialog(self, 
							message="Open File",
							defaultDir=os.getcwd(), 
							defaultFile="", 
							wildcard="*.*",
							style=wx.OPEN|wx.FD_FILE_MUST_EXIST)
		
		if dlg.ShowModal() == wx.ID_OK:
			self.RawFile.SetValue(dlg.GetPath())
			self.RawFile.SetInsertionPointEnd()
		dlg.Destroy()
		evt.Skip()
	
	def Interface_LayoutPanel(self,parent):
		# Create objects to display
		MainInterfacePanel = wx.Panel(parent)
		PanelCOM = wx.Panel(MainInterfacePanel)
		COM_Label = wx.StaticText(PanelCOM, -1, "Port:")
		list = self.__ReadComList()
		list.sort(self.sort_COM)
		self.COM = wx.Choice(PanelCOM,choices=list,name="Com port")
		if str("COM"+VarDemoTool.COM_Port) in self.COM.GetStrings():		# if save COM port is avaible
			self.COM.SetStringSelection(str("COM"+VarDemoTool.COM_Port))
		else:
			self.COM.SetStringSelection(self.COM.GetStrings()[0])
		Speed_Label = wx.StaticText(PanelCOM, -1, "Speed:")
		self.SpeedListBox = wx.Choice(PanelCOM,choices=VarDemoTool.SpeedList,name="speed")
		self.SpeedListBox.SetStringSelection(VarDemoTool.COM_Speed)
		self.OpenButton = wx.Button(PanelCOM, -1, "Open",name="Open")
		FlowControl_Label = wx.StaticText(PanelCOM, -1, "Flow\r\nControl:")
		self.FlowControlListBox = wx.Choice(PanelCOM,choices=["None","Hardware","Software"],name="flow control")
		self.FlowControlListBox.SetStringSelection("None")
		
		# Layout
		InterfaceStaticBox = wx.StaticBox(MainInterfacePanel, -1, "Interface:")
		InterfaceStaticBoxSizer = wx.StaticBoxSizer(InterfaceStaticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(COM_Label,pos=(0,0),flag=wx.TOP,border=3)
		sizer.Add(self.COM,(0,1))
		sizer.Add(Speed_Label,pos=(0,2),flag=wx.TOP,border=3)
		sizer.Add(self.SpeedListBox,(0,3))
		sizer.Add(FlowControl_Label,pos=(0,4),flag=wx.TOP,border=-3)
		sizer.Add(self.FlowControlListBox,(0,5))
		sizer.Add(self.OpenButton,(1,0),span=(1,7),flag=wx.ALIGN_CENTER_HORIZONTAL)
		PanelCOM.SetSizer(sizer)
		InterfaceStaticBoxSizer.Add(PanelCOM,0,wx.ALL,5)
		MainInterfacePanel.SetSizer(InterfaceStaticBoxSizer)
		return MainInterfacePanel
	
	def State_LayoutPanel(self,parent):
		self.MainStatePanel = wx.Panel(parent)
		COM_States_StaticBox = wx.StaticBox(self.MainStatePanel, -1, "Communication States")
		COM_States_StaticBoxSizer = wx.StaticBoxSizer(COM_States_StaticBox,wx.VERTICAL)
		StatePanel = wx.Panel(self.MainStatePanel)
		GenSizer = wx.BoxSizer(wx.HORIZONTAL)
		panel = self.Left_LayoutPanel(StatePanel)
		GenSizer.Add(panel)
		IN_Panel = self.IN_LayoutPanel(StatePanel)
		GenSizer.Add(IN_Panel,0,wx.LEFT,5)
		StatePanel.SetSizer(GenSizer)
		COM_States_StaticBoxSizer.Add(StatePanel,0,wx.ALL,5)
		self.MainStatePanel.SetSizer(COM_States_StaticBoxSizer)
		return self.MainStatePanel
		
	def Left_LayoutPanel(self,parent):
		panel = wx.Panel(parent)
		panelSizer = wx.BoxSizer(wx.VERTICAL)
		
		OUT_Panel = self.OUT_LayoutPanel(panel)
		panelSizer.Add(OUT_Panel,0,wx.BOTTOM,9)
		############
		self.BREAK = wx.CheckBox(panel,wx.NewId(),"Break",name="BREAK")
		panelSizer.Add(self.BREAK,0,wx.LEFT,10)
		panel.SetSizer(panelSizer)
		
		return panel
	
	def OUT_LayoutPanel(self,parent):
		OUT_Panel0 = wx.Panel(parent)
		
		OUT_Panel = wx.Panel(OUT_Panel0)
		
		self.RTS = wx.CheckBox(OUT_Panel,wx.NewId(),"RTS",name="RTS")
		self.DTR = wx.CheckBox(OUT_Panel,wx.NewId(),"DTR",name="DTR")
		
		self.RTS.SetValue(True)
		self.DTR.SetValue(True)
		
		OUT_StaticBox = wx.StaticBox(OUT_Panel0, -1, "OUT")
		OUT_StaticBoxSizer = wx.StaticBoxSizer(OUT_StaticBox,wx.VERTICAL)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.RTS,0,wx.BOTTOM,3)
		sizer.Add(self.DTR)
		OUT_Panel.SetSizer(sizer)
		
		OUT_StaticBoxSizer.Add(OUT_Panel,0,wx.ALL,5)
		OUT_Panel0.SetSizer(OUT_StaticBoxSizer)
		
		return OUT_Panel0
	
	def IN_LayoutPanel(self,parent):
		IN_Panel0 = wx.Panel(parent)
		
		IN_Panel = wx.Panel(IN_Panel0,name="IN Signal")
		
		self.CTS = wx.CheckBox(IN_Panel,wx.NewId(),"CTS",name="CTS")
		self.DSR = wx.CheckBox(IN_Panel,wx.NewId(),"DSR",name="DSR")
		self.RI = wx.CheckBox(IN_Panel,wx.NewId(),"RING/RI",name="RI")
		self.DCD = wx.CheckBox(IN_Panel,wx.NewId(),"RLSD/DCD",name="DCD")
		
		IN_StaticBox = wx.StaticBox(IN_Panel0, -1, "IN")
		IN_StaticBoxSizer = wx.StaticBoxSizer(IN_StaticBox,wx.VERTICAL)
		
		sizer = wx.BoxSizer(wx.VERTICAL)
		sizer.Add(self.CTS,0,wx.BOTTOM,3)
		sizer.Add(self.DSR,0,wx.BOTTOM,3)
		sizer.Add(self.RI,0,wx.BOTTOM,3)
		sizer.Add(self.DCD)
		IN_Panel.SetSizer(sizer)
		
		IN_StaticBoxSizer.Add(IN_Panel,0,wx.ALL,5)
		IN_Panel0.SetSizer(IN_StaticBoxSizer)
		
		return IN_Panel0
	
	def Raw_LayoutPanel(self,parent):
		# Create objects to display
		self.MainRawPanel = wx.Panel(parent)
		Panel = wx.Panel(self.MainRawPanel)
		self.RawFile = wx.TextCtrl(Panel,size=(273,-1),style=wx.TE_READONLY)
		self.OpenFileButton = wx.Button(Panel, -1, "...",size=(22,21))
		self.SendRawButton = wx.Button(Panel, -1, "Send",size=(30,21))
		
		# Layout
		InterfaceStaticBox = wx.StaticBox(self.MainRawPanel, -1, "Raw file send")
		InterfaceStaticBoxSizer = wx.StaticBoxSizer(InterfaceStaticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(self.RawFile,pos=(0,0))
		sizer.Add(self.OpenFileButton,(0,1))
		sizer.Add(self.SendRawButton,(0,2))
		Panel.SetSizer(sizer)
		InterfaceStaticBoxSizer.Add(Panel,0,wx.ALL,5)
		self.MainRawPanel.SetSizer(InterfaceStaticBoxSizer)
		return self.MainRawPanel
	
	def Send_LayoutPanel(self,parent):
		# Create objects to display
		self.MainSendPanel = wx.Panel(parent)
		Panel = wx.Panel(self.MainSendPanel)
		self.AT_Command = wx.ComboBox(Panel,value="ATE1V1&K3+CMEE=1",choices = [],size=(230,-1),style=wx.TE_PROCESS_ENTER,name="AT_Command")
		self.SendLineButton = wx.Button(Panel, -1, "Send Line",size=(55,21))
		self.SendButton = wx.Button(Panel, -1, "Send",size=(40,21))
		
		self.Bind(wx.EVT_TEXT_ENTER,self.__OnComboBox,self.AT_Command)
		self.Bind(wx.EVT_BUTTON,self.__OnComboBox,self.SendLineButton)
		self.Bind(wx.EVT_BUTTON,self.__OnComboBox,self.SendButton)
		
		# Layout
		InterfaceStaticBox = wx.StaticBox(self.MainSendPanel, -1, "Send AT Command")
		InterfaceStaticBoxSizer = wx.StaticBoxSizer(InterfaceStaticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(self.AT_Command,pos=(0,0))
		sizer.Add(self.SendLineButton,(0,1))
		sizer.Add(self.SendButton,(0,2))
		Panel.SetSizer(sizer)
		InterfaceStaticBoxSizer.Add(Panel,0,wx.ALL,5)
		self.MainSendPanel.SetSizer(InterfaceStaticBoxSizer)
		return self.MainSendPanel
	
	def __OnComboBox(self,evt):
		items = self.AT_Command.GetItems()
		command = self.AT_Command.GetValue()
		if command in items:
			index = items.index(command)
			self.AT_Command.Delete(index)
			self.AT_Command.SetValue(command)
		self.AT_Command.Insert(command,0)
		self.AT_Command.SetMark(0,-1)
		evt.Skip()
	
	def sort_COM(self,COMx,COMy):
		x=int(COMx.split("COM")[1])
		y=int(COMy.split("COM")[1])
		
		if x>y:
			return 1
		if x==y:
			return 0
		if x<y:
			return -1
	
	def __ReadComList(self):
		port = []
		SERIALCOMM_Find = False
		
		key = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\DEVICEMAP',0, _winreg.KEY_READ)
		keyNb = _winreg.QueryInfoKey(key)[0]
		for index in range(keyNb):
			if _winreg.EnumKey(key, index) == "SERIALCOMM":
				SERIALCOMM_Find = True
				break
		_winreg.CloseKey(key)

		if SERIALCOMM_Find:
			key = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\DEVICEMAP\SERIALCOMM',0, _winreg.KEY_READ)
			ValueNb = _winreg.QueryInfoKey(key)[1]
			for i in range(ValueNb):
				port.append(_winreg.EnumValue(key,i)[1])
			_winreg.CloseKey(key)
		return port
	
	def __onDeviceArrival(self,Name):
		#print "Arrival",Name
		list = self.COM.GetStrings()+[Name]
		list.sort(self.sort_COM)
		sav = self.COM.GetStringSelection()
		self.COM.Clear()
		for elem in list:
			self.COM.Append(elem)
		self.COM.SetStringSelection(sav)
	
	def __onDeviceRemove(self,Name):
		#print "Remove",Name
		if Name == self.COM.GetStringSelection():
			self.COM.SetStringSelection(self.COM.GetStrings()[0])
		self.COM.Delete(self.COM.FindString(Name))
	
	def Enable(self,State):
		if State:
			self.OpenButton.SetLabel("Close")
		else:
			self.OpenButton.SetLabel("Open")
		self.COM.Enable(not State)
		#self.SpeedListBox.Enable(not State)
		#self.FlowControlListBox.Enable(not State)
		self.MainStatePanel.Enable(State)
		self.MainRawPanel.Enable(State)
		self.MainSendPanel.Enable(State)
	
	def SetValues(self,COM_Port,COM_Speed,PIN_Code):
		pass

class FOTA_PDU(wx.Panel):
	def __init__(self, parent, id=-1):
		wx.Panel.__init__(self,parent, id)
		
		# Create objects to display
		panel = wx.Panel(self)
		PDU_Send_Label = wx.StaticText(panel, -1, "PDU File to Send:")
		self.PDU_File = wx.TextCtrl(panel,size=(186,-1),value=VarDemoTool.PDU_File,style=wx.TE_READONLY)
		self.PDU_File.SetToolTip(wx.ToolTip("Enter the PDU file to send"))
		self.PDU_File.SetInsertionPointEnd()
		self.FileToSendButton = wx.Button(panel,-1,"...",size=(22,17))
		
		# Layout
		staticBox = wx.StaticBox(self, -1, "Send PDU:")
		StaticBoxSizer = wx.StaticBoxSizer(staticBox,wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5,vgap=5)
		sizer.Add(PDU_Send_Label,pos=(0,0),flag=wx.TOP,border=3)
		sizer.Add(self.PDU_File,pos=(0,1))
		sizer.Add(self.FileToSendButton,pos=(0,2),flag=wx.TOP,border=3)
		panel.SetSizer(sizer)
		StaticBoxSizer.Add(panel,0,wx.ALL,5)
		self.SetSizer(StaticBoxSizer)
		
		# Events
		self.Bind(wx.EVT_BUTTON, self.__OnOpenFile, self.FileToSendButton)	# When Clic on Open File Button
	
	def __OnOpenFile(self,evt):
		
		dlg = wx.FileDialog(self, 
							message="Open PDU File",
							defaultDir=os.getcwd(), 
							defaultFile="", 
							wildcard="*.*",
							style=wx.OPEN|wx.FD_FILE_MUST_EXIST)
		
		if dlg.ShowModal() == wx.ID_OK:
			self.PDU_File.SetValue(dlg.GetPath())
			self.PDU_File.SetInsertionPointEnd()
		dlg.Destroy()
	
	# Test if all field are fielded
	def AllFielded(self):
		return self.PDU_File.GetValue()!=""


class GNSS_Page(wx.Panel):
	''' Coordonnées satellite '''
	def  __init__(self, parent, ide= -1):
		wx.Panel.__init__(self, parent, ide, name="GNSS")

		# Create objects to display
		self.ComAndSim = ComAndSim(self, False)
#		self.GNSS = GNSS(self)
		self.GNSS_Infos = GNSS_Infos(self)
		self.GNSS_SNR = GNSS_SNR(self)
		self.GNSS_Alt = GNSS_Alt(self)

		self.HelpButton = wx.Button(self, -1, "?", size=(25, 25), name="Help")
		
		#ajout Mai 2012
		self.NmeaOnly = wx.CheckBox(self, -1,"    NMEA trames only", (-1, -1),(-1, -1), style=wx.CHK_2STATE)
		self.Bind(wx.EVT_CHECKBOX, self.__OnCheck, self.NmeaOnly)
		# Layout
		Box = wx.BoxSizer(wx.VERTICAL)
		Box.Add(self.ComAndSim, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
#		Box.Add(self.GNSS, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

		Box.Add(self.NmeaOnly,0,wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
		Box.Add(self.GNSS_Infos, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
		Box.Add(self.GNSS_SNR, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)
		Box.Add(self.GNSS_Alt, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 5)

		# help button
		Box.Add((10, 10), 1)
		Box.Add(self.HelpButton, 0, wx.LEFT | wx.BOTTOM | wx.ALIGN_BOTTOM | wx.ALIGN_LEFT, 5)
		self.SetSizer(Box)

	def __OnCheck(self,evt):
		VarDemoTool.CheckNMEA = False
		if self.NmeaOnly.IsChecked():
			VarDemoTool.CheckNMEA = True
			wx.MessageBox("If you check this case, you have to send the AT messages to init the hardware !")

	def __OnSend(self, evt):
		''' Event on start gps reception '''
		StartScript(self, evt.GetId())

	def __OnStop(self, evt):
		''' Event on stop gps reception '''
		StartScript(self, evt.GetId())

	# Text to display in Help Dialog
	def Help(self):
		''' Help '''
		text = ["Version: "+VERSION+"\r\n"
				"This page allow you to make a satellite detection\r\n",
				"To start this application, you have to click the green satellite icon on the toolbar.\r\n",
				"To stop this application, you have to click the red satellite icon on the toolbar.\r\n"]
		return  '\r\n'.join(text)


class GNSS(wx.Panel):
	''' Panel for AT comands executed '''
	def __init__(self, parent, ide= -1):
		wx.Panel.__init__(self, parent, ide)

		# Create objects to display
		panel = wx.Panel(self)
		AT_Comand_Run = wx.StaticText(panel, -1, "Start:............AT+KGNSSRUN=1")
		AT_Comand_UART = wx.StaticText(panel, -1, "UART config:...AT+KUARTCFG=1")
		AT_Comand_FIX = wx.StaticText(panel, -1, "Fix:..............AT+KGNSSFIX=2,0")
		AT_Comand_NMEA = wx.StaticText(panel, -1, "Reception :.....AT+KNMEARCV=1")
		AT_Comand_Stop = wx.StaticText(panel, -1, "Stop :...........AT+KGNSSRUN=0")

		# Layout
		staticBox = wx.StaticBox(self, -1, "Send AT Command:")
		GNSS_StaticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5, vgap=1)
		sizer.Add(AT_Comand_Run, pos=(0, 0), flag=wx.TOP, border=3)
		sizer.Add(AT_Comand_UART, pos=(1, 0), flag=wx.TOP, border=3)
		sizer.Add(AT_Comand_FIX, pos=(2, 0), flag=wx.TOP, border=3)
		sizer.Add(AT_Comand_NMEA, pos=(3, 0), flag=wx.TOP, border=3)
		sizer.Add(AT_Comand_Stop, pos=(4, 0), flag=wx.TOP, border=3)
		panel.SetSizer(sizer)
		GNSS_StaticBoxSizer.Add(panel, 0, wx.ALL, 5)
		self.SetSizer(GNSS_StaticBoxSizer)


class GNSS_Infos(wx.Panel):
	''' Infos satellite '''
	def __init__(self, parent, ide= -1):
		wx.Panel.__init__(self, parent, ide)

		# Create objects to display
		panel = wx.Panel(self)
		TTFF = wx.StaticText(panel, -1, " TTFF (Time To First Fix): ")
		self.FieldTTFF = wx.TextCtrl(panel, -1, "",name="FieldTTFF")
		HMS = wx.StaticText(panel, -1, " format: h:mm:ss.ss")
		SatInView = wx.StaticText(panel, -1, "Satellite(s) in view : ")
		self.FieldSatInView = wx.TextCtrl(panel, -1, "",name="FieldSatInView")
		SatUsed = wx.StaticText(panel, -1, "Satellite(s) used : ")
		self.FieldSatUsed = wx.TextCtrl(panel, -1, "",name="FieldSatUsed")
		TimeUTC = wx.StaticText(panel, -1, "Time UTC:              ")
		self.FieldTimeUTC = wx.TextCtrl(panel, -1, "",name="FieldTimeUTC")
		TUTC = wx.StaticText(panel, -1, " format: hh:mm:ss.sss")
		Longitude = wx.StaticText(panel, -1, "Longitude:              ")
		self.FieldLongitude = wx.TextCtrl(panel, -1, "",name="FieldLongitude", size=(120,20))
		Latitude = wx.StaticText(panel, -1, "Latitude:              ")
		self.FieldLatitude = wx.TextCtrl(panel, -1, "",name="FieldLatitude", size=(120,20))
		longi = wx.StaticText(panel, -1, " deg:min:sec    E/W")
		lati = wx.StaticText(panel, -1, " deg:min:sec    N/S")

		# Layout
		staticBox = wx.StaticBox(self, -1, "Infos satellites:")
		GNSS_StaticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5, vgap=1)
		sizer.Add(TTFF, pos=(0, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldTTFF, pos=(0, 1), flag=wx.TOP, border=3)
		sizer.Add(HMS, pos=(0, 2), flag=wx.TOP, border=3)
		sizer.Add(SatInView, pos=(1, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSatInView, pos=(1, 1), flag=wx.TOP, border=3)
		sizer.Add(SatUsed, pos=(2, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSatUsed, pos=(2, 1), flag=wx.TOP, border=3)
		sizer.Add(TimeUTC, pos=(3, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldTimeUTC, pos=(3, 1), flag=wx.TOP, border=3)
		sizer.Add(TUTC, pos=(3, 2), flag=wx.TOP, border=3)
		sizer.Add(Longitude, pos=(4, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldLongitude, pos=(4, 1), flag=wx.TOP, border=3)
		sizer.Add(Latitude, pos=(5, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldLatitude, pos=(5, 1), flag=wx.TOP, border=3)
		sizer.Add(longi, pos=(4, 2), flag=wx.TOP, border=3)
		sizer.Add(lati, pos=(5, 2), flag=wx.TOP, border=3)
		panel.SetSizer(sizer)
		GNSS_StaticBoxSizer.Add(panel, 0, wx.ALL, 5)
		self.SetSizer(GNSS_StaticBoxSizer)


class GNSS_SNR(wx.Panel):
	''' '''
	def __init__(self,parent, ide= -1):
		wx.Panel.__init__(self, parent, ide)

		# Create objects to display
		panel = wx.Panel(self)
		IDSat1 = wx.StaticText(panel, -1, " ID: ")
		self.FieldIDSat1 = wx.TextCtrl(panel, -1, "",name="FieldIDSat1", size = (25,20))
		self.FieldIDSat2 = wx.TextCtrl(panel, -1, "",name="FieldIDSat2", size = (25,20))
		self.FieldIDSat3 = wx.TextCtrl(panel, -1, "",name="FieldIDSat3", size = (25,20))
		self.FieldIDSat4 = wx.TextCtrl(panel, -1, "",name="FieldIDSat4", size = (25,20))
		self.FieldIDSat5 = wx.TextCtrl(panel, -1, "",name="FieldIDSat5", size = (25,20))
		self.FieldIDSat6 = wx.TextCtrl(panel, -1, "",name="FieldIDSat6", size = (25,20))

		IDSat2 = wx.StaticText(panel, -1, " ID: ")
		self.FieldIDSat7 = wx.TextCtrl(panel, -1, "",name="FieldIDSat7", size = (25,20))
		self.FieldIDSat8 = wx.TextCtrl(panel, -1, "",name="FieldIDSat8", size = (25,20))
		self.FieldIDSat9 = wx.TextCtrl(panel, -1, "",name="FieldIDSat9", size = (25,20))
		self.FieldIDSat10 = wx.TextCtrl(panel, -1, "",name="FieldIDSat10", size = (25,20))
		self.FieldIDSat11 = wx.TextCtrl(panel, -1, "",name="FieldIDSat11", size = (25,20))
		self.FieldIDSat12 = wx.TextCtrl(panel, -1, "",name="FieldIDSat12", size = (25,20))

		IDSat3 = wx.StaticText(panel, -1, " ID: ")
		self.FieldIDSat13 = wx.TextCtrl(panel, -1, "",name="FieldIDSat13", size = (25,20))
		self.FieldIDSat14 = wx.TextCtrl(panel, -1, "",name="FieldIDSat14", size = (25,20))
		self.FieldIDSat15 = wx.TextCtrl(panel, -1, "",name="FieldIDSat15", size = (25,20))
		self.FieldIDSat16 = wx.TextCtrl(panel, -1, "",name="FieldIDSat16", size = (25,20))
		self.FieldIDSat17 = wx.TextCtrl(panel, -1, "",name="FieldIDSat17", size = (25,20))
		self.FieldIDSat18 = wx.TextCtrl(panel, -1, "",name="FieldIDSat18", size = (25,20))

		IDSat4 = wx.StaticText(panel, -1, " ID: ")
		self.FieldIDSat19 = wx.TextCtrl(panel, -1, "",name="FieldIDSat19", size = (25,20))
		self.FieldIDSat20 = wx.TextCtrl(panel, -1, "",name="FieldIDSat20", size = (25,20))
		self.FieldIDSat21 = wx.TextCtrl(panel, -1, "",name="FieldIDSat21", size = (25,20))
		self.FieldIDSat22 = wx.TextCtrl(panel, -1, "",name="FieldIDSat22", size = (25,20))
		self.FieldIDSat23 = wx.TextCtrl(panel, -1, "",name="FieldIDSat23", size = (25,20))
		self.FieldIDSat24 = wx.TextCtrl(panel, -1, "",name="FieldIDSat24", size = (25,20))

		self.FieldIDSat1.SetMaxLength(2)
		self.FieldIDSat2.SetMaxLength(2)
		self.FieldIDSat3.SetMaxLength(2)
		self.FieldIDSat4.SetMaxLength(2)
		self.FieldIDSat5.SetMaxLength(2)
		self.FieldIDSat6.SetMaxLength(2)
		self.FieldIDSat7.SetMaxLength(2)
		self.FieldIDSat8.SetMaxLength(2)
		self.FieldIDSat9.SetMaxLength(2)
		self.FieldIDSat10.SetMaxLength(2)
		self.FieldIDSat11.SetMaxLength(2)
		self.FieldIDSat12.SetMaxLength(2)
		self.FieldIDSat13.SetMaxLength(2)
		self.FieldIDSat14.SetMaxLength(2)
		self.FieldIDSat15.SetMaxLength(2)
		self.FieldIDSat16.SetMaxLength(2)
		self.FieldIDSat17.SetMaxLength(2)
		self.FieldIDSat18.SetMaxLength(2)
		self.FieldIDSat19.SetMaxLength(2)
		self.FieldIDSat20.SetMaxLength(2)
		self.FieldIDSat21.SetMaxLength(2)
		self.FieldIDSat22.SetMaxLength(2)
		self.FieldIDSat23.SetMaxLength(2)
		self.FieldIDSat24.SetMaxLength(2)

		SnrSat1 = wx.StaticText(panel, -1, " SNR : ")
		self.FieldSnrSat1 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat1", size = (25,20))
		self.FieldSnrSat2 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat2", size = (25,20))
		self.FieldSnrSat3 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat3", size = (25,20))
		self.FieldSnrSat4 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat4", size = (25,20))
		self.FieldSnrSat5 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat5", size = (25,20))
		self.FieldSnrSat6 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat6", size = (25,20))

		SnrSat2 = wx.StaticText(panel, -1, " SNR : ")
		self.FieldSnrSat7 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat7", size = (25,20))
		self.FieldSnrSat8 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat8", size = (25,20))
		self.FieldSnrSat9 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat9", size = (25,20))
		self.FieldSnrSat10 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat10", size = (25,20))
		self.FieldSnrSat11 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat11", size = (25,20))
		self.FieldSnrSat12 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat12", size = (25,20))

		SnrSat3 = wx.StaticText(panel, -1, " SNR : ")
		self.FieldSnrSat13 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat13", size = (25,20))
		self.FieldSnrSat14 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat14", size = (25,20))
		self.FieldSnrSat15 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat15", size = (25,20))
		self.FieldSnrSat16 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat16", size = (25,20))
		self.FieldSnrSat17 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat17", size = (25,20))
		self.FieldSnrSat18 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat18", size = (25,20))

		SnrSat4 = wx.StaticText(panel, -1, " SNR : ")
		self.FieldSnrSat19 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat19", size = (25,20))
		self.FieldSnrSat20 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat20", size = (25,20))
		self.FieldSnrSat21 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat21", size = (25,20))
		self.FieldSnrSat22 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat22", size = (25,20))
		self.FieldSnrSat23 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat23", size = (25,20))
		self.FieldSnrSat24 = wx.TextCtrl(panel, -1, "",name="FieldSnrSat24", size = (25,20))

		self.FieldSnrSat1.SetMaxLength(2)
		self.FieldSnrSat2.SetMaxLength(2)
		self.FieldSnrSat3.SetMaxLength(2)
		self.FieldSnrSat4.SetMaxLength(2)
		self.FieldSnrSat5.SetMaxLength(2)
		self.FieldSnrSat6.SetMaxLength(2)
		self.FieldSnrSat7.SetMaxLength(2)
		self.FieldSnrSat8.SetMaxLength(2)
		self.FieldSnrSat9.SetMaxLength(2)
		self.FieldSnrSat10.SetMaxLength(2)
		self.FieldSnrSat11.SetMaxLength(2)
		self.FieldSnrSat12.SetMaxLength(2)
		self.FieldSnrSat13.SetMaxLength(2)
		self.FieldSnrSat14.SetMaxLength(2)
		self.FieldSnrSat15.SetMaxLength(2)
		self.FieldSnrSat16.SetMaxLength(2)
		self.FieldSnrSat17.SetMaxLength(2)
		self.FieldSnrSat18.SetMaxLength(2)
		self.FieldSnrSat19.SetMaxLength(2)
		self.FieldSnrSat20.SetMaxLength(2)
		self.FieldSnrSat21.SetMaxLength(2)
		self.FieldSnrSat22.SetMaxLength(2)
		self.FieldSnrSat23.SetMaxLength(2)
		self.FieldSnrSat24.SetMaxLength(2)

		GP_View = wx.StaticText(panel, -1, "GPS viewed (1-32)")
		GP_View.SetOwnForegroundColour("BLACK")
		GP_View.SetOwnBackgroundColour("PINK")

		GP_Used = wx.StaticText(panel, -1, "GPS used")
		GP_Used.SetOwnForegroundColour("BLACK")
		GP_Used.SetOwnBackgroundColour(wx.Colour(255,100,80))

		GL_View = wx.StaticText(panel, -1, "Glonass viewed (65-88)")
		GL_View.SetOwnForegroundColour("BLACK")
		GL_View.SetOwnBackgroundColour("LIGHT BLUE")

		GL_Used = wx.StaticText(panel, -1, "Glonass used")
		GL_Used.SetOwnForegroundColour("BLACK")
		GL_Used.SetOwnBackgroundColour(wx.Colour(61,146,216))

		# Layout
		staticBox = wx.StaticBox(self, -1, "SNR satellites:")
		GNSS_StaticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5, vgap=0)
		sizer.Add(IDSat1, pos=(0, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat1, pos=(1, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat2, pos=(2, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat3, pos=(3, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat4, pos=(4, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat5, pos=(5, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat6, pos=(6, 0), flag=wx.TOP, border=3)

		sizer.Add(SnrSat1, pos=(0, 1), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat1, pos=(1, 1), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat2, pos=(2, 1), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat3, pos=(3, 1), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat4, pos=(4, 1), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat5, pos=(5, 1), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat6, pos=(6, 1), flag=wx.TOP, border=3)

		sizer.Add(IDSat2, pos=(0, 3), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat7, pos=(1, 3), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat8, pos=(2, 3), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat9, pos=(3, 3), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat10, pos=(4, 3), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat11, pos=(5, 3), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat12, pos=(6, 3), flag=wx.TOP, border=3)

		sizer.Add(SnrSat2, pos=(0, 4), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat7, pos=(1, 4), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat8, pos=(2, 4), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat9, pos=(3, 4), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat10, pos=(4, 4), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat11, pos=(5, 4), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat12, pos=(6, 4), flag=wx.TOP, border=3)

		sizer.Add(IDSat3, pos=(0, 6), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat13, pos=(1, 6), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat14, pos=(2, 6), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat15, pos=(3, 6), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat16, pos=(4, 6), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat17, pos=(5, 6), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat18, pos=(6, 6), flag=wx.TOP, border=3)

		sizer.Add(SnrSat3, pos=(0, 7), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat13, pos=(1, 7), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat14, pos=(2, 7), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat15, pos=(3, 7), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat16, pos=(4, 7), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat17, pos=(5, 7), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat18, pos=(6, 7), flag=wx.TOP, border=3)

		sizer.Add(IDSat4, pos=(0, 9), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat19, pos=(1, 9), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat20, pos=(2, 9), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat21, pos=(3, 9), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat22, pos=(4, 9), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat23, pos=(5, 9), flag=wx.TOP, border=3)
		sizer.Add(self.FieldIDSat24, pos=(6, 9), flag=wx.TOP, border=3)

		sizer.Add(SnrSat4, pos=(0, 10), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat19, pos=(1, 10), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat20, pos=(2, 10), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat21, pos=(3, 10), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat22, pos=(4, 10), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat23, pos=(5, 10), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSnrSat24, pos=(6, 10), flag=wx.TOP, border=3)

		sizer.Add(GP_View, pos=(8, 0), span= (1,4), flag=wx.TOP, border=3)
		sizer.Add(GP_Used, pos=(9, 0), span= (1,2), flag=wx.TOP, border=3)

		sizer.Add(GL_View, pos=(8, 5), span= (1,5),flag=wx.TOP, border=3)
		sizer.Add(GL_Used, pos=(9, 5), span= (1,2),flag=wx.TOP, border=3)

		panel.SetSizer(sizer)
		GNSS_StaticBoxSizer.Add(panel, 0, wx.ALL, 1)
		self.SetSizer(GNSS_StaticBoxSizer)


class GNSS_Alt(wx.Panel):
	''' Altitude '''
	def __init__(self, parent, ide= -1):
		wx.Panel.__init__(self, parent, ide)
		
		# Create objects to display
		panel = wx.Panel(self)
		
		Alt = wx.StaticText(panel, -1, " Altitude(m): ")
		self.FieldAltitude = wx.TextCtrl(panel, -1, "",name="FieldAltitude")
		HDOP = wx.StaticText(panel, -1, " HDOP: ")
		self.FieldHDOP = wx.TextCtrl(panel, -1, "",name="HDOP")
		SOG = wx.StaticText(panel, -1, " Speed Over Ground(km/h): ")
		self.FieldSOG = wx.TextCtrl(panel, -1, "",name="FieldSOG")

		# Layout
		staticBox = wx.StaticBox(self, -1, "")
		GNSS_StaticBoxSizer = wx.StaticBoxSizer(staticBox, wx.VERTICAL)
		sizer = wx.GridBagSizer(hgap=5, vgap=0)

		sizer.Add(Alt, pos=(0, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldAltitude, pos=(0, 1), flag=wx.TOP, border=3)
		sizer.Add(HDOP, pos=(1, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldHDOP, pos=(1, 1), flag=wx.TOP, border=3)
		sizer.Add(SOG, pos=(2, 0), flag=wx.TOP, border=3)
		sizer.Add(self.FieldSOG, pos=(2, 1), flag=wx.TOP, border=3)

		panel.SetSizer(sizer)
		GNSS_StaticBoxSizer.Add(panel, 0, wx.ALL, 1)
		self.SetSizer(GNSS_StaticBoxSizer)


class TableList(wx.ListCtrl):
	def __init__(self, parent, size, ColumnsTitles, ColumnsSize):
		wx.ListCtrl.__init__(self, parent, size=size, style=wx.LC_REPORT|wx.LC_HRULES|wx.LC_VRULES)
		
		self.ColumnsNb = len(ColumnsTitles)
		for i in range(len(ColumnsTitles)):
			self.InsertColumn(i, ColumnsTitles[i])
		
		for i in range(len(ColumnsSize)):
			self.SetColumnWidth(i, ColumnsSize[i])
	
	def AddItem(self, items):
		''' Add an item in the list '''
		if type(items) == list and items != [] and type(items[0]) != list:
			items = [items]
		
		for elem in items:
			index = self.InsertStringItem(sys.maxint, elem[0])
			for i in range(1,min(self.ColumnsNb,len(elem))):
				self.SetStringItem(index, i, elem[i])


###########
# For Test  #
###########
if __name__ == '__main__':
	'''class TestFrame(wx.Frame,WndProcHookMixin):
		def __init__(self, parent, title):
			WndProcHookMixin.__init__(self)
			wx.Frame.__init__(self, parent, title=title)
			self.log_flag=False
			self.log_tc=sys.stdout
			Notebook(self)
			self.SetSize((410,600))
			self.Show()
	try:
		import traceback
		app = wx.PySimpleApp(redirect=True)
		frm = TestFrame(None, "Splitter Example")
		app.SetTopWindow(frm)
		#frm2 = ConfigurationDialog(None, "Splitter Example")
		app.MainLoop()
		#ReadConfigFile()
		#WriteConfigFile()
	except:
		traceback.print_exc (file=open('error.txt', 'w'))
	'''
	# start autotest
#	import os,sys

	import autotest
	sys.path.append(os.getcwd().rsplit("\\",1)[0])

	app = autotest.MyApp(False)
	app.MainLoop()
	