import sys
import telnetlib
import time,re
import serial,threading
import paramiko
import VarGlobal
from VarGlobal import *
from   threadStop   import Thread,PauseAllThread,ContinueAllThread,GetPauseStatus,StopAllThread
from   datetime import datetime
import fnmatch
import re
import ComModuleAPI
from scp import SCPClient

print_mutex = threading.Lock()


class TARGET():
    
    def __init__(self, ip_addr ="127.0.0.1", user = "root", password = "root"):
        print 'SSH start session'
        self.ssh = paramiko.SSHClient()
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.host=ip_addr
        self.user= user
        self.password=password
        self.ssh.connect(ip_addr, username=user,password= password)

        self.sshBuffer =''

    def sendShellCmd(self,command,printmode="symbol"):
        "goal of the method : this method send Shell command to linux host via ssh"
        "INPUT : command : command need to send to linux"
        "printmode : prin mode type"
        "OUTPUT : None "
        try:
            dt = datetime.now() 
            timeDisplay =  "(%0.2d:%0.2d:%0.2d:%0.3d) Snd"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)
            SafePrintLog(timeDisplay +" IP "+ self.host+" ["+ascii2print(command,printmode)+"]",6)
            self.chan = self.ssh.get_transport().open_session()
            self.chan.exec_command(command)
            self.chan.set_combine_stderr(True)
        except Exception, e:
            print e
            print "----->Problem: Exception comes up when send command !!!"
    
    def sendInput(self,input,printmode="symbol"):
        "goal of the method : this method send Input for application"
        "INPUT : input: Input that we need to send"
        "printmode : prin mode type"
        "OUTPUT : None"
        try:     
            dt = datetime.now() 
            timeDisplay =  "(%0.2d:%0.2d:%0.2d:%0.3d) Input"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)
            SafePrintLog(timeDisplay +" IP "+ self.host+" ["+ascii2print(input,printmode)+"]",6)

            self.chan.send(input+'\n')
        except Exception, e:
            print e
            print "----->Problem: Exception comes up when send input !!!"
            
    def getResp(self,printmode="symbol"):
        "goal of the method : this method collect all response and return it"
        "INPUT : None"
        "OUTPUT : Received data (String) "
        try:     
            key = True
            response=''
            start_time = datetime.now()
            while key:
                diff_time = datetime.now() - start_time
                diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
                
                if self.chan.exit_status_ready():
                    key = False
                else:
                    dt = datetime.now() 
                    timeDisplay =  "(%0.2d:%0.2d:%0.2d:%0.3d) Rcv"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)
                    current_response = self.chan.recv(4096)
                    SafePrintLog(timeDisplay +" IP "+ self.host +" [" + ascii2print(current_response,printmode) +"] @"+str(diff_time_ms)+" ms " ,7)
                    response=response+ current_response
            return response
        except Exception, e:
            print e
            print "----->Problem: Exception comes up when get response !!!"
        
    def getRespOnMatch(self,waitpattern,timeout=60000,log_msg="logmsg", printmode="symbol"):
        "goal of the method : this method collect all response match with waitpattern and return it"
        "INPUT : waitpattern : the matching pattern for the received data"
        "        timeout (ms) : timeout between each received packet"
        "        log_msg : option for log message:"
        "        printmode : prin mode type"
        "OUTPUT : Received data (String) "
        start_time = datetime.now()
        
        flag_matchrsp = False
        flag_matchstring = False
        flag_timeout = False
        flag_wait_until_timeout = False
        flag_printline = False
        LogMsg = ""
        timestamp = ""
        
        #wait to time out 
        if waitpattern == None or waitpattern[0] == "":
            flag_wait_until_timeout = True
            waitpattern = [""]
            SafePrintLog("")
            SafePrintLog("Wait responses in %s ms" % str(timeout))
            SafePrintLog("")
        displaybuffer = ""
        displaypointer = 0
        while 1:
            # Read data from SSH Buffer
            if self.chan.recv_ready():
                self.sshBuffer += self.chan.recv(32768)
            # Loop for each character
            for (index,each_char) in enumerate(self.sshBuffer) :
                displaybuffer = self.sshBuffer[displaypointer:index+1]
                
                # display if matched with a line syntax
                displaybuffer = self.sshBuffer[displaypointer:index+1]
                line_syntax1 = "*\r\n*\r\n"
                line_syntax2 = "+*\r\n"
                line_syntax3 = "\r\n> "
                line_syntax4 = "*\n"
               
                if fnmatch.fnmatchcase(displaybuffer, line_syntax1) or \
                    fnmatch.fnmatchcase(displaybuffer, line_syntax2) or \
                    fnmatch.fnmatchcase(displaybuffer, line_syntax3) or \
                    fnmatch.fnmatchcase(displaybuffer, line_syntax4) :
                    # display timestamp
                    if VarGlobal.SndRcvTimestamp:
                        timestamp = TimeDisplay() + " "
                    # display data
                    received_data = ascii2print(displaybuffer,printmode)
                    LogMsg = timestamp+"Rcv IP "+self.host+" ["+received_data+"] "
                    displaypointer = index+1
                    flag_printline = True
            
                # match received response with waitpattern
                for (each_elem) in waitpattern:
                    receivedResp = self.sshBuffer[:index+1]
                    expectedResp = each_elem
                    if fnmatch.fnmatchcase(receivedResp, expectedResp):
                        flag_matchstring = True
                        break
            
                if flag_matchstring:
                    # display the remaining matched response when waitpettern is found
                    displaybuffer = self.sshBuffer[displaypointer:index+1]
                    if len(displaybuffer)>0:
                        # display timestamp
                        if VarGlobal.SndRcvTimestamp:
                            timestamp = TimeDisplay() + " "
                        # display data
                        received_data = ascii2print(displaybuffer,printmode)
                        #print "Rcv COM", com_port_name, "["+received_data+"]",
                        LogMsg = timestamp+"Rcv IP "+self.host+" ["+received_data+"] "
                        pass
                     # display time spent in receive
                    if VarGlobal.RcvTimespent:
                        diff_time = datetime.now() - start_time
                        diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
                        LogMsg += " <"+str(timeout)+" @"+str(diff_time_ms)+" ms "

                    flag_printline = True

                    # clear matched resposne in SSH Buffer
                    self.sshBuffer = self.sshBuffer[index+1:]
                    flag_matchrsp = True
                    
                # print linebreak for EOL
                if flag_printline:
                    flag_printline = False
                    SafePrintLog(LogMsg,7)

                # break for Match response
                if flag_matchrsp:
                    break
            # Count timeout
            diff_time = datetime.now() - start_time
            diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
            if diff_time_ms > timeout:
                if log_msg == "debug":
                    LogMsg = "Timeout: "+str(diff_time)+" diff_time_ms: "+str(diff_time_ms)
                    SafePrintLog(LogMsg,7)
                # display the remaining response when timeout
                displaybuffer = self.sshBuffer[displaypointer:]
                if len(displaybuffer)>0:
                    # display timestamp
                    if VarGlobal.SndRcvTimestamp:
                        timestamp = TimeDisplay() + " "
                    # display data
                    received_data = ascii2print(receivedResp,printmode)
                    LogMsg = "Rcv IP "+self.host+" ["+received_data+"]"
                    SafePrintLog(LogMsg,7)
                    pass

                # clear all resposne in SSH Buffer
                VarGlobal.myColor = VarGlobal.colorLsit[8]
                receivedResp = self.sshBuffer

                if flag_wait_until_timeout != True:
                    if log_msg == "logmsg" or log_msg == "debug":
                        if len(receivedResp) > 0:
                            
                            LogMsg = "\nNo Match! "+"@ IP "+ self.host+" <"+str(timeout)+" ms\n"
                            SafePrintLog(LogMsg,7)
                        if len(receivedResp) == 0:
                            LogMsg = "\nNo Response! "+"@IP "+self.host+ " <"+str(timeout)+" ms\n"
                            SafePrintLog(LogMsg,7)
                self.sshBuffer = ""
                flag_timeout = True
            
            if flag_matchrsp:
                break
            if flag_timeout:
                break

        return receivedResp
    
    def getSCPFile(self, remote_path,local_path, printmode="symbol"):
        "goal of the method : this method collect response based on regular expression, return response as long as it is matched"
        "INPUT : remote_path: Path of file in remote server"
        "        local_path  : Path of file in local server" 
        "        print mode:"
        "OUTPUT : None"
    
        try:     
            dt = datetime.now() 
            timeDisplay =  "(%0.2d:%0.2d:%0.2d:%0.3d) Get File"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)
            SafePrintLog(timeDisplay +" IP "+ self.host+" ["+ascii2print('from '+remote_path +' to '+ local_path,printmode)+"]",6)

            scp = SCPClient(self.ssh.get_transport())
            scp.get(remote_path,local_path)
        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            print "----->Problem: Exception comes up when get response !!!"

    def getRespExp(self, regular_expression,timeout=60000,log_msg="logmsg", printmode="symbol"):
        "goal of the method : this method collect response based on regular expression, return response as long as it is matched"
        "INPUT : regular_expression : the matching pattern for the received data"
        "        timeout (ms) : timeout between each received packet"
        "        log_msg : option for log message"
        "        print mode:"
        "OUTPUT : [match_result,Received data (String)]"
    
        try:     
            key = True
            flag_matchstring= False
            receivedResp=''
            start_time = datetime.now()
            diff_time = datetime.now() - start_time
            diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
            
            while key and diff_time_ms < timeout:
                if self.chan.exit_status_ready():
                    key = False
                else:
                    dt = datetime.now() 
                    timeDisplay =  "(%0.2d:%0.2d:%0.2d:%0.3d) Rcv"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)
                    current_response = self.chan.recv(4096)

                    SafePrintLog(timeDisplay + " IP "+ self.host + " ["+ ascii2print(current_response,printmode) +"] <"+str(timeout)+" @"+str(diff_time_ms)+" ms " ,7)
                    
                    receivedResp =receivedResp + current_response
                    
                    result = re.search(regular_expression, receivedResp)
                    if result:
                       flag_matchstring = True
                       break
                diff_time = datetime.now() - start_time
                diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
  
            if flag_matchstring: 
                return[True,receivedResp]
            else:
                SafePrintLog("No Match!  <%s ms"%timeout,8)
                SafePrintLog("Expected Response: %s"%regular_expression,7)
                SafePrintLog("Received Response: %s"%receivedResp,7)
                
                VarGlobal.statOfItem="NOK"
                return [False,receivedResp]
        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            print "----->Problem: Exception comes up when get response !!!"

    def waitnMatchResp(self, waitpattern,timeout=60000,log_msg="logmsg", printmode="symbol"):
        "goal of the method : Collect response based on pattern and return match result"
        "INPUT : waitpattern : the matching pattern for the received data"
        "        timeout (ms) : timeout between each received packet"
        "        log_msg : option for log message"
        "OUTPUT : Received data (String)"
    
        try:     
            flag_matchstring = False
            matched = False
            for (each_elem) in waitpattern:
                receivedResp = self.getRespOnMatch(waitpattern,timeout,log_msg,printmode)
                expectedResp = each_elem
                if fnmatch.fnmatchcase(receivedResp, expectedResp):
                    flag_matchstring = True
                    matched = True
                    break

            if matched == 0 :
                if log_msg == "logmsg" or log_msg == "debug":
                    if len(waitpattern)==1:
                        SafePrintLog("")
                        SafePrintLog("Expected Response: %s" % ascii2print(expectedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                        SafePrintLog("Received Response: %s" % ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                        SafePrintLog("")
                    if len(waitpattern)>1:
                        SafePrintLog("")
                        SafePrintLog("Expected Response: %s" % ascii2print(waitpattern[0],printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                        for (i,each_elem) in enumerate(waitpattern):
                            if i == 0:
                                pass
                            if i >0:
                                SafePrintLog("Expected Response: %s" % ascii2print(each_elem,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                        SafePrintLog("Received Response: %s" % ascii2print(receivedResp,printmode).replace("<CR>","\\r").replace("<LF>","\\n"), 8)
                        SafePrintLog("")
                VarGlobal.statOfItem="NOK"
        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            print "----->Problem: Exception comes up when get response !!!"

    def close(self):
        try:
            self.ssh.close()
            print "\nConnection to %s closed." % self.host
        except Exception, e:
            print e            
            print "----->Problem: Can not close ssh session !!!"
 
    def __del__(self):
        self.ssh.close()
        
def SafePrintLog( Msg, color = 8):
        "goal of the method : This method displays information, using a mutex"
        "INPUT : "
        "OUTPUT : "

        print_mutex.acquire()  
        VarGlobal.myColor = VarGlobal.colorLsit[color]
        print str(Msg)
        VarGlobal.myColor = VarGlobal.colorLsit[8]
        print_mutex.release()

def ascii2print(inputstring, mode="symbol"):
    if mode=="symbol":
        # calculate value to hexstring >> too slow , don't use these code
        if 0:
            outputstring = ""
            for eachchar in inputstring:
                if ord(eachchar)<32:
                    outputstring += VarGlobal.ascii_symbol[eachchar]
                elif ord(eachchar)==127:
                    outputstring += VarGlobal.ascii_symbol[eachchar]
                elif ord(eachchar)>127:
                    outputstring += "<"+"0x{:02X}".format(ord(eachchar))+">"
                else:
                    outputstring += eachchar

        # direct convert value to string by Dictionary >> very fast
        if 1:
            string_raw = inputstring
            # convert raw data to <symbol> for \x00 - \x1F
            #                     <0x??>   for \x80 - \xFF
            for key, value in VarGlobal.ascii_symbol.iteritems():
                string_raw = string_raw.replace(key,value)
            outputstring = string_raw


    if mode=="hexstring":
        # calculate value to hexstring >> too slow , don't use these code
        if 0:
            outputstring = ""
            for eachchar in inputstring:
                outputstring += "<"+"0x{:02X}".format(ord(eachchar))+">"
                
        # direct convert value to string by Dictionary >> very fast
        if 1:
            string_raw = inputstring
            for key, value in VarGlobal.ascii2hexstring_printable_tempsymbol.iteritems():
                string_raw = string_raw.replace(key,value)
            for key, value in VarGlobal.ascii2hexstring_printable_revert.iteritems():
                string_raw = string_raw.replace(key,value)
            for key, value in VarGlobal.ascii2hexstring_symbol.iteritems():
                string_raw = string_raw.replace(key,value)
            for key, value in VarGlobal.ascii2hexstring_extended.iteritems():
                string_raw = string_raw.replace(key,value)
            outputstring = string_raw


    if mode=="raw":
        string_raw = inputstring
        # convert <symbol> to raw data
        for key, value in VarGlobal.ascii_symbol.iteritems():
            string_raw = string_raw.replace(value,key)
        # convert <0x??> to raw data
        for key, value in VarGlobal.ascii2hexstring_printable.iteritems():
            string_raw = string_raw.replace(value,key)
        for key, value in VarGlobal.ascii2hexstring_symbol.iteritems():
            string_raw = string_raw.replace(value,key)
        for key, value in VarGlobal.ascii2hexstring_extended.iteritems():
            string_raw = string_raw.replace(value,key)
        outputstring = string_raw
                
    return outputstring

def TimeDisplay(dt = None):
        "Display the time ; if dt is empty retrun actual date time under format, otherless return dt under format"
        "INPUT  : (optionnal) dt : date Time"
        "OUTPUT : date Time under format hh:mm:ss:???"
        if dt == None:
                dt = datetime.now() 
        return "(%0.2d:%0.2d:%0.2d:%0.3d)"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)

if __name__ == "__main__":
    myTarget = TARGET("10.22.51.192")
    print 'Start SSH Session'
