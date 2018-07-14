# Test Name                                     Description
# A_BX_EmbeddedSW_STAMode_0020                  Check syntax for +SRWSTANETCFG command
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
# A_BX_EmbeddedSW_STAMode_0020
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_STAMode_0020"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")
    
    print "*****************************************************************************************************************"
    print "%s:Check syntax for +SRWSTANETCFG command" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Check +SRWSTANETCFG test command\n"
    SagSendAT(uart_com, 'AT+SRWSTANETCFG=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 2: Checking +SRWSTANETCFG execute command\n"
    SagSendAT(uart_com, 'AT+SRWSTANETCFG\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 3: Checking +SRWSTANETCFG write command \n"
    SagSendAT(uart_com, 'AT+SRWSTANETCFG=0,"192.168.100.2","255.255.255.0","192.168.100.1"\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Query +SRWSTANETCFG configuration\n"
    SagSendAT(uart_com, 'AT+SRWSTANETCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRWSTANETCFG: 0,"192.168.100.2","255.255.255.0","192.168.100.1"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Checking +SRWSTANETCFG write command with invalid value\n"
    SagSendAT(uart_com, 'AT+SRWSTANETCFG=0,"192.168.100.500","255.255.255.0","192.168.100.1"\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 6: Checking +SRWSTANETCFG write command with invalid value\n"
    SagSendAT(uart_com, 'AT+SRWSTANETCFG=10,"192.168.100.1","255.255.255.0","192.168.100.1001"\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 7: Checking +SRWSTANETCFG write command with missing parmameter\n"
    SagSendAT(uart_com, 'AT+SRWSTANETCFG=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 8: Checking +SRWSTANETCFG write command with extra parmameter\n"
    SagSendAT(uart_com, 'AT+SRWSTANETCFG=0,"192.168.100.2","255.255.255.0","192.168.100.100",0,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 9: Checking +SRWSTANETCFG read command with extra parmameter\n"
    SagSendAT(uart_com, 'AT+SRWSTANETCFG?10\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
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
