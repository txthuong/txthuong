# Test Name                                     Description
# A_BX_EmbeddedSW_KTCPCLOSE_0005                To check that +KTCPCLOSE supports client <session_id> 1 - 200
#
# Requirement
#   1 Euler module
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
    
    # Display DUT Information
    print "\nDisplay DUT information"
    print "\nGet model information"
    SagSendAT(uart_com, 'AT+FMM\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nGet serial number"
    SagSendAT(uart_com, 'AT+CGSN\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nGet revision information"
    SagSendAT(uart_com, 'ATI3\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'] , 2000)
    
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
# A_BX_EmbeddedSW_KTCPCLOSE_0005
# -----------------------------------------------------------------------------------
    
test_ID = "A_BX_EmbeddedSW_KTCPCLOSE_0005"
    
#######################################################################################
#   START
#######################################################################################
    
try:
    
    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")
    
    print "***************************************************************************************************************"
    print "%s:To check that +KTCPCLOSE supports client <session_id> 1 - 200" % test_ID
    print "***************************************************************************************************************"
    
    print '\nStep 1: Configure modules work as Station mode\n'
    SagSendAT(uart_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 2: Connect to the Wi-Fi network\n'
    SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s"\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print '\nStep 3: Activate Station connection\n'
    SagSendAT(uart_com, 'AT+SRWSTACON=1\r')
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
    
    print '\nStep 4: TCP Connection Configuration\n'
    for i in range (1,65):
        SagSendAT(uart_com, 'AT+KTCPCFG=,0,"%s",%s,1\r' %(tcp_server, tcp_port))
        SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: %s\r\n' %i], 2000)
        SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print '\nStep 6: Start TCP Connection (1-9)\n'
    for i in range (1,10):
        SagSendAT(uart_com, 'AT+KTCPCNX=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
    
    print '\nStep 7: Close the TCP connection with <session_id> from 1 to 9\n'
    for i in range (1,10):
        SagSendAT(uart_com, 'AT+KTCPCLOSE=%s,1\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
        
    print '\nStart TCP Connection (10-18)\r'
    for i in range (10,19):
        SagSendAT(uart_com, 'AT+KTCPCNX=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
    
    print '\nClose the TCP connection with <session_id> from 9 to 18\n'
    for i in range (10,19):
        SagSendAT(uart_com, 'AT+KTCPCLOSE=%s,1\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
        
    print '\nStart TCP Connection (19-27)\r'
    for i in range (19,28):
        SagSendAT(uart_com, 'AT+KTCPCNX=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
    
    print '\nClose the TCP connection with <session_id> from 19 to 27\n'
    for i in range (19,28):
        SagSendAT(uart_com, 'AT+KTCPCLOSE=%s,1\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
        
    print '\nStart TCP Connection (28-36)\r'
    for i in range (28,37):
        SagSendAT(uart_com, 'AT+KTCPCNX=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
    
    print '\Close the TCP connection with <session_id> from 28 to 36\n'
    for i in range (28,37):
        SagSendAT(uart_com, 'AT+KTCPCLOSE=%s,1\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
        
    print '\nStart TCP Connection (37-45)\r'
    for i in range (37,46):
        SagSendAT(uart_com, 'AT+KTCPCNX=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
    
    print '\Close the TCP connection with <session_id> from 37 to 45\n'
    for i in range (37,46):
        SagSendAT(uart_com, 'AT+KTCPCLOSE=%s,1\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
        
    print '\nStart TCP Connection (46-54)\r'
    for i in range (46,55):
        SagSendAT(uart_com, 'AT+KTCPCNX=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
    
    print '\Close the TCP connection with <session_id> from 46 to 54\n'
    for i in range (46,55):
        SagSendAT(uart_com, 'AT+KTCPCLOSE=%s,1\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
        
    print '\nStart TCP Connection (55 - 64)\r'
    for i in range (55,64):
        SagSendAT(uart_com, 'AT+KTCPCNX=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
    
    print '\Close the TCP connection with <session_id> from 55 to 64\n'
    for i in range (55,64):
        SagSendAT(uart_com, 'AT+KTCPCLOSE=%s,1\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
    SagSendAT(uart_com, 'AT+KTCPCNX=64\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KTCPCLOSE=64,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
        
    print '\nStep 8: Delete TCP Connection after closing it\n'
    for i in range (1,65):
        SagSendAT(uart_com, 'AT+KTCPDEL=%s\r' %i)
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
