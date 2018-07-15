######################################################
##  Author: HDB
##
##  v1:create subAccounts
##
######################################################


import requests
import json
from time import sleep

class AVMS2:   
    
    def __init__(self,imei):
        self.imei = imei        
        
        self.__serverUrl = "https://eu.airvantage.net"
        
        self.__api_url = self.__serverUrl + "/api/oauth/token"
        
        self.__username = "rtang@sierrawireless.com"
        self.__password  = "@wmapac201"
        
        self.__companyuid = "d7378fc019c649bf8131afe3d3eb3663"
        
        self.__clientId = "3155a297e64749ca9648b2993771480b"
        self.__secretKey="14f8e440d074421b9126e542af1d5a82"
        
        self.request_url = self.__api_url + "?client_id="+ self.__clientId + "&grant_type=password&username="+ self.__username + "&password=" + self.__password +"&client_secret=" + self.__secretKey
        
        print self.request_url    
        self.req = requests.get(self.request_url) 
        print self.req.status_code
        
        self.token = None
        
        if self.req.status_code != 200:
            #print "ERROR!!!!!!!!!!!!!!!!!!!!!!!"
            return ("ERROR")
        else:
            self.__response = self.req.json()
        
            #getToken = response["access_token"]
            self.token = self.__response["access_token"]
            print "Your token is :  " + self.token
            #return (getToken)
        
        self.__systemuid = "00000000000000000"
        
        self.uid = ''
        self.gatewayUid = ''
        self.name = ''
        self.subscribtionUid = ''
        self.uidFw = ''
        
        self.__getVeryImportParameter()
        #self.mySystemUid = ''
        
        
        
        rev = "MDM_SWI9X15A_07.10.08.00_LK_1.3.0_50d2713dfe_OS_3.4.91-8e09beee0c_c00035c758_RFS_unknown_UFS_unknown_LE_16.01.4.m1_91b6e138e461ebb592b50e2a404a2071"
        
        #self.__getDetailsApplication('AR7554-Model-WP14.4',rev, "AR7554")
    
    def __getVeryImportParameter(self):
        
        request = self.__serverUrl + '/api/v1/systems?company=' + self.__companyuid + '&fields=uid&access_token=' + self.token + '&gateway=imei:' + self.imei
        print request
        try:
            req = requests.get(request)
            print req.json()
            self.__systemuid = req.json()['items'][0]['uid']
            self.mySystemUid = self.__systemuid
            print "\nSystem UID: %s" % self.__systemuid
            print "Company UID: %s" % self.__companyuid
            print
        except:
            print "-------->ERROR: Fail to get the system UID !!!"
        
        try:
            d = self.getDetailsSystem()            
            self.uid = d['uid']
            self.gatewayUid = d['gateway']['uid']
            self.name = d['name']
            self.subscribtionUid = d['subscriptions'][0]['uid']
            for each in d['applications']:
                if each['category'] == 'FIRMWARE':
                    self.uidFw = each['uid']
        except:
            print "-------->ERROR: Fail to get very important paras !!!"
        
        
        
    def __getOperationsFor1system(self, state):
        #https://qa-trunk.airvantage.net/api/v1/operations
        api_url = self.__serverUrl + "/api/v1"   
       
        request_url = api_url + "/operations" +"?asc=name&company="+ self.__companyuid + "&access_token=" + self.token
        request_url = request_url +"&entities=system&target=" + self.__systemuid
        request_url =request_url +"&states=" + state 
        print request_url
        req = requests.get(request_url)
        #print req.json()
        resp = req.json()
        
        temp = []
        if resp['count'] == 0:
            print "-------->Comment: No job pendding"
        else:
            for app in  resp["items"]:
                uid= app['uid']
                print uid
                temp.append(uid)
        print "\nHere is the job list on server:"
        print temp
        return temp
    
    
    def __postcancelOperation(self,uid):
        #https://qa-trunk.airvantage.net/api/v1/operations/709e97e5de6b4df594d7227e896151f9/cancel?
        api_url = self.__serverUrl + "/api/v1"     
        postUrl = api_url + "/operations/" +uid +"/cancel"  + "?company="+ self.__companyuid + "&access_token=" + self.token
        print postUrl  
        headers = {'content-type': 'application/json'}
        data1={}
        #data1 = defineBodyType(param)
        #data1['data']=dataList
        
        r = requests.post(postUrl, data= json.dumps(data1) , headers = headers)        
        #print r.json()
        return r
    
    def cancelAllJobs(self):
        jobs = self.__getOperationsFor1system("IN_PROGRESS")
        
        for job in jobs:
            print "\nThis job would be cancelled: %s" % job
            self.__postcancelOperation(job)
            sleep(3)
    
    
    def checkNoJobOnServer(self, job_status = "IN_PROGRESS"):
        jobs = self.__getOperationsFor1system(job_status)
        result = "Has_Job"        
        if len(jobs) == 0:
            result = "No_Job"
        return result
    
    def createSynchronizeJob(self):
        #:systems => { :uids => [@sysUid] }    
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/synchronize"  + "?company="+ self.__companyuid + "&access_token=" + self.token  
        print postUrl
        headers = {'content-type': 'application/json'}
        
        data1 = self.__defineBodyType(self)
        
        operation = '0000'
        
        try:        
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to create synchronize job on server !!!"
            
        return operation
    
    def __defineBodyType(self,param):
        #if param.requestConnection.lower()=="true":
        #    rc=True
        #else:
        #    rc =False            
        
        data1 = {
                 "requestConnection":True,"scheduledTime":None,"timeout":None,"notify":False, 
                 }
        data1["systems"] = {"uids":[self.__systemuid]}  
        
        return data1
    
    def __getDetailsApplication(self, appName, appRev, appType):
        api_url = self.__serverUrl + "/api/v1"
        
        if appType == '-legato-application':
            appType = appName + appType
        
        #request_url = api_url + "/applications/" +"?company="+ self.__companyuid + "&access_token=" + self.token + "&name=" + appName + "&revision=" + appRev + "&type=" + appType
        request_url = api_url + "/applications/" +"?company="+ self.__companyuid + "&access_token=" + self.token + "&name=" + appName + "&fields=uid&revision=" + appRev + "&type=" + appType
        #print request_url
        appId = '0000'
        print request_url
        try:
            req = requests.get(request_url)
            temp = req.json()
            print temp
            if temp['count'] == 0:
                print "-------->ERROR: no package on server !!!"
            if temp['count'] > 1 :
                print "-------->ERROR: more than one package on server !!!"
            if temp['count'] == 1 :
                appId = temp['items'][0]['uid']
        except:
            print "-------->ERROR: fail to get package uid on server !!!"       
    
        return appId
    
    def postRetrieveData(self,dataList):  
        api_url = self.__serverUrl + "/api/v1"     
        postUrl = api_url + "/operations/systems/data/retrieve"  + "?company="+ self.__companyuid + "&access_token=" + self.token  
        headers = {'content-type': 'application/json'}
        data1 = self.__defineBodyType(self)
        
        operation = 'UnKnown'
        
        try:        
            data1['data']=dataList
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print r.json()
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to creat retreve job on server !!!"
        
        return operation
    
    #------------------------------------------------------------------------------------------------------------------------------------
    def postRetrieveReport(self,report_uid):
        operation = 'UnKnown'
        try: 
            api_url = self.__serverUrl  + "/api/v1"
            
            print "\nFirst we get the report detail:"
            request_url = api_url + "/datasets/" + report_uid + "?company="+ self.__companyuid + "&access_token=" + self.token  
            
            req = requests.get(request_url)
            resp = req.json()
            print "Response returned : "
            print resp
            
            
            postUrl = api_url + "/operations/systems/data/retrieve"  + "?company="+ self.__companyuid + "&access_token=" + self.token  
            headers = {'content-type': 'application/json'}
            data1 = self.__defineBodyType(self)
            
            print "\nNow we retreve the data defined in report:"
            print postUrl
               
            data1['data']=resp["configuration"]
            print data1
            
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print r.json()
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to creat retreve job list on server !!!"
            
        return operation
    
    #-------------------------------------------------------------------------------------------------------------------------------------
    def postRetrieveDataList(self,dataList): 
        api_url = self.__serverUrl  + "/api/v1"     
        postUrl = api_url + "/operations/systems/data/retrieve"  + "?company="+ self.__companyuid + "&access_token=" + self.token  
        headers = {'content-type': 'application/json'}
        data1 = self.__defineBodyType(self)
        
        operation = 'UnKnown'
        
        try:        
            data1['data']=dataList
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print r.json()
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to creat retreve job list on server !!!"
            
        return operation
    #-------------------------------------------------------------------------------------------------------------------------------------
    def getDetailsSystem(self):
        api_url = self.__serverUrl + "/api/v1"
           
        request_url = api_url + "/systems/" + self.__systemuid + "?company="+ self.__companyuid + "&access_token=" + self.token
        print request_url
        
        try:
            req = requests.get(request_url)
            response = req.json()
            
        
            self.uid = response['uid']
            self.gatewayUid = response['gateway']['uid']
            self.name = response['name']
            self.subscribtionUid = response['subscriptions'][0]['uid']
            for each in response['applications']:
                if each['category'] == 'FIRMWARE':
                    self.uidFw = each['revision']
        except:
            print "-------->ERROR: fail to get Details System on server !!!"
        return (response)
    
        
    def readTreeNode(self, node, multiple=False): 
        api_url = self.__serverUrl + "/api/v1"   
        request_url = api_url + "/systems/" + self.__systemuid +"/data" + "?company="+ self.__companyuid + "&access_token=" + self.token       
        
        print request_url
        result = 'UnKonwn'
        try:        
            req = requests.get(request_url)
            #print req.text
            temp = req.json()
            #print temp
            print temp[node][0]['value']
            result = temp[node][0]['value']
        except:
            print "-------->ERROR: fail to read node value from server !!!"
        return result
    
    def readTreeNodeList(self, node_list): 
        api_url = self.__serverUrl + "/api/v1"   
        request_url = api_url + "/systems/" + self.__systemuid +"/data" + "?company="+ self.__companyuid + "&access_token=" + self.token       
        
        print request_url
        result = {}        
        try:        
            req = requests.get(request_url)
            temp = req.json()
            for node in node_list:
                if node in temp.keys():
                    print temp[node][0]['value']
                    result[node] = temp[node][0]['value']
                    #result = temp[node][0]['value']
                else:
                    print '-------->Problem: node %s fail to read in server !!!' % node
                
        except:
            print "-------->ERROR: fail to read node value from server !!!"            
        return result
        
        
    
    def installApplication(self,appName, appRev, appType):        
        uidApp = self.__getDetailsApplication(appName, appRev, appType)
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/applications/install"  + "?company="+ self.__companyuid + "&access_token=" + self.token  
        print postUrl   
        headers = {'content-type': 'application/json'}
        
        operation = 'UnKnown'
        
        try:        
            data1 = self.__defineBodyType(self)            
            print self.__systemuid             
            data1["application"] = uidApp            
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print r.json()
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to create installation job on server !!!"
        
        return operation
    
    def installApplicationExt(self,appName, appRev, appType):
        
        uidApp = self.__getDetailsApplication(appName, appRev, appType)
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/applications/install"  + "?company="+ self.__companyuid + "&access_token=" + self.token  
        print postUrl   
        headers = {'content-type': 'application/json'}
        
        operation = 'UnKnown'
        
        try:        
            data1 = self.__defineBodyType(self)            
            print self.__systemuid             
            data1["application"] = uidApp            
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print r.json()
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to create installation job on server !!!"
        
        return (operation,uidApp)
    
    def unistallApplication(self,uidApp):
        print "\n---->Info: Create an uninstall job for %s" % uidApp
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/applications/uninstall"  + "?company="+ self.__companyuid + "&access_token=" + self.token  
           
        headers = {'content-type': 'application/json'}
        
        data1 = self.__defineBodyType(self)    
        data1["application"] = uidApp
      
        
        operation = 'UnKnown'
        print postUrl
        
        try:                
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print r.json()
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to create uninstallation job on server !!!"
        
        return operation
            
    def configureCommunication(self,
                               HBstate = "OFF",
                               HBperiod = "15",
                               STstate = "OFF",
                               STperiod = "15",
                               advReport = []):
        
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/configure"  + "?company=" + self.__companyuid + "&access_token=" + self.token 
        print postUrl
        
        operation = 'UnKnown'
      
        headers = {'content-type': 'application/json'}
        data1 = self.__defineBodyType(self)
        data1["heartbeat"]={"state" : HBstate , "period" : HBperiod}
        data1["statusReport"]={"state": STstate,"period": STperiod}
        if len(advReport) != 0:
            data1["reports"]=advReport
        
        try:                     
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print r.text
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to configure communication on server !!!"
        return operation
        
        
    
    def sendATCommand(self, atcommand):    
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/atcommand"  + "?company="+ self.__companyuid + "&access_token=" + self.token 
        print postUrl
        headers = {'content-type': 'application/json'}
        
        operation = 'UnKnown'
        
        data1 = self.__defineBodyType(self) 
        data1["atcommand"]= atcommand
                 
        try:
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print r.text
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to sent at command from server !!!"
        return operation
            
    def reboot(self):    
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/reboot"  + "?company="+ self.__companyuid + "&access_token=" + self.token 
        print postUrl
        
        operation = 'UnKnown'
    
        headers = {'content-type': 'application/json'}
        data1 = self.__defineBodyType(self)
        
        try:        
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print r.text
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to reboot system from server !!!"
        return operation
        
    def sendWakeUp(self):    
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/wakeup"  + "?company="+ self.__companyuid + "&access_token=" + self.token 
        headers = {'content-type': 'application/json'}
        
        operation = 'UnKnown'
                       
        data1 = {"systems":{"uids":[self.__systemuid]}}
            
        try:
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print r.text
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to send wake up SMS from server !!!"
        return operation
            
    def getOperationTasksDetails(self,uidOp):    
        api_url = self.__serverUrl + "/api/v1" 
        request_url = api_url + "/operations/" + uidOp + "/tasks?company="+ self.__companyuid + "&access_token=" + self.token
        print request_url
        
        state = 'UnKnown'
        
        try:
            req = requests.get(request_url)
            response = req.json()
            print response
            if response['count'] == 1:
                state = response['items'][0]['state']
        except:
            print "-------->ERROR: fail to check operation state from server !!!"
        
        print "State: %s\n" % state
        return state
    
    def writeData(self,node, value):      
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/settings"  + "?company="+ self.__companyuid + "&access_token=" + self.token  
        #print postUrl
        headers = {'content-type': 'application/json'}
        
        setting =[]
        temp = {}
        temp["key"] = node
        temp["value"] = value
        setting.append(temp)
        
        operation = 'UnKnown'
        
        try:
           
            data1 = self.__defineBodyType(self)        
            data1["templatename"] = None
            data1["reboot"] = False
            data1["settings"] = setting
            print data1         
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print '-----------'
            print r.text
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to check operation state from server !!!"
        return operation
    
    def sendCustomCommand(self,command):      
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/command"  + "?company="+ self.__companyuid + "&access_token=" + self.token  
        #print postUrl
        headers = {'content-type': 'application/json'}       
        
        operation = 'UnKnown'
        
        try:
           
            data1 = self.__defineBodyType(self)             
            data1["commandId"] = command           
            print data1         
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print '-----------'
            print r.text
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to check operation state from server !!!"
        return operation
    #---------------------------------------------------------------------------------------------------------------------------------
    def writeDataList(self,data_d={}):      
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/settings"  + "?company="+ self.__companyuid + "&access_token=" + self.token  
        #print postUrl
        headers = {'content-type': 'application/json'}
        
        setting =[]
        
        for each in data_d.keys():
            temp = {}
            temp["key"] = each
            temp["value"] = data_d[each]
            setting.append(temp)
        
        operation = 'UnKnown'
        
        try:
           
            data1 = self.__defineBodyType(self)        
            data1["templatename"] = None
            data1["reboot"] = False
            data1["settings"] = setting
            print data1         
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            print '-----------'
            print r.text
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to check operation state from server !!!"
        return operation
    
    def stopApplication(self, uidApp):
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/applications/stop"  + "?company="+ self.__companyuid + "&access_token=" + self.token  
           
        headers = {'content-type': 'application/json'}
        
        data1 = self.__defineBodyType(self)      
        data1["application"] = uidApp
        
        print postUrl
        
        operation = 'UnKnown'
        
        try:                 
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to stop application from server !!!"
            
        return operation
    
    def startApplication(self, uidApp):
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/operations/systems/applications/start"  + "?company="+ self.__companyuid + "&access_token=" + self.token  
           
        headers = {'content-type': 'application/json'}
        
        data1 = self.__defineBodyType(self)     
        data1["application"] = uidApp
        
        print postUrl
             
        operation = 'UnKnown'        
        try:           
            r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
            operation = r.json()['operation']
        
        except:
            print "-------->ERROR: fail to start application from server !!!"
            
        return operation
        
    
    def deleteSystem(self):
        api_url = self.__serverUrl + "/api/v1"
        # postUrl = api_url + "/operations/systems/delete"  + "?access_token=" + self.token 
        # headers = {'content-type': 'application/json'}
        #  
        # data1={}
        # data1["systems"] ={"uids" :[self.__systemuid]}
        # data1["Gateways"]=self.gatewayUid
        # data1["Subscriptions"]=self.subscribtionUid
        # print
        # print postUrl
        # print data1
        # print
        
        
           
        request_url = api_url + "/systems/" + self.__systemuid + "?company="+ self.__companyuid + "&access_token=" + self.token
        print request_url
        r = requests.delete(request_url)
        
        # r = requests.delete(postUrl, data= json.dumps(data1),headers = headers)
        print r
        
        return r
    
    # def createSystem(self, systemName = '', uidFw = '', uidGateway = '',uidSubscription = ''):
    #     
    #     if systemName == '':
    #         systemName = self.name
    #     if uidFw == '':
    #         uidFw = self.uidFw
    #     if uidGateway == '':
    #         uidGateway = self.gatewayUid
    #     if uidSubscription == '':
    #         uidSubscription = self.subscribtionUid
    # 
    #     api_url = self.__serverUrl + "/api/v1"
    #     postUrl = api_url + "/systems"  + "?access_token=" + self.token 
    #     headers = {'content-type': 'application/json'}
    #      
    #     data1={}
    #     data1["name"] =systemName
    #     data1["type"]=None
    #     data1["applications"]=[{"uid":uidFw}]
    #     data1["gateway"]={"uid":uidGateway}       
    #     
    #     
    #     if uidSubscription!="" :          
    #         data1["subscriptions"] =[{"uid" : uidSubscription}]
    #      
    #     r = requests.post(postUrl, data= json.dumps(data1), headers = headers)   
    #  
    #     print r.text
    #     return r
    
    def getConfigrationData(self):
        api_url = self.__serverUrl + "/api/v1"
        postUrl = api_url + "/applications/"  + self.uid + "/data?dataTypes=command,variable&company=" + self.__companyuid + "&access_token=" + self.token 
        print postUrl
        
        operation = 'UnKnown'        
        
        try:                     
            r = requests.get(postUrl)
            print r.text
            operation = r.json()['operation']
        except:
            print "-------->ERROR: fail to configure communication on server !!!"
        return operation
