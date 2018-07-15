#!/usr/bin/env python
# _*_ coding: utf-8 _*_

#----------------------------------------------------------------------------
# Nom:		  ProcList.py
# Objet:		un secteur dans l'interface graphique qui permet de afficher 
#			   avancement de test									   
#
# Auteur:	   Bingxun HOU
#
# Version:	  AutoTest 1.0
# Date:		 Avril - Septembre 2007
# Propri�t�	 Sagemcom
#
#05/07/2012         jm seillon            1.8.8            Replacement of all text "Sagem Communication" against "Sagemcom"
#----------------------------------------------------------------------------

import wx
import sys
from datetime import datetime

# class Process List correspond la liste en bas a droite
class ProcList(wx.ListCtrl): # ProcList est une ListCtrl de type virtuel
	def __init__(self, parent, size):
		wx.ListCtrl.__init__(self, 
							 parent,
							 -1,
							 size=size,
							 style=wx.LC_REPORT|
								   wx.LC_HRULES|
								   wx.LC_VRULES)
		
		self.InsertColumn(0, "Item No.")
		self.InsertColumn(1, "File")
		self.InsertColumn(2, "Time Begin")
		self.InsertColumn(3, "Time End")
		self.InsertColumn(4, "Stat")
		
		self.SetColumnWidth(0,  60) 
		self.SetColumnWidth(1, 260)
		self.SetColumnWidth(2, 100)
		self.SetColumnWidth(3, 100)
		self.SetColumnWidth(4, 100)

	def AddItem(self, item, file, time_begin, time_end, state):
		self.index = self.InsertStringItem(sys.maxint, item)
		self.SetStringItem(self.index, 1, file)
		if type(time_begin) == datetime:
			time_begin="%0.2d:%0.2d:%0.2d:%0.3d"%(time_begin.hour, time_begin.minute, time_begin.second, time_begin.microsecond/1000)
		self.SetStringItem(self.index, 2, time_begin)
		if type(time_end) == datetime:
			time_end = "%0.2d:%0.2d:%0.2d:%0.3d"%(time_end.hour, time_end.minute, time_end.second, time_end.microsecond/1000)
		self.SetStringItem(self.index, 3, time_end)
		self.SetStringItem(self.index, 4, state)
		self.SetItemBackgroundColour(self.index, "yellow")
		self.previousState = state

	def ModifyItem(self, time_end, state):
		if type(time_end) == datetime:
			time_end = "%0.2d:%0.2d:%0.2d:%0.3d"%(time_end.hour, time_end.minute, time_end.second, time_end.microsecond/1000)
		self.SetStringItem(self.index, 3, time_end)
		self.SetStringItem(self.index, 4, state)
		if state != 'OK':
			self.SetItemBackgroundColour(self.index, "red")
		else:
			self.SetItemBackgroundColour(self.index, "white")
		self.previousState = state
	
	def Itemcount(self):
		return self.GetItemCount()
	
	def Pause(self, pause=True):
		if pause:
			self.previousColorState = self.GetItemBackgroundColour(self.index)
			self.SetItemBackgroundColour(self.index, "blue")
			self.SetStringItem(self.index, 4, "Pause")
		else:
			self.SetItemBackgroundColour(self.index, self.previousColorState)
			self.SetStringItem(self.index, 4, self.previousState)