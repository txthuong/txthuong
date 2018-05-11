#!/bin/env python
# _*_ coding: utf-8 _*_

#----------------------------------------------------------------------------
# Name:			autotest.py
# Goal:			Main Application
#			it analyses arguments and launches MMI
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
#2009              JM Ruffle           1.6.7                   modifications to create 1.6.7
#2009              JM Ruffle           1.7MUX                  modifications to create 1.7MUX (parallel branch)
#07-09-2011        JF Weiss            1.8                     merge 1.6 and 1.7 MUX versions
#07-09-2011        JF Weiss            1.8.1                   add comments and light modifications
#22-02-2012        JF Weiss            1.8.2                   change to 1.8.2 version (3442 bug)
#29-02-2012        JF Weiss            1.8.2                   modify version management to be consistent with GNSS mgt
#07-03-2012        JM Seillon          1.8.3                   add GNSS Functionality
#xx-04-2012        JM Seillon          1.8.4                   modifications for GNSS feature
#xx-05-2012        JM Seillon          1.8.6                   3G optionnaly don't send KGNSS* automatically
#xx-05-2012        JM Seillon          1.8.9                   Correction bugs 3961, 3965, 4128, 4117, 4124
#26-07-2012        JM Seillon          1.9.0                   Correction bug 4313
#26-07-2012        JM Seillon          1.9.1                   Correction bug 4316
#18-12-2012        JFWeiss             1.9.3                   change VERSION (regression in MUX)
#11-03-2013	       Eric BARRE          1.9.3                   Change HiloStarter version
#02-04-2013        JFWeiss             1.9.4   
#26-04-2013        Eric BARRE          1.9.5                   change version due to inconsistency between debug mode and AT starter
#29-04-2013        JF Weiss            1.9.6                   change version for Advanced MUX
#28-10-2013        kmwong              1.9.6.1                 Beta version for 1-click
#08-12-2013        kmwong              1.9.6.2                 Release for new serial port library like CETI
#10-12-2013        kmwong              1.9.6.3                 Add CPIN? to string2cmd() for Intel module 
#15-12-2013        kmwong              1.9.6.4                 Log to filename.log and display, log with timestamp
#22-12-2013        kmwong              1.9.6.5                 Log Snd and Rcv timestamp and timespent in Rcv
#28-12-2013        kmwong              1.9.6.6                 Add xmodem download feature
#19-01-2014        kmwong              1.9.6.7                 bug fixes: SagWaitResp(), ascii2print()
#22-05-2014        Knwong              1.9.6.8                 modifications for Tracker 4678
#24-09-2014        rtn                 1.9.6.10                integrate wesh for AVMS
#30-10-2014        rtn                 1.9.6.11                integrate hardreset
#11-02-2015        rtn                 1.9.6.18                name change to AutoTestPlus

#import os, sys
#import wx
#import cStringIO, traceback
#from datetime import datetime

from AppModule.Test		import *
from AppModule.Output	   	import *
from AppModule.MainFrame	import *
from AppModule.ComModuleAPI	import *

# Software Version

VERSION_NORMAL = "Revision: 1.9.6.28".split(" ", 1)[1]
VERSION_DEMO = "Revision: 1.9.6.28".split(" ", 1)[1]





#The following should be put in a configuration file
# Functional mode:
# VarGlobal.NORMAL_MODE:  normal
# VarGlobal.DEMO_MODE  :  Demo mode
#get the value directly in VarGlobal.py
#VarGlobal.MODE = VarGlobal.NORMAL_MODE


if VarGlobal.MODE == VarGlobal.DEMO_MODE:
	NAME = "HiLo starter development tool " + VERSION_DEMO
	VERSION = VERSION_DEMO
else:
	NAME = 'AutoTestPlus ' + VERSION_NORMAL
	VERSION = VERSION_NORMAL


####################################################################################################################
class MyApp(wx.App):
	"main application class"