#####################################################################################################        
def createSystem(systemName = '', uidFw = '', uidGateway = '',uidSubscription = ''):
    
    serverUrl = "https://eu.airvantage.net"
        
    api_url = serverUrl + "/api/oauth/token"
    
    username = "rtang@sierrawireless.com"
    password  = "@wmapac201"
    
    companyuid = "d7378fc019c649bf8131afe3d3eb3663"
    
    clientId = "3155a297e64749ca9648b2993771480b"
    secretKey= "14f8e440d074421b9126e542af1d5a82"
    request_url = api_url + "?client_id="+ clientId + "&grant_type=password&username="+ username + "&password=" + password +"&client_secret=" + secretKey
    
    print request_url    
    req = requests.get(request_url) 
    print req.status_code
    
    token = None
    
    if req.status_code != 200:
        print "ERROR!!!!!!!!!!!!!!!!!!!!!!!"
        return ("ERROR")
    else:
        response = req.json()
    
        #getToken = response["access_token"]
        token = response["access_token"]
        print "Your token is :  " + token        #return (getToken)
    
    
    api_url = serverUrl + "/api/v1"
    postUrl = api_url + "/systems"  +"?company="+ companyuid + "&access_token=" + token

    headers = {'content-type': 'application/json'}
     
    data1={}
    data1["name"] =systemName
    data1["state"] ="INVENTORY"
    data1["lifeCycleState"] = "INVENTORY"
    data1["type"]=None
    data1["applications"]=[{"uid":"%s" % uidFw}]
    data1["gateway"]={"serialNumber":uidGateway}          
    data1["subscription"] ={"uid" : uidSubscription
                            }
    print postUrl
    print data1
    print
    
    temp = '0123456789'
    
    try:     
        r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
        print r.json()
        temp = r.json()['uid']
    except:
            print "-------->ERROR: fail to create a systeom on server !!!" 
    
    return temp

