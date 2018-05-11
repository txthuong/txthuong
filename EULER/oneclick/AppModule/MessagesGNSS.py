# -*- coding: iso-8859-15 -*-
'''
Classes of messages.
The message transmitted through parameter, is split into items, which returned.

Created on 24 fevr. 2012

@author: JM SEILLON
@copyright: 2012
@organization: Sagemcom
@version: 1.0.0
'''
#date              who                 version                 modification
#28-02-2012        JM Seillon          1.8.2                   creation for GNSS feature
#23-03-2012        JM Seillon          1.8.3                   changes for GNSS feature


class GPGGA_Class(object):
	'''
	Class for GPGGA message
	Global Positioning System Fixed Data: Message ID GGA
	'''
	#private member of class
	'''@cvar __MessLongitude: Longitude
	@cvar __MessLatitude : Latitude
	@cvar __message : message transmitted
	@cvar __MessID : message id
	@cvar __MessUTCTIME : UTC time
	@cvar __MessNSIndic : North South indicator
	@cvar __MessEWIndic : East West indicator
	@cvar __MessPosFIXIndic : position FIX indicator
	@cvar __MessSatellitesUsed : satellites used
	@cvar __MessHDOP : Horizontal Dilution of Precision
	@cvar __MessMSLAltitude : altitude
	@cvar __MessUnitsMSL : units in meters
	@cvar __MessGeoidSeparation : Geoid-to-ellipsoid separation.
	@cvar __MessUnitsGeoidSeparation : units in meters
	@cvar __MessAgeOfDiffCorr : Age of Diff. Corr.
	'''
	__MessLongitude = ""
	__MessLatitude = ""
	__message = ""
	__MessID = ""
	__MessUTCTIME = ""
	__MessNSIndic = ""
	__MessEWIndic = ""
	__MessPosFIXIndic = ""
	__MessSatellitesUsed = ""
	__MessHDOP = ""
	__MessMSLAltitude = ""
	__MessUnitsMSL = ""
	__MessGeoIdSeparation = ""
	__MessUnitsGeoIdSeparation = ""
	__MessAgeOfDiffCorr = ""
	
	def __init__(self, message):
		'''
		Constructor
		'''
		self.__message = message
		self.get_ID()

	def get_Longitude(self):
		''' Return Longitude dddmm.mmmm'''
		# The message is a string, for the numeric fields you have to convert 
		# the type string of the substring to the right type, int or float
		tmp = ""
		try:
			if len(self.__message.split(',')[4]) > 0:	
				longit_deg = float(self.__message.split(',')[4][0:3:1])
				longit_min = float(self.__message.split(',')[4][3:5:1] + '.' + self.__message.split(',')[4][6::1])
				# compute the coordinates
				tmp = str(longit_deg + longit_min/60) 
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp

	def get_Latitude(self):
		''' Return Latitutde ddmm.mmmm'''
		# The message is a string, for the numeric fields you have to convert 
		# the type string of the substring to the right type, int or float
		tmp = ""
		try:
			if len(self.__message.split(',')[2]) > 0:
				latit_deg = float(self.__message.split(',')[2][0:2:1])
				latit_min = float(self.__message.split(',')[2][2:4:1] + '.' + self.__message.split(',')[2][5::1])
				tmp = str(latit_deg + latit_min/60)
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp

	def get_ID(self):
		''' Return MessId '''
		# GPGGA protocol header
		tmp = ""
		try:
			self.__MessID = str(self.__message.split(',')[0])
			if self.__MessID == "$GPGGA":
				tmp = self.__MessID
			else:
				tmp = "Message error, wrong ID Message."
		except IndexError:
			tmp = " "
		return tmp

	def get_UTCTIME(self):
		''' Return MessUTCTIME hhmmss.sss'''
		# type string hhmmss.sss
		tmp = ""
		try:
			if len(self.__message.split(',')[1]) > 0:
				UtcTime = str(self.__message.split(',')[1])
				tmp = UtcTime[0:2:1] + ' : ' + UtcTime[2:4:1] + ' : ' + UtcTime[4::1]
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp

	def get_NSIndic(self):
		''' return MessNSIndic, N=north or S=south '''

		tmp = ""
		try:
			if len(self.__message.split(',')[3]) > 0:
				tmp = str(self.__message.split(',')[3])
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp

	def get_EWIndic(self):
		''' return EWIndic, E=east or W=west '''
		tmp = ""
		try:
			if len(self.__message.split(',')[5]) > 0:
				tmp = str(self.__message.split(',')[5])
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp

	def get_PosFIXIndic(self):
		''' return Pos FIX Indic '''
		# 0 = Fix not available or invalid
		# 1 = GPS SPS Mode, fix valid
		# 2 = Differential GPS,  SPS Mode, fix valid
		# 3-5 = Not supported
		# 6 = Dead Reckoning Mode, fix valid
		tmp = ""
		try:
			if len(self.__message.split(',')[6]) > 0:
				tmp = str(self.__message.split(',')[6])
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp

	def get_SatellitesUsed(self):
		''' return Satellites Used'''
		# Range 0 to 12
		tmp = ""
		try:
			if len(self.__message.split(',')[7]) > 0:
				tmp = str(self.__message.split(',')[7])
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp

	def get_HDOP(self):
		''' retrun HDOP'''
		# Horizontal Dilution of Precision
		tmp = ""
		try:
			if len(self.__message.split(',')[8]) > 0:
				tmp = str(self.__message.split(',')[8])
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp

	def get_MSLAltitude(self):
		''' return MSL Altitude'''
		# type float meters
		tmp = ""
		try:
			if len(self.__message.split(',')[9]) > 0:
				tmp = str(self.__message.split(',')[9])
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp

	def get_UnitsMSL(self):
		''' retrun Units MSL'''
		# M (meters) type string
		tmp = ""
		try:
			if len(self.__message.split(',')[10]) > 0:
				tmp = str(self.__message.split(',')[10])
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp

	def get_GeoIdSeparation(self):
		''' return Geo Id Separation '''
		# Geoid-to-ellipsoid separation.
		# Ellipsoid altitude=MSL Altitude + Geoid Separation
		# type float, meters
		tmp = ""
		try:
			if len(self.__message.split(',')[11]) > 0:
				tmp = str(self.__message.split(',')[11])
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp

	def get_UnitsGeoIdSeparation(self):
		''' return Units Geo Id Separation'''
		# M (meters), type string
		tmp=""
		try:
			if len(self.__message.split(',')[12]) > 0:
				tmp =  str(self.__message.split(',')[12])
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp

	def get_AgeOfDiffCorr(self):
		''' return Age of Diff Corr'''
		# Null fields when DGPS is not used
		# seconds
		tmp = ""
		if len(self.__message.split(',')[13]) > 0:
			tmp = str(self.__message.split(',')[13])
		else:
			tmp = " "
		return tmp

	def get_DiffRefStationID(self):
		''' return a diff ref station Id '''
		# format 0000
		tmp = ""
		if len(self.__message.split(',')[14]) > 0:
			tmp = str(self.__message.split(',')[14])
		else:
			tmp = " "
		return tmp


