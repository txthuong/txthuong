#!/bin/env python
# _*_ coding: utf-8 _*_

#----------------------------------------------------------------------------
# Name:			Mux0710.py
#
# Goal:			This module manages the MUX
#
# Author:		refer below
#
# Version:		refer below
#
# Date:			refer below
#
# Property:		SagemComm
#----------------------------------------------------------------------------


#date              who                 version                 modification
#2009-2011         JM Rufflé           1.0..1.7                creation and modifications
#22-09-2011        JF Weiss            1.8.1                   add comments and light modifications
#xx-03-2013        Gary Zhang          1.9.6                   advanced MUX
#06-05-2013        Frank Yang          1.9.7                   add new function SagMuxWaitAndMatchResp for response matching
#04-08-2015        Bob Tai             1.9.8                   add MUX match response function: SagMuxWaitnMatchResp with similar usage as
#                                                              SagWaitnMatchResp in ComModuleAPI
#10-08-2015        Bernard Lee         1.9.8.1                 add SagMuxWaitnMatchResp1 and SagMuxWaitAndDecodeDataResp


from ComModuleAPI import *
from Frame0710 import *
from Mux0710Dlg import *

import VarGlobal
import time

class Mux_Static_Variables(object):
	def __init__(self):
		'''	
		goal of the class : this class encapsulate static variables, used by this module
		INPUT : none
		OUTPUT : none
		'''
		self.FrameHeader = 6							# Size of MUX header 
		self.muxDataMaxLen = 31 - self.FrameHeader		# Maximum size of data
		
		self.Mux0710Thread = {}
		
		# Le verrou Serial_Out_mutex sécurisé
		self.Serial_Out_mutex = threading.Lock()
		self.firstOne = True
		self.dlciOnLeftBox = 1
		self.dlciOnRightBox = 2
		
		self.debugMode = False


MuxstaticVariables = Mux_Static_Variables()

def SafePrintOnMuxDlg(DecodedFrame,send=True):
	'''	
	goal of the method : this method is used to print MUX information ; it uses MUTEX to avoid mixing display from several threads
	INPUT : DecodedFrame, information to display
			send, boolean
	OUTPUT : none
	'''
	if DecodedFrame.crc and DecodedFrame.length != 0 and DecodedFrame.FrameType == UIH:
		if DecodedFrame.DLCI == MuxstaticVariables.dlciOnLeftBox:
			printOnLeftMuxTextBox(data2string(DecodedFrame.Info), send)
		
		if DecodedFrame.DLCI == MuxstaticVariables.dlciOnRightBox:
			printOnRightMuxTextBox(data2string(DecodedFrame.Info), send)

def SafePrintDecodedFrame(time, hCom, text, DecodedFrames='', color=None):
	'''	
	goal of the method : this method is used to print MUX information ; it uses MUTEX to avoid mixing display from several threads
	INPUT : DecodedFrame, information to display
	INPUT : time, time to display
			hCom, COM port instance
			text, text to display before the decoded frame
			DecodedFrame, decoded frame to display
			color, display colour
	OUTPUT : none
	'''
	try:
		if DecodedFrames.DLCI == 0 and DecodedFrames.Control == UIH:
			if   DecodedFrames.Info[0] & 0xFC == 0xE0:	# test if a Modem Status Command
				DLCI		 = (DecodedFrames.Info[2]&0xFC)>>2
				Flow_Control = (DecodedFrames.Info[3]&0x02)>>1 == 1
				DSR			 = (DecodedFrames.Info[3]&0x04)>>2 == 1
				CTS			 = (DecodedFrames.Info[3]&0x08)>>3 == 1
				RI			 = (DecodedFrames.Info[3]&0x40)>>6 == 1
				DCD			 = (DecodedFrames.Info[3]&0x80)>>7 == 1
				SafePrint(time, hCom, "RECV: MUX 07.10 Protocol : Modem Status Command On DLCI : "+str(DLCI)+" | Flow Control = "+str(Flow_Control)+" | DSR = "+str(DSR)+" | CTS = "+str(CTS)+" | RI = "+str(RI)+" | DCD = "+str(DCD),color=10)
				
				if DLCI == MuxstaticVariables.dlciOnLeftBox:
					SetDCDOnLeftMuxTextBox(DCD)
				if DLCI == MuxstaticVariables.dlciOnRightBox:
					SetDCDOnRightMuxTextBox(DCD)
			elif DecodedFrames.Info[0] & 0xFC == 0x80:	# test if a DLC parameter negotiation (PN)
				SafePrint(time, hCom, "RECV: MUX 07.10 Protocol : DLC Parameter Negotiation (PN)",color=10)
			elif DecodedFrames.Info[0] & 0xFC == 0xC0:	# test if a Multiplexer close down (CLD)
				SafePrint(time, hCom, "RECV: MUX 07.10 Protocol : Multiplexer Close Down (CLD)",color=10)
			elif DecodedFrames.Info[0] & 0xFC == 0x20:	# test if a Test command (test)
				SafePrint(time, hCom, "RECV: MUX 07.10 Protocol : Test command (test)",color=10)
			elif DecodedFrames.Info[0] & 0xFC == 0xA0:	# test if a Flow control On Command (FCon)
				SafePrint(time, hCom, "RECV: MUX 07.10 Protocol : Flow Control On Command (FCon)",color=10)
			elif DecodedFrames.Info[0] & 0xFC == 0x60:	# test if a Flow control Off Command (FCoff)
				SafePrint(time, hCom, "RECV: MUX 07.10 Protocol : Flow Control Off command (FCoff)",color=10)
			elif DecodedFrames.Info[0] & 0xFC == 0x10:	# test if a Non Supported command response (NSC)
				SafePrint(time, hCom, "RECV: MUX 07.10 Protocol : Non Supported Command response (NSC) | Command Type : ")+str((DecodedFrames.Info[2]&0xFC)>>2,color=10)
			elif DecodedFrames.Info[0] & 0xFC == 0x90:	# test if a Remote Port Negotiation command (RPN)
				SafePrint(time, hCom, "RECV: MUX 07.10 Protocol : Remote Port Negotiation command (RPN) On DLCI :")+str((DecodedFrames.Info[2]&0xFC)>>2,color=10)
			elif DecodedFrames.Info[0] & 0xFC == 0x50:	# test if a Remote Line Status Command (RLS)
				SafePrint(time, hCom, "RECV: MUX 07.10 Protocol : Remote Line Status command (RLS) On DLCI :")+str((DecodedFrames.Info[2]&0xFC)>>2,color=10)
			elif DecodedFrames.Info[0] & 0xFC == 0xD0:	# test if a Service Negotiation Command (SNC)
				SafePrint(time, hCom, "RECV: MUX 07.10 Protocol : Service Negotiation command (SNC) On DLCI :")+str((DecodedFrames.Info[2]&0xFC)>>2,color=10)
			
			if MuxstaticVariables.debugMode:
				SafePrint(time,hCom,'DEBUG RCV:'+text+str(DecodedFrames.FrameHex),color=11)
		else:
			SafePrint(time,hCom,text+str(DecodedFrames.FrameHex),color)
	except:
		SafePrint(time,hCom,text+str(DecodedFrames),color)
	VarGlobal.myColor = VarGlobal.colorLsit[8]

