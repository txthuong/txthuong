# Test Name                          Description
# A_BX_EmbeddedSW_KMQTTPUB_0002      Check that +KMQTTPUB can publish message to a specific MQTT session
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

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_KMQTTPUB_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KMQTTPUB_0002"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: Check that +KMQTTPUB can publish message to a specific MQTT session' % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Query MQTT configure"
    SagSendAT(uart_com, 'AT+KMQTTCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    dut_lwt_topic = 'TMA/DUT/status'
    dut_lwt_message = 'OFFLINE'
    max_session = 11

    print "\nStep 2: Configure MQTT connections"
    for session in range (1, max_session):
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,"%s",%s,4,"BX_DUT",60,1,1,"%s","%s",0,0,"%s","%s"\r' % (mqtt_server, mqtt_port, dut_lwt_topic, dut_lwt_message, mqtt_user, mqtt_password))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Query MQTT connection configuration"
    SagSendAT(uart_com, 'AT+KMQTTCFG?\r')
    for session in range (1, max_session):
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s,"%s",%s,4,"BX_DUT",60,1,1,"%s","%s",0,0,"%s","%s"\r\n' % (session, mqtt_server, mqtt_port, dut_lwt_topic, dut_lwt_message, mqtt_user, mqtt_password)], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    for session in range (1, max_session):
        print "\nStep 4: Start MQTT connection"
        SagSendAT(uart_com, 'AT+KMQTTCNX=%s\r' % session)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)

        topic = 'TMA/DUT/chanel%s' % session
        message = 'Testing +KMQTTSUB with session %s' % session

        print "\nStep 5: Subscribe a topic on server"
        SagSendAT(uart_com, 'AT+KMQTTSUB=%s,"%s",1\r' % (session, topic))
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)

        print "\nStep 6: Publish message to the topic"
        SagSendAT(uart_com, 'AT+KMQTTPUB=%s,"%s",0,0,"%s"\r' % (session, topic, message))
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTSUB: "%s","%s"\r\n' % (topic, message)], 2000)

        print "\nStep 7: Close MQTT session"
        SagSendAT(uart_com, 'AT+KMQTTCLOSE=%s\r' % session)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 5000)

    print "\nStep 8: Delete the MQTT connection"
    for session in range (1, max_session):
        SagSendAT(uart_com, 'AT+KMQTTDEL=%s\r' % session)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 9: Query MQTT connection configuration"
    SagSendAT(uart_com, 'AT+KMQTTCFG?\r')
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        raise Exception("---->Problem: MQTT configure was not deleted completely !!!")

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
