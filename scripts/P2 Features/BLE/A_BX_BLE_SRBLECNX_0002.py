# Test Name                                     Description
# A_BX_BLE_SRBLECNX_0002                        Check if connect with multiple device
# 
# Requirement
# 3 Euler modules
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
    
    # AUX1_UART Initialization
    print "\nOpen AT Command port"
    aux2_com = SagOpen(aux2_com, 115200, 8, "N", 1, "None")

    # Display AUX1 information
    print "\nDisplay AUX1 information"
    print "\nGet model information"
    SagSendAT(aux2_com, 'AT+FMM\r')
    SagWaitnMatchResp(aux2_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet serial number"
    SagSendAT(aux2_com, 'AT+CGSN\r')
    SagWaitnMatchResp(aux2_com, ['*\r\nOK\r\n'], 2000)

    print "\nGet revision information"
    SagSendAT(aux2_com, 'ATI3\r')
    SagWaitnMatchResp(aux2_com, ['*\r\nOK\r\n'], 2000)

    # AUX1 Initialization
    print "\nInitiate AUX1"
    SagSendAT(aux2_com, 'AT\r')
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

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
    
    SagSendAT(aux2_com, 'AT+SRBTNAME?\r')
    res = SagWaitResp(aux2_com, ['\r\n+SRBTNAME: "*"\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)
    aux2_name = res.split ('"')[1]
    print aux2_name
    
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
    
    SagSendAT(aux2_com, 'AT+SRBTADDR?\r')
    res = SagWaitResp(aux2_com, ['\r\n+SRBTADDR: "*"\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['OK\r\n'], 2000)
    aux2_bluetooth_addr = res.split ('"')[1]
    print aux2_bluetooth_addr
    
    print "\nAUX: Enable subsystem\n"
    SagSendAT(aux1_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    print "\nAUX: Enable subsystem\n"
    SagSendAT(aux2_com, 'AT+SRBTSYSTEM=1\r')
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)
    
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
# A_BX_BLE_SRBLECNX_0002
# -----------------------------------------------------------------------------------

test_ID = "A_BX_BLE_SRBLECNX_0002"

#######################################################################################
#   START
#######################################################################################
try:

    if test_environment_ready == "Not_Ready" or VarGlobal.statOfItem == "NOK":
        raise Exception("---->Problem: Test Environment Is Not Ready !!!")

    print "*****************************************************************************************************************"
    print "%s: Check if connect with multiple device" % test_ID
    print "*****************************************************************************************************************"
    
    print "\nStep 1: MA,MB,MC: Check BLE connection status, no device registered\n"
    SagSendAT(uart_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux2_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)
    
    print "\nStep 2: MB,MC: Start advertising\n" 
    SagSendAT(aux1_com, 'AT+SRBLEADV=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux2_com, 'AT+SRBLEADV=1\r')
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

    print "\nStep 3: MA: Device A scans while device B and C are advertising\n"
    SagSendAT(uart_com,'AT+SRBLESCAN=2,0\r')
    resp = SagWaitResp(uart_com, [''], 20000)
    if aux1_bluetooth_addr not in resp:
        raise Exception ("Device A does not scans device B")
    if aux2_bluetooth_addr not in resp:
        raise Exception ("Device A does not scans device C")
    
    print "\nStep 4: MA: Device A connects to device B (advertising)\n" 
    SagSendAT(uart_com, 'AT+SRBLECFG=%s\r' %aux1_bluetooth_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,0,"%s",23\r\n' %aux1_bluetooth_addr], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 5: MA: Initiate connection to device B\n" 
    SagSendAT(uart_com, 'AT+SRBLECNX=1\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 1,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBCSMART: 1,1,1\r\n'], 2000)
    
    print "\nStep 6: MB: Notification form MA\n" 
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLECFG: 1,0,"%s",23\r\n' %dut_bluetooth_addr], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLE_IND: 1,1\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    
    print "\nStep 7: MA: Query +SRBLECFG \n"
    SagSendAT(uart_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,1,"%s",23\r\n' %aux1_bluetooth_addr], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
        
    print "\nStep 8: MB: Query +SRBLECFG \n"
    SagSendAT(aux1_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLECFG: 1,1,"%s",23\r\n' %dut_bluetooth_addr], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    
    print "\nStep 9: MA: Device A connects to device C (advertising)\n" 
    SagSendAT(uart_com, 'AT+SRBLECFG=%s\r' %aux2_bluetooth_addr)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 2,0,"%s",23\r\n' %aux2_bluetooth_addr], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 10: MA: Initiate connection to device B\n" 
    SagSendAT(uart_com, 'AT+SRBLECNX=2\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 2,1\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 2,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLEMTU: 2,23\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBCSMART: 2,1,1\r\n'], 2000)
    
    print "\nStep 11: MC: Notification form MA\n" 
    SagWaitnMatchResp(aux2_com, ['\r\n+SRBLECFG: 1,0,"%s",23\r\n' %dut_bluetooth_addr], 2000)
    SagWaitnMatchResp(aux2_com, ['+SRBLE_IND: 1,1\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['+SRBLEMTU: 1,23\r\n'], 2000)
    
    print "\nStep 12: MA: Query +SRBLECFG \n"
    SagSendAT(uart_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLECFG: 1,1,"%s",23\r\n' %aux1_bluetooth_addr], 2000)
    SagWaitnMatchResp(uart_com, ['+SRBLECFG: 2,1,"%s",23\r\n' %aux2_bluetooth_addr], 2000)
    SagWaitnMatchResp(uart_com, ['OK\r\n'], 2000)
    
    print "\nStep 13: MC: Query +SRBLECFG \n"
    SagSendAT(aux2_com, 'AT+SRBLECFG?\r')
    SagWaitnMatchResp(aux2_com, ['\r\n+SRBLECFG: 1,1,"%s",23\r\n' %dut_bluetooth_addr], 2000)
    SagWaitnMatchResp(aux2_com, ['OK\r\n'], 2000)
    
    print "\nStep 14: MA: Disconnect from MB \n"
    SagSendAT(aux1_com, 'AT+SRBLECLOSE=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\n+SRBLE_IND: 1,0,22\r\n'], 2000)
    SagWaitnMatchResp(aux1_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 1,0,19\r\n'], 2000)
    
    print "\nStep 15: MA: Disconnect from MC \n"
    SagSendAT(aux2_com, 'AT+SRBLECLOSE=1\r')
    SagWaitnMatchResp(aux2_com, ['\r\n+SRBLE_IND: 1,0,22\r\n'], 2000)
    SagWaitnMatchResp(aux2_com, ['OK\r\n'], 2000)
    SagWaitnMatchResp(uart_com, ['\r\n+SRBLE_IND: 2,0,19\r\n'], 2000)
        
    print "\nStep 16: Delete the BLE configure\n"
    for i in (1,2):
        SagSendAT(uart_com, 'AT+SRBLEDEL=%s\r' %i)
        SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)
    
    SagSendAT(aux1_com, 'AT+SRBLEDEL=1\r')
    SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 3000)
    
    SagSendAT(aux2_com, 'AT+SRBLEDEL=1\r')
    SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)
    
    
    print "\nStep 17: Query +SRBLECFG \n"
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
    SagSendAT(aux2_com, 'AT&F\r')
    SagWaitnMatchResp(aux2_com, ['*\r\nREADY\r\n'], 2000)

#Print test result
PRINT_TEST_RESULT(test_ID, VarGlobal.statOfItem)

# -----------------------------------------------------------------------------------

print "\n----- Test Body End -----\n"

print "-----------Restore Settings---------------"

SagSendAT(uart_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(uart_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux1_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(aux1_com, ['\r\nOK\r\n'], 2000)

SagSendAT(aux2_com, 'AT+SRBTSYSTEM=0\r')
SagWaitnMatchResp(aux2_com, ['\r\nOK\r\n'], 2000)

# Close UART
SagClose(uart_com)
SagClose(aux1_com)
SagClose(aux2_com)