#!/usr/bin/env python
# _*_ coding: utf-8 _*_


#----------------------------------------------------------------------------
# Name:			MainFrame.py
#
# Goal:			Main MMI Window management
#
# Author:		refer below
#
# Version:		refer below
#
# Date:			refer below
#
# Property:		SagemComm
#----------------------------------------------------------------------------


#date              who                 version                 modification
#march 2009        Bingxun HOU         1.0                     creation
#2009              JM Ruffle           1.6.7                   modifications to create 1.6.7
#2009              JM Ruffle           1.7MUX                  modifications to create 1.7MUX (parallel branch)
#07-09-2011        JF Weiss            1.8                     merge 1.6 and 1.7 MUX versions
#07-09-2011        JF Weiss            1.8.1                   add comments and light modifications
#23-03-2012        JM Seillon          1.8.3                   change windows size for GNSS
#18-04-2012        JM Seillon          1.8.4                   Modification of the max and min main window size
#                                                              Add StartGNSS and StopGNSS icon in the Demo toolbar, with associated code OnStartGNSS and OnStopGNSS
#21-01-2015        RTN                 1.9.6.17                Support drap and drop 

import wx
import os
import images
import XmlTree
import cStringIO
import traceback
import VarGlobal
import Output
import VarDemoTool
import Histo
import subprocess

from AboutDlg     import AboutDlg
from Test         import Test
from ExcelDoc     import  ExcelDoc #,ExcelItem
from ProcList     import ProcList
from AddTestDlg   import AddTestDlg
from datetime     import datetime
from Mux0710Dlg   import DestroyDlg0710, openDlg07102
from ComModuleAPI import SafePrint, SagStopAllThread, SagPauseAllThread, SagContinueAllThread, SagCloseAll as SagCloseAllComPort, SagStopAllPort, SagReleaseAllComPort, print_mutex
from Output       import staticVariables as Output_staticVariables
from Mux0710Dlg   import ResetDisplayOfDCD_OnMuxDlg
from ComDetect    import WndProcHookMixin
from SubFrame     import Settings

if VarGlobal.DEMO_MODE:
	import InputDemoTool

##RTN Study - Begin
class FileDrop(wx.FileDropTarget):
    def __init__(self, window):
        wx.FileDropTarget.__init__(self)
        self.tree = window
        
        
    def OnDropFiles(self, x, y, filenames):       
        self.tree.OnAddTestByDrop(filenames)
        
        
        
        
##RTN Study - End
	

class MainFrame(wx.Frame, WndProcHookMixin):
	" main MMI window "
###########################

	def __init__(self, title, treelist, cfg, log_file, log_flag, list_test):
		" constructor ; WndProcHookMixin manages the COM port detection in real time. Used only in demo mode"
	###########################
		if VarGlobal.DEMO_MODE:
			WndProcHookMixin.__init__(self)
		wx.Frame.__init__(self, None, title=title, size=(950, 700), name="MainFrame")
		
		self.treelist = treelist
		self.cfg = cfg 
		self.log_file = log_file
		self.log_flag = log_flag
		self.list_test = list_test
		self.gui = True
		self.test = None
		
		self.ID_start_Menu = None
		self.ID_stop_Menu = None
		self.ID_start = None
		self.ID_stop = None
		self.ID_Config = None
		
		self.StartFlag = False
		self.PauseFlag = False
		self.ReleaseFlag = False
		self.MutexStatus = [True, True]
		
		self.NoteBook = None
		self.ID_startGNSS = wx.NewId()
		self.ID_stopGNSS = wx.NewId()
		
		# Set Icon 
		try:
			# Get the icon from file
			icon_chaine = images.get_sagem_iconData()
			icon_stream = cStringIO.StringIO(icon_chaine)
			LogoSagem = wx.BitmapFromImage(wx.ImageFromStream(icon_stream))
			icon = wx.IconFromBitmap(LogoSagem)
			self.SetIcon(icon)
#			self.SetIcon(LogoSagem)
			
			icon_stream.close()
			del icon_chaine, icon_stream
			
#			LogoSagem = wx.Bitmap("Logo.bmp",wx.BITMAP_TYPE_BMP)
#			icon = wx.IconFromBitmap(LogoSagem)
#			self.SetIcon(icon)
		except:
			pass
		
		# set the minimal size of the main window on the screen
		self.SetMinSize((640, 480))
		
		# The window is centered
		self.Centre(wx.BOTH)
		
		# Create menubar, menubar's menus, menus's items, toolbar, statusbar 
		self.menuBar = self.MakeMenuBar()
		self.SetMenuBar(self.menuBar)
		
		self.toolBar = self.CreateToolBar()
		self.statusBar = self.CreateStatusBar()
		
		# initialise MMI according to its type
		if VarGlobal.MODE == VarGlobal.DEMO_MODE:
			self.DemoMode_init()
		else:
			self.NormalMode_init()
		
		# event On Close
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindows)
		
		self.Show()
	
	def DemoMode_init(self):
		"MMI initialisation in case of demo mode"
	###########################
		# Create the panel above and below the right window
		self.rightPanel = wx.Panel(self, style=wx.BORDER_RAISED)
		
		if self.log_flag:
			log_file = self.log_file
		else:
			log_file = ""
		self.NoteBook = InputDemoTool.Notebook(self)