#######################################################################################################
def activateSystem(uidSystem):
    
    serverUrl = "https://eu.airvantage.net"
        
    api_url = serverUrl + "/api/oauth/token"
    
    username = "rtang@sierrawireless.com"
    password  = "@wmapac201"
    
    companyuid = "d7378fc019c649bf8131afe3d3eb3663"
    
    clientId = "3155a297e64749ca9648b2993771480b"
    secretKey="14f8e440d074421b9126e542af1d5a82"
    request_url = api_url + "?client_id="+ clientId + "&grant_type=password&username="+ username + "&password=" + password +"&client_secret=" + secretKey
    
    print request_url    
    req = requests.get(request_url) 
    print req.status_code
    
    token = None
    
    if req.status_code != 200:
        print "ERROR!!!!!!!!!!!!!!!!!!!!!!!"
        return ("ERROR")
    else:
        response = req.json()
    
        #getToken = response["access_token"]
        token = response["access_token"]
        print "Your token is :  " + token
        #return (getToken)
       
    api_url = serverUrl + "/api/v1"
    postUrl = api_url + "/operations/systems/activate"  + "?company="+ companyuid + "&access_token=" + token  
       
    headers = {'content-type': 'application/json'}
    data1={}   
    data1["uids"] = [uidSystem]
    
    print postUrl
    print data1
    
    try:                      
        r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
        print r.text
    
    except:
        print "-------->ERROR: fail to activate a systeom on server !!!" 
    
    try:
        pass
        # print "\nExpier toke\n"
        # request_url = serverUrl + "/api/oauth/expire?access_token=%s" % token
        # requests.post(request_url)
    except:
        print "-------->ERROR: fail to expire token !!!"
        
    return r
