# Test Name                                     Description
# A_BX_EmbeddedSW_KMQTTCFG_0001                 Check Syntax read, execute +KMQTTCFG  command with valid values, invalid values and values out of range
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
# A_BX_EmbeddedSW_KMQTTCFG_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KMQTTCFG_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check Syntax read, execute +KMQTTCFG  command with valid values, invalid values and values out of range" % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Check +KMQTTCFG test command\n"
    SagSendAT(uart_com, "AT+KMQTTCFG=?\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 2: Check +KMQTTCFG execute command\n"
    SagSendAT(uart_com, "AT+KMQTTCFG\r")
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 3: Check +KMQTTCFG read command\n"
    SagSendAT(uart_com, "AT+KMQTTCFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    session_id = 1
    print "\nStep 4: Check +KMQTTCFG write command with valid parameter <secure>"
    secure = ['0', '1']
    for sec in secure:
        SagSendAT(uart_com, 'AT+KMQTTCFG=%s,%s,%s,4,"test_id"\r' % (sec, mqtt_server, mqtt_port))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"test_id",60,1,0,,,0,0,,\r\n' % (session_id, mqtt_server, mqtt_port)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 5: Check +KMQTTCFG write command with parameter <server>\n"
    server = ['broker.hivemq.com', 'eu.airvantage.net']
    for ser in server:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id"\r' % (ser, mqtt_port))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"test_id",60,1,0,,,0,0,,\r\n' % (session_id, ser, mqtt_port)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 6: Check +KMQTTCFG write command with parameter <port>\n"
    port = [0, 1, 1883, 65535]
    for p in port:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id"\r' % (mqtt_server, p))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"test_id",60,1,0,,,0,0,,\r\n' % (session_id, mqtt_server, p)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 7: Check +KMQTTCFG write command with parameter <version>\n"
    version = ['3', '4']
    for ver in version:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,%s,"test_id"\r' % (mqtt_server, mqtt_port, ver))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,%s,"test_id",60,1,0,,,0,0,,\r\n' % (session_id, mqtt_server, mqtt_port, ver)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 8: Check +KMQTTCFG write command with parameter <clientid>\n"
    clientid = ['euler', 'euler@123', '123456', '[]!@#']
    for client in clientid:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,%s\r' % (mqtt_server, mqtt_port, client))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"%s",60,1,0,,,0,0,,\r\n' % (session_id, mqtt_server, mqtt_port, client)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 9: Check +KMQTTCFG write command with parameter <keepAliveInterval>\n"
    keepAliveInterval = [0, 1, 1883, 65535]
    for interval in keepAliveInterval:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",%s\r' % (mqtt_server, mqtt_port, interval))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"test_id",%s,1,0,,,0,0,,\r\n' % (session_id, mqtt_server, mqtt_port, interval)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 10: Check +KMQTTCFG write command with parameter <cleansession>\n"
    cleansession = [0, 1]
    for clean in cleansession:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,%s\r' % (mqtt_server, mqtt_port, clean))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"test_id",60,%s,0,,,0,0,,\r\n' % (session_id, mqtt_server, mqtt_port, clean)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 11: Check +KMQTTCFG write command with parameter <willFlag>\n"
    willFlag = [0, 1]
    for flag in willFlag:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,%s\r' % (mqtt_server, mqtt_port, flag))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"test_id",60,1,%s,,,0,0,,\r\n' % (session_id, mqtt_server, mqtt_port, flag)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 12: Check +KMQTTCFG write command with parameter <topicName>\n"
    topicName = ['euler', 'euler@123', '123456', '[]!@#']
    for topic in topicName:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,%s\r' % (mqtt_server, mqtt_port, topic))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"test_id",60,1,0,%s,,0,0,,\r\n' % (session_id, mqtt_server, mqtt_port, topic)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 13: Check +KMQTTCFG write command with parameter <message>\n"
    message = ['euler', 'euler@123', '123456', '[]!@#']
    for mes in message:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,"euler",%s\r' % (mqtt_server, mqtt_port, mes))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"test_id",60,1,0,"euler","%s",0,0,,\r\n' % (session_id, mqtt_server, mqtt_port, mes)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 14: Check +KMQTTCFG write command with parameter <retained>\n"
    retained = [0, 1]
    for r in retained:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,"euler","OFF",%s\r' % (mqtt_server, mqtt_port, r))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"test_id",60,1,0,"euler","OFF",%s,0,,\r\n' % (session_id, mqtt_server, mqtt_port, r)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 15: Check +KMQTTCFG write command with parameter <qos>\n"
    qos = [0, 1, 2]
    for q in qos:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,"euler","OFF",0,%s\r' % (mqtt_server, mqtt_port, q))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"test_id",60,1,0,"euler","OFF",0,%s,,\r\n' % (session_id, mqtt_server, mqtt_port, q)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 16: Check +KMQTTCFG write command with parameter <username>\n"
    username = ['euler', 'euler@123', '123456', '[]!@#']
    for user in username:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,"euler","OFF",0,0,%s\r' % (mqtt_server, mqtt_port, user))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"test_id",60,1,0,"euler","OFF",0,0,"%s",\r\n' % (session_id, mqtt_server, mqtt_port, user)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 17: Check +KMQTTCFG write command with parameter <username>\n"
    password = ['euler', 'euler@123', '123456', '[]!@#']
    for pw in password:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,"euler","OFF",0,0,"euler",%s\r' % (mqtt_server, mqtt_port, pw))
        SagWaitnMatchResp(uart_com, ['\r\n+KMQTTCFG: %s\r\n' % session_id], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTCFG?\r")
        SagWaitnMatchResp(uart_com, ['*\r\n+KMQTTCFG: %d,"%s",%s,4,"test_id",60,1,0,"euler","OFF",0,0,"euler","%s"\r\n' % (session_id, mqtt_server, mqtt_port, pw)], 2000)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        SagSendAT(uart_com, "AT+KMQTTDEL=1\r")
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nCheck +KMQTTCFG command with ERROR case"
    print "\nStep 18: Check +KMQTTCFG write command with invalid parameter <secure>"
    secure = [-1, 2, 'a', 'A', '@', '!']
    for sec in secure:
        SagSendAT(uart_com, 'AT+KMQTTCFG=%s,%s,%s,4,"test_id"\r' % (sec, mqtt_server, mqtt_port))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 19: Check +KMQTTCFG write command with invalid parameter <server>\n"
    server = ['broker.hivemq.com/space%20here.html', '"broker.hivemq.com"-1-1-1-1']
    for ser in server:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id"\r' % (ser, mqtt_port))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 20: Check +KMQTTCFG write command with invalid parameter <port>\n"
    port = [-1, 65536, 'a', 'A', '@', '!']
    for p in port:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id"\r' % (mqtt_server, p))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 21: Check +KMQTTCFG write command with invalid parameter <version>\n"
    version = ['-1', '2', '5', 'a', 'A', '@', '!']
    for ver in version:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,%s,"test_id"\r' % (mqtt_server, mqtt_port, ver))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 22: Check +KMQTTCFG write command with invalid parameter <clientid>\n"
    clientid = ['euler"', '""euler@123"']
    for client in clientid:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,%s\r' % (mqtt_server, mqtt_port, client))
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 23: Check +KMQTTCFG write command with invalid parameter <keepAliveInterval>\n"
    keepAliveInterval = [-1, 65536, 'a', 'A', '@', '!']
    for interval in keepAliveInterval:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",%s\r' % (mqtt_server, mqtt_port, interval))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 24: Check +KMQTTCFG write command with invalid parameter <cleansession>\n"
    cleansession = [-1, 2, 'a', 'A', '@', '!']
    for clean in cleansession:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,%s\r' % (mqtt_server, mqtt_port, clean))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 25: Check +KMQTTCFG write command with invalid parameter <willFlag>\n"
    willFlag = [-1, 2, 'a', 'A', '@', '!']
    for flag in willFlag:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,%s\r' % (mqtt_server, mqtt_port, flag))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 26: Check +KMQTTCFG write command with invalid parameter <topicName>\n"
    topicName = ['euler"', '""euler@123"']
    for topic in topicName:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,%s\r' % (mqtt_server, mqtt_port, topic))
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 27: Check +KMQTTCFG write command with invalid parameter <message>\n"
    message = ['euler"', '""euler@123"']
    for mes in message:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,"euler",%s\r' % (mqtt_server, mqtt_port, mes))
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 28: Check +KMQTTCFG write command with invalid parameter <retained>\n"
    retained = [-1, 2, 'a', 'A', '@', '!']
    for r in retained:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,"euler","OFF",%s\r' % (mqtt_server, mqtt_port, r))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 29: Check +KMQTTCFG write command with invalid parameter <qos>\n"
    qos = [-1, 3, 'a', 'A', '@', '!']
    for q in qos:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,"euler","OFF",0,%s\r' % (mqtt_server, mqtt_port, q))
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 30: Check +KMQTTCFG write command with invalid parameter <username>\n"
    username = ['euler"', '""euler@123"']
    for user in username:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,"euler","OFF",0,0,%s\r' % (mqtt_server, mqtt_port, user))
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 31: Check +KMQTTCFG write command with invalid parameter <username>\n"
    password = ['euler"', '""euler@123"']
    for pw in password:
        SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,"euler","OFF",0,0,"euler",%s\r' % (mqtt_server, mqtt_port, pw))
        SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print "\nStep 32: Check +KMQTTCFG write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+KMQTTCFG=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KMQTTCFG=0\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s\r' % mqtt_server)
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s\r' % (mqtt_server, mqtt_port))
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4\r' % (mqtt_server, mqtt_port))
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)

    print "\nStep 33: Check +KMQTTCFG write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+KMQTTCFG=0,%s,%s,4,"test_id",60,1,0,"euler","OFF",0,0,"euler","123456",1\r' % (mqtt_server, mqtt_port))
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    print "\nStep 34: Query MQTT configuration"
    SagSendAT(uart_com, "AT+KMQTTCFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        raise Exception ('\n----> Problem: Failed to test ERROR case')

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
