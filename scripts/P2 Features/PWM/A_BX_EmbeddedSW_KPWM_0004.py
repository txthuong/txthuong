# Test Name                                Description
# A_BX_EmbeddedSW_KPWM_0004                Check that all PWM parameters will revert to default after power down
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
    uart_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

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
# A_BX_EmbeddedSW_KPWM_0004
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KPWM_0004"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check that all PWM parameters will revert to default after power down" % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Check +KPWM default setting"
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Turn ON PWM 1"
    SagSendAT(uart_com, 'AT+KPWM=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,1,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Power down module by unplug USB cable, then plug in it"
    wx.MessageBox('Unplug/Plug in USB cable" then click "OK"', 'Info',wx.OK)
    uart_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    print "\nStep 4: Check +KPWM setting after reset"
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 5: Turn ON PWM 2"
    SagSendAT(uart_com, 'AT+KPWM=2,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,1,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 6: Power down module by unplug USB cable, then plug in it"
    wx.MessageBox('Unplug/Plug in USB cable" then click "OK"', 'Info',wx.OK)
    uart_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    print "\nStep 7: Check +KPWM setting after reset"
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 8: Turn ON both PWM 1 and PWM 2"
    SagSendAT(uart_com, 'AT+KPWM=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KPWM=2,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,1,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,1,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 9: Power down module by unplug USB cable, then plug in it"
    wx.MessageBox('Unplug/Plug in USB cable" then click "OK"', 'Info',wx.OK)
    uart_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    print "\nStep 10: Check +KPWM setting after reset"
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    period = 5000
    dutycycle = 40

    print "\nStep 11: Turn ON both PWM 1 and PWM 2 with <period>"
    SagSendAT(uart_com, 'AT+KPWM=1,1,%s\r' % period)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KPWM=2,1,%s\r' % period)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,1,%s,50\r\n' % period], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,1,%s,50\r\n' % period], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 12: Power down module by unplug USB cable, then plug in it"
    wx.MessageBox('Unplug/Plug in USB cable" then click "OK"', 'Info',wx.OK)
    uart_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    print "\nStep 13: Check +KPWM setting after reset"
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,0,1000,50\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 14: Turn ON both PWM 1 and PWM 2 with <period> and <dutycycle>"
    SagSendAT(uart_com, 'AT+KPWM=1,1,%s,%s\r' % (period, dutycycle))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KPWM=2,1,%s,%s\r' % (period, dutycycle))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+KPWM?\r")
    SagWaitnMatchResp(uart_com, ['+KPWM: 1,1,%s,%s\r\n' % (period, dutycycle)], 2000)
    SagWaitnMatchResp(uart_com, ['+KPWM: 2,1,%s,%s\r\n' % (period, dutycycle)], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 15: Power down module by unplug USB cable, then plug in it"
    wx.MessageBox('Unplug/Plug in USB cable" then click "OK"', 'Info',wx.OK)
    uart_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    print "\nStep 16: Check +KPWM setting after reset"
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
