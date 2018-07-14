# Test Name                                     Description
# A_BX_EmbeddedSW_KMQTTCFG_0002                 Check Last Will and Testament feature
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
    aux_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

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

    # Display AUX information
    print "\nDisplay AUX information"
    print "\nGet model information"
    SagSendAT(aux_com, 'AT+FMM\r')
    SagWaitnMatchResp(aux_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux_com, 'AT+CGSN\r')
    SagWaitnMatchResp(aux_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux_com, 'ATI3\r')
    SagWaitnMatchResp(aux_com, ['*\r\nOK\r\n'], 2000)

    # AUX Initialization
    print "\nInitiate AUX"
    # Configures module as Station mode
    SagSendAT(aux_com, 'AT+SRWCFG=1\r')
    SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000)

    # Configures the station connection information
    SagSendAT(aux_com, 'AT+SRWSTACFG="%s","%s",1\r' %(wifi_ssid,wifi_password))
    SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000)

    # Connect to configured Access Point
    SagSendAT(aux_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000)
    if SagWaitnMatchResp(aux_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        SagWaitnMatchResp(aux_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
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
# A_BX_EmbeddedSW_KMQTTCFG_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KMQTTCFG_0002"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: Check Last Will and Testament feature' % test_ID
    print "***************************************************************************************************************"

    print "\nOn DUT..."
    print "\nStep 1: Query MQTT configure"
    SagSendAT(uart_com, 'AT+KMQTTCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    dut_lwt_topic = 'TMA/DUT/status'
    dut_lwt_message = 'OFFLINE'
    print "\nStep 2: Configure a MQTT connection"
    SagSendAT(uart_com, 'AT+KMQTTCFG=0,"%s",%s,4,"BX_DUT",60,1,1,"%s","%s",0,0,"%s","%s"\r' % (mqtt_server, mqtt_port, dut_lwt_topic, dut_lwt_message, mqtt_user, mqtt_password))
    SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Query MQTT connection configuration"
    SagSendAT(uart_com, 'AT+KMQTTCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: 1,"%s",%s,4,"BX_DUT",60,1,1,"%s","%s",0,0,"%s","%s"\r\n' % (mqtt_server, mqtt_port, dut_lwt_topic, dut_lwt_message, mqtt_user, mqtt_password)], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Active MQTT connection"
    SagSendAT(uart_com, 'AT+KMQTTCNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)

    print "\nStep 5: Subscribe a topic on server"
    SagSendAT(uart_com, 'AT+KMQTTSUB=1,"%s",1\r' % dut_lwt_topic)
    # Module may receive retained message from the subscribed topic 
    resp = SagWaitResp(uart_com, [''], 4000)
    SagMatchResp(resp, ['\r\nOK\r\n\r\n+KMQTTSUB: "%s","*"\r\n' % dut_lwt_topic, '\r\nOK\r\n'])

    message = 'ONLINE'
    print "\nStep 6: Publish message to the subscribed topic"
    SagSendAT(uart_com, 'AT+KMQTTPUB=1,"%s",1,1,"%s"\r' % (dut_lwt_topic, message))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+KMQTTSUB: "%s","%s"\r\n' % (dut_lwt_topic, message)], 2000)

    print '\nOn AUX...'
    print "\nStep 7: Query MQTT configure"
    SagSendAT(aux_com, 'AT+KMQTTCFG?\r')
    SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000)

    aux_lwt_topic = 'TMA/AUX/status'
    aux_lwt_message = 'OFFLINE'
    print "\nStep 8: Configure a MQTT connection"
    SagSendAT(aux_com, 'AT+KMQTTCFG=0,"%s",%s,4,"BX_AUX",60,1,1,"%s","%s",0,0,"%s","%s"\r' % (mqtt_server, mqtt_port, aux_lwt_topic, aux_lwt_message, mqtt_user, mqtt_password))
    SagWaitnMatchResp(aux_com, ['\r\n+KMQTTCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 9: Query MQTT connection configuration"
    SagSendAT(aux_com, 'AT+KMQTTCFG?\r')
    SagWaitnMatchResp(aux_com, ['\r\n+KMQTTCFG: 1,"%s",%s,4,"BX_AUX",60,1,1,"%s","%s",0,0,"%s","%s"\r\n' % (mqtt_server, mqtt_port, aux_lwt_topic, aux_lwt_message, mqtt_user, mqtt_password)], 2000)
    SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 10: Active MQTT connection"
    SagSendAT(aux_com, 'AT+KMQTTCNX=1\r')
    SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 5000)

    print "\nStep 11: Subscribe a topic on server"
    SagSendAT(aux_com, 'AT+KMQTTSUB=1,"%s",1\r' % dut_lwt_topic)
    SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000)
    # Receive retained message
    SagWaitnMatchResp(aux_com, ['\r\n+KMQTTSUB: "%s","%s"\r\n' % (dut_lwt_topic, message)], 2000)

    print '\nOn DUT...'
    print "\nStep 12: Disconnect to WIFI AP"
    SagSendAT(uart_com, 'AT+SRWSTACON=0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)

    print '\nOn AUX...'
    print "\nStep 13: Check LWT message from DUT"
    SagWaitnMatchResp(aux_com, ['\r\n+KMQTTSUB: "%s","%s"\r\n' % (dut_lwt_topic, dut_lwt_message)], 120000)

    print "\nStep 14: Close MQTT session"
    SagSendAT(aux_com, 'AT+KMQTTCLOSE=1\r')
    SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 15: Delete the MQTT connection"
    SagSendAT(aux_com, 'AT+KMQTTDEL=1\r')
    SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 16: Query MQTT connection configuration"
    SagSendAT(aux_com, 'AT+KMQTTCFG?\r')
    if not SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: MQTT configure was not deleted properly !!!")

    print '\nOn DUT...'
    print "\nStep 18: Delete the MQTT connection"
    SagSendAT(uart_com, 'AT+KMQTTDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 19: Query MQTT connection configuration"
    SagSendAT(uart_com, 'AT+KMQTTCFG?\r')
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: MQTT configure was not deleted properly !!!")

    print "\nTest Steps completed"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux_com, 'AT&F\r')
    SagWaitnMatchResp(aux_com, ['*\r\nREADY\r\n'], 2000)

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

# Disconnect to configured Access Point
SagSendAT(aux_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000)
SagWaitnMatchResp(aux_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 2000)

# Restore station connection information to default
SagSendAT(aux_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(aux_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(aux_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
# Close AUX
SagClose(aux_com)
