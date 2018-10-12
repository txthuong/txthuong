# Test Name                                     Description
# A_BX_UART_AT&K_0005                           To check if hardware flow control working
# 
# Requirement
# 1 Euler module
#    
# Author: ptnlam
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

# -------------------------- DUT InitializAT+SYSRAMon ----------------------------------

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
# A_BX_UART_AT&K_0005
# -----------------------------------------------------------------------------------

test_ID = "A_BX_UART_AT&K_0005"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: To check if hardware flow control working" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Connect to Wi-Fi\n"
    SagSendAT(uart_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(uart_com, 'AT+SRWSTACFG="%s","%s",1\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(uart_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot connect to Wi-Fi !!!")
    
    print "\nStep 2: Configure a MQTT session\n"
    SagSendAT(uart_com, 'AT+KMQTTCFG=0,"%s",%s,4,"BX310x",0,1,1,"TMA/Euler","BX310x Left",0,0,"%s","%s"\r' %(mqtt_server, mqtt_port, mqtt_user, mqtt_password ))
    SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Active MQTT session\n"
    SagSendAT(uart_com, 'AT+KMQTTCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Enable Hardware Flow Control\n"
    SagSendAT(uart_com, 'AT&K3\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Set RTS to high\n"
    SagSetRTS(uart_com, 1)
    time.sleep(1) 
    
    print "\nStep 6: Subscribe to Broker to receive uptime of broker every 11 seconds\n"
    SagSendAT(uart_com, 'AT+KMQTTSUB=1,"$SYS/broker/uptime",1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
    
    print "\nStep 7: Check every 11 seconds, module receives a message from MQTT brokers\n"
    SagWaitnMatchResp(uart_com, ['\r\n+KMQTTSUB: "$SYS/broker/uptime","* seconds"\r\n'], 11000)
    SagWaitnMatchResp(uart_com, ['\r\n+KMQTTSUB: "$SYS/broker/uptime","* seconds"\r\n'], 11000)
    
    print "\nStep 8: Set RTS to low\n"
    SagSetRTS(uart_com, 0)
    
    print "\nStep 9: Wait for 1 minutes. Check URC on module\n"
    time.sleep(60) 
    if (SagWaitResp(uart_com, ['\r\n*\r\n'], 5000)):
        print "\nURC on module\n"
    else:
        print "\nModule should not receive any URC\n"
    
    print "\nStep 10: Set RTS to high\n"
    SagSetRTS(uart_com, 1)
    time.sleep(1) 
    
    print "\nStep 11: Check response\n"
    SagWaitnMatchResp(uart_com, ['\r\n+KMQTTSUB: "$SYS/broker/uptime","* seconds"\r\n'], 11000)
    SagWaitnMatchResp(uart_com, ['\r\n+KMQTTSUB: "$SYS/broker/uptime","* seconds"\r\n'], 11000)
    SagWaitnMatchResp(uart_com, ['\r\n+KMQTTSUB: "$SYS/broker/uptime","* seconds"\r\n'], 11000)
    
#    print "\nStep 12: Set RTS to low\n"
#    SagSetRTS(uart_com, 0)
    
#    print "\nStep 13: Disable Hardware Flow Control\n"
#    SagSendAT(uart_com, 'AT&K0')
#    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)

    print "\nStep 14: Close MQTT session\n"
    SagSendAT(uart_com, 'AT+KMQTTCLOSE=1')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)

    print "\nStep 15: Delete MQTT session\n"
    SagSendAT(uart_com, 'AT+KMQTTDEL=1')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
    
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


#Disconnect
SagSendAT(uart_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 3000)
SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 3000)

# Restore DUT
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)