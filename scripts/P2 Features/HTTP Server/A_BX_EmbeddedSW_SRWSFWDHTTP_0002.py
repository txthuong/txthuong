# Test Name                                     Description
# A_BX_EmbeddedSW_SRWSFWDHTTP_0002              Check URC +SRWS_DATA when enable/disable  forward HTTP requests to host
# 
# Requirement
# 1 Euler module
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

    print "\nGet default AP information"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 3000)
    wifi_mac_addr = resp.split('"')[3]
    SagSendAT(uart_com, 'AT+SRWAPCFG?\r')
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 3000)
    wifi_ssid = resp.split('"')[1]
    wifi_password = resp.split('"')[3]
    SagSendAT(uart_com, 'AT+SRWAPNETCFG?\r')
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 3000)
    wifi_dhcp_gateway = resp.split('"')[1]

    # AUX1 Initialization
    print "\nOpen AT Command port"
    aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    # Display DUT information
    print "\nDisplay DUT information"
    print "\nGet model information"
    SagSendAT(aux1_com, 'AT+FMM\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux1_com, 'AT+CGSN\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux1_com, 'ATI3\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

def send_escape(uart_com):
    SagSleep(1500)
    SagSendAT(uart_com, '+++')
    SagSleep(1500)
    resp = SagWaitResp(uart_com, ['\r\nOK\r\n', '*\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n'], 5000)
    if not SagMatchResp(resp, ['\r\nOK\r\n']):
        if not SagMatchResp(resp, ['*\r\nERROR\r\n', '\r\n+CME ERROR: *\r\n']):
            SagSendAT(uart_com, 'AT\r')
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n', '*\r\nERROR\r\n', "\r\n+CME ERROR: *\r\n"], 5000, update_result="not_critical")

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_SRWSFWDHTTP_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SRWSFWDHTTP_0002"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check URC +SRWS_DATA when enable/disable  forward HTTP requests to host" % test_ID
    print "***********************************************************************************************************************"

    print "\nOn AUX1 ..."
    print "Step 1: Configure WIFI STA to connect to default DUT Access Point"
    SagSendAT(aux1_com, 'AT+SRWSTACFG="%s","%s",1\r' %(wifi_ssid,wifi_password))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Connect to DUT AP"
    SagSendAT(aux1_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(aux1_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: AUX1 module cannot connect to DUT AP !!!")

    print "\nStep 3: Configure a HTTP connection to DUT web server"
    SagSendAT(aux1_com, 'AT+KHTTPCFG=,"%s"\r' % wifi_dhcp_gateway)
    SagWaitnMatchResp(aux1_com, ['\r\n+KHTTPCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nOn DUT ..."
    print "Step 4: Disable forward HTTP requests to host"
    SagSendAT(uart_com, 'AT+SRWSFWDHTTP=0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    data = 'hello'
    json_data = '{"information":{"model":1,"data":"%s"}}' % data

    print "\nOn AUX1 ..."
    print "Step 5: Set HTTP request header"
    SagSendAT(aux1_com, 'AT+KHTTPHEADER=1\r')
    if SagWaitnMatchResp(aux1_com, ['\r\nCONNECT\r\n'], 2000):
        SagSendAT(aux1_com, 'Content-Type: application/json\r\n')
        SagSendAT(aux1_com, 'Content-Length: %d\r\n' % len(json_data))
        send_escape(aux1_com)

    print "\nStep 6: Perform +KHTTPPOST to send data to DUT Web Server"
    SagSendAT(aux1_com, 'AT+KHTTPPOST=1,/bx31api\r')
    if SagWaitnMatchResp(aux1_com, ['\r\nCONNECT\r\n'], 2000):
        SagSendAT(aux1_com, json_data)
        send_escape(aux1_com)

    print "\nOn DUT ..."
    print "Step 7: Check URC +SRWS_DATA"
    SagWaitnMatchResp(uart_com, ['\r\n+SRWS_DATA: %s\r\n' % data], 2000)

    print "\nOn AUX1 ..."
    print "Step 8: Close HTTP connection to DUT web server"
    SagSendAT(aux1_com, 'AT+KHTTPCLOSE=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nOn DUT ..."
    print "Step 9: Enable forward HTTP requests to host"
    SagSendAT(uart_com, 'AT+SRWSFWDHTTP=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nOn AUX1 ..."
    print "Step 10: Set HTTP request header"
    SagSendAT(aux1_com, 'AT+KHTTPHEADER=1\r')
    if SagWaitnMatchResp(aux1_com, ['\r\nCONNECT\r\n'], 2000):
        SagSendAT(aux1_com, 'Content-Type: application/json\r\n')
        SagSendAT(aux1_com, 'Content-Length: %d\r\n' % len(json_data))
        send_escape(aux1_com)

    print "\nStep 11: Perform +KHTTPPOST to send data to DUT Web Server"
    SagSendAT(aux1_com, 'AT+KHTTPPOST=1,/bx31api\r')
    if SagWaitnMatchResp(aux1_com, ['\r\nCONNECT\r\n'], 2000):
        SagSendAT(aux1_com, json_data)
        send_escape(aux1_com)

    print "\nOn DUT ..."
    print "Step 12: Check URC +SRWS_DATA"
    SagWaitnMatchResp(uart_com, ['\r\n+SRWS_DATA: %s.*, "POST HTTP/1.1 Host: %s * %s\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_gateway, json_data)], 2000)

    print "\nOn AUX1 ..."
    print "Step 13: Close HTTP connection to DUT web server"
    SagSendAT(aux1_com, 'AT+KHTTPCLOSE=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 13: Delete the HTTP connection"
    SagSendAT(aux1_com, 'AT+KHTTPDELETE=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

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
SagSendAT(aux1_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)

# Restore station connection information to default
SagSendAT(aux1_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)