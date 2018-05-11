# Test Name                                     Description
# A_BX_EmbeddedSW_HTTPHEAD_0003                 Check that AT+KHTTPHEAD command can access a HTTP server by plain IP address
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

    # DUT Initialization
    print "\nInitiate DUT"
    # Configures module as Station mode
    SagSendAT(uart_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    # Configures the station connection information
    SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s",1\r' %(wifi_ssid,wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    # Connect to configured Access Point
    SagSendAT(uart_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        resp = wait_and_check_ip_address(uart_com, ['\r\n+SRWSTAIP: "192.168.0.*","255.255.255.0","192.168.0.1"\r\n'], 3, 10000)
        SagMatchResp(resp, ['\r\n+SRWSTAIP: "192.168.0.*","255.255.255.0","192.168.0.1"\r\n'])
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_HTTPHEAD_0003
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_HTTPHEAD_0003"
VarGlobal.statOfItem = "OK"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: Check that AT+KHTTPHEAD command can access a HTTP server by plain IP address' % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Query HTTP configuration"
    SagSendAT(uart_com, 'AT+KHTTPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Configure a HTTP connection with plain IP address"
    SagSendAT(uart_com, 'AT+KHTTPCFG=,%s\r' % http_server_ip_addressess)
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Query HTTP configuration"
    SagSendAT(uart_com, 'AT+KHTTPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPCFG: 1,,"%s",80,0,,,0,0\r\n' % http_server_ip_addressessess], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Perform +KHTTPHEAD to HTTP server by plain domain name"
    SagSendAT(uart_com, 'AT+KHTTPHEAD=1,"/"\r')
    SagWaitnMatchResp(uart_com, ['\r\nCONNECT\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['HTTP/1.1 200 OK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nStep 5: Query HTTP connection status"
    SagSendAT(uart_com, 'AT+KHTTPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPCFG: 1,,"%s",80,0,,,1,0\r\n' % http_server_ip_addressessess], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 6: Close HTTP connection"
    SagSendAT(uart_com, 'AT+KHTTPCLOSE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 7: Query HTTP connection status"
    SagSendAT(uart_com, 'AT+KHTTPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPCFG: 1,,"%s",80,0,,,0,0\r\n' % http_server_ip_addressessess], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 8: Delete HTTP configuration"
    SagSendAT(uart_com, 'AT+KHTTPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 9: Query HTTP configuration"
    SagSendAT(uart_com, 'AT+KHTTPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

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