class GPGSV_Class(object):
	'''
	Class for GPGSV message
	GNSS Satellites in View: Message ID GSV
	'''
	__message = "" #table of the elements
	__MessID = ""
	__MessNbOfMess = ""
	__MessNb = ""
	__MessSatellitesInView = ""
	
	
	def __init__(self, message):
		'''
		Constructor
		''' 
		self.__message = message[0:len(message)-3].split(',') #remove the 3 last chars because it is the checksum *hh
		

	def get_ID(self):
		''' Return MessId '''
		# GPGSV protocol header
		self.__MessID = str(self.__message[0])
		return self.__MessID

	def get_NbMess(self):
		''' return Total number of GSV messages 
		to be sent in this group 
		'''
		#Depending on the number of satellites tracked, multiple
		# messages of GSV data may be required. 
		#In some software versions, the m aximum number of satellites
		# reported as v isible is limit ed to 12, even though more may be visible

		self.__MessNbOfMess = str(self.__message[1])
		if len(self.__MessNbOfMess) > 0:
			return self.__MessNbOfMess
		else:
			return " "

	def get_MessNb(self):
		''' return the message number '''

		self.__MessNb = str(self.__message[2])
		if len(self.__MessNb) > 0:
			return self.__MessNb
		else:
			return " "

	def get_SatellitesInView(self):
		''' return number of Satellites in View '''
