#!/usr/bin/env python
# _*_ coding: utf-8 _*_

#----------------------------------------------------------------------------
# Name:			Mux0710.py
#
# Goal:			This module manages the frame object, some constants and some basic functions
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
#2009-2011         JM Ruffle                               1.0..1.7                creation and modifications
#22-09-2011        JF Weiss            1.8.1                   add comments and light modifications
#28-02-2012        JF Weiss            1.8.2                   bug 3442
#01-06-2012        JF Weiss            1.8.6                   bug 4028 (Flase instead of False)
#18-12-2012        JF Weiss            1.9.3                   5153 fix a regression done by g178317 in 1.9.2. MUX doesn't workanymore!!!
#xx-03-2013        Gary Zhang          1.9.6                   advanced MUX


import VarGlobal
from copy import copy
#from Mux0710Dlg import *

class InitFrame:
	'''
	This class collects all varaibles used for frame decoding
	'''
	def __init__(self):
		self.ReceivedFlag=0
		self.Address=''
		self.DLCI=-1
		self.CR=-1
		self.Control=''
		self.FrameType=-1
		self.PF=-1
		self.LengthFirst=-1
		self.LengthLast=-1
		self.NbLength=-1
		self.length=-1
		self.Info=[]
		self.Fcs=''
		self.Flag=''
		self.Frame=[]
		self.FrameHex=[]
		self.dt=None
		self.crc=False
	
	def strInfo(self):
		return data2string(self.Info)
'''
class Frame0710Dlg:
	def __init__(self):
		self.started = False
		self.dlg = None
'''
# init
param=[0,0,0,0,0]

DecodedFrame = InitFrame()
CodedFrame	 = InitFrame()

BASIC_FLAG=0xF9
#+ Advanced mode support
ADVANCE_FLAG=0x7E
#- Advanced mode support
NEW_FRAME=0
WAIT_ADDRESS=1
WAIT_CTRL=2
WAIT_LENGTH_FIRST=3
WAIT_LENGTH_LAST=4
WAIT_INFO=5
WAIT_FCS=6
WAIT_FLAG=7

#Significant bit
EA	= 0x01
C_R	= 0x02
P_F	= 0x10

# Control field
SABM = 0x2F
UA	 = 0x63
DM	 = 0x0F
DISC = 0x43
UIH	 = 0xEF
UI	 = 0x03

PSC			= 0x40
CLD			= 0xC0
Test_Frame	= 0x20
Fcon		= 0xA0
Fcoff		= 0x60
MSC			= 0xE0
NSC			= 0x10
SNC			= 0xD0

# type param
CR					= 0
CR_TYPE				= 1
PF					= 1
DLCI				= 2
DLCI0				= 0
LENGTH				= 3
DATA				= 4
TYPE				= 4
UNSUPPORTED_CMD		= 2
SERVICE				= 4
VOICE				= 5
SIGNAL				= 3

