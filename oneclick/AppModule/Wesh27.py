#-------------------------------------------------------------------------------
# Name:        Wesh.py
# Purpose:     This module acts as a command line tool for invoking commands on
#              AMS server 4.x
#              When a command is received, it sends a request to a webservice.
#              Then it listens and parses the response from the service,
#              and send back an intelligible answer .
#
# Author:      Infosys Tools
#
#
# Version      1.4.3
#
# Created:     20/01/2013
#-------------------------------------------------------------------------------

from __future__ import with_statement
import urllib2, urllib
import urllib2, urllib, urlparse
import re
import json
import sys
import fileinput
import ast
import xml.etree.ElementTree as ET
from io import open
from time import sleep


# Variable to track access token for a session
g_access_token = u''
g_server = u''
g_print = True

# API returns
API_SUCCESS = 0
AUTH_FAILED = -3 # Authenication Failure
API_FAILED = -2  # Web API failure / wrong parameter
INVALID = u'Invalid'

def createConfigFile():
    file = open(u'config.txt', u'w')
    file.close()

def writeConfigData(expr, data):
    file = open(u'config.txt', u'a')
    file.write(expr+u'='+data+u'\n')
    file.close()

def readConfigData(expr):
    try:
        f = open(u'config.txt')
        for line in f:
            if expr in line:
                return (line[len(expr+u'='):len(line)-1])
        return u''
    except:
        return u''

def setPrintValue(val):
    global g_print
    g_print = val


# Parser function
# The algorithm assumes that the input string will
# contain a list of systems identified between root
# level braces'{' & '}'
# For eg. {system1}, {system2}
def UIDSystemParser(string):
    openBrace = 0
    uid = u''
    index = 0
    # Preliminary string update
    # Trim the input string of the extra opening '{'
    if (string[:index+len(u'{"items":')] == u'{"items":'):
        string = string[index+len(u'{"items":'):]
    while index < len(string):
       if string[index] == u'{':
            openBrace = openBrace+1
       if string[index] == u'}':
            openBrace = openBrace-1
       if (openBrace == 1) & (string[index:index+3] == u'uid'):
            # Extraxt uid
            uid = string[index+6:]
            uid = uid[:uid.find(u'",')]
            return uid
       if uid == u'':
            index = index+1
       pass

#Parser Function
#Input: system, imei
#Output: system UID with matching imei
def UIDParser(string, imei):
    openBrace = 0
    uid = u''
    index = 0
    if(imei != u"null"):
        imei = u'"'+imei+u'"'
    while index < len(string):
       if string[index] == u'{':
            openBrace = openBrace+1
       if string[index] == u'}':
            openBrace = openBrace-1
       if (openBrace == 2) and string[index] == u'{':
            startindex = index
       if (string[index:index+4] == u'imei'):
            # Extraxt uid
            tmpimei = string[index+len(u'imei":'):]
            tmpimei = tmpimei[:tmpimei.find(u',')]
            # If imei match is found, get system uid
            if(imei == tmpimei):
                # Loop through the remaining string until
                # ending "}" is found for the system
                while(1):
                    index=index+1
                    if string[index] == u'{':
                        openBrace = openBrace+1
                    if string[index] == u'}':
                        openBrace = openBrace-1
                    if string[index] == u'}' and openBrace == 1:
                        response = UIDSystemParser(string[startindex:index])
                        return response
       index = index+1

# UID Parser function
# Input: system information string
# Output: UID
# This function extracts the sub-system UIDs from the system
def SystemParamParser(string,parameter):
    substring = u''
    result = u''
    uid = u''
    paramindex = 0
    index = 0
    final = u''
    while paramindex < 1:
       if string[index:index+len(parameter)] == parameter:
           substring = string[index-1:len(string)]
           if parameter == u'uid':
               result = u'"uid": '+UIDSystemParser(string)
           elif parameter == u'activityState':
               substring =substring[:substring.find(u',"')]
               result = substring
           elif parameter == u'gateway':
               substring =substring[:2+substring.find(u'"}')]
               result = substring
           elif (parameter == u'applications') or (parameter == u'subscriptions'):
            # Infosys Changes begin for Tracker 4516
               idx = 0
               appstring = []

               if parameter == u'subscriptions':
                # Check for NULL list
                 if (substring.find(u'subscriptions":[]') != -1):
                    return appstring
                 print substring[len(u'"subscriptions":')+1:1+substring.find(u'}')]
                 appstring.append(substring[len(u'"subscriptions":')+1:1+substring.find(u'}')])
                 substring = substring[len(u'"subscriptions":') + len(appstring[idx]) + 1:]

               if parameter == u'applications':
                # Check for NULL list
                if (substring.find(u'applications":[]') != -1):
                    return appstring
                print substring[len(u'"applications":')+1:1+substring.find(u'}')]
                appstring.append(substring[len(u'"applications":')+1:1+substring.find(u'}')])
                substring = substring[len(u'"applications":') + len(appstring[idx]) + 1:]

               while (substring[0] != u']'):
                # Multiple applications
                    idx = idx + 1
                    appstring.append(substring[1:2+substring.find(u'"}')])
                    print substring[1:2+substring.find(u'"}')]
                    substring = substring[len(appstring[idx]) + 1:]
               result = appstring
       index= index + 1
       if index >= len(string):
        if g_print == True:
            print u'Invalid parameter '+parameter
        paramindex = 1
        index = 0
       if result != u'':
            paramindex = 1
            return result
       pass


# 2.	Log into AMS server
# Authentication function
# Syntax: init <server> <login> <password> <client_id> <secret_key>
# Reponse: OK
# def Process_init(command):
def Process_init(server_c,login_c,password_c,client_id_c,secret_key_c):
     global g_access_token
     global g_server
	# Extract parameters
     g_server = server_c
     login = login_c
     password = password_c
     client_id = client_id_c
     secret_key = secret_key_c
     g_access_token = u''
     # Create config.txt to save Server and Access_Token
     createConfigFile()
     writeConfigData(u"Server", g_server)
     #print ("Server: ",g_server, "Login: ", login,"Password: ", password,
     #"Client ID: ", client_id, "Secret Key: ", secret_key)
     if g_print == True:
        print u"Authenticating..."
     request = g_server+u"/api/oauth/token?company=d7378fc019c649bf8131afe3d3eb3663&grant_type=password&username="+login+u"&password="+password+u"&client_id="+client_id+u"&client_secret="+secret_key
     print request
     try:
            #with urllib2.urlopen(request) as url:
            url = urllib2.urlopen(request)
            resp = url.read()
            s = unicode(resp, encoding=u'utf8')
            #Response Received
            try:
           	    # set access token to use in future connexions
                g_access_token_find = s.find(u'access_token')
                if g_access_token_find != -1:
                    g_access_token = s[s.find(u'access_token')+len(u'"access_token":'):s.find(u'","token_type"')]
                    if g_print == True:
                        print u"Access Token= "+g_access_token
                    writeConfigData(u"Access_Token", g_access_token)
                    if g_print == True:
                        print u"OK"
            except AttributeError:
                g_access_token = u'' # apply your error handling
     except:
        if g_print == True:
            print u"AUTHENTICATION FAILED. Please retry."
     # else:
     # print ("Incorrect Command: init <server> <login> <password> <client_id> <secret_key>")

     if g_access_token == u'':
          if g_print == True:
            print u"Invalid AUTHENTICATION API argument. Please retry."
          return (API_FAILED, INVALID)
     else:
        return (API_SUCCESS, g_access_token)

# 3.	Disconnect from AMS server
# WESH logout function
# Syntax: logout
# Reponse: OK
def Process_logout():
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)
     request = g_server+u'/api/oauth/expire?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token
     try:
        #with urllib2.urlopen(request) as url:
        url = urllib2.urlopen(request)
        resp = url.read()
        s = unicode(resp, encoding=u'utf8')
        #Response Received
        if g_print == True:
            print s
        g_access_token = u''
     except:
        if g_print == True:
            print u"LOGOUT FAILED. Please retry."
        return (API_FAILED, INVALID)
     return (API_SUCCESS, True)

