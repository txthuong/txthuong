#!/bin/env python
# _*_ coding: utf-8 _*_
#----------------------------------------------------------------------------
# Name:			MSDeCall.py
# Goal:			Structure of MSD message for eCall
# Document: URD1– 5725.1– 002 /  72739 Edition 12
#
# Author:		refer below
## Version:		refer below
## Date:			refer below
## Property:		SagemComm
#----------------------------------------------------------------------------
#date              who                 version                 modification
#07-08-2012      jm Seillon             1.0.0                   
#
'''
Created on 7 août 2012
@author: jm Seillon
Document: URD1– 5725.1– 002 /  72739 Edition 12
Class MSD message for ecall 
'''
import ctypes

class MSDeCall(object):
	'''
	This class is a Singleton, it allows to create one and only one message MSD.
	'''

	instance = None
	''' 
	@note: Private Class attributs 
	'''
	__ID = 0 # MSD format version set to 1 to discriminate from later MSD formats.
	__MessageID = 0 # Message identifier
	__Control =  bin(0) # Bit sequence
	__VIN = "" # VIN number according ISO 3779
	__CallNumber="" #number of the PSAP to call
	__ActivationMode= 0
	__VehPropStrType = 0 # These parameters identify the type of vehicle energy
	__Timestamp = 0
	__VehicleLocation = None
	__VehicleDirection = 0
	__RecentVehicleLocation_o = None
	__NomberOfPassengers_o = 0
	__OptionalAdditionalData_o = ""
	__VehiculeType = 0
	__Confidence = None
	
	def __new__(self,classe): 
		''' 
		constructor 
		'''
		if classe.instance is None:
			classe.instance = object.__new__(classe)
		return classe.instance
	
	def __init__(self,classe):
