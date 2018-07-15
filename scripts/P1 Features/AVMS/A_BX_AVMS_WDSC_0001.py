# Test Name                      Description
# A_BX_AVMS_WDSC_0001            To check syntax for WDSC command
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
        raise Exception("---->Problem: Module cannot connect to WIFI !!!")

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_AVMS_WDSC_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_AVMS_WDSC_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: To check syntax for WDSC command' % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Check +WDSC test command"
    SagSendAT(uart_com, 'AT+WDSC=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 2: Check +WDSC execute command"
    SagSendAT(uart_com, "AT+WDSC\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 3: Check +WDSC read command"
    SagSendAT(uart_com, "AT+WDSC?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 2,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 3,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 4,15,60,240,960,2880,10080,10080\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 5,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Check responses of +WDSC command with valid parameters"
    for mode in [0, 1, 2, 3, 5]:
        if mode == 3:
            for state in [1, 525600, 0]:
                SagSendAT(uart_com, "AT+WDSC=%d,%d\r" % (mode, state))
                SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        else:
            for state in [1, 0]:
                SagSendAT(uart_com, "AT+WDSC=%d,%d\r" % (mode, state))
                SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    SagSendAT(uart_com, "AT+WDSC=4,0\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    timer = ['1', '60', '120', '180', '240', '300', '20160']
    for i in range (1, 8):
        command = '4'
        for j in range (0, i):
            command = command + ',' + timer[j]
        SagSendAT(uart_com, 'AT+WDSC=%s\r' % command)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 4000)

    print "\nStep 5: Check responses of +WDSC command with invalid parameters"
    for mode in [0, 1, 2, 3, 4, 5]:
        if mode == 3:
            for state in [-1, 525601, 'a', 'A', '@', '!']:
                SagSendAT(uart_com, "AT+WDSC=%d,%s\r" % (mode, state))
                SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
        elif mode == 4:
            for state in [-1, 20161, 'a', 'A', '@', '!']:
                SagSendAT(uart_com, "AT+WDSC=%d,%s\r" % (mode, state))
                SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
        else:
            for state in [-1, 2, 'a', 'A', '@', '!']:
                SagSendAT(uart_com, "AT+WDSC=%d,%s\r" % (mode, state))
                SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 6: Check responses of +WDSC command with missing parameters"
    for mode in [0, 1, 2, 3, 4, 5]:
        SagSendAT(uart_com, "AT+WDSC=%d\r" % mode)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 7: Check responses of +WDSC command without parameters"
    SagSendAT(uart_com, "AT+WDSC=\r")
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 8: Reset timer to default"
    SagSendAT(uart_com, "AT+WDSC=4,15,60,240,960,2880,10080,10080\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 9: Query Device Services configuration in default"
    SagSendAT(uart_com, "AT+WDSC?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 0,0\r\n'], 2000):
        raise Exception("---->Problem: Failed to test ERROR case !!!")
    if not SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 1,0\r\n'], 2000):
        raise Exception("---->Problem: Failed to test ERROR case !!!")
    if not SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 2,0\r\n'], 2000):
        raise Exception("---->Problem: Failed to test ERROR case !!!")
    if not SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 3,0\r\n'], 2000):
        raise Exception("---->Problem: Failed to test ERROR case !!!")
    if not SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 4,15,60,240,960,2880,10080,10080\r\n'], 2000):
        raise Exception("---->Problem: Failed to test ERROR case !!!")
    if not SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 5,0\r\n'], 2000):
        raise Exception("---->Problem: Failed to test ERROR case !!!")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

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
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