# 5.	Find Device
# Syntax: findDevice IMEI
# Reponse: UID
def Process_findDevice(IMEI):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)
     #request = g_server+u'/api/v1/systems?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token
     request = g_server+u'/api/v1/systems?company=d7378fc019c649bf8131afe3d3eb3663&fields=uid&access_token=' + g_access_token + '&gateway=imei:' + IMEI
     #request = u'https://na.airvantage.net/api/v1/systems?access_token='+g_access_token
     
     try:
        #with urllib2.urlopen(request) as url:
        print request
        url = urllib2.urlopen(request)       
        
        resp = url.read()        
        s = unicode(resp, encoding=u'utf8')
        respjson = json.loads(s)
        
        #Response Received
        #systemuid =UIDParser(s,IMEI)
        systemuid = respjson['items'][0]['uid']
        if g_print == True:
            print u"System UID= "+systemuid
            print u"OK"
        return (API_SUCCESS, systemuid)
     except:
        if g_print == True:
            print u"REQUEST FAILED! Please try again"
        return (API_FAILED, INVALID)


# 6.	Send SMS notification
# Syntax: sendsms <Uids>
# Reponse: Operation ID
def Process_PostSMSWakeup(uids):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"FAILURE! Please issue Init command"
        return (AUTH_FAILED, INVALID)
     url = g_server+u'/api/v1/operations/systems/wakeup?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token
     #Infosys Changes begin for Tracker 4559
     json_dict = {    u"action"  : u'OPENAT_IDS_CONNECT',
         u"systems" : { u"uids" : uids}
     }
     #Infosys Changes end for Tracker 4559
     json_data = json.dumps(json_dict)

     # convert str to bytes (ensure encoding is OK)
     post_data = json_data.encode(u'utf-8')

     # we should also say the JSON content type header
     headers = { u'Content-Type' : u'application/json' }

     # now do the request for a url
     req = urllib2.Request(url, post_data, headers)

     # send the request
     try:
         res = urllib2.urlopen(req)
         the_page = res.read()
         text = the_page.decode(u"utf8")
         response = text[len(u'{operation": "'):len(text)-2]
         if g_print == True:
            print u'Wakeup Operation UID : ' +response #show the page source, to see I have a response
            print u"OK"
         return ( API_SUCCESS, response)
     except urllib2.HTTPError, e:
        if g_print == True:
            print e.read()
            print u"FAILURE"
        return (API_FAILED, INVALID)

# 7.	Read System details
# Syntax: ReadSystemDetails <UID> <Parameter>
# Reponse: Dictionary
def Process_ReadSystemDetails(UID,parameter):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)
     request = g_server+u'/api/v1/systems?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token+u'&uid='+UID
     try:
         with urllib2.urlopen(request) as url:
            resp = url.read()
            system = unicode(resp, encoding=u'utf8')
            FinalDict = {}
            #Response Received
            result = SystemParamParser(system,parameter)
            length = len(parameter)

            if parameter == u"gateway":
                TempDict = result[length+3:len(result)]     # will take the value of parameter
                ResultDict= TempDict.replace(u"null",u'"null"',6)
            if parameter == u"activityState":
                ResultDict = u'{'+result+u'}'
            if parameter == u"uid":
                TempDict = result[length+4:len(result)]    # will take the value of parameter
                ResultDict =u'{"'+parameter+u'":"'+TempDict+u'"}'
            # Infosys Changes begin for Tracker 4516
            # For 'subscriptions' & 'applications' return type is an
            # array of strings
            if parameter == u"applications" or parameter == u"subscriptions":
                TempDictList = []
                ResultDictList = []
                FinalDictList = []
                idx = 0
                print len(result)
                if (len(result) == 0):
                    return (API_SUCCESS, FinalDictList)
                for idx in xrange(0, len(result)):
                    TempDictList.append((result[idx])[:len(result[idx])])    # will take the value of parameter
                    ResultDictList.append(TempDictList[idx].replace(u"null",u'"null"',6))
                    FinalDictList.append(ast.literal_eval(ResultDictList[idx]))      # Convert the string to dictionary
                    if g_print == True:
                        print u'Parameter Values: '+ResultDictList[idx] #show the page source, to see I have a response
                return (API_SUCCESS, FinalDictList)
            # Infosys Changes end for Tracker 4516

            FinalDict = ast.literal_eval(ResultDict)      # Convert the string to dictionary
            if g_print == True:
                print u'Parameter Values: '+result #show the page source, to see I have a response
                print u"OK"
            return (API_SUCCESS, FinalDict)                                #Return dictionary
     except:
       if g_print == True:
          print u"REQUEST FAILED! Please try again"
       return (API_FAILED, INVALID)

# 8.	Get Tree node value
# Syntax treenodedata <uid> <DataParams>
# Response Dictionary
def Process_TreeNodeValue(uid, ids):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")

     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)

     # Extract parameters
     if g_print == True:
        print u"Fetching tree node value..."
     request = g_server+u"/api/v1/systems/"+uid+u"/data?company=d7378fc019c649bf8131afe3d3eb3663&access_token="+g_access_token+u"&ids="
     for item in ids:
        request = request+item+u","
     request = request[:len(request)-1]
     try:
            #with urllib2.urlopen(request) as url:
        url = urllib2.urlopen(request)
        resp = url.read()
        print resp
        Datavalue = unicode(resp, encoding=u'utf8')
        FinalDict = {}                                          # Declaring a Dictionary
        DatavalueDict = ast.literal_eval(Datavalue)      #Convert the Datavalue to dictionary
        if g_print == True:
            print u"Data Values= "+Datavalue
            print u'OK'
        for items in ids:
            DatavalueSub = DatavalueDict[items]         # Get the value of items
            stringVal = unicode(DatavalueSub)[1:-1]                 # remove the extra braces
            DatavalueSubDict = ast.literal_eval(stringVal)      # Again convert into dictinary
            Value = DatavalueSubDict[u'value']           # Get the value of "value" and store in value variable
            FinalDict[items]=Value                              # Form a  dictionary with items and value

        return (API_SUCCESS, FinalDict)                                        # return dictionary
                #Response Received
     except:
        if g_print == True:
            print u"REQUEST FAILED. Please retry."
        return (API_FAILED, INVALID)

# 9. Create Discovery Job
def Process_DiscoveryJob(appuid, sysuid, datalist, timeout=u'', wakeup=u''):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")

     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)

	# Extract parameters
     json_dict = {
     u"timeout" : timeout,
     u"applicationUid" : appuid,
     u"systems" : {
    	  u"uids" : [sysuid]
    },
    u"data" : datalist
    }

     url = g_server+u"/api/v1/operations/systems/data/retrieve?company=d7378fc019c649bf8131afe3d3eb3663&access_token="+g_access_token

     json_data = json.dumps(json_dict)

    # convert str to bytes (ensure encoding is OK)
     post_data = json_data.encode(u'utf-8')

    # we should also say the JSON content type header
     headers = { u'Content-Type' : u'application/json' }

# now do the request for a url
     req = urllib2.Request(url, post_data, headers)

# send the request
     try:
         res = urllib2.urlopen(req)
         the_page = res.read()
         text = the_page.decode(u"utf8")
         if g_print == True:
            print text #show the page source, to see I have a response
         response = text[len(u'{operation": "'):len(text)-2]
         if g_print == True:
            print u'Discover Job UID: '+response #show the page source, to see I have a response
         if (wakeup == u'true'):
            Process_PostSMSWakeup([sysuid])
         if g_print == True:
            print u"OK"
         return ( API_SUCCESS, response)
     except urllib2.HTTPError, e:
        if g_print == True:
            print e.read()
        return (API_FAILED, INVALID)