#		''' Create inner objets '''
#		self.__VehicleLocation = self.__Location()
#		self.__RecentVehicleLocation_o = self.__RecVehiculeLocation() 
		pass
	
	''' getters and setters'''
	@classmethod
	def getID(self):
		'''
		@return: ID 
		@type: Integer
		@note:  MSD format version set to 1 to discriminate from later MSD formats.
				Later versions have to be backwards compatible with existing versions.
				Systems receiving an MSD shall support all standardised
				MSD versions, which are each uniquely identified using an
				MSD format version parameter which shall always be
				contained in the first byte of all (current and future) MSD versions.
		'''
		return self.__ID

	@classmethod
	def setID(self,IDMsd):
		'''
		@param ID: ID
		@type: Integer
		@note:  MSD format version set to 1 to discriminate from later MSD formats.
				Later versions have to be backwards compatible with existing versions.
				Systems receiving an MSD shall support all standardised
				MSD versions, which are each uniquely identified using an
				MSD format version parameter which shall always be
				contained in the first byte of all (current and future) MSD versions.
		'''
		self.__ID = IDMsd

	@classmethod
	def getMessageID(self):
		'''
		@return: Message identifier
		@type: Integer
		@note: Message identifier, starting with 1 for each new eCall session
				and has to be incremented with every application layer MSD
				retransmission following a new ‘send MSD’ request after the
				incident event.
		'''
		return self.__MessageID

	@classmethod
	def setMessageID(self,MessId):
		'''
		@param: Message identifier
		@type: Integer
		@note: Message identifier, starting with 1 for each new eCall session
				and has to be incremented with every application layer MSD
				retransmission following a new ‘send MSD’ request after the
				incident event.
		'''
		self.__MessageID = MessId

	@classmethod
	def getVehiculeType(self):
		'''
		@return: VehiculeType
		@type: Integer € [0;255]
		@note:  00001 = passenger vehicle (Class M1)
				00010 = buses and coaches (Class M2)
				00011 = buses and coaches (Class M3)
				00100 = light commercial vehicles (Class N1)
				00101 = heavy duty vehicles (Class N2)
				00110 = heavy duty vehicles (Class N3)
				00111 = motorcycles (Class L1e)
				01000 = motorcycles (Class L2e)
				01001 = motorcycles (Class L3e)
				01010 = motorcycles (Class L4e)
				01011 = motorcycles (Class L5e)
				01100 = motorcycles (Class L6e)
				01101 = motorcycles (Class L7e)
		'''
		return self.__VehiculeType

	@classmethod
	def setVehiculeType(self,ctrl):
		'''
		@param: VehiculeType
		@type: Integer € [0;255]
		@note:  00001 = passenger vehicle (Class M1)
				00010 = buses and coaches (Class M2)
				00011 = buses and coaches (Class M3)
				00100 = light commercial vehicles (Class N1)
				00101 = heavy duty vehicles (Class N2)
				00110 = heavy duty vehicles (Class N3)
				00111 = motorcycles (Class L1e)
				01000 = motorcycles (Class L2e)
				01001 = motorcycles (Class L3e)
				01010 = motorcycles (Class L4e)
				01011 = motorcycles (Class L5e)
				01100 = motorcycles (Class L6e)
				01101 = motorcycles (Class L7e)
		'''
		self.__VehiculeType = ctrl

	def getConfidence(self):
		'''
		@return: Confidence
		@type: Integer € [0;255]
		@note: 	1=Position can be trusted
				0=No confidence in position
		'''
		return self.__Confidence

	@classmethod
	def setConfidence(self,ctrl):
		'''
		@param: Confidence
		@type: Integer € [0;255]
		@note: 	1=Position can be trusted
				0=No confidence in position
		'''
		self.__Confidence = ctrl

	@classmethod
	def getVIN(self):
		'''
		@return: Vehicle identification
		@type: String
		@note: VIN number according ISO 3779
				World Manufacturer Index (WMI)
				Vehicle Type Descriptor (VDS)
				Vehicle Identification Sequence (VIS)
		'''
		return self.__VIN

	@classmethod
	def setVIN(self,VIN):
		'''
		@param: Vehicle identification
		@type: String
		@note: VIN number according ISO 3779
				World Manufacturer Index (WMI)
				Vehicle Type Descriptor (VDS)
				Vehicle Identification Sequence (VIS)
		'''
		self.__VIN = VIN
		
	def getCallNumber(self):
		return self.__CallNumber

	@classmethod
	def setCallNumber(self,CallNB):
		self.__CallNumber = CallNB

	@classmethod
	def getActivationMode(self):
		return self.__ActivationMode

	@classmethod
	def setActivationMode(self,actMode):
		#< activation mode>:	integer type:
		#0	manual activation
		#1	Automatic activation. If omitted default value is 1

		self.__ActivationMode = actMode
		
	@classmethod
	def getVehPropStrType(self):
		'''
		@return: Vehicle Propulsion storage type
		@type: Integer
		@note: These parameters identify the type of vehicle energy
				storage(s) present.
				0 = indicates a type of storage not present
				1 = indicates type of storage which is present
				All bits set to zero indicate an unknown type of energy
				storage.
				Bit 7: unused
				Bit 6: unused
				Bit 5: 1 = hydrogen storage
				Bit 4: 1 = electric energy storage (with more than 42V and
				100 Ah)
				Bit 3: 1 = liquid propane gas (LPG)
				Bit 2: 1 = compressed natural gas (CNG)
				Bit 1: 1 = diesel tank present
				Bit 0: 1 = gasoline tank present
				Note 1 This information may be unreliable if there has been a
				change of vehicle propulsion type (e.g. from gasoline to
				CNG).
				Note 2 More than one bit may be set if there is more than one
				type of energy storage present.
		'''
		return self.__VehPropStrType

	@classmethod
	def setVehPropStrType(self,VPST):
		'''
		@param: Vehicle Propulsion storage type
		@type: Integer
		@note: These parameters identify the type of vehicle energy
				storage(s) present.
				0 = indicates a type of storage not present
				1 = indicates type of storage which is present
				All bits set to zero indicate an unknown type of energy
				storage.
				Bit 7: unused
				Bit 6: unused
				Bit 5: 1 = hydrogen storage
				Bit 4: 1 = electric energy storage (with more than 42V and
				100 Ah)
				Bit 3: 1 = liquid propane gas (LPG)
				Bit 2: 1 = compressed natural gas (CNG)
				Bit 1: 1 = diesel tank present
				Bit 0: 1 = gasoline tank present
				Note 1 This information may be unreliable if there has been a
				change of vehicle propulsion type (e.g. from gasoline to
				CNG).
				Note 2 More than one bit may be set if there is more than one
				type of energy storage present.
		'''
		self.__VehPropStrType = VPST

	@classmethod
	def getTimestamp(self):
		'''
		@return: Timestamp
		@type: Integer
		@note: Timestamp of incident event. Seconds elapsed since midnight
				January 1st, 1970 UTC.
				Failure value for time stamp set to “0”.
		'''
		return self.__Timestamp

	@classmethod
	def setTimestamp(self,Tstamp):
		'''
		@param: Timestamp
		@type: Integer
		@note: Timestamp of incident event. Seconds elapsed since midnight
				January 1st, 1970 UTC.
				Failure value for time stamp set to “0”.
		'''
		self.__Timestamp = Tstamp

	@classmethod
	def getVehicleLocationLatitude(self):
		'''
		@return: Vehicle location latitude
		@type: Integer
		@note: Position latitude (WGS84)
				Value range (-324000000 to 324000000)
				Maximum value Latitude = 90°00’00.00”
										= 90*60*60.000” = 324000.000”
										= 324 000 000 Miliarcseconds
										= 0x134FD900
				Minimum value Latitude = -90°00’00.00”
										= -90*60*60.000” = -324000.000”
										= -324 000 000 Miliarcseconds
										= 0xECB02700
				Example 48°18’1.20” N = 48.3003333 lat
									= (48*3600)+(18*60)+1.20”=173881,200”
				Which encodes to the following value:
							= 173881200d=0x0A5D3770
				If latitude is invalid or unknown, the value 0x7FFFFFFF shall
				be transmitted.
		'''
		return self.__Location.getLatitude()

	@classmethod
	def setVehicleLocationLatitude(self,VLocLat=0):
		'''
		@param: Vehicle location latitude
		@type: Integer
		@note: Position latitude (WGS84)
				Value range (-324000000 to 324000000)
				Maximum value Latitude = 90°00’00.00”
										= 90*60*60.000” = 324000.000”
										= 324 000 000 Miliarcseconds
										= 0x134FD900
				Minimum value Latitude = -90°00’00.00”
										= -90*60*60.000” = -324000.000”
										= -324 000 000 Miliarcseconds
										= 0xECB02700
				Example 48°18’1.20” N = 48.3003333 lat
									= (48*3600)+(18*60)+1.20”=173881,200”
				Which encodes to the following value:
							= 173881200d=0x0A5D3770
				If latitude is invalid or unknown, the value 0x7FFFFFFF shall
				be transmitted.
		'''
		VLocLat=VLocLat.replace("°","")
		VLocLat=VLocLat.replace(".","")
		VLocLat=VLocLat.replace("'",".")
		VLocLat=VLocLat.replace("’",".")
		VLocLat=VLocLat.replace('”',"")
		VLocLat=VLocLat.replace('"',"")
		self.__Location.setLatitude(VLocLat)

	@classmethod
	def getVehicleLocationLongitude(self):
		'''
		@return: Vehicle location longitude
		@type: Integer
		@note: Position longitude (WGS84)
				Value range (-648000000 to 648000000)
				Maximum value Longitude = 180°00’00.00”
										= 180*60*60.000” = 648000.000”
										= 648 000 000 Miliarcseconds
										= 0x269FB200
				Minimum value Longitude = -180°00’00.00”
										= -180*60*60.000” = -648000.000”
										= -648 000 000 Miliarcseconds
										= 0xD9604E00
				Example 11°37’2.52” E = 11.6173666 long
										= (11*3600)+(37*60)+2.52”=41822.520”
				Which encodes to the following value:
							= 41822520d=0x027E2938
				If longitude is invalid or unknown, the value 0x7FFFFFFF
				shall be transmitted.
		'''
		return self.__Location.getLongitude()

	@classmethod
	def setVehicleLocationLongitude(self,VLocLong=0):
		'''
		@param: Vehicle location longitude
		@type: Integer
		@note: Position longitude (WGS84)
				Value range (-648000000 to 648000000)
				Maximum value Longitude = 180°00’00.00”
										= 180*60*60.000” = 648000.000”
										= 648 000 000 Miliarcseconds
										= 0x269FB200
				Minimum value Longitude = -180°00’00.00”
										= -180*60*60.000” = -648000.000”
										= -648 000 000 Miliarcseconds
										= 0xD9604E00
				Example 11°37’2.52” E = 11.6173666 long
										= (11*3600)+(37*60)+2.52”=41822.520”
				Which encodes to the following value:
							= 41822520d=0x027E2938
				If longitude is invalid or unknown, the value 0x7FFFFFFF
				shall be transmitted.
		'''
		VLocLong=VLocLong.replace("°","")
		VLocLong=VLocLong.replace(".","")
		VLocLong=VLocLong.replace("'",".")
		VLocLong=VLocLong.replace("’",".")
		VLocLong=VLocLong.replace('”',"")
		VLocLong=VLocLong.replace('"',"")
		self.__Location.setLongitude(VLocLong)

	@classmethod
	def getVehicleDirection(self):
		'''
		@return: Vehicle direction
		@type: Integer
		@note: Direction of travel in 2 degrees steps from magnetic north (0-358, clockwise)
				If direction of travel is invalid or unknown, the value 0xFF shall be used.
		'''
		return self.__VehicleDirection

	@classmethod
	def setVehicleDirection(self,VDir):
		'''
		@param: Vehicle direction
		@type: Integer
		@note: Direction of travel in 2 degrees steps from magnetic north (0-358, clockwise)
				If direction of travel is invalid or unknown, the value 0xFF shall be used.
		'''
		self.__VehicleDirection = VDir

	@classmethod
	def getRecentVehicleLocation_o_LatDeltN1(self):
		#_o_ = Optionel
		'''
		@return: Recent vehicle location n-1, latitude
		@type: Integer
		@note: Latitude delta (+ for North and – for South) with respect to
				Current Vehicle position in Block 7.
				1 Unit = 100 miliarcseconds (WGS84), which is
				approximately 3m.
				Coded value range (-512..511) representing -51 200 to
				+51 100 miliarcseconds, or from 51,2”S to 51,1”N from the
				current position.
		'''
		return self.__RecVehiculeLocation.getLatitudeDeltaN1()

	@classmethod
	def setRecentVehicleLocation_o_LatDeltN1(self,RVLocLatDN1):
		'''
		@param: Recent vehicle location n-1, latitude
		@type: Integer
		@note: Latitude delta (+ for North and – for South) with respect to
				Current Vehicle position in Block 7.
				1 Unit = 100 miliarcseconds (WGS84), which is
				approximately 3m.
				Coded value range (-512..511) representing -51 200 to
				+51 100 miliarcseconds, or from 51,2”S to 51,1”N from the
				current position.
		'''
		self.__RecVehiculeLocation.setLatitudeDeltaN1(RVLocLatDN1)

	@classmethod
	def getRecentVehicleLocation_o_LongtDeltN1(self):
		#_o_ = Optionel
		'''
		@return: Recent vehicle location n-1, longitude
		@type: Integer
		@note: Longitude delta (+ for East and – for West) with respect to
				Current Vehicle position in Block 7.
				1 Unit = 100 miliarcseconds (WGS84), which is
				approximately 3m.
				Coded value range (-512..511) representing -51 200 to
				+51 100 miliarcseconds, or from 51,2”W to 51,1”E from the
				current position.
		'''
		return self.__RecVehiculeLocation.getLongitudeDeltaN1()

	@classmethod
	def setRecentVehicleLocation_o_LongDeltN1(self,RVLocLongDN1):
		'''
		@param: Recent vehicle location n-1, longitude
		@type: Integer
		@note: Longitude delta (+ for East and – for West) with respect to
				Current Vehicle position in Block 7.
				1 Unit = 100 miliarcseconds (WGS84), which is
				approximately 3m.
				Coded value range (-512..511) representing -51 200 to
				+51 100 miliarcseconds, or from 51,2”W to 51,1”E from the
				current position.
		'''
		self.__RecVehiculeLocation.setLongitudeDeltaN1(RVLocLongDN1)

	@classmethod
	def getRecentVehicleLocation_o_LatDeltN2(self):
		#_o_ = Optionel
		'''
		@return: Recent vehicle location n-2, latitude
		@type: Integer
		@note: Latitude delta (+ for North and – for South) with respect to
				Recent Vehicle position n-1 in Block 9.
				1 Unit = 100 miliarcseconds (WGS84), which is
				approximately 3m.
				Coded value range (-512..511) representing -51 200 to
				+51 100 miliarcseconds, or from 51,2”S to 51,1”N from the
				location represented by Recent Vehicle Location n-1.
		'''
		return self.__RecVehiculeLocation.getLatitudeDeltaN2()

	@classmethod
	def setRecentVehicleLocation_o_LatDeltN2(self,RVLocLatDN2):
		'''
		@param: Recent vehicle location n-2, latitude
		@type: Integer
		@note: Latitude delta (+ for North and – for South) with respect to
				Recent Vehicle position n-1 in Block 9.
				1 Unit = 100 miliarcseconds (WGS84), which is
				approximately 3m.
				Coded value range (-512..511) representing -51 200 to
				+51 100 miliarcseconds, or from 51,2”S to 51,1”N from the
				location represented by Recent Vehicle Location n-1.
		'''
		self.__RecVehiculeLocation.setLatitudeDeltaN2(RVLocLatDN2)

	@classmethod
	def getRecentVehicleLocation_o_LongtDeltN2(self):
		#_o_ = Optionel
		'''
		@return: Recent vehicle location n-2, longitude
		@type: Integer
		@note: Longitude delta (+ for East and – for West) with respect to
				Recent Vehicle position in Block 9.
				Coded value range (-512..511) representing -51 200 to
				+51 100 miliarcseconds, or from 51,2”W to 51,1”E from the
				location represented by Recent Vehicle Location n-1.
		'''
		return self.__RecVehiculeLocation.getLongitudeDeltaN2()

	@classmethod
	def setRecentVehicleLocation_o_LongDeltN2(self,RVLocLongDN2):
		'''
		@param: Recent vehicle location n-2, longitude
		@type: Integer
		@note: Longitude delta (+ for East and – for West) with respect to
				Recent Vehicle position in Block 9.
				Coded value range (-512..511) representing -51 200 to
				+51 100 miliarcseconds, or from 51,2”W to 51,1”E from the
				location represented by Recent Vehicle Location n-1.
		'''
		self.__RecVehiculeLocation.setLongitudeDeltaN2(RVLocLongDN2)

	@classmethod
	def getNomberOfPassengers_o(self):
		'''
		@return: No. of passengers
		@type: Integer
		@note: Minimum known number of fastened seatbelts, to be set to
				0xFF or the optional parameter omitted if no information is
				available.
				Note This information is indicative only as it may be not
				always be reliable in providing exact information about the
				number of passengers (e.g. because seatbelts may not be
				fastened by passengers or for other reasons).
		'''
		return self.__NomberOfPassengers_o

	@classmethod
	def setNomberOfPassengers_o(self,NOPsg):
		'''
		@param: No. of passengers
		@type: Integer
		@note: Minimum known number of fastened seatbelts, to be set to
				0xFF or the optional parameter omitted if no information is
				available.
				Note This information is indicative only as it may be not
				always be reliable in providing exact information about the
				number of passengers (e.g. because seatbelts may not be
				fastened by passengers or for other reasons).
		'''
		self.__NomberOfPassengers_o = NOPsg

	@classmethod
	def getOptionalAdditionalData_o(self):
		'''
		@return: Optional additional data
		@type: String
		@note: Further 103 bytes of data encoded as in ASN.1 definition.
				Note 1 ASN.1 provides already the indication of whether
				optional data is included by simply identifying the optional
				additional data field as optional.
				Note 2 Additional Data field may include an address where
				other relevant related data or functions are available.
		'''
		return self.__OptionalAdditionalData_o

	@classmethod
	def setOptionalAdditionalData_o(self,OAD):
		'''
		@param: Optional additional data
		@type: String
		@note: Further 103 bytes of data encoded as in ASN.1 definition.
				Note 1 ASN.1 provides already the indication of whether
				optional data is included by simply identifying the optional
				additional data field as optional.
				Note 2 Additional Data field may include an address where
				other relevant related data or functions are available.
		'''
		self.__OptionalAdditionalData_o = OAD

	class __Location(object):
		'''
		inner Class for the vehicle location.
		'''
		__Latitude = 0
		__Longitude = 0

		def __init__(self):
			''' constructor '''
	
		''' gettters and setters'''
		@classmethod
		def getLatitude(self):
			'''
			@return: latitude
			@type: Integer
			'''
			return self.__Latitude
	
		@classmethod
		def setLatitude(self,lat=0):
			'''
			@param: latitude
			@type: Integer
			'''
			self.__Latitude = lat
	
		@classmethod
		def getLongitude(self):
			'''
			@return: longitude
			@type: Integer
			'''
			return self.__Longitude
	
		@classmethod
		def setLongitude(self,longt=0):
			'''
			@param: longt
			@type: Integer
			'''
			self.__Longitude = longt

	class __RecVehiculeLocation(object):
		'''
		Inner Class for recent vehicle delta location, at t-1 and t-2
		'''
		__LatitudeDeltaN1 = 0
		__LongitudeDeltaN1 = 0
		__LatitudeDeltaN2 = 0
		__LongitudeDeltaN2 = 0

		def __init__(self):
			''' constructor '''
	
		''' getters and setters'''
		@classmethod
		def getLatitudeDeltaN1(self):
			'''
			@return: latitude delta for t-1
			@type: Integer
			'''
			return self.__LatitudeDeltaN1
	
		@classmethod
		def setLatitudeDeltaN1(self,LatDdeltN1=0):
			'''
			@param: latitude delta for t-1
			@type: Integer
			'''
			self.__LatitudeDeltaN1 = LatDdeltN1
	
		@classmethod
		def getLatitudeDeltaN2(self):
			'''
			@return: latitude delta for t-2 
			@type: Integer
			'''
			return self.__LatitudeDeltaN2
	
		@classmethod
		def setLatitudeDeltaN2(self,LatDdeltN2=0):
			'''
			@param: latitude delta for t-2
			@type: Integer
			'''
			self.__LatitudeDeltaN2 = LatDdeltN2
	
		@classmethod
		def getLongitudeDeltaN1(self):
			'''
			@return: longtitude delta for t-1
			@type: Integer
			'''
			return self.__LongitudeDeltaN1
	
		@classmethod
		def setLongitudeDeltaN1(self,LongtDdeltN1=0):
			'''
			@param: longtitude delta for t-1
			@type: Integer
			'''
			self.__LongitudeDeltaN1 = LongtDdeltN1
	
		@classmethod
		def getLongitudeDeltaN2(self):
			'''
			@return: longtitude delta for t-2 
			@type: Integer
			'''
			return self.__LongitudeDeltaN2
	
		@classmethod
		def setLongitudeDeltaN2(self,LongtDdeltN2=0):
			'''
			@param: longtitude delta for t-2
			@type: Integer
			'''
			self.__LongitudeDeltaN2 = LongtDdeltN2


