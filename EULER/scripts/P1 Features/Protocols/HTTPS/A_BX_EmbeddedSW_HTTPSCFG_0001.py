# Test Name                                     Description
# A_BX_EmbeddedSW_HTTPSCFG_0001                 Check syntax for AT+KHTTPSCFG command
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
# A_BX_EmbeddedSW_HTTPSCFG_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_HTTPSCFG_0001"
VarGlobal.statOfItem = "OK"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check syntax for AT+KHTTPSCFG command" % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Check +KHTTPSCFG test command\n"
    SagSendAT(uart_com, "AT+KHTTPSCFG=?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 2: Check +KHTTPSCFG execute command\n"
    SagSendAT(uart_com, "AT+KHTTPSCFG\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 3: Check +KHTTPSCFG read command\n"
    SagSendAT(uart_com, "AT+KHTTPSCFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    session_id = 1
    print "\nStep 4: Check +KHTTPSCFG write command\n"
    http_server = ['www.google.com', 'httpbin.org', '116.66.221.42']
    for server in http_server:
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,%s\r' % server)
        SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KHTTPSCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KHTTPSCFG: %d,,"%s",443,0,0,1,,,0,0\r\n' % (session_id, server)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        session_id = session_id + 1

    print "\nStep 5: Check +KHTTPSCFG write command with parameter <http_port>\n"
    http_port = [1, 80, 144, 2347, 8081, 16718, 39952, 65535]
    for port in http_port:
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,httpbin.org,%s\r' % port)
        SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KHTTPSCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KHTTPSCFG: %d,,"httpbin.org",%d,0,0,1,,,0,0\r\n' % (session_id, port)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        session_id = session_id + 1

    print "\nStep 6: Check +KHTTPSCFG write command with parameter <http_version>\n"
    http_version = [0, 1]
    for ver in http_version:
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,httpbin.org,443,%s\r' % ver)
        SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KHTTPSCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KHTTPSCFG: %d,,"httpbin.org",443,%d,0,1,,,0,0\r\n' % (session_id, ver)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        session_id = session_id + 1

    print "\nStep 7: Check +KHTTPSCFG write command with parameter <cipher_suite>\n"
    cipher_suite = [0, 1, 2, 3, 4, 5, 6, 7]
    for cs in cipher_suite:
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,httpbin.org,443,0,%s\r' % cs)
        SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KHTTPSCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KHTTPSCFG: %d,,"httpbin.org",443,0,%s,1,,,0,0\r\n' % (session_id, cs)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        session_id = session_id + 1

    print "\nStep 8: Check +KHTTPSCFG write command with parameter <sec_level>\n"
    sec_level = [1, 2, 3]
    for sec in sec_level:
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,httpbin.org,443,0,0,%s\r' % sec)
        SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KHTTPSCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KHTTPSCFG: %d,,"httpbin.org",443,0,0,%s,,,0,0\r\n' % (session_id, sec)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        session_id = session_id + 1

    print "\nStep 9: Check +KHTTPSCFG write command with parameter <login>\n"
    login = ['euler', 'euler@euler', 'euler123']
    for user in login:
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,httpbin.org,443,0,0,1,%s\r' % user)
        SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KHTTPSCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KHTTPSCFG: %d,,"httpbin.org",443,0,0,1,"%s",,0,0\r\n' % (session_id, user)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        session_id = session_id + 1

    print "\nStep 10: Check +KHTTPSCFG write command with parameter <password>\n"
    password = ['123', '12345678x@Xr', '1_Abc_123']
    for pw in password:
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,httpbin.org,443,0,0,1,euler,%s\r' % pw)
        SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KHTTPSCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KHTTPSCFG: %d,,"httpbin.org",443,0,0,1,"euler","%s",0,0\r\n' % (session_id, pw)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        session_id = session_id + 1

    print "\nDelete all HTTPS configurations\n"
    for i in range (1, session_id):
        SagSendAT(uart_com, 'AT+KHTTPSDEL=%d\r' % i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 11: Check +KHTTPSCFG write command with invalid parameter <http_server>\n"
    http_server = ['512.-1.-255.256', 'httpbin.org"', 'www.kernel.org/space%20here.html', '"www.kernel.org"-1-1-1-1-1-1-1']
    for server in http_server:
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,%s\r' % server)
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 12: Check +KHTTPSCFG write command with invalid parameter <http_port>\n"
    http_port = [-1, 65536, 'a', '*']
    for port in http_port:
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,httpbin.org,%s\r' % port)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 13: Check +KHTTPSCFG write command with invalid parameter <http_version>\n"
    http_version = [-1, 2, 'a', '*']
    for ver in http_version:
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,httpbin.org,443,%s\r' % ver)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 14: Check +KHTTPSCFG write command with invalid parameter <cipher_suite>\n"
    cipher_suite = [-1, 8, 'a', '*']
    for cs in cipher_suite:
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,httpbin.org,443,0,%s\r' % cs)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 15: Check +KHTTPSCFG write command with invalid parameter <sec_level>\n"
    sec_level = [-1, 0, 4, 'a', '*']
    for sec in sec_level:
        SagSendAT(uart_com, 'AT+KHTTPSCFG=,httpbin.org,443,0,0,%s\r' % sec)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 16: Check +KHTTPSCFG write command with invalid parameter <login>\n"
    login = '"euler'
    SagSendAT(uart_com, 'AT+KHTTPSCFG=,httpbin.org,443,0,%s\r' % login)
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 17: Check +KHTTPSCFG write command with invalid parameter <password>\n"
    password = '123"'
    SagSendAT(uart_com, 'AT+KHTTPSCFG=,httpbin.org,443,0,euler,%s\r' % password)
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 18: Query HTTPS configuration"
    SagSendAT(uart_com, "AT+KHTTPSCFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: Failed to test ERROR cases !!!")

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