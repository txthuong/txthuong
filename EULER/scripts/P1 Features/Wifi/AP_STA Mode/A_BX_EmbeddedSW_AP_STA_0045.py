# Test Name                                     Description
# A_BX_EmbeddedSW_AP_STA_0045                   Verify <channel> notification of +SRWSTACON should be correct
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
# A_BX_EmbeddedSW_AP_STA_0045
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_AP_STA_0045"

VarGlobal.statOfItem = "OK"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s:Verify <channel> notification of +SRWSTACON should be correct" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Enable module B as Access Point mode\n"
    SagSendAT(aux1_com, 'AT+SRWCFG=2\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000) 
    
    print "\nStep 2: Setup Access Point configurations\n"
    SagSendAT(aux1_com, 'AT+SRWAPCFG="%s","%s",4,11,0,100\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Enable DHCP with valid values \n"
    SagSendAT(aux1_com, 'AT+SRWAPNETCFG=1,"192.168.0.1","192.168.0.2","192.168.0.2",120\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Query the current Wifi AP operating mode of module B \n"
    SagSendAT(aux1_com, 'AT+SRWCFG?\r')
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWCFG: 2,0,"%s","%s"\r\n' %(aux1_mac_address_sta, aux1_mac_address)], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    
    print "\nStep 5: Query default Operating Mode of module A\n"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWCFG: 3,0,"%s","%s"\r\n' %(dut_mac_address_sta, dut_mac_address)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Configure Operating Mode of module A as AP and STA concurrent mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG=3\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Query default Operating Mode of module A\n"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWCFG: 3,0,"%s","%s"\r\n' %(dut_mac_address_sta, dut_mac_address)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 8: Configure the station connection\n"
    SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s"\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 9: Query current station configuration\n"
    SagSendAT(uart_com, 'AT+SRWSTACFG?\r' )
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTACFG: "%s","%s",0\r\n' %(wifi_ssid, wifi_password)], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 10: Connect to the access point from module B\n"
    SagSendAT(uart_com, 'AT+SRWSTACON=1\r' )
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 1,"%s","%s",11,3\r\n' %(wifi_ssid, aux1_mac_address)], 3000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "192.168.0.2","255.255.255.0","192.168.0.1"\r\n'], 3000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWAPSTA: 1,"%s"\r\n' %dut_mac_address_sta], 3000)
    
    print "\nStep 11: Check details of the current connection\n"
    SagSendAT(uart_com, 'AT+SRWSTACON?\r' )
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 1,"%s","%s",11,3\r\n' %(wifi_ssid, aux1_mac_address)], 3000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "192.168.0.2","255.255.255.0","192.168.0.1"\r\n'], 3000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 12: Disconnect to the access point\n"
    SagSendAT(uart_com, 'AT+SRWSTACON=0\r' )
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)
    
    print "\nStep 13: Check details of the current connection\n"
    SagSendAT(uart_com, 'AT+SRWSTACON?\r' )
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 0\r\n'], 2000)
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

#Disconnect
SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s",0\r' %(wifi_ssid, wifi_password))
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(uart_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(aux1_com, ['\r\n+SRWAPSTA: 0,"%s"\r\n' %dut_mac_address_sta], 2000)

# Restore AUX
SagSendAT(aux1_com, 'AT+SRWCFG=3\r')

# Close UART
SagClose(uart_com)
SagClose(aux1_com)