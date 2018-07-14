# Test Name                              Description
# A_BX_EmbeddedSW_HTTPSDELETE_0015       Check that +KHTTPSDELETE does not work with a server by unsupported <cipher_suite>
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
# A_BX_EmbeddedSW_HTTPSDELETE_0015
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_HTTPSDELETE_0015"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: Check that +KHTTPSDELETE does not work with a server by unsupported <cipher_suite>' % test_ID
    print "***************************************************************************************************************"

    # -------------------------- Start HTTPS server --------------------------------

    tn = TelnetUtil()
    # Open a telnet session
    dest = tn.open_telnet_session(https_server_addr_telnet,https_server_telnet_port,https_server_telnet_login,https_server_telnet_password)
    # Start HTTPS service
    tn.stop_https(dest, https_port)
    SagSleep(5000)
    https_cmd = 'cmd /c start python httpsd.py -x ./server.pem -c NULL-MD5 -p '+str(https_port)
    tn.send_cmd(dest, 'cd '+https_server_httpsd_dir)
    SagSleep(1000)
    tn.send_cmd(dest, https_cmd)
    SagSleep(5000)

    # ------------------------------------------------------------------------------

    print "\nStep 1: Query HTTPS configuration"
    SagSendAT(uart_com, 'AT+KHTTPSCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    all_cipher_suite = (0,1,2,3,4,5,6,7)

    print "\nCheck that +KHTTPSDELETE does not work with a server by unsupported <cipher_suite>"
    for cipher_suite in all_cipher_suite:
        print "\nStep 2: Setting +KHTTPSCFG with <cipher_suite>: %d..." % cipher_suite
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,%s,%s,1,%d\r' % (https_server2, https_port, cipher_suite))
        SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: 1\r\n'], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 3: Query HTTPS configuration"
        SagSendAT(uart_com, 'AT+KHTTPSCFG?\r')
        SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: 1,,"%s",%s,1,%d,1,,,0,0\r\n' % (https_server2, https_port, cipher_suite)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 4: Running +KHTTPSDELETE with <cipher_suite> %d..." % cipher_suite
        SagSendAT(uart_com, 'AT+KHTTPSDELETE=1,"/"\r')
        SagWaitnMatchResp(uart_com, ['\r\n+KHTTPS_ERROR: 1,12\r\n\r\nERROR\r\n'], 10000)
        print "\nQuery HTTPS connection status"
        SagSendAT(uart_com, 'AT+KHTTPSCFG?\r')
        if not SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: 1,,"%s",%s,1,%d,1,,,0,0\r\n' % (https_server2, https_port, cipher_suite)], 2000):
            print 'Problem: +KHTTPSDELETE work with server by unsupported cipher suite !!!\n'
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
