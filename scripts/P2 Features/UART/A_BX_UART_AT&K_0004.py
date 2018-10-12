# Test Name                                     Description
# A_BX_UART_AT&K_0004                           To check function of flow control
# 
# Requirement
# 1 Euler module
#    
# Author: ptnlam
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

# -------------------------- DUT InitializAT+SYSRAMon ----------------------------------

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

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_UART_AT&K_0004
# -----------------------------------------------------------------------------------

test_ID = "A_BX_UART_AT&K_0004"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: To check function of flow control" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Enable Hardware Flow Control\n"
    SagSendAT(uart_com, 'AT&K3\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Check current fow control configure\n"
    SagSendAT(uart_com, 'AT&K?\r')
    SagWaitnMatchResp(uart_com, ['\r\n&K: 3\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Set RTS to high\n"
    SagSetRTS(uart_com, 1)
    time.sleep(1) 
    
    print "\nStep 4: Send AT command, check response\n"
    SagSendAT(uart_com, 'ATI3\r')
    SagWaitnMatchResp(uart_com, ['\r\n%s\r\n' %firmware], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Set RTS to low\n"
    SagSetRTS(uart_com, 0)
    time.sleep(1) 
    
    print "\nStep 6: Send AT command, check response\n"
    SagSendAT(uart_com, 'ATI3\r')
    SagWaitResp(uart_com, ['\r\nOK\r\n'], 5000)
    print "\nModule should returns nothing\n"
    
    print "\nStep 7: Set RTS to high\n"
    SagSetRTS(uart_com, 1)
    time.sleep(1) 
    SagWaitnMatchResp(uart_com, ['\r\n%s\r\n' %firmware], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 8: Send AT command, check response\n"
    SagSendAT(uart_com, 'ATI3\r')
    SagWaitnMatchResp(uart_com, ['\r\n%s\r\n' %firmware], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 9: Disable Hardware Flow Control\n"
    SagSendAT(uart_com, 'AT&K0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 10: Send AT command, check response\n"
    SagSendAT(uart_com, 'ATI3\r')
    SagWaitnMatchResp(uart_com, ['\r\n%s\r\n' %firmware], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Set RTS to low\n"
    SagSetRTS(uart_com, 0)
    time.sleep(1) 
    
    print "\nStep 10: Send AT command, check response\n"
    SagSendAT(uart_com, 'ATI3\r')
    SagWaitnMatchResp(uart_com, ['\r\n%s\r\n' %firmware], 2000)
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

# Close UART
SagClose(uart_com)
