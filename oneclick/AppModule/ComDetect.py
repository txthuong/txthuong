##########################################################################
##
##  This is a modification of the original WndProcHookMixin by Kevin Moore,
##  modified to use ctypes only instead of pywin32, so it can be used
##  with no additional dependencies in Python 2.5
##
##########################################################################

import ctypes
from ctypes import wintypes

import wx

GWL_WNDPROC = -4
WM_DESTROY  = 2
DBT_DEVTYP_PORT			   = 0x00000003  # device Port
DBT_DEVTYP_DEVICEINTERFACE = 0x00000005  # device interface class
DBT_DEVICEREMOVECOMPLETE   = 0x8004  	 # device is gone
DBT_DEVICEARRIVAL		   = 0x8000  	 # system detected a new device
WM_DEVICECHANGE			   = 0x0219

## It's probably not neccesary to make this distinction, but it never hurts to be safe
if 'unicode' in wx.PlatformInfo:
	SetWindowLong  = ctypes.windll.user32.SetWindowLongW
	CallWindowProc = ctypes.windll.user32.CallWindowProcW
else:
	SetWindowLong  = ctypes.windll.user32.SetWindowLongA
	CallWindowProc = ctypes.windll.user32.CallWindowProcA

## Create a type that will be used to cast a python callable to a c callback function
WndProcType = ctypes.WINFUNCTYPE(ctypes.c_long, ctypes.c_int, ctypes.c_uint, ctypes.c_int, ctypes.c_int)

class DEV_BROADCAST_DEVICEINTERFACE(ctypes.Structure):
	_fields_ = [("dbcc_size", ctypes.c_ulong),
				("dbcc_devicetype", ctypes.c_ulong),
				("dbcc_reserved", ctypes.c_ulong),
				("dbcc_name", ctypes.c_wchar * 256)]


class DEV_BROADCAST_HDR(ctypes.Structure):
    _fields_ = [("dbch_size", wintypes.DWORD),
                ("dbch_devicetype", wintypes.DWORD),
                ("dbch_reserved", wintypes.DWORD)]


class WndProcHookMixin:
	"""
		This class can be mixed in with any wxWindows window class in order to hook it's WndProc function. 
		You supply a set of message handler functions with the function addMsgHandler. When the window receives that
		message, the specified handler function is invoked. If the handler explicitly returns False then the standard 
		WindowProc will not be invoked with the message. You can really screw things up this way, so be careful. 
		This is not the correct way to deal with standard windows messages in wxPython (i.e. button click, paint, etc) 
		use the standard wxWindows method of binding events for that. This is really for capturing custom windows messages
		or windows messages that are outside of the wxWindows world.
	"""
	def __init__(self):
		self.__msgDict = {}
		## We need to maintain a reference to the WndProcType wrapper
		## because ctypes doesn't
		self.__localWndProcWrapped = None
		self.rtnHandles = []

	def hookWndProc(self):
		self.__localWndProcWrapped = WndProcType(self.localWndProc)
		self.__oldWndProc = SetWindowLong(self.GetHandle(),
										GWL_WNDPROC,
										self.__localWndProcWrapped)
	def unhookWndProc(self):
		SetWindowLong(self.GetHandle(),
						GWL_WNDPROC,
						self.__oldWndProc)

		## Allow the ctypes wrapper to be garbage collected
		self.__localWndProcWrapped = None

	def addMsgHandler(self,messageNumber,handler):
		self.__msgDict[messageNumber] = handler

	def localWndProc(self, hWnd, msg, wParam, lParam):
		# call the handler if one exists
		# performance note: has_key is the fastest way to check for a key
		# when the key is unlikely to be found
		# (which is the case here, since most messages will not have handlers).
		# This is called via a ctypes shim for every single windows message 
		# so dispatch speed is important
		if self.__msgDict.has_key(msg):
			# if the handler returns false, we terminate the message here
			# Note that we don't pass the hwnd or the message along
			# Handlers should be really, really careful about returning false here
			if self.__msgDict[msg](wParam,lParam) == False:
				return

		# Restore the old WndProc on Destroy.
		if msg == WM_DESTROY: self.unhookWndProc()

		return CallWindowProc(self.__oldWndProc,
								hWnd, msg, wParam, lParam)
	
	def hookMsgHandler(self,handlerArrival,handlerRemoved):
		self.handlerArrival = handlerArrival
		self.handlerRemoved = handlerRemoved
		self.addMsgHandler(WM_DEVICECHANGE,self.__onDeviceChange)
		self.hookWndProc()
	
	def __onDeviceChange(self,wParam,lParam):
		if lParam:
			dbh = DEV_BROADCAST_HDR.from_address(lParam)
			if dbh.dbch_devicetype == DBT_DEVTYP_PORT:
				dbd = DEV_BROADCAST_DEVICEINTERFACE.from_address(lParam)
				dbcc_name = dbd.dbcc_name
				if wParam == DBT_DEVICEARRIVAL:
					#print "COM Arrival :",dbcc_name
					self.handlerArrival(dbcc_name)
				elif wParam == DBT_DEVICEREMOVECOMPLETE:
					#print "COM Removed :",dbcc_name
					self.handlerRemoved(dbcc_name)
		return True
		
	'''
	def registerDeviceNotification(self, guid, devicetype=DBT_DEVTYP_DEVICEINTERFACE):
		devIF = DEV_BROADCAST_DEVICEINTERFACE()
		devIF.dbcc_size = ctypes.sizeof(DEV_BROADCAST_DEVICEINTERFACE)
		devIF.dbcc_devicetype = DBT_DEVTYP_DEVICEINTERFACE
		
		if guid:
			devIF.dbcc_classguid = comtypes.GUID(guid)
			#devIF.dbcc_classguid = GUID.GUID(guid)
		return RegisterDeviceNotification(self.GetHandle(), ctypes.byref(devIF), 0)
	
	def unregisterDeviceNotification(self, handle):
		if UnregisterDeviceNotification(handle) == 0:
			raise Exception("Unable to unregister device notification messages")
	'''


