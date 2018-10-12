# Test Name                                     Description
# A_BX_EmbeddedSW_SRWSCHGWEB_0002               Check Main page (index.html) can be overwritten properly
# 
# Requirement
# 2 Euler module
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
    SagSendAT(uart_com, 'AT+SRWAPCFG?\r')
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 3000)
    wifi_ssid = resp.split('"')[1]
    wifi_mac_addr = resp.split('"')[3]
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

index = """<!DOCTYPE html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
<h1>Sierra Wireless<h1>
<h2>Configuration page<h2>
<form action="/wifi" method="post">
<div>
<label for="ssid">SSID:</label>
<br/>
<input type="text" id="ssid" name="ssid">
</div>
<div>
<label for="password">Password:</label>
<br/>
<input type="password" id="password" name="password">
</div>
<div class="button">
<button type="submit">Connect</button>
</div>
</form>
</body>
</html>
"""

modified_index = """<!DOCTYPE html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
<h1>Euler Product<h1>
<h2>Configuration page<h2>
<form action="/wifi" method="post">
<div>
<label for="ssid">SSID:</label>
<br/>
<input type="text" id="ssid" name="ssid">
</div>
<div>
<label for="password">Password:</label>
<br/>
<input type="password" id="password" name="password">
</div>
<div class="button">
<button type="submit">Connect</button>
</div>
</form>
</body>
</html>
"""

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_SRWSCHGWEB_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_SRWSCHGWEB_0002"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check Main page (index.html) can be overwritten properly" % test_ID
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
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Perform +KHTTPGET to get index page of DUT Web server"
    SagSendAT(aux1_com, 'AT+KHTTPGET=1,"\"\r')
    SagWaitnMatchResp(aux1_com, ['\r\nCONNECT\r\n'], 3000)
    SagWaitnMatchResp(aux1_com, ['HTTP/1.1 200 OK\r\n'], 3000)
    SagWaitnMatchResp(aux1_com, ['Sierra Wireless'], 3000)
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 3000)

    print "\nStep 5: perform +SRWSCHGWEB to overwrite index page of DUT with the modified one"
    SagSendAT(uart_com, 'AT+SRWSCHGWEB\r')
    SagWaitnMatchResp(uart_com, ['\r\nReady to send file\r\n'], 2000)
    SagSendAT(uart_com, modified_index)
    send_escape(uart_com)

    print "\nStep 6: Perform +KHTTPGET to get index page of DUT Web server"
    SagSendAT(aux1_com, 'AT+KHTTPGET=1,"\"\r')
    SagWaitnMatchResp(aux1_com, ['\r\nCONNECT\r\n'], 3000)
    SagWaitnMatchResp(aux1_com, ['HTTP/1.1 200 OK\r\n'], 3000)
    SagWaitnMatchResp(aux1_com, ['Euler Product'], 3000)
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 3000)

    print "\nStep 7: Close HTTP connection to DUT web server"
    SagSendAT(aux1_com, 'AT+KHTTPCLOSE=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 8: Delete the HTTP connection"
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