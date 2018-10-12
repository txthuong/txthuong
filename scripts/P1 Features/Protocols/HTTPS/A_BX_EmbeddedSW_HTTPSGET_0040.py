# Test Name                              Description
# A_BX_EmbeddedSW_HTTPSGET_0040          Check that +KHTTPSGET works with a server by <cipher_suite> TLS_RSA_WITH_AES_256_CBC_SHA256
#
# Requirement
#   1 Euler module
#   1 AP running at 2.4GHz band
#   1 HTTPS server supports TLS_RSA_WITH_AES_256_CBC_SHA256
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
        SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
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
# A_BX_EmbeddedSW_HTTPSGET_0040
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_HTTPSGET_0040"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: Check that +KHTTPSGET works with a server by <cipher_suite> TLS_RSA_WITH_AES_256_CBC_SHA256' % test_ID
    print "***************************************************************************************************************"

    # -------------------------- Start HTTPS server --------------------------------

    tn = TelnetUtil()
    # Open a telnet session
    dest = tn.open_telnet_session(https_server_addr_telnet,https_server_telnet_port,https_server_telnet_login,https_server_telnet_password)
    tn.stop_https(dest, int(https_port))
    SagSleep(5000)
    # Start HTTPS service
    https_cmd = 'cmd /c start httpd -f conf/httpd-TLS_RSA_WITH_AES_256_CBC_SHA256.conf'
    tn.send_cmd(dest, 'cd '+https_server_httpsd_dir)
    SagSleep(1000)
    tn.send_cmd(dest, https_cmd)
    SagSleep(5000)

    # ------------------------------------------------------------------------------

    print "\nStep 1: Query HTTPS configuration"
    SagSendAT(uart_com, 'AT+KHTTPSCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    supported_cipher_suite = (0, 43)

    print "\nCheck that +KHTTPSGET works with HTTPS server supported <cipher_suite> TLS_RSA_WITH_AES_256_CBC_SHA256"
    for cipher_suite in range(0, 79):
        print "\nStep 2: Setting +KHTTPSCFG with <cipher_suite>: %d..." % cipher_suite
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,%s,%s,1,%d\r' % (https_server2, https_port, cipher_suite))
        SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: 1\r\n'], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 3: Query HTTPS configuration"
        SagSendAT(uart_com, 'AT+KHTTPSCFG?\r')
        SagWaitnMatchResp(uart_com, ['+KHTTPSCFG: 1,,"%s",%s,1,%d,1,,,0,0,2,2\r\n' % (https_server2, https_port, cipher_suite)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 4: Perform +KHTTPSGET with <cipher_suite> %d..." % cipher_suite
        SagSendAT(uart_com, 'AT+KHTTPSGET=1,"/"\r')
        if cipher_suite in supported_cipher_suite:
            SagWaitnMatchResp(uart_com, ['\r\nCONNECT\r\n'], 5000)
            SagWaitnMatchResp(uart_com, ['HTTP/1.1 200 OK\r\n'], 5000)
            SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 5000)
            print "\nQuery HTTPS connection status"
            SagSendAT(uart_com, 'AT+KHTTPSCFG?\r')
            SagWaitnMatchResp(uart_com, ['+KHTTPSCFG: 1,,"%s",%s,1,%d,1,,,1,0,2,2\r\n' % (https_server2, https_port, cipher_suite)], 2000)
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
            print "\nClose HTTPS connection"
            SagSendAT(uart_com, "AT+KHTTPSCLOSE=1\r")
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        else :
            SagWaitnMatchResp(uart_com, ['\r\n+KHTTPS_ERROR: 1,12\r\n\r\nERROR\r\n'], 7000)
            print "\nQuery HTTPS connection status"
            SagSendAT(uart_com, 'AT+KHTTPSCFG?\r')
            if not SagWaitnMatchResp(uart_com, ['+KHTTPSCFG: 1,,"%s",%s,1,%d,1,,,0,0,2,2\r\n' % (https_server2, https_port, cipher_suite)], 2000):
                print 'Problem: +KHTTPSGET works with server by unsupported <cipher_suite> !!!\n'
                SagSendAT(uart_com, "AT+KHTTPSCLOSE=1\r")
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 5: Delete the HTTPS connection"
        SagSendAT(uart_com, 'AT+KHTTPSDEL=1\r')
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 6: Query HTTPS configuration"
    SagSendAT(uart_com, 'AT+KHTTPSCFG?\r')
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

# Stop HTTPS service
tn.stop_https(dest, int(https_port))

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