#  10.	Write Tree node value
def Process_WriteTreeNodeValue(appuid, sysuid, datalist, timeout=u'', wakeup=u''):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")

     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)

     setting_dict = []
     k = 0
     
     if len(datalist)%2 != 0:
        if g_print == True:
            print u'Improper data!'
        return (API_FAILED, INVALID)

     while (k < len(datalist)):
        datadict = {
        u"key":    datalist[k],
        u"value":  datalist[k+1],
        }
        k = k+2
        setting_dict.append(datadict)


     json_dict = {u"timeout" : timeout,
     u"applicationUid" : appuid,
       u"systems" : {
       u"uids" : [sysuid]
    }}
     json_dict[u"settings"] = setting_dict
     print 
     print json_dict
     print 

     url = g_server+u"/api/v1/operations/systems/settings?company=d7378fc019c649bf8131afe3d3eb3663&access_token="+g_access_token

     json_data = json.dumps(json_dict)

    # convert str to bytes (ensure encoding is OK)
     post_data = json_data.encode(u'utf-8')

    # we should also say the JSON content type header
     headers = { u'Content-Type' : u'application/json' }

# now do the request for a url
     req = urllib2.Request(url, post_data, headers)

# send the request
     try:
         res = urllib2.urlopen(req)
         the_page = res.read()
         text = the_page.decode(u"utf8")
         response = text[len(u'{operation": "'):len(text)-2]
         if g_print == True:
            print u'WriteTreeNodeValue Operation UID : ' +response #show the page source, to see I have a response
         if (wakeup == u'true'):
            Process_PostSMSWakeup([sysuid])
         if g_print == True:
            print u"OK"
         return (API_SUCCESS, response)
     except urllib2.HTTPError, e:
        if g_print == True:
            print e.read()
        return (API_FAILED, INVALID)

# Infosys Changes begin for Tracker 4408

def find_nth(srcstring, substring, n):
    i = -1
    for _ in xrange(n):
        i = srcstring.find(substring, i + len(substring))
        if i == -1:
            break
    return i

# 11.	Check Operation status
# Syntax: checkoperation <op uid>
# Reponse Tuple: ( Status, {uid, state} )
def Process_CheckOperationStatus(operationId):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)

     # Removed dependency on deprecated API: /api/v1/operations
     #request = g_server+'/api/v1/operations?access_token='+g_access_token+'&uid='+operationId
     request = g_server+u'/api/v1/operations/'+operationId+u'/tasks?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token
     try:
         # Get tasks for the operation
         url = urllib2.urlopen(request)         
         resp = url.read()
         s = unicode(resp, encoding=u'utf8')         
         if g_print == True:
             print s

         # Parse response to get state of operation tasks
         index = s.find(u'"count":')
         count = s[index + len(u'"count":')]
        # Iterate count times
        # Populate state_dict with { uid, uid_state }
        # for each uid in operation
         itr = 1
         state_dict = {}
         while (itr <= int(count)):
             start = find_nth(s, u'"state":"', itr) # Extract 'state' from response
             uid_state = s[start+len(u'"state":"'):]
             uid_state = uid_state[:uid_state.find(u'"')]

             start = find_nth(s, u'"target":"', itr) # Extract 'target' from response
             uid = s[start+len(u'"target":"'):]
             uid = uid[:uid.find(u'"')]
             # Set uid and corresponding state in dict
             state_dict[uid] = uid_state
             itr = itr + 1
         if g_print == True:
             print state_dict
         return (API_SUCCESS, state_dict)
     except:
         if g_print == True:
            print u"REQUEST FAILED. Please retry."
         return (API_FAILED, INVALID)

# 12.	System Activate
# Syntax: activate [Uid]
# Reponse Tuple: ( Status, Operation ID )
def Process_SystemActivate(uid):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"FAILURE! Please issue Init command"
        return (AUTH_FAILED, INVALID)

     url = g_server+u'/api/v1/operations/systems/activate?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token

     # Build JSON content for API
     json_dict = {u"uids" : [uid]}
     json_data = json.dumps(json_dict)

     # convert str to bytes (ensure encoding is OK)
     post_data = json_data.encode(u'utf-8')

     # we should also say the JSON content type header
     headers = { u'Content-Type' : u'application/json' }

     # now do the request for a url
     req = urllib2.Request(url, post_data, headers)

     # send the request to activate system(uid)
     try:
         res = urllib2.urlopen(req)
         the_page = res.read()
         text = the_page.decode(u"utf8")
         # Parse response for op uid
         response = text[len(u'{operation": "'):len(text)-2]
         if g_print == True:
            print u'System Activate Operation UID : ' +response
            print u"OK"
         return (API_SUCCESS, response)
     except urllib2.HTTPError, e:
        if g_print == True:
            print e.read()
            print u"FAILURE"
        return (API_FAILED, INVALID)

# 13.	System Switch To Maintenance
# Syntax: maintenance [Uid]
# Reponse Tuple: ( Status, Operation ID )
def Process_SystemMaintenance(uid):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"FAILURE! Please issue Init command"
        return (AUTH_FAILED, INVALID)

     url = g_server+u'/api/v1/operations/systems/maintenance?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token
     # Build JSON content for API
     json_dict = {u"uids" : [uid]}
     json_data = json.dumps(json_dict)

     # convert str to bytes (ensure encoding is OK)
     post_data = json_data.encode(u'utf-8')

     # we should also say the JSON content type header
     headers = { u'Content-Type' : u'application/json' }

     # now do the request for a url
     req = urllib2.Request(url, post_data, headers)

     # send the request to switch system to maintenance
     try:
         res = urllib2.urlopen(req)
         the_page = res.read()
         text = the_page.decode(u"utf8")
         # Parse response to get operation UID
         response = text[len(u'{operation": "'):len(text)-2]
         if g_print == True:
            print u'System Maintenance Operation UID : ' +response
            print u"OK"
         return ( API_SUCCESS, response)
     except urllib2.HTTPError, e:
        if g_print == True:
            print e.read()
            print u"FAILURE"
        return (API_FAILED, INVALID)

# 14.	Edit System
# Syntax: editsystem Uid gatewayuid appuidlist subsuidlist(optional)
# Reponse: Operation ID
def Process_EditSystem(uid, gatewayuid, appuidlist, subsuidlist=[]):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"FAILURE! Please issue Init command"
        return (AUTH_FAILED, INVALID)

     url = g_server+u'/api/v1/systems/'+uid+u'?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token

     # Build JSON content for the api
     headers = { u'Content-Type' : u'application/json' }
     k = 0
     # Build Application uid list
     applist_json = []
     while (k < len(appuidlist)):
        appdict_json = {u"uid":   appuidlist[k]}
        k = k+1
        applist_json.append(appdict_json)
     # Build Subscription uid list
     k = 0
     subslist_json = []
     while (k < len(subsuidlist)):
        subsdict_json = {u"uid":   subsuidlist[k]}
        k = k+1
        subslist_json.append(subsdict_json)

     json_dict ={u"gateway" : {u"uid" : gatewayuid},
                u"application" : applist_json,
                u"subscriptions" : subslist_json}

     #json_dict ={"gateway" : {"uid" : gatewayuid},
      #           "application" : [{"uid" : appuid}],
       #          "subscriptions" : [{"uid" : "85b45113632942c982325ac9abe6321c1"}]}
     json_data = json.dumps(json_dict)
     # convert str to bytes (ensure encoding is OK)
     put_data = json_data.encode(u'utf-8')

     # now do the PUT request with a url
     req = urllib2.Request(url, put_data, headers, method=u'PUT')

     try:
        # send request to edit system
         resp = urllib2.urlopen(req)
         if g_print == True:
            print resp.status
            print resp.reason
         # Parse response string
         the_page = resp.read()
         text = the_page.decode(u"utf8")
         if g_print == True:
            print text
         return (API_SUCCESS, resp.reason)
     except urllib2.HTTPError, e:
        if g_print == True:
            print e.read()
            print u"FAILURE"
        return (API_FAILED, INVALID)

   # 15.	Send AT command