def SagWaitThread0710Frame(hCom,dlci,nbOfFrame,timeout = 1000):
	'''	
	goal of the method : this method waits for received frame 
	INPUT : hCom, COM port instance
			dlci, dlci number (0 is the control DLCI)
			timeout, (ms) timeout for receiving frame
	OUTPUT : resultTab, including received frames
	'''
	resultTab = []
	
	flag = True
	start = datetime.now()
	Timeout = timeout
	
	event = MuxstaticVariables.Mux0710Thread[hCom].GetEvent(dlci)
	while flag:
		#call to WaitEvent() during timeout seconds 
		#bug xxxx v1.8.1 WaitEvent has its timeout in milliseconds, not in seconds
		flag = WaitEvent(event, Timeout)
		if flag:
			Table_Of_Frames = MuxstaticVariables.Mux0710Thread[hCom].ReadTableOfFrame(dlci)
			if len(resultTab) + len(Table_Of_Frames) >= nbOfFrame:
				flag = False
				for elem in Table_Of_Frames[:nbOfFrame-len(resultTab)]:
					HexElem = elem.FrameHex
					SafePrintDecodedFrame(elem.dt,MuxstaticVariables.Mux0710Thread[hCom].hCom,text="RECV: ",DecodedFrames=elem,color=7)
					resultTab.append(elem)
				MuxstaticVariables.Mux0710Thread[hCom].AddFramesAtStartOfTableOfFrame(Table_Of_Frames[nbOfFrame:])
			else:
				for elem in Table_Of_Frames:
					HexElem = elem.FrameHex
					SafePrintDecodedFrame(elem.dt,MuxstaticVariables.Mux0710Thread[hCom].hCom,text="RECV: ",DecodedFrames=elem,color=7)
					resultTab.append(elem)
		
		diff = datetime.now() - start
		Timeout = timeout - (diff.seconds * 1000.0 + diff.microseconds / 1000.0)
		if Timeout <= 0:
			SafePrint(None, MuxstaticVariables.Mux0710Thread[hCom].hCom,"RECV: ERROR time out, %s frame(s) missing"%(nbOfFrame-len(resultTab)),7)
	
	return resultTab

class MuxThread(Thread):
	def __init__(self, hCom, displayRECV=True):
		'''	
		goal of the method : constructor
		INPUT : hcom COM port
				displayRECV (boolean) flag to display or not the frames received on screen
		OUTPUT : none
		'''
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None,hCom,"	DEBUG		MuxThread.__init__()",color=2)
		Thread.__init__(self,name="MUX listen COM"+str(hCom.port+1))
		self.hCom = hCom
		self.displayRECV = displayRECV
		
		self.PowerSaveControlEnable = False
		self.SendWaikUp = False
		#SagEvent() is like SagCreateEvent()
		#creation of an event instance
		self.eventWaikUp = SagEvent("WaikUp")
		self.endOfWaikUp = False
		
		self.FlowControlEnable = False
		self.table_Of_Event_DLCI_FlowControl = {} #dictionnary, i.e. key/value values are Python events
		
		#creation of two MUTEX instances
		self.write_tbl_Frame_mutex   = threading.Lock()
		self.create_Recv_Event_mutex = threading.Lock()
		
		self.Table_Of_Frames = {}	#dictionnary, i.e. key/value
		self.Table_Of_Events = {}	#dictionnary, i.e. key/value
		
		self.Table_Of_DLCI_Status = []	#empty list
		
		self.Serial_Out_mutex = threading.Lock()
		
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None,hCom,"	DEBUG	fin MuxThread.__init__()", color=2)
	
	def run(self): 
		'''	
		goal of the method : this method starts the thread ; when started, the thread indefinitely loop waiting for input data in COM port
			when it detects data, it wits a little time to try receive a complete frame ; it calls then the automaton for frame analyzis
			It is the central engine of MUX processing
		INPUT : none
		OUTPUT : none
		'''
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None,self.hCom,"	DEBUG		Begin MuxThread.run() : thread MuxThread launched",color=2)
			SafePrint(None,self.hCom,"	DEBUG		@@@thread launched@@@",color=2)

		Serial_In = []
		try:
			while True:

				evtOk = self.hCom.waitRXData()
				if evtOk:
					time.sleep(0.01)
					bufferSize = self.hCom.inWaiting()
					if bufferSize:
						buffer = self.hCom.read(bufferSize)
						dt = datetime.now()
						if buffer:
							for i in range(len(buffer)):
								Serial_In.append(ord(buffer[i]))
						
						if MuxstaticVariables.debugMode:
							SafePrint(dt,self.hCom,"DEBUG : Serial In : %s"%table2hex(Serial_In),color=11)
						#call automaton
						Serial_In = self.__automate(Serial_In, dt)

			SafePrint(None,hCom,"end of thread")
		
		except SystemExit:
			self.hCom.stop()
			raise SystemExit
		except:
			VarGlobal.myColor = VarGlobal.colorLsit[9]	 							
			SafePrintError(None, self.hCom, "Thread Error!")
	
	def __automate(self, Serial_In, dt):
		'''	
		goal of the method : the goal of this method is to decode and analyze received frames (called by thread whend data is received)
			It is called automate because of its automaton like processing
		INPUT : Serial_In, (list) received data
				dt, current time
		OUTPUT : Temp_Frame, (list) data just received in hCom
		'''
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None,self.hCom,"	DEBUG		Begin MuxThread.__automate()",color=2)
			
		#create instance of InitFrame object (includes only variables, no method)
		DecodedFrame=InitFrame()
		
		DecodedFrameTable=[]
		Temp_Frame = []
		
		State_New_Frame=0
		State_Wait_Address=1
		State_Wait_CTRL=2
		State_Wait_Length_First=3
		State_Wait_Length_Last=4
		State_Wait_Info=5
		State_Wait_FCS=6
		State_Wait_End_Flag=7
		
		Decode_State = State_New_Frame
#+ Advanced mode support
		#print 'Received data length = %d'%len(Serial_In)
		# Decode Advanced mode frame
		if VarGlobal.AdvancedMode == True:
			#print Serial_In
			i = 0
			while i<len(Serial_In):
				if (Serial_In[i] == 0x7D and (Serial_In[i+1] == 0x7D or Serial_In[i+1] == 0x7E)):
					Temp_Frame.append(Serial_In[i+1])
					i = i + 2
				else:
					Temp_Frame.append(Serial_In[i])
					i = i + 1
			Serial_In = Temp_Frame;
			Temp_Frame = []
			#print 'after decode: len=%d'%len(Serial_In),
			#print Serial_In
