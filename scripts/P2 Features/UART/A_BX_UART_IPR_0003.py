# Test Name                                     Description
# A_BX_UART_IPR_0003                            To check IPR setting is persistent after AT+RST and restore to default after factory reset
# 
# Requirement
# 1 Euler module
#    
# Author: ptnlam
#
# Jira ticket:
#-----------------------------------------------------------------------------------------------------

# -------------------------- DUT Initializion ----------------------------------

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
# A_BX_UART_IPR_0003
# -----------------------------------------------------------------------------------

test_ID = "A_BX_UART_IPR_0003"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: To check IPR setting is persistent after AT+RST and restore to default after factory reset" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Check UART baud rate configure\n"
    SagSendAT(uart_com, 'AT+IPR?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+IPR: 115200\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Set baudrate to 9600\n"
    SagSendAT(uart_com, 'AT+IPR=9600\r')

    print "\nStep 3: Try to send AT command\n"
    SagSendAT(uart_com, 'AT\r')
    resp = SagWaitResp(uart_com, ['\r\nOK\r\n'], 2000)
    if resp == '\r\nOK\r\n':
        VarGlobal.statOfItem = "NOK"
        print "----> Problem: Module still able to send AT command !!!"

    print "\nStep 4: Change the serial terminal software configuration to the new value then reconnect\n"
    SagClose(uart_com)
    uart_com = SagOpen(uart_com, 9600, 8, "N", 1, "None")

    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 5: Check UART baud rate configure\n"
    SagSendAT(uart_com, 'AT+IPR?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+IPR: 9600\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    SagSendAT(uart_com, 'AT\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 6: Perform AT+RST\n"
    SagSendAT(uart_com, 'AT+RST\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    
    print "\nStep 7: Check IPR setting\n"
    SagSendAT(uart_com, 'AT+IPR?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+IPR: 9600\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 8: Perform reset factory\n"
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    
    SagSendAT(uart_com, 'AT\r')
    
    print "\nStep 9: Reconnect with default setting\n"
    SagClose(uart_com)
    uart_com = SagOpen(uart_com, 115200, 8, "N", 1, "None")
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 10: Check UART baud rate configure\n"
    SagWaitnMatchResp(uart_com, ['\r\n+IPR: 115200\r\n'], 2000)
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

# Close UART
SagClose(uart_com)