################################################################################################################################################################
def creatReport(name = "SZ-Validation-Temp",
                fwUid = "936dcb2affd4494aafdf79ad87cb54e8",
                congig_list = [""]):
    serverUrl = "https://eu.airvantage.net"
        
    api_url = serverUrl + "/api/oauth/token"
    
    username = "rtang@sierrawireless.com"
    password  = "@wmapac201"
    
    companyuid = "d7378fc019c649bf8131afe3d3eb3663"
    
    clientId = "3155a297e64749ca9648b2993771480b"
    secretKey="14f8e440d074421b9126e542af1d5a82"
    request_url = api_url + "?client_id="+ clientId + "&grant_type=password&username="+ username + "&password=" + password +"&client_secret=" + secretKey
    
    print request_url    
    req = requests.get(request_url) 
    print req.status_code
    
    token = None
    
    if req.status_code != 200:
        print "ERROR!!!!!!!!!!!!!!!!!!!!!!!"
        return ("ERROR")
    else:
        response = req.json()
    
        #getToken = response["access_token"]
        token = response["access_token"]
        print "Your token is :  " + token
        #return (getToken)
       
    api_url = serverUrl + "/api/v1"
    postUrl = api_url + "/datasets"  + "?company="+ companyuid + "&access_token=" + token  
       
    headers = {'content-type': 'application/json'}
    data1={}
    data1["name"] = name
    data1["application"] = fwUid
    data1["description"] = "This report is crated by AutoTestPlus."
    data1["configuration"] = congig_list
    
    print postUrl
    print data1
    
    report_id = "00000000000000000"
    try:                      
        r = requests.post(postUrl, data= json.dumps(data1), headers = headers)
        print r.text
        report_id = r.json()["dataset"]["uid"]
    except:
        print "-------->ERROR: fail to create a report on server !!!"
    
    try:
        pass
        # print "\nExpier toke\n"
        # request_url = serverUrl + "/api/oauth/expire?access_token=%s" % token
        # requests.post(request_url)
    except:
        print "-------->ERROR: fail to expire token !!!"    
    
    return report_id
