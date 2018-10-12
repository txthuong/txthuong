# Test Name                                     Description
# A_BX_BLE_SRBLECNX_0001                        Check syntax of +SRBLECNX command with valid values, invalid values and values out of range
# 
# Requirement
# 2 Euler modules
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
    
    # AUX1_UART Initialization
    print "\nOpen AT Command port"
    aux1_com = SagOpen(aux1_com, 115200, 8, "N", 1, "None")

    # Display AUX1 information
    print "\nDisplay AUX1 information"
    print "\nGet model information"
    SagSendAT(aux1_com, 'AT+FMM\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux1_com, 'AT+CGSN\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux1_com, 'ATI3\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nOK\r\n'], 2000)

    # AUX1 Initialization
    print "\nInitiate AUX1"
    SagSendAT(aux1_com, 'AT\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

    # Check BT name
    SagSendAT(uart_com, 'AT+SRBTNAME?\r')
    res = SagWaitResp(uart_com, ['\r\n+SRBTNAME: "*"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    uart_name = res.split ('"')[1]
    print uart_name
    
    SagSendAT(aux1_com, 'AT+SRBTNAME?\r')
    res = SagWaitResp(aux1_com, ['\r\n+SRBTNAME: "*"\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    aux1_name = res.split ('"')[1]
    print aux1_name
    
    #Get bluetooth address
    SagSendAT(uart_com, 'AT+SRBTADDR?\r')
    res = SagWaitResp(uart_com, ['\r\n+SRBTADDR: "*"\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    dut_bluetooth_addr = res.split ('"')[1]
    print dut_bluetooth_addr
    
    SagSendAT(aux1_com, 'AT+SRBTADDR?\r')
    res = SagWaitResp(aux1_com, ['\r\n+SRBTADDR: "*"\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    aux1_bluetooth_addr = res.split ('"')[1]
    print aux1_bluetooth_addr
    
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
# A_BX_BLE_SRBLECNX_0001
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLECNX_0001"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check syntax of +SRBLECNX command with valid values, invalid values and values out of range" % test_ID
    print "*****************************************************************************************************************"

    print "\nStep 1: Checking SRBLECNX test command\n"
    SagSendAT(uart_com, 'AT+SRBLECNX=?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 2: Checking SRBLECNX read command\n"
    SagSendAT(uart_com, 'AT+SRBLECNX?\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 3: Checking SRBLECNX execute command\n"
    SagSendAT(uart_com, 'AT+SRBLECNX\r')
    SagWaitnMatchResp(uart_com, ['\r\nERROR\r\n'], 2000)
    
    print "\nStep 4: Checking SRBLECNX write command (No BLE session exist)\n"
    SagSendAT(uart_com, 'AT+SRBLECNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
    print "\nStep 5: MA,MB: Check BLE connection status, no device registered\n"
    SagSendAT(uart_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 6: MB: Start advertising\n" 
    SagSendAT(aux1_com, 'AT+SRBLEADV=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 7: MA: Device A connects to device B (advertising)\n" 
    SagSendAT(uart_com, 'AT+SRBLECFG=%s\r' %aux1_bluetooth_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,0,"%s",23\r\n' %aux1_bluetooth_addr], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 8: MA: Initiate connection to device B\n" 
    SagSendAT(uart_com, 'AT+SRBLECNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 1,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBCSMART: 1,1,1\r\n'], 2000)
    
    print "\nStep 9: MB: Notification form MA\n" 
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLECFG: 1,0,"%s",23\r\n' %dut_bluetooth_addr], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLE_IND: 1,1\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    
    print "\nStep 11: MA: Query +SRBLECFG \n"
    SagSendAT(uart_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,1,"%s",23\r\n' %aux1_bluetooth_addr], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 12: MB: Query +SRBLECFG \n"
    SagSendAT(aux1_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLECFG: 1,1,"%s",23\r\n' %dut_bluetooth_addr], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    
    print "\nStep 13: MA: Disconnect from MB \n"
    SagSendAT(aux1_com, 'AT+SRBLECLOSE=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLE_IND: 1,0,22\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 1,0,19\r\n'], 2000)

    print "\nStep 14: Checking SRBLECNX write command with missing parameter\n"
    SagSendAT(uart_com, 'AT+SRBLECNX=\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 917\r\n'], 2000)
    
    print "\nStep 15: Checking SRBLECNX write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLECNX=1,1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)
    
    print "\nStep 16: Checking SRBLECNX write command with extra parameter\n"
    SagSendAT(uart_com, 'AT+SRBLECNX=1,1,a\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 915\r\n'], 2000)

    print "\nStep 17: Checking SRBLECNX write command with invalid parameter\n"
    for i in('a','*','%', '#'):
        SagSendAT(uart_com, 'AT+SRBLECNX=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 916\r\n'], 2000)
    SagSendAT(uart_com, 'AT+SRBLECNX=2\r')
    SagWaitnMatchResp(uart_com, ['\r\n+CME ERROR: 910\r\n'], 2000)
    
    print "\nStep 18: Delete the BLE configure\n"
    SagSendAT(uart_com, 'AT+SRBLEDEL=1\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+SRBLEDEL=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 3000)
    
    print "\nStep 19: Query +SRBLECFG \n"
    SagSendAT(uart_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    print "\nTest Steps completed\n"

except Exception, err_msg :
    VarGlobal.statOfItem = "NOK"
    print Exception, err_msg
    SagSendAT(uart_com, 'AT&F\r')
    SagWaitnMatchResp(uart_com, ['*\r\nREADY\r\n'], 2000)
    SagSendAT(aux1_com, 'AT&F\r')
    SagWaitnMatchResp(aux1_com, ['*\r\nREADY\r\n'], 2000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

# Close UART,AUX1
SagClose(uart_com)
SagClose(aux1_com)