def main():
	''' main function for test'''
	MyMSD = MSDeCall(MSDeCall)
#	MSD2 = MSDeCall(MSDeCall)
#	MSD1.setID(10) #IGNORE:E1103
#	vll = MSD1.getVehicleLocationLatitude()
#	MSD2.setID(35)
#	MSD2.setVehicleLocationLatitude(48)
#	MSD2.setRecentVehicleLocation_o_LatDeltN2(5)
#	IDMSD = MSD2.getID() #IGNORE:E1103
#	VLoc = MSD1.getVehicleLocationLatitude()
#	gRVL = MSD1.getRecentVehicleLocation_o_LatDeltN2()
#	print "ID mess: ",IDMSD
#	print "Veh loc latitude (t-1): ",vll
#	print "Vehicle location lat (t): ",VLoc
#	print "Rec vehicle location delta 2: ",gRVL
#	#msd1ID = MSD1.getID()+5
#	print "Id: ",MSD1.getID(), MSD1.getID()+5
#	MSD1.setID(123)
#	print "class meth ID: ",MSD2.getID()
#	a=f=g=h=1
#	b=c=d=e=0
#	
#	control = a*2**0 + b*2**1 + c*2**2 + d*2**3 + e*2**4 + f*2**5 + g*2**6 + h*2**7
#	MSD2.setControl(control)
#	print control
#	print MSD2.getControl()
#	
#	
##========================================================

if __name__ == '__main__':
	main()

