# Test Name                                     Description
# A_BX_EmbeddedSW_APmode_0022                   Use command +SRWAPNETCFG to configure DHCP disabled
#
# Requirement
# 2 Euler modules
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

    # DUT Initialization
    print "\nInitiate DUT"
    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_APmode_0022
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_APmode_0022"

VarGlobal.statOfItem = "OK"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s:Use command +SRWAPNETCFG to configure DHCP disabled" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Execute command to enable module as Access Point mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 2: Enable DHCP with valid values\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG=1,"192.168.0.1","192.168.0.2","192.168.0.101",720\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Query current DHCP setting\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPNETCFG: 1,"192.168.0.1","192.168.0.2","192.168.0.101",720\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Disable DHCP \n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG=0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Query DHCP value again\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPNETCFG: 0,"192.168.0.1","192.168.0.2","192.168.0.101",720\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 6: Enable DHCP:\n"
    SagSendAT(uart_com, 'AT+SRWAPNETCFG=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Query DHCP value again\n"
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

# Close UART, AUX1
SagClose(uart_com)
SagClose(aux1_com)