# a simple example
if __name__ == "__main__":
	import _winreg
	class MyPanel(wx.Panel):
		def __init__(self,parent):
			wx.Panel.__init__(self,parent)
			COM_Label = wx.StaticText(self, -1, "COM:")
			
			list = self.__ReadComList()
			list.sort(self.sort_COM)
			self.ComListBox = wx.Choice(self,choices=list)
			self.ComListBox.SetStringSelection(list[0])
			
			Box = wx.BoxSizer(wx.HORIZONTAL)	# BoxSizer for Vertical ScrollBar + VSB on panel3
			Box.Add(COM_Label,0)
			Box.Add(self.ComListBox,0)
			self.SetSizer(Box)
			
			parent.hookMsgHandler(self.__onDeviceChange)
		
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
			key = _winreg.OpenKey( _winreg.HKEY_LOCAL_MACHINE, 'HARDWARE\DEVICEMAP\SERIALCOMM',0, _winreg.KEY_READ)
			keyNb = _winreg.QueryInfoKey(key)[1]
			port = []
			for i in range(keyNb):
				port.append(_winreg.EnumValue(key,i)[1])
			_winreg.EnumValue(key,9)
			return port
		
		def __onDeviceChange(self,wParam,lParam):
			#print "WM_DEVICECHANGE [WPARAM:%i][LPARAM:%i]"%(wParam,lParam)
			if lParam:
				dbh = DEV_BROADCAST_HDR.from_address(lParam)
				if dbh.dbch_devicetype == DBT_DEVTYP_PORT:
					dbd = DEV_BROADCAST_DEVICEINTERFACE.from_address(lParam)
					dbcc_name = dbd.dbcc_name
					if wParam == DBT_DEVICEARRIVAL:
						print "COM Arrival :",dbcc_name
						list = self.ComListBox.GetStrings()+[dbcc_name]
						list.sort(self.sort_COM)
						sav = self.ComListBox.GetStringSelection()
						self.ComListBox.Clear()
						for elem in list:
							self.ComListBox.Append(elem)
						self.ComListBox.SetStringSelection(sav)
					elif wParam == DBT_DEVICEREMOVECOMPLETE:
						print "COM Removed :",dbcc_name
						if dbcc_name == self.ComListBox.GetStringSelection():
							self.ComListBox.SetStringSelection(self.ComListBox.GetStrings()[0])
						self.ComListBox.Delete(self.ComListBox.FindString(dbcc_name))
			return True
	
	
	class MyFrame(wx.Frame,WndProcHookMixin):
		def __init__(self,parent):
			WndProcHookMixin.__init__(self)
			wx.Frame.__init__(self,parent,-1,"Insert and Remove USE Device and Watch STDOUT",size=(640,480))
			
			panel = MyPanel(self)
			
			#self.Bind(wx.EVT_CLOSE, self.onClose)
		'''
		def onClose(self, event):
			self.unregisterDeviceNotification(self.devNotifyHandle)
			event.Skip()
		'''
	
	
	app = wx.App(False)
	frame = MyFrame(None)
	frame.Show()
	app.MainLoop()
	