# CRC table
crctable = [	#reversed, 8-bit, poly=0x07
				0x00, 0x91, 0xE3, 0x72, 0x07, 0x96, 0xE4, 0x75,  0x0E, 0x9F, 0xED, 0x7C, 0x09, 0x98, 0xEA, 0x7B,
				0x1C, 0x8D, 0xFF, 0x6E, 0x1B, 0x8A, 0xF8, 0x69,  0x12, 0x83, 0xF1, 0x60, 0x15, 0x84, 0xF6, 0x67,
				0x38, 0xA9, 0xDB, 0x4A, 0x3F, 0xAE, 0xDC, 0x4D,  0x36, 0xA7, 0xD5, 0x44, 0x31, 0xA0, 0xD2, 0x43,
				0x24, 0xB5, 0xC7, 0x56, 0x23, 0xB2, 0xC0, 0x51,  0x2A, 0xBB, 0xC9, 0x58, 0x2D, 0xBC, 0xCE, 0x5F,
				
				0x70, 0xE1, 0x93, 0x02, 0x77, 0xE6, 0x94, 0x05,  0x7E, 0xEF, 0x9D, 0x0C, 0x79, 0xE8, 0x9A, 0x0B,
				0x6C, 0xFD, 0x8F, 0x1E, 0x6B, 0xFA, 0x88, 0x19,  0x62, 0xF3, 0x81, 0x10, 0x65, 0xF4, 0x86, 0x17,
				0x48, 0xD9, 0xAB, 0x3A, 0x4F, 0xDE, 0xAC, 0x3D,  0x46, 0xD7, 0xA5, 0x34, 0x41, 0xD0, 0xA2, 0x33,
				0x54, 0xC5, 0xB7, 0x26, 0x53, 0xC2, 0xB0, 0x21,  0x5A, 0xCB, 0xB9, 0x28, 0x5D, 0xCC, 0xBE, 0x2F,
				
				0xE0, 0x71, 0x03, 0x92, 0xE7, 0x76, 0x04, 0x95,  0xEE, 0x7F, 0x0D, 0x9C, 0xE9, 0x78, 0x0A, 0x9B,
				0xFC, 0x6D, 0x1F, 0x8E, 0xFB, 0x6A, 0x18, 0x89,  0xF2, 0x63, 0x11, 0x80, 0xF5, 0x64, 0x16, 0x87,
				0xD8, 0x49, 0x3B, 0xAA, 0xDF, 0x4E, 0x3C, 0xAD,  0xD6, 0x47, 0x35, 0xA4, 0xD1, 0x40, 0x32, 0xA3,
				0xC4, 0x55, 0x27, 0xB6, 0xC3, 0x52, 0x20, 0xB1,  0xCA, 0x5B, 0x29, 0xB8, 0xCD, 0x5C, 0x2E, 0xBF,
				
				0x90, 0x01, 0x73, 0xE2, 0x97, 0x06, 0x74, 0xE5,  0x9E, 0x0F, 0x7D, 0xEC, 0x99, 0x08, 0x7A, 0xEB,
				0x8C, 0x1D, 0x6F, 0xFE, 0x8B, 0x1A, 0x68, 0xF9,  0x82, 0x13, 0x61, 0xF0, 0x85, 0x14, 0x66, 0xF7,
				0xA8, 0x39, 0x4B, 0xDA, 0xAF, 0x3E, 0x4C, 0xDD,  0xA6, 0x37, 0x45, 0xD4, 0xA1, 0x30, 0x42, 0xD3,
				0xB4, 0x25, 0x57, 0xC6, 0xB3, 0x22, 0x50, 0xC1,  0xBA, 0x2B, 0x59, 0xC8, 0xBD, 0x2C, 0x5E, 0xCF
			]
'''
mux0710Dlg = Frame0710Dlg()
def startDlg():
	if not(mux0710Dlg.started):
		mux0710Dlg.dlg = Mux0710Dlg( "Mux 07.10", "AT Channel", "Data Channel")
		mux0710Dlg.started = True
'''
def string2data(s):
	tab=[]
	for elem in range(len(s)):
		tab.append(ord(s[elem]))
	return tab
	
def data2string(data):
	if len(data)>0:
		s=''
		for elem in data:
			if elem != 0:
				s+=chr(elem)
		return s
	else:
		return None

def table2hex(table):
	tableHex=[]
	# transforme en string HEX
	for elem in table:
		tableHex.append("0x%.2X" % elem)
	return tableHex

def reInitFrame():
	DecodedFrame.ReceivedFlag=0
	DecodedFrame.Address=''
	DecodedFrame.DLCI=-1
	DecodedFrame.CR=-1
	DecodedFrame.Control=''
	DecodedFrame.FrameType=-1
	DecodedFrame.PF=-1
	DecodedFrame.LengthFirst=0
	DecodedFrame.LengthLast=0
	DecodedFrame.NbLength=0
	DecodedFrame.length=0
	DecodedFrame.Info=[]
	DecodedFrame.Fcs=''
	DecodedFrame.Flag=''
	DecodedFrame.Frame=[]
	DecodedFrame.FrameHex=[]
	DecodedFrame.crc=False

def WaitMoreInfo():
	if len(DecodedFrame.Info)>=DecodedFrame.length:
		return False
	else:
		return True

