# Test Name                                     Description
# A_BX_UART_IPR_0001                            To check syntax for command "+IPR"
# 
# Requirement
# 1 Euler module
#    
# Author: ptnlam
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

# -------------------------- DUT Initializion ----------------------------------

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
# A_BX_UART_IPR_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_UART_IPR_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: To check syntax for command +IPR" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Check test command\n"
    SagSendAT(uart_com, 'AT+IPR=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 2: Check execute command\n"
    SagSendAT(uart_com, 'AT+IPR\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 3: Check read command\n"
    SagSendAT(uart_com, 'AT+IPR?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+IPR: 115200\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Check +IPR write command with invalid parameter <uart_baud_rate> = [-1, 0, a, *]\n"
    for i in ('0','-1'):
        SagSendAT(uart_com, 'AT+IPR=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'],2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    for i in ('a','*','#'):
        SagSendAT(uart_com, 'AT+IPR=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'],2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        
    print "\nStep 6: Check write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+IPR=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 7: Check write command with extra parameters\n"
    SagSendAT(uart_com, 'AT+IPR=9600,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 7: Check write command with valid parameters\n"
    SagSendAT(uart_com, 'AT+IPR=9600\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Reconnect software terminal with new value baudrate\n"
    SagClose(uart_com)
    uart_com = SagOpen(uart_com, 9600, 8, "N", 1, "None")
    
    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Change IPR back defaut\n"
    SagSendAT(uart_com, 'AT+IPR=115200\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagClose(uart_com)
    uart_com = SagOpen(uart_com, 115200, 8, "N", 1, "None")
    
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