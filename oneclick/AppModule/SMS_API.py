#!/bin/env python
# _*_ coding: utf-8 _*_

# ---------------------------------------------------------------------------------
# Name:           SMSComAPI.py
# Purpose:        Define the common interfaces for automation script development.
#
# Author:         Roger Wang
#
# date           who         version     modification
# 2016-08-10     rowang        1.00      Creation
# 2016-08-25     Leven         1.43      Update the function description.
#
# ---------------------------------------------------------------------------------

import time
from ComModuleAPI import *

# Don't use it
def SendSMS(hCom, cmd, context):
    SagSendAT(hCom, cmd)
    resultat = SagWaitLine(hCom, ["> "], 6000)
    if resultat.tabLines[-1][0]!="> ":
        print '!!! Failed, expected response was : "> "'
        SagSendAT(hCom, context + chr(26))
    else:
        SagSendAT(hCom, context + chr(26))

# Don't use it
def check_nw_registered_idle(hCom, timeout=150):
    """
    Objective: to check the NW register status and in idle mode
    INPUT:     hCom: which one at port will be used.
               timeout: set a timeout for check nw status
    OUTPUT:    if NW registered and in idle mode return 'True', or 'False'.
    """
    SagSendAT(hCom, "AT!SELRAT?\r")	
    if SagWaitnMatchResp(hCom, ["\r\n!SELRAT: 01,*\r\n\r\nOK\r\n","\r\n!SELRAT: 05,*\r\n\r\nOK\r\n"],1000):
        pass
    else:
        SagSendAT(hCom, "AT!SELRAT=01\r")
        SagWaitnMatchResp(hCom,  ["\r\nOK\r\n"],1000)
    start_time=time.time()
    while(1):
        SagSleep(5000)
        SagSendAT(hCom, "AT!GSTATUS?\r")
        if SagWaitnMatchResp(hCom, ["*Attached*Idle*\r\nOK\r\n","*Attached*IDLE*\r\nOK\r\n"],1000):
            return True
        elif (time.time() - start_time) > timeout:
            print "## ERROR: ", "Module cann't attach NetWork or not IDLE"
            return False
        else:
            continue

# Don't use it
def check_nw_registered_lte(hCom, timeout=150):
    """
    Objective: to check the NW register status on LTE
    INPUT:     hCom: which one at port will be used.
               timeout: set a timeout for check nw status
    OUTPUT:    if LTE registered and in idle mode return 'True', or 'False'.
    """
    SagSendAT(hCom, "AT!SELRAT?\r")	
    if SagWaitnMatchResp(hCom, ["\r\n!SELRAT: 00,*\r\n\r\nOK\r\n"],1000):
        SagSendAT(hCom, "AT!GSTATUS?\r")
        if SagWaitnMatchResp(hCom, ["*LTE*Attached*\r\nOK\r\n"],1000):
            pass
        else:
            SagSendAT(hCom, "AT+CFUN=1\r")
            SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], 6000)		
    else:
        SagSendAT(hCom, "AT!SELRAT=00\r")
        SagWaitnMatchResp(hCom,  ["\r\nOK\r\n"],1000)	
        SagSendAT(hCom, "AT+CFUN=1\r")
        SagWaitnMatchResp(hCom, ["\r\nOK\r\n"], 6000)	
    start_time=time.time()
    while(1):
        SagSleep(5000)
        SagSendAT(hCom, "AT!GSTATUS?\r")
        if SagWaitnMatchResp(hCom, ["*LTE*Attached*Registered*Idle*\r\nOK\r\n"],1000):
            return True
        elif (time.time()-start_time) > timeout:
            print "## ERROR: ", "Module cann't attach NetWork or not IDLE"
            return False
        else:
            continue

