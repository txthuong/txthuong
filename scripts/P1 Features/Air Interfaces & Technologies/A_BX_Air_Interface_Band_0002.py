# Test Name                        Description
# A_BX_AirInterface_Band_0002      BX module should play the role as Access Point that smart phone can access to
#
# Requirement
#   1 Euler module
#   1 SmartPhone
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
# A_BX_AirInterface_Band_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_AirInterface_Band_0002"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: BX module should play the role as Access Point that smart phone can access to" % test_ID
    print "***********************************************************************************************************************"

    print "\nStep 1: Configures module as Access Point mode\n"
    SagSendAT(uart_com, "AT+SRWCFG=2\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    wifi_ssid = 'Euler_Smartphone'
    wifi_password = '12345678'
    wifi_dhcp_gateway = '192.168.100.1'

    print "\nStep 2: Configures the Access Point information\n"
    SagSendAT(uart_com, 'AT+SRWAPCFG="%s","%s",4,5,0,100\r' % (wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Configures the network for AP interface\n"
    SagSendAT(aux1_com, 'AT+SRWAPNETCFG=1,"%s","%s.2","%s.101",720\r' % (wifi_dhcp_gateway, return_subnet(wifi_dhcp_gateway), return_subnet(wifi_dhcp_gateway)))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    wx.MessageBox('Use SmartPhone to connect to SSID "Euler_Smartphone" then click "OK"', 'Info',wx.OK)

    print "\nStep 4: Check response message on module\n"
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 1,"*:*:*:*:*:*"\r\n'], 2000)

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

# Restore AP information to default
SagSendAT(uart_com, 'AT+SRWAPCFG="BX31-200A6","eulerxyz",3,1,0,100\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore NET configuration to default
SagSendAT(uart_com, 'AT+SRWAPNETCFG=1,"192.168.4.1","192.168.4.2","192.168.4.101",120\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
