# Test Name                                     Description
# A_BX_EmbeddedSW_KUDP_DATA_0008                To check when <data_mode> was set to 1, the max  length <data> can send  is 218, and  all received data shall be complete and consistent
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
# A_BX_EmbeddedSW_KUDP_DATA_0008
# -----------------------------------------------------------------------------------
    
test_ID = "A_BX_EmbeddedSW_KUDP_DATA_0008"

#######################################################################################
#   START
#######################################################################################
    
try:
    
    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")
    
    print "***************************************************************************************************************"
    print "%s:To check +KUDP_DATA can be received in UDP client to indicate there are incoming data" % test_ID
    print "***************************************************************************************************************"
    
    print '\nStep 1: Configure modules work as Station mode\n'
    SagSendAT(uart_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 2: Connect to the Wi-Fi network\n'
    SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s"\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+SRWSTACFG="%s","%s"\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 3: Activate Station connection\n'
    SagSendAT(uart_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        response1 = SagWaitResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
        
    SagMatchResp(response1, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)])
    uart_UDP_ip=response1.split('"')[1]
    
    SagSendAT(aux1_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(aux1_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        response2 = SagWaitResp(aux1_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
        
    SagMatchResp(response2, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)])
    aux1_UDP_ip=response2.split('"')[1]
    
    print '\nStep 4: DUT: UDP Server Connection Configuration with <data_mode>=1\n'
    SagSendAT(uart_com, 'AT+KUDPCFG=,1,1234,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KUDPCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 5: DUT: Display IP Address of the current connection\n'
    SagSendAT(uart_com, 'AT+SRWSTACON?\r')
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        response1 = SagWaitResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 6: DUT: Checking UDP Connection Configuration\n'
    SagSendAT(uart_com, 'AT+KUDPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KUDPCFG: 1,,1,1234,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print '\nStep 7: AUX: UDP Connection Configuration\n'
    SagSendAT(aux1_com, 'AT+KUDPCFG=,0\r')
    SagWaitnMatchResp(aux1_com, ['\r\n+KUDPCFG: 1\r\n'], 3000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 3000)
    
    print '\nStep 8: AUX: Display IP Address of the current connection\n'
    SagSendAT(aux1_com, 'AT+SRWSTACON?\r')
    if SagWaitnMatchResp(aux1_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        response1 = SagWaitResp(aux1_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    
    print '\nStep 9: AUX: Checking UDP Connection Configuration\n'
    SagSendAT(aux1_com, 'AT+KUDPCFG?\r')
    SagWaitnMatchResp(aux1_com, ['\r\n+KUDPCFG: 1,,0,0,0\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    
    print '\nStep 10: AUX: Send data to SERVER\n'
    SagSendAT(aux1_com, 'AT+KUDPSND=1,"%s",1234,"A_INTEL_PROTOCOM_KUDP_DATA_0008"\r' %uart_UDP_ip)
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print '\nDUT: Check URC "+KUDP_DATA" is received\n'
    SagWaitnMatchResp(uart_com, ['\r\n+KUDP_DATA: 1,31,"%s",*,A_INTEL_PROTOCOM_KUDP_DATA_0008\r\n' %aux1_UDP_ip], 2000)
    
    print '\nStep 12: AUX: Checking UDP Connection Configuration\n'
    SagSendAT(aux1_com, 'AT+KUDPCFG?\r')
    RES = SagWaitResp(aux1_com, ['\r\n+KUDPCFG: 1,,0,*,0\r\n'], 2000)
    SagMatchResp(RES, ['\r\n+KUDPCFG: 1,,0,*,0\r\n'])
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    aux1_port=RES.split(',')[3]
    
    print '\nStep 13: DUT: Send data to CLIENT - send 218 bytes data\n'
    SagSendAT(uart_com, 'AT+KUDPSND=1,"%s",%s,"12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678"\r' %(aux1_UDP_ip, aux1_port))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nAUX: Check URC "+KUDP_DATA" is received\n'
    SagWaitnMatchResp(aux1_com, ['\r\n+KUDP_DATA: 1,218,"%s",1234,12345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678\r\n' %uart_UDP_ip], 2000)
    
    print '\nStep 14: DUT: Send data to CLIENT - send >218 bytes data\n'
    SagSendAT(uart_com, 'AT+KUDPSND=1,"%s",%s,"1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890121234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890"\r' %(aux1_UDP_ip, aux1_port))
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print '\nStep 15: AUX: Close created session\n'
    SagSendAT(aux1_com, 'AT+KUDPCLOSE=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 16: AUX: Delete UDP Connection after closing it\n'
    SagSendAT(aux1_com, 'AT+KUDPDEL=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 17: DUT: Close created session\n'
    SagSendAT(uart_com, 'AT+KUDPCLOSE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 18: DUT: Delete UDP Connection after closing it\n'
    SagSendAT(uart_com, 'AT+KUDPDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nTest Steps completed\n"

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
SagSendAT(uart_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)

# Restore station connection information to default
SagSendAT(uart_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
SagClose(aux1_com)