# Syntax: sendatcommand Uid ATcmd
# Reponse Tuple : (Status, Operation ID)
def Process_SendATCommand(uid, atcmd):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"FAILURE! Please issue Init command"
        return (AUTH_FAILED, INVALID)

     url = g_server+u'/api/v1/operations/systems/atcommand?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token
     # Build JSON content for API
     json_dict = {   u"systems" : { u"uids" : [uid]},
                     u"atcommand" : atcmd
                 }
     json_data = json.dumps(json_dict)

     # convert str to bytes (ensure encoding is OK)
     post_data = json_data.encode(u'utf-8')

     # we should also say the JSON content type header
     headers = { u'Content-Type' : u'application/json' }

     # now do the request for a url
     req = urllib2.Request(url, post_data, headers)

     # send the request for AT command
     try:
         res = urllib2.urlopen(req)
         the_page = res.read()
         text = the_page.decode(u"utf8")
         # Parse response for Operation uid
         response = text[len(u'{operation": "'):len(text)-2]
         if g_print == True:
            print u'Send ATCommand Operation UID : ' +response
            print u"OK"
         return ( API_SUCCESS, response)
     except urllib2.HTTPError, e:
        if g_print == True:
            print e.read()
            print u"FAILURE"
        return (API_FAILED, INVALID)

# 16.	Get AT Response
# Syntax: getatresponse Op ID
# Reponse Tuple: (Status, Message parameter)
def Process_GetATResponse(operationId):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)

     request = g_server+u'/api/v1/operations/'+operationId+u'/tasks?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token
     try:
        #send the request for AT response
         with urllib2.urlopen(request) as url:
            resp = url.read()
            s = unicode(resp, encoding=u'utf8')
            if g_print == True:
                print s
            index = s.find(u'"count":')
            count = s[index + len(u'"count":')]

            index1 = s.find(u'"state":"')
            status = s[index1 + len(u'"state":"'):]
            status = status[:status.find(u'",')]

            atResp = u""
            # Get AT command response for one system uid at a time
            if (count == u'1'):
                start = s.find(u'"messages":') + len(u'"messages":')
                string_list = s[start:]

                ret_val = find_nth(string_list, u'"message":"', 1)
                if (ret_val != -1):
                    action = string_list[ret_val+len(u'"message":"'):]
                    action = action[:action.find(u'"')]
                    if(action == u'action [OPENAT_AT_COMMAND]'):
                        ret_val = find_nth(string_list, u'"message":"', 2)
                        # AT command response
                        if (ret_val != -1):
                            atResp = string_list[ret_val+len(u'"message":"result'):]
                            #print(atResp.find('"}],'))
                            atResp = atResp[:atResp.find(u'"}],')]
                            if (atResp == u'') and (status == u'SUCCESS'):
                                # For AT+CFUN=1, AT response is empty
                                return (API_SUCCESS, u'No ATResponse Message')
                            else:
                                # Trim starting/ending brackets [] in atResp
                                atResp = atResp[2:-1]
                                if (g_print):
                                    print u"Result of AT command: " + atResp
                                return (API_SUCCESS, atResp)
                        elif status == u'SUCCESS':
                            return (API_SUCCESS, atResp)
                return (API_FAILED, atResp)
     except:
         if g_print == True:
            print u"REQUEST FAILED. Please retry."
         return (API_FAILED, INVALID)

# 17.	Cancel Operation
# Syntax: cancel Op ID
# Reponse Tuple: (Status, Result string)
def Process_CancelOperation(operationId):     
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)
     # Send empty JSON content
     json_data = u""
     # convert str to bytes (ensure encoding is OK)
     post_data = json_data.encode(u'utf-8')
     request = g_server+u'/api/v1/operations/'+operationId+u'/cancel?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token
     try:
         # send the request to cancel operation
         #with urllib2.urlopen(request,post_data) as url:         
         url = urllib2.urlopen(request,post_data)         
         resp = url.read()         
         s = unicode(resp, encoding=u'utf8')
         if g_print == True:
             print s
         return (API_SUCCESS,'Job Cancelled')
     except:
         if g_print == True:
                print u"REQUEST FAILED. Please retry."
         return (API_FAILED, INVALID)

# 18.	Find Subscription UID
# Syntax: findsubscription <ICCID>
# Reponse Tuple: (Result, UID)
def Process_FindSubscription(ICCID):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)
     request = g_server+u'/api/v1/subscriptions?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token+u'&fields=uid&identifier='+ICCID
     try:
        with urllib2.urlopen(request) as url:
            resp = url.read()
            system = unicode(resp, encoding=u'utf8')
            if (g_print):
                print system
            if(system.find(u'uid')!= -1):
                uid = system[system.find(u'{"uid":"') + len(u'{"uid":"'):]
                uid = uid[:uid.find(u'"}]')]
                if (g_print):
                    print uid
                return (API_SUCCESS, uid)
            else:
                return (API_FAILED, INVALID)
     except:
        if g_print == True:
                print u"REQUEST FAILED. Please retry."
                return (API_FAILED, INVALID)


# 19.	Find Application UID
# Syntax: findapplication <name> <revision>
# Reponse Tuple: (Result, UID)
def Process_FindApplication(name=u"" , revision=u"", carrier_feature="NO", model=u"", carrier=u""):     
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)
     
     if(name != u"") :
        request = g_server+u'/api/v1/applications?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token+u'&fields=uid&name='+name
     if(revision != u"") :
        if carrier_feature == "YES":
            if carrier == "":
                request = g_server+u'/api/v1/applications?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token+u'&fields=uid&type=%s&revision=' % (model) +revision
            else:                
                request = g_server+u'/api/v1/applications?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token+u'&fields=uid&type=%s%%3A%s&revision=' % (model, carrier) +revision
        else:
            request = g_server+u'/api/v1/applications?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token+u'&fields=uid&revision='+revision
            #request = g_server+u'/api/v1/applications?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token+u'&fields=uid&type=%s%%3A'% model +u'&revision='+revision

     print request

     try:
##        with urllib2.urlopen(request) as url:
        url = urllib2.urlopen(request)
        resp = url.read()
        system = unicode(resp, encoding=u'utf8')
        jsonresp = json.loads(system)

        if (g_print):
            print system
        if (jsonresp['count'] != 1):
            print 'Total ' + str(jsonresp['count']) + ' applications are found, please check'
            return (API_FAILED, INVALID)
        else:
            uid = jsonresp['items'][0]['uid']
            if (g_print):
                print uid
            return (API_SUCCESS, uid)
     except:
        if g_print == True:
                print u"REQUEST FAILED. Please retry."
                return (API_FAILED, INVALID)

# Infosys Changes end for Tracker 4408


# Infosys Changes begin for Tracker 4409
# 20.	Release Application
# Syntax : Zip File Path, Force parameter(optional)
# Reponse Tuple: (Result,Op ID)
def Process_ReleaseApplication(zipPath, force=False):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID, INVALID)
     # convert str to bytes (ensure encoding is OK)
     if (force == 1):
        url = g_server+u'/api/v1/operations/applications/release?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token+u'&force=1'
     else:
        url = g_server+u'/api/v1/operations/applications/release?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token+u'&force=0'
     try:
        post_data = open(zipPath,u'rb')
        # update content type header
        headers = { u'Content-Type' : u'application/zip' }
        request = urllib2.Request(url,post_data.read())
        request.add_header(u"Content-Type", u"application/zip")
        request.add_header(u"Accept", u"*/*")
     except:
         if g_print == True:
            print u"Unable to generate post data"
            print u"FAILURE"
         return (API_FAILED, INVALID)

     try:
         res = urllib2.urlopen(request)
         # now do the request for a url
         #req = urllib.request(url, post_data.read())
         # req = urllib.request.Request(url, post_data.read(), headers)

         # send the request
         #res = urllib.request.urlopen(req)
         the_page = res.read()
         text = the_page.decode(u"utf8")
         response = text[len(u'{operation": "'):len(text)-2]
         if g_print == True:
            print u'Release App Operation UID : ' +response #show the page source, to see I have a response
            print u"OK"
         return ( API_SUCCESS, response)
     except urllib2.HTTPError, e:
         if g_print == True:
            print e.read()
            print u"FAILURE"
         return (API_FAILED, INVALID)

