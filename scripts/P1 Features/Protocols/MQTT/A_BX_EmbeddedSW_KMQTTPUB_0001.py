# Test Name                         Description
# A_BX_EmbeddedSW_KMQTTPUB_0001     Check Syntax read, execute +KMQTTPUB command with valid values, invalid values and values out of range
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
# A_BX_EmbeddedSW_KMQTTPUB_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KMQTTPUB_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: Check Syntax read, execute +KMQTTPUB command with valid values, invalid values and values out of range' % test_ID
    print "***************************************************************************************************************"

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

    print "\nStep 5: Check +KMQTTPUB test command"
    SagSendAT(uart_com, "AT+KMQTTPUB=?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 6: Check +KMQTTPUB execute command"
    SagSendAT(uart_com, "AT+KMQTTPUB\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 7: Check +KMQTTPUB read command"
    SagSendAT(uart_com, "AT+KMQTTPUB?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    topic = 'TMA/DUT/publish'
    message = 'Testing +KMQTTPUB'

    print "\nStep 8: Check +KMQTTPUB write command with valid parameters"
    for qos in [0, 1, 2]:
        for retained in [0, 1]:
            SagSendAT(uart_com, 'AT+KMQTTPUB=1,"%s",%s,%s,"%s"\r' % (topic, qos, retained, message))
            SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 4000)

    print "\nStep 9: Check +KMQTTPUB write command with not configured session id"
    session_id = [0, 2, 65535]
    for session in session_id:
        SagSendAT(uart_com, 'AT+KMQTTPUB=%s,"%s",0,0,"%s"\r\r' % (session, topic, message))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)

    print "\nStep 10: Check +KMQTTPUB write command with out-range and invalid parameter <session_id>"
    session_id = [-1, 65536, 'a', 'A', '$', '*']
    for session in session_id:
        SagSendAT(uart_com, 'AT+KMQTTPUB=%s,"%s",0,0,"%s"\r\r' % (session, topic, message))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 11: Check +KMQTTPUB write command with invalid parameter <qos>"
    qos = [-1, 3, 'a', 'A', '$', '*']
    for q in qos:
        SagSendAT(uart_com, 'AT+KMQTTPUB=1,"%s",%s,0,"%s"\r\r' % (topic, q, message))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 12: Check +KMQTTPUB write command with invalid parameter <retained>"
    retained = [-1, 3, 'a', 'A', '$', '*']
    for r in retained:
        SagSendAT(uart_com, 'AT+KMQTTPUB=1,"%s",0,%s,"%s"\r\r' % (topic, r, message))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 13: Check +KMQTTPUB write command with invalid parameter <topicName>"
    topicName = ['"Euler/Test', '"Euler/123""']
    for tp in topicName:
        SagSendAT(uart_com, 'AT+KMQTTPUB=1,%s,0,0,"%s"\r\r' % (tp, message))
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 14: Check +KMQTTPUB write command with invalid parameter <payload>"
    payload = ['"Testing', '"Euler""']
    for pl in payload:
        SagSendAT(uart_com, 'AT+KMQTTPUB=1,"%s",0,0,%s\r\r' % (topic, pl))
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 15: Check +KMQTTPUB write command with missing parameter"
    SagSendAT(uart_com, 'AT+KMQTTPUB=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KMQTTPUB=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KMQTTPUB=1,"%s"\r' % topic)
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KMQTTPUB=1,"%s",0\r' % topic)
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KMQTTPUB=1,"%s",0,0\r' % topic)
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 16: Check +KMQTTPUB write command with extra parameter"
    SagSendAT(uart_com, 'AT+KMQTTPUB=1,"%s",0,0,"%s",1\r' % (topic, message))
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    print "\nStep 17: Close the MQTT connection"
    SagSendAT(uart_com, 'AT+KMQTTCLOSE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

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
