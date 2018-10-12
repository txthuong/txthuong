# Test Name                                     Description
# A_BX_BT_SRAVRCPCFG_0001                       Check syntax for AT+SRAVRCPCFG command
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
# A_BX_BT_SRAVRCPCFG_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BT_SRAVRCPCFG_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax for AT+SRAVRCPCFG command" % test_ID
    print "*****************************************************************************************************************"
    
    bt_addr = 'ec:f3:42:09:96:78'
    
    print "\nStep 1: Check +SRAVRCPCFG test command\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 2: Checking +SRAVRCPCFG execute command\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 3: Checking +SRAVRCPCFG read command\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Configure I2S with the default values\n"
    SagSendAT(uart_com, 'AT+KI2SCFG=0,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Configure BTC to be discoverable and connectable\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 6: Enable BTC A2DP profile and use the codec of the dev kit\n"
    SagSendAT(uart_com, 'AT+SRAVRCPSTATE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Check syntax of +SRAVRCPCFG command with valid values\n"
    for i in ("00:00:00:00:00:00", "ff:ff:ff:ff:ff:ff", "00:11:22:aa:bb:cc"):
        SagSendAT(uart_com, 'AT+SRAVRCPCFG=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: *,0,"%s",AVRCP\r\n' %i], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 8: Checking +SRAVRCPCFG read command\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"00:00:00:00:00:00",AVRCP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBTCFG: 2,0,"ff:ff:ff:ff:ff:ff",AVRCP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBTCFG: 3,0,"00:11:22:aa:bb:cc",AVRCP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 9: Check syntax of +SRAVRCPCFG command with invalid values\n"
    for i in ('-11:22:-33:AA:BB:CC', 'GG:HH:11:22:FF:33', 'FF:FF:FF::FF:FF', '11:22:33:44:55:666', '11:22:#:44:55:66', 'AA:BB:CC', 'GG:HH:11:22:FF:33:44'):
        SagSendAT(uart_com, 'AT+SRAVRCPCFG=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 10: Check syntax of +SRAVRCPCFG command with additional values\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG=%s,1\r' %bt_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 11: Missing parameter\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 12: Check +SRAVRCPCFG read command with extra characters\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG?a1\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
   
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

SagSendAT(uart_com, "AT+SRAVRCPSTATE=0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)