# 21.	Publish Application
# Syntax: publishapp(uid)
# Reponse Tuple: (Result , Op ID)
def Process_PublishApplication(appuid):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID, INVALID)
     url = g_server+u'/api/v1/operations/applications/publish?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token

     json_dict = {u"application" : appuid }

     json_data = json.dumps(json_dict)

     # convert str to bytes (ensure encoding is OK)
     post_data = json_data.encode(u'utf-8')

     # we should also say the JSON content type header
     headers = { u'Content-Type' : u'application/json' }

     # now do the request for a url
     req = urllib2.Request(url, post_data, headers)

     try:
         # send the request
         res = urllib2.urlopen(req)
         the_page = res.read()
         text = the_page.decode(u"utf8")
         response = text[len(u'{operation": "'):len(text)-2]
         if g_print == True:
                print u'Publish App Operation UID : ' +response #show the page source, to see I have a response
                print u"OK"
         return ( API_SUCCESS, response)
     except urllib2.HTTPError, e:
        if g_print == True:
            print e.read()
            print u"FAILURE"
        return (API_FAILED, INVALID)


# 22.	Install Application
# Syntax: installapp(sysuid, appuid)
# Reponse Tuple: (Result , Op ID)
def Process_InstallApplication(sysuid, appuid):
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")
     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID, INVALID)
     url = g_server+u'/api/v1/operations/systems/applications/install?company=d7378fc019c649bf8131afe3d3eb3663&access_token='+g_access_token

     json_dict = {  u"systems" : {u"uids" : [sysuid]},
                     u"application" : appuid
                }

     json_data = json.dumps(json_dict)

     # convert str to bytes (ensure encoding is OK)
     post_data = json_data.encode(u'utf-8')

     # we should also say the JSON content type header
     headers = { u'Content-Type' : u'application/json' }

     # now do the request for a url
     req = urllib2.Request(url, post_data, headers)

     try:
         # send the request
         res = urllib2.urlopen(req)
         the_page = res.read()
         text = the_page.decode(u"utf8")
         response = text[len(u'{operation": "'):len(text)-2]
         if g_print == True:
                print u'Install App Operation UID : ' +response #show the page source, to see I have a response
                print u"OK"
         return ( API_SUCCESS, response)
     except urllib2.HTTPError, e:
         if g_print == True:
            print e.read()
            print u"FAILURE"
         return (API_FAILED, INVALID)
# Infosys changes end for Tracker 4409

# 23. Configure Communication
def Process_ConfigureCommunication(sysuid,
                                   heartbeat_state= 'OFF',
                                   heartbeat_period= '15',
                                   statusReport_state = 'OFF',
                                   statusReport_period = '15'):
    
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")

     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)

	# Extract parameters
     json_dict = {
         u"systems" : {
             u"uids" : [sysuid]
             },
         u"heartbeat" : {
             u"state" : heartbeat_state,
             u"period" : heartbeat_period
             },
         u"statusReport" : {
             u"state" : statusReport_state,
             u"period" : statusReport_period
             }
         }
             
                       
     url = g_server+u"/api/v1/operations/systems/configure?company=d7378fc019c649bf8131afe3d3eb3663&access_token="+g_access_token

     json_data = json.dumps(json_dict)
     

    # convert str to bytes (ensure encoding is OK)
     post_data = json_data.encode(u'utf-8')

    # we should also say the JSON content type header
     headers = { u'Content-Type' : u'application/json' }

# now do the request for a url
     req = urllib2.Request(url, post_data, headers)
     

# send the request
     try:
         res = urllib2.urlopen(req)         
         the_page = res.read()
         text = the_page.decode(u"utf8")
         if g_print == True:
            print text #show the page source, to see I have a response
         response = text[len(u'{operation": "'):len(text)-2]
         if g_print == True:
            print u'Discover Job UID: '+response #show the page source, to see I have a response         
         if g_print == True:
            print u"OK"
         return ( API_SUCCESS, response)
     except urllib2.HTTPError, e:
        if g_print == True:
            print e.read()
        return (API_FAILED, INVALID)

# 24. send sms
def Process_SendSms(label, text = "hello"):
    
     g_access_token = readConfigData(u"Access_Token")
     g_server = readConfigData(u"Server")

     if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)

	# Extract parameters
     json_dict = {
         u"systems" : {
             u"label" : label
             },
         u"content" : text
         }
             
                       
     url = g_server+u"/api/v1/operations/systems/sms?company=d7378fc019c649bf8131afe3d3eb3663&access_token="+g_access_token

     json_data = json.dumps(json_dict)
     

    # convert str to bytes (ensure encoding is OK)
     post_data = json_data.encode(u'utf-8')
     print post_data

    # we should also say the JSON content type header
     headers = { u'Content-Type' : u'application/json' }

# now do the request for a url
     req = urllib2.Request(url, post_data, headers)
     

# send the request
     try:
         res = urllib2.urlopen(req)         
         the_page = res.read()
         text = the_page.decode(u"utf8")         
         if g_print == True:
            print text #show the page source, to see I have a response
         response = text[len(u'{operation": "'):len(text)-2]
         if g_print == True:
            print u'Send SMS Job UID: '+response #show the page source, to see I have a response         
         if g_print == True:
            print u"OK"
         return ( API_SUCCESS, response)
     except urllib2.HTTPError, e:
        if g_print == True:
            print e.read()
        return (API_FAILED, INVALID)

# 25. get system detail
def Process_GetSystemDetail(sysuid):
    g_access_token = readConfigData(u"Access_Token")
    g_server = readConfigData(u"Server")
    if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)
    request = g_server+u"/api/v1/systems/"+sysuid+u"?company=d7378fc019c649bf8131afe3d3eb3663&access_token="+g_access_token
    print request
    try:        
        url = urllib2.urlopen(request)
        resp = url.read()
        
        s = unicode(resp, encoding=u'utf8')
        #Response Received
        detail_dict = json.loads(s)               
        if g_print == True:            
            print u"OK"
        return (API_SUCCESS, detail_dict)
    except:
        if g_print == True:
            print u"REQUEST FAILED! Please try again"
        return (API_FAILED, INVALID)

# 25. get system detail
def Process_GetOperationsDetail(sysuid):
    g_access_token = readConfigData(u"Access_Token")
    g_server = readConfigData(u"Server")
    if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)
    request = g_server+u"/api/v1/operations/?company=d7378fc019c649bf8131afe3d3eb3663&access_token="+g_access_token
    print request
    try:
        print '+++++++++'
        url = urllib2.urlopen(request)
        print "======="
        resp = url.read()        
        s = unicode(resp, encoding=u'utf8')
        
                
        #Response Received
        detail_dict = json.loads(s)
        for item in detail_dict["items"]:
            print item['uid']
            if item['uid'] == u"8381e0134e4a40748e86cf23526975f6":
                print 'hhhhhhhhh'
        s + 1
        if g_print == True:            
            print u"OK"
        return (API_SUCCESS, detail_dict)
    except:
        if g_print == True:
            print u"REQUEST FAILED! Please try again"
        return (API_FAILED, INVALID)

# 26. get operation for one system
def Process_GetOperationsFor1System(sysuid, state):
    g_access_token = readConfigData(u"Access_Token")
    g_server = readConfigData(u"Server")
    if g_server ==u'' or g_access_token == u'':
        if g_print == True:
            print u"REQUEST FAILED! Please issue Init command"
        return (AUTH_FAILED, INVALID)
    request = g_server+u"/api/v1/operations?asc=name&company=d7378fc019c649bf8131afe3d3eb3663&&access_token="+g_access_token+"&entities=system&target="+sysuid+"&states=" + state
    print request
    temp = []
    try:        
        url = urllib2.urlopen(request)        
        resp = url.read()        
        s = unicode(resp, encoding=u'utf8')
        print s
                
        #Response Received
        response = json.loads(s)
        if response['count']==0:
            print "no operation in Pending"
            return ('-1')
        for  app in response["items"]:
            uid= app['uid']
            print uid
            temp.append(uid)
