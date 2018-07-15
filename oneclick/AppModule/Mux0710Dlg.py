#!/bin/env python
# _*_ coding: utf-8 _*_


#----------------------------------------------------------------------------
# Name:			Mux0710Dlg.py
#
# Goal:			This module manages the MUX MMI
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
#2009-2011         JM Rufflé           1.0..1.7                creation and modifications
#22-09-2011        JF Weiss            1.8.1                   add comments and light modifications

import wx
import sys, os

import traceback
import images
import cStringIO
import VarGlobal
import threading

from Output   import *

class Mux0710Dlg(wx.MiniFrame):
	def __init__(self, titre, textbox1, textbox2):
		'''	
		goal of the method : constructor	
		INPUT : 
		OUTPUT : none
		'''
		wx.MiniFrame.__init__(self, None, -1, title = titre, size=(420, 340), style = wx.SYSTEM_MENU | wx.CLOSE_BOX | wx.RESIZE_BORDER | wx.CAPTION  )
		self.SetBackgroundColour(wx.LIGHT_GREY)
		# Le verrou write_tbl_Frame_mutex sécurisé
		self.print_mutex = threading.Lock()
		
		self.LastCarOnLeftBox=""
		self.LastCarOnRightBox=""
		self.isOpen = False
		
		self.SetMinSize((420,340))
		
		#panel Haut
		clearBtn = wx.Button(self, -1, "Clear logs")
		topBox = wx.BoxSizer(wx.HORIZONTAL)
		topBox.Add(clearBtn, 0, wx.RIGHT, 15)
		
		# Panel gauche
		self.leftTextBox = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE|wx.TE_RICH|wx.TE_READONLY|wx.HSCROLL)
		self.leftTitle = wx.StaticText(self, label = textbox1)
		leftBox = wx.BoxSizer(wx.VERTICAL)
		leftBox.Add(self.leftTitle, 0, wx.TOP|wx.CENTER, 5)
		leftBox.Add(self.leftTextBox, 1, wx.EXPAND)
		
		# Panel droit
		self.rightTextBox = wx.TextCtrl(self, -1, style=wx.TE_MULTILINE|wx.TE_RICH|wx.TE_READONLY|wx.HSCROLL)
		self.rightTitle = wx.StaticText(self, label = textbox2)
		rightBox = wx.BoxSizer(wx.VERTICAL)
		rightBox.Add(self.rightTitle, 0, wx.TOP|wx.CENTER, 5)
		rightBox.Add(self.rightTextBox, 1, wx.EXPAND)
		
		# Panel bas
		bottomBox = wx.BoxSizer(wx.HORIZONTAL)
		bottomBox.Add(leftBox, 1, wx.EXPAND|wx.ALL)
		bottomBox.Add(rightBox, 1, wx.EXPAND|wx.ALL)
		
		# Panel Complet
		main = wx.BoxSizer(wx.VERTICAL)
		main.Add(topBox, 0, wx.ALL, 5)
		main.Add(bottomBox, 1, wx.EXPAND|wx.ALL, 5)
		self.SetSizer(main)
		
		self.Bind(wx.EVT_BUTTON, self.clear_logs, clearBtn)
		
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindows)

	def Open(self):
		'''	
		goal of the method : 	
		INPUT : 
		OUTPUT : none
		'''
		self.print_mutex.acquire()  # prise de verrou
		self.isOpen = True
		self.Show(True)
		self.print_mutex.release()  # relanche de verrou
	
	def IsOpen(self):
		'''	
		goal of the method : 	
		INPUT : 
		OUTPUT : none
		'''
		return self.isOpen
	
	def OnCloseWindows(self, evt):
		'''	
		goal of the method : 	
		INPUT : 
		OUTPUT : none
		'''
		dlgMux.dlg0710 = None
		self.Destroy()
	
	def clear_logs(self, event):
		'''	
		goal of the method : 	
		INPUT : 
		OUTPUT : none
		'''
		self.rightTextBox.Clear()
		self.leftTextBox.Clear()
		dlgMux.textLeft = []
		dlgMux.textRight = []
	
	def printOnRightTextBox(self, text = '', send = True):
		'''	
		goal of the method : 	
		INPUT : 
		OUTPUT : none
		'''
		if self.LastCarOnRightBox == "\r" and text[0] == "\n":
			text = text[1:]
		if text != "":
			self.LastCarOnRightBox=text[-1]
		
		if send:
			Color = VarGlobal.colorLsit[6]
		else:
			Color = VarGlobal.colorLsit[7]
		
		self.rightTextBox.SetDefaultStyle(wx.TextAttr(Color))
		self.rightTextBox.AppendText(str(text))
		self.rightTextBox.SetDefaultStyle(wx.TextAttr("black"))
		
		x,y=self.rightTextBox.PositionToXY(self.rightTextBox.GetLastPosition())
		pos=self.rightTextBox.XYToPosition(x,y-16)
		if pos < 0:
			pos = 0
		self.rightTextBox.ShowPosition(pos)
	
	def printOnLeftTextBox(self, text = '', send = True):
		'''	
		goal of the method : 	
		INPUT : 
		OUTPUT : none
		'''
		if self.LastCarOnLeftBox == "\r" and text[0] == "\n":
			text = text[1:]
		self.LastCarOnLeftBox=text[-1]
		
		if send:
			Color = VarGlobal.colorLsit[6]
		else:
			Color = VarGlobal.colorLsit[7]
		
		self.leftTextBox.SetDefaultStyle(wx.TextAttr(Color))
		self.leftTextBox.AppendText(str(text))
		self.leftTextBox.SetDefaultStyle(wx.TextAttr("black"))
		
		x,y=self.leftTextBox.PositionToXY(self.leftTextBox.GetLastPosition())
		pos=self.leftTextBox.XYToPosition(x,y-16)
		if pos < 0:
			pos = 0
		self.leftTextBox.ShowPosition(pos)
	
	def SetLeftTitle(self,title):
		'''	
		goal of the method : 	
		INPUT : 
		OUTPUT : none
		'''
		self.leftTitle.SetLabel(str(title))
	
	def SetRightTitle(self,title):
		'''	
		goal of the method : 	
		INPUT : 
		OUTPUT : none
		'''
		self.rightTitle.SetLabel(str(title))
	
	def SetDCDOnRightMuxTextBox(self, status):
		'''	
		goal of the method : 	
		INPUT : 
		OUTPUT : none
		'''
		Color = self.rightTextBox.GetDefaultStyle().GetTextColour()
		if status:
			self.rightTextBox.SetDefaultStyle(wx.TextAttr(Color,colBack=wx.Colour(187,253,189)))
		else:
			self.rightTextBox.SetDefaultStyle(wx.TextAttr(Color,colBack="white"))
	
	def SetDCDOnLeftMuxTextBox(self, status):
		'''	
		goal of the method : 	
		INPUT : 
		OUTPUT : none
		'''
		Color = self.rightTextBox.GetDefaultStyle().GetTextColour()
		if status:
			self.leftTextBox.SetDefaultStyle(wx.TextAttr(Color,colBack=wx.Colour(187,253,189)))
		else:
			self.leftTextBox.SetDefaultStyle(wx.TextAttr(Color,colBack="white"))
	
