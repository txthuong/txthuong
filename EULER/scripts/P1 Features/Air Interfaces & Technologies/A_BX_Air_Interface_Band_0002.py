# Test Name                        Description
# A_BX_AirInterface_Band_0002      BX module should play the role as Access Point that smart phone can access to
#
# Requirement
#   1 Euler module
#   1 SmartPhone
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
    SagWaitnMatchResp(UART1, ['\r\nREADY\r\n'], 2000)

    # Display DUT information
    print "\nDisplay DUT information"
    print "\nGet model information"
    SagSendAT(UART1, "AT+FMM\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(uart_com, "AT+CGSN\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(uart_com, "ATI3\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    # DUT Initialization
    print "\nInitiate DUT"
    print "\nReset DUT"
    SagSendAT(uart_com, "AT+RST\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*READY\r\n'], 2000)

    SagSendAT(uart_com, "AT\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_AirInterface_Band_0002
# -----------------------------------------------------------------------------------
test_nb=""
test_ID = "A_BX_AirInterface_Band_0002"

VarGlobal.statOfItem = "OK"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")
        
    print "***********************************************************************************************************************"
    print "%s: BX module should play the role as Access Point that smart phone can access to" % test_ID
    print "***********************************************************************************************************************"
    
    print "\nStep 1: Configures module as Access Point mode\n"
    SagSendAT(uart_com, "AT+SRWCFG=2\r")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Configures the Access Point information\n"
    SagSendAT(uart_com, 'AT+SRWAPCFG="%s","%s",4,5,0,100\r' % (wifi_ssid, wifi_mac_addr))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Configures the network for AP interface\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG=1,"192.168.0.1","192.168.0.2","192.168.0.101",720\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    wx.MessageBox('User SmartPhone to connect to SSID "AP_EULER" then click "OK"', 'Info',wx.OK)
    
    print "\nStep 4: Check response message on module\n"
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 1,"*:*:*:*:*:*"\r\n'], 2000)

    print "\nTest Steps completed\n"
    
except Exception, err_msg :
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 3000)
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

# Restore DUT
SagSendAT(uart_com, 'AT+SRWAPNETCFG=0,"192.168.0.1","192.168.0.2","192.168.0.101",720\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
# Close UART
SagClose(uart_com)
