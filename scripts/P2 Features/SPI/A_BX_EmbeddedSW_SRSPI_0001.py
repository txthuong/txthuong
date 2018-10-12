# Test Name                                Description
# A_BX_EmbeddedSW_SRSPI_0001               Check syntax for AT+SRSPI command
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
# A_BX_EmbeddedSW_SRSPI_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SRSPI_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check syntax for AT+SRSPI command" % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Check +SRSPI test command"
    SagSendAT(uart_com, "AT+SRSPI=?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 2: Check +SRSPI execute command"
    SagSendAT(uart_com, "AT+SRSPI\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 3: Check +SRSPI read command"
    SagSendAT(uart_com, "AT+SRSPI?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPI: 0,0'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    # Check error cases
    print "\nStep 4: Check +SRSPI write command with invalid <mode>"
    mode = [-1, 4, 'a', 'A', '*', '#']
    for mo in mode:
        SagSendAT(uart_com, 'AT+SRSPI=%s,0\r' % mo)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 5: Check +SRSPI write command with invalid <flags>"
    flags = [-1, 4, 'a', 'A', '*', '#']
    for flag in flags:
        for mode in [0, 1, 2, 3]:
            SagSendAT(uart_com, 'AT+SRSPI=%s,%s\r' % (mode, flag))
            SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 6: Check +SRSPI write command with missing parameters"
    SagSendAT(uart_com, 'AT+SRSPI=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    for mode in [0, 1, 2, 3]:
        SagSendAT(uart_com, 'AT+SRSPI=%s\r' % mode)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    for flag in [0, 1, 2, 3]:
        SagSendAT(uart_com, 'AT+SRSPI=,%s\r' % flag)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 8: Check +SRSPI write command with extra parameters"
    SagSendAT(uart_com, 'AT+SRSPI=0,0,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    # Check valid cases
    print "\nStep 9: Check +SRSPI write command with valid parameters"
    mode = [0, 1, 2, 3]
    flags = [0, 1, 2, 3]
    for mo in mode:
        for flag in flags:
            SagSendAT(uart_com, 'AT+SRSPI=%s,%s\r' % (mo, flag))
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
SagSendAT(uart_com, 'AT+SRSPI=0,0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