class Mux0710DlgVar():
	def __init__(self):
		'''	
		goal of the method : 	
		INPUT : 
		OUTPUT : none
		'''
		self.dlg0710 = None
		self.leftTitle = "Channel DLCI"
		self.rightTitle = "Channel DLCI"
		self.leftText = ''
		self.rightText = ''
		self.textLeft = []
		self.textRight = []
		
dlgMux = Mux0710DlgVar()

def dlg0710IsOpen():
	'''	
	goal of the method : 	
	INPUT : 
	OUTPUT : none
	'''
	return dlgMux.dlg0710 != None

def DestroyDlg0710():
	'''	
	goal of the method : 	
	INPUT : 
	OUTPUT : none
	'''
	if dlg0710IsOpen():
		dlgMux.dlg0710.Destroy()
		dlgMux.dlg0710 = None

#ouverture de la fenetre de mux 07.10
def openDlg07102(title="Mux 07.10",leftBox=dlgMux.leftTitle,rightBox=dlgMux.rightTitle):
	'''	
	goal of the method : 	
	INPUT : 
	OUTPUT : none
	'''
	pass
	if not(dlg0710IsOpen()):
		dlgMux.dlg0710 = Mux0710Dlg(title, leftBox, rightBox)
		dlgMux.dlg0710.Open()
		
		if dlgMux.textLeft != []:
			for elem in dlgMux.textLeft:
				dlgMux.dlg0710.printOnLeftTextBox(elem[0], elem[1])
		if dlgMux.textRight != []:
			for elem in dlgMux.textRight:
				dlgMux.dlg0710.printOnRightTextBox(elem[0], elem[1])
	
def printOnRightMuxTextBox(text, send = True):
	'''	
	goal of the method : 	
	INPUT : 
	OUTPUT : none
	'''
	dlgMux.textRight.append([text,send])
	if dlg0710IsOpen():
		dlgMux.dlg0710.printOnRightTextBox(text, send)

def printOnLeftMuxTextBox(text, send = True):
	'''	
	goal of the method : 	
	INPUT : 
	OUTPUT : none
	'''
	dlgMux.textLeft.append([text,send])
	if dlg0710IsOpen():
		dlgMux.dlg0710.printOnLeftTextBox(text, send)

def SetLeftBoxTitle(title):
	'''	
	goal of the method : 	
	INPUT : 
	OUTPUT : none
	'''
	dlgMux.leftTitle = title
	if dlg0710IsOpen():
		dlgMux.dlg0710.SetLeftTitle(title)

def SetRightBoxTitle(title):
	'''	
	goal of the method : 	
	INPUT : 
	OUTPUT : none
	'''
	dlgMux.rightTitle = title
	if dlg0710IsOpen():
		dlgMux.dlg0710.SetRightTitle(title)

def SetDCDOnRightMuxTextBox(status):
	'''	
	goal of the method : 	
	INPUT : 
	OUTPUT : none
	'''
	if dlg0710IsOpen():
		dlgMux.dlg0710.SetDCDOnRightMuxTextBox(status)

def SetDCDOnLeftMuxTextBox(status):
	'''	
	goal of the method : 	
	INPUT : 
	OUTPUT : none
	'''
	if dlg0710IsOpen():
		dlgMux.dlg0710.SetDCDOnLeftMuxTextBox(status)

def ResetDisplayOfDCD_OnMuxDlg():
	'''	
	goal of the method : 	
	INPUT : 
	OUTPUT : none
	'''
	if dlg0710IsOpen():
		dlgMux.dlg0710.SetDCDOnRightMuxTextBox(False)
		dlgMux.dlg0710.SetDCDOnLeftMuxTextBox(False)
