# Test Name                                     Description
# A_BX_EmbeddedSW_KGPIO_0001                    Check syntax for AT+KGPIO command
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
# A_BX_EmbeddedSW_KGPIO_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KGPIO_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check syntax for AT+KGPIO command" % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Check +KGPIO test command"
    SagSendAT(uart_com, "AT+KGPIO=?\r")
    SagWaitnMatchResp(uart_com, ['+KGPIO: (0-39),(0-2)\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Check +KGPIO execute command"
    SagSendAT(uart_com, "AT+KGPIO\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 3: Check +KGPIO read command"
    SagSendAT(uart_com, "AT+KGPIO?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 4: Check +KGPIO write command with invalid parameter <io>"
    gpio = [20, 24, 28, 29, 30, 31]
    for io in gpio:
        for cde in [0, 1]:
            SagSendAT(uart_com, 'AT+KGPIO=%s,%s\r' % (io, cde))
            SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    gpio = [-1, 40, 'a', 'A', '*', '#', '!']
    for io in gpio:
        for cde in [0, 1, 2]:
            SagSendAT(uart_com, 'AT+KGPIO=%s,%s\r' % (io, cde))
            SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 5: Check +KGPIO write command with invalid parameter <cde>"
    cde = [-1, 3, 'a', 'A', '*', '#', '!']
    for c in cde:
        SagSendAT(uart_com, 'AT+KGPIO=5,%s\r' % c)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 6: Check +KGPIO write command with missing parameters"
    SagSendAT(uart_com, "AT+KGPIO=\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, "AT+KGPIO=5\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, "AT+KGPIO=,0\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, "AT+KGPIO=,1\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, "AT+KGPIO=,2\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 7: Check +KGPIO write command with extra parameter"
    SagSendAT(uart_com, "AT+KGPIO=5,2,1\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    SagSendAT(uart_com, "AT+KGPIO=5,1,1\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    SagSendAT(uart_com, "AT+KGPIO=5,0,1\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    print "\nTest Steps completed"

except Exception, err_msg:
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
