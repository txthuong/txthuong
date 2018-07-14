#!/bin/env python
# _*_ coding: utf-8 _*_
##########################################################################
# @Description
#  This module supports methods to control/monitor an object as a server,
#  a switch, or a router via telnet.   
#
##########################################################################
# @History
# Date              Who                 Version                 Modification
# 2017-05-03        lehuy               1.0                     Creation and modification 
# 2017-05-11        lehuy               1.1                     Enhance to cover change CIPHER when start HTTTPS  
#
##########################################################################

import sys
import telnetlib
import time,re
import serial
import VarGlobal

class TelnetUtil():    
    def __init__(self, default_port="23"):
        self.default_port = default_port
        
    def open_telnet_session(self, host, port, usr, pwd, os="window"):
        """
        Goal of the method: Open telnet session
        Input:  
              host: specifies a host to contact over the network
              port: specifies a port number to contact
              usr: user name to login 
              pwd: password to login
              os:  operation system (linux,window)
        Output: dest (a telnet session)
        """
        self.os = os
        try:
            print ("Opening a telnet session to %s:%s..." % (str(host), str(port) ))
            if (os == "window"):
                dest = telnetlib.Telnet(host, port)
                print dest.read_until("login: ", 60)
                dest.write(usr + '\r\n')
                print dest.read_until("password: ", 60)
                dest.write(pwd + '\r\n')
                print dest.read_until('>', 60)
            else:
                dest = telnetlib.Telnet(host, port)
                print dest.read_until("User name: ", 60)
                dest.write(usr + '\r\n')
                print dest.read_until("Password: ", 60)
                dest.write(pwd + '\r\n')
                print dest.read_until('$', 60)
         
            print ("Telnet to %s:%s successfully." % (str(host), str(port) ))
            return dest
            
        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            print "--->Problem: Cannot establish a telnet session to this destination. Please re-check IP, UserName and Password!"

    def start_https(self, dest, httpsd_dir, https_port, cipher=""):
        """
        Goal of the method: start https service on this server
        Input:  
              dest: a opening telnet session
              httpsd_dir: path contains httpsd.py and server.pem
              cipher: specific cipher user wants to enable 
              https_port: specify HTTPS port
        Output: return PID 
        """
        try:
            pid=-1
            # Check host name of server
            print re.findall(r'(.+)',self.send_cmd(dest,'hostname'))[1]
            
            # Start HTTPS server with specific port, specific cipher
            if cipher=="":
                print ("Starting HTTPS service with specific port: %s ..." % str(https_port))
                start_cmd = 'cmd /c start python ' + httpsd_dir + '\httpsd.py -x ' + httpsd_dir + '\server.pem -p ' + str(https_port)
                               
            else:
                print ("Starting HTTPS service with specific port: %s, and cipher: %s ..." % (str(https_port), cipher))
                start_cmd = 'cmd /c start python ' + httpsd_dir + '\httpsd.py -x ' + httpsd_dir + '\server.pem -c ' + cipher + ' -p ' + str(https_port)
                                    
            self.send_cmd(dest, start_cmd)
            time.sleep(5)         
            # Check status after starting
            print "Checking https service status after starting..."
            temp = self.send_cmd(dest,'netstat -ano', time_out=120)
            print temp
            if re.findall('(TCP.+?\d+.\d+.\d+.\d+:%d)' % https_port,temp):
                pid=re.findall(r'TCP.+?\d+.\d+.\d+.\d+:%d.+?\d+.\d+.\d+.\d+:\d+.+?(\d+)\r\n' % https_port,temp)[0]
                if pid!=-1:
                    print 'HTTPS service is started with pid %d' % int(pid)
                    return pid
                else:
                    self.close_telnet_session(dest)
                    VarGlobal.statOfItem="NOK"
                    raise Exception("---> Problem: Cannot start HTTPS service on this server!")
            else:
                self.close_telnet_session(dest)
                VarGlobal.statOfItem="NOK"
                raise Exception("---> Problem: Cannot start HTTPS service on this server!")
   
        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            print "---> Problem: Cannot start HTTPS service on this server!"
    
    def stop_https(self, dest, https_port):
        """
        Goal of the method: kill PID using specific port
        Input:  
              dest: a opening telnet session
              https_port: specify a port that user wants to kill 
        Output: 
        """
        try:
            pid = 1
            while pid != -1:
                pid = -1                
                # Check status specific port
                print ("Checking status port: %s ..." % str(https_port))
                temp = self.send_cmd(dest,'netstat -ano', time_out=120)
                print temp
                if re.findall('(TCP.+?\d+.\d+.\d+.\d+:%d)' % https_port,temp):
                    pid=re.findall(r'TCP.+?\d+.\d+.\d+.\d+:%d.+?\d+.\d+.\d+.\d+:\d+.+?(\d+)\r\n' % https_port,temp)[0]
                    print ("Killing PID: %d" % int(pid))
                    if re.findall('SUCCESS',self.send_cmd(dest,'taskkill /PID ' + str(pid) + ' /F', time_out=120)):
                        print ("PID %d is killed successfully." % int(pid))
                    else:
                        self.close_telnet_session(dest)
                        VarGlobal.statOfItem="NOK"
                        raise Exception("---> Problem: Cannot kill this process!")
                else:
                    print ("There is no process using this port: %s" % https_port)
                    break
            print ("All processes using this port are killed successfully")
            
        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            print "---> Problem: Cannot kill process using this port!"

    def send_cmd(self, dest, cmd, time_out=60):
        """
        Goal of the method: send command via telnet
        Input:  
            dest: a opening telnet session
            cmd : command to send
            time_out: duration for waiting response, the default value is 60s
        Output: response for command until the prompt appears 
        """
        try:
            print ("Sending command: %s" %cmd)
            dest.write(cmd + '\r\n')
            if (self.os == "window"):
                return dest.read_until('>', time_out)
            else:
                return dest.read_until('$', time_out)
        
        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            print "---> Problem: Cannot send a command to this destination!"

    def close_telnet_session(self,dest):
        """
        Goal of the method: close telnet session id
        Input:  
             dest: a opening telnet session
        Output: 
        """
        try:
            dest.write('exit\r\n')
            print ("The telnet session is closed successfully.")  

        except Exception, e:
            VarGlobal.statOfItem="NOK"
            print e
            print "---> Problem: Cannot close this telnet session!"
            
if __name__ == "__main__":

    myTelnet = TelnetUtil()
       
    myTelnet.open_telnet_session(host, port, usr, pwd, os)
    
    myTelnet.send_cmd(dest, cmd, time_out)
    
    myTelnet.close_telnet_session(dest)
    
    myTelnet.start_https(dest, httpsd_dir, cipher, https_port)
    
    myTelnet.stop_https(dest, https_port)
    