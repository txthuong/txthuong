#!/usr/bin/env python
# _*_ coding: utf-8 _*_

#----------------------------------------------------------------------------
# Nom:		AddTestDlg.py
# Objet:	Fen�tre qui permet de choisir le fichier config ou test 
#
# Auteur:	Bingxun HOU
#
# Version:	AutoTest 1.0
# Date:		Avril - Septembre 2007
# Propri�t�	Sagemcom
#
#Auteur        jm seillon              
# Date         05/07/2012
#version       1.8.8                  Replacement of all text "Sagem Communication" against "Sagemcom"
#----------------------------------------------------------------------------

import sys, os
import wx
import mouse
import time

class Static_Variables(object):
	directory = os.getcwd()

staticVariables = Static_Variables()

#Class DlgAddTest
class AddTestDlg(wx.Dialog):
	def __init__(self, treelist, list_test, config=False):
		
		self.config = config
		self.notClosing = True
		
		if self.config:
			wx.Dialog.__init__(self, None, -1, "Add Config", size=(320, 360))
			filtre="*.cfg"
		else:
			wx.Dialog.__init__(self, None, -1, "Add Test", size=(320, 360))
			filtre="*.py"
		self.treelist = treelist
		self.list_test = list_test
		self.cfg = ""
		
		boxSizer = wx.BoxSizer(wx.VERTICAL)
		
		self.staticBox = wx.StaticBox(self, -1, "Directory:")
		staticBoxSizer = wx.StaticBoxSizer(self.staticBox, wx.VERTICAL)
		
		self.dir = wx.GenericDirCtrl(self, -1, size=(290,260), style=wx.DIRCTRL_SELECT_FIRST)
		self.dir.SetFilter(filtre)
		self.dir.ShowHidden(False)
		#self.dir.SetPath(os.getcwd()) # Se positionner dans le r�pertoire pr�sent
		self.dir.SetPath(staticVariables.directory) # Se positionner dans le r�pertoire pr�sent
		
		# permet de capturer le double clic
		treeCtrl1=self.dir.GetTreeCtrl()
		treeCtrl1.Bind(wx.EVT_LEFT_DCLICK, self.__LeftDoubleClick)
		treeCtrl1.Bind(wx.EVT_CHAR, self.__KeyPress)
		treeCtrl1.Bind(wx.EVT_TREE_SEL_CHANGED, self.__OnSelChanged)
		self.treeCtrl1=treeCtrl1
		staticBoxSizer.Add(self.dir, 0, wx.TOP|wx.CENTER, 2)
		
		line  = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
		
		btnsizer = wx.StdDialogButtonSizer()
		
		self.btn_OK = wx.Button(self, wx.ID_OK)
		self.btn_OK.SetDefault()
		btnsizer.AddButton(self.btn_OK)
		
		btn_CANCEL = wx.Button(self, wx.ID_CANCEL)
		btnsizer.AddButton(btn_CANCEL)
		btnsizer.Realize()
		
		boxSizer.Add(staticBoxSizer, 0, wx.CENTER)
		boxSizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)
		boxSizer.Add(btnsizer, 0, wx.CENTER|wx.ALL, 5)
		
		self.SetSizer(boxSizer)
		
		treeCtrl1.SetFocus()   
		
		val = self.ShowModal() # Au moment d'afficher la fenetre dialog, bloquer la fenetre principale
		
		
		if val == wx.ID_OK:
			self.__AddSelectItem()
		else:
			self.__OnCancel()
			
		self.notClosing = False
		# Detruire le dialog
		self.Destroy()
	
	def __KeyPress(self, evt):
		if evt.GetUnicodeKey() == 13:  # if CR is press
			self.__AddSelectItem()
		else:
			evt.Skip()
	
	def __LeftDoubleClick(self, event):
		self.__AddSelectItem(dblclic=True)
	
	def __AddSelectItem(self,dblclic=False):
		selected_dir = self.dir.GetPath()
		if selected_dir == "":
			self.__OnMessage()
		elif not(selected_dir.endswith(".py")) and not(selected_dir.endswith(".cfg")) and dblclic:	 # gere le deploiment de repertroire
			TreeCtrl = self.dir.GetTreeCtrl()
			Selection = TreeCtrl.GetSelection()
			if TreeCtrl.IsExpanded(Selection):
				TreeCtrl.Collapse(Selection)
			else:
				TreeCtrl.Expand(Selection)
		else:
			
			if self.config:
				self.cfg = str(selected_dir)
				if self.treelist[1][0][1][0] == "":
					self.treelist[1][0][1][0] =self.__CreateTestTree(str(selected_dir))
				else:
					self.treelist[1][0][1].append(self.__CreateTestTree(str(selected_dir))) # convertir de unicode a string 
				self.Destroy()
			else:
				self.list_test.append(str(selected_dir))
				if self.treelist[1][1][1][0] == "":
					self.treelist[1][1][1][0] = self.__CreateTestTree(str(selected_dir))
				else:
					self.treelist[1][1][1].append(self.__CreateTestTree(str(selected_dir))) # convertir de unicode a string
			
			staticVariables.directory = selected_dir.rsplit("\\",1)[0]
				
			# Detruire le dialog
			self.Destroy()

	def __OnSelChanged(self, event):
		if self.notClosing:
			selected_dir = self.dir.GetPath()
			if self.config:
				pass
				
				if os.path.isfile(selected_dir):
					self.btn_OK.Enable(True)
				else:
					self.btn_OK.Enable(False)
	
	def __OnMessage(self, msg = "Attention! You have chosen anything."):
		dlg = wx.MessageDialog(self,
							   msg,
							   "Message",
							   wx.OK|wx.ICON_INFORMATION
							   #wx.YES_NO | wx.NO_DEFAULT | wx.CANCEL | wx.ICON_INFORMATION
							   )
		dlg.ShowModal()
		dlg.Destroy()

	def __OnCancel(self):
		pass
		
	def GetTreeList(self):
		return self.treelist 

	def GetListTest(self):
		return self.list_test

	def GetCfg(self):
		return self.cfg


	# fonction qui permet de creer le treelist
	def __CreateTestTree(self, root):
		list_copy = []
		if os.path.isfile(root):
			#return [os.path.basename(root), list_copy]
			return os.path.basename(root)
		else:
			list = os.listdir(root) # ! bug: chemin relatif 
			for elem in list:
				elem_copy = os.path.join(root, elem)
				if os.path.isdir(elem_copy):
					list_copy.append(self.__CreateTestTree(elem_copy))
				elif os.path.isfile(elem_copy) and elem_copy[-3:] == '.py':
					list_copy.append(elem)
			
			return [os.path.basename(root), list_copy]