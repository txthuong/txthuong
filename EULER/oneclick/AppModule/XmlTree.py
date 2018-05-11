#!/usr/bin/env python
# _*_ coding: utf-8 _*_

#----------------------------------------------------------------------------
# Nom:		  XmlTree.py
# Objet:		D�finition de la classe pour g�n�rer les fichiers XML  
#
# Auteur:	   Bingxun HOU
#
# Version:	  AutoTest 1.0
# Date:		 Avril - Septembre 2007
# Propri�t�	 Sagemcom
#
#05/07/2012         jm seillon            1.8.8            Replacement of all text "Sagem Communication" against "Sagemcom"
#----------------------------------------------------------------------------

import sys, os

class XmlNode():
	def __init__(self, name, level=-1, father=None):
		self.name = name
		self.level = level
		self.father = father
		self.son_list = []
		self.content = ''

	def AddSon(self, node):
		node.level = self.level + 1
		self.son_list.append(node)
		node.father = self

class XmlTree():
	def __init__(self):
		self.root = XmlNode('?xml version="1.0"?', 0)
		self.pointer = self.root
		self.height = 0

	def AddNode(self, name):
		node = XmlNode(name) 
		self.pointer.AddSon(node)
		self.pointer = node
		if self.pointer.level > self.height:
			self.height = self.pointer.level

	def SetContent(self, content):
		self.pointer.content = content

	def GoToFather(self):
		self.pointer = self.pointer.father

	def WriteNode(self, node):
		for son in node.son_list:
			if son.content == '':
				self.xml_file.write( '	'*(son.level-1) )
				self.xml_file.write('<%s>\n'%son.name)
		   
				self.WriteNode(son)
				
				self.xml_file.write( '	'*(son.level-1) )
				self.xml_file.write('</%s>\n'%son.name)
			else:
				self.xml_file.write( '	'*(son.level-1) )
				self.xml_file.write('<%s>'%son.name)
				self.xml_file.write('%s'%son.content)
				self.xml_file.write('</%s>\n'%son.name)


	def WriteTree(self, filename):
		self.xml_file = open(filename, 'w')
		self.xml_file.write('<%s>\n'%self.root.name)
		self.WriteNode(self.root)
		self.xml_file.close()

xmlTree = None
