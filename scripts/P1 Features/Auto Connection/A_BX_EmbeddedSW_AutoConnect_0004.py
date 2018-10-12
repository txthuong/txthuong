# Test Name                                     Description
# A_BX_EmbeddedSW_AutoConnect_0004              Check BX module should auto-connect to Wifi of other Euler module when it's powered on
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

    # AUX Initialization
    print "\nOpen AT Command port"
    aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    # Display DUT information
    print "\nDisplay AUX information"
    print "\nGet model information"
    SagSendAT(aux1_com, "AT+FMM\r")
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux1_com, "AT+CGSN\r")
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux1_com, "ATI3\r")
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_AutoConnect_0004
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_AutoConnect_0004"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Check BX module should auto-connect to Wifi of other Euler module when it's powered on" % test_ID
    print "***********************************************************************************************************************"

    wifi_ssid = 'Euler_Testing'
    wifi_password = '123456789'
    wifi_dhcp_gateway = '192.168.100.1'

    print "\nStep 1: Configures module AUX as Access Point mode"
    SagSendAT(aux1_com, "AT+SRWCFG=2\r")
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Configures the Access Point information"
    SagSendAT(aux1_com, 'AT+SRWAPCFG="%s","%s",4\r' % (wifi_ssid, wifi_password))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Configures the network for AP interface"
    SagSendAT(aux1_com, 'AT+SRWAPNETCFG=1,"%s","%s.2","%s.101",720\r' % (wifi_dhcp_gateway, return_subnet(wifi_dhcp_gateway), return_subnet(wifi_dhcp_gateway)))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Scan SSID"
    SagSendAT(uart_com, "AT+SRWSTASCN\r")
    response = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 10000)

    if '"%s"' % wifi_ssid not in response:
        raise Exception("----> Problem: Cannot find AUX Access Point !!!")
    else:
        print '\nFound Euler AP: "%s"' % wifi_ssid

    print "\nStep 5: Configures module as Station mode"
    SagSendAT(uart_com, "AT+SRWCFG=1\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 6: Configures the station connection information"
    SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s",1\r' % (wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 7: Connect to configured Access Point"
    SagSendAT(uart_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","*:*:*:*:*:*",*,*\r\n' % wifi_ssid], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","255.255.255.0","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_gateway)], 10000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWAPSTA: 1,"*:*:*:*:*:*"\r\n'], 10000)

    print "\nStep 8: Reset module"
    SagSendAT(uart_com, "AT+RST\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*READY\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWAPSTA: 0,"*:*:*:*:*:*"\r\n'], 10000)
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","*:*:*:*:*:*",*,*\r\n' % wifi_ssid], 10000):
        SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","255.255.255.0","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_gateway)], 10000)
    else:
        print "Failed to reconnect to AUX Access Point"
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWAPSTA: 1,"*:*:*:*:*:*"\r\n'], 10000)

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
SagWaitnMatchResp(aux1_com, ['\r\n+SRWAPSTA: 0,"*:*:*:*:*:*"\r\n'], 10000)

# Restore station connection information to default
SagSendAT(uart_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore AP information to default
SagSendAT(aux1_com, 'AT+SRWAPCFG="BX31-200A6","eulerxyz",3,1,0,100\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Restore NET configuration to default
SagSendAT(aux1_com, 'AT+SRWAPNETCFG=1,"192.168.4.1","192.168.4.2","192.168.4.101",120\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(aux1_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)

# Close AUX
SagClose(aux1_com)