#- Advanced mode support
		for elem in Serial_In:
			if   Decode_State == State_New_Frame:
				if VarGlobal.DEBUG_LEVEL == "DEBUG":
					SafePrint(None,self.hCom,"	DEBUG		automaton : NEW FRAME state",color=2)
					SafePrint(None,self.hCom,"	DEBUG		received elem = " + str(hex(elem)),color=2)
				#if opening flag
				#+ Advanced mode support
				if ((elem == BASIC_FLAG and VarGlobal.AdvancedMode == False) or (elem == ADVANCE_FLAG and VarGlobal.AdvancedMode == True)):
				#- Advanced mode support
					#we add the received data in list and change state
					Temp_Frame.append(elem)
					Decode_State = State_Wait_Address
				else:
					#create instance of Frame object
					#NJF v1.18.1 why creating the same instance ???
					DecodedFrame = InitFrame()
			
			elif Decode_State == State_Wait_Address:
				if VarGlobal.DEBUG_LEVEL == "DEBUG":
					SafePrint(None,self.hCom,"	DEBUG		automaton : WAIT ADDRESS state",color=2)
					SafePrint(None,self.hCom,"	DEBUG		received elem = " + str(hex(elem)),color=2)
				#several flags begin of Sequence can be received to wake up, or to ack a wake up sent by PC
				#+ Advanced mode support
				if ((elem == BASIC_FLAG and VarGlobal.AdvancedMode == False) or (elem == ADVANCE_FLAG and VarGlobal.AdvancedMode == True)):
				#- Advanced mode support
					DecodedFrame.ReceivedFlag+=1
					if DecodedFrame.ReceivedFlag>=3:
						SafePrint(None,self.hCom,"MUX 07.10 Waik Up flag recv",color=10)
						#if a wake up signal has been sent to module
						if self.SendWaikUp:
							#received 3 F9 : just set event for wake up
							self.eventWaikUp.set()
							self.SendWaikUp = False
						#else : no signal has been sent to the module, and we receive a wake up signal => we were in reduced power state
						#so wake up and send back the wake up signal
						else:
							self.__SendWaikUp()
						
						Temp_Frame = []
				else:
					#let's say it is the address field : append in received frame and change state
					Temp_Frame.append(elem)
					DecodedFrame.Address=elem
					Decode_State = State_Wait_CTRL
			
			elif Decode_State == State_Wait_CTRL:
				if VarGlobal.DEBUG_LEVEL == "DEBUG":
					SafePrint(None,self.hCom,"	DEBUG		automaton : WAIT CONTROL state",color=2)
					SafePrint(None,self.hCom,"	DEBUG		received elem = " + str(hex(elem)),color=2)
				Temp_Frame.append(elem)
				DecodedFrame.Control=elem
				#+ Advanced mode support
				if (VarGlobal.AdvancedMode == False):
					Decode_State = State_Wait_Length_First
				else:
					Decode_State = State_Wait_End_Flag   #advanced mode
				#- Advanced mode support
			elif Decode_State == State_Wait_Length_First:
				if VarGlobal.DEBUG_LEVEL == "DEBUG":
					SafePrint(None,self.hCom,"	DEBUG		automaton : LENGTH FIRST state",color=2)
					SafePrint(None,self.hCom,"	DEBUG		received elem = " + str(hex(elem)),color=2)
				Temp_Frame.append(elem)
				LengthFirst=elem
				DecodedFrame.LengthFirst=LengthFirst
				if LengthFirst & EA == EA:
					DecodedFrame.NbLength = 1
					DecodedFrame.length = DecodedFrame.LengthFirst>>1
					if LengthFirst == 1:
						Decode_State = State_Wait_FCS
					else:
						Decode_State = State_Wait_Info
				else:
					Decode_State = State_Wait_Length_Last
			
			elif Decode_State == State_Wait_Length_Last:
				if VarGlobal.DEBUG_LEVEL == "DEBUG":
					SafePrint(None,self.hCom,"	DEBUG		automaton : LENGTH LAST state (second length byte because EA bit has been set)",color=2)
					SafePrint(None,self.hCom,"	DEBUG		received elem = " + str(hex(elem)),color=2)
				Temp_Frame.append(elem)
				LengthLast=elem
				DecodedFrame.LengthLast=LengthLast
				DecodedFrame.NbLength = 2
				DecodedFrame.length = (DecodedFrame.LengthFirst>>1) + (DecodedFrame.LengthLast<<7)
				if DecodedFrame.LengthLast==0 and DecodedFrame.LengthFirst==0:
					Decode_State = State_Wait_FCS
				else:
					Decode_State = State_Wait_Info
			
			elif Decode_State == State_Wait_Info:
				if VarGlobal.DEBUG_LEVEL == "DEBUG":
					SafePrint(None,self.hCom,"	DEBUG		automaton : WAIT INFO state (wait information field)",color=2)
					SafePrint(None,self.hCom,"	DEBUG		received elem = " + str(hex(elem)),color=2)
				Temp_Frame.append(elem)
				DecodedFrame.Info.append(elem)
				
				#njf v1.8.1 should == only. If > that means either inconsistency or the FCS has already been received
				if len(DecodedFrame.Info)>=DecodedFrame.length :	# Wait more info?
					Decode_State = State_Wait_FCS
			
			elif Decode_State == State_Wait_FCS:
				if VarGlobal.DEBUG_LEVEL == "DEBUG":
					SafePrint(None,self.hCom,"	DEBUG		automaton : WAIT FCS state",color=2)
					SafePrint(None,self.hCom,"	DEBUG		received elem = " + str(hex(elem)),color=2)
				Temp_Frame.append(elem)
				Fcs=elem
				DecodedFrame.Fcs=Fcs
				Decode_State = State_Wait_End_Flag
			
			elif Decode_State == State_Wait_End_Flag:
				if VarGlobal.DEBUG_LEVEL == "DEBUG":
					SafePrint(None,self.hCom,"	DEBUG		automaton : WAIT END FLAG state",color=2)
					SafePrint(None,self.hCom,"	DEBUG		received elem = " + str(hex(elem)),color=2)
				#njf v1.8.1 should check content for consistency check, no ?
				Temp_Frame.append(elem)
				#+ Advanced mode support
				if (VarGlobal.AdvancedMode == True):
					DecodedFrame.Info.append(elem)
					if(elem != ADVANCE_FLAG):
						continue
					DecodedFrame.Fcs = Temp_Frame[len(Temp_Frame)-2]
					del DecodedFrame.Info[len(DecodedFrame.Info)-1] # delete tail flag
					del DecodedFrame.Info[len(DecodedFrame.Info)-1] # delete Fcs
					DecodedFrame.NbLength = 1
					DecodedFrame.length = len(DecodedFrame.Info)
				#- Advanced mode support
				#now the received frame is complete, we analyse it
				DecodedFrame.Flag  = elem
				DecodedFrame.Frame = Temp_Frame
				DecodedFrame.FrameHex = table2hex(Temp_Frame)
				DecodedFrame.DLCI = DecodedFrame.Address >> 2
				DecodedFrame.CR	= DecodedFrame.Address & 0x02
				DecodedFrame.PF = DecodedFrame.Control & 0x01
				DecodedFrame.FrameType  = DecodedFrame.Control & 0xEF
				#check the CRC consistency
				DecodedFrame.crc = CRC_Verify(DecodedFrame)
				DecodedFrame.dt = dt
				
				#add the newly decoded frame into the array of all received and decoded frames
				DecodedFrameTable.append(DecodedFrame)
				
				# test if this frame is a Power Save Control
				# that means the module wish to enter reduced power state
				if DecodedFrame.DLCI == 0 and DecodedFrame.Control == UIH and DecodedFrame.Info[0]&0xFC == 0x04:
					#@@@ njf v1.8.1 according to 27.010 §5.4.7, before sending the ack, all frame in progress shall be sent on the data DLCI
					SafePrint(None,self.hCom,"MUX 07.10 Protocol PSC frame detected",color=10)
					self.__SendPSCResponse()
					self.PowerSaveControlEnable = True #module is in power save state
				# test if a Modem Status Command
				elif DecodedFrame.DLCI == 0 and DecodedFrame.Control == UIH and DecodedFrame.Info[0] & 0xFC == 0xE0:
					DLCI		 = (DecodedFrame.Info[2]&0xFC)>>2
					Flow_Control = (DecodedFrame.Info[3]&0x02)>>1 == 1
					DSR			 = (DecodedFrame.Info[3]&0x04)>>2 == 1
					CTS			 = (DecodedFrame.Info[3]&0x08)>>3 == 1
					RI			 = (DecodedFrame.Info[3]&0x40)>>6 == 1
					DCD			 = (DecodedFrame.Info[3]&0x80)>>7 == 1
					if self.displayRECV:
						SafePrintDecodedFrame(dt,self.hCom,"RECV frame on dlci %s : "%DecodedFrame.DLCI,DecodedFrame,color=7)
					
					self.FlowControlEnable = Flow_Control
					if Flow_Control:
						#reset the event from dictionary
						self.table_Of_Event_DLCI_FlowControl[DLCI].clear()
					else:
						#set the event to true in dictionary
						self.table_Of_Event_DLCI_FlowControl[DLCI].set()
					
					if DLCI in self.Table_Of_DLCI_Status:
						self.Table_Of_DLCI_Status[self.Table_Of_DLCI_Status.index(DLCI)]=[Flow_Control,DSR,CTS,RI,DCD]
					else:
						self.Table_Of_DLCI_Status.append([DLCI,[Flow_Control,DSR,CTS,RI,DCD]])
				else:
					if self.displayRECV:
						SafePrintDecodedFrame(dt,self.hCom,"RECV frame on dlci %s : "%DecodedFrame.DLCI,DecodedFrame,color=7)
					
					#add the received and decoded frame in the global table
					self.__WriteTableOfFrame(DecodedFrame,add=True)
				Temp_Frame=[]
				#reinit DecodedFrame
				DecodedFrame=InitFrame()
				
				Decode_State = State_New_Frame
			else:
				if VarGlobal.DEBUG_LEVEL == "DEBUG":
					SafePrint(None,self.hCom,"	DEBUG		=====================================",color=2)
					SafePrint(None,self.hCom,"	DEBUG		automaton : UNKNOWN AUTOMATON STATE  ",color=2)
					SafePrint(None,self.hCom,"	DEBUG		ASSERT : this case shall never happen",color=2)
					SafePrint(None,self.hCom,"	DEBUG		DecodeState = " + str(Decode_State),color=2)
					SafePrint(None,self.hCom,"	DEBUG		=====================================",color=2)
					raise SystemExit
				
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None,self.hCom,"	DEBUG		End MuxThread.__automate()",color=2)
			
		return Temp_Frame
	
	def __WriteTableOfFrame(self,DecodedFrame,add=False):
		'''	
		goal of the method : the goal of this method is to add a frame in the table of received frames and to set "received fraame" event in the table of events of the DLCI
		INPUT : DecodedFrame, instance of Frame0710.InitFrame class 
				add, (boolean) if true, add the decoded frame in the table of received frames
		OUTPUT : none
		'''
		self.write_tbl_Frame_mutex.acquire()  # prise de verrou
		
		dlci = DecodedFrame.DLCI
		if dlci not in self.Table_Of_Events:
			self.__CreateRecvEvent(dlci)
		event = self.Table_Of_Events.get(dlci) #Table_Of_Event is a dictionnary ; returns data for this dlci
		
		if dlci in self.Table_Of_Frames and add:
			#there are already frames in the table of frame
			tabTemp = self.Table_Of_Frames.get(dlci)
			tabTemp.append(DecodedFrame)
			self.Table_Of_Frames[dlci]=tabTemp
		else:
			#it is the first frame
			self.Table_Of_Frames[dlci]=[DecodedFrame]
		event.set()
		self.write_tbl_Frame_mutex.release()  # relache de verrou
	
	def __CreateRecvEvent(self,dlci):
		'''	
		goal of the method : the goal of this method is to add the "received fraame" event in the table of events of the DLCI
		INPUT : dlci, DLCI number
		OUTPUT : none
		'''
		self.create_Recv_Event_mutex.acquire()  # prise de verrou
		if dlci not in self.Table_Of_Events:
			self.Table_Of_Events[dlci]=SagEvent('Event Recv on dlci %s'%dlci)
		self.create_Recv_Event_mutex.release()  # relache de verrou
	
	def __SendWaikUp(self):
		'''	
		goal of the method : the goal of this methods is to send three times the Begin of frame sequence to wake up the module if it is in power save mode
		INPUT : none
		OUTPUT : none
		'''
		#@@@njf v1.8.1 normally 27.010 §5.4.7 requests to send continuous flags (during T3) and stop only when it receives them back
		#@@@ and if the PC is in reduced power state and receives wake up flags from module it sends wake up flags up to receiving first valid frame
		
		self.SendWaikUp = True
		cmd = ''
		SafePrint(None, self.hCom, 'MUX 07.10 Protocol SEND Waik Up flags', color = 10)
		#+ Advanced mode support
		if VarGlobal.AdvancedMode == False:
			for i in range(4):
				cmd += chr(BASIC_FLAG)
		else:
			for i in range(4):
				cmd += chr(ADVANCE_FLAG)
		self.hCom.write(cmd)
	
	def __SendPSCResponse(self):
		'''	
		goal of the method : this methods sends back a Power saving response (when a frame Power Saving Control PSC has beenr eceived)
		INPUT : none
		OUTPUT : none
		'''
		
		#The PSC response is sent in a UIH frame
		#remember UIH = Basic Flag - Address field - Control Field - Length of Info (1 oe 2 octets) - Info (n octets) - Frame Checking Sequence - Basic Flag
		#address field 0x03 means DLCI=0 C/R=1 (response), EA=1 (no extension)
		#control field 0xEF means UIH with P/F=0
		#Legnth of info = 0x05 means EA=1 (no extension) and length = 2 octets : encapsulate the PSC
		#Info = 0x41 0x01 - 0x41 is the Type field of PSC with EA=1 and C/R=0 (@@@njf v1.8.1 : strange ! shouln't be 1 because response from responder to Initiater ?
		#					0x01 is the length byte of PSC with EA=1 (no extension), 0 octets length and so no value
		#FCS = 0xF2
		#+ Advanced mode support
		if VarGlobal.AdvancedMode == False:
			PSC =[BASIC_FLAG, 0x03, 0xEF, 0x05, 0x41, 0x01, 0xF2, BASIC_FLAG]
		else:
			PSC =[ADVANCE_FLAG, 0x03, 0xEF, 0x41, 0x01, 0x70, ADVANCE_FLAG]
		#- Advanced mode support
		cmd = ''.join(chr(elem) for elem in PSC)
		self.hCom.write(cmd)
	
	def AddFramesAtStartOfTableOfFrame(self,frames):
		'''
		goal of the method : the goal of this method is to add frames at the beginning of the table of received frames
		INPUT : frames, frames to add at the beginning of the table of received frames
		OUTPUT : none
		'''
		self.write_tbl_Frame_mutex.acquire()  # prise de verrou
		if frames != []:
			dlci=frames[0].DLCI
			
			if MuxstaticVariables.debugMode:
				SafePrint(None,None,"DEBUG : Add frames at start of table of frame : on dlci"%(dlci),color=11)
			
			if dlci not in self.Table_Of_Events:
				self.__CreateRecvEvent(dlci)
			event = self.Table_Of_Events.get(dlci)
			
			if dlci in self.Table_Of_Frames:
				tabTemp = self.Table_Of_Frames.get(dlci)
				tabTemp = frames + tabTemp
				self.Table_Of_Frames[dlci]=tabTemp
			else:
				self.Table_Of_Frames[dlci]=[frames]
			event.set()
		self.write_tbl_Frame_mutex.release()  # relache de verrou
	
	def ReadTableOfFrame(self,dlci):
		'''	
		goal of the method : 
		INPUT : dlci, DLCI number
		OUTPUT : FrameTable, the table of read frames from Table_Of_Frame and remove them in the table
		'''
		self.write_tbl_Frame_mutex.acquire()  # MUTEX acquire
		#built in function ; Table_Of_Frames is a dictionnary
		FrameTable = self.Table_Of_Frames.get(dlci,[])
		#empty the content for DLCI entry
		self.Table_Of_Frames[dlci] = []
		self.write_tbl_Frame_mutex.release()  # MUTEX release
		return FrameTable
	
	def GetEvent(self, dlci):
		'''	
		goal of the method : this method gets the event from table of event, for a given DLCI
		INPUT : dlci, DLCI number
		OUTPUT : event, 
		'''
		if dlci not in self.Table_Of_Events:
			self.__CreateRecvEvent(dlci)
		self.create_Recv_Event_mutex.acquire()  # prise de verrou
		event = self.Table_Of_Events.get(dlci)	# Table_Of_Events : dictionnary
		self.create_Recv_Event_mutex.release()  # relache de verrou
		return event
	
	def SendFrame(self,frames):
		'''	
		goal of the method : the goal of this method is to send data on the COM port ; if the module is in reduced power state, it must be wake up before
		INPUT : frames, data to send to the module
		OUTPUT : none
		'''
		#if module is in power save state, wake it up
		if self.PowerSaveControlEnable:
			self.endOfWaikUp = False
			self.__SendWaikUp()
			self.eventWaikUp.wait(10) #@@@ njf v1.8.1 should be T3 timer according to 27.010 §5.4.7
			#@@@ njf v1.8.1 : if timeout, an alarm should be raised
			self.eventWaikUp.clear()
			self.PowerSaveControlEnable = False
		
		self.hCom.write(frames)
	
	def SendHexaBin(self, data, hex = [],display=True):
		'''	
		goal of the method : the goal of this method is to send binary file, and fill the argument in hexa mode if needed
		INPUT : data, data to send
				hex, (list) if empty then fill it with data in hexa format
				display, (boolean) if true, then verbose mode
		OUTPUT : none
		'''
		try:
			if self.hCom.isOpen() == False:
				self.hCom.open()
			
			cmd=''
			if hex == []:
				hexa = True
			else:
				hexa = False
			
			#change list into string
			for elem in data:
				cmd += chr(elem)
				if hexa:
					#add the elements in hexa format into the data given argument
					hex.append("0x%0.2X"%elem)
			self.SendFrame(cmd)
			if display:
				SafePrint(None, self.hCom, 'SEND: %s'%(str(hex)), color = 6)
		except SystemExit:
			raise SystemExit
		except:
			SafePrintError(None, self.hCom,"SEND in MUX: Error!")
		
	def MuxSend(self, typeFrame, dlci, data = 0 , cr=1, pf=None, display=True):
		'''	
		goal of the method : the goal of this method is to format data to send into a DLCI frame (or to open a mux connection using SABM)
		INPUT : typeFrame,
				dlci, DLCI number
				data, data to send
				cr, Command/Receive flag
				pf, Poll/Final bit
				display, (boolean) if true then verbose mode
		OUTPUT : none
		'''
		try:
			self.Serial_Out_mutex.acquire()  # prise de verrou
			if pf == None:
				if typeFrame == SABM:
					pf = 1
				elif typeFrame == UIH:
					pf = 0
			
			param[CR]   = cr
			param[DLCI] = dlci
			param[PF]   = pf
			param[DATA] = data
			
			if data != 0:
				dataToSend = param[DATA]
				if display and type(data)==str:
					SafePrint(None, self.hCom, 'SENDING on dlci %s : %s'%(dlci,str(param[DATA]).replace("\r","\\r").replace("\n","\\n")), color = 6)
			else:
				dataToSend=" "
			
			#send n frames (according to the max size)
			for i in range(int(len(dataToSend)/(MuxstaticVariables.muxDataMaxLen*1.0)+0.999999999999999)):
				if data != 0:
					param[DATA] = data[i*MuxstaticVariables.muxDataMaxLen : (i+1)*MuxstaticVariables.muxDataMaxLen]
				#+ Advanced mode support
				FrameToSend = buildFrame(typeFrame,param,VarGlobal.AdvancedMode)
				#- Advanced mode support

				#if flow control enabled and if saturated
				if self.FlowControlEnable and dlci in self.table_Of_Event_DLCI_FlowControl:
					#wait for the event for 300 seconds
					self.table_Of_Event_DLCI_FlowControl[dlci].wait(300)
					SagSleep(0.001,silent=True)
				self.SendHexaBin(FrameToSend.Frame, FrameToSend.FrameHex,display=display)
				SafePrintOnMuxDlg(FrameToSend)
		except SystemExit:
			raise SystemExit
		except:		
			SafePrintError(None, self.hCom, "Error can't SEND MUX FRAME!")
		finally:
			self.Serial_Out_mutex.release()  # relache de verrou
	
	def MuxSendFile(self, dlci, FileName, EOF = None):
		'''	
		goal of the method : 
		INPUT : 
		OUTPUT : none
		'''
		try:
			file = open(FileName, 'rb')
			tab = file.read()
			file.close()
			
			SafePrint(None, self.hCom,'SEND: Start Send File : %s'%(FileName),color = 4)
			self.MuxSend(UIH, dlci, data = tab, display=False)
			if EOF != None:
				self.MuxSend(UIH, dlci, data = EOF, display=False)
			SafePrint(None, self.hCom,'SEND: Send File : %s complet'%(FileName),color = 4)
		except SystemExit:
			raise SystemExit
		except:
			self.hCom.close()
			SafePrintError(None, self.hCom, "SEND: Error!")
			raise stop_exception
	
	def MuxOpenDLCI(self, dlci, timeout = 1000):
		'''	
		goal of the method : 
		INPUT : 
		OUTPUT : none
		'''
		VarGlobal.myColor = VarGlobal.colorLsit[2]
		if dlci == 0:
			SafePrint(None,self.hCom,"Open Mux Control Channel")
		else:
			SafePrint(None,self.hCom,"Open Channel %s"%dlci)
			if MuxstaticVariables.firstOne:
				SetLeftBoxTitle("Channel DLCI %s"%dlci)
				MuxstaticVariables.dlciOnLeftBox=dlci
			else:
				SetRightBoxTitle("Channel DLCI %s"%dlci)
				MuxstaticVariables.dlciOnRightBox=dlci
			MuxstaticVariables.firstOne = not(MuxstaticVariables.firstOne)
		VarGlobal.myColor = VarGlobal.colorLsit[8]
		self.table_Of_Event_DLCI_FlowControl[dlci] = SagEvent("Flow Control on dlci %s"%dlci)
		self.table_Of_Event_DLCI_FlowControl.get(dlci).set()
		self.MuxSend(SABM,dlci)
		DecodedFrame = SagWaitThread0710Frame(self.hCom,nbOfFrame=1,dlci=dlci, timeout=timeout)