##            rep = AVREADY_api._postcancelOperation(param, uid)
##            if rep.status_code != 200:
##                print rep
##            else:              
##                print "operation is cancelled"   
        if g_print == True:            
            print u"OK"
            return (API_SUCCESS, temp)
    except:
        if g_print == True:
            print u"REQUEST FAILED! Please try again"
        return (API_FAILED, INVALID) 
     

    
# Command Parser function
# Input: NA
# Output: Return Status OK/FAILURE
# This routine takes user input, parses the input command string
# and performs the command operation
def init_parser(complete_command):
    # Wait for incoming commands
    #while 1:
    if 1:
        response = "N/A"
        print complete_command
##        complete_command = raw_input(u"Please Input the Command: ")
##        if g_print == True:
##            print u"Command Received: ", complete_command
##        # Parse the command and process the command
##		# Set a default response
##        response = u"Unknown command"
        # Check if the command matches known commands, and launch appropriate function
        tokens = complete_command.split(u" ")
        if tokens[0] == u"init":
            # Extract parameters
            if len(tokens)== 6:
               server_c = tokens[1]
               login_c = tokens[2]
               password_c = tokens[3]
               client_id_c = tokens[4]
               secret_key_c = tokens[5]
               response = Process_init(server_c,login_c,password_c,client_id_c,secret_key_c)

        elif tokens[0] == u"finddevice":
            IMEI= tokens[1]
            response = Process_findDevice(IMEI)
            # print('UID= '+response)

        elif tokens[0] == u"sendsmswakeup":
            UIDs = tokens[1:len(tokens)]
            response = Process_PostSMSWakeup(UIDs)
            # print('Operation Id= '+response)

        elif tokens[0] == u"readsystem":
            #param_list= ['applications','uid','subscriptions','activityState','gateway']
            response = Process_ReadSystemDetails(tokens[1],tokens[2])
            # print('Param Values= '+response)

        elif tokens[0] == u"treenodedata":
            response = Process_TreeNodeValue(tokens[1],tokens[2:len(tokens)])
            # print('DataValues= '+response)

        elif tokens[0] == u"discoveryjob" or tokens[0] == u"writetreenodevalue":
             timeout = tokens[len(tokens)-2]
             wakeup = tokens[len(tokens)-1]
             if timeout[:len(u'timeout')]==u'timeout':
                timeout = timeout[len(u'timeout='):]
             else:
                timeout = u""

             if wakeup[:len(u'wakeup')]==u'wakeup':
                wakeup = wakeup[len(u'wakeup='):]
             else:
                wakeup = u""

             if timeout != u"" and wakeup != u"":
                data_list = tokens[3:(len(tokens)-2)]
             elif timeout == u"" and wakeup == u"":
                data_list = tokens[3:(len(tokens))]
             else:
                data_list = tokens[3:(len(tokens))-1]

             if tokens[0] == u"discoveryjob":
                #data_list = ["root.DevDetail.SwV", "en"]
                response = Process_DiscoveryJob(tokens[1], tokens[2], data_list , timeout, wakeup)

             if tokens[0] == u"writetreenodevalue":
                 #data_list = ["car.engine.speed", "100" ,"car.engine.speed1", "200"]
                response = Process_WriteTreeNodeValue(tokens[1], tokens[2], data_list , timeout, wakeup)

        elif tokens[0] == u"checkoperation":
            if len(tokens)== 2:
                response = Process_CheckOperationStatus(tokens[1])
# Infosys changes begin for Tracker 4408
        elif tokens[0] == u"activate":
            if len(tokens)==2:
                UID = tokens[1]
                response = Process_SystemActivate(UID)

        elif tokens[0] == u"maintenance":
            if len(tokens)==2:
                UID = tokens[1]
                response = Process_SystemMaintenance(UID)

        elif tokens[0] == u"editsystem":
            if len(tokens)>=4:
                subs_list = []
                app_list = tokens[3].split(u",")
                if len(tokens)== 5:
                    subs_list = tokens[4].split(u",")
                response = Process_EditSystem(tokens[1], tokens[2], app_list, subs_list)

        elif tokens[0] == u"sendatcommand":
            if len(tokens)==3:
                UID = tokens[1]
                atcmd = tokens[2]
                response = Process_SendATCommand(UID, atcmd)

        elif tokens[0] == u"getatresponse":
            if len(tokens)==2:
                response = Process_GetATResponse(tokens[1])

        elif tokens[0] == u"canceloperation":
            if len(tokens)==2:
                response = Process_CancelOperation(tokens[1])

        elif tokens[0] == u"findsubscription":
            if len(tokens)==2:
                response = Process_FindSubscription(tokens[1])

        elif tokens[0] == u"findapplication":
            print tokens
            if len(tokens)==5:
                if(tokens[1].find(u'name=')!= -1):
                    name = tokens[1][(tokens[1]).find(u'name=')+len(u'name='):]
                    revision = u""
                elif(tokens[1].find(u'revision=')!= -1):
                    revision = tokens[1][(tokens[1]).find(u'revision=') + len(u'revision=') :]
                    name = u""
                carrier_feature = tokens[2]
                model = tokens[3]
                carrier = tokens[4]
                response = Process_FindApplication(name, revision, carrier_feature, model, carrier)
# Infosys changes end for Tracker 4408
# Infosys changes begin for Tracker 4409
        elif tokens[0] == u"releaseapp":
            token=1
            zipPath = u''
            limit = len(tokens)
            force = 0
            if(tokens[len(tokens) - 1] == u'0') or (tokens[len(tokens) - 1] == u'1'):
                force = tokens[len(tokens) - 1]
                limit = len(tokens) - 1
            while token < limit:
                zipPath = zipPath + tokens[token]+u' '
                token=token+1
                #if (len(tokens) == 3):
                 #   force = int(tokens[2])
                #else :
                 #   force = 0
            response = Process_ReleaseApplication(zipPath, force)

        elif tokens[0] == u"publishapp":
            if len(tokens)==2:
                response = Process_PublishApplication(tokens[1])

        elif tokens[0] == u"installapp":
            if len(tokens)==3:
                response = Process_InstallApplication(tokens[1], tokens[2])
# Infosys changes end for Tracker 4409

        elif tokens[0] == u"logout":
            response = Process_logout()

        elif tokens[0] == u"getsystemdetail":            
            response = Process_GetSystemDetail(tokens[1])
        elif tokens[0] == u"getoperations":            
            response = Process_GetOperationsFor1System(tokens[1],tokens[2])
            

        elif tokens[0] == u"sendmessage":
            print len(tokens)
            if len(tokens)==3:
                print "yes"
                response = Process_SendSms(tokens[1], tokens[2])

        elif tokens[0] == u"Configurecommunication":
            if len(tokens) >= 3:
                fields = {u'heartbeat_state' : u'OFF',
                          u'heartbeat_period' : u'15',
                          u'statusReport_state' : u'OFF',
                          u'statusReport_period' : u'15'
                          }                
                
                for i in range(2, len(tokens)):                    
                    if tokens[i].split(u"=")[0] in fields.keys():                        
                        fields[tokens[i].split(u"=")[0]] = tokens[i].split(u"=")[1]             


                response = Process_ConfigureCommunication(tokens[1],
                                                          heartbeat_state = fields['heartbeat_state'],
                                                          heartbeat_period = fields['heartbeat_period'],
                                                          statusReport_state = fields['statusReport_state'],
                                                          statusReport_period = fields['statusReport_period']
                                                          )
                

        elif tokens[0] == u"close":
            if g_print == True:
                print u'Exiting...'
            return
        else:
            if g_print == True:
                print response

        print response
        return response

# Wesh Python Script entry point
def main():
    #invoke the command parser
    init_parser()
    pass
###################################################################################
def findDevice(IMEI):
    if init_parser(u'finddevice ' + IMEI)[0] == 0:
        return Process_findDevice(IMEI)[1].strip()
    else:
        return u"000000000000"
    
