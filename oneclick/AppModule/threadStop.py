#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# source: inspire de: http://mail.python.org/pipermail/python-list/2004-May/260937.html
 
#date              who                 version                 modification
#xx-05-2012        JM Seillon          1.8.4                   changes for GNSS feature

import sys
import threading
import VarGlobal
from datetime import datetime

##############################################################################
pause	  	 = False
PauseLock 	 = threading.Lock()
kill	  	 = False
displayTrace = False

# Function to pause all threads
def PauseAllThread():
	global pause,PauseLock
	#print 'global pause'
	pause = True
	PauseLock.acquire()

# Function to continue all threads
def ContinueAllThread():
	global pause,PauseLock
	#print 'global continue'
	if pause:
		pause = False
		PauseLock.release()

# Function to get a status of pause all threads
def GetPauseStatus(self):
	global pause
	return pause

# Function to stop all threads
def StopAllThread():
	global pause,PauseLock,kill
	if pause:
		PauseLock.release()
	pause = False
	kill = True

'''def WaitForMultipleEvent(eventlist, WaitAll ,timeout):		# function under test
	EndOfEvent = threading.Event()
	
	def __waitEvent(event, timeout, EndOfEvent):
		event.wait(timeout)
		event.set()
		EndOfEvent.set()
	
	for event in eventlist:
		threading.Thread(target=__waitEvent, args=[event,timeout,EndOfEvent]).start()
	
	allEventRecv = False
	while not(allEventRecv):
		EndOfEvent.wait(timeout+1)
		
		for event in eventlist:
			allEventRecv = True
			if WaitAll:
				allEventRecv = allEventRecv and event.isSet()
			else:
				break
'''


# This class is able to stop or break a thread at the end of each line
class Thread(threading.Thread):
	"""Sous-classe de threading.Thread, avec une methode stop() et pause()"""
	
	def __init__(self, *args, **keywords):
		global kill
		threading.Thread.__init__(self, *args, **keywords)

		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			print "begin Thread.__init__()\r\n"
		
		kill					= False
		self.__kill				= False
		self.__pause			= False
		self.__PauseLock		= threading.Lock()		# Lock to break the excecution
		self.__EndOfThreadEvent = threading.Event()		# Event to detect the end of Thread

	def start(self):
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			print "begin Thread.start()\r\n"
		self.__EndOfThreadEvent.clear()					# Reset Event to detect the end of Thread
		self.run_sav = self.run
		self.run = self.run2
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			print "thread Thread is launched\r\n"
			print "@@@thread launched@@@\r\n"
		threading.Thread.start(self)
		#if VarGlobal.DEBUG_LEVEL == "DEBUG":
		#	print "thread is starting"
	
	def Pause(self):
		self.__pause = True
		self.__PauseLock.acquire()
	
	def Continue(self):
		if self.__pause:
			self.__pause = False
			self.__PauseLock.release()
	
	def stop(self):
		if self.__pause:
			self.__PauseLock.release()
			self.__pause = False
		self.__kill = True
	
	def run2(self):
		sys.settrace(self.__trace)
		self.run_sav()
		self.run = self.run_sav
		self.__EndOfThreadEvent.set()					# Set Event to detect the end of Thread
	
	def __trace(self, frame, event, arg):
		global pause, PauseLock, kill, displayTrace
		'''if frame.f_globals["__name__"] == "threading" or frame.f_globals["__name__"] == "serial.serialwin32" or frame.f_globals["__name__"] == "__main__" or frame.f_globals["__name__"] == "Test":
			print "thread", frame.f_globals["__name__"], frame.f_lineno, event, arg
		'''
		'''if displayTrace and frame.f_globals["__name__"] in ["AppModule.DemoToolScripts","AppModule.InputDemoTool"]:
			print "DEBUG:", frame.f_globals["__name__"], frame.f_lineno, event, arg
		'''
		if self.__kill or kill:							# Test if stop is require
			if event == 'line':
				raise SystemExit()
		if pause and event == 'line':					# Test if global pause is require
			#print "global pause"
			PauseLock.acquire()
			PauseLock.release()
		if self.__pause and event == 'line':			# Test if pause is require
			#print "local pause"
			self.__PauseLock.acquire()
			self.__PauseLock.release()
		return self.__trace
	
	def DisplayTrace(self,state):
		global displayTrace
		displayTrace = state
	
	def GetPauseStatus(self):
		return self.__pause
	
	def WaitEndOfThread(self, timeout=None):			# timeout in milliseconds
		try:
			if timeout != None:
				start = datetime.now
				self.__EndOfThreadEvent.wait(timeout/1000.0)
				diff = datetime.now - start
				diff_time = diff.seconds + diff.microseconds / 1000000.0
				self.__EndOfThreadEvent.clear()
				return diff_time < timeout
			else:
				self.__EndOfThreadEvent.wait()
				self.__EndOfThreadEvent.clear()
				return True
		except SystemExit:
			self.__kill = True
			raise SystemExit()