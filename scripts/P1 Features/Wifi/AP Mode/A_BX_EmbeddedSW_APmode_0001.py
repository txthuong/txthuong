# Test Name                                     Description
# A_BX_EmbeddedSW_APmode_0001                   Check Syntax of write +SRWAPCFG command with valid values, invalid values and values out of range.
# 
# Requirement
#    1 Euler module
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
# A_BX_EmbeddedSW_APmode_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_APmode_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check Syntax of write +SRWAPCFG command with valid values, invalid values and values out of range." % test_ID
    print "*****************************************************************************************************************"
    
    wifi_ssid = 'euler_testing'
    
    print "\nStep 1: Execute command to enable module as Access Point mode\n"
    SagSendAT(uart1_com, 'AT+SRWCFG=2\r')
    SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Execute command with valid values to setup Access Point configurations\n"
    SagSendAT(uart1_com, 'AT+SRWAPCFG="%s","%s",4,5,0,100\r' %(wifi_ssid,wifi_password))
    SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Execute command to query current AP configurations\n"
    SagSendAT(uart1_com, 'AT+SRWAPCFG?\r')
    SagWaitnMatchResp(uart1_com, ['\r\n+SRWAPCFG: "%s","%s",4,5,0,100\r\n' %(wifi_ssid,wifi_password)], 2000)
    SagWaitnMatchResp(uart1_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: Execute command with invalid SSID to setup Access Point configurations\n"
    SagSendAT(uart1_com, 'AT+SRWAPCFG="012345678901234567890123456789012","123456789",4,5,0,100\r')
    SagWaitnMatchResp(uart1_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 5: Execute command with invalid Authentication mode to setup Access Point configurations\n"
    SagSendAT(uart1_com, 'AT+SRWAPCFG="eulertest","123456789",6,5,0,100\r')
    SagWaitnMatchResp(uart1_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 6: Execute command with invalid channel to setup Access Point configurations\n"
    SagSendAT(uart1_com, 'AT+SRWAPCFG="eulertest","123456789",4,15,2,100\r')
    SagWaitnMatchResp(uart1_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 7: Execute command with invalid Hidden SSID flag to setup Access Point configurations\n"
    SagSendAT(uart1_com, 'AT+SRWAPCFG="eulertest","123456789",4,5,3,100\r')
    SagWaitnMatchResp(uart1_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
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
SagSendAT(uart1_com, 'AT+SRWCFG=0\r')
SagWaitnMatchResp(uart1_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart1_com)