#Don't use it for any new script, only keep it for existing script developed by Leven
def send_msglen_PDU(sms_number="",Len="",DCS=""):
    """
    Objective: Send a fixed length of PDU message to dest MT
               sms_number: SMS target number
               Len: the length of SMS, can be "160"/"161"/"140"/"141"/"70"/"71"
               DCS: PDU message character set, can be "7-BIT"/"8-BIT"/"UCS2"
    OUTPUT:    the length and PDU content for AT+CMGS, likes AT+CMGS=length,PDUcontent
    """
    import re
    isms_number_1=''
    sms_num = (re.findall('\d+',sms_number))[0]
    if len(sms_num) % 2 != 0:
        sms_num_0 = sms_num + 'F'
    else:
        sms_num_0 = sms_num
    for i in re.findall(r'(.{2})',sms_num_0):
        sms_0 = []
        for j in i:
            sms_0.insert(0,j)
        isms_number_1 = isms_number_1 +str(''.join(sms_0))

    len_sms_num = ('%X' %len(sms_num))
    if len(len_sms_num)  == 1:
        len_sms_num = '0' + len_sms_num

    if DCS == 'UCS2'and Len == 70:
        idcs = '08'
        Len = 140
        sms_content = '4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D'
    if DCS == '8-BIT'and Len == 140:
        idcs = '04'
        sms_content = '4161426243634464456546664767486849694A6A4B6B4C6C4D6D4E6E4F6F50705171527253735474557556765777587859795A7A303132333435363738394161426243634464456546664767486849694A6A4B6B4C6C4D6D4E6E4F6F50705171527253735474557556765777587859795A7A3031323334353637383941614262436344644565466647674868'
    if DCS == '7-BIT'and Len == 160:
        idcs = '00'
        sms_content='C1B0503C1C13C9C5B2D17C3C23D1C9B452BD5C33D9CDB6D3FD7C43E1D1B8543E9D53E9D5BAD57EBD63F1D9BC560F8BC966B49AED86CB05C342F1704C2417CB46F3F18C4427D34AF572CD6437DB4EF7F30D8547E352F9744EA557EB56FBF58EC567F35A3D2C269BD16AB61B2E170C0BC5C331915C2C1BCDC733129D4C2BD5CB3593DD6C3BDDCF37141E8D4BE5'
    if DCS == 'UCS2'and Len == 71:
        idcs = '08'
        Len = 142
        sms_content = '4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60597D4F60'
    if DCS == '8-BIT'and Len == 141:
        idcs = '04'
        sms_content = '4161426243634464456546664767486849694A6A4B6B4C6C4D6D4E6E4F6F50705171527253735474557556765777587859795A7A303132333435363738394161426243634464456546664767486849694A6A4B6B4C6C4D6D4E6E4F6F50705171527253735474557556765777587859795A7A303132333435363738394161426243634464456546664767486849'
    if DCS == '7-BIT'and Len == 161:
        idcs = '00'
        sms_content='C1B0503C1C13C9C5B2D17C3C23D1C9B452BD5C33D9CDB6D3FD7C43E1D1B8543E9D53E9D5BAD57EBD63F1D9BC560F8BC966B49AED86CB05C342F1704C2417CB46F3F18C4427D34AF572CD6437DB4EF7F30D8547E352F9744EA557EB56FBF58EC567F35A3D2C269BD16AB61B2E170C0BC5C331915C2C1BCDC733129D4C2BD5CB3593DD6C3BDDCF37141E8D4BE553'

    len_sms ='%X'%(Len)
    if len(len_sms)  == 1:
        len_sms = '0' + len_sms

    PDU = '00'+'0100'+len_sms_num+'81'+isms_number_1+'00'+idcs+len_sms+sms_content
    pduLength = len('0100'+len_sms_num+'81'+isms_number_1+'00'+idcs+len_sms+sms_content)/2
    return str(pduLength),PDU

#Don't use it for any new script, only keep it for existing script developed by Leven
def send_concatenated_sms_PDU(sms_number=""):
    """
    Objective: Send a concatenated of PDU message to dest phone"
               sms_number: SMS target number
    OUTPUT:    length1,PDUcontent1,length2,PDUcontent2 for sent two SMS, likes AT+CMGS=length1,PDUcontent1 and likes AT+CMGS=length2,PDUcontent2
    """
    import re
    isms_number_1=''
    sms_num = (re.findall('\d+',sms_number))[0]
    if len(sms_num) % 2 != 0:
        sms_num_0 = sms_num + 'F'
    else:
        sms_num_0 = sms_num
    for i in re.findall(r'(.{2})',sms_num_0):
        sms_0 = []
        for j in i:
            sms_0.insert(0,j)
        isms_number_1 = isms_number_1 +str(''.join(sms_0))

    len_sms_num = ('%X' %len(sms_num))
    if len(len_sms_num)  == 1:
        len_sms_num = '0' + len_sms_num

    sms_content_1='4161426243634464456546664767486849694A6A4B6B4C6C4D6D4E6E4F6F50705171527253735474557556765777587859795A7A303132333435363738394161426243634464456546664767486849694A6A4B6B4C6C4D6D4E6E4F6F50705171527253735474557556765777587859795A7A3031323334353637383941614262436344644565'
    sms_content_2='46664767486849694A6A4B6B4C6C4D6D4E6E4F6F50705171527253735474557556765777587859795A7A303132333435363738394161426243634464456546664767486849694A6A4B6B4C6C4D6D4E6E4F6F50705171527253735474557556765777587859795A7A30313233343536373839'
    len_sms_1 ='%X'%(134+6)
    len_sms_2 ='%X'%(114+6)
    PDU_1 = '00'+'5100'+len_sms_num+'81'+isms_number_1+'000401'+len_sms_1+'050003250201'+sms_content_1
    pduLength_1 = len('5100'+len_sms_num+'81'+isms_number_1+'000401'+len_sms_1+'050003250201'+sms_content_1)/2
    PDU_2 = '00'+'5100'+len_sms_num+'81'+isms_number_1+'000401'+len_sms_2+'050003250202'+sms_content_2
    pduLength_2 = len('5100'+len_sms_num+'81'+isms_number_1+'000401'+len_sms_2+'050003250202'+sms_content_2)/2
    return str(pduLength_1),PDU_1,str(pduLength_2),PDU_2