def decodeTrame(resultat, display=True):
	multiFrame=frameVierge=[]
	if resultat == []:
		VarGlobal.myColor = VarGlobal.colorLsit[8] 
		print "!!! Failed, Frame not receive"
		return InitFrame()
	
	for elem in resultat:
		if elem == []:
			VarGlobal.myColor = VarGlobal.colorLsit[8] 
			print "!!! Failed, Frame not receive"
			if len(resultat) != 1:
				multiFrame.append(InitFrame())
				return multiFrame
			else:
				 return frameVierge
			break
		
		frame = elem.tabLines[0]
		reInitFrame()
		
		DecodedFrame.Frame = frame[0]
		DecodedFrame.FrameHex = frame[1]
		frame=frame[0]
		DecodAutoState = NEW_FRAME
		
		for elem in frame:
			if   DecodAutoState == NEW_FRAME:
				#print "case_NewFrame"
				if elem == BASIC_FLAG:
					DecodAutoState = WAIT_ADDRESS
				else:
					reInitFrame()
			
			elif DecodAutoState == WAIT_ADDRESS:
				#print "case_WaitAddress"
				if elem == BASIC_FLAG:
					DecodedFrame.ReceivedFlag+=1
				else:
					DecodedFrame.Address=elem
					DecodAutoState = WAIT_CTRL
			
			elif DecodAutoState == WAIT_CTRL:
				#print "case_Ctrl"
				DecodedFrame.Control=elem
				DecodAutoState = WAIT_LENGTH_FIRST
			
			elif DecodAutoState == WAIT_LENGTH_FIRST:
				#print "case_LengthFirst"
				LengthFirst=elem
				DecodedFrame.LengthFirst=LengthFirst
				if LengthFirst & EA == EA:
					DecodedFrame.NbLength = 1
					DecodedFrame.length = DecodedFrame.LengthFirst>>1
					if LengthFirst == 1:
						DecodAutoState = WAIT_FCS
					else:
						DecodAutoState = WAIT_INFO
				else:
					DecodAutoState = WAIT_LENGTH_LAST
			
			elif DecodAutoState == WAIT_LENGTH_LAST:
				#print "case_LengthLast"
				LengthLast=elem
				DecodedFrame.LengthLast=LengthLast
				DecodedFrame.NbLength = 2
				DecodedFrame.length = (DecodedFrame.LengthFirst>>1) + (DecodedFrame.LengthLast<<7)
				if DecodedFrame.LengthLast==0 and DecodedFrame.LengthFirst==0:
					DecodAutoState = WAIT_FCS
				else:
					DecodAutoState = WAIT_INFO
			
			elif DecodAutoState == WAIT_INFO:
				#print "case_Info"
				Info=elem
				DecodedFrame.Info.append(Info)
				
				if(WaitMoreInfo() == False):
					DecodAutoState = WAIT_FCS
			
			elif DecodAutoState == WAIT_FCS:
				#print "case_Fcs"
				Fcs=elem
				DecodedFrame.Fcs=Fcs
				DecodAutoState = WAIT_FLAG
			
			elif DecodAutoState == WAIT_FLAG:
				#print "case_Flag"
				DecodedFrame.Flag = elem
				#return WAIT_CTRL
			else:
				pass
		
		DecodedFrame.DLCI = DecodedFrame.Address >> 2
		DecodedFrame.CR	 = DecodedFrame.Address & 0x02
		
		DecodedFrame.PF = DecodedFrame.Control & 0x01
		DecodedFrame.FrameType  = DecodedFrame.Control & 0xEF
		
		DecodedFrame.crc = CRC_Verify(DecodedFrame)
		VarGlobal.myColor = VarGlobal.colorLsit[8] 
		if display:
			if DecodedFrame.crc:
				if VarGlobal.MODE != VarGlobal.DEMO_MODE:
					print "--->  Success <CRC OK>"
				else:
					print ""
			else:
				print "---> Fail <CRC error>"
		
		if len(resultat) != 1:
			multiFrame.append(copy(DecodedFrame))
			DecodAutoState = NEW_FRAME
		
	if len(resultat) != 1:
		return multiFrame
	else:
		return DecodedFrame

