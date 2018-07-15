# Test Name                    Description
# A_BX_AVMS_CNT_0014           Check the device is able to connect to the server each X minutes specified in Heartbeat period
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
# A_BX_AVMS_CNT_0014
# -----------------------------------------------------------------------------------

test_ID = "A_BX_AVMS_CNT_0014"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Check the device is able to connect to the server each X minutes specified in Heartbeat period" % test_ID
    print "***********************************************************************************************************************"

    print "\nStep 1: Configures unsolicited indication for Device Services"
    SagSendAT(uart_com, "AT+WDSI=8191\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 10000)

    print "\nStep 2: Query Device Services general status"
    SagSendAT(uart_com, "AT+WDSG\r")
    SagWaitnMatchResp(uart_com, ['\r\n+WDSG: 0,3\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSG: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Query Device Services configuration"
    SagSendAT(uart_com, 'AT+WDSC?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 2,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 3,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 4,15,60,240,960,2880,10080,10080\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 5,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Initiate a connection to the Device Services server"
    SagSendAT(uart_com, 'AT+WDSS=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 4\r\n'], 20000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 6\r\n'], 20000)
    SagWaitnMatchResp(uart_com, ['*\r\n+WDSI: 23,1\r\n'], 20000)

    print "\nStep 5: Release the connection to the Device Services server"
    SagSendAT(uart_com, 'AT+WDSS=1,0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 4000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 8\r\n'], 10000)

    SagSendAT(uart_com, 'AT+CGSN\r')
    resp = SagWaitResp(uart_com, ["\r\n*\r\n\r\nOK\r\n"], 4000)
    seri_number = resp.split("\r\n")[1]
    my_system = AVMS3(seri_number)
    my_system.cancelAllJobs()

    print "\nStep 6: Configure communication on AVMS server"
    uid_operation = my_system.configureCommunication('ON',15,'OFF',30)

    print "\nStep 7: Initiate a connection to the Device Services server"
    SagSendAT(uart_com, 'AT+WDSS=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
#-----------------------------------------------------------------------------------
# Strange behaviour --> Need to recheck
#    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 4\r\n'], 20000)
#    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 6\r\n'], 20000)
#    SagWaitnMatchResp(uart_com, ['*\r\n+WDSI: 23,1\r\n'], 20000)
#    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 8\r\n'], 90000)
    # Module reset to active communication configuration
#    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 90000)
#    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
#        SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
#    else:
#        raise Exception("---->Problem: Module cannot reconnect to Wi-Fi AP !!!")
#-----------------------------------------------------------------------------------
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 4\r\n'], 20000)
    start_time = datetime.now()
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 6\r\n'], 20000)
    SagWaitnMatchResp(uart_com, ['*\r\n+WDSI: 23,1\r\n'], 20000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 8\r\n'], 90000)

    print "\nStep 8: Check operation status"
    if my_system.getOperationTasksDetails(uid_operation) != 'SUCCESS':
        print 'Problem: Configuring communication is not complete !!!'
    else:
        print 'Configuring communication is complete'

    print "\nStep 9: Query Device Services configuration"
    SagSendAT(uart_com, 'AT+WDSC?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 2,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 3,15\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 4,15,60,240,960,2880,10080,10080\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 5,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 10: Check that device connect to AVMS server after every heartbeat period automatically"
    resp = SagWaitResp(uart_com, ['\r\n+WDSI: 4\r\n'], 900000)
    diff_time = datetime.now() - start_time
    diff_time_ms = diff_time.seconds * 1000 + diff_time.microseconds / 1000
    if (SagMatchResp(resp,['\r\n+WDSI: 4\r\n'])) and (diff_time_ms>=840000):
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 6\r\n'], 20000)
        SagWaitnMatchResp(uart_com, ['*\r\n+WDSI: 23,1\r\n'], 20000)
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 8\r\n'], 90000)
    else:
        print '\n----> Problem: Polling mode is not working properly!!!'

    print "\nStep 11: Disable Heartbeat on AVMS server"
    my_system.configureCommunication('OFF',15,'OFF',30)

    print "\nStep 12: Initiate a connection to the Device Services server"
    SagSendAT(uart_com, 'AT+WDSS=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 4\r\n'], 20000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 6\r\n'], 20000)
    SagWaitnMatchResp(uart_com, ['*\r\n+WDSI: 23,1\r\n'], 20000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 8\r\n'], 90000)

    print "\nStep 13: Query Device Services configuration"
    SagSendAT(uart_com, 'AT+WDSC?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 2,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 3,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 4,15,60,240,960,2880,10080,10080\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 5,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 14: Check that device should not connect to AVMS server automatically any more"
    resp = SagWaitResp(uart_com, [''], 900000)
    if '\r\n+WDSI: 4\r\n' in resp:
        print '\n----> Problem: Device still connect to AVMS server automatically !!!'
        VarGlobal.statOfItem = "NOK"
    else:
        print '\n----> No automatic connection is triggered after polling period'

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

# Restore Station connection information to default
SagSendAT(uart_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore Wi-Fi mode to default
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
