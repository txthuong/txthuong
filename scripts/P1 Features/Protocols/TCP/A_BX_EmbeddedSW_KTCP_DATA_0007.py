# Test Name                                     Description
# A_BX_EmbeddedSW_KTCP_DATA_0007                To check URC "+KTCP_DATA"  with <data> is received correctly when the module receives 10KB data from server
#
# Requirement
#   2 Euler modules
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

    # AUX1_UART Initialization
    print "\nOpen AT Command port"
    aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    # Display AUX1 information
    print "\nDisplay AUX1 information"
    print "\nGet model information"
    SagSendAT(aux1_com, 'AT+FMM\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nGet serial number"
    SagSendAT(aux1_com, 'AT+CGSN\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux1_com, 'ATI3\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    # DUT Initialization
    print "\nInitiate DUT"
    # Configures module as Station mode
    SagSendAT(aux1_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    # Configures the station connection information
    SagSendAT(aux1_com, 'AT+SRWSTACFG="%s","%s",1\r' %(wifi_ssid,wifi_password))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    # Connect to configured Access Point
    SagSendAT(aux1_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(aux1_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        resp = SagWaitResp(aux1_com, ['\r\n+SRWSTAIP: *\r\n'], 10000)
        aux1_ip_address = resp.split('"')[1]
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
# A_BX_EmbeddedSW_KTCP_DATA_0007
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KTCP_DATA_0007"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: To check URC "+KTCP_DATA"  with <data> is received correctly when the module receives 10KB data from server' % test_ID
    print "***************************************************************************************************************"

    aux1_tcp_port = '1234'

    print '\nOn AUX1...'
    print 'Step 1: Configure a TCP server'
    SagSendAT(aux1_com, 'AT+KTCPCFG=,1,,%s\r' % aux1_tcp_port)
    SagWaitnMatchResp(aux1_com, ['\r\n+KTCPCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 2: Start TCP server\n'
    SagSendAT(aux1_com, 'AT+KTCPCNX=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nOn DUT...'
    print 'Step 3: Configure a TCP connection to AUX1 TCP Server'
    SagSendAT(uart_com, 'AT+KTCPCFG=,0,"%s",%s\r' % (aux1_ip_address, aux1_tcp_port))
    SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: 1\r\n'], 3000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)

    print '\nStep 4: Start TCP Connection'
    SagSendAT(uart_com, 'AT+KTCPCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    resp = SagWaitResp(aux1_com, ['\r\n+KTCP_SRVREQ: *\r\n'], 5000)
    dut_tcp_port = resp.split(',')[3].split('\r')[0]
    SagMatchResp(resp, ['\r\n+KTCP_SRVREQ: 1,2,"%s",%s\r\n' % (dut_ip_address, dut_tcp_port)])

    print '\nOn AUX1...'
    print '\nStep 5: Query TCP Connection'
    SagSendAT(aux1_com, 'AT+KTCPCFG?\r')
    SagWaitnMatchResp(aux1_com, ['\r\n+KTCPCFG: 1,1,,1,"",%s,,1,0\r\n' % aux1_tcp_port], 2000)
    SagWaitnMatchResp(aux1_com, ['+KTCPCFG: 2,1,,2,1,"%s",%s,%s,1,0\r\n' % (dut_ip_address, dut_tcp_port, aux1_tcp_port)], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)

    data = '0123456789'

    while len(data) < 10000:
        data += data

    print '\nStep 6: Send 10Kb data to DUT CLIENT'
    SagSendAT(aux1_com, 'AT+KTCPSTART=2\r')
    SagWaitnMatchResp(aux1_com, ['\r\nCONNECT\r\n'], 2000)
    SagSendAT(aux1_com, data)
    SagSendAT(aux1_com, '+++')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nOn DUT...'
    print 'Step 7: Check URC "+KTCP_DATA" is received'
    receive_data = ''
    while True:
        resp = SagWaitResp(uart_com, ['\r\n+KTCP_DATA: 1,*,*\r\n'], 2000)
        if not SagMatchResp(resp, ['\r\n+KTCP_DATA: 1,*,*\r\n']):
            break
        else:
            receive_data += resp.split(',')[2].split('\r')[0]

    if receive_data == data:
        print '----> Data is received correctly !!!'
    else:
        print '----> Problem: Data is received incorrectly !!!'
        VarGlobal.statOfItem = "NOK"

    print '\nStep 8: Close TCP session'
    print 'On DUT...'
    SagSendAT(uart_com, 'AT+KTCPCLOSE=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    #SagWaitnMatchResp(aux1_com, ['\r\n+KTCP_NOTIF: 2,4\r\n'], 2000)
    print 'On AUX1...'
    SagSendAT(aux1_com, 'AT+KTCPCLOSE=1,0\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(aux1_com, 'AT+KTCPCLOSE=2,1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 9: Delete TCP connection'
    print '\nOn DUT...'
    SagSendAT(uart_com, 'AT+KTCPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    print '\nOn AUX1...'
    SagSendAT(aux1_com, 'AT+KTCPDEL=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(aux1_com, 'AT+KTCPDEL=2\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 10: Query TCP connection'
    SagSendAT(uart_com, 'AT+KTCPCFG?\r')
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: TCP configure was not deleted properly !!!")
    SagSendAT(aux1_com, 'AT+KTCPCFG?\r')
    if not SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: TCP configure was not deleted properly !!!")

    print "\nTest Steps completed"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux1_com, 'AT&F\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nREADY\r\n'], 2000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Disconnect to configured Access Point
SagSendAT(uart_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)
SagSendAT(aux1_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)

# Restore station connection information to default
SagSendAT(uart_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, 'AT+SRWCFG=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
SagClose(aux1_com)