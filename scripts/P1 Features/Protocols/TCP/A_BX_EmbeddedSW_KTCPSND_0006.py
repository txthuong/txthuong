# Test Name                                   Description
# A_BX_EmbeddedSW_KTCPSND_0006                To check data can be sent to HTTP server
#
# Requirement
#   1 Euler modules
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
        resp = SagWaitResp(uart_com, ['\r\n+SRWSTAIP: *\r\n'], 10000)
        dut_ip_address = resp.split('"')[1]
        SagMatchResp(resp, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)])
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
# A_BX_EmbeddedSW_KTCPSND_0006
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KTCPSND_0006"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: To check data can be sent to HTTP server"' % test_ID
    print "***************************************************************************************************************"

    http_server = 'www.wavecom.com'
    http_port = 80

    print '\nStep 1: Configure a TCP connection'
    SagSendAT(uart_com, 'AT+KTCPCFG=,0,"%s",%s\r' % (http_server, http_port))
    SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: 1\r\n'], 3000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)

    print '\nStep 2: Start TCP Connection'
    SagSendAT(uart_com, 'AT+KTCPCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 3: Query TCP Connection'
    SagSendAT(uart_com, 'AT+KTCPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: 1,1,,2,1,"%s",*,%s,1,0\r\n' % (tcp_server, tcp_port)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    data = '1234567890\03'

    print '\nStep 4: Send data to HTTP server'
    SagSendAT(uart_com, 'AT+KTCPSND=1,"%s"\r' % data)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_DATA: 1,*,*\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+KTCP_NOTIF: 1,4\r\n'], 10000)

    print '\nStep 5: Close TCP session'
    SagSendAT(uart_com, 'AT+KTCPCLOSE=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 6: Delete TCP connection'
    SagSendAT(uart_com, 'AT+KTCPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 7: Query TCP connection'
    SagSendAT(uart_com, 'AT+KTCPCFG?\r')
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: TCP configure was not deleted properly !!!")

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
SagSendAT(uart_com, 'AT+SRWCFG=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
