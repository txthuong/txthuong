# Test Name                                     Description
# A_BX_UART_AT&K_0001                           Check if we can connect to module with not default setting of UART
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
    uart_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

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
# A_BX_UART_AT&K_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_UART_AT&K_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check if we can connect to module with not default setting of UART" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Check baudrate\n"
    SagSendAT(uart_com, 'AT+IPR?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+IPR: 115200\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: Check AT&K\n"
    SagSendAT(uart_com, 'AT&K?\r')
    SagWaitnMatchResp(uart_com, ['\r\n&K: 0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 3: Change baudrate\n"
    SagSendAT(uart_com, 'AT+IPR=9600\r')
    SagClose(uart_com)
    uart_com = SagOpen(aux1_com, 9600, 8, "N", 1, "None")

    print "\nStep 4: Try to send AT command\n"
    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Check current baudrate\n"
    SagSendAT(uart_com, 'AT+IPR?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+IPR: 9600\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Enable flow control\n"
    SagSendAT(uart_com, 'AT&K3\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Try to send AT command\n"
    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 8: Check AT&K\n"
    SagSendAT(uart_com, 'AT&K?\r')
    SagWaitnMatchResp(uart_com, ['\r\n&K: 3\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    SagSendAT(uart_com, 'AT+IPR=115200\r')
    SagClose(uart_com)
    uart_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    print "\nStep 7: Enable flow control\n"
    SagSendAT(uart_com, 'AT&K0\r')
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
