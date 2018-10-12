# Test Name                                     Description
# A_BX_BLE_SRBLECFG_0002                        Check print all BLE sessions when multiple devices are connected
# 
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
# A_BX_BLE_SRBLECFG_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLECFG_0002"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax of +SRBLECFGCFG command with valid values, invalid values and values out of range" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Create 1st BLE session\n"
    SagSendAT(uart_com, 'AT+SRBLECFG=11:11:11:11:11:11\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,0,"11:11:11:11:11:11",23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: Query: AT+SRBLECFG?\n"
    SagSendAT(uart_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,0,"11:11:11:11:11:11",23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 3: Create 2nd BLE session\n"
    SagSendAT(uart_com, 'AT+SRBLECFG=11:11:11:11:11:22\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 2,0,"11:11:11:11:11:22",23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: Query: AT+SRBLECFG?\n"
    SagSendAT(uart_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,0,"11:11:11:11:11:11",23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLECFG: 2,0,"11:11:11:11:11:22",23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 5: Create 3th BLE session\n"
    SagSendAT(uart_com, 'AT+SRBLECFG=11:11:11:11:11:33\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 3,0,"11:11:11:11:11:33",23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Query: AT+SRBLECFG?\n"
    SagSendAT(uart_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,0,"11:11:11:11:11:11",23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLECFG: 2,0,"11:11:11:11:11:22",23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLECFG: 3,0,"11:11:11:11:11:33",23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 10: Close the BLE configure\n"
    for i in range (1,4):
        SagSendAT(uart_com, 'AT+SRBLEDEL=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 11: Query +SRBLECFG \n"
    SagSendAT(uart_com, 'AT+SRBLECFG?\r')
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

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)