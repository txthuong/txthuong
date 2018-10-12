# Test Name                                     Description
# A_BX_BLE_SRBLEADV_0001                        Check syntax of +SRBLEADV command with valid values, invalid values and values out of range
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
    
    print "\nDUT: Enable subsystem\n"
    SagSendAT(uart_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
except Exception, e:
    print "***** Test environment check fails !!!*****"
    print type(e)
    print e
    test_environment_ready = "Not_Ready"

print "\n------------Test Environment check: End------------"

print "\n----- Test Body Start -----\n"

# -----------------------------------------------------------------------------------
# A_BX_BLE_SRBLEADV_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLEADV_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s:Check syntax of +SRBLEADV command with valid values, invalid values and values out of range" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 3: Checking +SRBLEADV test command\n"
    SagSendAT(uart_com, 'AT+SRBLEADV=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 4: Checking +SRBLEADV read command\n"
    SagSendAT(uart_com, 'AT+SRBLEADV?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 5: Checking +SRBLEADV execute command\n"
    SagSendAT(uart_com, 'AT+SRBLEADV\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 6: Checking +SRBLEADV write command\n"
    SagSendAT(uart_com, 'AT+SRBLEADV=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: Checking +SRBLEADV write command for stop advertising\n"
    SagSendAT(uart_com, 'AT+SRBLEADV=0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 8: Checking +SRBLEADV write command for start advertising, set advertising data (Flag=0x06, Name=MyName, Service UUID16=ABCD), scan Response (TX Power level=-1) and start advertising\n"
    SagSendAT(uart_com, 'AT+SRBLEADV=1, "\\02\\01\\06\\07\\09\\4d\\79\\4e\\61\\6d\\65\\03\\03\\cd\\ab", "\\02\\0a\\ff"\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 9: Check write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADV=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 7: Check write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADV=1, "\\02\\01\\06\\07\\09\\4d\\79\\4e\\61\\6d\\65\\03\\03\\cd\\ab", "\\02\\0a\\ff",1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 8: Check write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLEADV=1, "\\02\\01\\06\\07\\09\\4d\\79\\4e\\61\\6d\\65\\03\\03\\cd\\ab", "\\02\\0a\\ff",1,a\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 9: Check write command with invalid parameter\n"
    for i in ('2','-1','50','a','#',';'):
        SagSendAT(uart_com, 'AT+SRBLEADV=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 10: Stop advertising\n"
    SagSendAT(uart_com, 'AT+SRBLEADV=0\r')
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

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)