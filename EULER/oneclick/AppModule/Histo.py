#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Auteur   JM Seillon
#Date      27/04/2012
#
#
#26-07-2012        JM Seillon          1.9.0                 add ClearListData()
#11-03-2013		   Eric BARRE		   1.9.3				  HiloStarter: fix the GNSS feature to support the display of the ID/SNR before fix

#
import wx
from wx.lib import newevent
import  time
import  thread


(UpdateBarEvent, EVT_UPDATE_BARGRAPH) = newevent.NewEvent()

listGNSS = []

# Création d'un nouveau cadre, dérivé du wxPython 'Frame'.

class Histo(wx.Frame):
	def __init__(self, parent, log):
		''' constructor '''
		wx.Frame.__init__(self, parent, -1, "Hilo Starter Graph",style=wx.CAPTION | wx.MINIMIZE_BOX | wx.RESIZE_BORDER)
		self.log = log

		panel = wx.Panel(self, -1)
		panel.SetFont(wx.Font(10, wx.SWISS, wx.NORMAL, wx.BOLD))

		panel.Fit()
		self.listDatas = []

		self.graph = GraphWindow(self,self.listDatas)
		self.sizeGraph = ((self.graph.GetCharWidth()+10)*24, 150)
		self.graph.SetSize(((self.graph.GetCharWidth()+10)*50, 150))

		sizer = wx.BoxSizer(wx.HORIZONTAL)
		sizer.Add(self.graph, 1, wx.EXPAND)

		self.SetSizer(sizer)
		self.SetAutoLayout(True)
		sizer.Fit(self)

		self.Bind(EVT_UPDATE_BARGRAPH, self.OnUpdate)

		self.threads = []
		self.threads.append(CalcBarThread(self, 0,self.listDatas))

		for t in self.threads:
			t.Start()

		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

	def OnUpdate(self, evt):
		''' Update of the graphic window'''			
		self.graph.Refresh(False)


	def OnCloseWindow(self, evt):
		''' Close the window '''
		busy = wx.BusyInfo("One moment please, waiting for threads to die...")
		wx.Yield()

		for t in self.threads:
			t.Stop()

		running = 1
		while running:
			running = 0
			for t in self.threads:
				running = running + t.IsRunning()
			time.sleep(0.01)
			
		self.Destroy()

	def SetListData(self,name,listData):
		''' Data acquisition '''
		global listGNSS
		listGNSS = listData
		self.listDatas = listData

	def ClearListData(self):
		global listGNSS
		listGNSS=[]

class GraphWindow(wx.Window):
	''' Graphic window'''
	def __init__(self, parent,listDatas):
		''' Constructor'''
		wx.Window.__init__(self, parent, -1)
		global listGNSS
		self.linePos = 0
		self.barHeight = 0
		self.barWidth = 0
		self.values = listGNSS
