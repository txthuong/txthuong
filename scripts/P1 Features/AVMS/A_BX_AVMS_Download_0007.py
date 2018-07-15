# Test Name                       Description
# A_BX_AVMS_Download_0007         Verify that user can change device configuration to request agreement before downloading package. Then it can go back to default configuration after user agreement for package download is deactivated.
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
        raise Exception("---->Problem: Module cannot connect to WIFI !!!")

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_AVMS_Download_0007
# -----------------------------------------------------------------------------------

test_ID = "A_BX_AVMS_Download_0007"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: Verify that user can change device configuration to request agreement before downloading package. Then it can go back to default configuration after user agreement for package download is deactivated.' % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Configures unsolicited indication for Device Services"
    SagSendAT(uart_com, 'AT+WDSI=8191\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Query Device Services general status"
    SagSendAT(uart_com, 'AT+WDSG\r')
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

    SagSendAT(uart_com, 'AT+CGSN\r')
    resp = SagWaitResp(uart_com, ["\r\n*\r\n\r\nOK\r\n"], 4000)
    imei = resp.split("\r\n")[1]
    mySystem = AVMS3(imei)
    mySystem.cancelAllJobs()
    if mySystem.checkNoJobOnServer() != "No_Job":
        raise Exception("\n----Problem: There are some jobs still active!!!!!\n\n")

    print "\nStep 4: Create synchronize job on AVMS server"
    mySystem.createSynchronizeJob()

    print "\nStep 5: Initiate a connection to the Device Services server"
    SagSendAT(uart_com, 'AT+WDSS=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 4000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 4\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 6\r\n'], 30000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 23,1\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 8\r\n'], 90000)

    print "\nStep 6: Set user agreement for package download"
    SagSendAT(uart_com, 'AT+WDSC=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 4000)

    print "\nStep 7: Set user agreement for installation package"
    SagSendAT(uart_com, 'AT+WDSC=2,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 4000)

    print "\nStep 8: Check user agreement for package download and package installation is activated"
    SagSendAT(uart_com, 'AT+WDSC?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 1,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 2,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 3,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 4,15,60,240,960,2880,10080,10080\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 5,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\n---->Info: Check the firmware on AVMS server is same as in sample.cfg"
    fw_rev = mySystem.readTreeNode("lwm2m.3.0.3")
    print "\n---->Info: Firmware version on server is: %s" %fw_rev
    print "\n---->Info: Firmware version in sample.cfg is: %s" %(avms['fw_initial'])
    if fw_rev != avms['fw_initial']:
        raise Exception("------>Problem: Firmware version on server != Firmware version in sample.cfg")

    print '\nStep 9: Create upgrade job on DM server'
    upgrade_job = mySystem.installApplication(avms['upgrade_package_name'],avms['upgrade_package_revision'],avms['model'])

    print "\nStep 10: Initiate a connection to the Device Services server to trigger the upgrade FW job"
    SagSendAT(uart_com, 'AT+WDSS=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 4000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 4\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 6\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 23,1\r\n'], 30000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 2\r\n'], 90000)

    print "\nStep 11: Query Device Services general status"
    SagSendAT(uart_com, 'AT+WDSG\r')
    SagWaitnMatchResp(uart_com, ['\r\n+WDSG: 0,3\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSG: 1,2\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print '\nWait for session with server finished ...'
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 8\r\n'], 90000)

    print "\nStep 12: Delay the Upgrade Job for 2 minutes"
    SagSendAT(uart_com, 'AT+WDSR=2,2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 13: Check the reception of a new user agreement for download 2 minutes later"
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 2\r\n'], 120000)

    print "\nStep 14: Reset module configuration"
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)

    print "\nStep 15: Reconnect to WIFI AP"
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
        raise Exception("---->Problem: Module cannot reconnect to WIFI AP !!!")

    print "\nStep 16: Configures unsolicited indication for Device Services"
    SagSendAT(uart_com, 'AT+WDSI=8191\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 17: Query Device Services configuration"
    SagSendAT(uart_com, 'AT+WDSC?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 2,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 3,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 4,15,60,240,960,2880,10080,10080\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 5,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 18: Waiting for 2 minutes. Check that a user agreement request is not displayed again"
    resp = SagWaitResp(uart_com, [''], 120000)
    if '\r\n+WDSI: 2\r\n' in resp:
        print '\n----> Problem: The reception of a user agreement for download still appears with default configuration'
    else:
        print '\n----> The reception of a user agreement for download is not displayed again'

    print "\nStep 19: Cancel installed application job"
    mySystem.cancelAllJobs()

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

# Restore Station connection information to default
SagSendAT(uart_com, 'AT+SRWSTACFG="","",1\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Restore WIFI mode to default
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
