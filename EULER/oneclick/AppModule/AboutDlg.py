#!/usr/bin/env python
# _*_ coding: utf-8 _*_

#----------------------------------------------------------------------------
# Nom:		  AboutDlg.py
# Objet:		Fen�tre de la courte information sur le logiciel 
#
# Auteur:	   Bingxun HOU
#
# Version:	  AutoTest 1.0
# Date:		 Avril - Septembre 2007
# Propriete	 Sagemcom
#
#Auteur        jm seillon              
# Date         05/07/2012
#version       1.8.9                  Replacement of all text "Sagem Communication" against "Sagemcom"
#----------------------------------------------------------------------------

#import sys, os
import wx


# Definition de la class AboutDlg
class AboutDlg(wx.Dialog):
	def __init__(self, parent):
		wx.Dialog.__init__(self, parent, -1, "About AutoTestAT")
		info = wx.AboutDialogInfo()
		info.Name = "AutoTest"
		info.Version = "1.9.6.28"
		info.Copyright = "(C) 2007 Sagemcom URD1"
		info.SetDescription("Software \"AutoTestPlus\" is a tool of the automation of\n"	  
							"the test for GSM/GSM-R/GPRS/WCDMA/HSxPA/LTE modules. It can run	 \n"	 
							"the scenario of test writen in python using the	 \n"	
							"fonctions API of this software.					 \n" )   
		info.WebSite = ("http://http://cnhkg-ed-hkva17/wiki/wp-admin/", "Home Page")
		#info.Developers = ["  Bingxun HOU	houbingxun@yahoo.fr"]
		wx.AboutBox(info)
