# Test Name                                     Description
# A_BX_EmbeddedSW_APmode_0037                   Check command +SRWAPNETCFG is persistent after module resets
#
# Requirement
# 1 Euler module
#  
# Author: ptnlam
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
# A_BX_EmbeddedSW_APmode_0037
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_APmode_0037"

VarGlobal.statOfItem = "OK"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check command +SRWAPNETCFG is persistent after module resets" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Execute command to enable module as Access Point mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Query current Wifi operating mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWCFG: 2,0,"%s","%s"\r\n' %(dut_mac_address_sta, dut_mac_address)], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 3: Setup Access Point\n"
    SagSendAT(uart_com, 'AT+SRWAPCFG="%s","%s",4,11,0,100\r' %(wifi_ssid, wifi_password))
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Set up DHCP\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG=1,"192.168.0.1","192.168.0.2","192.168.0.101",720?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Query current DHCP setting\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPNETCFG: 1,"192.168.0.1","192.168.0.2","192.168.0.101",720\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 6: Reset module\n"
    SagSendAT(uart_com, 'AT+RST\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 3000)
    
    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Query current DHCP setting\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPNETCFG: 1,"192.168.0.1","192.168.0.2","192.168.0.101",720\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
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

# Restore DUT
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)