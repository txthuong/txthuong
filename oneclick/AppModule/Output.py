#!/usr/bin/env python
# _*_ coding: utf-8 _*_

#----------------------------------------------------------------------------
# Nom:		  Output.py
# Objet:		Le module de redirection de sortie 
#			   Le logiciel utilise redirection pour sauvegarder les traces 
#			   de l'information sur les diff�rents sorties, ils sont bas� 
#			   sur la classe Output, plusieur classes d�riv�s de Output  
#			   pour orienter les messages vers les diff�rents m�dia.
#
# Auteur:	   Bingxun HOU
#
# Version:	  AutoTest 1.0
# Date:		 Avril - Septembre 2007
# Propri�t�	 Sagemcom
#
#05/07/2012         jm seillon            1.8.8            Replacement of all text "Sagem Communication" against "Sagemcom"
#----------------------------------------------------------------------------

import sys,os
import wx
import time
#import ComModuleAPI
import VarGlobal

import threading
"""
Cette classe fournit une sortie qui permet de remplacer le sortie standard.
Cette sortie peut contenir deux directions:
	- gui: TextCtrl de fenetre principale
	- log_file: fichier log doit etre genere en cas ou log_flag vaut 1
"""
class Static_Variables():
	def __init__(self):
		pass
	flag  = False
	flag2 = False
	pos = 0
	display = 1
	# Le verrou print_mutex et print s�curis�
	print_mutex = threading.Lock()

staticVariables = Static_Variables()


def SagActivatePrintOnGUI(status):
	staticVariables.display = status
	
# La class de base abstrait "Output"
class Output:
	def __init__(self):
		pass

	def write(self):
		pass

# La classe derive de la class Output, reimplante fonction write()
class MyStdout(Output):
	"""Cette classe permet d'afficher le message sur la sortie standard
	et le fichier log en meme temps."""
	
	def __init__(self):
		# Sauvgarder sys.stdout vers self.save_stdout
		self.save_stdout = sys.stdout 

	def write(self, text):
        # kmwong remove
		#self.save_stdout.write(wx.TextAttr(VarGlobal.myColor, "white"))
		self.save_stdout.write(text)
        # kmwong remove
		#self.save_stdout.write(wx.TextAttr("black"))		
		#self.save_stdout.write(text) # en effet, le vrai stdout soit l'ecran		
		time.sleep(0.001)


# La classe derive de la class Output, reimplante fonction write()
class LogOutputWithPath(Output):
	"""Cette classe permet d'afficher le message sur la sortie standard
	et le fichier log en meme temps."""

	def __init__(self, log_fullpath):
		# Sauvgarder sys.stdout vers self.save_stdout
		self.save_stdout = sys.stdout 
		self.log_fullpath = log_fullpath

	def write(self, text):
		self.save_stdout.write(text) # en effet, le vrai stdout soit l'ecran
		
		file = open(self.log_fullpath, 'a')
		file.write(text)
		file.close()

# kmwong
class LogDisplayFileOutput(Output):
	"""Cette classe permet d'afficher le message sur la sortie standard
	et le fichier log en meme temps."""
	
	def __init__(self, log_file, log_file_timestamp):
		# Sauvgarder sys.stdout vers self.save_stdout
		self.save_stdout = sys.stdout 
		self.log_file = log_file
		self.log_file_timestamp = log_file_timestamp
	def write(self, text):
		# Display
		self.save_stdout.write(text)

		# Log
		file = open(self.log_file, 'a')
		file.write(text)
		file.close()

		# Log with timestamp
		file = open(self.log_file_timestamp, 'a')
		file.write(text)
		file.close()



# kmwong
class GuiLogOutput(Output):
	"""Cette classe permet d'afficher le message sur la sortie standard
	et le fichier log en meme temps."""
	
	def __init__(self, gui_out, log_file, log_file_timestamp): 
		self.gui_out  = gui_out
		# kmwong
		#self.log_file = log_file
		self.log_file = log_file
		self.log_file_timestamp = log_file_timestamp

	def write(self, text):
		# GUI
		self.gui_out.SetDefaultStyle(wx.TextAttr(VarGlobal.myColor))
		self.gui_out.AppendText(text)
		self.gui_out.SetDefaultStyle(wx.TextAttr("black"))

		# Log
		file = open(self.log_file, 'a')
		file.write(text)
		file.close()

		# Log with timestamp
		file = open(self.log_file_timestamp, 'a')
		file.write(text)
		file.close()


class ClearLogFileOutput(Output):
	"""Cette classe permet d'afficher le message sur la sortie standard
	et le fichier log en meme temps."""
	
	def __init__(self, log_file):
		# Sauvgarder sys.stdout vers self.save_stdout
		self.save_stdout = sys.stdout 
		self.log_file = log_file

		file = open(self.log_file, 'w')
		file.write("")
		file.close()

	def write(self, text):
		self.save_stdout.write(text) # en effet, le vrai stdout soit l'ecran
		file = open(self.log_file, 'w')
		file.write("clear")
		file.close()


# La classe derive de la class Output, reimplante fonction write()
class LogOutput(Output):
	"""Cette classe permet d'afficher le message sur la sortie standard
	et le fichier log en meme temps."""
	
	def __init__(self, log_file):
		# Sauvgarder sys.stdout vers self.save_stdout
		if not(os.path.isdir("Logs")):
			os.mkdir("Logs")
		self.save_stdout = sys.stdout 
		self.log_file = "Logs\\"+log_file

	def write(self, text):
		#self.save_stdout.write(text) # en effet, le vrai stdout soit l'ecran
		file = open(self.log_file, 'a')
		file.write(text)
		file.close()

