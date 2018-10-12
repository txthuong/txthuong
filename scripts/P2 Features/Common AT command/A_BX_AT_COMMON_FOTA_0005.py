# Test Name                             Description
# A_BX_AT_COMMON_FOTA_0005              Check that module can redo FOTA job if it lost power while downloading is in progress
#
# Requirement
#   1 Euler module
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
    SagSendAT(uart_com, "AT+FMM\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(uart_com, "AT+CGSN\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(uart_com, "ATI3\r")
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    fw_current = resp.split('\r\n')[1]
    SagMatchResp(resp, ['\r\n%s\r\nOK\r\n' % fw_current])

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
# A_BX_AT_COMMON_FOTA_0005
# -----------------------------------------------------------------------------------

test_ID = "A_BX_AT_COMMON_FOTA_0005"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Check that module can redo FOTA job if it lost power while downloading is in progress" % test_ID
    print "***********************************************************************************************************************"

    print '\nStep 1: Perform +FOTA command to upgrade with a unsigned FW'
    if fw_current == fw_initial:
        SagSendAT(uart_com, 'AT+FOTA=%s\r' % unsigned_package_url)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagWaitnMatchResp(uart_com, ['\r\n+FOTA: 9,*\r\n'], 10000)
        for iPercent in range (1, 101):
            if not SagWaitnMatchResp(uart_com, ['\r\n+FOTA: 18,%d\r\n' % iPercent], 7000):
                break
        SagWaitnMatchResp(uart_com, ['\r\n+FOTA: 10\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['\r\n+FOTA: 13\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['\r\n+FOTA: 15\r\n'], 10000)
    else:
        raise Exception("---->Problem: The current test FW is not correct !!!")

    print "\nStep 2: Check new update FW"
    SagSendAT(uart_com, "ATI3\r")
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    fw_current = resp.split('\r\n')[1]
    SagMatchResp(resp, ['\r\n%s\r\nOK\r\n' % fw_current])
    if fw_current == fw_initial:
        print '----> OTA update client has finished unsuccessfully with unsigned FW'
    else:
        raise Exception("---->Problem: OTA update client has finished successfully with unsigned FW!!!")

    print "\nTest Steps completed"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT+RST\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

try:

    # Check current revision
    SagSendAT(uart_com, "ATI3\r")
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    fw_current = resp.split('\r\n')[1]
    SagMatchResp(resp, ['\r\n%s\r\nOK\r\n' % fw_current])

    if fw_current != fw_initial:
        SagSendAT(uart_com, 'AT+FOTA=%s\r' % package_url)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagWaitnMatchResp(uart_com, ['\r\n+FOTA: 9,*\r\n'], 10000)
        for iPercent in range (1, 101):
            if not SagWaitnMatchResp(uart_com, ['\r\n+FOTA: 18,%d\r\n' % iPercent], 7000):
                break
        SagWaitnMatchResp(uart_com, ['\r\n+FOTA: 10\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['\r\n+FOTA: 12\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['\r\n+FOTA: 16\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000)
        SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)

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
