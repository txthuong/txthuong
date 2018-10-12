# Test Name                                     Description
# A_BX_EmbeddedSW_SRWSFWDHTTP_0001              Check syntax for +SRWSFWDHTTP command
# 
# Requirement
# 1 Euler module
#
# Author: txthuong
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

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_SRWSFWDHTTP_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SRWSFWDHTTP_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax for +SRWSFWDHTTP command" % test_ID
    print "***********************************************************************************************************************"

    print "\nStep 1: Check +SRWSFWDHTTP test command"
    SagSendAT(uart_com, 'AT+SRWSFWDHTTP=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 2: Check +SRWSFWDHTTP execute command"
    SagSendAT(uart_com, 'AT+SRWSFWDHTTP\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 3: Check +SRWSFWDHTTP read command"
    SagSendAT(uart_com, 'AT+SRWSFWDHTTP?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSFWDHTTP: *\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Check +SRWSFWDHTTP write command with valid parameter"
    for state in [1, 0]:
        SagSendAT(uart_com, 'AT+SRWSFWDHTTP=%s\r' % state)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 5: Check +SRWSFWDHTTP write command with invalid parameter <state>"
    for state in [-1, 2, 'a', 'A', '!', '@', '%']:
        SagSendAT(uart_com, 'AT+SRWSFWDHTTP=%s\r' % state)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 6: Check +SRWSFWDHTTP write command with missing parameter"
    SagSendAT(uart_com, 'AT+SRWSFWDHTTP=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 7: Check +SRWSFWDHTTP write command with extra parameter"
    for state in [0, 1]:
        SagSendAT(uart_com, 'AT+SRWSFWDHTTP=%s,1\r' % state)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, 'AT+SRWSFWDHTTP=%s,"A"\r' % state)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nTest Steps completed"

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