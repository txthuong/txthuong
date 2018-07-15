# Test Name                                Description
# A_BX_EmbeddedSW_HTTPPOST_0005            Check that +KHTTPPOST can send data to HTTP server in chunked transfer encoding
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
# A_BX_EmbeddedSW_HTTPPOST_0005
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_HTTPPOST_0005"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: Check that +KHTTPPOST can send data to HTTP server in chunked transfer encoding' % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Query HTTP configuration"
    SagSendAT(uart_com, 'AT+KHTTPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Configure a HTTP connection"
    SagSendAT(uart_com, 'AT+KHTTPCFG=,%s\r' % http_server)
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Query HTTP configuration"
    SagSendAT(uart_com, 'AT+KHTTPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPCFG: 1,,"%s",80,0,,,0,0\r\n' % http_server], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Check HTTP Header default state"
    SagSendAT(uart_com, 'AT+KHTTPHEADER?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    data = '1234567890abcdefghijk'

    print "\nStep 5: Set HTTP header field"
    connected = False
    SagSendAT(uart_com, 'AT+KHTTPHEADER=1\r')
    if SagWaitnMatchResp(uart_com, ["\r\nCONNECT\r\n"], 3000):
        connected = True
        SagSendAT(uart_com, 'Content-Length: %d\r\n' % len(data))
        SagSendAT(uart_com,'+++\r')
        resp = SagWaitResp(uart_com, [''], 10000)
        if not SagMatchResp(resp, ["\r\nOK\r\n"]):
            if SagMatchResp(resp, ["*\r\nERROR\r\n", "*\r\n+CME ERROR: *\r\n"]):
                print '\nPROBLEM: HTTP header was not set successfully\n'
            else:
                connected = False

    if not connected:
        print "\nPROBLEM: HTTP Header was not set properly.\n"
        SagSendAT(uart_com, '+++\r')
        SagSleep(1500)
        if not SagWaitnMatchResp(uart_com, ["*\r\nOK\r\n", "*\r\nERROR\r\n", "*\r\n+CME ERROR: *\r\n"], 5000, update_result="not_critical"):
            raise Exception ('\nPROBLEM: +KHTTPHEADER command does not process +++ properly.\n')
        SagSendAT(uart_com, 'AT\r')
        if not SagWaitnMatchResp(uart_com, ["\r\nOK\r\n"], 20000):
            SagSleep(300000)
        raise Exception('\nFailed to execute command +KHTTPHEADER!!!\n')

    print "\nStep 6: Run +KHTTPPOST to send data to HTTP server"
    connected = False
    SagSendAT(uart_com, 'AT+KHTTPPOST=1,"/post"\r')
    if SagWaitnMatchResp(uart_com, ["\r\nCONNECT\r\n"], 20000):
        connected = True
        SagSendAT(uart_com, '%s' % data)
        SagSendAT(uart_com,'+++')
        if SagWaitnMatchResp(uart_com, ["HTTP/1.1 200 OK\r\n"], 30000):
            SagWaitnMatchResp(uart_com, ['*"data":*"%s"' % data], 30000)
            SagWaitnMatchResp(uart_com, ["*\r\nOK\r\n"], 20000)
        else:
            connected = False

    if not connected:
        SagSendAT(uart_com, '+++\r')
        SagSleep(1500)
        if not SagWaitnMatchResp(uart_com, ["*\r\nOK\r\n", "*\r\nERROR\r\n", "*\r\n+CME ERROR: *\r\n"], 5000, update_result="not_critical"):
            raise Exception ('\nPROBLEM: +KHTTPPOST command does not process +++ properly.\n')
        SagSendAT(uart_com, 'AT\r')
        if not SagWaitnMatchResp(uart_com, ["\r\nOK\r\n"], 20000):
            SagSleep(300000)
        raise Exception('\nFailed to execute command +KHTTPPOST!!!\n')

    print "\nStep 7: Close HTTP connection"
    SagSendAT(uart_com, 'AT+KHTTPCLOSE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 8: Query HTTP connection status"
    SagSendAT(uart_com, 'AT+KHTTPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPCFG: 1,,"%s",80,0,,,0,0\r\n' % http_server], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 9: Delete HTTP configuration"
    SagSendAT(uart_com, 'AT+KHTTPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 10: Query HTTP configuration"
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