#####################
## Functions could be use by user ##
#####################
def SagMuxSetMaximumFrameSize(size=31):
	'''	
	goal of the method : 
	INPUT : 
	OUTPUT : none
	'''
	MuxstaticVariables.muxDataMaxLen = size - MuxstaticVariables.FrameHeader

def SagMuxStartThreadWait(hCom,displayRECV=True):
	'''	
	goal of the method : this method instanciates and starts the MuxThread object (thread) ; so, one specific thread is started for MUX processing
	INPUT : hCom, COM port instance
			displayRECV, (boolean) flag to display or not on screen the frames received
	OUTPUT : none
	'''
	try:
		if VarGlobal.MODE != VarGlobal.DEMO_MODE:
			SafePrint(None, hCom,"start thread listen mux",10)
		if hCom not in MuxstaticVariables.Mux0710Thread:
			#instanciation of MuxThrad class and launch new thread
			if VarGlobal.DEBUG_LEVEL == "DEBUG":
				SafePrint(None,hCom,"	DEBUG		thread MuxThread is created", color=2)
			#create the thread (1 thread for each hCom
			MuxstaticVariables.Mux0710Thread[hCom] = MuxThread(hCom,displayRECV)
			if VarGlobal.DEBUG_LEVEL == "DEBUG":
				SafePrint(None,hCom,"	DEBUG		thread MuxThread is starting", color=2)
			#start the thread
			MuxstaticVariables.Mux0710Thread[hCom].start()
	except SystemExit:
		raise SystemExit
	except:		
		raise
		#SafePrintError(TimeDisplay(), "(COM%d) Error can't start thread!"%(hCom.port+1))

