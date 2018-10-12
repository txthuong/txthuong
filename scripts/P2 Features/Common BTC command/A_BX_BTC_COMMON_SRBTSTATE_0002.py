# Test Name                                     Description
# A_BX_BTC_COMMON_SRBTSTATE_0002                Check the function of command +SRBTSTATE
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

    # AUX Initialization
    print "\nOpen AT Command port"
    aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    # Display DUT information
    print "\nDisplay DUT information"
    print "\nGet model information"
    SagSendAT(aux1_com, 'AT+FMM\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux1_com, 'AT+CGSN\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux1_com, 'ATI3\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    # DUT Initialization
    print "\nInitiate DUT"
    SagSendAT(aux1_com, 'AT\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nAUX: Enable subsystem\n"
    SagSendAT(aux1_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
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
# A_BX_BTC_COMMON_SRBTSTATE_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BTC_COMMON_SRBTSTATE_0002"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "****************************************************************************************************************"
    print "%s: Check the function of command +SRBTSTATE" % test_ID
    print "*****************************************************************************************************************"
    
    print "\Check BT addr\n"
    SagSendAT(uart_com, 'AT+SRBTADDR?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTADDR: "%s"\r\n' %dut_bluetooth_address], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 1: Check read command\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTSTATE: 0,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 2: Disable Discoverable state of module\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,0\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 3: Query the Bluetooth state\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTSTATE: 1,0\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 4: Use smartphone or AUX module to scan this DUT\n"
    SagSendAT(aux1_com, 'AT+SRBLESCAN=10,0\r')
    res = SagWaitResp(aux1_com, [''], 20000)
    if dut_bluetooth_address in res:
        raise Exception("---->Problem: Cant scan this DUT => FAIL")
        VarGlobal.statOfItem == "NOK"

    print "\nStep 5: Check write command with lack of parameter\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 6: Check write command with lack of parameter\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=,1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    
    print "\nStep 7: Check write command extra parameters\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,2,1,1,a\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 8: Check write command with valid parameter\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=1,2\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 9: Check read command\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBTSTATE: 1,2\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 10: Check write command with connectable_mode = (0,1)\n"
    for i in ('0','1'):
        SagSendAT(uart_com, 'AT+SRBTSTATE=%s,2\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 11: Check write command with connectable_mode = (-1,2,100,*,#,$)\n"
    for i in ('-1','2','100','*','#','$'):
        SagSendAT(uart_com, 'AT+SRBTSTATE=%s,2\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
        
    print "\nStep 12: Check write command with discoverable_mode = (0,1,2)\n"
    for i in ('0','1','2'):
        SagSendAT(uart_com, 'AT+SRBTSTATE=1,%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
        
    print "\nStep 13: Check write command with discoverable_mode = (-1,3,100,*,#,$)\n"
    for i in ('*','#','$'):
        SagSendAT(uart_com, 'AT+SRBTSTATE=1,%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)

    print "\nStep 14: Set to default value\n"
    SagSendAT(uart_com, 'AT+SRBTSTATE=0,0\r')
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

SagSendAT(aux1_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
