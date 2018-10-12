# Test Name                                Description
# A_BX_POWER_SRPSCFG_0001                  Check syntax for AT+SRPSCFG command
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
# A_BX_POWER_SRPSCFG_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_POWER_SRPSCFG_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check syntax for AT+SRPSCFG command" % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Check +SRPSCFG test command"
    SagSendAT(uart_com, "AT+SRPSCFG=?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 2: Check +SRPSCFG execute command"
    SagSendAT(uart_com, "AT+SRPSCFG\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 3: Check +SRPSCFG read command"
    SagSendAT(uart_com, "AT+SRPSCFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRPSCFG: 0,0,0'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    # Check error cases
    print "\nStep 4: Check +SRPSCFG write command with invalid <wake-up mode>"
    wake_up_mode = [-1, 2, 'a', 'A', '*', '#']
    for mode in wake_up_mode:
        SagSendAT(uart_com, 'AT+SRPSCFG=%s,32,1\r' % mode)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 5: Check +SRPSCFG write command with invalid <option_1>"
    option_1 = [-1, 'a', 'A', '*', '#']
    for op in option_1:
        SagSendAT(uart_com, 'AT+SRPSCFG=0,%s,1\r' % op)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
        SagSendAT(uart_com, 'AT+SRPSCFG=1,%s\r' % op)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 6: Check +SRPSCFG write command with invalid <option_2>"
    option_2 = [-1, 2, 'a', 'A', '*', '#']
    for op in option_2:
        SagSendAT(uart_com, 'AT+SRPSCFG=0,32,%s\r' % op)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 7: Check +SRPSCFG write command with missing parameters"
    SagSendAT(uart_com, 'AT+SRPSCFG=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+SRPSCFG=0\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+SRPSCFG=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+SRPSCFG=0,32\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+SRPSCFG=,32\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+SRPSCFG=0,,0\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 8: Check +SRPSCFG write command with extra parameters"
    SagSendAT(uart_com, 'AT+SRPSCFG=0,32,1,a\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    SagSendAT(uart_com, 'AT+SRPSCFG=0,32,1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    SagSendAT(uart_com, 'AT+SRPSCFG=1,32,1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    # Check valid cases
    print "\nStep 9: Check +SRPSCFG write command with valid parameters"
    option_1 = [0, 2, 4, 12, 13, 14, 15, 25, 26, 27, 32, 33, 34, 35, 36, 37, 38, 39]
    option_2 = [0, 1]
    for op1 in option_1:
        for op2 in option_2:
            print '\n<wake-up mode>: RTC GPIO, <option_1>: %s, <option_2>: %s ...' % (op1, op2)
            SagSendAT(uart_com, 'AT+SRPSCFG=0,%s,%s\r' % (op1, op2))
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
            SagSendAT(uart_com, "AT+SRPSCFG?\r")
            SagWaitnMatchResp(uart_com, ['\r\n+SRPSCFG: 0,%s,%s' % (op1, op2)], 2000)
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    option_1 = [5, 15, 30, 60, 120, 3600]
    for op1 in option_1:
        print '\n<wake-up mode>: Timer, <option_1>: %s ...' % op1
        SagSendAT(uart_com, 'AT+SRPSCFG=1,%s\r' % op1)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+SRPSCFG?\r")
        SagWaitnMatchResp(uart_com, ['\r\n+SRPSCFG: 1,%s' % op1], 2000)
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

# Restore Power Saving Configuration to default
SagSendAT(uart_com, 'AT+SRPSCFG=0,0,0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
