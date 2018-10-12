# Test Name                                     Description
# A_BX_EmbeddedSW_KGPIO_0003                    Check if GPIO can set or reset when it is configured no pull mode
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

    # AUX1 Initialization
    print "\nOpen AT Command port"
    aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    # Display DUT information
    print "\nDisplay DUT information"
    print "\nGet model information"
    SagSendAT(aux1_com, 'AT+FMM\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux1_com, 'AT+CGSN\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux1_com, 'ATI3\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_KGPIO_0003
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KGPIO_0003"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check if GPIO can set or reset when it is configured no pull mode" % test_ID
    print "***************************************************************************************************************"

    gpio = [2]

    wx.MessageBox('Connect GPIO %s of 2 mdoules accordantly then click "OK"' % gpio, 'Info',wx.OK)

    for io in gpio:
        print '\nOn DUT'
        print "Step 1: Set GPIO %s as output with no pull mode" % io
        SagSendAT(uart_com, 'AT+KGPIOCFG=%s,0,2\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print '\nOn AUX1'
        print "Step 2: Set GPIO %s as input with pull up resistor" % io
        SagSendAT(aux1_com, 'AT+KGPIOCFG=%s,1,0\r' % io)
        SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

        print '\nOn DUT'
        print "Step 3: Set GPIO %s to LOW" % io
        SagSendAT(uart_com, 'AT+KGPIO=%s,0\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print '\nOn AUX1'
        print "Step 4: Read value of GPIO %s on AUX1" % io
        SagSendAT(aux1_com, 'AT+KGPIO=%s,2\r' % io)
        SagWaitnMatchResp(aux1_com, ['\r\n+KGPIO: %s,0\r\n' % io], 2000)
        SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

        print '\nOn DUT'
        print "Step 5: Set GPIO %s to HIGH" % io
        SagSendAT(uart_com, 'AT+KGPIO=%s,1\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print '\nOn AUX1'
        print "Step 6: Read value of GPIO %s on AUX1" % io
        SagSendAT(aux1_com, 'AT+KGPIO=%s,2\r' % io)
        SagWaitnMatchResp(aux1_com, ['\r\n+KGPIO: %s,1\r\n' % io], 2000)
        SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

        print '\nOn DUT'
        print "Step 7: Set GPIO %s to LOW" % io
        SagSendAT(uart_com, 'AT+KGPIO=%s,0\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print '\nOn AUX1'
        print "Step 8: Read value of GPIO %s on AUX1" % io
        SagSendAT(aux1_com, 'AT+KGPIO=%s,2\r' % io)
        SagWaitnMatchResp(aux1_com, ['\r\n+KGPIO: %s,0\r\n' % io], 2000)
        SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nTest Steps completed"

except Exception, err_msg:
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux1_com, 'AT&F\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nREADY\r\n'], 2000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Close UART
SagClose(uart_com)
# Close AUX1
SagClose(aux1_com)