######################################################################################################################
def deleteReport(uid):
    serverUrl = "https://eu.airvantage.net"
        
    api_url = serverUrl + "/api/oauth/token"
    
    username = "rtang@sierrawireless.com"
    password  = "@wmapac201"
    
    companyuid = "d7378fc019c649bf8131afe3d3eb3663"
    
    clientId = "3155a297e64749ca9648b2993771480b"
    secretKey="14f8e440d074421b9126e542af1d5a82"
    request_url = api_url + "?client_id="+ clientId + "&grant_type=password&username="+ username + "&password=" + password +"&client_secret=" + secretKey
    
    print request_url    
    req = requests.get(request_url) 
    print req.status_code
    
    token = None
    
    if req.status_code != 200:
        print "ERROR!!!!!!!!!!!!!!!!!!!!!!!"
        return ("ERROR")
    else:
        response = req.json()
    
        #getToken = response["access_token"]
        token = response["access_token"]
        print "Your token is :  " + token
        #return (getToken)
       
    api_url = serverUrl + "/api/v1"
    postUrl = api_url + "/datasets/" + uid + "?company="+ companyuid + "&access_token=" + token     
    
    
    print postUrl
    
    try:                  
        r = requests.delete(postUrl)
        print r.text
    except:
        print "-------->ERROR: fail to delete a report !!!"
        
    try:
        pass
        # print "\nExpier toke\n"
        # request_url = serverUrl + "/api/oauth/expire?access_token=%s" % token
        # requests.post(request_url)
    except:
        print "-------->ERROR: fail to expire token !!!"
    
    print r.text
    return r
