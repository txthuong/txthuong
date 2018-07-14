# Test Name                       Description
# A_BX_AVMS_Download_0008         In case a user agreement is needed before the package download, verify that a new request for user agreement is returned by the device if the answer has not been given in time by the user
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
# A_BX_AVMS_Download_0008
# -----------------------------------------------------------------------------------

test_ID = "A_BX_AVMS_Download_0008"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print '%s: n case a user agreement is needed before the package download, verify that a new request for user agreement is returned by the device if the answer has not been given in time by the user' % test_ID
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

    print "\nStep 12: Waiting for 30 minutes later (default value of the timer) a new user agreement for download should be received"
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 2\r\n'], 1800000)

    print "\nStep 13: Accept download"
    SagSendAT(uart_com, 'AT+WDSR=3\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 9,*\r\n'], 35000)
    for iPercent in range (0, 101):
        if not SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 18,%d\r\n' % iPercent], 7000):
            break
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 10\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 12\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 4\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 6\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 23,1\r\n'], 30000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 3\r\n'], 30000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 8\r\n'], 90000)

    print "\nStep 14: Accept the installation"
    SagSendAT(uart_com, 'AT+WDSR=4\r')
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 14\r\n'], 10000)
    # Module reset to active new FW
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 20000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 0\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 16\r\n'], 10000)
    if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
        SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
    else:
        raise Exception("---->Problem: Module cannot reconnect to Wi-Fi network !!!")
    SagWaitnMatchResp(uart_com, ['*\r\n+WDSI: 4\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['*\r\n+WDSI: 6\r\n'], 30000)
    SagWaitnMatchResp(uart_com, ['*\r\n+WDSI: 23,1\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 8\r\n'], 90000)

    for retry in range(15):
        time.sleep(10)
        job_status = mySystem.getOperationTasksDetails(upgrade_job)
        print "\nInfo: Query server on %s time" %(retry+1)
        print "Job %s state = %s" %(upgrade_job, job_status)
        if job_status in ["SUCCESS"]:
            break
        if retry == 14:
            VarGlobal.statOfItem = "NOK"
            print "\n-------->Problem: Job not done, reach maximum retry times!!!\n\n"
    
    fw_rev = mySystem.readTreeNode("lwm2m.3.0.3")
    print "\n---->Info: Firmware version on server is: %s" % fw_rev
    print "\n---->Info: Firmware version in sample.cfg is: %s" % avms['upgrade_package_revision']
    if fw_rev != avms['upgrade_package_revision']:
        raise Exception("------>Problem: Upgrade FW is not successful!!!\n\n")

    print "\nStep 15: Set user agreement for package download to default"
    SagSendAT(uart_com, 'AT+WDSC=1,0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 4000)

    print "\nStep 16: Set user agreement for installation package to default"
    SagSendAT(uart_com, 'AT+WDSC=2,0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 4000)

    print "\nStep 17: Query Device Services configuration"
    SagSendAT(uart_com, 'AT+WDSC?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 2,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 3,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 4,15,60,240,960,2880,10080,10080\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+WDSC: 5,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nTest Steps completed\n"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT+RST\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

try:
    if mySystem.readTreeNode("lwm2m.3.0.3") != avms['fw_initial']:
        mySystem.cancelAllJobs()
        print "\nFall back to normal state"
        fallback_job = mySystem.installApplication(avms['package_name'],avms['package_revision'],avms['model'])
        SagSendAT(uart_com, 'AT+WDSS=1,1\r')
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 4000)
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 4\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 6\r\n'], 30000)
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 23,1\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 9,*\r\n'], 35000)
        for iPercent in range (0, 101):
            if not SagWaitnMatchResp(uart_com, ['*\r\n+WDSI: 18,%d\r\n' % iPercent], 7000):
                break
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 10\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 12\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 14\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 8\r\n'], 10000)
        # Module reset to active new FW
        SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 20000)
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 0\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 16\r\n'], 10000)
        if SagWaitnMatchResp(uart_com, ['*\r\n+SRWSTASTATUS: 1,"%s","%s",*,*\r\n' % (wifi_ssid, wifi_mac_addr)], 20000):
            SagWaitnMatchResp(uart_com, ['\r\n+SRWSTAIP: "%s.*","%s","%s"\r\n' % (return_subnet(wifi_dhcp_gateway), wifi_dhcp_subnet_mask, wifi_dhcp_gateway)], 10000)
        else:
            raise Exception("---->Problem: Module cannot reconnect to Wi-Fi network !!!")
        SagWaitnMatchResp(uart_com, ['*\r\n+WDSI: 4\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['*\r\n+WDSI: 6\r\n'], 30000)
        SagWaitnMatchResp(uart_com, ['*\r\n+WDSI: 23,1\r\n'], 10000)
        SagWaitnMatchResp(uart_com, ['\r\n+WDSI: 8\r\n'], 90000)

        for retry in range(15):
            time.sleep(10)
            job_status = mySystem.getOperationTasksDetails(upgrade_job)
            print "\nInfo: Query server on %s time" %(retry+1)
            print "Job %s state = %s" %(upgrade_job, job_status)
            if job_status in ["SUCCESS"]:
                break
            if retry == 14:
                VarGlobal.statOfItem = "NOK"
                print "\n-------->Problem: Job not done, reach maximum retry times!!!\n\n"

        fw_rev = mySystem.readTreeNode("lwm2m.3.0.3")
        print "\n---->Info: Firmware version on server is: %s" % fw_rev
        print "\n---->Info: Firmware version in sample.cfg is: %s" % avms['package_revision']
        if fw_rev != avms['package_revision']:
            raise Exception("------>Problem: Fall back FW is not successful!!!\n\n")

except Exception, err_msg :
    print Exception, err_msg

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
