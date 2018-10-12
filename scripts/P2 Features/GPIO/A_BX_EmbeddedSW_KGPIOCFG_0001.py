# Test Name                                     Description
# A_BX_EmbeddedSW_KGPIOCFG_0001                 Check syntax for AT+KGPIOCFG command
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
# A_BX_EmbeddedSW_KGPIOCFG_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KGPIOCFG_0001"

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

    print "\nStep 2: Check +KGPIOCFG execute command"
    SagSendAT(uart_com, "AT+KGPIOCFG\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 3: Check +KGPIOCFG read command"
    SagSendAT(uart_com, "AT+KGPIOCFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 4: Check +KGPIOCFG write command with invalid parameter <n>"
    gpio = [-1, 40, 'a', 'A', '*', '#', '!']
    for n in gpio:
        SagSendAT(uart_com, 'AT+KGPIOCFG=%s,0,2\r' % n)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 4: Check +KGPIOCFG write command with invalid parameter <dir>"
    dir = [-1, 2, 'a', 'A', '*', '#', '!']
    for d in dir:
        SagSendAT(uart_com, 'AT+KGPIOCFG=5,%s,2\r' % d)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 5: Check +KGPIOCFG write command with invalid parameter <pull mode>"
    pull_mode = [-1, 3, 'a', 'A', '*', '#', '!']
    for pm in pull_mode:
        SagSendAT(uart_com, 'AT+KGPIOCFG=5,0,%s\r' % pm)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 6: Check +KGPIOCFG write command with missing parameters"
    SagSendAT(uart_com, "AT+KGPIOCFG=\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, "AT+KGPIOCFG=5\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, "AT+KGPIOCFG=5,0\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, "AT+KGPIOCFG=,0\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    SagSendAT(uart_com, "AT+KGPIOCFG=,,2\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 7: Check +KGPIOCFG write command with extra parameter"
    SagSendAT(uart_com, "AT+KGPIOCFG=5,0,2,1\r")
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
