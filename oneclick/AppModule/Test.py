#!/usr/bin/env python
# _*_ coding: utf-8 _*_


#----------------------------------------------------------------------------
# Name:			test.py
# Goal:			Ce module implante un objet qui repr?sente une session de  
#			   test. 
#			   Dans l'implantation de classe Test, une fonction run_test
#			   qui permet de lancer le test. Donc, il fournit un 
#			   environnement de l'ex?cution de sc?nario en utilisant 
#			   from ComModuleAPI, mais il faut aussi partager des variable
#			   global avec ComModuleAPI, pour cela, on cr?e un fichier 
#			   VarGlobal qui contient les varialbles va ?tre partager 
#			   entre les modules Test, ComModuleAPI et MainFrame
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
#04->09-2007      Bingxun HOU          1.0                     creation
#08-09-2011       JFWeiss              1.8.1                   comments and light modifications
#                                                              put into Test class the methods defined without any class
#                                                              they are not used for this version ; remove also the Static_Variables class
#                                                              which becom global variable in Test class
#03-2012          JM Seillon           1.8.3                   Modification, add 'self' as first param in function member(it's mandatory). 
#
#02-04-2013       JF Weiss             1.9.4                   fix on import

import os, sys
import wx
import time
import serial
import threading
import VarGlobal
import XmlTree
import ConfigParser
import re

import Output
from Output       import staticVariables as Output_staticVariables
from datetime		   import datetime
from ComModuleAPI	   import *
from ExcelDoc		   import *
from threadStop		   import Thread
from PersonalException import *
from Frame0710		   import *
from Mux0710		   import *

if VarGlobal.MODE == VarGlobal.DEMO_MODE:
	import DemoToolScripts
	import VarDemoTool


def MySendAT(comPort, commands):
    ser = serial.Serial(comPort - 1)
    ser.baudrate = '115200'
    ser.bytesize = 8
    ser.parity = 'N'
    ser.stopbits = 1
    ser.timeout = 2
    ser.rtscts = True

    for ipr in ['115200','9600']:
            ser.write("AT\r")
            time.sleep(1)
            if ser.inWaiting() > 0:
                  ser.baudrate = ipr
                  break

    ser.write(commands)
    print "COM%s => %s" % (comPort, commands.replace('\r','<CR>').replace('\n','<LF>'))
    time.sleep(1)
    output = ''
    while ser.inWaiting() > 0:
        output += ser.read(1)

    time.sleep(0.1)
    while ser.inWaiting() > 0:
        output += ser.read(1)
    ser.close()
    if output != '':
        print "COM%s <= %s" % (comPort, output.replace('\r','<CR>').replace('\n','<LF>'))
    return output

