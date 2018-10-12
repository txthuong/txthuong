# Test Name                                     Description
# A_BX_UART_IPR_0002                            To check AT+IPR set fixed UART baud rate
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
    uart_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

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
# A_BX_UART_IPR_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_UART_IPR_0002"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: To check AT+IPR set fixed UART baud rate" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Check UART baud rate configure\n"
    SagSendAT(uart_com, 'AT+IPR?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+IPR: 115200\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    for baudrate in (600, 1200, 2400, 4800, 14400, 19200, 38400, 57600, 115200, 128000, 256000, 1024000, 2048000):
        print "\nStep 2: Set baudrate %s\n" % baudrate
        SagSendAT(uart_com, 'AT+IPR=%s\r' % baudrate)
        SagSleep(2000)

        print "\nStep 3: Try to send AT command\n"
        SagSendAT(uart_com, 'AT\r')
        resp = SagWaitResp(uart_com, [''], 2000)
        if resp != '':
            VarGlobal.statOfItem = "NOK"
            print "----> Problem: Module still receive response from UART with different baudrate !!!"

        print "\nStep 4: Change the serial terminal software configuration to the new value then reconnect\n"
        SagClose(uart_com)
        uart_com = SagOpen(aux1_com, baudrate, 8, "N", 1, "None")
        SagSleep(2000)

        SagSendAT(uart_com, 'AT\r')
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 5: Check UART baud rate configure\n"
        SagSendAT(uart_com, 'AT+IPR?\r')
        SagWaitnMatchResp(uart_com, ['\r\n+IPR: %s\r\n' % baudrate], 2000)
        SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

        SagSendAT(uart_com, 'AT\r')
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 6: Change baudrate back default"
    SagSendAT(uart_com, 'AT+IPR=115200\r')
    SagSleep(2000)

    SagClose(uart_com)
    uart_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")
    SagSleep(2000)

    SagSendAT(uart_com, 'AT\r')
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