def logIn():
    init_parser(ur'init https://edge.m2mop.net pbenattar@sierrawireless.com OASiS_ADMIN 1f98d30f01f84cc3abc2abfe59b8b3e7 210bb1449894481a88c1af1613a9a454')

def logOut():
    Process_logout()

def wakpUp(UID):
    init_parser(u"sendsmswakeup " + UID)



def sendSmsWakeup(UID):
    return Process_PostSMSWakeup(UID)
#############################################################################
Uid_Dict = {#'359515050046956' : '53ac5df2afc849f8bdf7053593ecba40',
            '354610060001524' : '45c8bcbedf3a4e678cc2fb42c54c827b'
            }
class AVMS:
    uid = "00000000000000000"
    
    def __init__(self,imei):
        self.imei = imei
        #init_parser(ur'init https://edge.m2mop.net pbenattar@sierrawireless.com OASiS_ADMIN 1f98d30f01f84cc3abc2abfe59b8b3e7 210bb1449894481a88c1af1613a9a454')
        init_parser(ur'init https://eu.airvantage.net rtang@sierrawireless.com @wmapac201 3155a297e64749ca9648b2993771480b 14f8e440d074421b9126e542af1d5a82')
        temp = init_parser(u'finddevice ' + self.imei)        
        if temp[0] == 0:
            AVMS.uid = temp[1].strip()
            print "AVMS.uid = %s" % str(AVMS.uid)
        else:
            if imei in Uid_Dict.keys():
                print "UID data base is used:"
                AVMS.uid = Uid_Dict[imei]
                print "AVMS.uid = %s" % AVMS.uid
        temp = self.readTreeValue(u"root.DevInfo.Mod")
        self.model = "FF"
        self.carrier = ""
        self.carrier_feature = "NO"
        if ":" in temp:
            self.model = temp.split(":")[0]
            self.carrier = temp.split(":")[1]
            self.carrier_feature = "YES"
        

    def __del__(self):
        print "-----AvMS Server Log out------"
        print "-----Log out ------"
        #init_parser(u"logout")

    def synchronize(self):
        print "----Create a synchronize job: root.----"
        temp = init_parser(u"discoveryjob 4f919b449e4c4fca961e9058c62d372c " + AVMS.uid + u" root.")
        if temp[0] != 0:
            for i in range(0,11):
                sleep(3)
                temp = init_parser(u"discoveryjob 4f919b449e4c4fca961e9058c62d372c " + AVMS.uid + u" root.")
                if temp[0] == 0:
                    break
        return temp[1]

    def discoveryjob(self, node = "root."):
        print "----Create a discoveryjob job: %s----" % node
        temp = init_parser(u"discoveryjob 4f919b449e4c4fca961e9058c62d372c " + AVMS.uid + u" %s" % node)
        return temp[1]

    def wakeUp(self):
        init_parser(u"sendsmswakeup " + AVMS.uid)

    def upgradeFirmware2(self,revision, carrier):
        if carrier =="":
            temp = init_parser(u"findapplication revision=" + revision + " " + "YES" + " " + self.model + " " + carrier)
        else:
            temp = init_parser(u"findapplication revision=" + revision + " " + "YES" + " " + self.model + " " + carrier)
        appuid = temp[1]
        temp = init_parser(u"installapp " + AVMS.uid + u" " + appuid)
        return temp[1]
        

    def upgradeFirmware(self,revision):
        print "\nWe check model type first:"
        temp = self.readTreeValue(u"root.DevInfo.Mod")
        if ":" in temp:
            self.model = temp.split(":")[0]
            self.carrier = temp.split(":")[1]
            self.carrier_feature = "YES"
            self.carrier = self.carrier.replace("&","%26")
            self.carrier = self.carrier.replace("+","%2B")
        else:
            self.model = temp
        print temp
        print "\n"
        temp = init_parser(u"findapplication revision=" + revision.replace(" ","%20") + " " + self.carrier_feature + " " + self.model + " " + self.carrier)
        appuid = temp[1]
        temp = init_parser(u"installapp " + AVMS.uid + u" " + appuid)
        return temp[1]

    def readTreeValue(self,treePath):
        temp = init_parser(u"treenodedata " + AVMS.uid + u" " + treePath)
        if temp[0] == API_SUCCESS:
            return temp[1][treePath]
        else:
            return 'ERROR'

    #for monitorning
    def readMontoringNode(self,treePath):
        temp = init_parser(u"treenodedata " + AVMS.uid + u" root" + treePath.replace(r'/','.'))
        if temp[0] == API_SUCCESS:
            return temp[1][u"root" + treePath.replace(r'/','.')]
        else:
            return 'ERROR'
    def writeTreeValue(self,treePath):
        temp = init_parser(u"writetreenodevalue 4f919b449e4c4fca961e9058c62d372c " + AVMS.uid + u" " + treePath)

    def cancelJob(self,opp_id):       
        print "This job ID would be cancelled : %s" % str(opp_id)
        try:
            init_parser(u"canceloperation " + opp_id)
        except:
            print "Fail to cancel job Id: %s" % str(opp_id)
        

    def configureCommunication(self, **params):
        temp = u"Configurecommunication " + AVMS.uid
        for field, value in params.iteritems():
            temp += u" "            
            temp += (field + u"=" + value)        
        init_parser(temp)

    def applySetting(self, *params):        
        temp = u"writetreenodevalue 4f919b449e4c4fca961e9058c62d372c " + AVMS.uid
        for data in params:
            temp += u" "
            temp += (u"root" + data.split('=')[0].strip() + u" " + data.split('=')[1].strip())

        temp = temp.replace(r'/','.')        
        init_parser(temp)

    def sendTextSms(self, text = "This message is from AvMS server"):
        temp = "sendmessage " + "HL8548_B302" + u" " + text.replace(" ","-")        
        init_parser(temp)
    
    def getSystemDetail(self):
        temp = u"getsystemdetail " + AVMS.uid
        init_parser(temp)
    def getOperations(self, state):
        temp = u"getoperations " + AVMS.uid + " " + state
        result = init_parser(temp)
        return result
    def checkJobStatus(self, jobID):        
        temp = init_parser(u"checkoperation " + jobID)
        if temp[0] == 0:
            return temp[1].values()[0]
        else:
            return 'Unkown'
    def cancelAllJobs(self):
        jobs = self.getOperations("IN_PROGRESS")
        if jobs[0] == 0:
            for job in jobs[1]:        
                self.cancelJob(job)
                sleep(3)
        
        
            

        #init_parser(u"Configurecommunication " + AVMS.uid + u" " + heartbeat_state + u" " + heartbeat_period)
##import sys
##sys.setrecursionlimit(1000000)
##class MntParams():
##    def __getattr__(self, name):
##        self.__dict__[name] = MntParams()
##        return self.__dict__[name]        
##        
if __name__ == u'__main__':
    #main()
##    SagSendAT(UART1, 'AT+CGSN\r')
##    resp = SagWaitResp(UART1, ["\r\n*\r\n\r\nOK\r\n"], 4000)
##    imei = resp.split("\r\n")[1]

    
    #mySystem = AVMS(u"359515050053655")
    
    mySystem = AVMS(u"356170060003333")
    #mySystem.discoveryjob("root.")
    #mySystem.wakeUp()
    #JobId = mySystem.synchronize()
    #print mySystem.checkJobStatus('bcea9410cd364f4893e6fe74c1f187a4')
    
