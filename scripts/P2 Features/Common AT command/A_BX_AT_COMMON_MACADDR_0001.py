# Test Name                                     Description
# A_BX_AT_COMMON_MACADDR_0001                   To check syntax and input range for the AT command "+MACADDR"
# 
# Requirement
# 1 Euler module
#    
# Author: ptnlam
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

# -------------------------- DUT InitializAT+MACADDRon ----------------------------------

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
# A_BX_AT_COMMON_MACADDR_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_AT_COMMON_MACADDR_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")
        
    print "*****************************************************************************************************************"
    print "%s: To check syntax of AT command MACADDR" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Check test command\n"
    SagSendAT(uart_com, 'AT+MACADDR=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 2: Check read command\n"
    SagSendAT(uart_com, 'AT+MACADDR?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+MACADDR: "cc:93:4a:00:00:74"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 3: Check write command\n"
    for i in ('20:fa:bb:20:02:70','-1','1','0'):
        SagSendAT(uart_com, 'AT+MACADDR=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    for i in ('a','*','#'):
        SagSendAT(uart_com, 'AT+MACADDR=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    SagSendAT(uart_com, 'AT+MACADDR=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 4: Check execute command\n"
    SagSendAT(uart_com, 'AT+MACADDR\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 5: Check execute command with invalid parameter\n"
    for i in ('-1','1'):
        SagSendAT(uart_com, 'AT+MACADDR%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    for i in ('a','*','#'):
        SagSendAT(uart_com, 'AT+MACADDR%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nTest Steps completed\n"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT+MACADDR\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Close UART
SagClose(uart_com)
