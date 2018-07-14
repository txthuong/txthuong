# Test Name                                     Description
# A_BX_EmbeddedSW_HTTPSHEADER_0001              Check syntax for AT+HTTPSHEADER command
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
# A_BX_EmbeddedSW_HTTPSHEADER_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_HTTPSHEADER_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: Check syntax for AT+HTTPSHEADER command' % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Query HTTPS connection configuration"
    SagSendAT(uart_com, 'AT+KHTTPSCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Configure a HTTPS connection"
    SagSendAT(uart_com, 'AT+KHTTPSCFG=,%s\r' % https_server)
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Query HTTPS connection configuration"
    SagSendAT(uart_com, 'AT+KHTTPSCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: 1,,"%s",443,0,0,1,,,0,0\r\n' % https_server], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Check +KHTTPSHEADER test command"
    SagSendAT(uart_com, "AT+KHTTPSHEADER=?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 5: Check +KHTTPSHEADER execute command"
    SagSendAT(uart_com, "AT+KHTTPSHEADER\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 6: Check +KHTTPSHEADER read command"
    SagSendAT(uart_com, "AT+KHTTPSHEADER?\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 7: Check +KHTTPSHEADER write command with valid parameters"
    Send_ESC = False
    SagSendAT(uart_com, 'AT+KHTTPSHEADER=1\r')
    if not SagWaitnMatchResp(uart_com, ["\r\nCONNECT\r\n"], 3000):
        print "\nPROBLEM: +KHTTPSHEADER command does not send response CONNECT.\n"
        Send_ESC = True
    if not Send_ESC:
        SagSendAT(uart_com, 'This is header')
        SagSendAT(uart_com,'+++\r')
        if not SagWaitnMatchResp(uart_com, ["\r\nOK\r\n"], 3000):
            print "\nPROBLEM: +KHTTPSHEADER command does not return OK.\n"
            Send_ESC = True
    if Send_ESC:
        SagSendAT(uart_com, '+++\r')
        SagSleep(1500)
        if not SagWaitnMatchResp(uart_com, ["*\r\nOK\r\n", "*\r\nERROR\r\n", "*\r\n+CME ERROR: *\r\n"], 5000, update_result="not_critical"):
            print "\nPROBLEM: +KHTTPSHEADER command does not process +++ properly.\n"

    print "\nStep 8: Check +KHTTPSHEADER write command with missing parameter"
    SagSendAT(uart_com, 'AT+KHTTPSHEADER=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 9: Check +KHTTPSHEADER write command with extra parameter"
    SagSendAT(uart_com, 'AT+KHTTPSHEADER=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    print "\nStep 10: Check +KHTTPSHEADER write command with not configured and out-range session"
    session_id = [-1, 0, 2, 65535, 65536]
    for session in session_id:
        SagSendAT(uart_com, 'AT+KHTTPSHEADER=%s\r' % session)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)

    print "\nStep 11: Check +KHTTPSHEADER write command with invalid parameter <session_id>"
    session_id = ['a', 'A', '$', '*']
    for session in session_id:
        SagSendAT(uart_com, 'AT+KHTTPSHEADER=%s\r' % session)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 12: Query configured header"
    SagSendAT(uart_com, 'AT+KHTTPSHEADER?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSHEADER: 1,14\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['This is header\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 13: Delete HTTPS configuration"
    SagSendAT(uart_com, 'AT+KHTTPSDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 14: Query HTTPS connection configuration"
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