def SagMuxStopThreadWait(hCom):
	'''	
	goal of the method : this method stops the MUX thread
	INPUT : hCom, COM port instance
	OUTPUT : none
	'''
	try:
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None,hCom,"	DEBUG		thread MuxThread is stopping", color=2)
		MuxstaticVariables.Mux0710Thread[hCom].stop()
		MuxstaticVariables.Mux0710Thread[hCom] = None
		if VarGlobal.MODE != VarGlobal.DEMO_MODE:
			SafePrint(None, None,"stop thread listen mux",10)
	except SystemExit:
		raise SystemExit
	except:		
		SafePrintError(None, MuxstaticVariables.Mux0710Thread[hCom].hCom, "Error can't start thread!"%())

def SagMuxOpenDLCI(hCom, dlci, timeout = 1000):
	'''	
	goal of the method : this method opens a DLCI (Data Link Connection. For MUX, it shall open 1 control DLCI and at least one data DLCI
	This opening is done sending a SABM frame ; in case of success, module ack with an UA frame (Unumbered Ack), else by a DM frame (Disconnected Mode)
	INPUT : hCom, COM port instance
			dlci, dlci number (0 is the control DLCI)
			timeout, timeout for receiving the opening ack/nack
	OUTPUT : none
	'''
	if hCom in MuxstaticVariables.Mux0710Thread:
		MuxstaticVariables.Mux0710Thread[hCom].MuxOpenDLCI(dlci, timeout)
	else:
		SafePrint(None, hCom, "Error can't open DLCI %s!"%dlci)