##    mySystem.configureCommunication(heartbeat_state = u'OFF',
##                                    heartbeat_period = u'30',
##                                    statusReport_state = u'OFF',
##                                    statusReport_period = u'15'
##                                    )               
    
    
    mySystem.cancelAllJobs()
    #mySystem.upgradeFirmware(u"RHL7528.2.20b.152000.201601281606.x7160_1")
    #mySystem.cancelAllJobs()

    #mySystem.readTreeValue(u"root.DevDetail.FwV")
    #mySystem.readTreeValue(u"root.Wm.Mon.Sim.Imsi.Val")
    #mySystem.readTreeValue(u"root.Wm.Mon.Sim.Ccid.Val")
    #mySystem.readTreeValue(u"root.Wm.Mon.Cell.Rssi.Val")
    #mySystem.readTreeValue(u"root.Wm.Mon.Cell.EcIo.Val")
    #mySystem.readTreeValue(u"root.DevInfo.DevId") #IMEI
    #mySystem.readTreeValue(u"root.Wm.Mon.Cell.Id.Val") #Current Network Technology
    #mySystem.readTreeValue(u"root.Wm.Mon.Cell.LTE.Link.RSRP.Val")
    #mySystem.readTreeValue(u"root.Wm.Mon.Cell.LTE.Link.RSRQ.Val")
    #mySystem.readTreeValue(u"root.Wm.Mon.Traf.Gprs.Home.Up.Val")
    #mySystem.readTreeValue(u"root.Wm.Mon.Traf.Gprs.Roam.Up.Val")
    #mySystem.readTreeValue(u"root.Wm.Mon.Traf.Gprs.Home.Down.Val")
    #mySystem.readTreeValue(u"root.Wm.Mon.Traf.Gprs.Roam.Down.Val")
    #mySystem.readTreeValue(u"root.Wm.Mon.Nwk.IpAd.Val")



    
    #print mySystem.readTreeValue(u"root.DevInfo.Mod")
    #print mySystem.readTreeValue(u"root.Wm.Mon.Traf.Sms.Home.Mt.Val")
    #print mySystem.readMontoringNode(u".Wm/Mon/Traf/Call/Home/Mo/Val" )
##    mySystem.applySetting(r".Wm/Mon/Traf/Call/Home/Mo/Trig/Mode = 1",
##                          r".Wm/Mon/Traf/Call/Home/Mo/Trig/Val = 2")
    
##    params.Wm.Mon.Traf.Sms.Home.Mt.Tim.Trig.Mode = 9
##    print params.Wm.Mon.Traf.Sms.Home.Mt.Tim.Trig.Mode
    
##    print mySystem.applySetting(r".Wm/Mon/Traf/Sms/Home/Mt/Tim/Trig/Mode = 1",
##                                r".Wm/Mon/Traf/Sms/Home/Mt/Trig/Val= 2")
    #print mySystem.writeTreeValue(u"root.Wm.Mon.Traf.Sms.Home.Mt.Tim.Trig.Mode 1 root.Wm.Mon.Traf.Sms.Home.Mt.Trig.Val 2 root.Wm.Mon.Traf.Sms.Home.Mt.Res 1" )
##    print mySystem.readTreeValue(u"root.Wm.Mon.Traf.Sms.Home.Mt.Trig.Hyst" )
##    print mySystem.readTreeValue(u"root.Wm.Mon.Traf.Sms.Home.Mt.Trig.Mode" )
##    print mySystem.readTreeValue(u"root.Wm.Mon.Traf.Sms.Home.Mt.Trig.Val" )
    #print mySystem.readTreeValue(u"root.Wm.Mon.Traf.Sms.Home.Mt.Val" )
    #print mySystem.synchronize()
    #print mySystem.cancelJob(u"d76ff4441e254344aef9e084df4bd2eb")
    #print mySystem.writeTreeValue({u"root.Wm.Mon.Traf.Sms.Home.Mo.Tim":[{u"value":u"0"}]})
    #print mySystem.readTreeValue(u"root.SystemRemote.Monitoring.Traffic.SMS.Mo.Err.Last.Timing")
    


#--------------- Syntax/Example: ping-------------------------------

# 2. Login To the AMS Server
# Syntax:  init <server> <login> <password> <client_id> <secret_key>
# Example: init https://edge.m2mop.net pbenattar@sierrawireless.com OASiS_ADMIN 1f98d30f01f84cc3abc2abfe59b8b3e7 210bb1449894481a88c1af1613a9a454

# 3. Disconnect from AMS server
# Syntax:  logout
# Example: logout

# 4. Close WESH tool
# Syntax:  close
# Example: close

# 5. Find Device
# Syntax:  finddevice <IMEI>
# Example: finddevice 356021010030704

# 6. Send SMS notification
# Syntax:  sendsmswakeup <UIDs>
# Example: sendsmswakeup 1f1f921355a9413997101f88c969da04 36635f7ea4f548a2a6b40f40c8a6a821

# 7. Read System details
# Syntax:  readsystem <UID> <Parameter>
# Example: readsystem 36635f7ea4f548a2a6b40f40c8a6a821 applications

# 8. Get Tree node value
# Syntax:  treenodedata <UID> <DataParam_List>
# Example: treenodedata 36635f7ea4f548a2a6b40f40c8a6a821 root.DevDetail.

# 9. Create Discovery Job
# Syntax:  discoveryjob <ApUID> <UID> <DataParam_List> <Timeout> <WakeUp>
# Example: discoveryjob 4f919b449e4c4fca961e9058c62d372c 36635f7ea4f548a2a6b40f40c8a6a821 root.DevDetail.SwV wakeup=true

# 10. Write Tree node value
# Syntax:  writetreenodevalue <ApUID> <UID> <DataParam_List> <Timeout> <WakeUp>
# Example: writetreenodevalue 4f919b449e4c4fca961e9058c62d372c 36635f7ea4f548a2a6b40f40c8a6a821 root.DevDetail.SwV test wakeup=true

#11. Check Operation status
# Syntax:  checkoperation <Operation Id>
# Example: checkoperation 2fb910115788487a9f8787163d43bfd0

#12. System Activation
# Syntax:  activate <UID>
# Example: activate 36635f7ea4f548a2a6b40f40c8a6a821

#13. Switch System to Maintenance
# Syntax:  maintenance <UID>
# Example: activate 36635f7ea4f548a2a6b40f40c8a6a821

#14. Edit System Information
# Syntax:  editsystem <UID> <Gateway UID> <App UID1,App UID2> <Subs UID1, Subs UID2>
# Example: editsystem 36635f7ea4f548a2a6b40f40c8a6a821 3afbce902aed4a5fa9374b91ddbfc969 f95cd7f8eb2e482e8792eaa067f1c9e0

#15. Send AT Command
# Syntax:  sendatcommand <UID> <ATCommand>
# Example: sendatcommand 36635f7ea4f548a2a6b40f40c8a6a821

#16. Get Response to AT Command
# Syntax:  getatresponse <Operation ID>
# Example: getatresponse 36635f7ea4f548a2a6b40f40c8a6a821

#17. Cancel Operation
# Syntax:  canceloperation <Operation ID>
# Example: canceloperation 94fc107645bd4027b7721526a2032b23

#18. Find Subscription
# Syntax:  findsubscription <ICCID>
# Example: findsubscription 89331058030225220152

#19. Find Application
# Syntax:  findapplication <Name or Revision>
# Example: findapplication name=OASIS2.52_WP24_WMP100
# Example: findapplication revision=B7.52.0.201303011325.WMP100

#20. Release application
# Syntax:  releaseapp <Zip File Path>  <Force parameter(optional)>
# Example: releaseapp C:\Users\admin\Desktop\4409\Oasis-7.52.0.WP34.SL6087.zip 0

#21. Publish application
# Syntax:  publishapp <appuid>
# Example: publishapp 43c4a1d58f8649aaa193275a7af28103

#22. Install Application
# Syntax: installapp(sysuid, appuid)
# Example : installapp 1f1f921355a9413997101f88c969da04 f95cd7f8eb2e482e8792eaa067f1c9e0

#23.
# Syntax:  Configurecommunication <UID> heartbeat_period=?? heartbeat_state=?? statusReport_state=?? statusReport_period=??
# Example: Configurecommunication 1cd4078a05d54e2395ab0d152ce214dd heartbeat_period=15 heartbeat_state=ON
# Example: Configurecommunication 1cd4078a05d54e2395ab0d152ce214dd statusReport_state=OFF heartbeat_period=30 heartbeat_state=ON statusReport_period=15

#24. Get tasks
# Syntax: testtasks

#26. Get Operations Detail

#-------------------------------------------------------------------


