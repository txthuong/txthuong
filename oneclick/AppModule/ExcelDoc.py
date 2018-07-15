#!/usr/bin/env python
# _*_ coding: utf-8 _*_

#----------------------------------------------------------------------------
# Nom:		  ExcelDoc.py
# Objet:		generation de fichier Excel
#			   Il contient deux classes represente le fichier Excel et 
#			   les articles de fichier excel 
#
# Auteur:	   Bingxun HOU
#
# Version:	  AutoTest 1.0
# Date:		 Avril - Septembre 2007
# Propri�t?	Sagemcom
#
#05/07/2012        jm seillon            1.8.8            Replacement of all text "Sagem Communication" against "Sagemcom"
#----------------------------------------------------------------------------

import sys, os
import win32com.client

class ExcelItem():
	def __init__(self, Number):
		self.ItemNumber  = Number
		self.Vesion	  = "" 
		self.Reference   = ""
		self.Title	   = ""
		self.TestDesc	= ""
		self.Actor	   = ""
		self.Date		= ""
		self.TestType	= ""
		self.Avance	  = ""
		self.Stat		= ""
		self.SoftVersion = ""
		self.Comment	 = ""

	def SetVersion(self, Version):
		self.Version = Version 

	def SetReference(self, Reference):
		self.Reference = Reference 

	def SetTitle(self, Title):
		self.Title = Title 

	def SetDate(self, Date):
		self.Date = Date 

	def SetTestType(self, TestType):
		self.TestType = TestType 

	def SetAvance(self, Avance):
		self.Avance = Avance 

	def SetStat(self, Stat):
		self.Stat = Stat 

	def SetSoftVersion(self, SoftVersion):
		self.SoftVersion = SoftVersion 
		
	def SetComment(self, Comment):
		self.Comment = Comment 


