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
# A_BX_EmbeddedSW_Disablemode_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_Disablemode_0001"

VarGlobal.statOfItem = "OK"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s:Configures the module's WIFI mode in Disabled mode " % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Execute command to enable module as Access Point mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Execute command with valid values to setup Access Point configurations\n"
    SagSendAT(uart_com, 'AT+SRWAPCFG="%s","%s",4,5,0,100\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Execute command to query current AP configurations \n"
    SagSendAT(uart_com, 'AT+SRWAPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPCFG: "%s","%s",4,5,0,100\r\n' %(wifi_ssid, wifi_password)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: Execute command to enable DHCP\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG=1,"192.168.0.1","192.168.0.2","192.168.0.2",720\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Execute command to query current Wifi configurations \n"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWCFG: 2,0,"%s","%s"\r\n' %(dut_stamac_address, dut_mac_address)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Use another module to connect to this Access Point\n"
    SagSendAT(aux1_com, 'AT+SRWSTACFG="%s","%s",1\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Connect to Access Point\n"
    SagSendAT(aux1_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 1,"%s","%s",5,3\r\n' % (wifi_ssid, dut_mac_address)], 2000 )
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTAIP: "192.168.0.2","255.255.255.0","192.168.0.1"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 1,"%s"\r\n' % aux1_mac_address], 2000)
    
    print "\nStep 8: Execute command to change module state as Disable mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG=0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 0,"%s"\r\n' % aux1_mac_address], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 0,4\r\n'], 2000)
    
    print "\nStep 9: Use another module to reconnect to this Access Point\n"
    SagSendAT(aux1_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nTest Steps completed\n"
except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg

#Print test result.

PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

#Disable Wifi auto-connect
SagSendAT(aux1_com, 'AT+SRWSTACFG="%s","%s",0\r' %(wifi_ssid,wifi_password))
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 0,202\r\n'], 2000)

# Restore DUT
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