#		self.ID_startGNSS = wx.NewId()
#		self.ID_stopGNSS = wx.NewId()
		
		# above right panel
		self.log_tc = wx.TextCtrl(self.rightPanel, -1, style=wx.TE_MULTILINE | wx.TE_RICH | wx.TE_READONLY | wx.HSCROLL | wx.TE_NOHIDESEL)
		self.process_lc = ProcList(self.rightPanel, size=(-1, 200))
		self.label_log_tc = wx.StaticText(self.rightPanel, label="Messages")
		
		rightBox = wx.BoxSizer(wx.VERTICAL)
		rightBox.Add(self.label_log_tc, 0, wx.TOP | wx.CENTER, 5)
		rightBox.Add(self.log_tc, 1, wx.EXPAND)
		
		self.process_lc.Show(False)
		self.rightPanel.SetSizer(rightBox)
		
		self.process_lc.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleclickOnProcess_lc)
		Box = wx.BoxSizer(wx.HORIZONTAL)
		Box.Add(self.NoteBook, 0, wx.EXPAND)
		Box.Add(self.rightPanel, 1, wx.EXPAND)
		self.SetSizer(Box)
		self.Layout()
		
#		VarDemoTool.Histo = Histo.Histo(self, -1)
#		self.histo.Show()
	
	def NormalMode_init(self):
		"MMI initialisation in case of normal mode"	
	###########################
		# this instance allows to split the main window in 2 subwindows
		splitter = wx.SplitterWindow(self, -1, style=wx.CLIP_CHILDREN | wx.SP_LIVE_UPDATE | wx.SP_3D)
		
		# left panel creation
		leftPanel = wx.Panel(splitter)
		
		# right panel creation
		self.rightPanel = wx.Panel(splitter)
		
		# Display the list of config file and test files in left panel
		tID = wx.NewId() 
		self.tree = wx.TreeCtrl(leftPanel, tID, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT) 
		self.root = self.tree.AddRoot(self.treelist[0])
		for elem in self.treelist[1]:
			child = self.tree.AppendItem(self.root, elem[0])
			self.tree.SetPyData(child, None)
			self.display_test_tree(child, elem[1])
		
		#expand two first root elements
		firstChild = self.tree.GetFirstChild(self.root)
		self.tree.Expand(firstChild[0])
		
		self.tree.Expand(self.tree.GetNextChild(self.root, firstChild[1])[0])

		# left panel management and display
		leftBox = wx.BoxSizer(wx.VERTICAL)
		leftBox.Add(wx.StaticText(leftPanel, label="List Of Tests"), 0, wx.TOP | wx.CENTER, 5)
		leftBox.Add(self.tree, 1, wx.EXPAND)
		leftPanel.SetSizer(leftBox)

		# RTN : drap and drop
		dt = FileDrop(self)
		self.tree.SetDropTarget(dt)
		
		
		# above right panel management and display
		self.log_tc = wx.TextCtrl(self.rightPanel, -1, style=wx.TE_MULTILINE | wx.TE_RICH | wx.TE_READONLY | wx.HSCROLL | wx.TE_NOHIDESEL)
		self.process_lc = ProcList(self.rightPanel, size=(-1, 100))
		self.label_log_tc = wx.StaticText(self.rightPanel, label="Messages")
		
		#add a bow on right panel
		rightBox = wx.BoxSizer(wx.VERTICAL)
		rightBox.Add(self.label_log_tc, 0, wx.TOP | wx.CENTER, 5)
		rightBox.Add(self.log_tc, 1, wx.EXPAND)
		rightBox.Add(wx.StaticText(self.rightPanel, label="Process"), 0, wx.TOP | wx.CENTER, 5)
		rightBox.Add(self.process_lc, 0, wx.EXPAND)
		self.rightPanel.SetSizer(rightBox)
		
		self.process_lc.Bind(wx.EVT_LEFT_DCLICK, self.OnDoubleclickOnProcess_lc)
		
		# Set splitter 
		splitter.SplitVertically(leftPanel, self.rightPanel, 320)
		splitter.SetMinimumPaneSize(120)
	
	def OnCloseWindows(self, evt):
		"Close window event management"
	###########################
		DestroyDlg0710()
		if self.test != None:
			self.test.stop()
		SagStopAllThread(silent=True)
		SagCloseAllComPort(silent=True)
		self.timer2 = wx.Timer(self)
		self.Bind(wx.EVT_TIMER, self.kill)
		self.timer2.Start(500, True)
	
	def kill(self, evt):
		"Kill event management "
	###########################
		self.Destroy()
	
	def display_test_tree(self, father, list):
		" "
	###########################
		for elem in list:
			if type(elem) == type('string'):
				child = self.tree.AppendItem(father, elem)
				self.tree.SetPyData(child, None)
			else:
				child = self.tree.AppendItem(father, elem[0])
				self.tree.SetPyData(child, None)
				self.display_test_tree(child, elem[1])
	
	#############################
	# menu creation methods	#
	#############################
	def MakeMenuBar(self):
		" "
	###########################
		self.ID_Config = None
		if VarGlobal.MODE == VarGlobal.DEMO_MODE:
			return self.DemoMode_MenuBar()
		else:
			return self.NormalMode_MenuBar()
	
	def DemoMode_MenuBar(self):
		"This method manage sthe menu bar in case of demo mode"
	###########################
		# File menu creation
		menuFile = wx.Menu()
		self.itemLog = menuFile.Append(401, "Log", "Produce the log file or not", wx.ITEM_CHECK)
		itemExit = menuFile.Append(wx.ID_EXIT, "Exit", "Exit the software", wx.ITEM_NORMAL)
		if self.log_flag:
			self.itemLog.Check()
		
		# Configuration menu creation
		ConfigurationFile = wx.Menu()
		self.ID_Config = wx.NewId()
		self.itemConfig = ConfigurationFile.Append(self.ID_Config, "Configuration", "Configuration of Com, SIM and GPRS parameters", wx.ITEM_NORMAL)
		
		# menubar creation
		menuBar = wx.MenuBar()
		menuBar.Append(menuFile, 		 "File")
		menuBar.Append(ConfigurationFile, "Configuration")
		
		# bind events on the menu
		self.Bind(wx.EVT_MENU, self.OnClose, itemExit)
		self.Bind(wx.EVT_MENU, self.OnLog, 	  self.itemLog)
		self.Bind(wx.EVT_MENU, self.OnConfig, self.itemConfig)
		
		return menuBar
	
	def NormalMode_MenuBar(self):
		"This method manage sthe menu bar in case of normal mode"
	###########################
	
		# File menu creation
		menuFile = wx.Menu()
		itemOpencfg = menuFile.Append(-1, "Module Configuration...", "Open Configuration Dialog", wx.ITEM_NORMAL)
		itemConfigFile = menuFile.Append(-1, "Open Config File...", "Open Configuration File", wx.ITEM_NORMAL)
		itemExit = menuFile.Append(wx.ID_EXIT, "Exit", "Exit the software", wx.ITEM_NORMAL)
		
		# gestion menu creation
		menuGestion = wx.Menu()
		itemAddCfg	 = menuGestion.Append(-1, "Add Config", "Add a config file to test project list", wx.ITEM_NORMAL)
		itemAddTest = menuGestion.Append(-1, "Add Test", "Add a scenario test to test project list", wx.ITEM_NORMAL)
		menuGestion.AppendSeparator()
		itemCleanTest = menuGestion.Append(-1, "Clean Test", "Clean the all scenarios test in test project list", wx.ITEM_NORMAL)
		itemCleanAll = menuGestion.Append(-1, "Clean All", "Clean all in the test project list (config file and the scenario test)", wx.ITEM_NORMAL)
		
		# automation menu creation
		menuAutomation = wx.Menu()
		self.ID_start_Menu = wx.NewId() # cr�er un ID le boutton run
		self.ID_stop_Menu = wx.NewId() # cr�er un ID le boutton stop
		itemRun = menuAutomation.Append(self.ID_start_Menu, "Run...", "Run all scenarios tests", wx.ITEM_NORMAL)
		itemBreak = menuAutomation.Append(self.ID_stop_Menu, "Stop", "Break the test", wx.ITEM_NORMAL)
		
		# result menu creation
		menuResult = wx.Menu()
		self.itemLog = menuResult.Append(401, "Log", "Produce the log file or not", wx.ITEM_CHECK)
		if self.log_flag:
			self.itemLog.Check()
		menuResult.AppendSeparator()
		itemXML = menuResult.Append(-1, "XML", "Produce the XML file", wx.ITEM_NORMAL)
		itemExcel = menuResult.Append(-1, "Excel", "Produce the Excel file", wx.ITEM_NORMAL)
		menuResult.AppendSeparator()
		itemMux0710 = menuResult.Append(-1, "MUX 07.10", "Open 07.10 Windows", wx.ITEM_NORMAL)
		
		# Help menu creation
		menuHelp = wx.Menu()
		itemAbout = menuHelp.Append(wx.ID_ABOUT, "&About", "Information about this software", wx.ITEM_NORMAL)
		
		# menubar creation
		menuBar = wx.MenuBar()
		menuBar.Append(menuFile, 		"File")
		
		menuBar.Append(menuGestion, 		"Gestion")
		menuBar.Append(menuAutomation, 	"Automation")
		menuBar.Append(menuResult, 	 	"Result")
		menuBar.Append(menuHelp, 	   	"Help")
		
		#deactivate start & stop buttons 
		menuBar.Enable(self.ID_start_Menu, 1)
		menuBar.Enable(self.ID_stop_Menu, 0)
		
		# bind events on the menu
		self.Bind(wx.EVT_MENU, self.OnOpenCfg, 	 itemOpencfg)
		self.Bind(wx.EVT_MENU, self.OnOpenCfgFile,      itemConfigFile)
		self.Bind(wx.EVT_MENU, self.OnClose, 	 itemExit)
		self.Bind(wx.EVT_MENU, self.OnAddCfg, 	 itemAddCfg)
		self.Bind(wx.EVT_MENU, self.OnAddTest, itemAddTest)
		self.Bind(wx.EVT_MENU, self.OnCleanTest, itemCleanTest)
		self.Bind(wx.EVT_MENU, self.OnCleanAll, itemCleanAll)
		self.Bind(wx.EVT_MENU, self.OnRun, 		 itemRun)
		self.Bind(wx.EVT_MENU, self.OnStop, 		 itemBreak)
		self.Bind(wx.EVT_MENU, self.OnLog, 		 self.itemLog)
		self.Bind(wx.EVT_MENU, self.OnXML, 		 itemXML)
		self.Bind(wx.EVT_MENU, self.OnExcel, 	 itemExcel)
		self.Bind(wx.EVT_MENU, self.OnAbout, 	 itemAbout)
		self.Bind(wx.EVT_MENU, self.OnOpenDlg0710, itemMux0710)
		
		return menuBar
	
	#######################################
	# tools bar creation	#
	#######################################
	def DemoMode_ToolBar(self):
		"tool bar elements creation in demo mode"
	###########################
		self.ID_stop = wx.NewId()
		self.ID_clear = wx.NewId()
