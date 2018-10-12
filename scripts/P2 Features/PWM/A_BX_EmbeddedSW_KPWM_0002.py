# Test Name                                Description
# A_BX_EmbeddedSW_KPWM_0002                Check that PWM setting can be written and read correctly with both PWM1 and PWM2
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
# A_BX_EmbeddedSW_KPWM_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KPWM_0002"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check that PWM setting can be written and read correctly with both PWM1 and PWM2" % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Check +KPWM default setting"
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Turn ON/OFF PWM 1"
    for operation in (0, 1):
        SagSendAT(uart_com, 'AT+KPWM=1,%s\r' % operation)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KPWM?\r")
        SagWaitnMatchResp(uart_com, ['+KPWM: 1,%s,1000,50\r\n' % operation], 2000)
        SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Turn ON/OFF PWM 1 with <period>"
    for operation in (0, 1):
        for period in (100, 1000, 10000, 100000, 500000):
            SagSendAT(uart_com, 'AT+KPWM=1,%s,%s\r' % (operation, period))
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
            SagSendAT(uart_com, "AT+KPWM?\r")
            SagWaitnMatchResp(uart_com, ['+KPWM: 1,%s,%s,50\r\n' % (operation, period)], 2000)
            SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Turn ON/OFF PWM 1 with <period> and <dutycycle>"
    for operation in (0, 1):
        for period in (100, 1000, 10000, 100000, 500000):
            for dutycycle in (0,10, 25, 50, 75, 90, 100):
                SagSendAT(uart_com, 'AT+KPWM=1,%s,%s,%s\r' % (operation, period, dutycycle))
                SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
                SagSendAT(uart_com, "AT+KPWM?\r")
                SagWaitnMatchResp(uart_com, ['+KPWM: 1,%s,%s,%s\r\n' % (operation, period, dutycycle)], 2000)
                SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
                SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 5: Restore PWM 1 to default"
    SagSendAT(uart_com, 'AT+KPWM=1,0,1000,50\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 6: Turn ON/OFF PWM 2"
    for operation in (0, 1):
        SagSendAT(uart_com, 'AT+KPWM=2,%s\r' % operation)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KPWM?\r")
        SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
        SagWaitnMatchResp(uart_com, ['+KPWM: 2,%s,1000,50\r\n' % operation], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 7: Turn ON/OFF PWM 2 with <period>"
    for operation in (0, 1):
        for period in (100, 1000, 10000, 100000, 500000):
            SagSendAT(uart_com, 'AT+KPWM=2,%s,%s\r' % (operation, period))
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
            SagSendAT(uart_com, "AT+KPWM?\r")
            SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
            SagWaitnMatchResp(uart_com, ['+KPWM: 2,%s,%s,50\r\n' % (operation, period)], 2000)
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 8: Turn ON/OFF PWM 2 with <period> and <dutycycle>"
    for operation in (0, 1):
        for period in (100, 1000, 10000, 100000, 500000):
            for dutycycle in (0,10, 25, 50, 75, 90, 100):
                SagSendAT(uart_com, 'AT+KPWM=2,%s,%s,%s\r' % (operation, period, dutycycle))
                SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
                SagSendAT(uart_com, "AT+KPWM?\r")
                SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
                SagWaitnMatchResp(uart_com, ['+KPWM: 2,%s,%s,%s\r\n' % (operation, period, dutycycle)], 2000)
                SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 9: Restore PWM 2 to default"
    SagSendAT(uart_com, 'AT+KPWM=2,0,1000,50\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
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
