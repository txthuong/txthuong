'''
Graphic to display the satellites position
This program can be used to create a dynamic graphic to dislay the sat position.
It is an exemple.
Today this code is not used in autotest application
Created on 6 avr. 2012

@author: jm Seillon
'''
import wx
import math
import random



class GNSS_Graphic(wx.Window):
	def __init__(self, parent, title, labels):
		wx.Window.__init__(self, parent)
		self.title = title
		self.labels = labels
		self.data = [0,0] * len(labels)
		self.titleFont = wx.Font(14, wx.SWISS, wx.NORMAL, wx.BOLD)
		self.labelFont = wx.Font(10, wx.SWISS, wx.NORMAL, wx.NORMAL)
		self.buffer = wx.EmptyBitmap(0, 0)
		self.InitBuffer()
		
		self.Bind(wx.EVT_SIZE, self.OnSize)
		
		self.Bind(wx.EVT_PAINT, self.OnPaint)


	def OnSize(self, evt):
		self.InitBuffer()

	def OnPaint(self, evt):
		dc = wx.BufferedPaintDC(self, self.buffer)

	def InitBuffer(self):
		w, h = self.GetClientSize()
		self.buffer = wx.EmptyBitmap(w, h)
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.DrawGraph(dc)

	def GetData(self):
		return self.data

	def Setdata(self, newData):
		assert len(newData) == len(self.data)
		self.data = newData[:]
		dc = wx.BufferedDC(wx.ClientDC(self), self.buffer)
		self.DrawGraph(dc)

	def PolarToCartesian(self, radius, angle, cx, cy):
		x = radius * math.cos(math.radians(angle))
		y = radius * math.sin(math.radians(angle))
		return (cx+x, cy-y)

	def DrawGraph(self, dc):
		spacer = 10
		scaledmax = 150.0
		
		dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
		dc.Clear()
		dw, dh = dc.GetSize()
		dc.SetFont(self.titleFont)
		tw, th = dc.GetTextExtent(self.title)
		dc.DrawText(self.title, (dw-tw)/2, spacer)
		
		th = th + 2 * spacer
		cx = dw/2
		cy = (dh-th)/2 + th
		
		mindim = min(cx, (dh-th)/2)
		scale = mindim/scaledmax
		
		dc.SetPen(wx.Pen("black", 1))
		
		dc.SetBrush(wx.TRANSPARENT_BRUSH)
		dc.DrawCircle(cx, cy, 25*scale)
		dc.DrawCircle(cx, cy, 50*scale)
		dc.DrawCircle(cx, cy, 75*scale)
		dc.DrawCircle(cx, cy, 100*scale)
		
		dc.SetPen(wx.Pen("balck", 2))
		dc.DrawLine(cx-110*scale, cy, cx+110*scale, cy)
		dc.DrawLine(cx, cy-110*scale, cx, cy+110*scale)
		
		dc.SetFont(self.labelFont)
		maxval = 0
		angle = 0
		polypoints = []
		for i, label in enumerate(self.labels):
			val = self.data[i]
			point = self.PolarToCartesian(val*scale, angle+90, cx, cy)
			polypoints.append(point)
			x, y = self.PolarToCartesian(125*scale, angle, cx, cy)
			dc.DrawText(label, x, y)
			if val > maxval:
				maxval = val
			angle = angle + 360/len(self.labels)
			
		c = "forest green"
		if maxval > 70:
			c = "yellow"
		if maxval > 95:
			c = "red"
		dc.SetBrush(wx.Brush(c))
		dc.SetPen(wx.Pen(c, 3))
		for circ in polypoints:
			dc.DrawCircle(circ[0],circ[1],3)


class GNSSFrame(wx.Frame):
	def __init__(self):
		wx.Frame.__init__(self, None, title="Double buffered drawing.", size=(480, 480))
		self.plot = GNSS_Graphic(self, "Satellites 'Radar' plot", ["W", "NW", "N", "NE", "E", "SE", "S", "SW"])
		
		data = []
		for d in self.plot.GetData():
			data.append(random.randint(0, 75))
		self.plot.Setdata(data)
		
		self.Bind(wx.EVT_TIMER, self.OnTimeout)
		self.timer = wx.Timer(self)
		self.timer.Start(500)
		
	def OnTimeout(self, evt):
		data = []
		for d in self.plot.GetData():
			val = d + random.uniform(-5, 5)
			if val < 0:
				val = 0
			if val > 110:
				val = 110
			data.append(val)
		self.plot.Setdata(data)


if __name__ == '__main__':
	app = wx.PySimpleApp()
	frm = GNSSFrame()
	frm.Show()
	app.MainLoop()
