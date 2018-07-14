# Test Name                                     Description
# A_BX_EmbeddedSW_AutoConnect_0001              Check BX module should auto-connect to previous connected Wifi of smartphone when it's powered on
#
# Requirement
#   1 Euler module
#   1 Smartphone
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

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_AutoConnect_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_AutoConnect_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Check BX module should auto-connect to previous connected Wifi of smartphone when it's powered on" % test_ID
    print "***********************************************************************************************************************"

    wifi_ssid = 'Euler_Testing'
    wifi_password = '12345678'

    print "\nStep 1: Start Wifi Hotspot on Smartphone"
    wx.MessageBox('Activate Wifi Hotspot on Smartphone with SSID "%s" and password "%s" then click "OK"' % (wifi_ssid, wifi_password), 'Info',wx.OK)

    print "\nStep 2: Scan WI-FI Hotspot"
    SagSendAT(uart_com, "AT+SRWSTASCN\r")
    SagWaitnMatchResp(uart_com, ['*+SRWSTASCN: *,*,*,"%s","*:*:*:*:*:*"\r\n' % wifi_ssid], 10000)
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 10000)

    print "\nStep 3: Configures module as Station mode"
    SagSendAT(uart_com, "AT+SRWCFG=1\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Configures the station connection information"
    SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s",1\r' % (wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 5: Connect to configured Access Point"
    SagSendAT(uart_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","*:*:*:*:*:*",*,*\r\n' % wifi_ssid], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "192.168.43.*","255.255.255.0","192.168.43.1"\r\n'], 10000)

    print "\nStep 6: Reset module"
    SagSendAT(uart_com, "AT+RST\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*READY\r\n'], 2000)
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","*:*:*:*:*:*",*,*\r\n' % wifi_ssid], 10000):
        SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "192.168.43.*","255.255.255.0","192.168.43.1"\r\n'], 10000)
    else:
        print "Failed to reconnect to Smartphone Hotspot"

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

# Disconnect to configured Access Point
SagSendAT(uart_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)

# Restore station connection information to default
SagSendAT(uart_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