def SagMuxSend(hCom, typeFrame, dlci, data = 0 , cr=1, pf=None, display=True):
	'''	
	goal of the method : this method sends information inside a MUX frame on a given DLCI
	INPUT : hCom, COM port instance
			typeFrame, type of MUX frame (typically UIH frame (Unumbered Information, with Header check)
			dlci, dlci number (0 is the control DLCI)
			data, information to send inside the frame (e.g. 'ATE\r)
			cr, (boolean) flag to indicate it is a Command or a Response
			pf, Poll/Final bit set to 1 if SABM frame (connection requested)
			display, (bolean) indicate if information about sednding shall be displayed or not
	OUTPUT : none
	'''
	if hCom in MuxstaticVariables.Mux0710Thread:
		MuxstaticVariables.Mux0710Thread[hCom].MuxSend(typeFrame,dlci,data,cr,pf,display)
	else:
		SafePrint(None, hCom, "Error can't SEND MUX FRAME!")

def SagMuxSendFile(hCom, dlci, FileName, EOF = None):
	'''	
	goal of the method : this method sends a file inside a MUX frame on a given DLCI
	INPUT : hCom, COM port instance
			dlci, dlci number (0 is the control DLCI)
			Filename, file name to send
			EOF, end of file pattern
	OUTPUT : none
	'''
	if hCom in MuxstaticVariables.Mux0710Thread:
		MuxstaticVariables.Mux0710Thread[hCom].MuxSendFile(dlci, FileName, EOF)
	else:
		SafePrint(None, hCom, "Error can't SEND MUX FILE!")

def SagMuxWaitAndDecodeData(hCom,data , dlci, timeout = 10000):
	'''	
	goal of the method : this method waits and decodes received frame 
		Problem : it searches in all already received frame and remove all frames analysed which don't match
					so if the searched frame doesn't exist, it will remove all frames following thisone
	INPUT : hCom, COM port instance
			data, information to check in received frame ; it can be a list
			dlci, dlci number (0 is the control DLCI)
			timeout, timeout for receiving frame
	OUTPUT : none
	'''
	
	if type(data) == list:
		data=data2string(data)
	
	DecodedFramesTab = []
	
	flagTimeout = False
	flagFind = False
	crc = False
	start = datetime.now()
	Timeout = timeout
	lenTable_Of_Frames=0
	
	#instance of MuxThread class ; this event seems to be set when frame has been received from DLCI
	event = MuxstaticVariables.Mux0710Thread[hCom].GetEvent(dlci)
	
	while not(flagTimeout or flagFind) :
		#call to WaitEvent() during timeout seconds 
		#bug xxxx v1.8.1 WaitEvent has its timeout in milliseconds, not in seconds
		flagTimeout = not(WaitEvent(event, Timeout))
		
		if not(flagTimeout):
			#Mux0710Thread[hCom] is a thread of MuxThread class
			Table_Of_Frames = MuxstaticVariables.Mux0710Thread[hCom].ReadTableOfFrame(dlci)
			lenTable_Of_Frames += len(Table_Of_Frames)
			for DecodedFrames in Table_Of_Frames:
				if VarGlobal.DEBUG_LEVEL == "DEBUG":
					SafePrint(None, hCom,"	DEBUG			SagMuxWaitAndDecodeData() DecodedFrames (hex) " + str(DecodedFrames.FrameHex), color=2)
					SafePrint(None, hCom,"	DEBUG			data to find " + data,color=2)
				crc += DecodedFrames.crc
				DecodedFramesTab.append(DecodedFrames)
				if not(flagFind):
					SafePrintOnMuxDlg(DecodedFrames,False)
					#if the keyword has been found in frame
					if len(DecodedFrames.Info)>0 and data2string(DecodedFrames.Info).find(data) != -1:
						flagFind = True
						#if it remains some frames in input table, put them back at the beginning
						if len(Table_Of_Frames)>len(DecodedFramesTab):
							MuxstaticVariables.Mux0710Thread[hCom].AddFramesAtStartOfTableOfFrame(Table_Of_Frames[(len(DecodedFramesTab)-lenTable_Of_Frames):])
						break
		
		diff = datetime.now() - start
		Timeout = timeout - (diff.seconds * 1000.0 + diff.microseconds / 1000.0)
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None, hCom,"	DEBUG			remaining timeout= " + str(Timeout), color=2)
		if Timeout <= 0:
			SafePrint(None, MuxstaticVariables.Mux0710Thread[hCom].hCom,"RECV: ERROR time out",color=7)
			flagTimeout = True
	
	if crc==len(DecodedFramesTab) and flagFind:
		if VarGlobal.MODE != VarGlobal.DEMO_MODE:
			SafePrint(None,hCom,"--->  Success <CRC OK>")
		else:
			SafePrint(None,hCom,"")
	elif crc and not(flagFind):
		SafePrint(None,hCom,"---> Fail <CRC OK>")
	elif not(crc) and flagFind:
		if VarGlobal.MODE != VarGlobal.DEMO_MODE:
			SafePrint(None,hCom,"---> Success <CRC error>")
		else:
			SafePrint(None,hCom,"")
	elif not(crc) and not(flagFind):
		SafePrint(None,hCom,"---> Fail <CRC error>")
	
	return DecodedFramesTab, flagTimeout

def SagMuxWaitAndDecodeDataResp(hCom, waitpattern, dlci, timeout = 10000):
	'''	
	goal of the method : this method waits and decodes received frame 
		Problem : it searches in all already received frame and remove all frames analysed which don't match
					so if the searched frame doesn't exist, it will remove all frames following this one
	INPUT : hCom, COM port instance
			waitpattern : the matching pattern for the received frames
			dlci, dlci number (0 is the control DLCI)
			timeout, timeout for receiving frame
	OUTPUT : Received data (List and String)
	'''
	
	DecodedFramesTab = []
	receivedResp = ""
	
	flagTimeout = False
	flagFind = False
	crc = False
	start = datetime.now()
	Timeout = timeout
	lenTable_Of_Frames=0
	
	#instance of MuxThread class ; this event seems to be set when frame has been received from DLCI
	event = MuxstaticVariables.Mux0710Thread[hCom].GetEvent(dlci)
	
	while not(flagTimeout or flagFind) :
		#call to WaitEvent() during timeout seconds 
		#bug xxxx v1.8.1 WaitEvent has its timeout in milliseconds, not in seconds
		flagTimeout = not(WaitEvent(event, Timeout))
		
		if not(flagTimeout):
			#Mux0710Thread[hCom] is a thread of MuxThread class
			Table_Of_Frames = MuxstaticVariables.Mux0710Thread[hCom].ReadTableOfFrame(dlci)
			lenTable_Of_Frames += len(Table_Of_Frames)
			for DecodedFrames in Table_Of_Frames:
				if VarGlobal.DEBUG_LEVEL == "DEBUG":
					SafePrint(None, hCom,"	DEBUG			SagMuxWaitAndDecodeData() DecodedFrames (hex) " + str(DecodedFrames.FrameHex), color=2)
					SafePrint(None, hCom,"	DEBUG			data to find " + data,color=2)
				crc += DecodedFrames.crc
				DecodedFramesTab.append(DecodedFrames)
				if not(flagFind):
					SafePrintOnMuxDlg(DecodedFrames,False)
					if len(DecodedFrames.Info)>0:
						receivedResp += data2string(DecodedFrames.Info)
						#if the data pattern has been matched in the response
						for (each_elem) in waitpattern:
							if fnmatch.fnmatchcase(receivedResp, each_elem):
								flagFind = True
								break
						if flagFind:
							#if it remains some frames in input table, put them back at the beginning
							if len(Table_Of_Frames)>len(DecodedFramesTab):
								MuxstaticVariables.Mux0710Thread[hCom].AddFramesAtStartOfTableOfFrame(Table_Of_Frames[(len(DecodedFramesTab)-lenTable_Of_Frames):])
								break
		
		diff = datetime.now() - start
		Timeout = timeout - (diff.seconds * 1000.0 + diff.microseconds / 1000.0)
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None, hCom,"	DEBUG			remaining timeout= " + str(Timeout), color=2)
		if Timeout <= 0:
			SafePrint(None, MuxstaticVariables.Mux0710Thread[hCom].hCom,"RECV: ERROR time out",color=7)
			flagTimeout = True
	
	if crc==len(DecodedFramesTab) and flagFind:
		if VarGlobal.MODE != VarGlobal.DEMO_MODE:
			SafePrint(None,hCom,"--->  Success <CRC OK>")
		else:
			SafePrint(None,hCom,"")
	elif crc and not(flagFind):
		SafePrint(None,hCom,"---> Fail <CRC OK>")
	elif not(crc) and flagFind:
		if VarGlobal.MODE != VarGlobal.DEMO_MODE:
			SafePrint(None,hCom,"---> Success <CRC error>")
		else:
			SafePrint(None,hCom,"")
	elif not(crc) and not(flagFind):
		SafePrint(None,hCom,"---> Fail <CRC error>")
	
	return DecodedFramesTab, receivedResp

