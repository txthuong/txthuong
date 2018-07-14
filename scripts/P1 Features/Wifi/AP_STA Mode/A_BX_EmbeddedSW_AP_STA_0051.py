# Test Name                                     Description
# A_BX_EmbeddedSW_AP_STA_0051                   Check that device configured as Wi-Fi STA has a static IP or get one from DHCP
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
# A_BX_EmbeddedSW_AP_STA_0051
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_AP_STA_0051"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s:Verify <gateway> notification of +SRWSTACON should be correct" % test_ID
    print "*****************************************************************************************************************"
    
    wifi_ssid = 'euler_testing'
    
    print "\nStep 1: Configure Operating Mode of module A as AP and STA concurrent mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG=3\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Query default Operating Mode of module A\n"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWCFG: 3,0,"%s","%s"\r\n' %(dut_mac_address_sta, dut_mac_address)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 4: Setup Access Point mode\n"
    SagSendAT(uart_com, 'AT+SRWAPCFG="%s","%s",4,5,0,100\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Execute command to query current AP configurations\n"
    SagSendAT(uart_com,'AT+SRWAPCFG?\r' )
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPCFG: "%s","%s",4,5,0,100\r\n' %(wifi_ssid, wifi_password)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Enable DHCP with valid values\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG=1,"%s","%s.2","%s.102",720\r' % (wifi_dhcp_gateway, return_subnet(wifi_dhcp_gateway), return_subnet(wifi_dhcp_gateway)))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Query network configuration\n"
    SagSendAT(uart_com,'AT+SRWAPNETCFG?\r' )
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPNETCFG: 1,"%s","%s.2","%s.102",720\r\n' % (wifi_dhcp_gateway, return_subnet(wifi_dhcp_gateway), return_subnet(wifi_dhcp_gateway))], 3000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 8: Enable AUX module as Wi-Fi station\n"
    SagSendAT(aux1_com,'AT+SRWCFG=1\r' )
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 9: Configure the station connection\n"
    SagSendAT(aux1_com,'AT+SRWSTACFG="%s","%s",1\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 10: Set static addresses\n"
    SagSendAT(aux1_com,'AT+SRWSTANETCFG=0,"%s.5","%s","%s"\r' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 11: Connect to Access Point module\n"
    SagSendAT(aux1_com,'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 1,"%s","%s",5,3\r\n' %(wifi_ssid, dut_mac_address)], 3000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTAIP: "%s.5","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 3000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 1,"%s"\r\n' %aux1_mac_address_sta], 3000)
    
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
SagSendAT(aux1_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)
SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 0,"%s"\r\n' %aux1_mac_address_sta], 3000)

# Restore station connection information to default
SagSendAT(aux1_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Restore NET configuration to default
SagSendAT(aux1_com, 'AT+SRWSTANETCFG=1,"0.0.0.0","0.0.0.0","0.0.0.0"\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(aux1_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Restore AP information to default
SagSendAT(uart_com, 'AT+SRWAPCFG="BX31-200A6","eulerxyz",3,1,0,100\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore NET configuration to default
SagSendAT(uart_com, 'AT+SRWAPNETCFG=1,"192.168.4.1","192.168.4.2","192.168.4.101",120\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)

# Close AUX
SagClose(aux1_com)