'''
# La classe derive de la class Output, reimplante fonction write()
# ici on peut changer la couleur de print
class GuiOutput(Output):
	"""Cette classe permet d'afficher le message sur la fenetre du logiciel"""
	
	def __init__(self, gui_out): 
		self.gui_out = gui_out

	def write(self, text):
		self.gui_out.SetDefaultStyle(wx.TextAttr(VarGlobal.myColor))
		self.gui_out.AppendText(text)
		self.gui_out.SetDefaultStyle(wx.TextAttr("black"))
'''
# La classe derive de la class Output, reimplante fonction write()
# ici on peut changer la couleur de print
class GuiOutput(Output):
	"""Cette classe permet d'afficher le message sur la fenetre du logiciel"""
	
	def __init__(self, gui_out): 
		self.gui_out = gui_out

	def write(self, text):
		# securite pour ne pas ecrit deux fois en meme temps (lors de deux thread simultann�)
		staticVariables.print_mutex.acquire()  # prise de verrou
        
		if staticVariables.display == 0:
			pass
		
		elif staticVariables.display == 1:
			self.gui_out.SetDefaultStyle(wx.TextAttr(VarGlobal.myColor))
			self.gui_out.AppendText(text)
		
		elif staticVariables.display == 2:
		
			self.gui_out.SetDefaultStyle(wx.TextAttr(VarGlobal.myColor))
			flag = False
			remove=0
			text=text.splitlines(1)
			for elem in text:
				if elem.find("\b") != -1:
					for i in range(elem.count("\b")):
						if elem.startswith("\b"):
							elem = elem[1:]
							remove +=1
						else:
							pos = elem.find("\b")
							if pos >0:
								if pos < len(elem) and elem[pos+1] != "\b":
									if remove == 0:
										elem = elem[0:pos-1]+elem[pos+1:len(elem)]
									else:
										if (pos-remove-1) < 0:
											elem = elem[pos+1:len(elem)]+elem[pos-(remove-len(elem[pos+1:len(elem)])+1):pos]
										else:
											elem = elem[0:pos-remove-1]+elem[pos+1:len(elem)]+elem[pos-(remove-len(elem[pos+1:len(elem)])+1):pos]
										remove = 0
								else:
									remove += 1
									elem = elem[:pos] + elem[pos+1:]
				if staticVariables.flag:
					if staticVariables.flag2:
						self.gui_out.Replace(staticVariables.pos,staticVariables.pos+len(elem.replace("\r","").replace("\n","")),elem.replace("\r","").replace("\n",""))
						staticVariables.pos = self.gui_out.GetInsertionPoint()
						self.gui_out.SetInsertionPointEnd()
						if elem.endswith("\r\n") or elem.endswith("\n"):
							self.gui_out.AppendText("\n")
							staticVariables.flag  = False
							staticVariables.flag2  = False
						if elem.endswith("\r"):
							staticVariables.flag  = False
							staticVariables.flag2  = False
					else:
						pos = self.gui_out.GetInsertionPoint()
						x,y = self.gui_out.PositionToXY(pos)
						pos2= self.gui_out.XYToPosition(0, y)
						self.gui_out.Replace(pos2,pos2+len(elem.replace("\r","").replace("\n","")),elem.replace("\r","").replace("\n",""))
						staticVariables.pos = self.gui_out.GetInsertionPoint()
						self.gui_out.SetInsertionPointEnd()
						if elem.endswith("\r\n") or elem.endswith("\n"):
							self.gui_out.AppendText("\n")
							staticVariables.flag  = False
						staticVariables.flag2 = True
				else:
					self.gui_out.AppendText(elem.replace("\r",""))
				
				if elem.endswith("\r"):
					staticVariables.flag = True
			
			self.gui_out.SetDefaultStyle(wx.TextAttr("black"))		  
		
		staticVariables.print_mutex.release()  # relanche de verrou
    
	def replaceCurentLine(self, text):
		pos = self.gui_out.GetInsertionPoint()
		x,y = self.gui_out.PositionToXY(pos)
		pos2= self.gui_out.XYToPosition(0, y)
		self.gui_out.Remove(pos,pos2)
		self.write(text)



# La classe derive de la class Output, reimplante fonction write()
class GuiOnlyOutput(Output):
	"""Cette classe permet d'afficher le message sur la sortie standard
	et le fichier log en meme temps."""
	
	def __init__(self, gui_out): 
		self.gui_out  = gui_out

	def write(self, text):
		self.gui_out.SetDefaultStyle(wx.TextAttr(VarGlobal.myColor))
		self.gui_out.AppendText(text)
		self.gui_out.SetDefaultStyle(wx.TextAttr("black"))


# La classe derive de la class Output, reimplante fonction write()
class Output_odd:
	def __init__(self, gui, log_file='logfile.log', log_flag=False): 
		self.gui_out  = gui
		self.log_file = log_file
		self.log_flag = log_flag

	def write(self, text):
		#self.gui_out.AppendText(text)
		self.gui_out.SetDefaultStyle(wx.TextAttr(VarGlobal.myColor))
		self.gui_out.AppendText(text)
		self.gui_out.SetDefaultStyle(wx.TextAttr("black"))						
		if self.log_flag:
			if not(os.path.isdir("Logs")):
				os.mkdir("Logs")
			file = open(self.log_file, 'a')
			file.write(text)
			file.close()


if __name__ == '__main__':
	save_stdout = sys.stdout
	sys.stdout = LogOutput("logfile.log")
	print "bonjour et bonsoir"
	sys.stdout = save_stdout
