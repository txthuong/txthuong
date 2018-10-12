# Test Name                                     Description
# A_BX_BT_SRAVRCPPTCMD_0002                     Check +SRAVRCPPTCMD incase the session is not configured and not connected
# Requirement
# 1 Euler module
#    
# Author: ptnlam
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

# -------------------------- DUT Initialization ----------------------------------
test_environment_ready = "Ready"

try:

    print "\n------------Test Environment check: Begin------------"
    # UART Initialization
    print "\nOpen AT Command port"
    uart_com = SagOpen(uart_com, 115200, 8, "N", 1, "None")

    # Display DUT information
    print "\nDisplay DUT information"
    print "\nGet model information"
    SagSendAT(uart_com, 'AT+FMM\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(uart_com, 'AT+CGSN\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(uart_com, 'ATI3\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    # DUT Initialization
    print "\nInitiate DUT"
    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nDUT: Enable subsystem\n"
    SagSendAT(uart_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_BT_SRAVRCPPTCMD_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BT_SRAVRCPPTCMD_0002"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check +SRAVRCPPTCMD in case the session is not configured and not connected" % test_ID
    print "*****************************************************************************************************************"
    
    bt_addr = 'ec:f3:42:09:96:78'
    
    print "\nStep 1: Configure I2S with the default values\n"
    SagSendAT(uart_com, 'AT+KI2SCFG=0,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Configure BTC to be discoverable and connectable\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Enable BTC AVRCP profile and use the codec of the dev kit\n"
    SagSendAT(uart_com, 'AT+SRA2DPSTATE=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Enable BTC AVRCP profile and use the codec of the dev kit\n"
    SagSendAT(uart_com, 'AT+SRAVRCPSTATE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Query AVRCP session (No configuration exist)\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 6: Check +SRAVRCPPTCMD write command with not configured session\n"
    SagSendAT(uart_com, 'AT+SRAVRCPPTCMD=1,0,2\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
    print "\nStep 7: Configure a AVRCP session\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG=%s\r' %bt_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",AVRCP\r\n' %bt_addr], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 8: Configure a A2DP session\n"
    SagSendAT(uart_com, 'AT+SRA2DPCFG=%s\r' %bt_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 2,0,"%s",A2DP\r\n' %bt_addr], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 9: Check +SRAVRCPPTCMD write command with not configured session\n"
    SagSendAT(uart_com, 'AT+SRAVRCPPTCMD=1,0,2\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 922\r\n'], 2000)
    
    print "\nStep 10: Active A2DP session (AVRCP also active)\n"
    SagSendAT(uart_com, 'AT+SRA2DPCNX=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRA2DPAUDIOCFG: 0,44100\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 2,1,"%s",A2DP\r\n' %bt_addr], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,1,"%s",AVRCP\r\n' %bt_addr], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRAVRCPRMTFEAT: *\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRAVRCPMTD: 0,*\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRAVRCPMTD: 1,*\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRAVRCPMTD: 2,*\r\n'], 2000)
    
    print "\nStep 11: Connect to device, query AVRCP session\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,1,"%s",AVRCP\r\n' %bt_addr], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 12: Check +SRAVRCPPTCMD write command\n"
    SagSendAT(uart_com, 'AT+SRAVRCPPTCMD=1,0,2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRAVRCPTCMD: 0,0\r\n'], 5000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRAVRCPTCMD: 0,1\r\n'], 5000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRA2DPAUDIOSTATE: 2\r\n'], 5000)
    
    print "\nStep 12: Disconnect to device\n"
    SagSendAT(uart_com, 'AT+SRA2DPCLOSE=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",AVRCP\r\n' %bt_addr], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 2,0,"%s",A2DP\r\n' %bt_addr], 2000)
    
    print "\nStep 13: Query AVRCP session\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"%s",AVRCP\r\n' %bt_addr], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 14: Delete AVRCP,A2DP configuration\n"
    SagSendAT(uart_com, 'AT+SRAVRCPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, 'AT+SRA2DPDEL=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
   
    print "\nStep 15: Query AVRCP session\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
   
   
    print "\nTest Steps completed\n"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Restore BT state to default
SagSendAT(uart_com, "AT+KI2SCFG=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(uart_com, "AT+SRBTSTATE=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(uart_com, "AT+SRA2DPSTATE=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(uart_com, "AT+SRAVRCPSTATE=0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)