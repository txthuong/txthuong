# Test Name                                     Description
# A_BX_EmbeddedSW_KGPIOCFG_0002                 Check +KGPIOCFG with ALL special GPIOs
#
# Requirement
#   1 Euler module
#
# Author: txthuong
#
# Jira ticket:
#
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
# A_BX_EmbeddedSW_KGPIOCFG_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KGPIOCFG_0002"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check syntax for AT+KGPIOCFG command" % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Check +KGPIOCFG test command"
    SagSendAT(uart_com, "AT+KGPIOCFG=?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+KGPIOCFG: (0-39),(0-1),(0-2)\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 2: Check +KGPIOCFG write command with unsupported parameter <n>"
    gpio1 = [20, 24, 28, 29, 30, 31]
    for io in gpio1:
        SagSendAT(uart_com, 'AT+KGPIOCFG=%s,0,2\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
        SagSendAT(uart_com, 'AT+KGPIOCFG=%s,1,0\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
        SagSendAT(uart_com, 'AT+KGPIOCFG=%s,1,1\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    gpio2 = [34, 35, 36, 37, 38, 39]
    for io in gpio2:
        SagSendAT(uart_com, 'AT+KGPIOCFG=%s,0,2\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 3: Check +KGPIOCFG write command with valid parameters"
    gpio1 = gpio1 + [1, 3, 6, 7, 8, 9, 11]
    for io in range(0, 40):
        if io not in gpio1:
            SagSendAT(uart_com, 'AT+KGPIOCFG=%s,1,0\r' % io)
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
            SagSendAT(uart_com, 'AT+KGPIOCFG=%s,1,1\r' % io)
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
            if io not in gpio2:
                SagSendAT(uart_com, 'AT+KGPIOCFG=%s,0,2\r' % io)
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
