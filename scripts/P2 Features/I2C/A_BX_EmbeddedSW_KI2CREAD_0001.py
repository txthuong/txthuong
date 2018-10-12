# Test Name                                     Description
# A_BX_EmbeddedSW_KI2CREAD_0001                 Check syntax for AT+KI2CREAD command
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
# A_BX_EmbeddedSW_KI2CREAD_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_EmbeddedSW_KI2CREAD_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax for AT+KI2CREAD command" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Enable I2C port number 0\n"
    SagSendAT(uart_com, 'AT+KI2CCFG=0,1,0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: Check +KI2CREAD test command\n"
    SagSendAT(uart_com, 'AT+KI2CREAD=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 3: Check +KI2CREAD execute command\n"
    SagSendAT(uart_com, 'AT+KI2CREAD\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 4: Check +KI2CREAD read command\n"
    SagSendAT(uart_com, 'AT+KI2CREAD?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 5: Check +KI2CREAD write command with valid parameters\n"
    SagSendAT(uart_com, 'AT+KI2CREAD=0,"\\6A","\\0F",1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KI2CREAD: "i"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 6: Check +KI2CREAD write command with valid parameters\n"
    SagSendAT(uart_com, 'AT+KI2CREAD=0,"\\6A",,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KI2CREAD: "\\00"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 7: Check +KI2CREAD write command with invalid parameter port_number = -1, 2, a, *\n"
    for port_number in ('-1','2','a','*'):
        SagSendAT(uart_com, 'AT+KI2CREAD=%s,"\\6A","\\5D",1\r' %port_number)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 8: Check +KI2CREAD write command with invalid parameter slave_addr = '\-1A','\GG','11','*','\123','\','/'\n"
    for slave_addr in ('"\\-1A"','"\\GG"','"11"','"*"','"\\123"','"\"','"/"'):
        SagSendAT(uart_com, 'AT+KI2CREAD=0,%s,"\\5D",1\r' %slave_addr)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 9: Check +KI2CREAD write command with invalid parameter opcode ='\-1A','\GG','11','*','\123','\','/'\n"
    for opcode in ('"\\-1A"','"\\GG"','"\"','"/"'):
        SagSendAT(uart_com, 'AT+KI2CREAD=0,%s,"\\5D",1\r' %opcode)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 10: Check +KI2CREAD write command with invalid parameter length_read_bytes = -1, 2, a, *\n"
    for length_read_bytes in ('-1','2','a','*'):
        SagSendAT(uart_com, 'AT+KI2CREAD=0,"\\6A","\\5D",%s\r' %length_read_bytes)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 11: Check +KI2CREAD write command with missing all parameters\n"
    SagSendAT(uart_com, 'AT+KI2CREAD=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 12: Check +KI2CREAD write command with missing parameters\n"
    SagSendAT(uart_com, 'AT+KI2CREAD=0\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 13: Check +KI2CREAD write command with missing parameters\n"
    SagSendAT(uart_com, 'AT+KI2CREAD=0,"\\6A"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 14: Check +KI2CREAD write command with missing parameters\n"
    SagSendAT(uart_com, 'AT+KI2CREAD=0,"\\6A",,\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 15: Check +KI2CREAD write command with missing parameters\n"
    SagSendAT(uart_com, 'AT+KI2CREAD=,"\\6A","\\5D",1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 16: Check +KI2CREAD write command with missing parameters\n"
    SagSendAT(uart_com, 'AT+KI2CREAD=0,"\\6A","\\5D",1,1,"a"\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
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

# Restore BT state to default
SagSendAT(uart_com, "AT+KI2CCFG=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)