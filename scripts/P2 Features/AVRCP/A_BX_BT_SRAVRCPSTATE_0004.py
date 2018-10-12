# Test Name                                     Description
# A_BX_BT_SRAVRCPSTATE_0004                     Check if AVRCP session will be deleted when we disable the profile
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
# A_BX_BT_SRAVRCPSTATE_0004
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BT_SRAVRCPSTATE_0004"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check +SRAVRCPSTATE when AVRCP profile is already disable or enable" % test_ID
    print "*****************************************************************************************************************"
    
    bt_addr = 'ec:f3:42:09:96:78'
    
    print "\nStep 1: Reset Factory module\n"
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 5000)
    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
    
    print "\nDUT: Enable subsystem\n"
    SagSendAT(uart_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Check default AVRCP state\n"
    SagSendAT(uart_com, 'AT+SRAVRCPSTATE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRAVRCPSTATE: 0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 3: Enable AVRCP\n"
    SagSendAT(uart_com, 'AT+SRAVRCPSTATE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Configure several AVRCP sessions\n"
    for i in ('ec:f3:42:09:96:78','ec:f3:42:09:96:79','ec:f3:42:09:96:80'):
        SagSendAT(uart_com, 'AT+SRAVRCPCFG=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: *,0,"%s",AVRCP\r\n' %i], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Query AVRCP configure\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG?\r')
    for i in ('ec:f3:42:09:96:78','ec:f3:42:09:96:79','ec:f3:42:09:96:80'):
        SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: *,0,"%s",AVRCP\r\n' %i], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Disable AVRCP\n"
    SagSendAT(uart_com, 'AT+SRAVRCPSTATE=0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 7: Query AVRCP configure. (All configuration were deleted)\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 8: Disable AVRCP\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG = %s\r' %bt_addr)
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

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)