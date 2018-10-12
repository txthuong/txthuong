# Test Name                             Description
# A_BX_EmbeddedSW_KCERTDELETE_0001      Check syntax for AT+KCERTDELETE command
#
# Requirement
#   1 Euler module
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
    SagSendAT(uart_com, "AT+FMM\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(uart_com, "AT+CGSN\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(uart_com, "ATI3\r")
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)

except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_EmbeddedSW_KCERTDELETE_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KCERTDELETE_0001"

#######################################################################################
#   START
#######################################################################################

try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "***********************************************************************************************************************"
    print "%s: Check syntax of command AT+KCERTDELETE" % test_ID
    print "***********************************************************************************************************************"

    print '\nStep 1: Check +KCERTDELETE test command'
    SagSendAT(uart_com, 'AT+KCERTDELETE=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print '\nStep 2: Check +KCERTDELETE execute command'
    SagSendAT(uart_com, 'AT+KCERTDELETE\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print '\nStep 3: Check +KCERTDELETE read command'
    SagSendAT(uart_com, 'AT+KCERTDELETE?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)

    print '\nStep 4: Check +KCERTDELETE write command with invalid parameter <data_type>'
    data_type = [-1, 2, 'a', 'A', '#', '$']
    for dt in data_type:
        SagSendAT(uart_com, 'AT+KCERTDELETE=%s\r' % dt)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print '\nStep 5: Check +KCERTDELETE write command with invalid parameter <index>'
    index_1 = [-1, 3, 3001]
    for data_type in (0, 1):
        for id in index_1:
            SagSendAT(uart_com, 'AT+KCERTDELETE=%s,%s\r' % (data_type, id))
            SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 918\r\n'], 2000)
    index_2 = ['a', 'A', '#', '$']
    for data_type in (0, 1):
        for id in index_2:
            SagSendAT(uart_com, 'AT+KCERTDELETE=%s,%s\r' % (data_type, id))
            SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print '\nStep 6: Check +KCERTDELETE write command with missing parameters'
    SagSendAT(uart_com, 'AT+KCERTDELETE=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KCERTDELETE=,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print '\nStep 7: Check +KCERTDELETE write command with extra parameter'
    SagSendAT(uart_com, 'AT+KCERTDELETE=0,0,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    SagSendAT(uart_com, 'AT+KCERTDELETE=1,0,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

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

# Close UART
SagClose(uart_com)
