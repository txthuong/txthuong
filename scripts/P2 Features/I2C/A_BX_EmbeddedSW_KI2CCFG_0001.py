# Test Name                                     Description
# A_BX_EmbeddedSW_KI2CCFG_0001                  Check syntax for AT+KI2CCFG command
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

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_KI2CCFG_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KI2CCFG_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax for AT+KI2CCFG command" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Check +KI2CCFG test command\n"
    SagSendAT(uart_com, 'AT+KI2CCFG=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 2: Check +KI2CCFG execute command\n"
    SagSendAT(uart_com, 'AT+KI2CCFG\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 3: Check +KI2CCFG write command with valid parameters\n"
    SagSendAT(uart_com, 'AT+KI2CCFG=0,1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Check +KI2CCFG write command with valid parameters\n"
    SagSendAT(uart_com, 'AT+KI2CCFG=0,0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Check +KI2CCFG write command with invalid parameter port_number = -1, 2, a, *\n"
    for port_number in ('-1','2','a','*'):
        SagSendAT(uart_com, 'AT+KI2CCFG=%s,0\r' %port_number)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 6: Check +KI2CCFG write command with invalid parameter enable = -1, 2, a, *\n"
    for enable in ('-1','2','a','*'):
        SagSendAT(uart_com, 'AT+KI2CCFG=%s,0\r' %enable)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 7: Check +KI2CCFG write command with invalid parameter freq = -1, 2, a, *\n"
    for freq in ('-1','2','a','*'):
        SagSendAT(uart_com, 'AT+KI2CCFG=%s,0\r' %freq)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 8: Check +KI2CCFG write command with missing all parameters\n"
    SagSendAT(uart_com, 'AT+KI2CCFG=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 9: Check +KI2CCFG write command with missing parameter enable\n"
    SagSendAT(uart_com, 'AT+KI2CCFG=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 10: Check +KI2CCFG write command with missing parameter port_number\n"
    SagSendAT(uart_com, 'AT+KI2CCFG=,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 11: Check +KI2CCFG write command with extra parameters\n"
    SagSendAT(uart_com, 'AT+KI2CCFG=1,1,1,1,A\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

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