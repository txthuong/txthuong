# Test Name                                Description
# A_BX_POWER_SRPSMODE_0002                 Check if can select Power Saving mode without power saving configuration
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
# A_BX_POWER_SRPSMODE_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_POWER_SRPSMODE_0002"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check if can select Power Saving mode without power saving configuration" % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Query power saving configuration"
    SagSendAT(uart_com, "AT+SRPSCFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRPSCFG: 0,0,0'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Check +SRPSMODE write command without power saving configuration"
    SagSendAT(uart_com, 'AT+SRPSMODE=0\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    SagSendAT(uart_com, 'AT+SRPSMODE=1\r')
    SagWaitnMatchResp(uart_com, ['*\r\nERROR\r\n'], 2000)

    timer = 10

    print "\nStep 3: Configure Power Saving with Wakeup mode: Timer and timer is %s seconds" % timer
    SagSendAT(uart_com, "AT+SRPSCFG=1,%s\r" % timer)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Check +SRPSMODE write command with power saving configuration"
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