#################################

	
	def OnInit(self):
		"main class ; the main class has not __init__ but OnInit"
	#################################
		# save stdout and stderror, before redirect them toward GuiOutput (that will allow to come back on stdout later)
		saveStreams = sys.stdout, sys.stderr
		
		from sys import argv
		self.cfg, self.log_file, self.log_flag, self.log_fullpath, self.xml_file, self.gui, self.help, self.list_test = self.getopts(argv)	
		
		# preparation of the list of 1 config file, n test files
		self.treelist = ['Test Projet', []]  # un list permet de represente le list de test sous forme d'un arbre
		self.treelist[1].append(["config file", [self.cfg]])  # config file list (only 1 file) ; insert from argument
		self.treelist[1].append(["tests file", []])  # test list ; it will be filled below
		
		if len(self.list_test) == 0:
			self.treelist[1][1][1].append("")
		else:
			for elem in self.list_test:
				self.treelist[1][1][1].append(self.create_test_tree(elem))
		
		if self.help:
			self.help_msg()
		#launch MMI
		elif (self.gui == True) or ((self.gui	 == False) and (self.cfg	 == '') and
									(self.log_flag == True) and (self.xml_file == '') and
									(self.help	 == False) and (self.list_test == [])):
			
			# create main window and display it
			mainFrame = MainFrame(NAME, self.treelist, self.cfg, self.log_file, self.log_flag, self.list_test)
			self.SetTopWindow(mainFrame)
		#autotest in CLI
		else:
			try:
				#redirect the logs into a file and display
				print "log to file"
				print "%s" % self.log_file
				if self.log_fullpath == '':
					log_output = ""
				else:
					print "log to particular path"
					log_output = self.log_fullpath
				#start the test execution
				test = Test(self.cfg, self.gui, self.list_test, log_output, self.xml_file)
				test.start()
				#test.run()
			except NameError:
				f = cStringIO.StringIO()
				traceback.print_exc(file=f)
				error_msg = self.get_error_msg(f.getvalue())
				print error_msg
		
		# go back to stdout
		sys.stdout, sys.stderr = saveStreams
		
		return True
	
	def getopts(self, argv):
		"This function saves arguments into variables"
	#################################
		cfg = ''
		log_file = ''
		log_flag = False
		log_fullpath = ''
		xml_file = ''
		xml_flag = False
		gui = False
		help = False
		list_test = []
		argv = argv[1:]
		if len(argv) == 0:
			print os.getcwd()
			thisPath = os.getcwd()+'/'
			cfg = thisPath + 'sample.cfg'
			log_flag = True
			log_fullpath = thisPath + 'Logs'
			gui = True
			list_test.append(thisPath + 'sample/sample.py')
		else:
			while argv:
				if argv[0] == '-cfg':
					cfg = argv[1]
					argv = argv[2:]
				elif argv[0] == '-log':
					log_flag = True
					argv = argv[1:]
				elif argv[0] == '-logpath':
					log_fullpath = argv[1]
					argv = argv[2:]
				elif argv[0] == '-xml':
					xml_flag = True
					argv = argv[1:]
				elif argv[0] == '-gui':
					gui = True
					argv = argv[1:]
				elif argv[0] == '-h':
					help = True
					argv = argv[1:]
				elif argv[0][0] == '-':
					print "Error: There is not the parameter %s." % argv[0]
					sys.exit()
				else:
					#log_file = argv[0]
					list_test.append(argv[0])
					argv = argv[1:]
		
		# define the log filename and xml filename
		dt = datetime.now()
		#log_file = "%d-%0.2d-%0.2d__%0.2d-%0.2d-%0.2d.log" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
		log_file = "%s.log" % os.path.basename(list_test[0]).split(".")[0]
		if xml_flag == True:
			xml_file = "%d-%0.2d-%0.2d__%0.2d-%0.2d-%0.2d.xml" % (dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)
		       
		# set log_flag to True by default
		log_flag = True

		return (cfg, log_file, log_flag, log_fullpath, xml_file, gui, help, list_test)
	

	def create_test_tree(self, root):
		"create the test list"
	#################################
		list_copy = []
		if os.path.isfile(root):
			return os.path.basename(root)
		else:
			list = os.listdir(root) 
			for elem in list:
				elem_copy = os.path.join(root, elem)
				if os.path.isdir(elem_copy):
					list_copy.append(self.create_test_tree(elem_copy))
				elif os.path.isfile(elem_copy) and elem_copy[-3:] == '.py':
					list_copy.append(elem)
			
			return [os.path.basename(root), list_copy]
	
	def get_error_msg(self, msg_exception):
		"this method creates the message error structure to be displayed"
	#################################
		lines = msg_exception.split('\n')
		head_msg_error = '--------------------------- Error Message ---------------------------\n' 
		tail_msg_error = '---------------------------------------------------------------------\n'
		return head_msg_error + '\n'.join(lines[0:-1]) + '\n' + tail_msg_error
	
	def help_msg(self):
		"this method creates the help message"
	#################################
		print "------------------------------------------------------------------------------"
		print "|                                                                            |" 
		print "|                                                                            |" 
		print "|         @               @          @@@@@@@@@                   @           |" 
		print "|        @ @     @   @  @@@@@@   @@@     @      @@@@    @@@@@  @@@@@@        |" 
		print "|       @   @    @   @    @     @   @    @     @    @  @         @           |" 
		print "|      @ @@@ @   @   @    @     @   @    @     @@@@@@   @@@@     @           |" 
		print "|     @       @  @   @    @     @   @    @     @            @    @           |" 
		print "|    @         @  @@@ @    @@    @@@     @      @@@@   @@@@@      @@         |" 
		print "| -------------------------------------------------------------------------- |" 
		print "| Help Message:                                                              |" 
		print "|                                                                            |" 
		print "| Synopsys:                                                                  |" 
		print "|     autotest [-cfg filename.cfg] [-log] [-gui] [-h] [directory|filename.py]|" 
		print "|                                                                            |" 
		print "| Parameter:                                                                 |" 
		print "|     -cfg         indicate using the config filename.                       |" 
		print "|                  filename.cfg is config filename.                          |" 
		print "|     -log         launche with capture of log file.                         |" 
		print "|     -logpath     custom path for log path.                                 |" 
		print "|     -gui         launche the graphical mode.                               |" 
		print "|     -h           help information.                                         |" 
		print "|     directory    directory is searched for script test file                |" 
		print "|     filename.py  script test filename.                                     |" 
		print "|                                                                            |" 
		print "------------------------------------------------------------------------------"


####################################################################################################################
if __name__ == '__main__':
	app = MyApp(False)
	app.MainLoop()

