# Test Name                                Description
# A_BX_POWER_SRPSMODE_0001                 Check syntax for AT+SRPSMODE command
#
# Requirement
#   1 Euler module
#   1 AP running at 2.4GHz band
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
# A_BX_POWER_SRPSMODE_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_POWER_SRPSMODE_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check syntax for AT+SRPSMODE command" % test_ID
    print "***************************************************************************************************************"

    timer = 10

    print "\nStep 1: Configure Power Saving with Wakeup mode: Timer and timer is %s seconds" % timer
    SagSendAT(uart_com, "AT+SRPSCFG=1,%s\r" % timer)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Check +SRPSMODE test command"
    SagSendAT(uart_com, "AT+SRPSMODE=?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 3: Check +SRPSMODE execute command"
    SagSendAT(uart_com, "AT+SRPSMODE\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 4: Check +SRPSMODE read command"
    SagSendAT(uart_com, "AT+SRPSMODE?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    # Check error cases
    print "\nStep 5: Check +SRPSMODE write command with invalid <sleep mode>"
    sleep_mode = [-1, 2, 'a', 'A', '*', '#']
    for mode in sleep_mode:
        SagSendAT(uart_com, 'AT+SRPSMODE=%s\r' % mode)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 6: Check +SRPSMODE write command with missing parameters"
    SagSendAT(uart_com, 'AT+SRPSMODE=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 7: Check +SRPSMODE write command with extra parameters"
    SagSendAT(uart_com, 'AT+SRPSMODE=0,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    SagSendAT(uart_com, 'AT+SRPSMODE=1,a\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    # Check valid cases
    print "\nStep 8: Check +SRPSMODE write command with valid parameters"
    wait_time = timer * 1000 + 2000
    SagSendAT(uart_com, 'AT+SRPSMODE=0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], wait_time)

    SagSendAT(uart_com, 'AT+SRPSMODE=1\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], wait_time)

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
