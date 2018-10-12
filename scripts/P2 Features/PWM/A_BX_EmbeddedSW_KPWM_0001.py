# Test Name                                Description
# A_BX_EmbeddedSW_KPWM_0001                Check syntax for AT+KPWM command
#
# Requirement
#   1 Euler module
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
# A_BX_EmbeddedSW_KPWM_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KPWM_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check syntax for AT+KPWM command" % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Check +KPWM test command"
    SagSendAT(uart_com, "AT+KPWM=?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 2: Check +KPWM execute command"
    SagSendAT(uart_com, "AT+KPWM\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 3: Check +KPWM read command"
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    # Check error cases
    print "\nStep 4: Check +KPWM write command with invalid <output>"
    output = [-1, 0, 3, 'a', 'A', '!', '&']
    for operation in (0, 1):
        for op in output:
            SagSendAT(uart_com, 'AT+KPWM=%s,%s\r' % (op, operation))
            SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 5: Check +KPWM write command with invalid <operation>"
    operation =  [-1, 2, 'a', 'A', '!', '&']
    for ouput in (1, 2):
        for op in operation:
            SagSendAT(uart_com, 'AT+KPWM=%s,%s\r' % (ouput, op))
            SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 6: Check +KPWM write command with invalid <period>"
    period = [-1, 1, 500001, 'a', 'A', '!', '&']
    for pe in period:
        SagSendAT(uart_com, 'AT+KPWM=1,1,%s,50\r' % pe)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 7: Check +KPWM write command with invalid <dutycycle>"
    dutycycle = [-1, 101, 'a', 'A', '!', '&']
    for dc in dutycycle:
        SagSendAT(uart_com, 'AT+KPWM=1,1,1000,%s\r' % dc)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 8: Check +KPWM write command with missing parameters"
    SagSendAT(uart_com, 'AT+KPWM=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    for output in (1, 2):
        SagSendAT(uart_com, 'AT+KPWM=%s\r' % output)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    for operation in (0, 1):
        SagSendAT(uart_com, 'AT+KPWM=,%s\r' % operation)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 9: Check +KPWM write command with extra parameters"
    for output in (1, 2):
        SagSendAT(uart_com, 'AT+KPWM=%s,1,1000,40,1\r' % output)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    # Check valid cases
    print "\nStep 10: Check +KPWM write command with valid parameters"
    for output in (1, 2):
        for operation in (0, 1):
            SagSendAT(uart_com, 'AT+KPWM=%s,%s\r' % (output, operation))
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
            for period in (2, 1000, 10000, 500000):
                for dutycycle in (0, 25, 50, 75, 100):
                    SagSendAT(uart_com, 'AT+KPWM=%s,%s,%s,%s\r' % (output, operation, period, dutycycle))
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

# Restore PWM to default
SagSendAT(uart_com, 'AT+KPWM=1,0,1000,50\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(uart_com, 'AT+KPWM=2,0,1000,50\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