#		print "message: " + str(self.__message)
		
		if self.__message[3][0]=="0": #remove the first 0 in case of "09"
			self.__message[3]=self.__message[3][1:len(self.__message[3])]
			
		self.__MessSatellitesInView = int(self.__message[3])
		
		if int(self.__MessSatellitesInView) > 0:
			return int(self.__MessSatellitesInView)
		else:
			return 0

	def get_SatellitesChanel(self):
		''' return a satellites' data table by chanel '''
#		print"traitement get_SatellitesChanel"
		TabMess = None
		i = 0
		OFFSET=4 # -4 to remove the $GPGSV, total number of sentence, sentence ID and the total number of satellites
		nbSat= int( (len(self.__message) - OFFSET)/4 ) #nb satellite in the message
		TabMess = [["" for j in range(4)] for i in range(nbSat)] # 4 informations in by satellite: ID,Elevation,Azimuth,SNR
		i, j = 0,0
		while i < nbSat:
			j = 0
			while j < 4:
				TabMess[i][j]=str(self.__message[OFFSET+j+(4*i)])
				if j==3 and TabMess[i][j]=="": # SNR: display 0 for an empty string
					TabMess[i][j]="0"
				
				j += 1
			i += 1

		return TabMess


class GPGSA_Class(object):
	'''
	Class for GPGSA message
	Global Positioning System Fixed Data: Message ID GGA
	'''
	__message = ""
	__MessID = ""
	__MessLongitude = ""
	__MessMode1 = ""
	__MessMode2 = ""
	__MessSatellitesUsed = []
	__MessPDOP = ""
	__MessHDOP = ""
	__MessVDOP = ""

	def __init__(self, message):
		'''
		Constructor
		'''
		self.__message = message

	def get_ID(self):
		''' Return MessId '''
		# GPGSA protocol header

		self.__MessID = str(self.__message.split(',')[0])
		if self.__MessID == "$GPGSA":
			return self.__MessID
		else:
			return "Message error, wrong ID Message."

	def get_Mode1(self):
		''' return Mode1 '''
		#Mode1 = M -> Manual - Forced to operate in 2D or 3D mode
		#Mode1 = A -> 2D Automatic - Allowed to automatically switch 2D/3D

		self.__MessMode1 = str(self.__message.split(',')[1])
		if len(self.__MessMode1) > 0:
			return self.__MessMode1
		else:
			return " "

	def get_Mode2(self):
		''' return Mode2 '''
		#Mode2 = 1 -> Fix not available
		#Mode2 = 2 -> 2D (<4 SVs used)
		#Mode2 = 3 -> 3D (>3 SVs used)
		
		self.__MessMode2 = str(self.__message.split(',')[2])
		if len(self.__MessMode2) > 0:
			return self.__MessMode2
		else:
			return " "
		
	def get_SatellitesUsed(self):
		''' return a table of satellites used '''
		
		listSatUsed = self.__message.split(',')[3:15]
#		print"listSatUsed: " + str(listSatUsed)
		if len(listSatUsed) > 0:
			#print"list sat used: " + str(listSatUsed)
			i = 0
			for numSat in listSatUsed:
				#print"numSat: " + str(numSat) + "    long: " + str(len(numSat))
				if numSat != "" :
					i += 1
					#print"filtred numSat: " + str(numSat) + "   long: " + str(len(numSat))
					#self.__MessSatellitesUsed.append(str(numSat))

#			print self.__MessSatellitesUsed
#			print "Numb sat used: " + str(len(self.__MessSatellitesUsed))
			return i
		else:
			return 0

	def get_PDOP(self):
		''' return  Position Dilution of Precision'''
		#Position Dilution of Precision
		self.__MessPDOP = str(self.__message.split(',')[16])
		if len(self.__MessPDOP) > 0:
			return self.__MessPDOP
		else:
			return " "

	def get_HDOP(self):
		''' return Horizontal Dilution of Precision '''
		#Horizontal Dilution of Precision
		self.__MessHDOP = str(self.__message.split(',')[16])
		if len(self.__MessHDOP) > 0:
			return self.__MessHDOP
		else:
			return " "
		
	def get_VDOP(self):
		''' return Vertical Dilution of Precision '''
		#Vertical Dilution of Precision
		self.__MessVDOP = str(self.__message.split(',')[18])
		if len(self.__MessVDOP) > 0:
			return self.__MessVDOP
		else:
			return " "


