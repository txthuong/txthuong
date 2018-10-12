# Test Name                                     Description
# A_BX_EmbeddedSW_KI2CREAD_0005                 Check data is written and read correctly
# 
# Requirement
# 1 Euler module
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
# A_BX_EmbeddedSW_KI2CREAD_0005
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KI2CREAD_0005"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check data is written and read correctly" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Read default I2C configure"
    SagSendAT(uart_com, 'AT+KI2CCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KI2CCFG: 0,0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KI2CCFG: 1,0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 2: Enable I2C port 0 with low mode"
    SagSendAT(uart_com, 'AT+KI2CCFG=0,1,0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: Query I2C configure"
    SagSendAT(uart_com, 'AT+KI2CCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KI2CCFG: 0,1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KI2CCFG: 1,0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    slave_addr = '6A'
    opcode = '5E'

    for i in range(33, 127):
        data_hex = format(i, "02x")
        data_ascii = data_hex.decode("hex")

        print "\nStep 4: Perform +KI2CWRITE command with port 0"
        SagSendAT(uart_com, 'AT+KI2CWRITE=0,"\\%s","\\%s\\%s"\r' % (slave_addr, opcode, data_hex))
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 5: Read the written data"
        SagSendAT(uart_com, 'AT+KI2CREAD=0,"\\%s","\\%s",1\r' % (slave_addr, opcode))
        SagWaitnMatchResp(uart_com, ['\r\n+KI2CREAD: "%s"\r\n' % data_ascii], 2000)
        SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 6: Enable I2C port 0 with fast mode"
    SagSendAT(uart_com, 'AT+KI2CCFG=0,1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 7: Query I2C configure"
    SagSendAT(uart_com, 'AT+KI2CCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KI2CCFG: 0,1,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KI2CCFG: 1,0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    for i in range(33, 127):
        data_hex = format(i, "02x")
        data_ascii = data_hex.decode("hex")

        print "\nStep 8: Perform +KI2CWRITE command with port 0"
        SagSendAT(uart_com, 'AT+KI2CWRITE=0,"\\%s","\\%s\\%s"\r' % (slave_addr, opcode, data_hex))
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

        print "\nStep 9: Read the written data"
        SagSendAT(uart_com, 'AT+KI2CREAD=0,"\\%s","\\%s",1\r' % (slave_addr, opcode))
        SagWaitnMatchResp(uart_com, ['\r\n+KI2CREAD: "%s"\r\n' % data_ascii], 2000)
        SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

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

# Restore BT state to default
SagSendAT(uart_com, "AT+KI2CCFG=0,0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)