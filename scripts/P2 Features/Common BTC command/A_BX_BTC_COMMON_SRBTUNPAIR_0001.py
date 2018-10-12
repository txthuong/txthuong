# Test Name                                     Description
# A_BX_BTC_COMMON_SRBTUNPAIR_0001               To check syntax and input range for the AT command "+SRBTUNPAIR"
# 
# Requirement
# 1 Euler module + 1 smartphone 
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
# A_BX_BTC_COMMON_SRBTUNPAIR_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BTC_COMMON_SRBTUNPAIR_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "****************************************************************************************************************"
    print "%s: To check syntax and input range for the AT command +SRBTUNPAIR" % test_ID
    print "*****************************************************************************************************************"
    
    smartphone_bluetooth_addr = 'ec:f3:42:09:96:78'
    
    print "\nStep 1: Set the state of the module to connectable and pairable\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Pairing Bluetooth of Smartphone with module\n"
    wx.MessageBox('Pairing Bluetooth of Smartphone with module then click "OK"', 'Info',wx.OK)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTPAIR: "%s",1\r\n' %smartphone_bluetooth_addr], 2000)
    
    print "\nStep 3: Query +SRBTPAIR command\n"
    SagSendAT(uart_com, 'AT+SRBTPAIR?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTPAIR: "%s"\r\n' %smartphone_bluetooth_addr], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: Check +SRBTUNPAIR test command\n"
    SagSendAT(uart_com, 'AT+SRBTUNPAIR=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 5: Check +SRBTUNPAIR execute command\n"
    SagSendAT(uart_com, 'AT+SRBTUNPAIR\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 6: Query +SRBTPAIR command\n"
    SagSendAT(uart_com, 'AT+SRBTPAIR?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Check +SRBTUNPAIR read command\n"
    SagSendAT(uart_com, 'AT+SRBTUNPAIR?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 8: Check +SRBTUNPAIR write command\n"
    SagSendAT(uart_com, 'AT+SRBTUNPAIR="%s"\r' %smartphone_bluetooth_addr)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 9: Check write command without parameters\n"
    SagSendAT(uart_com, 'AT+SRBTUNPAIR=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 10: Check write command with extra parameters\n"
    SagSendAT(uart_com, 'AT+SRBTUNPAIR=%s,1\r' %smartphone_bluetooth_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    print "\nStep 11: Check write command with extra parameters\n"
    SagSendAT(uart_com, 'AT+SRBTUNPAIR=%s,1,a\r' %smartphone_bluetooth_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    print "\nStep 12: Check write command with invalid parameters\n"
    for bt_addr in ('-11:22:-33:AA:BB:CC', 'GG:HH:11:22:FF:33', 'FF:FF:FF::FF:FF', '11:22:33:44:55:666', '11:22:#:44:55:66', 'AA:BB:CC', 'GG:HH:11:22:FF:33:44'):
        SagSendAT(uart_com, 'AT+SRBTUNPAIR=%s,1,a\r' %bt_addr)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 13: Check +SRBTUNPAIR execute command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBTUNPAIR123\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 14: Query pair list. All pair devices are removed\n"
    SagSendAT(uart_com, 'AT+SRBTPAIR?\r')
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

# Set to defaut value
SagSendAT(uart_com, 'AT+SRBTSTATE=0,0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)