class GPRMC_Class(object):
	'''
	Class for GPRMC message
	Recommended Minim um Specific GNSSData: Message ID RMC
	'''
	#private member of class
	__message = ""
	__MessID = ""
	__MessUTCTIME = ""
	__MessStatus = ""
	__MessLatitude = ""
	__MessNSIndic = ""
	__MessLongitude = ""
	__MessSOG = ""
	__MessCOG = ""
	__MessDate = ""
	__MessMagVar = ""
	__MessEWIndic = ""
	__MessMode = ""

	def __init__(self, message):
		'''
		Constructor
		'''
		self.__message = message

	def get_Id(self):
		''' Return MessId '''
		# RMC protocol header
		# type string
		self.__MessID = str(self.__message.split(',')[0])
		if len(self.__MessID) > 0:
			return self.__MessID
		else:
			return " "

	def get_UTCTIME(self):
		''' Return MessUTCTIME hhmmss.sss'''
		# type string hhmmss.sss
		tmp = ""
		try:
			if len(self.__message.split(',')[1]) > 0:
				UtcTime = str(self.__message.split(',')[1])
				tmp = UtcTime[0:2:1] + ' : ' + UtcTime[2:4:1] + ' : ' + UtcTime[4::1]
			else:
				tmp = " "
		except IndexError:
			tmp = " "
		return tmp


	def get_Status(self):
		'''return Status  '''
		# A=data valid or V=data not valid
		if len(self.__message.split(',')[2]) > 0:
			return str(self.__message.split(',')[2])
		else:
			return " "

	def get_Latitude(self):
		''' Return Latitutde ddmm.mmmm'''
		# The message is a string, for the numeric fields you have to convert 
		# the type string of the substring to the right type, int or float
		# type string
		if len(self.__message.split(',')[3]) > 0:
			latit_deg = float(self.__message.split(',')[3][0:2:1])
			latit_min = float(self.__message.split(',')[3][2:4:1] + '.' + self.__message.split(',')[3][5::1])
			self.__MessLatitude = str(latit_deg + latit_min/60)
		else:
			self.__MessLatitude = " "
			
		return self.__MessLatitude

	def get_NSIndic(self):
		''' return MessNSIndic, N=north or S=south '''
		# type string
		if len(self.__message.split(',')[4]) > 0:
			return str(self.__message.split(',')[4])
		else:
			return " "

	def get_Longitude(self):
		''' Return Longitude dddmm.mmmm'''
		# The message is a string, for the numeric fields you have to convert 
		# the type string of the substring to the right type, int or float
		#type string
		if len(self.__message.split(',')[5]) > 0:	
			longit_deg = float(self.__message.split(',')[5][0:3:1])
			longit_min = float(self.__message.split(',')[5][3:5:1] + '.' + self.__message.split(',')[5][6::1])
			# compute the coordinates
			self.__MessLongitude = str(longit_deg + longit_min/60) 
		else:
			self.__MessLongitude = " "

		return self.__MessLongitude

	def get_EWIndic(self):
		''' return EWIndic, E=east or W=west '''
		if len(self.__message.split(',')[6]) > 0:
			return str(self.__message.split(',')[6])
		else:
			return " "

	def get_SOG(self):
		''' return speed over ground in knots '''
		if len(self.__message.split(',')[7]) > 0:
			return str(self.__message.split(',')[7])
		else:
			return " "

	def get_COG(self):
		''' return Course Over Ground in degrees'''
		if len(self.__message.split(',')[8]) > 0:
			return str(self.__message.split(',')[8])
		else:
			return " "

	def get_Date(self):
		''' return the date, ddmmyy '''
		if len(self.__message.split(',')[9]) > 0:
			return str(self.__message.split(',')[9])
		else:
			return " "

	def get_MagVar(self):
		''' return Magnetic Variation, 
		E=east or W=west, in degrees. 
		'''
		if len(self.__message.split(',')[10]) > 0:
			return str(self.__message.split(',')[10])
		else:
			return " "

	def get_EWIndic2(self):
		''' return East /West Indicator, E=east 
		CSR Technology Inc. do es not support magnet ic declination.
		All  course over ground data are geodetic WGS84 directions 
		relativ e to true North.
		'''
		if len(self.__message.split(',')[11]) > 0:
			return str(self.__message.split(',')[11])
		else:
			return " "
		
	def get_Mode(self):
		''' return teh Mode.
		A=Autonomous
		D=DGPS
		E=DR
		N=Output Data Not Valid
		R=Coarse Position (Position was calculated based on one or more
			of the SVs having their states derived from almanac 
			parameters, as opposed to ephemerides)
		S=Simulator
		'''
		if len(self.__message.split(',')[12]) > 0:
			return str(self.__message.split(',')[12])
		else:
			return " "