class Test(Thread):
	"this class instanciates threads ; it shall be instanciated using start() and not run()"
	"run method will be executed automatically by Python"
	
	receive_exception  = False
	no_receive_exception = False
	stop_exception = False
	COM_exception = False

	def __init__(self, cfg, gui, list_test, test_output, xml_file='', MainFrame=None, DemoToolId=None):
		"constructor"
		Thread.__init__(self)
		self.cfg = cfg
		self.gui = gui
		self.list_test= list_test
		self.test_output = test_output
		self.xml_file = xml_file
		self.MainFrame = MainFrame
		self.DemoToolId = DemoToolId
		receive_exception  = False
		no_receive_exception = False
		stop_exception = False
		COM_exception = False

	def run(self): 
		"this method executes the tests cases the one after the others"
		"when instancating the thread, it is advised to use start() and not directly run()"
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			print "Begin Test.run() : thread Test launched\r\n"
			print "@@@thread launched@@@\r\n"
		try:
			ExitSagWaitLineWhenRecvError(False)
			
			cfg = self.cfg
			list_test= self.list_test
			#test_output = self.test_output
			xml_file = self.xml_file
			#process_lc = self.process_lc
			current_file = ''
			
			if VarGlobal.MODE == VarGlobal.DEMO_MODE:
				DemoToolScripts.RaiseRunEvent(self.DemoToolId)

			# GUI
			if self.gui == True:
				gui_out = self.test_output
				test_output = GuiOnlyOutput(gui_out)

			# CLI
			if self.gui == False:
				test_output = MyStdout()

			sys.stdout = test_output
			sys.stderr = sys.stdout
			
			# set color for error
			VarGlobal.myColor = "coral"
			#print "testing error message"

			# to know the excution duration
			start_time = datetime.now()
			
			VarGlobal.excelDoc = ExcelDoc()
			
			XmlTree.xmlTree = XmlTree.XmlTree() 
			XmlTree.xmlTree.AddNode('test')
			
			# For test report
			VarGlobal.numOfCommand = 0.0
			VarGlobal.numOfTest = 0.0
			VarGlobal.numOfSuccessfulTest = 0.0 
			VarGlobal.numOfFailedTest = 0.0
			VarGlobal.numOfCommand = 0.0
			VarGlobal.numOfResponse = 0.0
			VarGlobal.numOfSuccessfulResponse = 0.0 
			VarGlobal.numOfFailedResponse = 0.0
			VarGlobal.excelCommentGlobal = ''
			
			self.item_counter = 1
			

			
			# mettre en oeuvre tous les tests dans la list de test
			if self.MainFrame != None:
				self.MainFrame.process_lc.DeleteAllItems()
			
			for test in list_test:
				files_test = None
				DVQ_Version = test # DVQ xxx
				if os.path.isfile(test) or VarGlobal.MODE == VarGlobal.DEMO_MODE:
					if test[-3:] == '.py' or VarGlobal.MODE == VarGlobal.DEMO_MODE:
						files_test = [[None,"",[test]]]
					else: 
						print "Message: The indicated test file name is not .py"
				elif os.path.isdir(test):
					files_test = os.walk(test)
				else:
					print "Message: The indicated test (file or directory) %s don't exist."%test
				
				if files_test != None:
					for path, subdirs, files in files_test:
						
						# For excel part
						if path != test and files_test != [[None,"",[test]]]:
							VarGlobal.excelDoc.NewItem()
							VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetVersion(DVQ_Version)
							VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetReference(path.split("\\")[-1].split(" ")[0])
							VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetTitle(" ".join(path.split("\\")[-1].split(" ")[1:])[:-3])
							dt = datetime.now() 
							VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetDate("%d/%d/%d"%(dt.day, dt.month, dt.year))
							VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetComment(VarGlobal.excelCommentGlobal)										
						
						if path != None:
							path = path.replace('\\', '\\\\')



						for file in files:
							# kmwong temp solution for independent log for each script

							# .log Start

							# CLI - custom path
							if self.gui == False:
								if os.path.isdir(self.test_output):
									print "it is a path"
									print self.test_output
									#self.test_output = ""
									filepath = self.test_output + "\\"

							# CLI - default path 
							if self.gui == False:
								if not(os.path.isdir(self.test_output)):
									if not(os.path.isdir("Logs")):
										os.mkdir("Logs")
									filepath = "Logs\\"

							# GUI
							if self.gui == True:
								gui_out = self.test_output
								if not(os.path.isdir("Logs")):
									os.mkdir("Logs")
								filepath = "Logs\\"



							filefullname = os.path.basename(file) # fullpath
							filename = os.path.splitext(filefullname)[0]   # filename
							filetimestamp = time.strftime("__%Y_%m_%d__%H_%M_%S", time.localtime())
							log_out = filepath + filename + ".log"
							log_out_timestamp = filepath + filename + filetimestamp + ".log"
							
							#print log_out_timestamp


							# Clear log
							tempclearlog = ClearLogFileOutput(log_out)

							# Append log
							if self.gui == True:
								test_output = GuiLogOutput(gui_out, log_out, log_out_timestamp)
								#test_output = LogDisplayFileOutput(log_out, log_out_timestamp)
							else:
								test_output = LogDisplayFileOutput(log_out, log_out_timestamp)
							sys.stdout = test_output
							sys.stderr = sys.stdout


							# .cfg Start
							VarGlobal.myColor = "DARK BLUE"
							print "**********************************************************************"
							print "                              Start the Test                          "
							print "  ------------------------------------------------------------------  "
							print time.strftime("                      %Y-%m-%d %H:%M:%S", time.localtime())
							print "**********************************************************************"

							if VarGlobal.MODE != VarGlobal.DEMO_MODE:
								VarGlobal.myColor = "coral"
								print 'CONFIG FILE: %s\n' % cfg
								print 'AutoTestPlus version : V%s ' % VarGlobal.VERSION
								current_file = cfg
								try:
									#execute config file content (as a source Linux)
									execfile(cfg)
								except IOError:
									print "MESSAGE: Error! The config file don't exist."


							# .py start
							if file.find('.py', -3) != -1 or VarGlobal.MODE == VarGlobal.DEMO_MODE: # trouver les fichiers avec le nom extension .py
								if self.MainFrame != None and self.MainFrame.log_tc != None:
									VarGlobal.posInLog.append(self.MainFrame.log_tc.GetLastPosition())
								if path != None:
									path_file = path+'\\\\'+file
								else:	
									path_file = file
								
								current_file = file
								
								VarGlobal.excelCommentGlobal = ''
								# for Excel part
								VarGlobal.excelDoc.NewItem()
								VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetVersion(DVQ_Version)
								VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetReference(file.split(" ")[0])
								VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetTitle(" ".join(file.split(" ")[1:])[:-3])
								dt = datetime.now() 
								VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetDate("%d/%d/%d"%(dt.day, dt.month, dt.year))
								VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetAvance("R")
								VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetComment(VarGlobal.excelCommentGlobal)		
								VarGlobal.statOfItem = 'OK'
								
								VarGlobal.myColor = "forest green"
								print "--------------------------------------------------------------------  "
								if VarGlobal.MODE != VarGlobal.DEMO_MODE:
									print "FILE: ",file
								current_file = file
																
								# process window state
								VarGlobal.process_stat = 'OK'
								# print the information for process window 
								if self.MainFrame != None:
									self.MainFrame.process_lc.AddItem("%d"%self.item_counter, 
																	   file,
																	   datetime.now(),
																	   "",
																	   "Running")
								# For xml tree
								XmlTree.xmlTree.AddNode("scenario%d"%self.item_counter)
								XmlTree.xmlTree.AddNode("name")
								XmlTree.xmlTree.SetContent(file)
								XmlTree.xmlTree.GoToFather()
								
								flag_no_exception = True
								# execute the test
								try:
									if VarGlobal.MODE == VarGlobal.DEMO_MODE:
										DemoToolScripts.StartScript(file,self.DemoToolId)
									else:
										#execute test case file content (as a source Linux)
										execfile(path_file)  # detecte de NameError dans la fonction qui fait l'appel.
								#2016-Dec-05, pdkhai, cover script syntax error case
								except SyntaxError as eSyntax:
									VarGlobal.myColor = VarGlobal.colorLsit[9]
									print('Script have syntax error')
									print 'Line ',eSyntax.lineno,': ',eSyntax.text
									VarGlobal.statOfItem = "NOK"
								except stop_exception:
									flag_no_exception = False
									VarGlobal.myColor = VarGlobal.colorLsit[9]
									print "Stop"
									VarGlobal.process_stat = "Stop"
									if self.MainFrame != None:
										if stop_exception:
											self.MainFrame.process_lc.ModifyItem(datetime.now(),"STOPPED & STOP ALL")
										else:
											self.MainFrame.process_lc.ModifyItem(datetime.now(),"STOPPED")
									raise stop_exception
								except COM_exception:
									flag_no_exception = False
									VarGlobal.myColor = VarGlobal.colorLsit[9]
									#print "COM error"
									VarGlobal.process_stat = "COM error"
									if self.MainFrame != None:
										if COM_exception:
											self.MainFrame.process_lc.ModifyItem(datetime.now(),"COM ERROR & STOP ALL")
										else:
											self.MainFrame.process_lc.ModifyItem(datetime.now(),"COM ERROR")
									raise stop_exception
								except receive_exception:
									flag_no_exception = False
									VarGlobal.myColor = VarGlobal.colorLsit[9]
									print "Stop current script : Waiting command not receive !!"
									VarGlobal.process_stat = "CMD NOT RECV"
									if self.MainFrame != None:
										if receive_exception:
											self.MainFrame.process_lc.ModifyItem(datetime.now(),"CMD NOT RECV & STOP ALL")
										else:
											self.MainFrame.process_lc.ModifyItem(datetime.now(),"CMD NOT RECV")
									raise stop_exception
								except no_receive_exception:
									flag_no_exception = False
									VarGlobal.myColor = VarGlobal.colorLsit[9]
									print "Stop current script : Nothing receive !!"
									VarGlobal.process_stat = "NOTHING RECV"
									if self.MainFrame != None:
										if receive_exception:
											self.MainFrame.process_lc.ModifyItem(datetime.now(),"NOTHING RECV & STOP ALL")
										else:
											self.MainFrame.process_lc.ModifyItem(datetime.now(),"NOTHING RECV")
									raise stop_exception
								except:
									raise
								
								# for xml tree
								XmlTree.xmlTree.GoToFather()
								
								# To be sure all launches threads are finished (optional threads : MuxThread, Thread (started by MuxThread)
								if self.gui == True:
									#njf v1.8.1 : change temporarly the max nb of threads from 2 to 3 to avoid blocking end of scenario (launched tasks : Test, Thread (started by Test) )
									while threading.activeCount() > 3: # if threads have been launched
										time.sleep(1)
										if VarGlobal.DEBUG_LEVEL == "DEBUG":
											print "wait for end of threads at the end of the last scenario. Nb threads = " + str(threading.activeCount())
								else:
									while threading.activeCount() > 3: # if threads have been launched
										time.sleep(1)
								
								# For process window at the end of the test execution
								# 2016-Dec-05, pdkhai, to read log and parse result    
								result = ''
								fo = open(log_out_timestamp, "r+")
								read_result = re.findall('Status (.*): (.*)\n',fo.read())
								if len(read_result) > 0:
									for idx in range(len(read_result)):
										result = result + read_result[idx][1] + ' '
								else:
									result = ''

								if self.MainFrame != None and flag_no_exception:
									if result is '':
										self.MainFrame.process_lc.ModifyItem(datetime.now(), VarGlobal.process_stat)
									else:
										self.MainFrame.process_lc.ModifyItem(datetime.now(), VarGlobal.process_stat, result)
								self.item_counter += 1
								VarGlobal.numOfTest += 1.0
								if VarGlobal.process_stat == 'OK':
									VarGlobal.numOfSuccessfulTest += 1.0
								else:
									VarGlobal.numOfFailedTest += 1.0
								
								VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetStat(VarGlobal.statOfItem)
								VarGlobal.excelDoc.list[VarGlobal.excelDoc.GetIndex()].SetComment(VarGlobal.excelCommentGlobal)
				
			# For tree xml
			XmlTree.xmlTree.GoToFather()
			if xml_file != '':
				XmlTree.xmlTree.WriteTree(xml_file)
			
			# To compute the total duration
			end_time = datetime.now()
			diff_time = (end_time - start_time).seconds * 1000.0 + (end_time - start_time).microseconds / 1000.0
			
			if VarGlobal.DEBUG_LEVEL == "DEBUG":
				print "end of the last scenario. Nb threads = " + str(threading.activeCount())
			VarGlobal.myColor = "DARK BLUE"
			if VarGlobal.MODE != VarGlobal.DEMO_MODE:
				# print "\n\n***************************************************************************************************************"
				# print "                           Report Of Test                             "
				# print "  -----------------------------------------------------------------------------------------------------------------"
				# print "  - Total Number Of Test File: %d" % VarGlobal.numOfTest
				# print "  - Number Of Successful Test: %d" % VarGlobal.numOfSuccessfulTest 
				# print "  - Number Of Failed Test: %d" % VarGlobal.numOfFailedTest
				# if VarGlobal.numOfTest != 0:
				# 	print "  - Successful Rate Of Test: %.2f%%" % ((VarGlobal.numOfSuccessfulTest/VarGlobal.numOfTest)*100.0)
				# print "  ------------------------------------------------------------------------------------------------------------------"
				# print "  - Total Number Of Sended AT Command: %d" % VarGlobal.numOfCommand 
				# print "  - Total Number Of Received Response: %d" % VarGlobal.numOfResponse 
				# print "  - Number Of Sucessful Response: %d" % VarGlobal.numOfSuccessfulResponse 
				# print "  - Number Of Failed Response: %d" % VarGlobal.numOfFailedResponse 
				# if VarGlobal.numOfResponse != 0:
				# 	print "  - Successful Rate Of AT Command: %.2f%%" % ((VarGlobal.numOfSuccessfulResponse/VarGlobal.numOfResponse)*100.0)
				print "  ------------------------------------------------------------------------------------------------------------------"
				print "  - Total Execution Time: %d milliseconds" % diff_time 
			print "\n***************************************************************************************************************"
			print "                              End of Test                             "
			print "  ---------------------------------------------------------------------------------------------------------------"
			print time.strftime("              %a, %d %b %Y %H:%M:%S", time.localtime())
			print "***************************************************************************************************************"
		except SystemExit:
			VarGlobal.myColor = VarGlobal.colorLsit[9]
			print "Stop button pressed"
			if self.MainFrame != None:
				if self.MainFrame.process_lc.Itemcount() == 0:
					self.MainFrame.process_lc.AddItem("1", current_file,datetime.now(),"","STOPPED")
				self.MainFrame.process_lc.ModifyItem(datetime.now(),"STOPPED")
		except stop_exception:
			if self.MainFrame != None:
				if self.MainFrame.process_lc.Itemcount() == 0:
					self.MainFrame.process_lc.AddItem("1",current_file,datetime.now(),"","STOP ALL")
				self.MainFrame.process_lc.ModifyItem(datetime.now(),"STOP ALL")
			VarGlobal.myColor = VarGlobal.colorLsit[9]
			print "Stop all"
		except:
			if self.MainFrame != None:
				if self.MainFrame.process_lc.Itemcount() == 0:
					self.MainFrame.process_lc.AddItem("1",current_file, datetime.now(), "", "SYS ERROR")
				self.MainFrame.process_lc.ModifyItem(datetime.now(),"SYS ERROR")
			VarGlobal.myColor = VarGlobal.colorLsit[9]
			raise
		finally:
			#self.StartFlag = False
			#self.PauseFlag = False
			ExitSagWaitLineWhenRecvError(False)
			if VarGlobal.MODE == VarGlobal.DEMO_MODE:
				DemoToolScripts.ClearRunEvent(self.DemoToolId)
			
			if self.MainFrame!=None:
				self.MainFrame.RunStopButtonsState(OnRun=False)
			VarGlobal.myColor = VarGlobal.colorLsit[9]
			
			SagStopAllThreadWithout(self)
			SagCloseAll()

	# to manage the autotets behaviour when exceptions occur (not used in V1.8.1)
	def StopAutotestWhen_COMError(self, value):
		COM_exception = value

	def StopAutotestWhen_ReceiveError(self, value):
		receive_exception = value

	def StopAutotestWhen_NothingReceive(self, value):
		no_receive_exception = value

	def StopAutotestWhen_StopEvent(self, value):
		stop_exception = value

	def ExceptionsWhichStopAll(self, except1="", except2="", except3="", except4=""):
		receive_exception  = False
		no_receive_exception = False
		stop_exception = False
		COM_exception = False
		if except1 == "receive_exception" or except2 == "receive_exception" or except3 == "receive_exception" or except4 == "receive_exception":
			receive_exception = True
		if except1 == "no_receive_exception" or except2 == "no_receive_exception" or except3 == "no_receive_exception" or except4 == "no_receive_exception":
			no_receive_exception = True
		if except1 == "stop_exception" or except2 == "stop_exception" or except3 == "stop_exception" or except4 == "stop_exception":
			stop_exception = True
		if except1 == "COM_exception" or except2 == "COM_exception" or except3 == "COM_exception" or except4 == "COM_exception":
			COM_exception = True

	def AddExceptionsWhichStopAll(self, except1="", except2="", except3="", except4=""):
		if except1 == "receive_exception" or except2 == "receive_exception" or except3 == "receive_exception" or except4 == "receive_exception":
			receive_exception = True
		if except1 == "no_receive_exception" or except2 == "no_receive_exception" or except3 == "no_receive_exception" or except4 == "no_receive_exception":
			no_receive_exception = True
		if except1 == "stop_exception" or except2 == "stop_exception" or except3 == "stop_exception" or except4 == "stop_exception":
			stop_exception = True
		if except1 == "COM_exception" or except2 == "COM_exception" or except3 == "COM_exception" or except4 == "COM_exception":
			COM_exception = True

	def RemoveExceptionsWhichStopAll(self, except1="", except2="", except3="", except4=""):
		if except1 == "receive_exception" or except2 == "receive_exception" or except3 == "receive_exception" or except4 == "receive_exception":
			receive_exception = False
		if except1 == "no_receive_exception" or except2 == "no_receive_exception" or except3 == "no_receive_exception" or except4 == "no_receive_exception":
			no_receive_exception = False
		if except1 == "stop_exception" or except2 == "stop_exception" or except3 == "stop_exception" or except4 == "stop_exception":
			stop_exception = False
		if except1 == "COM_exception" or except2 == "COM_exception" or except3 == "COM_exception" or except4 == "COM_exception":
			COM_exception = False

	def StopAllComPort(self):
		try:
			for hCom in list_hCom:
				# hCom.stop()
				hCom.close()
		except:
			pass
