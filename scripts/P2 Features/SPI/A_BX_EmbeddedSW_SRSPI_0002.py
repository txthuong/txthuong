# Test Name                                Description
# A_BX_EmbeddedSW_SRSPI_0002               Check that SRSPI write command will be applied on the next reboot and restore to default after AT&F
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
# A_BX_EmbeddedSW_SRSPI_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SRSPI_0002"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check that SRSPI write command will be applied on the next reboot and restore to default after AT&F" % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Check SPI default setting"
    SagSendAT(uart_com, "AT+SRSPI?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRSPI: 0,0'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    mode = [0, 1, 2, 3]
    flags = [0, 1, 2, 3]

    for mo in mode:
        for flag in flags:
            print "\nStep 2: Configure SPI mode and bit numbering: <mode>=%s, <flags>=%s" % (mo, flag)
            SagSendAT(uart_com, 'AT+SRSPI=%s,%s\r' % (mo, flag))
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
            print "\nStep 3: Check SPI setting"
            SagSendAT(uart_com, "AT+SRSPI?\r")
            SagWaitnMatchResp(uart_com, ['\r\n+SRSPI: %s,%s' % (mo, flag)], 2000)
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
            print "\nStep 4: Perform a reboot"
            SagSendAT(uart_com, "AT+RST\r")
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
            SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
            print "\nStep 5: Check SPI setting"
            SagSendAT(uart_com, "AT+SRSPI?\r")
            SagWaitnMatchResp(uart_com, ['\r\n+SRSPI: %s,%s' % (mo, flag)], 2000)
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
            print "\nStep 6: Perform AT&F"
            SagSendAT(uart_com, "AT&F\r")
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
            SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
            print "\nStep 7: Check SPI setting"
            SagSendAT(uart_com, "AT+SRSPI?\r")
            SagWaitnMatchResp(uart_com, ['\r\n+SRSPI: 0,0'], 2000)
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
