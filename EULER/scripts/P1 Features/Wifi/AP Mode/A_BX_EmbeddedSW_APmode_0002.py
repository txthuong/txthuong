# Test Name                                     Description
# A_BX_EmbeddedSW_APmode_0002                   Check Syntax of write +SRWAPNETCFG command with valid values, invalid values and values out of range
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
    uart1_com = SagOpen(uart_com, 115200, 8, "N", 1, "None")

    # Display DUT information
    print "\nDisplay DUT information"
    print "\nGet model information"
    SagSendAT(uart1_com, 'AT+FMM\r')
    SagWaitnMatchResp(uart1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(uart1_com, 'AT+CGSN\r')
    SagWaitnMatchResp(uart1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(uart1_com, 'ATI3\r')
    SagWaitnMatchResp(uart1_com, ['*\r\nOK\r\n'], 2000)

    # DUT Initialization
    print "\nInitiate DUT"
    SagSendAT(uart1_com, 'AT\r')
    SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_APmode_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_APmode_0002"

VarGlobal.statOfItem = "OK"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check Syntax of write +SRWAPNETCFG command with valid values, invalid values and values out of range" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Execute command to enable module as Access Point mode\n"
    SagSendAT(uart1_com, 'AT+SRWCFG=2\r')
    SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: 'Execute command to enable DHCP with valid values\n"
    SagSendAT(uart1_com, 'AT+SRWAPNETCFG=1,"192.168.0.1","192.168.0.2","192.168.0.101",720\r')
    SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Execute command to enable DHCP with invalid values (exceed DHCP pool size)\n"
    SagSendAT(uart1_com, 'AT+SRWAPNETCFG=1,"192.168.0.1","192.168.0.2","192.168.0.103",720\r')
    SagWaitnMatchResp(uart1_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 4: Execute command to enable DHCP with invalid values (start DHCP IP address is same with IP address of module)\n"
    SagSendAT(uart1_com, 'AT+SRWAPNETCFG=1,"192.168.0.1","192.168.0.1","192.168.0.100",720\r')
    SagWaitnMatchResp(uart1_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 5:Execute command to enable DHCP with invalid values (end DHCP IP address is less than start IP address)\n"
    SagSendAT(uart1_com, 'AT+SRWAPNETCFG=1,"192.168.0.1","192.168.0.10","192.168.0.9",720\r')
    SagWaitnMatchResp(uart1_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 6: Query current DHCP settings\n"
    SagSendAT(uart1_com, 'AT+SRWAPNETCFG?\r')
    SagWaitnMatchResp(uart1_com, ['\r\n+SRWAPNETCFG: 1,"192.168.0.1","192.168.0.2","192.168.0.101",720\r\n'], 2000)
    SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Execute command to disable DHCP\n"
    SagSendAT(uart1_com, 'AT+SRWAPNETCFG=0\r')
    SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 8: Query current DHCP settings\n"
    SagSendAT(uart1_com, 'AT+SRWAPNETCFG?\r')
    SagWaitnMatchResp(uart1_com, ['\r\n+SRWAPNETCFG: 0,"192.168.0.1","192.168.0.2","192.168.0.101",720\r\n'], 2000)
    SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 9: Execute command to enable DHCP\n"
    SagSendAT(uart1_com, 'AT+SRWAPNETCFG=1\r')
    SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep10: Query current DHCP settings\n"
    SagSendAT(uart1_com, 'AT+SRWAPNETCFG?\r')
    SagWaitnMatchResp(uart1_com, ['\r\n+SRWAPNETCFG: 1,"192.168.0.1","192.168.0.2","192.168.0.101",720\r\n'], 2000)
    SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)
    
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

#Disable DHCP
SagSendAT(uart1_com, 'AT+SRWAPNETCFG=0\r')
SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)

# Restore DUT
SagSendAT(uart1_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart1_com)
