# Test Name                                     Description
# A_BX_I2S_KI2SCFG_0001                         To check syntax and input values of AT command "+KI2SCFG"
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
# A_BX_I2S_KI2SCFG_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_I2S_KI2SCFG_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: To check syntax and input values of AT command +KI2SCFG" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: Check +KI2SCFG test command\n"
    SagSendAT(uart_com, 'AT+KI2SCFG=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 2: Check +KI2SCFG execute command\n"
    SagSendAT(uart_com, 'AT+KI2SCFG\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 3: Check +KI2SCFG write command\n"
    SagSendAT(uart_com, 'AT+KI2SCFG=0,1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 4: Check +KI2SCFG read command\n"
    SagSendAT(uart_com, 'AT+KI2SCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KI2SCFG: 0, 1, 0, 0, 26, 18, 33, 32\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KI2SCFG: 1, 0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 5: Check +KI2SCFG write command with port_number = '0','1'\n"
    for port_number in (0,1):
        SagSendAT(uart_com, 'AT+KI2SCFG=%s,1\r' %port_number)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        
    print "\nStep 6: Check +KI2SCFG write command with enable = '0','1'\n"
    for enable in (0,1):
        SagSendAT(uart_com, 'AT+KI2SCFG=1,%s\r' %enable)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Check +KI2SCFG write command with invalid port_number = '-'1','2,'*','$','100'\n"
    for port_number in ('-1','2','*','$','100'):
        SagSendAT(uart_com, 'AT+KI2SCFG=%s,1\r' %port_number)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 8: Check +KI2SCFG write command with invalid enable = '-'1','2,'*','$','100'\n"
    for enable in ('-1','2','*','$','100'):
        SagSendAT(uart_com, 'AT+KI2SCFG=1,%s\r' %enable)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 9: Check: AT+KI2SCFG?\n"
    SagSendAT(uart_com, 'AT+KI2SCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KI2SCFG: 0, 1, 0, 0, 26, 18, 33, 32\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KI2SCFG: 1, 1, 0, 0, 26, 18, 33, 32\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 10: Check +KI2SCFG write command with communication_format = '0','1','2','3'\n"
    for communication_format in (0,1,2,3):
        SagSendAT(uart_com, 'AT+KI2SCFG=1,1,%s,0,26,18,33,32\r' %communication_format)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 11: Check: AT+KI2SCFG?\n"
    SagSendAT(uart_com, 'AT+KI2SCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KI2SCFG: 0, 1, 0, 0, 26, 18, 33, 32\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KI2SCFG: 1, 1, 3, 0, 26, 18, 33, 32\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 12: Check +KI2SCFG write command with invalid communication_format = '-'1','2,'*','$','100'\n"
    for communication_format in ('-1','2','*','$','100'):
        SagSendAT(uart_com, 'AT+KI2SCFG=1,1,%s,0,26,18,33,32\r' %communication_format)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
        
    print "\nStep 13: Check +KI2SCFG write command with channel_format = '0','1','2','3','4'\n"
    for channel_format in (0,1,2,3,4):
        SagSendAT(uart_com, 'AT+KI2SCFG=1,1,0,%s,26,18,33,32\r' %channel_format)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 14: Check +KI2SCFG write command with invalid channel_format = '-'1','2,'*','$','100'\n"
    for channel_format in ('-1','2','*','$','100'):
        SagSendAT(uart_com, 'AT+KI2SCFG=1,1,0,%s,26,18,33,32\r' %channel_format)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 15: Check: AT+KI2SCFG?\n"
    SagSendAT(uart_com, 'AT+KI2SCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KI2SCFG: 0, 1, 0, 0, 26, 18, 33, 32\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KI2SCFG: 1, 1, 0, 4, 26, 18, 33, 32\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 16: Check +KI2SCFG write command with bckt = 26\n"
    SagSendAT(uart_com, 'AT+KI2SCFG=1,1,0,0,26,18,33,32\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 17: Check: AT+KI2SCFG?\n"
    SagSendAT(uart_com, 'AT+KI2SCFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+KI2SCFG: 0, 1, 0, 0, 26, 18, 33, 32\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+KI2SCFG: 1, 1, 0, 0, 26, 18, 33, 32\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)

    print "\nStep 18: Check +KI2SCFG write command with invalid bckt = '-'1','2,'*','$','100'\n"
    for bckt in ('-1','2','*','$','100'):
        SagSendAT(uart_com, 'AT+KI2SCFG=1,1,0,0,%s,18,33,32\r' %bckt)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 19: Check +KI2SCFG write command with ws = 18\n"
    SagSendAT(uart_com, 'AT+KI2SCFG=1,1,0,0,26,18,33,32\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 20: Check +KI2SCFG write command with invalid ws = '-'1','2,'*','$','100'\n"
    for ws in ('-1','2','*','$','100'):
        SagSendAT(uart_com, 'AT+KI2SCFG=1,1,0,0,26,%s,33,32\r' %ws)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 21: Check +KI2SCFG write command with data_out = 33\n"
    SagSendAT(uart_com, 'AT+KI2SCFG=1,1,0,0,26,18,33,32\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 22: Check +KI2SCFG write command with invalid data_out = '-'1','2,'*','$','100'\n"
    for data_out in ('-1','2','*','$','100'):
        SagSendAT(uart_com, 'AT+KI2SCFG=1,1,0,0,26,%s,33,32\r' %data_out)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 23: Check +KI2SCFG write command with data_in = 33\n"
    SagSendAT(uart_com, 'AT+KI2SCFG=1,1,0,0,26,18,33,32\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 24: Check +KI2SCFG write command with invalid data_in = '-'1','2,'*','$','100'\n"
    for data_in in ('-1','2','*','$','100'):
        SagSendAT(uart_com, 'AT+KI2SCFG=1,1,0,0,26,%s,33,32\r' %data_in)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 25: Missing parameter\n"
    SagSendAT(uart_com, 'AT+KI2SCFG=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 26: Missing parameter: port_number = 0, 1\n"
    for port_number in (0,1):
        SagSendAT(uart_com, 'AT+KI2SCFG=%s\r' %port_number)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 27: Extra parameter\n"
    SagSendAT(uart_com, 'AT+KI2SCFG=0,1,0,0,26,18,33,32,1\r')
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
SagSendAT(uart_com, "AT+KI2SCFG=0,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
SagSendAT(uart_com, "AT+KI2SCFG=1,0\r")
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)