#		self.ID_startGNSS = wx.NewId()
#		self.ID_stopGNSS = wx.NewId()
		
		try:
			# Get icon for stop button road panel
			icon_chaine = images.getStopData()
			icon_stream = cStringIO.StringIO(icon_chaine)
			icon_image_Stop = wx.BitmapFromImage(wx.ImageFromStream(icon_stream))
			
			# Get icon for clear logs button
			icon_chaine = images.getClearData()
			icon_stream = cStringIO.StringIO(icon_chaine)
			icon_image_Clear = wx.BitmapFromImage(wx.ImageFromStream(icon_stream))
			
			icon_stream.close()
			del icon_chaine, icon_stream
		except :
			pass

		try:
			stop_chaine = images.get_gps_stopData()
			stop_stream = cStringIO.StringIO(stop_chaine)
			stop_GNSS_bmp = wx.BitmapFromImage(wx.ImageFromStream(stop_stream))
			
			start_chaine = images.get_gps_startData()
			start_stream = cStringIO.StringIO(start_chaine)
			start_GNSS_bmp = wx.BitmapFromImage(wx.ImageFromStream(start_stream))
			
			stop_stream.close()
			start_stream.close()
			del stop_chaine, stop_stream
			del start_chaine, start_stream

		except :
			pass
		
		self.outils = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.NO_BORDER)
		self.outils.SetToolBitmapSize((24, 24))
		
		self.outils.AddSimpleTool(self.ID_stop, icon_image_Stop, shortHelpString="Stop", longHelpString="Stop")
		self.outils.AddSeparator()
		self.outils.AddSimpleTool(self.ID_clear, icon_image_Clear, shortHelpString="clear log", longHelpString="clear log")
		self.outils.AddSeparator()
		self.outils.EnableTool(self.ID_stop, 0)
		self.outils.EnableTool(self.ID_clear, 1)

		self.outils.AddSimpleTool(self.ID_startGNSS, start_GNSS_bmp, shortHelpString="Start GNSS", longHelpString="Start GNSS")
		self.outils.AddSimpleTool(self.ID_stopGNSS, stop_GNSS_bmp, shortHelpString="Stop GNSS", longHelpString="Stop GNSS")

		self.outils.EnableTool(self.ID_stopGNSS, 0)
		self.outils.EnableTool(self.ID_startGNSS, 1)
			
		self.outils.AddSeparator()
		
		wx.EVT_MENU(self, self.ID_stop, self.OnStop)
		wx.EVT_MENU(self, self.ID_clear, self.OnClear_log)
		wx.EVT_MENU(self, self.ID_stopGNSS, self.OnStopGNSS)
		wx.EVT_MENU(self, self.ID_startGNSS, self.OnStartGNSS)
		
		self.outils.Realize()
		self.SetToolBar(self.outils)
		return self.outils
	
	def OnStopGNSS(self, evt):
		''' Event on start gps reception '''
		VarDemoTool.flagStop = True
		#Stop spécifique
		current_page = self.NoteBook.GetCurrentPage().GetName()
