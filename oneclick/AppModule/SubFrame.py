#-------------------------------------------------------------------------------
# Name:		SubFrame.py
# Purpose:	 This module use to create child window 
#
# Author:	  pdkhai
#
#
# Version	  1.0
#
# Created:	 2016-Dec-09
#-------------------------------------------------------------------------------
import wx
import re
import serial.tools.list_ports
import sys
import os
import subprocess
import _winreg as winreg
import itertools
from os import walk

reload(sys)  
sys.setdefaultencoding('utf8')

class Settings(wx.Dialog):
	def __init__(self, settings, *args, **kwargs):
		wx.Dialog.__init__(self, None, title='Configuration', size=(420, 500), name="Configuration")
		self.panel = wx.Panel(self)
		self.settings = settings
		self.setargs = args
		fo = open(self.settings[0], 'r')
		content = fo.read()
		fo.close()

		self.sim_ini = re.findall('SIM_INI *= *r\'(.*)(\w{3}_.{4}.ini)\'', content)
		self.sim_ini1 = re.findall('AUX_SIM_INI *= *r\'(.*)(\w{3}_.{4}.ini)\'', content)
		self.sim_ini2 = re.findall('AUX2_SIM_INI *= *r\'(.*)(\w{3}_.{4}.ini)\'', content)
		
		self.get_sim_list()
		self.get_com_ports()
		self.ModuleGUI_init()
		self.OnUpdateField('e')
		
		self.cb[0].Bind(wx.EVT_TEXT,self.OnSelectCOM1)
		self.cb[1].Bind(wx.EVT_TEXT,self.OnSelectCOM2)
		self.cb[2].Bind(wx.EVT_TEXT,self.OnSelectCOM3)
		self.cb[3].Bind(wx.EVT_TEXT,self.OnSelectCOM4)
		self.cb[4].Bind(wx.EVT_TEXT,self.OnSelectCOM5)
		self.cb[5].Bind(wx.EVT_TEXT,self.OnSelectCOM6)
		self.cb[6].Bind(wx.EVT_TEXT,self.OnSelectCOM7)
		self.cb[7].Bind(wx.EVT_TEXT,self.OnSelectCOM8)
		self.cb[8].Bind(wx.EVT_TEXT,self.OnSelectCOM9)
		self.cb4.Bind(wx.EVT_COMBOBOX,self.OnSelectSIM1)
		self.cb8.Bind(wx.EVT_COMBOBOX,self.OnSelectSIM2)
		self.cb12.Bind(wx.EVT_COMBOBOX,self.OnSelectSIM3)
		self.bt1.Bind(wx.EVT_BUTTON, self.OnClose)
		self.bt2.Bind(wx.EVT_BUTTON, self.OnOpenCfg)
		self.bt3.Bind(wx.EVT_BUTTON, self.OnRefresh)


		
		self.Bind(wx.EVT_CLOSE, self.OnClose)
		
	def ModuleGUI_init(self):
		col1 = 5
		col2 = 10 
		col3 = 130 
		col4 = 200
		col5 = 240 
		row1 = 5
		row2 = 25 
		row3 = 50
		row4 = 75
		row5 = 100
		h1 = 130
		h2 = 260
		h3 = 17
		cb_width1 = 265
		cb_width2 = 90
		sb_width1 = 400
		st_width1 = 115
		self.cb = []
		
		wx.StaticBox(self, -1, 'Module 1', (col1, row1), size=(sb_width1, h1))
		wx.StaticText(self,-1, label='UART1_COM', pos=(col2,row2), size=(st_width1,h3))
		wx.StaticText(self,-1, label='UART2_COM', pos=(col2,row3), size=(st_width1,h3))
		wx.StaticText(self,-1, label='UART3_COM', pos=(col2,row4), size=(st_width1,h3))
		wx.StaticText(self,-1, label='SIM', pos=(col2,row5), size=(st_width1,h3))
		self.cb.append(wx.ComboBox(self,-1, choices=self.port_list.keys(), style=wx.CB_DROPDOWN|wx.CB_READONLY, pos=(col3,row2), size=(cb_width1,h3)))
		self.cb.append(wx.ComboBox(self,-1, choices=self.port_list.keys(), style=wx.CB_DROPDOWN|wx.CB_READONLY, pos=(col3,row3), size=(cb_width1,h3)))
		self.cb.append(wx.ComboBox(self,-1, choices=self.port_list.keys(), style=wx.CB_DROPDOWN|wx.CB_READONLY, pos=(col3,row4), size=(cb_width1,h3)))
		self.cb4 = wx.ComboBox(self,-1, choices=self.sim_list, style=wx.CB_DROPDOWN|wx.CB_READONLY, pos=(col3,row5), size=(cb_width2,h3))
		wx.StaticBox(self, -1, 'Module 2', (col1, row1+h1), size=(sb_width1, h1))
		wx.StaticText(self,-1, label='AUX_COM',       pos=(col2,row2+h1), size=(st_width1,h3))
		wx.StaticText(self,-1, label='AUX_UART2_COM', pos=(col2,row3+h1), size=(st_width1,h3))
		wx.StaticText(self,-1, label='AUX_USB_COM',   pos=(col2,row4+h1), size=(st_width1,h3))
		wx.StaticText(self,-1, label='SIM', pos=(col2,row5+h1), size=(st_width1,h3))
		self.cb.append(wx.ComboBox(self,-1, choices=self.port_list.keys(), style=wx.CB_DROPDOWN|wx.CB_READONLY, pos=(col3,row2+h1), size=(cb_width1,h3)))
		self.cb.append(wx.ComboBox(self,-1, choices=self.port_list.keys(), style=wx.CB_DROPDOWN|wx.CB_READONLY, pos=(col3,row3+h1), size=(cb_width1,h3)))
		self.cb.append(wx.ComboBox(self,-1, choices=self.port_list.keys(), style=wx.CB_DROPDOWN|wx.CB_READONLY, pos=(col3,row4+h1), size=(cb_width1,h3)))
		self.cb8 = wx.ComboBox(self,-1, choices=self.sim_list, style=wx.CB_DROPDOWN|wx.CB_READONLY, pos=(col3,row5+h1), size=(cb_width2,h3))
		wx.StaticBox(self, -1, 'Module 3', (col1, row1+h2), size=(sb_width1, h1))
		wx.StaticText(self,-1, label='AUX2_COM',       pos=(col2,row2+h2), size=(st_width1,h3))
		wx.StaticText(self,-1, label='AUX2_UART2_COM', pos=(col2,row3+h2), size=(st_width1,h3))
		wx.StaticText(self,-1, label='AUX2_USB_COM',   pos=(col2,row4+h2), size=(st_width1,h3))
		wx.StaticText(self,-1, label='SIM', pos=(col2,row5+h2), size=(st_width1,h3))
		self.cb.append(wx.ComboBox(self,-1, choices=self.port_list.keys(), style=wx.CB_DROPDOWN|wx.CB_READONLY, pos=(col3,row2+h2), size=(cb_width1,h3)))
		self.cb.append(wx.ComboBox(self,-1, choices=self.port_list.keys(), style=wx.CB_DROPDOWN|wx.CB_READONLY, pos=(col3,row3+h2), size=(cb_width1,h3)))
		self.cb.append(wx.ComboBox(self,-1, choices=self.port_list.keys(), style=wx.CB_DROPDOWN|wx.CB_READONLY, pos=(col3,row4+h2), size=(cb_width1,h3)))
		self.cb12 = wx.ComboBox(self,-1, choices=self.sim_list, style=wx.CB_DROPDOWN|wx.CB_READONLY, pos=(col3,row5+h2), size=(cb_width2,h3))
		self.bt1 = wx.Button(self,-1, label='OK', pos=(320,430), size=(80,30))
		self.bt2 = wx.Button(self,-1, label='Open cfg...', pos=(10,430), size=(80,30))
		self.bt3 = wx.Button(self,-1, label='Refresh', pos=(95,430), size=(80,30))

	def serial_ports(self):
		""" Lists serial port names

			:raises EnvironmentError:
				On unsupported or unknown platforms
			:returns:
				A list of the serial ports available on the system
		"""
		if sys.platform.startswith('win'):
			ports = ['COM%s' % (i + 1) for i in range(256)]
		elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
			# this excludes your current terminal "/dev/tty"
			ports = glob.glob('/dev/tty[A-Za-z]*')
		elif sys.platform.startswith('darwin'):
			ports = glob.glob('/dev/tty.*')
		else:
			raise EnvironmentError('Unsupported platform')

		result = []
		for port in ports:
			try:
				s = serial.Serial(port)
				s.close()
				result.append(port)
			except (OSError, serial.SerialException):
				pass
		return result
		
	def get_com_registry(self):
		path = 'HARDWARE\\DEVICEMAP\\SERIALCOMM'
		key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, path)
		ports = []

		for i in itertools.count():
			try:
				ports.append(winreg.EnumValue(key, i))
			except EnvironmentError:
				break
		return ports

	def get_com_ports(self):
		ports = list(serial.tools.list_ports.comports())
		self.port_list = {}
		for p in ports:
			self.port_list[p[1].replace('(','').replace(')','')] = p[0]
		subports = self.get_com_registry()
		for sp in subports:
			if sp[1] not in self.port_list.values():
				self.port_list[sp[1]] = sp[1]

	def setCOMvalue(self,val,item):
		for key in self.port_list.keys():
			if val in key and key[len(key)-3-len(val):len(key)-len(val)] == 'COM':
				item.SetValue(key)
				
	def get_sim_list(self):
		self.sim_list = []
		for (dirpath, dirnames, filenames) in walk(self.sim_ini[0][0]):
			self.sim_list.extend(filenames)
			break

	def OnClose(self, e):
		self.Destroy()


	def onCancel(self, e):
		self.EndModal(wx.ID_CANCEL)

	def onOk(self, e):
		for i in range(3):
			self.settings[i] = self.checkboxes[i].GetValue()
		self.EndModal(wx.ID_OK)

	def GetSettings(self):
		return self.settings	

	def file_process(func):
		def inner(self,*args, **kwargs):
			fo = open(self.settings[0], 'r')
			self.content = fo.read()
			fo.close()
			func(self,*args, **kwargs)
			fo = open(self.settings[0], 'w')
			fo.write(self.content)
			fo.close()
		return inner	
		
	
	@file_process
	def OnSelectCOM1(self, event):
		st = '\nUART1_COM = %s'%(self.port_list[event.GetString()].replace('COM',''))
		self.content = re.sub('\nUART1_COM.*',st, self.content)
	
	@file_process
	def OnSelectCOM2(self, event):
		st = '\nUART2_COM = %s'%(self.port_list[event.GetString()].replace('COM',''))
		self.content = re.sub('\nUART2_COM.*',st, self.content)
		
	@file_process
	def OnSelectCOM3(self, event):
		st = '\nUART3_COM = %s'%(self.port_list[event.GetString()].replace('COM',''))
		self.content = re.sub('\nUART3_COM.*',st, self.content)

	@file_process
	def OnSelectCOM4(self, event):
		st = '\nAUX_COM = %s'%(self.port_list[event.GetString()].replace('COM',''))
		self.content = re.sub('\nAUX_COM.*',st, self.content)

	@file_process
	def OnSelectCOM5(self, event):
		st = '\nAUX_UART2_COM = %s'%(self.port_list[event.GetString()].replace('COM',''))
		self.content = re.sub('\nAUX_UART2_COM.*',st, self.content)

	@file_process
	def OnSelectCOM6(self, event):
		st = '\nAUX_USB_COM = %s'%(self.port_list[event.GetString()].replace('COM',''))
		self.content = re.sub('\nAUX_USB_COM.*',st, self.content)

	@file_process
	def OnSelectCOM7(self, event):
		st = '\nAUX2_COM = %s'%(self.port_list[event.GetString()].replace('COM',''))
		self.content = re.sub('\nAUX2_COM.*',st, self.content)

	@file_process
	def OnSelectCOM8(self, event):
		st = '\nAUX2_UART2_COM = %s'%(self.port_list[event.GetString()].replace('COM',''))
		self.content = re.sub('\nAUX2_UART2_COM.*',st, self.content)

	@file_process
	def OnSelectCOM9(self, event):
		st = '\nAUX2_USB_COM = %s'%(self.port_list[event.GetString()].replace('COM',''))
		self.content = re.sub('\nAUX2_USB_COM.*',st, self.content)

	@file_process
	def OnSelectSIM1(self, event):
		st = '\nSIM_INI = r\'%s%s\''%(self.sim_ini[0][0],event.GetString())
		self.content = re.sub('\nSIM_INI.*',st, self.content)
	
	@file_process
	def OnSelectSIM2(self, event):
		st = '\nAUX_SIM_INI = r\'%s%s\''%(self.sim_ini[0][0],event.GetString())
		self.content = re.sub('\nAUX_SIM_INI.*',st, self.content)
		
	@file_process
	def OnSelectSIM3(self, event):
		st = '\nAUX2_SIM_INI = r\'%s%s\''%(self.sim_ini[0][0],event.GetString())
		self.content = re.sub('\nAUX2_SIM_INI.*',st, self.content)
		
	def OnUpdateField(self,event):
		fo = open(self.settings[0], 'r')
		content = fo.read()
		fo.close()
		self.com = []
		com1_1 = re.findall('UART1_COM *= *([\d]*)\n', content)
		com1_2 = re.findall('UART2_COM *= *([\d]*)\n', content)
		com1_3 = re.findall('UART3_COM *= *([\d]*)\n', content)
		com1_4 = re.findall('PowerSupply *= *r\'(.*)\'\n', content)
		com1_5 = re.findall('AUX_COM *= *([\d]*)\n', content)
		com1_6 = re.findall('AUX_UART2_COM *= *([\d]*)\n', content)
		com1_7 = re.findall('AUX_USB_COM *= *([\d]*)\n', content)
		com1_8  = re.findall('AUX2_COM *= *([\d]*)\n', content)
		com1_9  = re.findall('AUX2_UART2_COM *= *([\d]*)\n', content)
		com1_10 = re.findall('AUX2_USB_COM *= *([\d]*)\n', content)
		self.sim_ini = re.findall('SIM_INI *= *r\'(.*)(\w{3}_.{4}.ini)\'', content)
		self.sim_ini1 = re.findall('AUX_SIM_INI *= *r\'(.*)(\w{3}_.{4}.ini)\'', content)
		self.sim_ini2 = re.findall('AUX2_SIM_INI *= *r\'(.*)(\w{3}_.{4}.ini)\'', content)
		for com in [com1_1,com1_2,com1_3,com1_5,com1_6,com1_7,com1_8,com1_9,com1_10]:
			if len(com) > 0:
				try:
					int(com[0])
				except ValueError:
					print 'Invalid COM in cfg file'
				self.com.append(com[0])
			else:
				self.com.append('0')
		
		for idx in range(len(self.com)):
			self.setCOMvalue(self.com[idx],self.cb[idx])
		self.cb4.SetValue(self.sim_ini[0][1])
		self.cb8.SetValue(self.sim_ini1[0][1])
		self.cb12.SetValue(self.sim_ini2[0][1])
		
	def OnOpenCfg(self, event):
		#os.startfile(self.settings[0])
		notepadPath = r'C:\Windows\System32\notepad.exe'
		subprocess.Popen("%s %s" % (notepadPath, self.settings[0]))
		
	def OnRefresh(self, event):
		self.get_com_ports()
		self.get_sim_list()
		for cb in self.cb:
			cb.Destroy()
		self.cb4.Destroy()
		self.cb8.Destroy()
		self.cb12.Destroy()
		self.ModuleGUI_init()
		self.OnUpdateField('e')