########################################################################################################################################################
def findAllReport():
    serverUrl = "https://eu.airvantage.net"
        
    api_url = serverUrl + "/api/oauth/token"
    
    username = "rtang@sierrawireless.com"
    password  = "@wmapac201"
    
    companyuid = "d7378fc019c649bf8131afe3d3eb3663"
    
    clientId = "3155a297e64749ca9648b2993771480b"
    secretKey="14f8e440d074421b9126e542af1d5a82"
    request_url = api_url + "?client_id="+ clientId + "&grant_type=password&username="+ username + "&password=" + password +"&client_secret=" + secretKey
    
    print request_url    
    req = requests.get(request_url) 
    print req.status_code
    
    token = None
    
    if req.status_code != 200:
        print "ERROR!!!!!!!!!!!!!!!!!!!!!!!"
        return ("ERROR")
    else:
        response = req.json()
    
        #getToken = response["access_token"]
        token = response["access_token"]
        print "Your token is :  " + token
        #return (getToken)
       
    api_url = serverUrl + "/api/v1"
    postUrl = api_url + "/datasets?fields=uid,name,configuration"  + "&company="+ companyuid + "&access_token=" + token  
       
    print postUrl
    
    
    try:                  
        r = requests.get(postUrl)    
        temp = r.json()
        #print temp
        
        # print "\Expire Token\n"
        # request_url = serverUrl + "/api/oauth/expire?access_token=%s" % token
        # 
        # r = requests.post(request_url)
    except:
        print "-------->ERROR: fail to expire token !!!"
        
    return temp["items"]


    