#		print"Current page: " + current_page
		if current_page == "GNSS":
			VarDemoTool.flagStop = True
			self.outils.EnableTool(self.ID_startGNSS, 0)
			self.outils.EnableTool(self.ID_stopGNSS, 0)
#			print"flagStop: ",VarDemoTool.flagStop
	
	def OnStartGNSS(self, evt):
		''' Event on start gps reception '''
		global GNSS_flag
		GNSS_flag = True
		nBook = self.NoteBook
		VarDemoTool.flagStop = False
		if (nBook.GetCurrentPage().GetName() == "GNSS"):
			self.toolBar.EnableTool(self.ID_stopGNSS, 0)
			self.toolBar.EnableTool(self.ID_startGNSS, 0)
			VarDemoTool.Histo = Histo.Histo(self, -1)
			FuncName = "GNSS_Start"
#			print nBook.GetCurrentPage().GetName()
			InputDemoTool.StartScript2(self, FuncName, nBook)
		else:
			self.toolBar.EnableTool(self.ID_stopGNSS, 0)
			self.toolBar.EnableTool(self.ID_startGNSS, 1)
			wx.MessageBox("Select the GNSS tab before !","Warning !")

	def NormalMode_ToolBar(self):
		"tool bar elements creation in normal mode"
	###########################
		self.ID_conf = wx.NewId() 		# create ID for button : add conf
		self.ID_test = wx.NewId() 		# create ID for button : add test
		self.ID_start = wx.NewId() 		# create ID for button : run
		self.ID_stop = wx.NewId() 		# create ID for button : stop
		self.ID_clear = wx.NewId() 		# create ID for button : clear logs
		self.ID_release = wx.NewId() 	# create ID for button : COM ports release
		self.ID_modulecfg = wx.NewId() 	# create ID for button : Module configuration
		
		try:
			# get Icon of add config files button
			icon_chaine = images.getOpen_ConfData()
			icon_stream = cStringIO.StringIO(icon_chaine)
			icon_image_Open_Conf = wx.BitmapFromImage(wx.ImageFromStream(icon_stream))
			
			# get Icon of add test files button
			icon_chaine = images.getOpen_ScriptData()
			icon_stream = cStringIO.StringIO(icon_chaine)
			icon_image_Open_Script = wx.BitmapFromImage(wx.ImageFromStream(icon_stream))
			
			# get Icon of test execution button
			icon_chaine = images.getPlayData()
			icon_stream = cStringIO.StringIO(icon_chaine)
			self.icon_Run = wx.BitmapFromImage(wx.ImageFromStream(icon_stream))
			
			# get Icon of Pause button
			self.icon_Pause = wx.BitmapFromImage(images.getPauseImage())
			
			# get Icon of stop test execution button
			icon_chaine = images.getStopData()
			icon_stream = cStringIO.StringIO(icon_chaine)
			icon_image_Stop = wx.BitmapFromImage(wx.ImageFromStream(icon_stream))
			
			# get Icon of clear logs button
			icon_chaine = images.getClearData()
			icon_stream = cStringIO.StringIO(icon_chaine)
			icon_image_Clear = wx.BitmapFromImage(wx.ImageFromStream(icon_stream))
			
			# get Icon of release all COM ports button
			icon_Release = wx.BitmapFromImage(images.getReleaseImage())
			
			# get icon of Configuration button
			icon_chaine = images.get_config_icon()
			icon_stream = cStringIO.StringIO(icon_chaine)
			self.icon_modulecfg = wx.BitmapFromImage(wx.ImageFromStream(icon_stream))
			icon_stream.close()
			del icon_chaine, icon_stream
		except:
			pass
		
		outils = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL | wx.NO_BORDER)
		outils.SetToolBitmapSize((24, 24))
		
		outils.AddSimpleTool(self.ID_conf, icon_image_Open_Conf , shortHelpString="Add config file", longHelpString="Add Config file")
		
		outils.AddSimpleTool(self.ID_test, icon_image_Open_Script, shortHelpString="Add Test", longHelpString="Add tests scripts")
		outils.AddSeparator()
		outils.AddSimpleTool(self.ID_start, self.icon_Run, shortHelpString="run", longHelpString="run")
		outils.AddSimpleTool(self.ID_stop, icon_image_Stop, shortHelpString="Stop", longHelpString="Stop")
		outils.AddSeparator()
		outils.AddSimpleTool(self.ID_clear, icon_image_Clear, shortHelpString="clear log", longHelpString="clear log")
		outils.AddSeparator()
		outils.AddSimpleTool(self.ID_release, icon_Release, shortHelpString="release all Com port", longHelpString="release all Com port")
		outils.AddSeparator()
		outils.AddSimpleTool(self.ID_modulecfg, self.icon_modulecfg, shortHelpString="Open configuration windows", longHelpString="Open configuration windows")

		outils.EnableTool(self.ID_start, 1)
		outils.EnableTool(self.ID_stop, 0)
		outils.EnableTool(self.ID_release, 0)
		
		wx.EVT_MENU(self, self.ID_conf, self.OnAddCfg)
		wx.EVT_MENU(self, self.ID_test, self.OnAddTest)
		wx.EVT_MENU(self, self.ID_start, self.OnRun)
		wx.EVT_MENU(self, self.ID_stop, self.OnStop)
		wx.EVT_MENU(self, self.ID_clear, self.OnClear_log)
		wx.EVT_MENU(self, self.ID_release, self.OnReleaseComPort)
		wx.EVT_MENU(self, self.ID_modulecfg, self.OnOpenCfg)
		
		outils.Realize()
		self.SetToolBar(outils)
		
		return outils
	
	def CreateToolBar(self):
		"tool bar creation"
	###########################
		if VarGlobal.MODE == VarGlobal.DEMO_MODE:
			return self.DemoMode_ToolBar()
		else:
			return self.NormalMode_ToolBar()

	def OnClear_log(self, event): 
		"action to preform when clickong on clear log button"
	###########################
		self.log_tc.Clear()
		self.process_lc.DeleteAllItems()

	def get_error_msg(self, msg_exception):
		"this method creates the message error structure to be displayed"
	###########################
		lines = msg_exception.split('\n')
		head_msg_error = '--------------------------- Error Message ---------------------------\n' 
		tail_msg_error = '---------------------------------------------------------------------\n'
		return head_msg_error + '\n'.join(lines[-4:-1]) + '\n' + tail_msg_error


	####################################
	# events management methods #
	####################################
	def OnOpenDlg0710(self, event):
		" "
	###########################
		openDlg07102()
	
	# double click sur process_lc
	def OnDoubleclickOnProcess_lc(self, event):
		" "
	###########################
		if VarGlobal.posInLog != []:
			self.log_tc.ShowPosition(VarGlobal.posInLog[self.process_lc.GetFocusedItem()])
	
	# Ouverture de la dialog config
	def OnConfig(self, evt):
		" "
	###########################
		InputDemoTool.ConfigurationDialog(self, self.NoteBook)
	
	def OnClose(self, event):
		"This method manages the behaviour when clicked on window close"
	###########################
		self.Close(True)
	
	def OnAddCfg(self, event):
		"This method manages the behaviour when clicking on add config file"
	###########################
		if self.cfg == '':
			addTestDlg = AddTestDlg(self.treelist, self.list_test, config=True)
		else:
			cfgExistDlg = wx.MessageDialog(self,
										   'Can t add a config file ; remove current config file before adding a new one',
										   'Add Config file',
										   wx.OK | wx.ICON_INFORMATION)
			cfgExistDlg.ShowModal()
			cfgExistDlg.Destroy()
			return
		
		self.treelist = addTestDlg.GetTreeList()
		self.tree.DeleteAllItems()
		self.root = self.tree.AddRoot(self.treelist[0])
		for elem in self.treelist[1]:
			child = self.tree.AppendItem(self.root, elem[0])
			self.tree.SetPyData(child, None)
			self.display_test_tree(child, elem[1])
		
		#expand config file list and test files list 
		firstChild = self.tree.GetFirstChild(self.root)
		self.tree.Expand(firstChild[0])
		self.tree.Expand(self.tree.GetNextChild(self.root, firstChild[1])[0])
		
		self.list_test = addTestDlg.GetListTest()
		self.cfg = addTestDlg.GetCfg()
		
		
	def OnAddTest(self, event):                
		"This method manages the behaviour when clicking on add test files"
	###########################
		addTestDlg = AddTestDlg(self.treelist, self.list_test)
		
		self.treelist = addTestDlg.GetTreeList()		
		self.tree.DeleteAllItems()
		self.root = self.tree.AddRoot(self.treelist[0])
		for elem in self.treelist[1]:
			child = self.tree.AppendItem(self.root, elem[0])
			self.tree.SetPyData(child, None)
			self.display_test_tree(child, elem[1])
		
		#expand config file list and test files list 
		firstChild = self.tree.GetFirstChild(self.root)
		self.tree.Expand(firstChild[0])
		self.tree.Expand(self.tree.GetNextChild(self.root, firstChild[1])[0])
		
		self.list_test = addTestDlg.GetListTest()
		
		self.toolBar.EnableTool(self.ID_stop, 0)
		self.toolBar.EnableTool(self.ID_start, 1)
		self.menuBar.Enable(self.ID_stop_Menu, 0)
		self.menuBar.Enable(self.ID_start_Menu, 1)

	## rtn STUDY
	def OnAddTestByDrop(self, filelists):                
		"This method manages the behaviour when clicking on add test files"
	###########################
		#addTestDlg = AddTestDlg(self.treelist, self.list_test)
		self.treelist[1][1][1] = filter(None,self.treelist[1][1][1])
		
		temp = []
		for elem in filelists:
			if ".py" in elem or ".PY" in elem:
				self.treelist[1][1][1].append(os.path.basename(elem.replace("\\","/")).encode('ascii','ignore'))
			if ".cfg" in elem:
				temp.append(elem.replace("\\","/").encode('ascii','ignore'))
				self.treelist[1][0][1] = temp
				self.cfg = temp[0]                                		

		self.tree.DeleteAllItems()
		self.root = self.tree.AddRoot(self.treelist[0])		
		for elem in self.treelist[1]:
			child = self.tree.AppendItem(self.root, elem[0])
			self.tree.SetPyData(child, None)
			self.display_test_tree(child, elem[1])			
		
		#expand config file list and test files list 
		firstChild = self.tree.GetFirstChild(self.root)
		self.tree.Expand(firstChild[0])
		self.tree.Expand(self.tree.GetNextChild(self.root, firstChild[1])[0])
		
		#self.list_test = addTestDlg.GetListTest()
		for elem in filelists:
			if ".py" in elem or ".PY" in elem:
				self.list_test.append(elem.replace("\\","/").encode('ascii','ignore'))
		
		
		self.toolBar.EnableTool(self.ID_stop, 0)
		self.toolBar.EnableTool(self.ID_start, 1)
		self.menuBar.Enable(self.ID_stop_Menu, 0)
		self.menuBar.Enable(self.ID_start_Menu, 1)
	
	def OnCleanTest(self, event):
		"This method manages the behaviour when clicking on clean test files"
	###########################
		# delete and create again the test files list
		self.treelist[1][1][1] = [""]
		
		self.tree.DeleteAllItems() 
		self.list_test = []
		
		# add file list 
		self.root = self.tree.AddRoot(self.treelist[0])
		
		for elem in self.treelist[1]:
			child = self.tree.AppendItem(self.root, elem[0])
			self.tree.SetPyData(child, None)
			self.display_test_tree(child, elem[1])
		
		#expand config file list and test files list 
		firstChild = self.tree.GetFirstChild(self.root)
		self.tree.Expand(firstChild[0])
		self.tree.Expand(self.tree.GetNextChild(self.root, firstChild[1])[0])

	# Supprimer tous les contenus dans la liste de test
	def OnCleanAll(self, event):
		"This method manages the behaviour when clicking on gestion > clean all (so both config file and test files)"
	###########################
		# delete and create again the config file liste and the test files list
		self.treelist[1][0][1] = [""]
		self.treelist[1][1][1] = [""]
		self.tree.DeleteAllItems()
		self.root = self.tree.AddRoot(self.treelist[0])
		
		for elem in self.treelist[1]:
			child = self.tree.AppendItem(self.root, elem[0])
			self.tree.SetPyData(child, None)
			self.display_test_tree(child, elem[1])
			
		#expand config file list and test list
		firstChild = self.tree.GetFirstChild(self.root)
		self.tree.Expand(firstChild[0])
		self.tree.Expand(self.tree.GetNextChild(self.root, firstChild[1])[0])
		
		# clear config file list
		self.cfg = ""
		
		# clear list file list
		self.list_test = []
	
	def OnRun(self, event):
		"This method manages the behaviour when clicking on start button (or automation > start)"
	###########################
		try:
			if self.StartFlag:
				self.OnPause()
			else:
				# if log flag set, the logs are going both on GUI and file
				
				#if self.log_flag:
					#self.test_output = Output.GuiLogOutput(self.log_tc, self.log_file)
				#else logs are displayed only on GUI
				#else:
					#self.test_output = Output.GuiOutput(self.log_tc)

				#manage the enabled/disabled START and STOP buttons
				self.RunStopButtonsState(OnRun=True)

				# kmwong , self.log_tc >> MainFrame message windows in right side 
				self.test = Test(self.cfg, self.gui, self.list_test, self.log_tc, MainFrame=self, DemoToolId=None)
				#self.test = Test(self.cfg, self.gui, self.list_test, self.test_output, MainFrame=self, DemoToolId=None)
				
				#1.8.1 JFW : put in comment ; it seems to be a wrong copy/paste (2 times the same code)
				#???why a second time ?
				#if self.log_flag:
				#	self.test_output = GuiLogOutput(self.log_tc, self.log_file)
				#else:
				#	self.test_output = GuiOutput(self.log_tc)
				#???why a second instance ?
				#self.test = Test(self.cfg, self.gui, self.list_test, self.test_output, MainFrame=self)
				
				#launch the thread Test (which execute tests)
				self.test.start()
				self.test.setName("Test")
			#??? why a second time ?
			self.RunStopButtonsState(OnRun=True)
		except NameError:
			f = cStringIO.StringIO()
			traceback.print_exc(file=f)
			error_msg = self.get_error_msg(f.getvalue())
			print error_msg
	
	def OnPause(self):
		"This method manages the behaviour when clicking on pause (for an executing test)"
	###########################
		if self.PauseFlag:
			# Continue
			self.process_lc.Pause(False)
			self.toolBar.SetToolNormalBitmap(self.ID_start, self.icon_Pause)
			self.toolBar.SetToolShortHelp(self.ID_start, "Pause")
			self.toolBar.SetToolLongHelp(self.ID_start, "Pause")
			if self.ReleaseFlag:
				SagReleaseAllComPort(release=False)
				self.ReleaseFlag = False
			
			SafePrint(None, None, "Pause realize", color=1)
			self.toolBar.EnableTool(self.ID_release, 0)
			# Restore print mutex
			if self.MutexStatus[0]:
				print_mutex.acquire()
			if self.MutexStatus[1]:
				Output_staticVariables.print_mutex.acquire()
			SagContinueAllThread(silent=True)
		else:
			# Pause
			from threadStop import displayTrace
			displayTrace = True
			# Save print mutex status
			self.MutexStatus = [print_mutex.locked(), Output_staticVariables.print_mutex.locked()]
			# Release print mutex
			try:
				print_mutex.release()
				Output_staticVariables.print_mutex.release()
			except SystemExit:
				raise SystemExit
			except:
				pass
			
			self.toolBar.EnableTool(self.ID_release, 1)
			SagPauseAllThread(silent=True)
			self.process_lc.Pause(True)
			self.toolBar.SetToolNormalBitmap(self.ID_start, self.icon_Run)
			self.toolBar.SetToolShortHelp(self.ID_start, "Continue")
			self.toolBar.SetToolLongHelp(self.ID_start, "Continue")
			SafePrint(None, None, "Pause activate", color=1)
		self.PauseFlag = not(self.PauseFlag)
	
	def OnStop(self, event):
		"This method manages the behaviour when clicking on stop (for an executing test)"
	###########################
		SagStopAllPort()
		SagStopAllThread(silent=True)
		ResetDisplayOfDCD_OnMuxDlg()
	
	def RunStopButtonsState(self, OnRun=True):
		"This method manages the states changes (enable/disable) of START,PAUSE and STOP buttons"
		###########################
		#if start button clicked
		if OnRun:
			if self.ID_start != None:
				#change the START button to PAUSE button
				self.toolBar.SetToolNormalBitmap(self.ID_start, self.icon_Pause)
				self.toolBar.SetToolShortHelp(self.ID_start, "Pause")
				self.toolBar.SetToolLongHelp (self.ID_start, "Pause")

			#enable the STOP button
			self.toolBar.EnableTool(self.ID_stop, 1)
			if self.ID_stop_Menu != None:
				self.menuBar.Enable(self.ID_stop_Menu, 1)
			if self.ID_start_Menu != None:
				self.menuBar.Enable(self.ID_start_Menu, 0)
			self.StartFlag = True
		#if STOP button clicked
		else:
			ResetDisplayOfDCD_OnMuxDlg()
			if self.ID_start != None:
				self.toolBar.SetToolNormalBitmap(self.ID_start, self.icon_Run)
				self.toolBar.SetToolShortHelp(self.ID_start, "Run")
				self.toolBar.SetToolLongHelp(self.ID_start, "Run")
				self.toolBar.EnableTool(self.ID_start, 1)
				self.toolBar.EnableTool(self.ID_release, 0)
			#disable the STOP button
			self.toolBar.EnableTool(self.ID_stop, 0)
			self.ReleaseFlag = False
			if self.ID_stop_Menu != None:
				self.menuBar.Enable(self.ID_stop_Menu, 0)
			if self.ID_start_Menu != None:
				self.menuBar.Enable(self.ID_start_Menu, 1)
			if self.ID_Config != None:
				self.menuBar.Enable(self.ID_Config, True)
			self.StartFlag = False
			self.PauseFlag = False

	def OnReleaseComPort(self, evt):
		"This method manages the behaviour when clicking on releasing all COM ports button "
	###########################
		self.ReleaseFlag = not(self.ReleaseFlag)
		SagReleaseAllComPort(self.ReleaseFlag)
	
	def OnLog(self, event):
		"This method manages the behaviour when clicking on Result>log menu"
	###########################
		self.log_flag = not self.log_flag
        # kmwong
		#if not(os.path.isdir("Logs")):
		#	os.mkdir("Logs")
		#dt = datetime.now()
		#self.log_file = "Logs\\%d-%0.2d-%0.2d__%0.2d-%0.2d-%0.2d.log" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
	
	def OnXML(self, event):
		"This method manages the behaviour when clicking on Result>XML menu"
	###########################
		dlg = wx.FileDialog(self,
							message="Save file as XML",
							defaultDir=os.getcwd(),
							defaultFile="",
							wildcard="*.xml",
							style=wx.SAVE)
		
		if dlg.ShowModal() == wx.ID_OK:
			XmlTree.xmlTree.WriteTree(dlg.GetFilename())
		dlg.Destroy()
	
	def OnExcel(self, event):
		"This method manages the behaviour when clicking on Result>Excel menu"
	###########################
		if VarGlobal.excelDoc == None:
			VarGlobal.excelDoc = ExcelDoc()
		VarGlobal.excelDoc.Display()
	
	# Ev�nement quand il a lieu de cliquer sur "About"
	def OnAbout(self, event):
		"This method manages the behaviour when clicking on Help>about menu"
	###########################
		aboutDlg = AboutDlg(self)
		aboutDlg.Show()

	def OnOpenCfg(self, event):
		self.settings = [self.cfg, False, False]
		settings_dialog = Settings(self.settings, self)
		res = settings_dialog.ShowModal()
		
	def OnOpenCfgFile(self, event):
		#os.startfile(self.cfg)
		notepadPath = r'C:\Windows\System32\notepad.exe'
		subprocess.Popen("%s %s" % (notepadPath, self.cfg))
		
####################################################################################################################		
if __name__ == '__main__':
	pass
