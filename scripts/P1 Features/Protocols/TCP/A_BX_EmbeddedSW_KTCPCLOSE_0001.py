# Test Name                                     Description
# A_BX_EmbeddedSW_KTCPCLOSE_0001                To check syntax and input range for the AT command "+KTCPCLOSE", Close Current TCP Operation
#
# Requirement
#   1 Euler module
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
    
    # Display DUT Information
    print "\nDisplay DUT information"
    print "\nGet model information"
    SagSendAT(uart_com, 'AT+FMM\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nGet serial number"
    SagSendAT(uart_com, 'AT+CGSN\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'], 2000)
    
    print "\nGet revision information"
    SagSendAT(uart_com, 'ATI3\r')
    SagWaitnMatchResp(uart_com, ['*\r\nOK\r\n'] , 2000)
    
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
# A_BX_EmbeddedSW_KTCPCLOSE_0001
# -----------------------------------------------------------------------------------
    
test_ID = "A_BX_EmbeddedSW_KTCPCLOSE_0001"
    
#######################################################################################
#   START
#######################################################################################
    
try:
    
    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")
    
    print "***************************************************************************************************************"
    print "%s:To check syntax and input range for the AT command +KTCPCLOSE, Close Current TCP Operation" % test_ID
    print "***************************************************************************************************************"
    
    print '\nStep 1: Check read command\n'
    SagSendAT(uart_com, 'AT+KTCPCLOSE?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print '\nStep 2: Check execute command\n'
    SagSendAT(uart_com, 'AT+KTCPCLOSE\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print '\nStep 3: Check test command\n'
    SagSendAT(uart_com, 'AT+KTCPCLOSE=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print '\nStep 4: Check command with missing parameter\n'
    SagSendAT(uart_com, 'AT+KTCPCLOSE=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print '\nStep 5: Check command without parameter\n'
    SagSendAT(uart_com, 'AT+KTCPCLOSE\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print '\nStep 6: Check command with extra parameter\n'
    SagSendAT(uart_com, 'AT+KTCPCLOSE=1,1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
    print '\nStep 7: Checking <session_id>from 1 to 200\n'
    for i in range(1,201):
        SagSendAT(uart_com, 'AT+KTCPCLOSE=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
    print '\nStep 8: Checking <session_id> =[0,201] [a,$,*]\n'
    col_num = ['0','201']
    col_text =[ 'a','$','*']
    for i in col_num:
        SagSendAT(uart_com, 'AT+KTCPCLOSE=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
    for i in col_text:
        SagSendAT(uart_com, 'AT+KTCPCLOSE=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print '\nStep 9: Checking <session_id> =[0,201] [a,$,*]\n'
    for i in col_num:
        SagSendAT(uart_com, 'AT+KTCPCLOSE=%s,1\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
    for i in col_text:
        SagSendAT(uart_com, 'AT+KTCPCLOSE=%s,1\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print '\nStep 10: Checking <closing_type> =[0,2] [a,$,*]\n'
    for i in col_num:
        SagSendAT(uart_com, 'AT+KTCPCLOSE=1,%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
    for i in col_text:
        SagSendAT(uart_com, 'AT+KTCPCLOSE=1,%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
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