######################################################################################################################################

if __name__ == u'__main__':
    mySystem = AVMS2(u"356776070002220")
    import time
    test = mySystem.cancelAllJobs()
    # for retry in range(20):
    #     time.sleep(10)
    #     job_status = mySystem.getOperationTasksDetails(test)
    #     print "****Info: Query server for retrieving data job on %s time(s)" % (retry + 1)
    #     print "****Info: Job %s state = %s" % (test, job_status)
    #     if job_status in ["SUCCESS"]:
    #         break
    #     if retry == 19:
    #         raise Exception("\n---->Problem: Retrieve data job not done, reach maximum retry times!!!\n\n")
    #print mySystem.readTreeNode("lwm2m.4.0.4")
    print mySystem.readTreeNode("lwm2m.10241.0.3") 
    #test = mySystem.postRetrieveData(["lwm2m.4.0.4"])
    #test = mySystem.sendCustomCommand('lwm2m.7.0.6')
    
    # for retry in range(20):
    #     time.sleep(10)
    #     job_status = mySystem.getOperationTasksDetails(test)
    #     print "****Info: Query server for retrieving data job on %s time(s)" % (retry + 1)
    #     print "****Info: Job %s state = %s" % (test, job_status)
    #     if job_status in ["SUCCESS"]:
    #         break
    #     if retry == 19:
    #         raise Exception("\n---->Problem: Retrieve data job not done, reach maximum retry times!!!\n\n") 

    # mySystem.writeDataList({"lwm2m.7.0.0":0,"lwm2m.7.0.1":0})
    
    # # 1. Create a report, fwUid can be refered from AVMS.ini                
    # report_uid = creatReport(name = "SZ-Validation-Temp", fwUid = "936dcb2affd4494aafdf79ad87cb54e8", congig_list=["lwm2m.1.0.2"])
    # # 2. Retreve the report
    # mySystem = AVMS2(u"352768050019914")
    # job_id = mySystem.postRetrieveReport(report_uid)
    # print job_id
    # 
    # # Waiting job is done and then do your test
    # 
    # # 3. delete report
    # print "Now we delete the report:"    
    # temp = findAllReport()
    # for each_d in temp:
    #     if "SZ-V" in each_d["name"]:            
    #         print each_d["uid"]
    #         deleteReport(each_d["uid"])
    
    # mySystem = AVMS2(u"356776070020810")
    
    # mySystem.configureCommunication('OFF','30','OFF','30',
    #                                 [{"period" : "20",
    #                                   "dataset" : {"uid" : "af2061ef883449ae845866672097d005"}}])
    #mySystem = AVMS2(u"352768050019914") #Huy's system
    
    # mySystem.getConfigrationData()
    # 

    # print mySystem.uid    
    # print mySystem.gatewayUid
    # print mySystem.name
    # print mySystem.subscribtionUid
    # print mySystem.uidFw
    
    
    
    # mySystem.deleteSystem()
    
    
    # uidSystem = createSystem(   "AR7554_Ficosa",                       # System name
    #                             "936dcb2affd4494aafdf79ad87cb54e8",    # System uidFw
    #                             "MQ548200020810",                      # System SN
    #                             "b8aa738d4cf74b3f9f4038d32a062e4f")    # Subscription uid
    # 
    # 
    # activateSystem("16dc24bdd5ec4ff8906f61a2584f3271")
    
    #jobID = mySystem.stopApplication('dd50b5885bf24c0da34ec93e24bc385e')
    
    #jobID = mySystem.startApplication('dd50b5885bf24c0da34ec93e24bc385e')
    #resp = mySystem.getDetailsSystem()
    #print resp
    
    # for each_dict in resp['applications']:
    #     print each_dict
    #     if each_dict['category'] == 'APPLICATION':
    #         print "this applicatin need uninstall : %s" % each_dict['uid']
    #         mySystem.unistallApplication(each_dict['uid'])
    #         
    #     print
    
    
        
    
    
    #code = mySystem.createSynchronizeJob()
    
    #mySystem.cancelAllJobs()
    
    
    #mySystem.writeData(node, value)
    
    #print mySystem.checkNoJobOnServer()
    
    #mySystem.postRetrieveDataList(["lwm2m.3.0.0","lwm2m.1.0.2"])
    
    # d_server = {'lwm2m.1.0.0':'Short Server ID',
    #             'lwm2m.1.0.1':'Lifetime',
    #             'lwm2m.1.0.2':'Default Minimum Period',
    #             'lwm2m.1.0.3':'Default Maximum Period',
    #             'lwm2m.1.0.4':'Disable',
    #             'lwm2m.1.0.5':'Disable Timeout',
    #             'lwm2m.1.0.6':'Notification Storing When Disabled or Offline',
    #             'lwm2m.1.0.7':'Binding',
    #             'lwm2m.1.0.8':'Registration Update Trigger'
    #             }
    # 
    # for node in d_server.keys():
    #     pass
    
    #d = mySystem.readTreeNodeList(["lwm2m.1.0.2","lwm2m.1.0.3"])
    
    # For A_AV_LWM2M.50
    # time1 = time.time()
    
    #temp = mySystem.getDetailsSystem()
    #time2 = temp['lastCommDate']
    
    # time2 - time1 < 60 ??
    
    
    
    
    
    # print mySystem.readTreeNode("lwm2m.1.0.3")
    # print '-----------------------------------'
    # print mySystem.readTreeNode("lwm2m.3.0.0")
    # print mySystem.readTreeNode("lwm2m.3.0.1")
    # print mySystem.readTreeNode("lwm2m.3.0.2")
    # print mySystem.readTreeNode("lwm2m.3.0.20")
    #rev = "MDM_SWI9X15A_07.10.15.00_LK_1.3.0_50d2713dfe_OS_3.4.91-8e09beee0c_99d3311011_RFS_unknown_UFS_unknown_LE_16.01.7.m1_5727ce50185d510ef37bb8ecf52f8b27"
    #mySystem.installApplication('AR7554-WP16.1',rev,"AR7554")
    # 
    # sw_name = "helloWorld_testapp_02"
    # sw_revision = "1.0.0"
    # sw_type = "-legato-application"
    # (jobId, appUid) = mySystem.installApplicationExt(sw_name,sw_revision,sw_type)
    # mySystem.unistallApplication(appUid)
    # mySystem.cancelAllJobs()