def SagMuxWaitnMatchResp(hCom, waitpattern, dlci, timeout, response="\r\nOK\r\n", condition="wildcard", update_result="critical", log_msg="logmsg", printmode="symbol"):
    '''    
    goal of the method : this method waits and decodes received frame then compare it  
        
    INPUT : hCom, COM port instance
            data, information to check in received frame ; it can be a list
            dlci, dlci number (0 is the control DLCI)
            timeout, timeout for receiving frame
            response, delimiter for the response; assume the response ends with \r\n\OK\r\n
    OUTPUT : none
    '''
    if condition not in ["wildcard"]:
        condition = "wildcard"

    result=False
    decodedframestab, flagtimeout = SagMuxWaitAndDecodeData(hCom,response, dlci, timeout) 
    if (len(decodedframestab)==0) or (flagtimeout==True):        
        return result
    respmsg=""
    for i in decodedframestab:
        respmsg=respmsg+(str(i.strInfo()))
    result=SagMatchResp(respmsg, waitpattern, condition, update_result, log_msg, printmode)
    return result

#   decodedframestab = SagMuxWaitAndDecodeData(hCom,response, dlci, timeout)
#   respmsg = ""
#   for i in decodedframestab:
#       respmsg += (str(i.strInfo()))
#   return SagMatchResp(respmsg, waitpattern, condition, update_result, log_msg, printmode)

def SagMuxWaitnMatchResp1(hCom, waitpattern, dlci, timeout, condition="wildcard", update_result="critical", log_msg="logmsg", printmode="symbol"):
    '''    
    goal of the method : combine SagMuxWaitAndDecodeDataResp() and SagMatchResp()
        
    INPUT : hCom, COM port instance
            waitpattern : the matching pattern for the received frames
            dlci, dlci number (0 is the control DLCI)
            timeout, timeout for receiving frame
    OUTPUT : Boolean >> True:response matched, False:repsonse mis-matched
    '''
    if condition not in ["wildcard"]:
        condition = "wildcard"

    (decodedframestab, response) = SagMuxWaitAndDecodeDataResp(hCom, waitpattern, dlci, timeout)
    return SagMatchResp(response, waitpattern, condition, update_result, log_msg, printmode)

def SagMuxWaitAndMatchResp(hCom,data , dlci, timeout = 10000):
	'''	
	goal of the method : this method waits and decodes received frame 
		Problem : it searches in all already received frame and remove all frames analysed which don't match
					so if the searched frame doesn't exist, it will remove all frames following thisone
	INPUT : hCom, COM port instance
			data, information to check in received frame ; it can be a list
			dlci, dlci number (0 is the control DLCI)
			timeout, timeout for receiving frame
	OUTPUT : none
	'''
	
	if type(data) == list:
		data=data2string(data)
	
	DecodedFramesTab = []
	
	flagTimeout = False
	flagFind = False
	crc = False
	start = datetime.now()
	Timeout = timeout
	lenTable_Of_Frames=0
	MatchedResp = False
	
	#instance of MuxThread class ; this event seems to be set when frame has been received from DLCI
	event = MuxstaticVariables.Mux0710Thread[hCom].GetEvent(dlci)
	
	while not(flagTimeout or flagFind) :
		#call to WaitEvent() during timeout seconds 
		flagTimeout = not(WaitEvent(event, Timeout))
		
		if not(flagTimeout):
			#Mux0710Thread[hCom] is a thread of MuxThread class
			Table_Of_Frames = MuxstaticVariables.Mux0710Thread[hCom].ReadTableOfFrame(dlci)
			lenTable_Of_Frames += len(Table_Of_Frames)
			for DecodedFrames in Table_Of_Frames:
				if VarGlobal.DEBUG_LEVEL == "DEBUG":
					SafePrint(None, hCom,"	DEBUG			SagMuxWaitAndDecodeData() DecodedFrames (hex) " + str(DecodedFrames.FrameHex), color=2)
					SafePrint(None, hCom,"	DEBUG			data to find " + data,color=2)
				crc += DecodedFrames.crc
				DecodedFramesTab.append(DecodedFrames)
				if not(flagFind):
					SafePrintOnMuxDlg(DecodedFrames,False)
					#if the keyword has been found in frame
					if len(DecodedFrames.Info)>0 and data2string(DecodedFrames.Info).find(data) != -1:
						flagFind = True
						#if it remains some frames in input table, put them back at the beginning
						if len(Table_Of_Frames)>len(DecodedFramesTab):
							MuxstaticVariables.Mux0710Thread[hCom].AddFramesAtStartOfTableOfFrame(Table_Of_Frames[(len(DecodedFramesTab)-lenTable_Of_Frames):])
						break
		
		diff = datetime.now() - start
		Timeout = timeout - (diff.seconds * 1000.0 + diff.microseconds / 1000.0)
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None, hCom,"	DEBUG			remaining timeout= " + str(Timeout), color=2)
		if Timeout <= 0:
			SafePrint(None, MuxstaticVariables.Mux0710Thread[hCom].hCom,"RECV: ERROR time out",color=7)
			flagTimeout = True
	
	if crc==len(DecodedFramesTab) and flagFind:
		if VarGlobal.MODE != VarGlobal.DEMO_MODE:
			SafePrint(None,hCom,"--->  Success <CRC OK>")
		else:
			SafePrint(None,hCom,"")
		MatchedResp = True
	elif crc and not(flagFind):
		SafePrint(None,hCom,"---> Fail <CRC OK>")
		MatchedResp = False
	elif not(crc) and flagFind:
		if VarGlobal.MODE != VarGlobal.DEMO_MODE:
			SafePrint(None,hCom,"---> Success <CRC error>")
		else:
			SafePrint(None,hCom,"")
		MatchedResp = False
	elif not(crc) and not(flagFind):
		SafePrint(None,hCom,"---> Fail <CRC error>")
		MatchedResp = False
	
	return MatchedResp
	
def SagMuxWaitData(hCom,dlci, EOF ='', timeout = 30000, SaveDataToFile = False, FileName = ""):
	'''	
	goal of the method : 
	INPUT : 
	OUTPUT : none
	'''
	if type(EOF)==int:
		timeout=EOF
		EOF=''
	
	DecodedFramesTab = []
	flag = True
	FindFlag=False
	crc = False
	lenTable_Of_Frames=0
	
	SaveDataToFile = FileName!=""  or SaveDataToFile
	
	if SaveDataToFile:
		if FileName == "":
				FileName = "Data On DLCI %s.txt"%dlci
				FileName = FileName.split(".")[0] + " " + ("%s"%datetime.now()).split(".")[0].replace(":",".") + "." + FileName.split(".")[1]
		fic = open(FileName,'w')
		fic.close()
	
	event = MuxstaticVariables.Mux0710Thread[hCom].GetEvent(dlci)
	
	while flag:
		flag = WaitEvent(event, timeout/1000.0)
		if flag:
			Table_Of_Frames = MuxstaticVariables.Mux0710Thread[hCom].ReadTableOfFrame(dlci)
			lenTable_Of_Frames += len(Table_Of_Frames)
			
			for DecodedFrame in Table_Of_Frames:
				SafePrintOnMuxDlg(DecodedFrame,False)
				if DecodedFrame.DLCI==dlci or DecodedFrame.DLCI==0:
					if SaveDataToFile:
						if DecodedFrame.length != 0 and DecodedFrame.FrameType == 0xEF and DecodedFrame.DLCI == dlci:
							file = open(FileName, 'ab')
							file.write(data2string(DecodedFrame.Info))
							file.close()
				crc += DecodedFrame.crc
				DecodedFramesTab.append(DecodedFrame)
				
				if EOF !=''  and data2string(DecodedFrame.Info).find(EOF) != -1 and DecodedFrame.DLCI==dlci:
					flag = False
					FindFlag = True
					#if it remains some frames in input table
					if lenTable_Of_Frames>len(DecodedFramesTab):
						MuxstaticVariables.Mux0710Thread[hCom].AddFramesAtStartOfTableOfFrame(Table_Of_Frames[(len(DecodedFramesTab)-lenTable_Of_Frames):])
					break
	
	if FindFlag:
		SafePrint(None, MuxstaticVariables.Mux0710Thread[hCom].hCom,"EOF found on dlci: %s"%(dlci),color=7)
	else:
		SafePrint(None, MuxstaticVariables.Mux0710Thread[hCom].hCom,"End of waiting data on dlci: %s"%(dlci),color = 7)
	
	if crc==len(DecodedFramesTab):
		if VarGlobal.MODE != VarGlobal.DEMO_MODE:
			SafePrint(None,hCom,"--->  Success <CRC OK>		SagMuxWaitData")
	else:
		SafePrint(None,hCom,"---> Fail <CRC error>		SagMuxWaitData")
	return DecodedFramesTab


