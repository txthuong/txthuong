# Test Name                       Description
# A_BX_EmbeddedSW_KGPIO_0005      Check if GPIO level can be changed as the external input level if it is configured as Input and internal pull down resistor
#
# Requirement
#  2 Euler module
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
# A_BX_EmbeddedSW_KGPIO_0005
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KGPIO_0005"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check if GPIO level can be changed as the external input level if it is configured as Input and internal pull down resistor" % test_ID
    print "***************************************************************************************************************"

    gpio = [2]

    wx.MessageBox('Connect GPIO %s of 2 mdoules accordantly then click "OK"' % gpio, 'Info',wx.OK)

    for io in gpio:
        print '\nOn DUT'
        print "Step 1: Set GPIO %s as input with pull down resistor" % io
        SagSendAT(uart_com, 'AT+KGPIOCFG=%s,1,1\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 2: Read input value of GPIO %s" % io
        SagSendAT(uart_com, 'AT+KGPIO=%s,2\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\n+KGPIO: %s,0\r\n' % io], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    for io in gpio:
        print '\nOn AUX1'
        print "Step 3: Set GPIO %s as output with no pull mode" % io
        SagSendAT(aux1_com, 'AT+KGPIOCFG=%s,0,2\r' % io)
        SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 4: Change level GPIO %s of DUT to LOW by driving correspond GPIO of AUX to LOW" % io
        SagSendAT(aux1_com, 'AT+KGPIO=%s,0\r' % io)
        SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

        print '\nOn DUT'
        print "Step 5: Read value of GPIO %s" % io
        SagSendAT(uart_com, 'AT+KGPIO=%s,2\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\n+KGPIO: %s,0\r\n' % io], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print '\nOn AUX1'
        print "Step 6: Change level GPIO %s of DUT to HIGH by driving correspond GPIO of AUX to HIGH" % io
        SagSendAT(aux1_com, 'AT+KGPIO=%s,1\r' % io)
        SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

        print '\nOn DUT'
        print "Step 7: Read value of GPIO %s" % io
        SagSendAT(uart_com, 'AT+KGPIO=%s,2\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\n+KGPIO: %s,1\r\n' % io], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print '\nOn AUX1'
        print "Step 8: Change level GPIO %s of DUT to LOW by driving correspond GPIO of AUX to LOW" % io
        SagSendAT(aux1_com, 'AT+KGPIO=%s,0\r' % io)
        SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

        print '\nOn DUT'
        print "Step 9: Read value of GPIO %s" % io
        SagSendAT(uart_com, 'AT+KGPIO=%s,2\r' % io)
        SagWaitnMatchResp(uart_com, ['\r\n+KGPIO: %s,0\r\n' % io], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

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
