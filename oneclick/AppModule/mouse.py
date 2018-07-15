#!/usr/bin/env python
# _*_ coding: utf-8 _*_

# START SENDINPUT TYPE DECLARATIONS
from ctypes import *

PUL = POINTER(c_ulong)
class KeyBdInput(Structure):
	_fields_ = [("wVk", c_ushort),
			 ("wScan", c_ushort),
			 ("dwFlags", c_ulong),
			 ("time", c_ulong),
			 ("dwExtraInfo", PUL)]

class HardwareInput(Structure):
	_fields_ = [("uMsg", c_ulong),
			 ("wParamL", c_short),
			 ("wParamH", c_ushort)]

class MouseInput(Structure):
	_fields_ = [("dx", c_long),
			 ("dy", c_long),
			 ("mouseData", c_ulong),
			 ("dwFlags", c_ulong),
			 ("time",c_ulong),
			 ("dwExtraInfo", PUL)]

class Input_I(Union):
	_fields_ = [("ki", KeyBdInput),
			  ("mi", MouseInput),
			  ("hi", HardwareInput)]

class Input(Structure):
	_fields_ = [("type", c_ulong),
			 ("ii", Input_I)]

class POINT(Structure):
	_fields_ = [("x", c_ulong),
			 ("y", c_ulong)]
# END SENDINPUT TYPE DECLARATIONS

user32 = windll.user32

def LeftClick():
	FInputs = Input * 2
	extra = c_ulong(0)

	click = Input_I()
	click.mi = MouseInput(0, 0, 0, 2, 0, pointer(extra))
	release = Input_I()
	release.mi = MouseInput(0, 0, 0, 4, 0, pointer(extra))

	x = FInputs( (0, click), (0, release) )
	user32.SendInput(2, pointer(x), sizeof(x[0]))

def DoubleClick():
	FInputs = Input * 2
	extra = c_ulong(0)

	click = Input_I()
	click.mi = MouseInput(0, 0, 0, 2, 0, pointer(extra))
	release = Input_I()
	release.mi = MouseInput(0, 0, 0, 4, 0, pointer(extra))

	x = FInputs( (0, click), (0, release) )
	user32.SendInput(2, pointer(x), sizeof(x[0]))
	user32.SendInput(2, pointer(x), sizeof(x[0]))
	
def RightClick():
	FInputs = Input * 2
	extra = c_ulong(0)

	click = Input_I()
	click.mi = MouseInput(0, 0, 0, 8, 0, pointer(extra))
	release = Input_I()
	release.mi = MouseInput(0, 0, 0, 16, 0, pointer(extra))

	x = FInputs( (0, click), (0, release) )
	user32.SendInput(2, pointer(x), sizeof(x[0]))