######################
## Functions with virtual serial port ##
######################
class ThreadRouteComtoDlci(Thread):
	def __init__(self,hCom,dlci,MuxThread = None):
		'''	
		goal of the method : constructor
		INPUT : 
		OUTPUT : none
		'''
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None,hCom,"	DEBUG		Instance ThreadRouteComtoDlci.__init()", color=2)
		Thread.__init__(self,name="Route data on COM%s and send to dlci %s"%(hCom.port+1,dlci))
		self.hCom = hCom
		self.dlci = dlci
		if MuxThread == None:
			MuxThread = MuxstaticVariables.Mux0710Thread[hCom]
		self.MuxThread = MuxThread
	
	def run(self):
		'''	
		goal of the method : 
		INPUT : 
		OUTPUT : none
		'''
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None,self.hCom,"	DEBUG		thread ThreadRouteComtoDlci.run()", color=2)
			SafePrint(None,self.hCom,"	DEBUG		@@@thread launched@@@", color=2)
		Serial_In = []
		try:
			while True:
				evtOk = self.hCom.waitRXData()
				if evtOk:
					time.sleep(0.01)
					bufferSize = self.hCom.inWaiting()
					if bufferSize:
						buffer = self.hCom.read(bufferSize)
						dt = datetime.now()
						if buffer:
							Serial_In = []
							for i in range(len(buffer)):
								Serial_In.append(ord(buffer[i]))
						
						if MuxstaticVariables.debugMode:
							SafePrint(dt,self.hCom,"DEBUG (COM%s): Serial In : %s"%(self.hCom.port+1,Serial_In),color=11)
						self.__Send(Serial_In)
		except SystemExit:
			self.hCom.stop()
			raise SystemExit
		except:					
			SafePrintError(None, self.hCom, "Thread %s Error!"%self.getName())
	
	def __Send(self, Serial_In):
		'''	
		goal of the method : 
		INPUT : 
		OUTPUT : none
		'''
		SagMuxSend(self.MuxThread.hCom,UIH,self.dlci,Serial_In,display=MuxstaticVariables.debugMode)

def SagMuxRouteComToDlci(hCom, dlci):
	'''	
	goal of the method : 
	INPUT : 
	OUTPUT : none
	'''
	if VarGlobal.MODE != VarGlobal.DEMO_MODE:
		SafePrint(None, hCom,"Start thread Route COM%s to dlci %s"%(hCom.port+1,dlci),10)
	Thread = ThreadRouteComtoDlci(hCom,dlci)
	#AddThreadInList(Thread)
	if VarGlobal.DEBUG_LEVEL == "DEBUG":
		SafePrint(None,hCom,"	DEBUG		thread ThreadRouteComtoDlci is starting", color=2)
	Thread.start()

class ThreadRouteDlciToCom(Thread):
	def __init__(self,dlci, hCom, MuxThread = None,logData=False):
		'''	
		goal of the method : constructor
		INPUT : 
		OUTPUT : none
		'''
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None,hCom,"	DEBUG		Instance ThreadRouteDlciToCom.__init()", color=2)
		Thread.__init__(self,name="Route Mux frame on dlci %s to COM%s"%(dlci, hCom.port+1))
		self.dlci = dlci
		self.hCom = hCom
		if MuxThread == None:
			MuxThread = MuxstaticVariables.Mux0710Thread[hCom]
		self.MuxThread = MuxThread
		self.logData = logData
	
	def run(self):
		'''	
		goal of the method : 
		INPUT : 
		OUTPUT : none
		'''
		if VarGlobal.DEBUG_LEVEL == "DEBUG":
			SafePrint(None,self.hCom,"	DEBUG		thread ThreadRouteDlciToCom.run()", color=2)
			SafePrint(None,self.hCom,"	DEBUG		@@@thread launched@@@", color=2)
		try:
			event = self.MuxThread.GetEvent(self.dlci)
			
			while True:
				WaitEvent(event)
				Table_Of_Frames = self.MuxThread.ReadTableOfFrame(self.dlci)
				for DecodedFrame in Table_Of_Frames:
					data = str(data2string(DecodedFrame.Info))
					if MuxstaticVariables.debugMode or self.logData:
						SafePrintOnMuxDlg(DecodedFrame,False)
						file = open('Data on dlci %s.txt'%self.dlci, 'a')
						file.write(data)
						file.close()
					self.hCom.write(data)
					
		except SystemExit:
			self.hCom.stop()
			raise SystemExit
		except:					
			SafePrintError(None, self.hCom, "Thread %s Error!"%self.getName())

def SagMuxRouteDlciToCom(dlci,hCom):
	'''	
	goal of the method : 
	INPUT : 
	OUTPUT : none
	'''
	if VarGlobal.MODE != VarGlobal.DEMO_MODE:
			SafePrint(None, hCom,"start thread Route dlci %s to COM%s"%(dlci,hCom.port+1),10)
	Thread = ThreadRouteDlciToCom(dlci,hCom,logData=True)
	#AddThreadInList(Thread)
	if VarGlobal.DEBUG_LEVEL == "DEBUG":
		SafePrint(None,hCom,"	DEBUG		Thread ThreadRouteDlciToCom is starting", color=2)
	Thread.start()

#####################
## Functions could be use by user ##
#####################
def SagMuxRouteComAndDlci(hCom,dlci):
	'''	
	goal of the method : 
	INPUT : 
	OUTPUT : none
	'''
	SagMuxRouteComToDlci(hCom, dlci)
	SagMuxRouteDlciToCom(dlci,hCom)

###########################
## Test open 2 channel in 2 virtual com port ##
###########################
if __name__ == '__main__':
	pass
	"""
	MODULE = SagOpen("COM6", 115200)
	
	#Init(MRM)
	
	# ouverture du mux 07.10
	#AT+CMUX
	SagSend(MODULE, "AT+CMUX=0,0,5,64\r\n")
	resultat = SagWaitLine(MODULE, ["OK"], 5000)
	result = SagTestCmd(resultat.tabLines, ["OK"])
	Sleep(1000)
	SetMaximumFrameSize(64)
	# start autotest to listen Mux Frames
	SagMuxStartThreadWait(MODULE,displayRECV=False)
	
	#################
	## Open Channel 0, 1 & 2  ##
	#################
	FTPdlci  = 1
	DATAdlci = 2
	
	SagMuxOpenDLCI(MODULE,dlci=0)
	SagMuxOpenDLCI(MODULE,dlci=DATAdlci)
	SagMuxOpenDLCI(MODULE,dlci=FTPdlci)
	
	DATACOM = SagOpen("COM61",115200)
	WINCOM = SagOpen("COM63",115200)
	
	SagMuxRouteComAndDlci(DATACOM,DATAdlci)
	SagMuxRouteComAndDlci(WINCOM,FTPdlci)
	"""
	