def SetAddress(cr, dlci):
	if(dlci > 63):
		return False
	
	if(cr != 0):
		CodedFrame.Address = EA + C_R + (dlci << 2)
	else:
		CodedFrame.Address = EA + (dlci << 2)

	return True

def SetControl(pf, Ctrl):
	if(pf != 0):
		CodedFrame.Control = P_F + Ctrl
	else:
		CodedFrame.Control = Ctrl
	CodedFrame.FrameType = Ctrl
	return True
#+ Advanced mode support
def SetData(adv, data=[]):
#- Advanced mode support
	if len(data) != 0:
		CodedFrame.Info = data
	#bug 3442
	#SetLength(len(data)*2) was called. The *2 was to shift the byte on the left (the last bit is EA bit)
	#but checks are done on this length. So, the shift is done after the checks in called function
	SetLength(len(data))
#+ Advanced mode support
	CRC_Calculate(adv)
#- Advanced mode support

def SetLength(length):
	# frame too long
	if(length >= 0x8000):
		return 0
	
	if(length >= 0x80):
		CodedFrame.NbLength  = 2
		Temp = length % 128
		
		#bug 3442 - the last bit is the EA bit, so shift
		CodedFrame.LengthFirst = Temp << 1
		CodedFrame.LengthLast = (length - Temp)>>7
	else:
		CodedFrame.NbLength = 1
		Temp = length % 128
		
		#bug 3442 - 
		CodedFrame.LengthFirst = (Temp << 1)  + EA
		CodedFrame.LengthLast = 0
	CodedFrame.length = length << 1
	
#+ Advanced mode support
def CRC_Calculate(adv):
#- Advanced mode support	#only for UIH frames
	#Init
	m_FCS = 0xFF
	
	frame = []
	frame.append(CodedFrame.Address)
	frame.append(CodedFrame.Control)
#+ Advanced mode support
	if adv == False:
		frame.append(CodedFrame.LengthFirst)
		if CodedFrame.NbLength == 2:
			frame.append(CodedFrame.LengthLast)
#- Advanced mode support
	for elem in frame:
		m_FCS = crctable[m_FCS^elem]

	# Ones complement
	CodedFrame.Fcs = 0xFF - m_FCS

def CRC_Verify(Frame):
	#Init
	m_FCS = 0xFF
	
	frame = []
	frame.append(Frame.Address)
	frame.append(Frame.Control)
#+ Advanced mode support
	if VarGlobal.AdvancedMode == False:
		frame.append(Frame.LengthFirst)
		if Frame.NbLength == 2:
			frame.append(Frame.LengthLast)
#- Advanced mode support
	if Frame.Control & 0xEF == UI:
		for i in range(Frame.length):
			frame.append(Frame.Info[i])
	
	for elem in frame:
		m_FCS = crctable[m_FCS^elem]

	
	#njf v1.8.1 a virer
	#m_FCS = crctable[m_FCS^Frame.Fcs]
	#if VarGlobal.DEBUG_LEVEL == "DEBUG":
		#print "Frame.Fcs = " + str(hex(Frame.Fcs))
		#print "computed CRC = " + str(hex(m_FCS))
	#if(m_FCS == Frame.Fcs):
		#FCS is OK
		#return True
	#else:
		#FCS is not OK
		#return False
	#njf fin a virer
	
	#njf v1.8.1 code original a remettre
	# Ones complement
	m_FCS = 0xFF - m_FCS
	if VarGlobal.DEBUG_LEVEL == "DEBUG":
		print "	DEBUG	Frame.Fcs = " + str(hex(Frame.Fcs))
		print "	DEBUG	computed CRC = " + str(hex(m_FCS))
	if(m_FCS == Frame.Fcs):
		#FCS is OK
		return True
	else:
		#FCS is not OK
		return False
	#njf v1.8.1 fin code original a remettre

