import sys
import time,re
from   datetime import datetime
import subprocess
import threading
import ComModuleAPI
import VarGlobal
import psutil
from VarGlobal import *

print_mutex = threading.Lock()

def kill_SubProcess(p):
    try:
        if p.poll() is  None:
            subprocess.Popen('taskkill /F /T /PID %s' %p.pid)
            
    except Exception, e:
        print e
        print "----->Problem: Exception comes up when kill process !!!"


class ADB():
   
    def __init__(self, id = ''):
        self.id= id

    def sendShellCmd(self,command,timeout=10):
        "goal of the method : Send a command to "
        "INPUT : command : Command we need to send"
        "        timeout : timeout to execute command"
        "OUTPUT : None "
        try:
            start_time = datetime.now()
            dt = datetime.now() 
            timeDisplay =  "(%0.2d:%0.2d:%0.2d:%0.3d) Snd"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)
            SafePrintLog(timeDisplay +" ADB "+ self.id+" ["+ 'adb %s' % command +"]",6)
            
            p = subprocess.Popen('adb %s'%command,shell=True,stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            t = threading.Timer(timeout, kill_SubProcess, args=(p))
            t.start()            
            #p.wait()            

            output = p.communicate()[0]                     

            # Rtang: add something to cancel the timer
            try:
                if t is not None:
                    if t.isAlive():
                        print "\nTerminate the monitoring process"
                        t.cancel()
                        print "%s : Timer is cancelled" % datetime.now().strftime("%y/%m/%d %H:%M:%S")
                    else:
                        print "\nMonitoring process expired, script is killed"
                else:
                    print "Timer expired ???"
            except Exception,e:
                print e
                traceback.print_exc()
                print "---->Problem when terminating mornitor process !!!"
            
            timeDisplay =  "(%0.2d:%0.2d:%0.2d:%0.3d) Rcv"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)
            diff_time = datetime.now() - start_time
            diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
            for each_line in output.split('\n'):
                SafePrintLog(timeDisplay + " ADB "+ self.id + " ["+ each_line.replace("\r","<CR>").replace("\n","<CR>") +"]"+" @"+str(diff_time_ms)+" ms " ,7)
            
            return output           
            
        except Exception, e:
            print e
            print "----->Problem: Exception comes up when send command !!!"
            return "\r\nERROR\r\n"


def SafePrintLog( Msg, color = 8):
        "goal of the method : This method displays information, using a mutex"
        "INPUT : "
        "OUTPUT : "

        print_mutex.acquire()  
        VarGlobal.myColor = VarGlobal.colorLsit[color]
        print str(Msg)
        VarGlobal.myColor = VarGlobal.colorLsit[8]
        print_mutex.release()

def TimeDisplay(dt = None):
        "Display the time ; if dt is empty retrun actual date time under format, otherless return dt under format"
        "INPUT  : (optionnal) dt : date Time"
        "OUTPUT : date Time under format hh:mm:ss:???"
        if dt == None:
                dt = datetime.now() 
        return "(%0.2d:%0.2d:%0.2d:%0.3d)"%(dt.hour, dt.minute, dt.second, dt.microsecond/1000)
        
if __name__ == "__main__":
    print 'Start ADB'

    myAdb = ADB()
    myAdb.sendShellCmd("adb -s 3261d4 killall -9 QCMAP_ConnectionManager")

