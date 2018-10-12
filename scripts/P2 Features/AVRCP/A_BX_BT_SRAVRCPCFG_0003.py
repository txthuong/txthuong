# Test Name                                     Description
# A_BX_BT_SRAVRCPCFG_0003                       Check +SRAVRCPCFG with maximum session
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
# A_BX_BT_SRAVRCPCFG_0003
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BT_SRAVRCPCFG_0003"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check +SRAVRCPCFG with maximum session" % test_ID
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
    
    print "\nStep 5: Configure AVRCP profile, repeat 64 times\n"
    for session in range (1, 65):
        if session >= 10:
            bt_hex_addr = 'ff:ff:ff:ff:ff:%s' % session
        else:
            bt_hex_addr = 'ff:ff:ff:ff:ff:0%s' % session
            
        SagSendAT(uart_com, 'AT+SRAVRCPCFG=%s\r' %bt_hex_addr)
        SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: %s,0,"%s",AVRCP\r\n' %(session, bt_hex_addr)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 6: Try to create session 65\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG=ff:ff:ff:ff:ff:65\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 912\r\n'], 2000)

    print "\nStep 7: Checking +SRAVRCPCFG\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"ff:ff:ff:ff:ff:01",AVRCP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*+SRBTCFG: 64,0,"ff:ff:ff:ff:ff:64",AVRCP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 8: Delete session 64th\n"
    SagSendAT(uart_com, 'AT+SRAVRCPDEL=64\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 9: Checking +SRAVRCPCFG\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"ff:ff:ff:ff:ff:01",AVRCP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*+SRBTCFG: 63,0,"ff:ff:ff:ff:ff:63",AVRCP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 10: Try to create session 65\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG=ff:ff:ff:ff:ff:65\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 64,0,"ff:ff:ff:ff:ff:65",AVRCP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 11: Checking +SRAVRCPCFG\n"
    SagSendAT(uart_com, 'AT+SRAVRCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 1,0,"ff:ff:ff:ff:ff:01",AVRCP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*+SRBTCFG: 64,0,"ff:ff:ff:ff:ff:65",AVRCP\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 8: Delete AVRCP session\n"
    for i in range (1,65):
        SagSendAT(uart_com, 'AT+SRAVRCPDEL=%s\r' %i)
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