def MakeFrame():
	# generate frame
	CodedFrame.Frame = []
	CodedFrame.FrameHex = []
	
	CodedFrame.Frame.append(BASIC_FLAG)
	CodedFrame.Frame.append(CodedFrame.Address)
	CodedFrame.Frame.append(CodedFrame.Control)
	CodedFrame.Frame.append(CodedFrame.LengthFirst)
	if CodedFrame.NbLength == 2:
		CodedFrame.Frame.append(CodedFrame.LengthLast)
	if CodedFrame.length != 0:
		for i in range(CodedFrame.length/2):
			CodedFrame.Frame.append(CodedFrame.Info[i])
	CodedFrame.Frame.append(CodedFrame.Fcs)
	CodedFrame.crc = True
	CodedFrame.Frame.append(BASIC_FLAG)
	CodedFrame.FrameHex = table2hex(CodedFrame.Frame)
#+ Advanced mode support
def MakeFrameAdv():
	# generate frame
	CodedFrame.Frame = []
	CodedFrame.FrameHex = []
	
	CodedFrame.Frame.append(ADVANCE_FLAG)
	if (CodedFrame.Address == 0x7D or CodedFrame.Address == 0x7E):
		CodedFrame.Frame.append(0x7D)
	CodedFrame.Frame.append(CodedFrame.Address)
	if (CodedFrame.Control == 0x7D or CodedFrame.Control == 0x7E):
		CodedFrame.Frame.append(0x7D)
	CodedFrame.Frame.append(CodedFrame.Control)
	if CodedFrame.length != 0:
		for i in range(CodedFrame.length/2):
			CodedFrame.Frame.append(CodedFrame.Info[i])
	if (CodedFrame.Fcs == 0x7D or CodedFrame.Fcs == 0x7E):
		CodedFrame.Frame.append(0x7D)
	CodedFrame.Frame.append(CodedFrame.Fcs)
	CodedFrame.crc = True
	CodedFrame.Frame.append(ADVANCE_FLAG)
	CodedFrame.FrameHex = table2hex(CodedFrame.Frame)
#- Advanced mode support
#+ Advanced mode support
def buildFrame(type, Param, adv):
	if isString(param[DATA]):
		param[DATA]=string2data(param[DATA])	
	
	if   type == SABM:
		SetAddress( Param[CR], Param[DLCI] )
		SetControl( Param[PF], SABM )
		SetData(adv=adv)
		
	elif type == UA:
		SetAddress( Param[CR], Param[DLCI] )
		SetControl( Param[PF], UA )
		SetData(adv=adv)
		
	elif type == DM:
		SetAddress( Param[CR], Param[DLCI] )
		SetControl( Param[PF], DM )
		SetData(adv=adv)
		
	elif type == DISC:
		SetAddress( Param[CR], Param[DLCI] )
		SetControl( Param[PF], DISC)
		SetData(adv=adv)
	
	elif type == UIH:
		SetAddress( Param[CR], Param[DLCI] )
		SetControl( Param[PF], UIH )
		SetData(adv, Param[DATA])
	
	elif type == UI:
		SetAddress( Param[CR], Param[DLCI] )
		SetControl( Param[PF], UI )
		SetData(adv, Param[DATA])
	
	if adv == False:
		MakeFrame()
	else:
		MakeFrameAdv()
	CodedFrame.DLCI = Param[DLCI]
	CodedFrame.Info = Param[DATA]
	
	return CodedFrame
#- Advanced mode support
def buildUIHFrame(dlci, cmd, cr = 1, pf = 0):
	param[CR]=cr
	param[DLCI]=dlci
	param[PF]=pf
	
	if isString(cmd):
		param[DATA]=string2data(cmd)
	elif isList(cmd):
		ok = True
		for elem in cmd:
			if isInt(cmd[0]):
				ok = ok & True
			else:
				ok = ok & False
		
		if ok:
			param[DATA] = cmd
		else:
			print "error command format in buildUIHFrame"
	else:
		print "error command format in buildUIHFrame"
	
	return buildFrame(UIH,param)

def isString(cmd):
	return type(cmd) == str

def isList(cmd):
	return type(cmd) == list

def isInt(cmd):
	return type(cmd) == int
