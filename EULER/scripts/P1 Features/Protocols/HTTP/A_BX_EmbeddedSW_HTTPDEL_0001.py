# Test Name                                     Description
# A_BX_EmbeddedSW_HTTPDEL_0001                  Check syntax for AT+KHTTPDEL command
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
# A_BX_EmbeddedSW_HTTPDEL_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_HTTPDEL_0001"
VarGlobal.statOfItem = "OK"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: Check syntax for AT+KHTTPDEL command' % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Configure a HTTP connection"
    SagSendAT(uart_com, 'AT+KHTTPCFG=,%s\r' % http_server)
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Query HTTP connection configuration"
    SagSendAT(uart_com, 'AT+KHTTPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPCFG: 1,,"%s",80,0,,,0,0\r\n' % http_server], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Check +KHTTPDEL test command"
    SagSendAT(uart_com, "AT+KHTTPDEL=?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 4: Check +KHTTPDEL execute command"
    SagSendAT(uart_com, "AT+KHTTPDEL\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 5: Check +KHTTPDEL read command"
    SagSendAT(uart_com, "AT+KHTTPDEL?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 6: Check +KHTTPDEL write command with missing parameter"
    SagSendAT(uart_com, 'AT+KHTTPDEL=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 7: Check +KHTTPDEL write command with extra parameter"
    SagSendAT(uart_com, 'AT+KHTTPDEL=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    print "\nStep 8: Check +KHTTPDEL write command with not configured and out-range session"
    session_id = [-1, 0, 2, 65535, 65536]
    for session in session_id:
        SagSendAT(uart_com, "AT+KHTTPDEL=%s\r" % session)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)

    print "\nStep 9: Check +KHTTPDEL write command with invalid parameter <session_id>"
    session_id = ['a', 'A', '$', '*']
    for session in session_id:
        SagSendAT(uart_com, "AT+KHTTPDEL=%s\r" % session)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 10: Check +KHTTPDEL write command with valid session_id"
    SagSendAT(uart_com, 'AT+KHTTPDEL=1\r')
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
