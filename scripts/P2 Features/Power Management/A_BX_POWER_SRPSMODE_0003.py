# Test Name                                Description
# A_BX_POWER_SRPSMODE_0003                 Check if setting is persistent after module wake up from light sleep mode
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

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_POWER_SRPSMODE_0003
# -----------------------------------------------------------------------------------

test_ID = "A_BX_POWER_SRPSMODE_0003"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***************************************************************************************************************"
    print "%s: Check if setting is persistent after module wake up from light sleep mode" % test_ID
    print "***************************************************************************************************************"

    print "\nStep 1: Query power saving configuration"
    SagSendAT(uart_com, "AT+SRPSCFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRPSCFG: 0,0,0'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    timer = 10

    print "\nStep 2: Configure Power Saving with Wakeup mode: Timer and timer is %s seconds" % timer
    SagSendAT(uart_com, "AT+SRPSCFG=1,%s\r" % timer)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Query Power Saving Configuration"
    SagSendAT(uart_com, "AT+SRPSCFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRPSCFG: 1,%s' % timer], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 4: Configure a HTTP connection"
    SagSendAT(uart_com, "AT+KHTTPCFG=,%s\r" % http_server)
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPCFG: 1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 5: Query HTTP Configuration"
    SagSendAT(uart_com, "AT+KHTTPCFG?\r")
    SagWaitnMatchResp(uart_com, ['+KHTTPCFG: 1,,"%s",80,0,,,0,0\r\n' % http_server], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 6: Configure a HTTPS connection"
    SagSendAT(uart_com, "AT+KHTTPSCFG=,%s\r" % https_server)
    SagWaitnMatchResp(uart_com, ['\r\n+KHTTPSCFG: 2\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 7: Query HTTP Configuration"
    SagSendAT(uart_com, "AT+KHTTPSCFG?\r")
    SagWaitnMatchResp(uart_com, ['+KHTTPSCFG: 2,,"%s",443,0,0,1,,,0,0,2,2\r\n' % https_server], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 8: Configure a TCP connection"
    SagSendAT(uart_com, 'AT+KTCPCFG=,0,"%s",%s\r' % (tcp_server, tcp_port))
    SagWaitnMatchResp(uart_com, ['+KTCPCFG: 3\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 9: Query TCP Configuration"
    SagSendAT(uart_com, "AT+KTCPCFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: 3,0,,0,"%s",%s,,1,0\r\n' % (tcp_server, tcp_port)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 10: Configure a SPP connection"
    SagSendAT(uart_com, 'AT+SRSPPCFG="ff:ff:ff:ff:ff:ff"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 4,0,"ff:ff:ff:ff:ff:ff",SPP,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 11: Query SPP Configuration"
    SagSendAT(uart_com, "AT+SRSPPCFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 4,0,"ff:ff:ff:ff:ff:ff",SPP,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 12: Configure a SPP connection"
    SagSendAT(uart_com, 'AT+SRBLECFG="aa:bb:cc:33:22:11"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 5,0,"aa:bb:cc:33:22:11",23'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 13: Query SPP Configuration"
    SagSendAT(uart_com, "AT+SRBLECFG?\r")
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 5,0,"aa:bb:cc:33:22:11",23'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 14: Perform +SRPSMODE to put module to light sleep mode"
    wait_time = timer * 1000 + 2000
    SagSendAT(uart_com, 'AT+SRPSMODE=0\r')
    print "\nWaiting for module wake up from light sleep mode after %s seconds" % timer
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], wait_time)

    print "\nStep 15: Query Configuration"
    SagSendAT(uart_com, "AT+SRPSCFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\n+SRPSCFG: 1,%s' % timer], 2000):
        print '----> Problem: The configure is not preserved from light sleep mode!!!'
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+KHTTPCFG?\r")
    if not SagWaitnMatchResp(uart_com, ['+KHTTPCFG: 1,,"%s",80,0,,,0,0\r\n' % http_server], 2000):
        print '----> Problem: The configure is not preserved from light sleep mode!!!'
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+KHTTPSCFG?\r")
    if not SagWaitnMatchResp(uart_com, ['+KHTTPSCFG: 2,,"%s",443,0,0,1,,,0,0,2,2\r\n' % https_server], 2000):
        print '----> Problem: The configure is not preserved from light sleep mode!!!'
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+KTCPCFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\n+KTCPCFG: 3,0,,0,"%s",%s,,1,0' % (tcp_server, tcp_port)], 2000):
        print '----> Problem: The configure is not preserved from light sleep mode!!!'
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+SRSPPCFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\n+SRBTCFG: 4,0,"ff:ff:ff:ff:ff:ff",SPP,0'], 2000):
        print '----> Problem: The configure is not preserved from light sleep mode!!!'
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 5,0,"aa:bb:cc:33:22:11",23'], 2000):
        print '----> Problem: The configure is not preserved from light sleep mode!!!'
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 16: Delete configuration"
    SagSendAT(uart_com, "AT+KHTTPDEL=1\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+KHTTPSDEL=2\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+KTCPDEL=3\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+SRSPPDEL=4\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagSendAT(uart_com, "AT+SRBLEDEL=5\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 17: Query configuration"
    SagSendAT(uart_com, "AT+KHTTPCFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        print '----> Problem: The HTTTP configure is not deleted properly!!!'
    SagSendAT(uart_com, "AT+KHTTPSCFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        print '----> Problem: The HTTTPS configure is not deleted properly!!!'
    SagSendAT(uart_com, "AT+KTCPCFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        print '----> Problem: The TCP configure is not deleted properly!!!'
    SagSendAT(uart_com, "AT+SRSPPCFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        print '----> Problem: The SPP configure is not deleted properly!!!'
    SagSendAT(uart_com, "AT+SRBLECFG?\r")
    if not SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000):
        print '----> Problem: The BLE configure is not deleted properly!!!'

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

# Restore Power Saving Configuration to default
SagSendAT(uart_com, 'AT+SRPSCFG=0,0,0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