class ExcelDoc():
	def __init__(self):
		self.counter = 0
		self.list = [] 

	def NewItem(self):
		self.counter = self.counter + 1
		self.list.append(ExcelItem(self.counter)) 

	# Prendre le index du present element dans la liste
	def GetIndex(self):
		return self.counter - 1
		
	def Display(self): #, result):
		# Creation de l'objet Excel
		excel = win32com.client.Dispatch("Excel.Application")
		excel.Visible = 1

		# Creation de classeur
		excel.Workbooks.Add()

		# Creation de titre
		#excel.ActiveSheet.Columns("A:A").ColumnWidth = 20	
		excel.ActiveSheet.Rows("1:1").RowHeight = 30  
		excel.ActiveSheet.Rows("2:2").RowHeight = 30  
		excel.ActiveSheet.Range("A1:L1").Interior.ColorIndex = 4 # vert 
		excel.ActiveSheet.Range("A1").Font.Bold = True		  # Font en gras 
		excel.ActiveSheet.Range("A1").Value = 'AT commands test handbook'
		excel.ActiveSheet.Range("F1").Font.Bold = True
		excel.ActiveSheet.Range("F1").Value = 'VERSION:'
		excel.ActiveSheet.Range("K1").Font.Bold = True
		excel.ActiveSheet.Range("K1").Value = 'IMEI'
		excel.ActiveSheet.Range("L1").Font.Bold = True
		excel.ActiveSheet.Range("L1").Value = 'SIM'

		# Ajustement du taille et alignement
		excel.ActiveSheet.Rows("3:3").RowHeight = 20  
		excel.ActiveSheet.Columns("A:A").ColumnWidth = 10	
		excel.ActiveSheet.Columns("B:B").ColumnWidth = 10	
		excel.ActiveSheet.Columns("C:C").ColumnWidth = 10	
		excel.ActiveSheet.Columns("D:D").ColumnWidth = 20	
		excel.ActiveSheet.Columns("E:E").ColumnWidth = 20	
		excel.ActiveSheet.Columns("F:F").ColumnWidth = 10	
		excel.ActiveSheet.Columns("G:G").ColumnWidth = 10	
		excel.ActiveSheet.Columns("H:H").ColumnWidth = 10	
		excel.ActiveSheet.Columns("I:I").ColumnWidth = 10	
		excel.ActiveSheet.Columns("J:J").ColumnWidth = 10	
		excel.ActiveSheet.Columns("K:K").ColumnWidth = 20	
		excel.ActiveSheet.Columns("L:L").ColumnWidth = 50	
		excel.ActiveSheet.Columns("A:A").HorizontalAlignment = 2
		excel.ActiveSheet.Columns("B:B").HorizontalAlignment = 2
		excel.ActiveSheet.Columns("C:C").HorizontalAlignment = 2
		excel.ActiveSheet.Columns("D:D").HorizontalAlignment = 2
		excel.ActiveSheet.Columns("E:E").HorizontalAlignment = 2
		excel.ActiveSheet.Columns("F:F").HorizontalAlignment = 2
		excel.ActiveSheet.Columns("G:G").HorizontalAlignment = 2
		excel.ActiveSheet.Columns("I:I").HorizontalAlignment = 2
		excel.ActiveSheet.Columns("J:J").HorizontalAlignment = 2
		excel.ActiveSheet.Columns("K:K").HorizontalAlignment = 2
		excel.ActiveSheet.Columns("L:L").HorizontalAlignment = 2

		# Creation de tete du tableau
		excel.ActiveSheet.Range("A3:L3").Borders.LineStyle = 1 # File simple
		excel.ActiveSheet.Range("A3:L3").Font.Bold = True
		excel.ActiveSheet.Range("A3:L3").Interior.ColorIndex = 6  # jaune 
		excel.ActiveSheet.Cells(3, 1).Value = 'Item'
		excel.ActiveSheet.Cells(3, 2).Value = 'Version'
		excel.ActiveSheet.Cells(3, 3).Value = 'Reference'
		excel.ActiveSheet.Cells(3, 4).Value = 'Title'
		excel.ActiveSheet.Cells(3, 5).Value = 'Test Description '
		excel.ActiveSheet.Cells(3, 6).Value = 'Actor'
		excel.ActiveSheet.Cells(3, 7).Value = 'Date'
		excel.ActiveSheet.Cells(3, 8).Value = 'Test Type'
		excel.ActiveSheet.Cells(3, 9).Value = 'Avance'
		excel.ActiveSheet.Cells(3,10).Value = 'Stat'
		excel.ActiveSheet.Cells(3,11).Value = 'Soft Version'
		excel.ActiveSheet.Cells(3,12).Value = 'Comment'

		cpt = 4
		for elem in self.list:
			excel.ActiveSheet.Cells(cpt, 1).Value = elem.ItemNumber 
			excel.ActiveSheet.Cells(cpt, 2).Value = elem.Version
			excel.ActiveSheet.Cells(cpt, 3).Value = elem.Reference
			excel.ActiveSheet.Cells(cpt, 4).Value = elem.Title
			excel.ActiveSheet.Cells(cpt, 5).Value = elem.TestDesc
			excel.ActiveSheet.Cells(cpt, 6).Value = elem.Actor
			excel.ActiveSheet.Cells(cpt, 7).Value = elem.Date
			excel.ActiveSheet.Cells(cpt, 8).Value = elem.TestType
			excel.ActiveSheet.Cells(cpt, 9).Value = elem.Avance
			excel.ActiveSheet.Cells(cpt,10).Value = elem.Stat
			if elem.Stat == 'OK':
				excel.ActiveSheet.Cells(cpt,10).Interior.ColorIndex = 4
			elif elem.Stat == 'NOK':
				excel.ActiveSheet.Cells(cpt,10).Interior.ColorIndex = 3 
			else:
				excel.ActiveSheet.Cells(cpt,10).Interior.ColorIndex = 0 


			excel.ActiveSheet.Cells(cpt,11).Value = elem.SoftVersion
			excel.ActiveSheet.Cells(cpt,12).Value = elem.Comment			
			cpt = cpt + 1