##        
##        #self.__getDetailsApplication('AR7554-Model-WP14.4',rev, "AR7554")
##    mySystem.installApplication('AR7554RD-WP15.4_m99',rev,"AR7554RD")
##    mySystem.cancelAllJobs()
    #mySystem.configureCommunication('OFF',30,'OFF',30)
    #mySystem.sendATCommand("ATI3")
    #mySystem.reboot()
    #mySystem.sendWakeUp()
    #mySystem.getOperationTasksDetails(code)
    
    #write 3600 to node lwm2m.1.0.1
    #print mySystem.writeData('lwm2m.1.0.1', 3600)
    
    # Create a normal sw installation with version N
    # myAvmsCfg = AVMSCFG(AVMS_INI)
    # mySystem = AVMS2(u"356776070020810")
    # mySystem.installApplication(myAvmsCfg.AVMS_SW_Upgrade_Package_Name,
    #                             myAvmsCfg.AVMS_SW_Revision_Initial,
    #                             myAvmsCfg.AVMS_SW_Type
    #                             )
    # 
    # # Create a normal sw upgrade from N to N+1    
    # mySystem.installApplication(myAvmsCfg.AVMS_SW_Upgrade_Package_Name,
    #                             myAvmsCfg.AVMS_SW_Revision_Target,
    #                             myAvmsCfg.AVMS_SW_Type
    #                             )
    # 
    # # Create a normal sw upgrade with very big App
    # mySystem.installApplication(myAvmsCfg.AVMS_SW_Upgrade_Big_Package_Name,
    #                             myAvmsCfg.AVMS_SW_Revision_Initial,
    #                             myAvmsCfg.AVMS_SW_Type
    #                             )
    

