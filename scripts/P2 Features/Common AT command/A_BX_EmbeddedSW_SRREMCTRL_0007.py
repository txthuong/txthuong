# Test Name                            Description
# A_BX_EmbeddedSW_SRREMCTRL_0007       Check that remote control will return to disable after AT+RST or factory reset
#
# Requirement
#   2 Euler module
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
    SagSendAT(uart_com, "AT+FMM\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(uart_com, "AT+CGSN\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(uart_com, "ATI3\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet BlueTooth address"
    SagSendAT(uart_com, "AT+SRBTADDR?\r")
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    SagMatchResp(resp, ['*\r\nOK\r\n'])
    dut_bluetooth_address = resp.split('"')[1]

    print "\nGet BLE configure"
    SagSendAT(uart_com, "AT+SRBLE?\r")
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    dut_bt_name = resp.split('"')[1]
    dut_max_mtu = resp.split(',')[1]

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_SRREMCTRL_0007
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SRREMCTRL_0007"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Check that remote control will return to disable after AT+RST or factory reset" % test_ID
    print "***********************************************************************************************************************"

    print '\nStep 1: Get remote controller'
    SagSendAT(uart_com, 'AT+SRREMCTRL?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRREMCTRL: 0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    session = 1

    print '\nStep 2: Enable remote controll with session id %s' % session
    SagSendAT(uart_com, 'AT+SRREMCTRL=%s\r' % session)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 3: Get remote controller'
    SagSendAT(uart_com, 'AT+SRREMCTRL?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRREMCTRL: %s\r\n' % session], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 4: Perform AT+RST'
    SagSendAT(uart_com, 'AT+RST\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)

    print '\nStep 5: Get remote controller'
    SagSendAT(uart_com, 'AT+SRREMCTRL?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRREMCTRL: 0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 6: Enable remote controll with session id %s' % session
    SagSendAT(uart_com, 'AT+SRREMCTRL=%s\r' % session)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 7: Get remote controller'
    SagSendAT(uart_com, 'AT+SRREMCTRL?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRREMCTRL: %s\r\n' % session], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 8: Perform factory reset'
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)

    print '\nStep 9: Get remote controller'
    SagSendAT(uart_com, 'AT+SRREMCTRL?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRREMCTRL: 0\r\n'], 2000)
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