#		print"listDatas histo: ",listDatas
#		print"Values histo: ", self.values

		''' init des fonts'''
		font = wx.Font(8, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.SetFont(font)

		self.Bind(wx.EVT_ERASE_BACKGROUND, self.OnEraseBackground)
		self.Bind(wx.EVT_PAINT, self.OnPaint)

	def SetValue(self, index, value):
		''' data for one bar'''
		if len(value) != 0:
			if index < len(value):
				couleur = value[0]
				numSat = value[1]
				snr = value[2]
				cur = snr
		else:
			couleur = wx.Colour(255,255,255)
			numSat = 0
			snr = 0
			cur = snr

	def SetFont(self, font):
		''' Config font'''
		wx.Window.SetFont(self, font)
		wmax = hmax = 0
		w,h = self.GetTextExtent("AA")
		if w > wmax: wmax = w
		if h > hmax: hmax = h
		self.linePos = wmax + 10
		self.barHeight = hmax
		self.barWidth = wmax

	def GetBestWidth(self):
		return 3 * (self.barWidth + 1) * len(listGNSS)

	def GetBestHeight(self):
		return 2 * (self.barHeight + 1) * len(listGNSS)

	def Draw(self, dc, size):
		''' Draw the graphic'''
		XoffSet = 25
		dc.SetFont(self.GetFont())
		dc.SetTextForeground(wx.BLACK)
		dc.SetBackground(wx.Brush("WHITE"))
#		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()
		dc.SetPen(wx.Pen(wx.BLACK, 2, wx.SOLID))
		dc.DrawLine(XoffSet,130, size.width*24-10,130)#tracer de l'axe des x
		dc.DrawLine(XoffSet,130, XoffSet,0) #tracer de l'axe des y
		dc.SetPen(wx.Pen(wx.NamedColour(wx.LIGHT_GREY), 1, wx.DOT))
		dc.DrawLine(XoffSet,130-75, 1200,130-75)
		dc.SetPen(wx.Pen(wx.BLACK, 1, wx.SOLID))
		for i in range(7):
			if i > 0:
				dc.DrawText(str(10*i), 3,130-15*(i+0.5) )
				dc.DrawLine(XoffSet-4,130-15*i, XoffSet+4,130-15*i)
				dc.SetPen(wx.Pen(wx.NamedColour(wx.LIGHT_GREY), 1, wx.DOT))
				dc.DrawLine(XoffSet,130-15*i, 1200,130-15*i)
			dc.SetPen(wx.Pen(wx.BLACK, 1, wx.SOLID))


		dc.DrawText("SNR:", 3,5 )
		dc.DrawText("ID:", 3,135 )
		bx = xpos = self.barWidth
#		print len(self.values)
		for x in listGNSS: # draw all bars

			numSat=x[0][1]
			if numSat>0:
				couleur=x[0][0]
				val = x[0][2]
				dc.DrawText(str(numSat), XoffSet+xpos,132 )
				dc.SetPen(wx.Pen(couleur))
				dc.SetBrush(wx.Brush(couleur))
				try:
					dc.DrawRectangle(XoffSet+xpos,130, bx,-int(val)*1.5)
					dc.DrawText(str(val),XoffSet+xpos,5)
				except ValueError:
					pass
					
				xpos = xpos + 2*bx
				if xpos > size[0]-10:
					break

	def OnPaint(self, evt):
		dc = wx.BufferedPaintDC(self)
		self.Draw(dc, self.GetSize())

	def OnEraseBackground(self, evt):
		pass


class CalcBarThread():
	def __init__(self, win, barNum, listdata):
		self.running = False
		self.win = win
		self.val = 0
		self.numSat = 0
		self.barNum = barNum
		global listGNSS
		self.data = listGNSS
		if len(self.data) != 0:
			try:
				self.numSat = self.data[barNum][1]
	#			print"self.data[",barNum,"]: ", self.data[barNum]
				self.val = self.data[barNum][2]
#				print"Snr: ",self.val
			except IndexError:
				pass

		self.keepGoing = False

	def Start(self):
		self.keepGoing = self.running = True
		thread.start_new_thread(self.Run, ())

	def Stop(self):
		self.keepGoing = False

	def IsRunning(self):
		return self.running

	def Run(self):
		global listGNSS
		self.data = listGNSS
		barNume = 0
		self.val = None

		while self.keepGoing:
			if len(listGNSS)> 0 and barNume < len(listGNSS):
				self.val = listGNSS[barNume]
			else:
				self.val = ((0,0,0,0),0,0)
			#crée un évènement pour le calcul d'une barre
			evt = UpdateBarEvent(barNum = barNume, value = self.val)
			wx.PostEvent(self.win, evt)

			if barNume < len(listGNSS):
				barNume += 1
			else:
				barNume = 0
			time.sleep(0.25)

			if self.val < 0: self.val = 0
			if self.val > 100: self.val = 100

		self.running = False


# Chaque application wxWidgets doit avoir une classe dérivée de wx.App
class TestApp(wx.App):
	def OnInit(self):
		frame = Histo(None, -1)
		self.SetTopWindow(frame)
		frame.Show(True)
		return True
 
 
if __name__ == '__main__':
	app = TestApp(0) # créer une nouvelle instance de l'application
	app.MainLoop()   # lancer l'application