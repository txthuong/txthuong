# Test Name                                     Description
# A_BX_EmbeddedSW_Disablemode_0001              Configures the module's WIFI mode in Disabled mode
#
# Requirement
# 2 Euler modules
#  
# Author: ptnlam
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
    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nQuery WIFI configuration"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    dut_mac_address_sta = resp.split('"')[1]
    dut_mac_address = resp.split('"')[3]
    SagMatchResp(resp, ['\r\n+SRWCFG: 3,0,"%s","%s"\r\nOK\r\n' %(dut_mac_address_sta, dut_mac_address)])

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

    print "\nQuery WIFI configuration"
    SagSendAT(aux1_com, 'AT+SRWCFG?\r')
    resp = SagWaitResp(aux1_com, ['*\r\nOK\r\n'], 2000)
    aux1_mac_address_sta = resp.split('"')[1]
    aux1_mac_address = resp.split('"')[3]
    SagMatchResp(resp, ['\r\n+SRWCFG: 3,0,"%s","%s"\r\nOK\r\n' %(aux1_mac_address_sta, aux1_mac_address)])

    # AUX1 Initialization
    print "\nInitiate AUX1"
    SagSendAT(aux1_com, 'AT\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_Disablemode_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_Disablemode_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s:Configures the module's WIFI mode in Disabled mode " % test_ID
    print "*****************************************************************************************************************"

    print "\nStep 1: Query default AP NET configure"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG?\r')
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    wifi_dhcp_gateway = resp.split('"')[1]
    SagMatchResp(resp, ['\r\n+SRWAPNETCFG: 1,"%s","%s.2","%s.101",120\r\nOK\r\n' %(wifi_dhcp_gateway, return_subnet(wifi_dhcp_gateway), return_subnet(wifi_dhcp_gateway))])

    print "\nStep 2: Query default AP configure"
    SagSendAT(uart_com, 'AT+SRWAPCFG?\r')
    resp = SagWaitResp(uart_com, ['*\r\nOK\r\n'], 2000)
    wifi_ssid = resp.split('"')[1]
    wifi_password = resp.split('"')[3]
    SagMatchResp(resp, ['\r\n+SRWAPCFG: "%s","%s",3,1,0,100\r\nOK\r\n' %(wifi_ssid, wifi_password)])

    print "\nStep 3: Use another module to connect to this Access Point\n"
    SagSendAT(aux1_com, 'AT+SRWSTACFG="%s","%s",1\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Connect to Access Point\n"
    SagSendAT(aux1_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(aux1_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, dut_mac_address)], 20000):
        SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 1,"%s"\r\n' % aux1_mac_address_sta], 2000)

    print "\nStep 5: Execute command to change module state as Disable mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG=0\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 0,"%s"\r\n' % aux1_mac_address_sta], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 0,4\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 0,202\r\n'], 3000)

    print "\nStep 6: Check that AUX module unable to reconnect to WIFI AP"
    for i in range(0, 5):
        SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 0,201\r\n'], 10000)

    print "\nStep 7: Disconnect to WIFI AP"
    SagSendAT(aux1_com, 'AT+SRWSTACON=0\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    print "\nTest Steps completed\n"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux1_com, 'AT&F\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nREADY\r\n'], 2000)

#Print test result.

PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Restore station connection information to default
SagSendAT(aux1_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(aux1_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

