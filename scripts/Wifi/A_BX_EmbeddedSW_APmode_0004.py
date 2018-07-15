# Test Name                                     Description
# A_BX_EmbeddedSW_APmode_0004                   Use command +SRWAPCFG to configure Hide SSID

#
# Requirement
# 2 Euler module
#  
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
    
    
    # AUX1_UART Initialization
    print "\nOpen AT Command port"
    aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    # Display AUX1 information
    print "\nDisplay AUX1 information"
    print "\nGet model information"
    SagSendAT(aux1_com, 'AT+FMM\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux1_com, 'AT+CGSN\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux1_com, 'ATI3\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    # AUX1 Initialization
    print "\nInitiate AUX1"
    SagSendAT(aux1_com, 'AT\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_APmode_0004
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_APmode_0004"

VarGlobal.statOfItem = "OK"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready":
        VarGlobal.statOfItem = "NOK"
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Use command +SRWAPCFG to configure Hide SSID." % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Enable module A as Access Point mode\n"
    SagSendAT(uart_com, 'AT+SRWCFG=2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 10000)
    
    print "\nStep 2: 'Setup Access Point with Hide SSID:\n"
    SagSendAT(uart_com, 'AT+SRWAPCFG="eulertest","123456789",4,5,1,100\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 10000)
    
    print "\nStep 3: Query current AP configurations\n"
    SagSendAT(uart_com, 'AT+SRWAPCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPCFG: "eulertest","123456789",4,5,1,100\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 10000)
    
    print "\nStep 4: Use module B to scan Hidden SSID\n"
    SagSendAT(aux1_com, 'AT+SRWSTASCN\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 40000)
    
    print "\nStep 5:Setup module B Station configurations\n"
    SagSendAT(aux1_com, 'AT+SRWSTACFG="eulertest","123456789",1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 10000)
    
    print "\nStep 6: Connect to Access Point (module A) from module B\n"
    SagSendAT(aux1_com, 'AT+SRWSTACON=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 10000)
    SagWaitnMatchResp(aux1_com, ['*\r\n+SRWSTASTATUS: 1,"eulertest","*:*:*:*:*:*",*,*\r\n'], 10000)
    SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTAIP: "192.168.*.*","255.255.255.0","192.168.*.1"\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 1,"*:*:*:*:*:*"\r\n'], 10000)
    
    print "\nStep 7: List associated (connected) Wi-Fi stations in module A\n"
    SagSendAT(uart_com, 'AT+SRWAPSTA?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 1,"*:*:*:*:*:*","*.*.*.*"\r\n'], 10000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 10000)
    
    print "\nTest Steps completed\n"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

#Disconnect
SagSendAT(aux1_com, 'AT+SRWSTACFG="a","12345678x@X",0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 10000)

SagSendAT(aux1_com, 'AT+SRWSTACON=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 10000)
SagWaitnMatchResp(aux1_com, ['\r\n+SRWSTASTATUS: 0,8\r\n'], 10000)
SagWaitnMatchResp(uart_com, ['\r\n+SRWAPSTA: 0,"*:*:*:*:*:*"\r\n'], 10000)

# Restore DUT
SagSendAT(uart_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 10000)

SagSendAT(aux1_com, 'AT+SRWCFG=3\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 10000)

# Close UART
# SagClose(uart_com)
# SagClose(aux1_com)