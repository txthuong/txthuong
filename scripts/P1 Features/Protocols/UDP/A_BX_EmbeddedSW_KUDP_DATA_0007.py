# Test Name                                     Description
# A_BX_EmbeddedSW_KUDP_DATA_0007                To check when <data_mode> was set to 0, Data shall not be shown in the URC
#
# Requirement
# 1 Euler modules
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
    
except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"
    
print "\n------------Test Environment check: End------------"
    
print "\n----- Test Body Start -----\n"
    
# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_KUDP_DATA_0007
# -----------------------------------------------------------------------------------
    
test_ID = "A_BX_EmbeddedSW_KUDP_DATA_0007"
    
#######################################################################################
#   START
#######################################################################################
    
try:
    
    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")
    
    print "***************************************************************************************************************"
    print "%s:To check when <data_mode> was set to 0, Data shall not be shown in the URC" % test_ID
    print "***************************************************************************************************************"
    
    print '\nStep 1: Configure modules work as Station mode\n'
    SagSendAT(uart_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 2: Connect to the Wi-Fi network\n'
    SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s"\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nStep 3: Activate Station connection\n'
    SagSendAT(uart_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
    
    print '\nStep 4: UDP Connection Configuration\n'
    SagSendAT(uart_com, 'AT+KUDPCFG=,0\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KUDPCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 5: Display IP Address of the current connection\n'
    SagSendAT(uart_com, 'AT+SRWSTACON?\r')
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 6: AUX: Checking UDP Connection Configuration\n'
    SagSendAT(uart_com, 'AT+KUDPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KUDPCFG: 1,,0,0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print '\nStep 7: Send data to SERVER\n'
    SagSendAT(uart_com, 'AT+KUDPSND=1,"%s",%s,"A_INTEL_PROTOCOM_KUDP_DATA_0007 part 1"\r' %(udp_server, udp_port))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    response = SagWaitResp(uart_com, ['\r\n+KUDP_DATA: 1,38,"%s",*,A_INTEL_PROTOCOM_KUDP_DATA_0007 part 1\r\n' %udp_server], 2000)
    if '+KUDP_DATA' in response:
        print ('\r\nFAIL, when <data_mode> was set to 0, Data be shown in the URC\r\n')
        
    if '+KUDP_DATA' not in response:
        print ('\r\nOK, when <data_mode> was set to 0, Data not be shown in the URC \r\n')
    
    print '\nStep 8: Send data to SERVER again\n'
    SagSendAT(uart_com, 'AT+KUDPSND=1,"%s",%s,"A_INTEL_PROTOCOM_KUDP_DATA_0007 part 2"\r' %(udp_server, udp_port))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 9: Wait about 30 seconds to check if there is URC +KUDP_DATA\n'
    time.sleep(30)
    response = SagWaitResp(uart_com, ['\r\n+KUDP_DATA: 1,38,"%s",*,A_INTEL_PROTOCOM_KUDP_DATA_0007 part 1\r\n' %udp_server], 2000)
    if '+KUDP_DATA' in response:
        print ('\r\nFAIL, when <data_mode> was set to 0, Data be shown in the URC\r\n')
        
    if '+KUDP_DATA' not in response:
        print ('\r\nOK, when <data_mode> was set to 0, Data not be shown in the URC \r\n')
    
    print '\nStep 8: Close created session\n'
    SagSendAT(uart_com, 'AT+KUDPCLOSE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 9: Delete UDP Connection after closing it\n'
    SagSendAT(uart_com, 'AT+KUDPDEL=1\r')
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