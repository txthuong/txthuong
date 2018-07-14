# Test Name                                     Description
# A_BX_Air_Interface_Band_0001                  BX module should connect to third-party Access Point successfully that is running at 2.4Ghz band
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
    SagWaitnMatchResp(uart_com, ['\r\nREADY\r\n'], 3000)

    # Display DUT information
    print "\nDisplay DUT information"
    print "\nGet model information"
    SagSendAT(uart_com, "AT+FMM\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 3000)

    print "\nGet serial number"
    SagSendAT(uart_com, "AT+CGSN\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 3000)

    print "\nGet revision information"
    SagSendAT(uart_com, "ATI3\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 3000)

    # DUT Initialization
    print "\nInitiate DUT"
    SagSendAT(uart_com, "AT\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_Air_Interface_Band_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_Air_Interface_Band_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: BX module should connect to third-party Access Point successfully that is running at 2.4Ghz band" % test_ID
    print "***************************************************************************************************************"
    
    print "\nStep 1: Configure third party access point works at 2.4GHz\n"
    
    print "\nStep 2: Use module to scan SSID\n"
    SagSendAT(uart_com, "AT+SRWSTASCN\r")
    SagWaitnMatchResp(uart_com, ['*+SRWSTASCN: *,*,*,"%s","%s"\r\n' % (wifi_ssid, wifi_mac_addr)], 10000)
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 10000)
    
    print "\nStep 3: Configure module as Station mode\n"
    SagSendAT(uart_com, "AT+SRWCFG=1\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
    
    print "\nStep 4: Configure the station connection information\n"
    SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s"\r' %(wifi_ssid,wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
    
    print "\nStep 5: Connect to configured Access Point\n"
    SagSendAT(uart_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)

    print "\nStep 6: Disconnect to configured Access Point\n"
    SagSendAT(uart_com, 'AT+SRWSTACON=0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 3000)

    print "\nTest Steps completed\n"

except Exception, err_msg :
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 3000)
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Restore DUT

# Restore Station connection information to default
SagSendAT(uart_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