class GNGSA_Class(object):
	'''
	Class for GNGSA message
	GNSS DOP and Active Satellites: Message ID GSA
	'''
	__message = ""
	__MessID = ""
	
	def __init__(self, message):
		'''
		Constructor
		'''
		self.__message = message[0:len(message)-3].split(',') #remove the 3 last chars because it is the checksum *hh
		
	#test the sequence length to check it is a valid sequence
	def isValidMsg(self):
		if len(self.__message)==18:
			return True
		else:
			return False
	def isFix(self):
		if self.__message[2]>1:
			return True
		else:
			return False

	def get_ID(self):
		''' Return MessId '''
		# GNGSA protocol header

		self.__MessID = str(self.__message[0])
		if self.__MessID == "$GNGSA":
			return self.__MessID
		else:
			return "Message error, wrong ID Message."

	def get_SatellitesUsed(self):
		''' return a table of satellites used '''
		
		listSatUsed = self.__message[3:15]
		i=0
		while i<len(listSatUsed):
			if listSatUsed[i]=="":
				del listSatUsed[i] #remove empty item
			else:
				i=i+1

		return listSatUsed


class GLGSV_Class(GPGSV_Class):
	'''
	Class for GLGSV message
	'''
	__message = ""
	__MessID = ""
	
	def __init__(self, message):
		'''
		Constructor
		'''
		self.__message = message
		self.GLGSV = GPGSV_Class.__init__(self, message)
		self.__glgsv()

	def __glgsv(self):
		return self.GLGSV 

class GNGSV_Class(object):
	'''
	Class for GNGSV message
	'''
	__message = ""
	__MessID = ""
	
	def __init__(self, message):
		'''
		Constructor
		'''
		self.__message = message

	def get_ID(self):
		''' Return MessId '''
		# GNGSV protocol header

		self.__MessID = str(self.__message.split(',')[0])
		if self.__MessID == "$GNGSV":
			return self.__MessID
		else:
			return "Message error, wrong ID Message."


class GPGLL_Class(object):
	'''
	Class for GPGLL message
	Geographic Position - Latitude/Longitude: Message ID GLL
	'''
	__message = ""
	__MessID = ""
	
	def __init__(self, message):
		'''
		Constructor
		'''
		self.__message = message

	def get_ID(self):
		''' Return MessId '''
		# GPGLL protocol header

		self.__MessID = str(self.__message.split(',')[0])
		if self.__MessID == "$GPGLL":
			return self.__MessID
		else:
			return "Message error, wrong ID Message."


class GPMSS_Class(object):
	'''
	Class for GPMSS message
	MSK Receiver Signal: Message ID MSS
	'''
	__message = ""
	__MessID = ""
	
	def __init__(self, message):
		'''
		Constructor
		'''
		self.__message = message

	def get_ID(self):
		''' Return MessId '''
		# GPMSS protocol header

		self.__MessID = str(self.__message.split(',')[0])
		if self.__MessID == "$GPMSS":
			return self.__MessID
		else:
			return "Message error, wrong ID Message."


class GPVTG_Class(object):
	'''
	Class for GPVTG message
	Course Over Ground and  Ground Speed: Message ID VTG
	'''
	__message = ""
	__MessID = ""
	
	def __init__(self, message):
		'''
		Constructor
		'''
		self.__message = message

	def get_ID(self):
		''' Return MessId '''
		# GPVTG protocol header

		self.__MessID = str(self.__message.split(',')[0])
		if self.__MessID == "$GPVTG":
			return self.__MessID
		else:
			return "Message error, wrong ID Message."


class GPZDA_Class(object):
	'''
	Class for GPZDA message
	Time and Date: Message ID ZDA
	'''
	__message = ""
	__MessID = ""
	
	def __init__(self, message):
		'''
		Constructor
		'''
		self.__message = message

	def get_ID(self):
		''' Return MessId '''
		# GPZDA protocol header

		self.__MessID = str(self.__message.split(',')[0])
		if self.__MessID == "$GPZDA":
			return self.__MessID
		else:
			return "Message error, wrong ID Message."


